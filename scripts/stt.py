#!/usr/bin/env python3
"""
stt.py — 음성/영상 → 텍스트 (Whisper) 자동 전사 (CLAUDE.md 워크플로 2번 자동화)

CLAUDE.md '알려진 함정' 을 코드로 박아 둔 전사기:
  #2 API 키: env OPENAI_API_KEY 무효면 openclaw.json 의
     skills.entries.openai-whisper-api.apiKey 로 폴백
  #3 길이 제한: <23분(1400초) → gpt-4o-transcribe, 그 이상 → whisper-1
  #3 25MB 초과 → ffmpeg 으로 분할 후 순서대로 전사 → 합치기
  #4 환각 루프: 전사 후 unique/words 비율·최대 연속반복 검사,
     의심되면 다른 모델로 1회 자동 재전사
  #5 긴 전사는 nohup 백그라운드 권장 (아래 '대량 실행' 참고)

사용법:
  python3 scripts/stt.py <audio파일> [--out transcript.txt]
  python3 scripts/stt.py --all                 # 모든 과목, transcript 없는 오디오 전부
  python3 scripts/stt.py --subject blockchain  # 특정 과목만
  python3 scripts/stt.py <file> --force         # 기존 transcript 무시하고 재전사

대량 실행(함정 #5 — foreground 장시간 대기 금지):
  nohup python3 scripts/stt.py --all > /tmp/stt.log 2>&1 &
  tail -f /tmp/stt.log
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECTS = ["blockchain", "data_analytics", "chemistry"]

GPT4O = "gpt-4o-transcribe"
WHISPER = "whisper-1"
LEN_LIMIT_SEC = 1400      # 함정 #3: gpt-4o ~23분
SIZE_LIMIT_MB = 25        # API 업로드 한도
SPLIT_SEC = 1200          # 분할 시 세그먼트 길이(20분)
HALLUC_RATIO = 0.20       # 함정 #4: unique/words 이 값 미만이면 환각 의심
# 연속반복(run)은 실제 강의에도 흔함("이거 이거 이거", 연습 반복 지시 등).
# 극단적 반복 + 어휘 다양성도 낮을 때만 환각으로 본다(오판 방지).
HALLUC_RUN = 200
HALLUC_RUN_RATIO = 0.35


# ---------- API 키 (함정 #2) ----------
def resolve_api_key() -> str:
    env = os.environ.get("OPENAI_API_KEY", "").strip()
    # env 키가 있어도 과거 401 이력 → openclaw.json 을 우선 신뢰
    cfg_path = os.environ.get("OPENCLAW_CONFIG_PATH",
                              os.path.expanduser("~/.openclaw/openclaw.json"))
    try:
        cfg = json.load(open(cfg_path))
        key = (cfg.get("skills", {}).get("entries", {})
               .get("openai-whisper-api", {}).get("apiKey", "")).strip()
        if key:
            return key
    except Exception:
        pass
    if env:
        return env
    sys.exit("API 키를 찾을 수 없습니다 (env OPENAI_API_KEY 또는 openclaw.json).")


# ---------- 오디오 메타 ----------
def duration_sec(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def pick_model(dur: float) -> str:
    return GPT4O if dur < LEN_LIMIT_SEC else WHISPER


def other_model(model: str) -> str:
    return WHISPER if model == GPT4O else GPT4O


# ---------- 전사 호출 ----------
def transcribe_one(path: str, model: str, api_key: str) -> str:
    """단일 파일(<=25MB, 모델 길이제한 내) 전사 → 텍스트."""
    base = os.path.splitext(os.path.basename(path))[0]
    # gpt-4o 계열은 response_format=json 만 허용, whisper-1 은 text 가능
    fmt = "json" if model.startswith("gpt-4o") else "text"
    cmd = [
        "curl", "-sS", "https://api.openai.com/v1/audio/transcriptions",
        "-H", f"Authorization: Bearer {api_key}",
        "-F", f"file=@{path}",
        "-F", f"model={model}",
        "-F", f"response_format={fmt}",
        "-F", "language=ko",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"curl 실패: {res.stderr[:300]}")
    raw = res.stdout
    if fmt == "json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError(f"응답 파싱 실패: {raw[:300]}")
        if "error" in data:
            raise RuntimeError(f"API 오류: {data['error'].get('message', raw[:300])}")
        return data.get("text", "")
    if raw.lstrip().startswith("{") and '"error"' in raw:
        raise RuntimeError(f"API 오류: {raw[:300]}")
    return raw


def split_audio(path: str) -> list[str]:
    """25MB 초과(함정 #3) → ffmpeg 으로 SPLIT_SEC 단위 분할. 세그먼트 경로 리스트."""
    tmpdir = tempfile.mkdtemp(prefix="stt_split_")
    pat = os.path.join(tmpdir, "seg_%03d.m4a")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "segment",
         "-segment_time", str(SPLIT_SEC), "-c", "copy", pat],
        check=True)
    return sorted(os.path.join(tmpdir, f) for f in os.listdir(tmpdir))


# ---------- 환각 검사 (함정 #4) ----------
def hallucination_score(text: str) -> tuple[float, int]:
    words = re.findall(r"\S+", text)
    if len(words) < 30:
        return (1.0, 0)
    ratio = len(set(words)) / len(words)
    # 최대 연속 동일 토큰 길이
    run = best = 1
    for i in range(1, len(words)):
        run = run + 1 if words[i] == words[i - 1] else 1
        best = max(best, run)
    return (ratio, best)


def looks_hallucinated(text: str) -> bool:
    ratio, run = hallucination_score(text)
    if ratio < HALLUC_RATIO:
        return True
    # 극단적 연속반복은 어휘 다양성까지 낮을 때만 환각으로 간주
    return run >= HALLUC_RUN and ratio < HALLUC_RUN_RATIO


def transcribe_file(path: str, api_key: str, model: str | None = None) -> str:
    """길이/용량/환각을 모두 처리하는 메인 전사 루틴."""
    dur = duration_sec(path)
    chosen = model or pick_model(dur)

    # 25MB 초과 → 분할 전사 후 합치기
    if size_mb(path) > SIZE_LIMIT_MB:
        print(f"   ↳ {size_mb(path):.1f}MB > 25MB, ffmpeg 분할", flush=True)
        segs = split_audio(path)
        parts = []
        for i, seg in enumerate(segs, 1):
            seg_dur = duration_sec(seg)
            seg_model = pick_model(seg_dur)
            print(f"     · seg {i}/{len(segs)} [{seg_model}]", flush=True)
            txt = transcribe_one(seg, seg_model, api_key)
            txt = retry_if_hallucinated(seg, seg_dur, seg_model, txt, api_key, indent="       ")
            parts.append(txt)
        return "\n".join(parts)

    print(f"   ↳ {dur/60:.0f}min [{chosen}]", flush=True)
    txt = transcribe_one(path, chosen, api_key)
    return retry_if_hallucinated(path, dur, chosen, txt, api_key, indent="   ")


def retry_if_hallucinated(path: str, dur: float, model: str, txt: str,
                          api_key: str, indent: str = "   ") -> str:
    """환각 의심 시 다른 모델로 1회 재전사. 단:
       - 더 나쁘거나 실패하면 원본을 유지(데이터 손실 방지).
       - 폴백 모델이 길이 제한을 못 넘기면(gpt-4o 23분 초과) 재전사 생략."""
    if not looks_hallucinated(txt):
        return txt
    ratio, run = hallucination_score(txt)
    alt = other_model(model)
    # 함정 #3: gpt-4o 는 23분 초과 처리 불가 → 폴백 무의미, 원본 유지
    if alt == GPT4O and dur >= LEN_LIMIT_SEC:
        print(f"{indent}⚠️ 환각 의심(ratio={ratio:.2f}, run={run}) "
              f"이지만 길이상 {alt} 재전사 불가 → 원본 유지(수동 확인 권장)", flush=True)
        return txt
    print(f"{indent}⚠️ 환각 의심(ratio={ratio:.2f}, run={run}) → {alt} 재전사", flush=True)
    try:
        alt_txt = transcribe_one(path, alt, api_key)
    except Exception as e:
        print(f"{indent}   재전사 실패({str(e)[:80]}) → 원본 유지", flush=True)
        return txt
    # 어휘 다양성이 더 높은(=환각 적은) 쪽을 채택
    if hallucination_score(alt_txt)[0] > ratio:
        return alt_txt
    print(f"{indent}   재전사도 개선 없음 → 원본 유지(수동 확인 권장)", flush=True)
    return txt


# ---------- 대상 수집 ----------
def audio_files(subjects: list[str]) -> list[str]:
    found = []
    for s in subjects:
        ad = os.path.join(ROOT, s, "audio")
        if not os.path.isdir(ad):
            continue
        for f in sorted(os.listdir(ad)):
            if f.lower().endswith((".m4a", ".mp4", ".mp3", ".wav", ".webm")):
                found.append(os.path.join(ad, f))
    return found


def transcript_path(audio: str) -> str:
    subject_dir = os.path.dirname(os.path.dirname(audio))
    base = os.path.splitext(os.path.basename(audio))[0]
    return os.path.join(subject_dir, "transcript", base + ".txt")


def run_one(audio: str, api_key: str, force: bool):
    out = transcript_path(audio)
    rel = os.path.relpath(audio, ROOT)
    if os.path.exists(out) and not force:
        print(f"⏭  {rel}  (transcript 이미 있음, --force 로 재전사)")
        return
    print(f"🎧 {rel}")
    try:
        txt = transcribe_file(audio, api_key)
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write(txt.strip() + "\n")
    ratio, run = hallucination_score(txt)
    print(f"   ✅ {os.path.relpath(out, ROOT)}  (ratio={ratio:.2f})")


def main():
    ap = argparse.ArgumentParser(description="Whisper 자동 전사 (모델선택·분할·환각검사 내장)")
    ap.add_argument("audio", nargs="?", help="오디오 파일 경로")
    ap.add_argument("--all", action="store_true", help="모든 과목의 미전사 오디오")
    ap.add_argument("--subject", choices=SUBJECTS, help="특정 과목만")
    ap.add_argument("--out", help="단일 파일 전사 결과 경로")
    ap.add_argument("--force", action="store_true", help="기존 transcript 무시")
    ap.add_argument("--model", choices=[GPT4O, WHISPER], help="모델 강제 지정")
    args = ap.parse_args()

    api_key = resolve_api_key()

    if args.audio:
        out = args.out or transcript_path(args.audio)
        print(f"🎧 {args.audio}")
        txt = transcribe_file(args.audio, api_key, model=args.model)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w") as fh:
            fh.write(txt.strip() + "\n")
        ratio, run = hallucination_score(txt)
        print(f"   ✅ {out}  (ratio={ratio:.2f}, max-run={run})")
        return

    subjects = [args.subject] if args.subject else SUBJECTS
    targets = audio_files(subjects)
    if not targets:
        print("전사할 오디오가 없습니다.")
        return
    print(f"== {len(targets)}개 오디오 검토 ==")
    for a in targets:
        run_one(a, api_key, args.force)
    print("\n다음 단계: transcript 교정 + Quarto 노트(.qmd) 작성은 판단이 필요한 단계라 "
          "사람/LLM 이 직접 (CLAUDE.md 워크플로 3~4).")


if __name__ == "__main__":
    main()
