너는 이 저장소의 **노트 작성자(Producer)** 역할이다. 먼저 저장소 루트의 `CLAUDE.md` 를 끝까지 읽고(특히 '노트 작성 워크플로우', '출력 규칙', 'Quarto 노트 템플릿', '과목별 특이사항 > chemistry', 그리고 하단 'Codex 위임 규약'), 그 계약을 그대로 따른다. 아래는 이번 작업 브리프다.

## 작업: 화학 9장(열화학·화학에너지) 노트 작성

### 1) 입력 (녹음 위주로 정리 — 이게 1차 출처)
- `chemistry/transcript/9-26_part1_43min.txt`
- `chemistry/transcript/9-26_part2_11min.txt`
- `chemistry/transcript/9-26_part3_3min.txt`
세 파트는 같은 강의의 연속이다(파트 순서대로 시간순). 녹음일 2026-06-01.

### 2) 규격 (참조)
- `CLAUDE.md` 전체 규약.
- 보조자료 PDF `chemistry/pdf/9-26.pdf` — **반드시 4페이지부터** 참조한다(1~3페이지 해당 분량은 온라인 강의로 진행되어 이 녹음에 없음). ⚠️ GoodNotes PDF 한글은 추출 시 깨짐(함정 #6) → PDF는 **수치·화학식·영어 용어 보완**용으로만 쓰고, 한글 서술은 transcript 기준.
- 중간 **문제풀이**(엔탈피/열량계 계산)는 `chemistry/pdf/9-26_practice_problems.pdf` 의 연습문제 **9.43, 9.47, 9.49** 에 대한 것이다. 이 세 문제를 노트에 포함하되, **계산을 네가 직접 검산**해서 정확한 풀이·답을 적어라(PDF의 손글씨 스캔은 OCR이 깨져 있으니 신뢰하지 말 것). 9.47은 NH4NO3 용해가 흡열(ΔH>0)이라 **냉찜질 팩**이며 온도가 내려간다(문제 지문의 '발열/핫팩' 표현은 오타) — 물리적으로 맞게 서술.

### 3) 출력
- `chemistry/notes/2026-06-01_ch9-thermochemistry.qmd`
- frontmatter: `title`, `date: "2026-06-01"`(녹음일), `categories: [chemistry]`.
- 화학 반응식·열역학 수식은 LaTeX(`$...$`), 개념 흐름은 Mermaid 또는 callout 활용(chemistry 규칙).
- 전문 용어는 `한국어 (English)` 병기. 1파일=1노트.

### 4) 합격기준 (DoD — 보고 전 네가 자가검증)
- `quarto render chemistry/notes/2026-06-01_ch9-thermochemistry.qmd` 가 에러 0으로 통과, `_site` HTML 생성.
- frontmatter 3필드 존재, categories=chemistry.
- 녹음에 실제 나온 내용 위주, PDF에만 있고 녹음에 없는 내용은 제외(단 위 문제풀이 3개는 명시적으로 포함). 잡담·행정·필러 제외.
- 9.43/9.47/9.49 계산 결과가 단위까지 정확.

### 5) 금지
- `origin/`, `chemistry/transcript/`, `chemistry/audio/`, `**/_legacy/` 수정 금지. 전사 재실행 금지.
- 노트 '확정'(전체 quarto 리스팅 갱신)은 리뷰어 몫이니 하지 말 것. 너는 해당 1개 파일만 렌더해 검증한다.

### 6) 완료 보고
- `WORKLOG.md` **최상단**에 항목 추가: 제목·계획 체크리스트·발생한 문제(있으면)·`**상태**: 리뷰대기`.
- 마지막 메시지로 (a)생성한 파일 경로 (b)렌더 통과 여부 (c)9.43/9.47/9.49 네가 계산한 답 (d)리뷰어가 봐야 할 불확실 지점을 요약하라.
