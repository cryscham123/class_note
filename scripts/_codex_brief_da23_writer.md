너는 이 저장소의 **노트 작성자(Producer, ①-A)** 역할이다. 먼저 저장소 루트의 `CLAUDE.md` 를 끝까지 읽고(특히 '노트 작성 워크플로우', '출력 규칙', 'Quarto 노트 템플릿', '과목별 특이사항 > data_analytics', 하단 'Codex 위임 규약'), 그 계약을 그대로 따른다. 아래는 이번 작업 브리프다.

## 작업: 데이터애널리틱스 23강(추천 시스템 / Recommender Systems) 노트 작성

### 1) 입력 (녹음 위주로 정리 — 1차 출처)
- `data_analytics/transcript/23_recommender_systems_part1_18min.txt`
- `data_analytics/transcript/23_recommender_systems_part2_43min.txt`
두 파트는 같은 강의의 연속(파트 순서 = 시간순). 녹음일 **2026-05-26**.
보조: `data_analytics/pdf/23_recommender_systems.pdf` — 용어/수식/R코드/수치 보완용으로만. GoodNotes PDF 한글은 추출 시 깨질 수 있으니(함정 #6) 한글 서술은 transcript 기준.

### 2) 규격 (참조)
- `CLAUDE.md` 전체 규약. data_analytics 규칙: 통계/수식은 LaTeX(`$...$`), 코드 예시는 **R**.
- 전문 용어는 `한국어 (English)` 병기. 1파일=1노트. 부연/추가설명은 본문과 구분되는 callout 블록으로.
- 추천시스템 핵심 개념을 빠짐없이: 콘텐츠 기반 vs 협업 필터링(user-based/item-based), 유사도(코사인/피어슨), 행렬분해(matrix factorization, latent factor), 평가지표, cold-start 등 **강의에서 실제 다룬 범위**로. 녹음에 없는 내용 추가 금지.

### 3) 출력
- `data_analytics/notes/2026-05-26_23-recommender-systems.qmd`
- frontmatter: `title`, `date: "2026-05-26"`(녹음일), `categories: [data_analytics]`.
- Mermaid 다이어그램 쓸 경우 **펜스는 반드시 ` ```{mermaid} `(중괄호 O)** — 함정 #9. ` ```mermaid `(중괄호 X)는 렌더 안 됨.

### 4) 합격기준 (DoD — 보고 전 자가검증)
- `quarto render data_analytics/notes/2026-05-26_23-recommender-systems.qmd` 가 에러 0으로 통과, `_site` HTML 생성.
- mermaid 썼다면 생성 HTML에 `<pre class="mermaid">` 존재 확인(중괄호 펜스 검증).
- frontmatter 3필드 존재, categories=data_analytics.
- 녹음에 실제 나온 내용 위주, PDF에만 있고 녹음에 없는 내용 제외. 잡담·행정·필러(서두 잡담 등) 제외.

### 5) 금지
- `origin/`, `data_analytics/transcript/`, `data_analytics/audio/`, `**/_legacy/`, `**/notes/_research/` 수정 금지. 전사 재실행 금지.
- 노트 '확정'(전체 quarto 리스팅 갱신)은 리뷰어 몫이니 하지 말 것. 너는 해당 1개 파일만 렌더해 검증한다.

### 6) 완료 보고
- `WORKLOG.md` 해당 항목(23강)에 작성자 결과를 한 줄로 추가하거나, 없으면 최상단에 짧게 기록하고 `상태: 리뷰대기`.
- 마지막 메시지로 (a)생성한 파일 경로 (b)렌더 통과 여부 (c)다룬 소주제 목록 (d)리뷰어가 봐야 할 불확실/모호 지점을 요약하라.
