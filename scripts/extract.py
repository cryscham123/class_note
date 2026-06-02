#!/usr/bin/env python3
"""
extract.py — .goodnotes 추출 + 과목 자동 분류 (CLAUDE.md 워크플로 1번 자동화)

origin/*.goodnotes 를 열어서:
  - 파일명 prefix 로 과목 판별 (화학- / 블록체인- / 데이터애널리틱스-)
  - 첨부파일을 매직바이트로 판별 → MP4 오디오는 <과목>/audio/, PDF 는 <과목>/pdf/
  - 오디오가 여러 개면 creation_time(없으면 zip 순서)으로 정렬해 _part1, _part2 ...
  - 처리한 .goodnotes 는 origin/done/ 으로 이동
  - 마지막에 manifest(과목·길이·녹음일 후보)를 출력 → 노트 date 규칙에 사용

알려진 함정 반영:
  #1 한글 파일명 NFD → os.listdir + unicodedata.normalize('NFC')
  #7 date 후보 = 오디오 creation_time (있을 때만; 없으면 수동 확인 필요로 표시)

사용법:
  python3 scripts/extract.py            # origin/ 의 모든 .goodnotes 처리
  python3 scripts/extract.py --dry-run  # 이동/추출 없이 분류 결과만 출력
  python3 scripts/extract.py --keep     # origin/done 으로 옮기지 않음
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, unicodedata, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = os.path.join(ROOT, "origin")
DONE = os.path.join(ORIGIN, "done")

# 파일명 prefix → 과목 폴더 (NFC 기준)
SUBJECT_BY_PREFIX = {
    "화학-": "chemistry",
    "블록체인-": "blockchain",
    "데이터애널리틱스-": "data_analytics",
}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def slugify(s: str) -> str:
    """파일명 base → 안전한 ascii-ish slug. 한글/공백/특수문자는 '-' 로."""
    s = nfc(s).strip()
    out = []
    for ch in s:
        if ch.isalnum() and ord(ch) < 128:
            out.append(ch.lower())
        elif ch in ("_",):
            out.append("_")
        else:
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-_") or "untitled"


def classify(name: str) -> str | None:
    n = nfc(name)
    for prefix, subject in SUBJECT_BY_PREFIX.items():
        if n.startswith(prefix):
            return subject
    return None


def base_after_prefix(name: str) -> str:
    n = nfc(name)
    if n.endswith(".goodnotes"):
        n = n[: -len(".goodnotes")]
    for prefix in SUBJECT_BY_PREFIX:
        if n.startswith(prefix):
            return n[len(prefix):]
    return n


def kind_of(blob: bytes) -> str | None:
    """매직바이트로 첨부 종류 판별."""
    head = blob[:16]
    if head[4:8] == b"ftyp":
        return "audio"   # MP4/M4A 컨테이너
    if head[:4] == b"%PDF":
        return "pdf"
    return None


def ffprobe(path: str) -> tuple[float | None, str | None]:
    """(duration_sec, creation_time) — 없으면 None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "quiet",
             "-show_entries", "format=duration:format_tags=creation_time",
             "-of", "json", path],
            capture_output=True, text=True, check=True,
        ).stdout
        data = json.loads(out).get("format", {})
        dur = data.get("duration")
        ct = (data.get("tags", {}) or {}).get("creation_time")
        return (float(dur) if dur else None, ct)
    except Exception:
        return (None, None)


def list_goodnotes() -> list[str]:
    if not os.path.isdir(ORIGIN):
        return []
    return sorted(
        f for f in os.listdir(ORIGIN)
        if f.endswith(".goodnotes") and os.path.isfile(os.path.join(ORIGIN, f))
    )


def process(fname: str, dry: bool, keep: bool) -> dict:
    src = os.path.join(ORIGIN, fname)
    subject = classify(fname)
    rec = {"source": nfc(fname), "subject": subject, "audio": [], "pdf": [], "date_hint": None}
    if subject is None:
        rec["error"] = "과목 prefix 판별 실패 (화학-/블록체인-/데이터애널리틱스- 아님)"
        return rec

    base = slugify(base_after_prefix(fname))
    z = zipfile.ZipFile(src)

    # 첨부 수집 + 종류 판별
    audios, pdfs = [], []
    for n in z.namelist():
        if not n.startswith("attachments/"):
            continue
        blob = z.read(n)
        k = kind_of(blob)
        if k == "audio":
            audios.append((n, blob))
        elif k == "pdf":
            pdfs.append((n, blob))

    audio_dir = os.path.join(ROOT, subject, "audio")
    pdf_dir = os.path.join(ROOT, subject, "pdf")

    # 오디오: 길이/녹음일 메타를 먼저 뽑고 creation_time 순으로 정렬
    tmp_meta = []
    for idx, (n, blob) in enumerate(audios):
        tmp = os.path.join("/tmp", f"_gn_{base}_{idx}.m4a")
        with open(tmp, "wb") as fh:
            fh.write(blob)
        dur, ct = ffprobe(tmp)
        tmp_meta.append({"zip": n, "blob": blob, "dur": dur, "ct": ct, "tmp": tmp})
    tmp_meta.sort(key=lambda m: (m["ct"] or "", m["zip"]))

    multi = len(tmp_meta) > 1
    for i, m in enumerate(tmp_meta, 1):
        mins = round(m["dur"] / 60) if m["dur"] else 0
        part = f"_part{i}" if multi else ""
        out_name = f"{base}{part}_{mins}min.m4a"
        dest = os.path.join(audio_dir, out_name)
        if not dry:
            os.makedirs(audio_dir, exist_ok=True)
            shutil.move(m["tmp"], dest)
        else:
            os.remove(m["tmp"])
        rec["audio"].append({"file": f"{subject}/audio/{out_name}",
                             "min": mins, "creation_time": m["ct"]})
        if m["ct"] and not rec["date_hint"]:
            rec["date_hint"] = m["ct"][:10]

    for i, (n, blob) in enumerate(pdfs, 1):
        suffix = f"_{i}" if len(pdfs) > 1 else ""
        out_name = f"{base}{suffix}.pdf"
        dest = os.path.join(pdf_dir, out_name)
        if not dry:
            os.makedirs(pdf_dir, exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(blob)
        rec["pdf"].append(f"{subject}/pdf/{out_name}")

    z.close()
    if not dry and not keep:
        os.makedirs(DONE, exist_ok=True)
        shutil.move(src, os.path.join(DONE, fname))
        rec["moved_to_done"] = True
    return rec


def main():
    ap = argparse.ArgumentParser(description="goodnotes 추출 + 과목 자동 분류")
    ap.add_argument("--dry-run", action="store_true", help="이동/추출 없이 분류 결과만")
    ap.add_argument("--keep", action="store_true", help="origin/done 으로 옮기지 않음")
    args = ap.parse_args()

    files = list_goodnotes()
    if not files:
        print("origin/ 에 처리할 .goodnotes 가 없습니다.")
        return
    print(f"== {len(files)}개 .goodnotes 처리 {'(dry-run)' if args.dry_run else ''} ==\n")
    results = [process(f, args.dry_run, args.keep) for f in files]

    for r in results:
        print(f"[{r.get('subject') or '???'}] {r['source']}")
        if r.get("error"):
            print(f"   ⚠️  {r['error']}")
            continue
        for a in r["audio"]:
            ct = a["creation_time"] or "creation_time 없음 → 녹음일 수동 확인"
            print(f"   🎧 {a['file']}  ({a['min']}min, {ct})")
        for p in r["pdf"]:
            print(f"   📄 {p}")
        if r.get("date_hint"):
            print(f"   📅 date 후보(녹음일): {r['date_hint']}")
        print()

    # 다음 단계용 manifest 저장
    man = os.path.join(ROOT, "scripts", "last_extract.json")
    with open(man, "w") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)
    print(f"manifest → {man}")
    if not args.dry_run:
        print("다음 단계:  python3 scripts/stt.py --all   (transcript 없는 오디오 전사)")


if __name__ == "__main__":
    main()
