# 작업 로그 (WORKLOG)

각 작업은 **시작 전 계획 작성 → 진행하며 완료 체크 → 문제/이슈 기록** 순서로 남긴다.
최신 작업을 위에 추가(최신순).

형식:
```
## YYYY-MM-DD HH:MM — <작업 제목>
**상태**: 진행중 | 완료 | 보류

### 계획
- [ ] 단계 1
- [ ] 단계 2
- [ ] 단계 3

### 문제 / 이슈
- (발생한 문제, 원인, 해결 여부. 없으면 "없음")

### 비고
- (남은 작업 / 다음 할 것 등)
```

완료한 단계는 `- [x]` 로 체크. 문제가 생긴 단계는 옆에 ⚠️ 표시 후 아래 문제 항목에 상세 기록.

---

## 2026-06-03 23:54 — DA 23강 추천시스템 리서치 (①-B codex 리서처)
**상태**: 완료

### 계획
- [x] `CLAUDE.md` 리서처 위임 규약·DoD 확인
- [x] transcript 2개와 PDF를 읽고 강의 실제 토픽 파악
- [x] official 소스만 사용해 항목별 fact-check 근거·부연설명 후보·이미지 후보 조사
- [x] `data_analytics/notes/_research/23-recommender-systems.md` 작성
- [x] 리서치 노트 자체 검토: 출처 URL·이미지 라이선스·충돌 플래그 누락 확인
- [x] `WORKLOG.md`에 `리서치: 완료` 기록

### 문제 / 이슈
- 없음

### 비고
- 출력: `data_analytics/notes/_research/23-recommender-systems.md`
- 리서치: 완료
- 금지: `.qmd`, `origin/`, `transcript/`, `audio/`, `_legacy/` 수정하지 않음.

## 2026-06-03 23:52 — DA 23강 추천시스템 노트 작성 (듀얼에이전트 Review-Gate)
**상태**: 리뷰대기 (①-A 작성자 초안 완료; ①-B 리서치 완료; ② 리뷰어 단계는 별도 진행)

### 계획
- [x] 사전점검: 23 transcript 2개(part1 18min·part2 43min) `--scan` 클린(ratio 0.57/0.46), PDF `23_recommender_systems.pdf` 존재, 녹음일 2026-05-26
- [x] ①-A-1 codex(작성자): CLAUDE 계약·입력 파일 확인
- [x] ①-A-2 codex(작성자): transcript 2개 시간순 독해 및 강의 범위 추출
- [x] ①-A-3 codex(작성자): PDF에서 용어·수식·R 코드만 보완 확인
- [x] ①-A-4 codex(작성자): `.qmd` 초안 작성
- [x] ①-A-5 codex(작성자): 단일 render·frontmatter·Mermaid 검증 → `상태: 리뷰대기`
- [x] ①-B codex(리서처): 추천시스템 토픽 official 소스 리서치 → `notes/_research/23-recommender-systems.md`
- [ ] ② Claude(리뷰어): 초안↔리서치 교차검증·머지·DoD 검증 → 확정(전체 render 리스팅 갱신)
- [ ] origin 중복본 `데이터애널리틱스-23_recommender_systems.goodnotes` 처리(이미 done에 존재 → 정리)

### 문제 / 이슈
- `23_recommender_systems_part2_43min.txt` 끝이 "그냥 바이러스가"에서 문장 중간처럼 종료됨. 기존 `--scan`은 클린이었고 전사 재실행은 금지되어 있으므로, 노트는 transcript에 명확히 나온 NCF cold-start 완화까지만 반영하고 끝부분 추정 보강은 하지 않음.

### 비고
- 작성자 결과: `data_analytics/notes/2026-05-26_23-recommender-systems.qmd` 생성. 단일 `quarto render` 성공, frontmatter 확인, Mermaid HTML `<pre class="mermaid mermaid-js">` 3개 확인. 상태: 리뷰대기.
- 리서치: 완료 — `data_analytics/notes/_research/23-recommender-systems.md`
- 입력: `data_analytics/transcript/23_recommender_systems_part1_18min.txt`, `..._part2_43min.txt`. 보조 PDF `data_analytics/pdf/23_recommender_systems.pdf`
- 23강은 05-31 작업때 `- [ ]` 로 남아 미작성이던 강의. 이번에 완료 목표.

---

## 2026-06-03 23:20 — 20강 NN 전사 부분잘림 복구 + 노트 후반부 보강
**상태**: 완료 (Claude 직접, 재전사는 백그라운드)

### 계획
- [x] 증상 진단: 20강(61분) 전사가 ~92% 지점(출력층 sigmoid 도중)에서 문장 중간 끊김 + 이후 `. . .` 점-런 1,176자. 실내용 ~13.6k자뿐
- [x] 원인: whisper-1 통째 전사가 ~20분 지점 이후 점-런으로 무너짐. 전체 ratio 0.405라 stt.py 환각검사 통과(부분잘림 사각지대)
- [x] 복구: `ffmpeg`로 20분×3+88초 4토막 분할 → 각 토막 `stt.py`(gpt-4o) 백그라운드 재전사 → 전부 정상(ratio 0.48~0.80, 점런 0)
- [x] 합본 25,273자(원 실내용 대비 ~1.85배)로 transcript 교체. 원본은 `.truncated.bak` 백업
- [x] 복구분 분석: 21강(deep NN)로 넘어가는 강의라 **역전파/경사하강은 20강에 없음**(강의 중 "학습법은 다음 강" 명시). 노트에 빠졌던 것 = softmax 계산예시, depth/표현위계(에지→객체), **train/val/test 분할(98:1:1, CV 안 함)**
- [x] 노트 보강: §7 깊이·표현위계(+mermaid), §8 softmax 계산·예시, **§9 데이터 분할 신설**, lecture-summary 3줄 갱신
- [x] `quarto render` 성공, mermaid 2개 `<pre class="mermaid">` 정상

### 문제 / 이슈
- stt.py 환각검사가 **부분 잘림(후반 점-런)** 을 못 걸러냄 → CLAUDE.md 함정 #4에 "부분 잘림 사각지대 + 길이대비 단어수/끝부분 점런 확인 + 분할 재전사" 보강.
- 다른 긴 오디오도 같은 식으로 잘렸을 수 있음 → **전 과목 길이대비 전사량 일괄 점검 필요**(아래 비고).

### 비고
- 21강 노트는 역전파 다루는지 별도 확인 필요(20강에서 이월됨).

---

## 2026-06-03 23:30 — stt.py 환각검출 강화 + --scan + 전사 일괄점검
**상태**: 완료 (Claude 직접·검증)

### 계획
- [x] `stt.py` 검출기 보강: `tail_unique_ratio`(꼬리 윈도우 비율, TAIL_RATIO=0.30) + `max_phrase_run`(n-gram 구 반복, PHRASE_RUN=12) 추가 → 부분잘림·구반복형 환각 포착
- [x] 자동복구 강화: 긴 파일(23분 초과, gpt-4o 통째 불가)도 "원본유지 포기" 대신 `transcribe_split_gpt4o`(분할+gpt-4o)로 자동 재전사
- [x] `--scan` 모드 신설: 전 transcript 환각/잘림 일괄 점검(읽기전용), 의심파일+재전사 명령 출력
- [x] PHRASE_RUN 임계값 보정: 6→12 (7~11회는 실제 강의반복/stutter라 제외; 20+만 명백 루프). 경계 케이스 실측 후 결정(svm_part2 "그 문제만 풀고"×7=경미, chem6_part2 "KS는"×38=손상)
- [x] 전체 스캔 결과: 손상 4개 색출 — **전부 화학**: 9-26_part1(prun62,tail0.26), chem6_part2(38), chem7_part1(22), chem7_part3(56,tail0.05). 복구된 20강·DA 전부 ok
- [x] CLAUDE.md 함정 #4 + 스크립트 설명 갱신(--scan, 분할 자동복구)

### 문제 / 이슈
- 없음. (cpm은 모델별 장황도 차이로 단독판정 부적합 → 참고용 컬럼으로만, 하드신호는 ratio/tail/phrase)

### 비고
- 화학 손상 4건 재전사 완료(아래 항목 참조).

---

## 2026-06-03 23:38 — 화학 전사 4건 복구 (자동검출·복구 실전 검증)
**상태**: 완료 (재전사 백그라운드, 원본은 .halluc.bak 백업)

### 계획
- [x] 손상 4건 `--force` 재전사: 9-26_part1, chem6_part2, chem7_part1, chem7_part3
- [x] 9-26_part1: whisper-1 재전사도 환각(tail=0.05, phrase_run=128) → **신규 분할+gpt-4o 자동복구 발동** → ratio 0.62 채택 ✅ (자동화 실전 검증됨)
- [x] chem6_part2·chem7_part1: whisper-1 재전사가 이번엔 클린(STT 비결정성) → 직접 채택
- [x] chem7_part3: gpt-4o 재전사, 1.75KB→5.3KB(≈3배, 거의 통째 손상이었음), 정상 종료 확인
- [x] 복구 후 `--scan`: **의심 transcript 0개** (전 과목 클린)

### 문제 / 이슈
- 없음.

### 비고
- ⚠️ **후속 필요**: 이 손상 전사로 작성된 화학 노트가 내용 누락됐을 수 있음 → ch6(이온결합)·ch7(공유결합)·9-26(ch9 열화학) 노트를 복구 transcript와 대조해 보강 필요. (20강과 동일 패턴 가능성)

---

## 2026-06-03 21:55 — 17강 부스팅 섹션 작성 (PDF 기준)
**상태**: 완료 (Claude 직접 작성·검증)

### 계획
- [x] `ensemble_methods.pdf` 부스팅 파트 추출(pdftotext, p.18~23) — 이 PDF는 한글 정상 추출(mojibake 아님)
- [x] 노트 7번 placeholder → 본문 작성: 개념(순차·잔차적합), 회귀 부스팅 알고리즘(초기화/갱신/최종), mermaid 순차도, 파라미터 3개(λ·B·d), 배깅 vs 부스팅
- [x] 교수님 추가 설명(오너 제공) 반영: "λ는 bias-variance 직접관계 아님→U자형 아님→λ 고정하고 B 튜닝" → callout-important로 출처 명시
- [x] lecture-summary에 부스팅 한 줄 추가
- [x] `quarto render <file>` 성공, mermaid 2개 `<pre class="mermaid">` 정상(함정 #9 체크)

### 문제 / 이슈
- 작성 중 깨진 markdown 표 조각 남겼다가 즉시 제거. 그 외 없음.

### 비고
- 본문=PDF 슬라이드 기준, 교수님 구두 보충 1건은 별도 callout으로 구분 표기. 실습(gbm)은 18강.
- 듀얼 에이전트 파이프라인 미가동(web 리서치 없이 PDF만).

---

## 2026-06-03 19:08 — Mermaid 렌더 안 됨 일괄 수정 (펜스 문법)
**상태**: 완료 (Claude 직접 수정·검증)

### 계획
- [x] 증상 확인: DA 노트 14번부터 mermaid가 `graph LR ...` raw 텍스트로 출력(오너 제보)
- [x] 원인: 펜스가 ` ```mermaid `(중괄호 X) → Quarto가 다이어그램으로 처리 안 함. 13번 SVM 노트는 ` ```{mermaid} ` 라 정상
- [x] 레포 전체 `^```mermaid$` → ` ```{mermaid} ` 일괄 치환 (Python, 정확매칭): 9개 파일 16블록
  - DA: 14-svm-practice, 15-decision-trees, 17-ensemble, 20-nn, 21-dnn, 22-image, 25-text, 26-word-embedding
  - BC: 21-mev (3블록)
- [x] 잔여 깨진 펜스 0 확인
- [x] `quarto render`(전체) 24개 전부 에러 0, _site 갱신
- [x] 노트14 HTML 검증: `<pre class="mermaid">` 형태로 출력 = 브라우저 렌더 정상, 깨진 코드블록 형태 소멸

### 문제 / 이슈
- `quarto render` 는 ` ```mermaid `(잘못)도 에러 없이 통과 → 렌더 성공만으론 못 걸러냄. HTML에 `<pre class="mermaid">` 있는지로 확인해야 함. → CLAUDE.md 함정 #9 추가.

### 비고
- 기존 DoD의 "렌더 성공" 체크가 이 버그를 못 잡았음. mermaid 쓰는 노트는 펜스 중괄호 여부를 별도 확인 권장.

---

## 2026-06-03 19:05 — SVM 노트 7번 OvA 그림 + 부연 추가
**상태**: 완료 (Claude 직접 작성·검증)

### 계획
- [x] OvA(One-vs-All) 결정규칙 설명용 그림 생성 (matplotlib) — 클러스터 3개 + 기하적으로 일관된 'k vs 나머지' 경계, 부호거리 $f_k$ 비교
- [x] `data_analytics/notes/img/svm-ova-multiclass.png` 저장
- [x] 노트 7번에 `![]()` 임베드(@fig-ova) + callout-note(학습 K번 독립 / 예측 부호최대 / 절댓값 아님) 추가
- [x] `quarto render <file>` 단일 렌더 성공

### 문제 / 이슈
- 1차 그림은 목표 f값 맞추려 법선·offset을 임의 배치 → 경계가 실제 3-클래스 배치와 불일치(오너가 지적). 클러스터 3개를 깔고 각 OvA 경계를 centroid 기반으로 진짜 분리하도록 재작성해 해결.
- 한글 폰트(NanumGothic)에 ₖ(아래첨자) 글리프 없어 깨짐 → `f_k` 일반표기로 교체.

### 비고
- 외부 web 출처 없음(개념 도식, ISLR ch.9 수준). 듀얼 에이전트 미가동.
- 본문 OvA/OvO 텍스트는 기존 그대로, 그림·부연만 보강.

---

## 2026-06-03 18:42 — SVM 노트 5번 부연 설명 추가
**상태**: 완료 (Claude 직접 작성·검증)

### 계획
- [x] 오너 질문(쌍대 형식·내적·margin 이해)에 맞춰 `2026-04-11_support-vector-machines.qmd` 5번 섹션에 callout-note 부연 3개 추가
  - 쌍대 형식 관점 전환($\beta=\sum\alpha_i x_i$ 직관 포함)
  - 첨자 $i$(데이터)·$j$(feature)·$x$(새 점) 의미 + 학습/예측 시 $x$ 자리 차이
  - margin 최대화 = $\lVert\beta\rVert$ 최소화 4단계
- [x] `quarto render <file>` 단일 렌더 성공 (HTML 생성, 에러 0)

### 문제 / 이슈
- 없음. (site-url 누락 WARN 은 기존부터 있던 무관 경고)

### 비고
- 부연은 오너와의 대화에서 도출한 개념 설명(ISLR ch.9 수준 표준 내용)이라 외부 web 출처는 달지 않음. 듀얼 에이전트 파이프라인은 미가동(단일 작성).
- 본문 $\binom{n}{2}$ 표기는 그대로 유지 — $O(n^2)$ 로 정확, 부연에 카운팅 의미만 명시.

---

## 2026-06-02 16:40 — DA 25/26 + 블록체인 21 노트 작성
**상태**: 완료 (Claude 직접 작성·검증)

### 계획
- [x] `extract.py` 로 3개 .goodnotes 추출 (audio/pdf 분리, done/ 이동)
- [x] `stt.py --all` 전사 (26 part1 13min→gpt-4o, 26 part2 51min·BC21 26min→whisper-1)
- [x] 전사 환각 루프(ratio) 검사 — 전부 정상 (25: 0.59/0.45, 26: 0.54/0.42, BC21: 0.58)
- [x] DA 25 text analytics 노트 작성 + 단일 render
- [x] DA 26 word embedding 노트 작성 + 단일 render
- [x] 블록체인 21 노트 작성 + 단일 render
- [x] 전체 `quarto render` 로 리스팅 갱신 (24개 전부 성공, _site/index.html 생성)

### 산출물
- `data_analytics/notes/2026-05-28_25-text-analytics.qmd` (BoW/DTM/TF-IDF, R tm 실습 F1 0.82)
- `data_analytics/notes/2026-06-02_26-word-embedding.qmd` (Word2Vec/Skip-gram, GloVe, 풀링, F1 0.865)
- `blockchain/notes/2026-06-01_21-mev.qmd` (MEV: 아비트라지/청산/샌드위치, 멤풀, 가스경쟁/중앙화)

### 문제 / 이슈
- date 멀티데이: 25(part1 05-26 / part2 48min 05-28), 26(part1 05-28 / part2 51min 06-02). 본체(최장 part) 기준 → 25=05-28, 26=06-02 로 확정. ⚠️ 오너 최종 확인 권장.

### 비고
- 25_text_analytics 는 이전에 transcript/done 존재(부분 처리)였고 노트만 없었음 → 이번에 작성 완료.

**상태**: 승인 (codex 작성 → Claude 리뷰 반영)

### 리뷰 (Claude, 2026-06-01 15:36)
- 계산 재검산: 9.43(−0.388 kJ, 발열)·9.47(3.05 °C)·9.49(−469 kJ/mol) 전부 정확 ✓
- 녹음 대조: AgCl 침전 예시·CH₄+Cl₂(클로로폼) 결합에너지 예시 모두 transcript에 실재 확인(STT가 Ag→"age", CHCl₃→"CHC"로 깨뜨려 1차 grep에선 누락으로 오인) ✓
- **수정 1건**: §4 AgCl 예시에서 온도(32.6°C)·답(−63.5 kJ/mol)이 날조됨 — 강의는 반응·몰수(10+10mL, 0.01 mol)까지만 설명하고 실측값은 학생 실습 몫. → 측정 수치 제거하고 절차(q=cmΔT → 한계반응물 몰수로 나눔)만 남김 + "수치 주의" callout 추가. 재렌더 통과. ⇒ **교훈: codex가 강의에서 셋업만 한 예제에 임의 측정수치를 채우는 경향 — 리뷰 시 구체 수치는 transcript 출처 확인 필수**

### 계획
- [x] `CLAUDE.md` 계약 확인
- [x] 9장 transcript 3개를 시간순으로 읽고 녹음 중심 개요 작성
- [x] `9-26.pdf` 4페이지 이후에서 수치·화학식·영어 용어만 보완
- [x] 연습문제 9.43, 9.47, 9.49를 직접 계산·검산
- [x] `chemistry/notes/2026-06-01_ch9-thermochemistry.qmd` 작성
- [x] 단일 `quarto render` 검증 및 frontmatter 확인

### 문제 / 이슈
- 전사 part1 후반에 "보온병 열량..." 질문이 비정상적으로 반복되는 STT 구간이 있음. 전체 ratio는 0.49로 환각 기준(0.2 미만)은 아니지만 내용상 반복 필러라 노트에는 반영하지 않음.

### 비고
- 입력: `chemistry/transcript/9-26_part1_43min.txt`, `chemistry/transcript/9-26_part2_11min.txt`, `chemistry/transcript/9-26_part3_3min.txt`
- PDF: `chemistry/pdf/9-26.pdf`는 4페이지부터 용어·수치 보완용, `9-26_practice_problems.pdf`는 9.43/9.47/9.49 문제 확인용
- 계산 검산: 9.43 `q=-0.388 kJ`(0.388 kJ 방출, 발열), 9.47 `T_f=3.05 °C`(흡열 냉찜질), 9.49 `q_rxn=-29.0 kJ`, `ΔH=-469 kJ/mol`
- 검증: `quarto render chemistry/notes/2026-06-01_ch9-thermochemistry.qmd` 에러 0, `_site/chemistry/notes/2026-06-01_ch9-thermochemistry.html` 생성. `site-url` 누락 feed 경고는 기존 프로젝트 설정 경고로 HTML 생성에는 영향 없음.

## 2026-05-31 17:37 — 노트 date 불일치 정리
**상태**: 완료

### 계획
- [x] 전체 `.qmd` 노트의 파일명 날짜와 frontmatter `date` 대조
- [x] 불일치 노트 수정 및 필요 시 파일명/산출물 정리
- [x] Quarto 렌더로 목록 날짜 갱신 검증

### 문제 / 이슈
- 1차 검증 기준을 파일명 prefix와 metadata date 일치 여부로만 잡아, 파일명과 metadata가 같이 처리일로 잘못 들어간 blockchain 노트들을 놓침. 원본 GoodNotes attachment 날짜 기준으로 재대조해 해결.
- 검증 중 `_site/index.html` 확인 명령 인용을 잘못 넣어 산출물이 잠시 확인 출력으로 덮임. 원본 `.qmd`는 영향 없었고, 즉시 `quarto render`로 `_site/index.html` 재생성해 복구 완료.

### 비고
- 기준: CLAUDE.md 날짜 규칙 — `date`와 파일명 prefix는 오디오 `creation_time` 기준 녹음일
- 수정: `data_analytics/notes/2026-04-11_support-vector-machines.qmd` metadata `date`를 `2026-05-29` → `2026-04-11`로 변경
- 추가 수정: blockchain 12~19-20 metadata `date`를 원본 GoodNotes 오디오 attachment 날짜로 변경
  - 12=2026-04-15, 13=2026-04-22, 14=2026-04-27, 15=2026-04-29, 16=2026-05-06, 17-18=2026-05-11, 19-20=2026-05-18
- 검증: blockchain metadata date 재대조 통과, `quarto render` 성공, `_site/index.html` listing-date 갱신 확인

## 2026-05-31 16:35 — 화학 6장 Born-Haber mermaid syntax error 수정
**상태**: 완료

### 계획
- [x] 깨진 블록 특정 (ch6 §6 Born–Haber, line 137 graph TD)
- [x] mermaid-cli 10.2.2로 에러 재현 → "Lexical error" 원인 확인
- [x] 엣지 라벨 따옴표 처리 후 재검증
- [x] quarto 재렌더로 HTML 갱신

### 문제 / 이슈
- 원인: 따옴표 없는 엣지 라벨 `-->|...|` 안에 **원문자(①②③④⑤)·½··(middle dot)·→** 등 특수문자가 들어가 Quarto 번들 mermaid(10.2.0-rc.2) 렉서가 거부 ("Lexical error / Unrecognized text"). 최신 mermaid에선 통과하나 구버전에서 실패.
- 해결: 엣지 라벨을 모두 `|"..."|` 로 감쌈 → 10.2.2 렌더 성공 검증 후 적용.
- 확인: data_analytics 노트(decision-trees, ensemble)에도 따옴표 없는 엣지 라벨이 있으나 `<`/`>=`/한글뿐이라 정상 렌더됨 → 수정 불필요. ⇒ **mermaid 엣지 라벨에 특수문자/유니코드 기호 넣을 땐 항상 따옴표로 감쌀 것**.

### 비고
- 대상 파일: notes/2026-05-11_ch6-ionic-bonding.qmd

## 2026-05-31 14:17 — 화학 5장 노트: 라이만/발머/파셴 설명 보강
**상태**: 완료

### 계획
- [x] 사용자 질문(수소 방출 스펙트럼 계열) 응대
- [x] ch5 노트에 mermaid 다이어그램만 있고 텍스트 설명이 없음을 확인
- [x] 다이어그램 하단에 3계열 설명 + callout(자주 헷갈리는 점) 추가

### 문제 / 이슈
- 다이어그램(라이만/발머/파셴 → UV/VIS/IR)은 있었으나 본문 설명이 없어 학습자가 의미를 파악하기 어려웠음 → 설명 블록 추가로 해결

### 비고
- 추가 내용: 도착 준위(n=1/2/3)가 계열명을 결정, 수소 전용(수소꼴 이온 포함), n=2·3은 중간 기착지(계단식 방출), 출발점·경로는 확률적
- 대상 파일: notes/2026-05-04_ch5-periodicity-atomic-structure.qmd

## 2026-05-31 10:47 — 데이터애널리틱스 20~25 노트 작성
**상태**: 진행중

### 계획
- [x] 20 신경망 기초 노트 → notes/2026-05-12_20-neural-networks.qmd
- [x] 21 심층신경망(학습·오버피팅) 노트 → notes/2026-05-14_21-deep-neural-networks.qmd
- [x] 22 이미지 응용·표현학습 노트 → notes/2026-05-21_22-image-representation-learning.qmd
- [ ] 23 추천 시스템 노트 → notes/2026-05-26_23-recommender-systems.qmd
- [ ] 25 텍스트 분석 노트 → notes/2026-05-28_25-text-analytics.qmd
- [ ] 5개 .qmd Quarto 렌더 검증 (mermaid+LaTeX)

### 문제 / 이슈
- (없음)

### 비고
- 입력: transcript/ 신규 8개(20·21part1/2·22·23part1/2·25part1/2). 함정 #6대로 PDF는 용어/코드 보완용
- 녹음일: 20=05-12, 21=05-14, 22=05-21, 23=05-26, 25=05-28 (creation_time)
- 파일 1개 단위가 아니라 강의(번호) 1개 = 노트 1개. part1/2 합쳐 한 노트

---

## 2026-05-31 11:58 — 블록체인 19-20 노트 리뷰 반영 (PoW 문제·RANDAO)
**상태**: 승인(렌더 검증 완료)

### 계획
- [x] PoW 문제 칸 3개 녹음 대조 — 1·2(19강)·3 채굴풀(20강) 모두 근거 확인, 채굴풀 칸 유지
- [x] 누락분 보완: "2018-19 이더리움 3대 문제" 표 추가(풀노드 비대화→탈중앙, 19강+PDF p19) → 솔루션 매핑
- [x] RANDAO 정확성 보강: 강의 단순화 본문 유지 + callout(각 슬롯 Proposer reveal/BLS 조작불가/~2 epoch 뒤 배정/제네시스 eth1 시드) 추가, 출처 명시
- [x] `quarto render` 검증 — HTML 정상 생성, 추가분 6항목 렌더 확인

### 문제 / 이슈
- 리뷰 중 1차 오판: 채굴풀 집중화를 19강만 보고 "강의 외 보강"이라 판단 → 20강 transcript에 명확히 존재(솔로채굴 변동성→풀형성→풀 운영자 블록구성→중앙화) 확인 후 철회. ⇒ 19-20 합본 노트는 **두 강 transcript 모두 대조** 필요

### 비고
- 본문은 강의(시험범위) 수준 유지, 정확성 보강은 callout/표로 분리하고 출처 표시(CLAUDE.md '녹음 위주 + 보강 출처' 원칙)
- 산출물: blockchain/notes/2026-05-30_19-20-rollup-stage-pos-merge.qmd (+ _site HTML)

## 2026-05-31 00:10 — 자동화 스크립트 작성 + 데이터애널리틱스 20~25 추출·전사
**상태**: 전사 완료 / 노트 작성 대기

### 계획
- [x] `scripts/extract.py` 작성 — goodnotes 추출+과목분류+매직바이트 분리+녹음일 산출
- [x] `scripts/stt.py` 작성 — 모델 자동선택/25MB 분할/환각검사/키 폴백 (함정 #1~4,#7 코드화)
- [x] CLAUDE.md 에 자동화 스크립트 섹션 추가
- [x] 신규 5개 goodnotes(20,21,22,23,25) 추출 → audio 9 + pdf 5, origin/done 이동
- [x] 신규 9개 오디오 STT → transcript/ (전부 생성)
- [ ] transcript 교정 + .qmd 노트 작성 (3~4번, LLM 판단 작업)

### 문제 / 이슈
- **stt.py 환각 재전사 버그**: #20(61분)이 부분 반복(run=581)으로 환각 오판 → 폴백 gpt-4o가 23분 초과로 실패하며 whisper-1 원본까지 폐기됨. → (1) 임계값을 `ratio<0.2` 또는 `(run>=200 and ratio<0.35)`로 완화, (2) 폴백 실패/미개선 시 원본 보존, (3) gpt-4o 폴백은 길이 제한 내에서만. 수정 후 #20 정상(ratio 0.41 보존). ⇒ 함정 #4 보강
- **기존 강의 재전사 발생**: legacy transcript는 `decision_trees_part1.txt`인데 extract는 `_24min` 접미사 명명 → 이름 불일치로 미존재 판단, svm/decision_trees/ensemble 재전사 시작. API 비용 낭비라 중단.
  → **해결(data_analytics)**: transcript 이름을 현재 오디오 basename과 1:1로 정리. legacy 3개(svm_47min→svm_part2_47min, svm_53min→svm_part3_53min, svm_practice→svm_practice_41min) rename, 중복 6개는 `transcript/_legacy/`로 이동(보존).
  → **해결(blockchain·chemistry)**: 동일한 이름 불일치 발견(transcript에 `_Nmin` 접미사 없음, --all 시 16개 재전사 위험). blockchain 9개·chemistry 7개 transcript를 오디오 basename으로 rename(1:1 자동 매칭).
  → **검증**: 3과목 전부 오디오=transcript 동수, `stt.py --all` 재실행 시 **33개 전원 스킵, API 0회** 확인.

### 비고
- 녹음일 후보(creation_time 자동): 20=05-12, 21=05-14(본체, part1 1분은 05-12 잔여), 22=05-21, 23=05-26(본체), 25=05-28(본체)
- 22번은 온라인 강의 섞여 녹음 일부만(46분) — 정상
- 남은 작업: 신규 5강의 노트 .qmd 작성 → **Codex 위임 규약(Review-Gate)** 으로 진행 (CLAUDE.md 하단 섹션). codex=작성자, Claude=리뷰어, 오너=최종승인. 상태머신 `draft→리뷰대기→승인`.

## 2026-05-30 14:33 — 데이터애널리틱스 14~18 노트 정리
**상태**: 완료

### 계획
- [x] 5개 goodnotes 전부 추출 (PDF→pdf/, 오디오→audio/, 토픽별 명명)
- [x] STT 전부 (긴 녹음 whisper-1) → transcript/ (6개 오디오)
- [x] 14 SVM 실습 노트 → notes/2026-04-23_14-svm-practice.qmd
- [x] 15 의사결정나무 노트 → notes/2026-04-23_15-decision-trees.qmd
- [x] 16 의사결정나무 실습 노트 → notes/2026-04-28_16-decision-trees-practice.qmd
- [x] 17 앙상블 기법 노트 → notes/2026-04-30_17-ensemble-methods.qmd
- [x] 18 앙상블 실습 노트 → notes/2026-05-07_18-ensemble-methods-practice.qmd
- [x] 5개 .goodnotes → origin/done/ 이동 (origin 비움)
- [x] Quarto 렌더 검증 (5개 전부 HTML 생성, mermaid+LaTeX 정상)

### 문제 / 이슈
- **전사 백그라운드 잡이 중간에 중단**(foreground 대기 명령이 harness에 의해 137 kill되면서 같이 종료된 것으로 보임). 6개 중 2개만 완료된 적 있음 → nohup으로 재실행하여 나머지 처리 (해결)
- **decision_trees_practice(17분) whisper-1에서 환각 루프**(ratio 0.09, "알파트 압수" 반복) → gpt-4o-transcribe로 재전사하여 해결(ratio 0.57). ⇒ 짧은 파일은 gpt-4o, 환각 시 모델 교체
- **ensemble_methods boosting은 교수가 영상으로 대체** → 17 노트엔 bagging/bootstrap/OOB/random forest까지, boosting은 18 실습(gbm)에서 다룸
- 긴 오디오(38·45·62분) gpt-4o 23분 제한 → whisper-1 사용 (기존 화학 작업과 동일 패턴)

### 비고
- 파일 1개 = 노트 1개. _practice는 별도 "실습" 노트. 노트 파일명에 강의번호 prefix(`14-`,`15-`...) 사용 (사용자/린터가 정리한 규칙 따름)
- date = 강의 녹음일(audio creation_time). 15는 04-23(24분)+04-28(45분) 2개 → 04-23 기준
- 코드 예시 R, 수식 LaTeX (CLAUDE.md data_analytics 규칙)
- 녹음일: 14=04-23, 15=04-23/04-28, 16=04-28, 17=04-30, 18=05-07
- 기존 svm 노트는 처리 중 녹음일(2026-04-11)로 수정·번호 prefix 정리됨(2026-04-11_support-vector-machines.qmd) — 날짜 규칙 위반 해소
- **origin/ 완전히 비움 = blockchain·chemistry·data_analytics 모든 과목 처리 완료**

## 2026-05-30 09:55 — 화학 6장·7장 노트 정리
**상태**: 완료

### 계획
- [x] 6장 attachments 추출 (PDF→pdf/, 오디오 mp4 2개→audio/, 시간순 정렬)
- [x] 6장 STT → transcript/ (part1 gpt-4o-transcribe, part2 whisper-1)
- [x] 6장 교정 (오인식·필러 제거, PDF 용어 보완) — 노트 생성에 통합
- [x] 6장 노트 .qmd 생성 → notes/2026-05-11_ch6-ionic-bonding.qmd
- [x] 6장 .goodnotes → origin/done/ 이동
- [x] 7장 attachments 추출 (PDF→pdf/, 오디오 mp4 3개→audio/, 시간순 정렬)
- [x] 7장 STT → transcript/ (part1 whisper-1, part2·part3 gpt-4o→part3 whisper-1 재시도)
- [x] 7장 교정 — 노트 생성에 통합
- [x] 7장 노트 .qmd 생성 → notes/2026-05-18_ch7-covalent-bonding.qmd
- [x] 7장 .goodnotes → origin/done/ 이동
- [x] 두 노트 Quarto 렌더 검증 (mermaid+LaTeX 정상 컴파일, _site HTML 생성)

### 문제 / 이슈
- origin 화학 파일명이 NFD 인코딩 → shell glob/grep 매칭 실패. Python os.listdir + unicodedata.normalize('NFC')로 우회 (해결)
- gpt-4o-transcribe는 오디오 **1400초(약 23분) 길이 제한** → 6장 part2(40분)·7장 part1(38분) 400 에러. whisper-1(25MB 한도, 길이 무관)로 재전사하여 해결. ⇒ 긴 녹음은 whisper-1 사용 또는 분할
- env의 OPENAI_API_KEY는 만료/무효(401). openclaw.json의 skills.entries.openai-whisper-api.apiKey 사용 (해결)
- **7장 part3(15분)이 gpt-4o-transcribe에서 환각 루프**(동일 문장 수백 회 반복)로 사용 불가 → whisper-1 재전사로 해결. (해당 구간은 N2O 루이스 구조 연습 반복 지시라 실제로도 반복 많음) ⇒ 환각 루프 발견 시 다른 모델로 재전사
- 날짜 규칙 불일치: 기존 chem5 노트는 처리일(2026-05-29)을 date로 사용했으나, 스터디 노트엔 강의일이 맞다고 판단해 6·7장은 **녹음일**(6장 05-11, 7장 05-18)로 작성. ⇒ **사용자 확인 후 "강의 녹음일" 표준으로 확정**. chem5도 녹음일(2026-05-04)로 date 수정 + 파일명 변경(2026-05-04_ch5-...), 전체 quarto 재렌더로 listing 갱신 (해결)
  - ⇒ 노트 date = **오디오 creation_time 기준 강의 녹음일**, 파일명 prefix도 동일

### 비고
- 6장: 이온결합과 몇 가지 주족의 화학 / 7장: 공유결합과 분자구조
- 오디오는 확장자 없이 attachments/ 에 저장, 매직바이트(ftyp mp42)로 판별
- 6장 오디오 2.72MB+9.66MB, 7장 0.36MB+9.24MB+3.60MB
- 산출물: notes/2026-05-11_ch6-ionic-bonding.qmd, notes/2026-05-18_ch7-covalent-bonding.qmd

## 2026-06-04 11:30 — data_analytics 21강 노트 보강 (온라인 강의 부분)
**상태**: 완료
- [x] 21강 후반 온라인(녹화) 강의 부분이 노트에 누락된 것 확인 (기존 §10 정규화까지만 있었음)
- [x] PDF(pdf/21_deep_neural_networks.pdf p.19~21) 기준으로 §11 하이퍼파라미터, §12 실무 고려사항 추가
- [x] 교수 구두 설명 추가(오너 제공): 튜닝 순서 = architecture→training→regularization 순차, architecture는 표준 구성 써서 잘 튜닝 안 함 → callout으로 별도 표기
- [x] lecture-summary 보강, quarto render 단일 렌더 성공(에러 0)
- 비고: lecture 17 boosting 선례와 동일 패턴(온라인/녹화 강의 = PDF 기준 + 구두 추가분만 별도 표기). 웹 리서치 불필요(오너 제공 + PDF)한 소규모 추가라 듀얼에이전트 게이트 생략하고 인라인 처리.

## 2026-06-04 13:35 — data_analytics 22강 노트 앞부분(온라인 강의) 보강
**상태**: 완료
- [x] 기존 22강 노트는 응용부(얼굴인식/객체탐지/전이학습)만 상세, 앞부분 CNN 기초는 §1 한 단락으로 압축돼 있었음
- [x] PDF(pdf/22_-image_applications_representation_learning.pdf p.3~16) 기준으로 앞부분 확장: §1 표현→응용, §2 FC 한계(공간구조·파라미터 150,528→약963만), §3 합성곱(필터·패딩·채널), §4 다중필터·풀링·전체구조(+모델진화 LeNet~EfficientNet), §5 이미지분류(softmax/CE)·계층적 표현학습
- [x] 응용부 섹션 번호 2/3/4 → 6/7/8 로 재배치
- [x] quarto render 성공, mermaid 2개(CNN 파이프라인+YOLO) 정상 렌더(`mermaid mermaid-js`)
- 비고: 오너 확인 — 앞부분은 온라인 강의, PDF 외 구두 추가분 없음 → PDF 그대로 작성. 웹 리서치 불필요한 PDF 전사라 듀얼에이전트 게이트 생략, 인라인 처리. (21강 보강과 동일 패턴)
