# 2026-1 강의 노트 프로젝트

## 과목
- **blockchain** — 블록체인
- **data_analytics** — 데이터 분석
- **chemistry** — 화학

## 폴더 구조
```
<과목>/
├── audio/       # 원본 녹음 파일
├── pdf/         # 수업 자료 PDF
├── transcript/  # Whisper STT 원본 텍스트 (교정 전)
├── notes/       # 최종 노트 (.qmd 파일)
└── summary/     # 해당 과목 전체 요약 (.qmd)
```

## 작업 기록 (필수)

작업 **시작 전**에 `WORKLOG.md` 최상단에 계획(체크리스트)을 먼저 작성한다. 그 다음:

- **step 하나가 끝날 때마다 즉시** 해당 항목을 `- [x]`로 체크한다 (나중에 몰아서 X).
- **오류·이슈가 발생하는 즉시** "문제/이슈"에 기록한다 (원인 + 해결 여부). 한 작업이 끝난 뒤가 아니라 그 순간 기록.

형식은 `WORKLOG.md` 상단 템플릿 참조.

### ⚠️ 알려진 함정 — 작업 전 반드시 확인 (과거 오류에서 도출)

새 작업을 시작하기 전에 이 목록을 먼저 읽고 같은 실수를 반복하지 않는다. 새 오류가 생기면 WORKLOG에 기록 후 **여기에도 한 줄 요약을 추가**한다.

1. **한글 파일명은 NFD 인코딩** (macOS GoodNotes). shell glob/`grep 화학`/`ls 데이터*` 매칭 **실패**함. → 반드시 Python `os.listdir()` + `unicodedata.normalize('NFC', f)` 로 탐색·매칭.
2. **STT API 키**: 환경변수 `OPENAI_API_KEY`는 만료/무효(401). → `openclaw.json` 의 `skills.entries.openai-whisper-api.apiKey` 사용.
3. **gpt-4o-transcribe는 오디오 1400초(~23분) 길이 제한**(초과 시 400). → **23분 초과 녹음은 whisper-1**(25MB 한도, 길이 무관) 사용. 25MB 초과면 ffmpeg 분할.
4. **whisper-1은 조용/반복 구간에서 환각 루프**(같은 문장 수백 회 반복) 가능. **gpt-4o-transcribe도 마찬가지**. → 전사 후 `unique/words` 비율로 검사(0.2 미만 또는 극단적 반복이면 의심), 발생 시 **다른 모델로 재전사**. 짧은(<23분) 파일은 gpt-4o 우선.
   - ⚠️ **부분 잘림/구반복 사각지대**(과거 20강 NN·일부 화학에서 발생): 후반부만 `. . .` 점-런 또는 "같은 구 반복"(예: "KS는 KS는" ×38)으로 끊겨도 **전역 ratio·단일토큰 run 검사를 통과**함. → stt.py 검출기 보강됨: **꼬리 윈도우 unique 비율**(`TAIL_RATIO`)과 **구(n-gram) 반복 run**(`PHRASE_RUN`)을 추가로 검사, 긴 파일은 통째 재시도 대신 **분할+gpt-4o 자동 재전사**. 기존 transcript 일괄 점검은 `python3 scripts/stt.py --scan`. 노트 작성 전 의심 파일은 이 스캔으로 먼저 확인.
5. **긴 전사를 foreground 명령으로 오래 기다리지 말 것**: harness가 장시간 대기 명령을 137로 kill하며, 그때 같은 셸의 백그라운드 잡도 함께 죽을 수 있음. → 전사는 `nohup ... &` 로 띄우고, 짧은 폴링으로 상태만 확인. 완료 파일은 개별 검증.
6. **GoodNotes PDF의 한글은 추출 시 깨짐(mojibake)** — 폰트 인코딩 때문. R 코드·영어·수식·숫자는 정상 추출됨. → 노트는 **녹음본(transcript) 위주**로 쓰고 PDF는 코드/용어/수치 보완용으로만.
7. **노트 `date`·파일명은 강의 녹음일**(audio `creation_time`) 기준. 처리일 아님. 파일명은 `YYYY-MM-DD_<강의번호>-<topic>.qmd`.
8. **Quarto는 여러 .qmd 동시 렌더 시 경로 꼬임** 발생. → 검증은 `quarto render <파일>` 로 **하나씩**, 또는 전체는 `quarto render`(인자 없이).
9. **Mermaid 다이어그램 펜스는 반드시 ` ```{mermaid} ` (중괄호 O)**. ` ```mermaid `(중괄호 X)로 쓰면 렌더 안 되고 `graph LR ...` 소스가 raw 코드블록으로 그대로 출력됨. → 노트 작성/검수 시 mermaid 블록은 중괄호 형태인지 확인. (`quarto render` 는 둘 다 에러 없이 통과하므로 렌더 성공만으로는 못 걸러냄 — HTML에 `<pre class="mermaid">` 있는지로 확인.)

## 자동화 스크립트 (`scripts/`)

워크플로 1~2번(원본 추출·STT)은 스크립트로 자동화됨. 함정 #1~#4·#7 이 코드에 반영되어 있으니 **수작업 대신 먼저 사용**한다.

- `python3 scripts/extract.py` — `origin/*.goodnotes` 추출 + 과목 자동분류(prefix) + 매직바이트로 audio/pdf 분리 + creation_time 으로 녹음일 후보 산출 → `origin/done/` 이동. `--dry-run` 으로 미리보기.
- `python3 scripts/stt.py --all` — 미전사 오디오 전부 전사. 길이로 모델선택(gpt-4o↔whisper-1), 25MB 초과 분할, 환각 검사 후 자동 재전사, API 키는 openclaw.json 폴백. 긴 작업은 `nohup ... &` 로.
  - 환각 검사 = 전역 ratio + 단일토큰 run + **꼬리 윈도우 비율** + **구(n-gram) 반복 run**. 길어서 통째 폴백 불가한 파일은 **분할 후 gpt-4o 재전사**로 자동 복구.
- `python3 scripts/stt.py --scan` — 기존 transcript 를 환각/부분잘림 관점에서 **일괄 점검(읽기전용)**, 의심 파일과 재전사 명령을 출력. 새 노트 작업 전/후 점검용.
- 남는 수작업 = **교정 + .qmd 노트 작성(3~4번)**: 판단이 필요한 단계라 LLM 이 직접. 스크립트가 깔아준 transcript/녹음일을 입력으로 사용.
- ⚠️ chemistry slug 는 한글이 빠져(예: `7-26`) 다소 불명확 → 노트 .qmd 명명 시 PDF/내용 보고 topic 보정.

## 노트 작성 워크플로우

1. **원본 추출** — `origin/` 의 `.goodnotes` 파일에서 자동 추출 (`scripts/extract.py`)
   - MP4 → `<과목>/audio/`
   - PDF → `<과목>/pdf/`
   - 파일명 규칙: `화학-`, `블록체인-`, `데이터애널리틱스-` prefix로 과목 판별
   - 과목 판별 우선순위: 파일명 prefix → PDF 내용 확인
   - 작업 완료 후 해당 `.goodnotes` 파일을 `origin/done/` 으로 이동
   - ⚠️ 한글 파일명 NFC/NFD 불일치 주의 (macOS→Linux 복사 시 발생)
     glob/직접 매칭 대신 `os.listdir()` 또는 `find` 와일드카드로 파일 탐색할 것
     Python unicodedata.normalize('NFC', filename) 으로 정규화 후 비교
2. **STT** — 음성 파일을 Whisper로 텍스트 변환 → `transcript/` 저장
   - 파일이 25MB 초과 시 ffmpeg으로 자동 분할 후 순서대로 전사, 결과 합치기
2. **교정** — 오인식 수정, 필러 제거, PDF 자료 기반 용어 보완
3. **노트 생성** — 아래 Quarto 형식으로 `notes/` 저장
4. **요약** — 요청 시 `summary/` 저장

## 출력 규칙

- **언어**: 한국어 (전문 용어는 영어 병기)
- **형식**: Quarto Markdown (`.qmd`)
- **요약**: 내용 전개 후 마지막에만
- **포함**: 웹 검색 부연 설명 (출처 명시), Mermaid 다이어그램
- **제외**: 수업과 무관한 잡담, 행정 공지, 반복 필러
- **기준**: 녹음본 위주로 정리. PDF는 용어 보완/확인 용도로만 참조. PDF에만 있고 녹음에 없는 내용은 제외

---

## Quarto 노트 템플릿

파일명: `YYYY-MM-DD_주제.qmd`

> **날짜 규칙**: `date` 와 파일명 prefix는 **강의 녹음일**(오디오 attachment의 `creation_time` 기준)을 사용한다. 처리일이 아님.

````qmd
---
title: "강의 제목"
date: "YYYY-MM-DD"
categories: [blockchain | data_analytics | chemistry]
---

::: {.key-questions}
- 이 강의에서 답해야 할 핵심 질문 1
- 핵심 질문 2
:::

## 소주제 1

::: {.column-margin}
**키워드**

관련 질문이나
핵심 개념 한 줄
:::

내용 서술. 전문 용어는 **한국어 (English)** 형식으로.

::: {.callout-note title="부연 설명"}
웹 검색으로 찾은 추가 설명. 출처: [출처명](URL)
:::

::: {.callout-tip title="PDF 자료 연결"}
수업 자료 PDF의 관련 내용 요약.
:::

```{mermaid}
graph TD
    A[개념A] --> B[개념B]
    B --> C[개념C]
```

## 소주제 2

...

## 개념 연결

이전 강의 또는 타 과목 개념과의 연결.

::: {.lecture-summary}
- 핵심 포인트 1
- 핵심 포인트 2
- 핵심 포인트 3
:::
````

---

## 과목별 특이사항

### blockchain
- **녹음본 위주로 정리** — 교수님이 실제로 다룬 내용만 포함. PDF는 용어 보완/확인 용도로만 참조
- PDF에만 있고 녹음에 없는 내용은 노트에서 제외
- 합의 알고리즘, 암호화 개념 등 Mermaid sequence/flowchart 적극 활용
- 코드 예시는 Python 또는 Solidity

### data_analytics
- 통계/수식은 LaTeX (`$...$`) 사용
- 코드 예시는 R

### chemistry
- 화학 반응식은 LaTeX (`$...$`) 사용
- 분자 구조/반응 메커니즘은 Mermaid 또는 설명형 다이어그램

---

## Codex 위임 규약 (Review-Gate)

노트 생성(워크플로 3~4번)은 **리뷰 게이트 + 듀얼 에이전트** 방식으로 codex에 위임한다. 두 codex(작성자·리서처)가 **병렬**로 돌고, 리뷰어가 둘을 교차검증해 머지한다. 각 codex 는 이 파일만 읽고 자기 레인을 파악한다.

### 역할 (각 역할 = 책임 · 쓰기권한 · 핸드오프)

**①-A codex — 작성자(Producer)**
- 책임: `transcript/` 기반으로 `.qmd` 초안 작성 → `quarto render <file>` 자가검증 통과까지.
- 쓰기권한: `<과목>/notes/`, `<과목>/summary/` 만. **읽기**: transcript·pdf.
- ❌ 금지: `origin/`·`transcript/`·`audio/`·`_legacy/` 수정, 전사 재실행, 노트 **확정**(리스팅 갱신은 리뷰어 몫).
- 핸드오프: 초안+렌더 통과 시 WORKLOG에 `상태: 리뷰대기` 로 기록하고 멈춘다.

**①-B codex — 리서처(Researcher)** *(작성자와 병렬)*
- 책임: 해당 노트 토픽들을 web 검색으로 조사해 **fact check 근거 + 부연설명 후보 + 공식 이미지**를 출처와 함께 정리한 리서치 노트 산출.
- 소스 제한: **공신력 있는 official 자료만** — 교과서, 학회/표준기구, 정부·대학(.gov/.edu) 공식 문서, 1차 논문. 블로그·위키 짜깁기·콘텐츠팜 ❌.
- 쓰기권한: `<과목>/notes/_research/<노트slug>.md` (임시 리서치 노트) 만. **읽기**: transcript·pdf.
- ❌ 금지: `.qmd` 본 노트 직접 수정(머지는 리뷰어 몫), official 아닌 출처 인용, 출처·이미지 라이선스 표기 누락.
- 핸드오프: 리서치 노트에 각 항목별 [출처 URL] 명시하고 WORKLOG에 `리서치: 완료` 기록 후 멈춘다.

**② Claude(메인) — 리뷰어(Gate)**
- 책임: ①-A 초안 ↔ ①-B 리서치 노트를 **교차검증** — 사실 충돌은 출처와 함께 플래그(임의 머지 금지), 설명 부족분에 official 부연·이미지를 출처 표기해 머지. 이후 아래 DoD 자동검증 + 품질 샘플검수. 통과 시 확정(전체 `quarto render`로 리스팅 갱신), 미흡 시 `상태: 수정요청` + 구체 피드백으로 반려.
- 핸드오프: date 애매(멀티데이 녹음)·과목 편집 판단, 해소 안 되는 사실 충돌은 오너에게 에스컬레이션.

**③ 오너(사람) — 최종승인**
- 책임: date 확정, 과목 특이 편집 결정, 최종 sign-off. 리뷰어가 막혔을 때만 호출.

### 상태머신 (WORKLOG `상태:` 필드)
`draft(작성) ∥ 리서치 → (둘 다 완료) → 리뷰대기 → 교차검증·머지 → 승인`, 반려 시 `수정요청 → (codex 재작업) → 리뷰대기`.
- 작성(①-A)과 리서치(①-B)는 **병렬**. 둘 다 끝나야 리뷰어가 리뷰대기를 집는다.
- 각 화살표를 당기는 주체: 작성=codex-A, 리서치=codex-B, 교차검증·머지·리뷰대기/승인/수정요청 전이=리뷰어, date·편집·사실충돌 확정=오너.

### 작업 브리프 6칸 (codex 에 위임할 때 항상 채운다)
1. **입력**: 대상 transcript/pdf 정확한 경로
2. **규격**: 본 CLAUDE.md '노트 작성 워크플로우'·'출력 규칙'·'Quarto 노트 템플릿'·해당 '과목별 특이사항'
3. **출력**: `<과목>/notes/YYYY-MM-DD_<주제>.qmd` (date·파일명 = 오디오 creation_time 기준 녹음일)
4. **합격기준(DoD)**: 아래 체크리스트 전부 통과
5. **금지**: 위 '쓰기권한' 의 ❌ 항목
6. **완료보고**: WORKLOG 최상단에 계획·결과·`상태: 리뷰대기` 기록

리서처(①-B)에 위임할 때도 같은 6칸을 채우되 — **출력**=`<과목>/notes/_research/<slug>.md`, **규격**=official 소스 제한·항목별 출처 표기, **완료보고**=`리서치: 완료`. 작성자와 동시에 띄운다.

### DoD 체크리스트 (codex 자가검증 → 리뷰어 재검증)
- [ ] `quarto render <file>` 단일 렌더 성공(에러 0), `_site` HTML 생성
- [ ] frontmatter `title`/`date`/`categories` 존재, `categories` 는 blockchain|data_analytics|chemistry 중 하나
- [ ] `date` 와 파일명 prefix = 오디오 creation_time 녹음일(처리일 아님). 멀티데이면 본체(가장 긴 part) 기준 + 리뷰어 확인 플래그
- [ ] 녹음본(transcript) 위주 서술, PDF에만 있고 녹음에 없는 내용 제외, 잡담·행정·필러 제외
- [ ] 전문용어 `한국어 (English)` 병기, 과목별 수식/코드 규칙(LaTeX·R·Solidity 등) 준수
- [ ] 웹검색 부연은 출처 명시, 1파일=1노트 원칙
- [ ] 부연·이미지는 **official 출처만**(교과서/학회/gov·edu/1차논문), 각 항목 [출처 URL]·이미지 라이선스 표기
- [ ] transcript ↔ 리서치노트 **사실 충돌은 머지하지 말고 출처와 함께 플래그**(오너 확정 대상)
- [ ] 부연설명은 본문과 구분되는 블록(`::: {.callout-note}` 등)에 분리, 강의내용 vs 추가내용 식별 가능
- [ ] transcript ratio<0.2(환각 의심) 구간은 노트에 반영하지 말고 WORKLOG에 표시
