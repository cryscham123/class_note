너는 이 저장소의 **리서처(Researcher, ①-B)** 역할이다. 먼저 저장소 루트의 `CLAUDE.md` 를 끝까지 읽고(특히 하단 'Codex 위임 규약 > ①-B codex 리서처' 와 'DoD 체크리스트'), 그 계약을 그대로 따른다. 너는 본 `.qmd` 노트를 **직접 수정하지 않는다**. 리서치 노트만 산출한다.

## 작업: 데이터애널리틱스 23강(추천 시스템 / Recommender Systems) 리서치

### 1) 맥락 입력 (토픽 파악용 — 읽기 전용)
- `data_analytics/transcript/23_recommender_systems_part1_18min.txt`
- `data_analytics/transcript/23_recommender_systems_part2_43min.txt`
- `data_analytics/pdf/23_recommender_systems.pdf`
이 강의가 다루는 토픽을 먼저 파악한 뒤, 그 토픽들에 대해 web 검색으로 **fact check 근거 + 부연설명 후보 + 공식 이미지**를 출처와 함께 정리한다.

### 2) 소스 제한 (엄격)
- **공신력 있는 official 자료만**: 표준 교과서(예: ISLR/ESL, Aggarwal "Recommender Systems: The Textbook", Ricci et al. Handbook), 학회/표준기구, 대학 강의자료(.edu), 1차 논문(예: Koren et al. 2009 "Matrix Factorization Techniques for Recommender Systems", IEEE Computer).
- ❌ 개인 블로그, Medium, 위키 짜깁기, 콘텐츠팜 인용 금지.
- 각 항목마다 **[출처: 제목, URL]** 명시. 이미지 가져오면 **라이선스/출처** 표기 필수.

### 3) 리서치 항목 (강의 토픽 기준, 실제 다룬 것 위주)
- 콘텐츠 기반 필터링 vs 협업 필터링 정의·차이
- 사용자기반(user-based) / 아이템기반(item-based) 협업 필터링, 유사도(코사인·피어슨 상관) 수식
- 행렬분해(matrix factorization / latent factor model) — 수식·직관, SVD와의 관계
- 평가지표(RMSE/MAE, precision@k 등), cold-start 문제, sparsity
- 강의 서술과 **사실 충돌 가능성** 있는 지점(예: 용어 혼용, 수식 부호/정규화)을 체크해 플래그

### 4) 출력
- `data_analytics/notes/_research/23-recommender-systems.md` (디렉터리 없으면 생성)
- 항목별: 「강의에서의 서술 → official 근거 → (충돌 시) 플래그」 구조로. 본 노트에 바로 머지 가능한 부연설명 후보는 callout 문안 형태로 적어두면 좋다.

### 5) 금지
- `.qmd` 본 노트, `origin/`, `transcript/`, `audio/`, `_legacy/` 수정 금지. official 아닌 출처 인용 금지. 출처·이미지 라이선스 표기 누락 금지.

### 6) 완료 보고
- `WORKLOG.md` 23강 항목에 `리서치: 완료` 한 줄 기록.
- 마지막 메시지로 (a)리서치 노트 경로 (b)핵심 fact-check 결과 (c)강의와 충돌하는 지점(있으면) 을 요약하라.
