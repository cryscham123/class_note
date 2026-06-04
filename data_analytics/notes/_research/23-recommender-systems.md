# DA 23강 추천 시스템 리서치 노트

- 역할: ①-B codex 리서처
- 입력: `data_analytics/transcript/23_recommender_systems_part1_18min.txt`, `data_analytics/transcript/23_recommender_systems_part2_43min.txt`, `data_analytics/pdf/23_recommender_systems.pdf`
- 출력 목적: 본 `.qmd`에 직접 머지하지 않고, 리뷰어가 fact-check와 부연 설명을 교차검증할 수 있는 근거 노트 제공
- 소스 원칙: 교과서/핸드북, 학회·저널 1차 논문, 대학 강의자료만 사용. 개인 블로그/위키/콘텐츠팜 미사용.

## 강의 토픽 맵

- Part 1: 추천 시스템의 일상적 사례, rule-based → collaborative filtering (CF) → matrix factorization (MF) → neural collaborative filtering (NCF) 흐름, user-based CF와 item-based CF의 직관, 사용자-아이템 평점 행렬, Pearson correlation과 cosine similarity.
- Part 2: cosine 기반 neighbor 선택, 평균/가중평균 예측, 사용자별 평점 normalization, binary 구매 여부 데이터, CF의 계산 비용·cold start·sparsity, train/test에서 일부 관측 평점을 가리고 MAE/RMSE로 평가, MF의 latent factor 모델과 `R ≈ UV^T`, FunkSVD/ALS/gradient descent, NCF의 embedding table·MLP·MSE/BCE loss, side information으로 cold start 완화.

## 핵심 공식 출처

- [출처: Charu C. Aggarwal, *Recommender Systems: The Textbook*, Springer, https://link.springer.com/book/10.1007/978-3-319-29659-3]
- [출처: Aggarwal, "Neighborhood-Based Collaborative Filtering", Springer, https://link.springer.com/chapter/10.1007/978-3-319-29659-3_2]
- [출처: Aggarwal, "Content-Based Recommender Systems", Springer, https://link.springer.com/chapter/10.1007/978-3-319-29659-3_4]
- [출처: Aggarwal, "Evaluating Recommender Systems", Springer, https://link.springer.com/chapter/10.1007/978-3-319-29659-3_7]
- [출처: Ricci, Rokach, Shapira (eds.), *Recommender Systems Handbook*, 3rd ed., Springer, https://link.springer.com/book/10.1007/978-1-0716-2197-4]
- [출처: Gunawardana & Shani, "A Survey of Accuracy Evaluation Metrics of Recommendation Tasks", JMLR 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]
- [출처: Sarwar et al., "Item-based Collaborative Filtering Recommendation Algorithms", WWW 2001/ACM, https://doi.org/10.1145/371920.372071]
- [출처: University of Minnesota Experts page for Sarwar et al. 2001, https://experts.umn.edu/en/publications/item-based-collaborative-filtering-recommendation-algorithms]
- [출처: Linden, Smith & York, "Amazon.com Recommendations: Item-to-Item Collaborative Filtering", IEEE Internet Computing 2003, https://doi.org/10.1109/MIC.2003.1167344]
- [출처: Koren, Bell & Volinsky, "Matrix Factorization Techniques for Recommender Systems", IEEE Computer 2009, https://doi.org/10.1109/MC.2009.263]
- [출처: Stanford CS246 2019, "Recommender Systems", https://snap.stanford.edu/class/cs246-2019/slides/07-recsys1.pdf]
- [출처: Stanford CS246 2012, "Recommender Systems: Latent Factor Models", https://snap.stanford.edu/class/cs246-2012/slides/08-recsys2.pdf]
- [출처: He et al., "Neural Collaborative Filtering", WWW 2017/ACM, https://doi.org/10.1145/3038912.3052569]

## 1. Content-Based Filtering vs Collaborative Filtering

### 강의에서의 서술

- 강의는 주로 collaborative filtering을 다루며, user-based CF와 item-based CF를 구분한다.
- user-based CF는 "나와 비슷한 사용자"가 좋아한 아이템을 추천하고, item-based CF는 "내가 선호한 아이템과 비슷하게 다른 사용자들에게 선호된 아이템"을 추천한다고 설명한다.
- Content-based filtering 자체는 중심 주제로 길게 다루지 않는다.

### official 근거

- Gunawardana & Shani는 CF가 과거에 같은 아이템을 선호한 사용자는 미래에도 유사하게 선호할 것이라는 가정에 기반하며, 많은 CF 방법이 user-item rating matrix의 미지 entry를 예측한다고 정리한다. 같은 논문은 user-based CF가 active user와 비슷한 사용자의 neighborhood를 찾고, item-based CF가 특정 active item을 선호한 사용자들의 정보를 이용한다고 설명한다. [출처: Gunawardana & Shani 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]
- 같은 논문은 content-based recommendation을 "item features를 사용해 사용자의 feature preference를 학습하고, 유사한 feature를 가진 새 아이템을 추천"하는 방식으로 구분한다. [출처: Gunawardana & Shani 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]
- Aggarwal의 content-based chapter도 CF가 사용자 간 rating pattern의 상관을 쓰는 반면, content-based는 item attribute를 사용한다고 구분한다. [출처: Aggarwal, "Content-Based Recommender Systems", https://link.springer.com/chapter/10.1007/978-3-319-29659-3_4]

### 플래그

- **주의: item-based CF와 content-based filtering은 다르다.** item-based CF의 "아이템 유사도"는 보통 사용자-아이템 상호작용 행렬에서 계산된다. content-based는 장르, 텍스트, 배우, 가격, 이미지 같은 item attribute를 사용한다. 본 노트에서 item-based CF를 "콘텐츠 기반"으로 합치면 사실 충돌.

### callout 후보

::: {.callout-note title="Item-based CF는 content-based가 아니다"}
Item-based collaborative filtering은 "아이템을 기준으로 본다"는 점 때문에 content-based recommendation과 헷갈리기 쉽다. 그러나 item-based CF의 유사도는 보통 사용자들의 공동 평점·구매 패턴에서 나온다. 반면 content-based recommendation은 아이템의 장르, 텍스트, 태그, 이미지 같은 속성(feature)을 사용한다. 출처: [Gunawardana & Shani 2009](https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf), [Aggarwal, Content-Based Recommender Systems](https://link.springer.com/chapter/10.1007/978-3-319-29659-3_4)
:::

## 2. User-Based / Item-Based CF와 similarity 수식

### 강의에서의 서술

- UBCF는 (1) 추천 대상 사용자와 유사한 neighbor를 찾고, (2) neighbor들이 선호한 미관측 아이템을 추천한다.
- similarity로 Pearson correlation과 cosine similarity를 주로 소개한다.
- 공통으로 평가한 아이템만 사용해 similarity를 계산한다.
- `k = 3` neighbor 예제에서 cosine similarity 기준으로 `u1, u3, u4`를 선택하고, neighbor 평점의 평균 또는 similarity-weighted average로 예측 평점을 계산한다.
- 공통 평가 아이템이 1개뿐이면 cosine similarity가 항상 1이 되므로 neighbor 후보에서 제외한다고 설명한다.

### official 근거

- Aggarwal은 neighborhood-based CF가 "비슷한 사용자는 비슷한 rating behavior를 보이고, 비슷한 item은 비슷한 rating을 받는다"는 사실에 기반하며, user-based와 item-based 두 종류가 있다고 설명한다. [출처: Aggarwal, "Neighborhood-Based Collaborative Filtering", https://link.springer.com/chapter/10.1007/978-3-319-29659-3_2]
- Sarwar et al.은 item-based technique이 user-item matrix에서 item 사이 관계를 먼저 분석하고, 그 관계로 사용자 추천을 계산한다고 설명한다. 또한 item-item correlation, cosine similarity, weighted sum, regression model을 비교한다. [출처: Sarwar et al. 2001, https://doi.org/10.1145/371920.372071]
- Amazon의 item-to-item collaborative filtering은 Linden et al. 2003의 IEEE 논문으로 정리되어 있다. 강의 PDF의 Amazon 예시는 이 계열과 잘 맞는다. [출처: Linden, Smith & York 2003, https://doi.org/10.1109/MIC.2003.1167344]
- Stanford CS246도 user-user CF와 item-item CF를 구분하고, similarity metric으로 Jaccard, cosine, Pearson correlation을 제시한다. [출처: Stanford CS246 2017 review slides, https://snap.stanford.edu/class/cs246-2017/slides/review.pdf]

### 수식 후보

공통 평가 아이템 집합을 $I_{uv}$라 하면:

$$
\operatorname{cos}(u,v)
= \frac{\sum_{i \in I_{uv}} r_{ui} r_{vi}}
{\sqrt{\sum_{i \in I_{uv}} r_{ui}^2}\sqrt{\sum_{i \in I_{uv}} r_{vi}^2}}
$$

$$
\operatorname{corr}(u,v)
= \frac{\sum_{i \in I_{uv}} (r_{ui}-\bar r_u)(r_{vi}-\bar r_v)}
{\sqrt{\sum_{i \in I_{uv}} (r_{ui}-\bar r_u)^2}\sqrt{\sum_{i \in I_{uv}} (r_{vi}-\bar r_v)^2}}
$$

간단한 weighted-average 예측:

$$
\hat r_{ui}
= \frac{\sum_{v \in N_k(u;i)} s(u,v) r_{vi}}
{\sum_{v \in N_k(u;i)} s(u,v)}
$$

실무·교과서형 변형에서는 사용자 평균 또는 baseline을 빼고 예측한 뒤 되돌리는 형태도 흔하다.

$$
\hat r_{ui}
= \bar r_u +
\frac{\sum_{v \in N_k(u;i)} s(u,v)(r_{vi}-\bar r_v)}
{\sum_{v \in N_k(u;i)} |s(u,v)|}
$$

### 플래그

- **cosine 범위:** 강의 PDF는 cosine similarity를 `-1`에서 `1` 사이라고 설명한다. 수학적으로는 맞지만, 원자료가 1~5점처럼 모두 양수이면 cosine은 보통 `0`에서 `1` 범위에 머문다. 평균 중심화나 음수 feature가 있으면 음수가 가능하다.
- **공통 평가 1개:** positive rating 한 쌍만 있으면 cosine은 1이 되어 의미가 없다. Pearson은 표본 분산을 계산할 수 없어 사실상 undefined가 된다. 예제처럼 후보 제외가 타당하다.
- **weighted average 분모:** 강의 예제는 similarity가 모두 양수라 `sum(similarity)` 분모가 자연스럽다. 음수 similarity까지 허용하면 분모가 0에 가까워지거나 부호가 뒤집힐 수 있으므로, 실제 구현에서는 양수 neighbor만 쓰거나 `sum |similarity|`, mean-centered deviation, baseline model을 함께 쓴다.
- **STT 용어:** transcript에는 "표본 상관기술", "코사인 시뮬레이션"으로 들리는 부분이 있다. 노트에는 각각 **표본상관계수 (sample/Pearson correlation coefficient)**, **코사인 유사도 (cosine similarity)**로 정리하는 것이 맞다.

### callout 후보

::: {.callout-note title="공통 평가 아이템 수가 너무 적으면 유사도가 과신된다"}
두 사용자가 공통으로 평가한 영화가 1개뿐이면, 양수 평점 기준 cosine similarity는 항상 1이 된다. 이는 "완전히 비슷하다"는 뜻이 아니라 비교할 정보가 부족하다는 뜻이다. 그래서 neighborhood CF에서는 최소 공통 평가 개수, similarity threshold, shrinkage 같은 장치를 함께 둔다. 출처: [Aggarwal, Neighborhood-Based Collaborative Filtering](https://link.springer.com/chapter/10.1007/978-3-319-29659-3_2)
:::

## 3. Normalization과 rating bias

### 강의에서의 서술

- 사람마다 평점을 관대하게/엄격하게 주기 때문에 사용자별 z-score 표준화를 적용할 수 있고, 데이터 특성에 따라 성능이 향상될 수 있다고 설명한다.
- 구매 여부 데이터는 0/1로 표현하고 같은 방식의 추천 문제로 볼 수 있다고 설명한다.

### official 근거

- Stanford CS246 review slides는 Pearson correlation을 "non-missing ratings의 mean을 제거한 zero-centered 방식"으로 설명하며, CF에서 baseline estimate를 제거하고 rating deviation을 모델링해 user/item bias 영향을 줄일 수 있다고 정리한다. [출처: Stanford CS246 2017 review slides, https://snap.stanford.edu/class/cs246-2017/slides/review.pdf]
- Aggarwal의 neighborhood chapter note도 Pearson coefficient가 row-wise mean-centered cosine과 연결됨을 설명한다. [출처: Aggarwal, "Neighborhood-Based Collaborative Filtering", https://link.springer.com/chapter/10.1007/978-3-319-29659-3_2]
- Gunawardana & Shani는 CF가 rating prediction뿐 아니라 binary selection/click 같은 추천 task로도 평가될 수 있음을 논한다. [출처: Gunawardana & Shani 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]

### 플래그

- z-score 표준화 후 예측값을 원래 평점 척도에서 해석하려면 보통 inverse transform 또는 평균/baseline 보정이 필요하다.
- 구매/클릭 0/1 데이터는 "평점 회귀"와 loss·평가지표가 달라진다. 0/1이면 MSE보다 log loss/BCE, AUC, precision@k/recall@k 같은 ranking/분류 지표가 더 직접적일 수 있다.

### callout 후보

::: {.callout-note title="평점 평균을 빼는 이유"}
추천 시스템의 rating은 사용자별 기준 차이가 크다. 어떤 사용자는 평균적으로 4점을 주고, 어떤 사용자는 좋은 영화에도 3점만 줄 수 있다. 그래서 similarity를 계산할 때 사용자 평균을 빼거나 baseline을 따로 모델링하면 "평점의 절대 크기"보다 "취향의 패턴"을 더 잘 비교할 수 있다. 출처: [Stanford CS246 review slides](https://snap.stanford.edu/class/cs246-2017/slides/review.pdf), [Aggarwal, Neighborhood-Based Collaborative Filtering](https://link.springer.com/chapter/10.1007/978-3-319-29659-3_2)
:::

## 4. Evaluation: RMSE/MAE와 precision@k

### 강의에서의 서술

- 전체 사용자 집합을 train/test로 나누고, test 사용자마다 일부 item만 알고 있다고 가정한 뒤 나머지 관측 평점을 가려 예측한다.
- 예측 평점과 실제 평점의 차이로 MAE, MSE, RMSE를 계산할 수 있다고 설명한다.
- PDF 예제는 MAE = 0.886, RMSE = 1.024를 제시한다.

### official 근거

- Aggarwal의 평가 chapter는 collaborative filtering 평가가 classification/regression 평가와 유사하다고 설명한다. [출처: Aggarwal, "Evaluating Recommender Systems", https://link.springer.com/chapter/10.1007/978-3-319-29659-3_7]
- Gunawardana & Shani는 offline evaluation metric 선택이 추천 알고리즘 선택에 결정적이며, RMSE는 predicted preference와 true preference 사이의 거리를 재고, recall은 선호 아이템 중 추천된 비율을 계산한다고 설명한다. 또한 recommendation task, utility optimization, rating prediction task를 구분한다. [출처: Gunawardana & Shani 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]
- Stanford CS246 slides도 known rating과 predicted rating을 비교해 RMSE를 계산하고, top-k 추천에서는 precision at top 10 같은 지표를 언급한다. [출처: Stanford CS246 2019, "Recommender Systems", https://snap.stanford.edu/class/cs246-2019/slides/07-recsys1.pdf]
- Recommender Systems Handbook 3판은 evaluation을 별도 파트로 두고, accuracy뿐 아니라 value, impact, fairness, novelty, diversity까지 다룬다. [출처: Ricci, Rokach, Shapira (eds.), *Recommender Systems Handbook*, https://link.springer.com/book/10.1007/978-1-0716-2197-4]

### 수식 후보

관측된 평가 쌍 집합을 $\Omega_{\text{test}}$라 하면:

$$
\operatorname{MAE}
= \frac{1}{|\Omega_{\text{test}}|}
\sum_{(u,i)\in \Omega_{\text{test}}}
|r_{ui} - \hat r_{ui}|
$$

$$
\operatorname{RMSE}
= \sqrt{
\frac{1}{|\Omega_{\text{test}}|}
\sum_{(u,i)\in \Omega_{\text{test}}}
(r_{ui} - \hat r_{ui})^2
}
$$

Top-k 추천에서 관련 아이템 집합을 $Rel_u$, 추천 상위 k개를 $Rec_u@k$라 하면:

$$
\operatorname{Precision@k}(u)
= \frac{|Rec_u@k \cap Rel_u|}{k}
$$

$$
\operatorname{Recall@k}(u)
= \frac{|Rec_u@k \cap Rel_u|}{|Rel_u|}
$$

### 플래그

- **MAE 명칭:** transcript에는 "Min Absolute Error"처럼 들리는 부분이 있으나 정확한 명칭은 **Mean Absolute Error**다. PDF는 약어 MAE만 제시한다.
- **RMSE/MAE의 범위:** RMSE/MAE는 rating prediction 성능을 보는 지표다. 실제 사용자에게 "상위 10개 중 좋은 것을 얼마나 잘 골랐는가"를 보려면 precision@k, recall@k, MAP, nDCG 같은 ranking 지표가 더 직접적이다.
- **평가 split:** 강의의 "이미 본 영화를 안 본 척하고 예측"하는 설명은 offline holdout evaluation으로 타당하다. 다만 무작위 holdout은 시간 순서와 실제 배포 상황을 왜곡할 수 있으므로, 실서비스 평가에서는 timestamp-based split 또는 online A/B test도 고려한다.

### callout 후보

::: {.callout-note title="RMSE가 낮아도 좋은 추천 리스트라는 보장은 없다"}
RMSE와 MAE는 예측 평점의 숫자 오차를 평가한다. 하지만 추천 서비스의 화면은 보통 "상위 k개 아이템"을 보여주므로, 사용자가 실제로 관심 가질 아이템이 top-k 안에 들어오는지가 더 중요할 수 있다. 이때는 precision@k, recall@k, nDCG 같은 ranking 지표를 함께 본다. 출처: [Gunawardana & Shani 2009](https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf), [Stanford CS246 2019 slides](https://snap.stanford.edu/class/cs246-2019/slides/07-recsys1.pdf)
:::

## 5. Cold Start와 Sparsity

### 강의에서의 서술

- 새로운 사용자나 새 영화는 평점 정보가 없어 similarity를 계산하기 어렵고, 이를 cold start 문제로 설명한다.
- 사용자-아이템 행렬은 대부분 비어 있으므로 sparse matrix이며, 채워진 비율이 낮으면 similarity 계산이 부정확해진다고 설명한다.
- NCF에서 side information을 사용하면 cold start를 완화할 수 있다고 설명한다.

### official 근거

- Sarwar et al.은 웹 규모 추천에서 high coverage를 data sparsity 상황에서 달성해야 하는 것이 핵심 challenge라고 설명하며, 전통적 CF는 참여자 수가 늘수록 작업량이 증가한다고 지적한다. [출처: Sarwar et al. 2001, https://doi.org/10.1145/371920.372071]
- Gunawardana & Shani는 Netflix dataset 예시에서 사용자가 전체 영화 중 작은 일부만 평가해 데이터가 매우 sparse하다고 설명한다. [출처: Gunawardana & Shani 2009, https://jmlr.csail.mit.edu/papers/volume10/gunawardana09a/gunawardana09a.pdf]
- Schein et al.은 cold-start recommendation을 명시적으로 다루며, community에서 아직 아무도 rating하지 않은 item을 추천하는 문제를 benchmark한다고 설명한다. [출처: Schein et al., "Methods and Metrics for Cold-Start Recommendations", SIGIR 2002/ACM, https://doi.org/10.1145/564376.564421]
- He et al. NCF의 기본 기여는 inner product를 neural architecture로 대체해 user-item interaction function을 학습하는 것이다. [출처: He et al. 2017, https://doi.org/10.1145/3038912.3052569]

### 플래그

- **NCF 자체가 cold start를 해결하는 것은 아니다.** 기본 NCF도 user ID/item ID embedding이 필요하므로 완전 신규 사용자·아이템에는 약하다. 강의의 설명처럼 side information을 받아 embedding을 생성하는 별도 network를 붙이면 완화할 수 있다.
- Cold start에는 new user, new item, new system이 구분된다. 강의는 new user/new item 중심이다.

### callout 후보

::: {.callout-note title="Cold start는 정보가 없는 행 또는 열의 문제"}
Collaborative filtering은 과거 상호작용으로 사용자와 아이템의 유사도를 학습한다. 새 사용자는 행(row)에 관측값이 거의 없고, 새 아이템은 열(column)에 관측값이 거의 없다. 그래서 기본 CF/MF/ID-embedding 기반 NCF는 cold start에 취약하다. 장르, 줄거리, 이미지, 사용자 프로필 같은 side information을 함께 쓰면 이 문제를 완화할 수 있다. 출처: [Schein et al. 2002](https://doi.org/10.1145/564376.564421), [He et al. 2017](https://doi.org/10.1145/3038912.3052569)
:::

## 6. Matrix Factorization / Latent Factor Model

### 강의에서의 서술

- 사용자-영화 평점 행렬 $R$을 사용자 latent factor 행렬 $U$와 아이템 latent factor 행렬 $V$의 곱 $R \approx UV^T$로 근사한다.
- $u_i$와 $v_j$의 내적이 사용자 $i$의 아이템 $j$에 대한 예측 평점이다.
- latent factor column의 의미는 장르처럼 해석될 수도 있지만, 일반적으로는 예측 성능을 위해 학습된 잠재 요인이라 의미 해석이 어렵다.
- 실제 평점이 존재하는 entry에 대해서만 오차를 계산하고, MSE를 줄이도록 $U,V$를 gradient descent 등으로 학습한다.
- PDF는 FunkSVD, ALS, gradient descent를 언급한다.
- MF는 CF보다 대규모 데이터에서 일반적으로 정확도가 높을 수 있지만 해석 가능성이 낮고, 학습 단계가 복잡하며 cold start는 여전히 남는다고 설명한다.

### official 근거

- Koren, Bell & Volinsky는 matrix factorization이 사용자와 아이템을 joint latent factor space로 mapping하고, 그 공간에서 user-item interaction을 내적으로 모델링한다고 설명한다. [출처: Koren, Bell & Volinsky 2009, https://doi.org/10.1109/MC.2009.263]
- Stanford CS246 latent factor slides는 예측을 $\hat r_{ui}=q_i \cdot p_u^T$로 쓰고, missing entry가 있는 추천 데이터에서는 일반 SVD가 그대로 정의되지 않으므로 관측 rating에 대한 특수 최적화 문제로 $P,Q$를 찾는다고 설명한다. [출처: Stanford CS246 2012, https://snap.stanford.edu/class/cs246-2012/slides/08-recsys2.pdf]
- Aggarwal의 model-based CF chapter는 matrix factorization, ALS, gradient descent 계열 방법을 model-based collaborative filtering의 핵심으로 다룬다. [출처: Aggarwal, "Model-Based Collaborative Filtering", https://link.springer.com/chapter/10.1007/978-3-319-29659-3_3]

### 수식 후보

관측 rating 집합을 $\Omega$라 하면 기본 latent factor model:

$$
\hat r_{ui} = p_u^T q_i
$$

정규화 없는 기본 목적함수:

$$
\min_{P,Q}
\sum_{(u,i)\in\Omega}
(r_{ui} - p_u^T q_i)^2
$$

정규화와 bias를 포함한 흔한 형태:

$$
\hat r_{ui}
= \mu + b_u + b_i + p_u^T q_i
$$

$$
\min_{P,Q,b}
\sum_{(u,i)\in\Omega}
(r_{ui} - \mu - b_u - b_i - p_u^T q_i)^2
+ \lambda(\|p_u\|^2 + \|q_i\|^2 + b_u^2 + b_i^2)
$$

### 플래그

- **SVD 용어:** "FunkSVD"는 추천 시스템 문맥에서 관측된 entry에 대한 low-rank factor를 학습하는 알고리즘 이름으로 쓰인다. 선형대수의 classical SVD처럼 완전한 행렬을 직교 행렬과 singular value로 분해하는 절차와는 다르다. 본 노트에 "그냥 SVD를 적용한다"라고 쓰면 missing entry 때문에 부정확하다.
- **latent factor 수:** 강의에서 "column 수가 많아지면 성능이 더 좋아질 것"이라고 직관적으로 말한 부분은 보완이 필요하다. factor 수가 커지면 train error는 줄 수 있지만, sparse data에서는 overfitting이 커져 test RMSE/ranking metric이 나빠질 수 있다. 정규화와 validation이 필요하다.
- **MF > CF:** 대규모 rating prediction에서 MF가 강력하다는 서술은 표준적이지만, 모든 데이터·모든 metric에서 항상 CF보다 낫다는 보장은 아니다.

### callout 후보

::: {.callout-note title="MF는 빈칸이 있는 행렬에 classical SVD를 그대로 적용하는 것이 아니다"}
추천 시스템의 평점 행렬은 대부분 비어 있기 때문에, 일반적인 SVD처럼 모든 entry가 알려진 행렬을 분해할 수 없다. Matrix factorization은 관측된 평점 쌍에 대해서만 오차를 계산하고, 그 오차가 작아지도록 사용자 벡터와 아이템 벡터를 학습한다. 출처: [Koren, Bell & Volinsky 2009](https://doi.org/10.1109/MC.2009.263), [Stanford CS246 latent factor slides](https://snap.stanford.edu/class/cs246-2012/slides/08-recsys2.pdf)
:::

## 7. NCF와 side information (강의 실제 토픽 보충)

### 강의에서의 서술

- MF의 $u_i, v_j$를 embedding vector로 해석하고, MF는 두 embedding의 내적으로 user-item interaction을 모델링한다고 설명한다.
- NCF는 embedding을 concat한 뒤 hidden layer를 통과시켜 비선형 관계를 학습한다고 설명한다.
- rating prediction은 MSE, 구매/클릭 0/1은 cross-entropy를 사용할 수 있다고 설명한다.
- side information을 embedding 생성 network에 넣으면 cold start를 완화할 수 있다고 설명한다.

### official 근거

- He et al.은 NCF를 "inner product를 neural architecture로 대체"해 data로부터 arbitrary function을 학습하는 framework로 제안한다. [출처: He et al. 2017, https://doi.org/10.1145/3038912.3052569]
- Recommender Systems Handbook 3판은 fundamental technique 중 하나로 neural networks를 포함하고, "Deep Learning for Recommender Systems" 장을 둔다. [출처: Ricci, Rokach, Shapira (eds.), *Recommender Systems Handbook*, https://link.springer.com/book/10.1007/978-1-0716-2197-4]

### 플래그

- 강의 transcript 말미에 "CF와 MF와 SF 세가지 방식"으로 들리는 부분은 맥락상 **CF, MF, NCF** 또는 STT 오인식 가능성이 높다. 노트에는 NCF로 정리.
- Side information은 NCF의 기본 ID embedding 구조와 별도의 확장이다. "NCF라서 cold start가 자동 해결된다"는 식으로 쓰지 말 것.

### callout 후보

::: {.callout-note title="NCF는 내적 대신 신경망으로 상호작용을 학습한다"}
Matrix factorization은 사용자 embedding과 아이템 embedding의 내적을 예측 점수로 쓴다. Neural collaborative filtering은 두 embedding을 이어 붙이고, 이를 여러 hidden layer에 통과시켜 더 복잡한 비선형 상호작용을 학습한다. 단, 완전 신규 사용자·아이템은 여전히 embedding을 만들어야 하므로 side information 없이는 cold start가 남는다. 출처: [He et al. 2017](https://doi.org/10.1145/3038912.3052569)
:::

## 8. 공식 이미지 후보와 라이선스 메모

이미지 파일은 직접 가져오지 않았다. 아래는 리뷰어가 본 노트에 이미지를 넣고 싶을 때 확인할 공식 후보와 라이선스 주의사항이다.

1. User/item CF와 similarity 도식
   - 후보: Stanford CS246 2019 "Recommender Systems" slides의 utility matrix, user-user/item-item CF, RMSE/precision 설명 슬라이드.
   - 출처: [Stanford CS246 2019 slides, https://snap.stanford.edu/class/cs246-2019/slides/07-recsys1.pdf]
   - 라이선스/주의: Stanford/Jure Leskovec course material. 명시적 오픈 라이선스 확인 전 직접 이미지 재배포보다 자체 Mermaid/표 재작성 권장.

2. Latent factor 2D map / MF 직관 도식
   - 후보: Stanford CS246 2012 "Recommender Systems: Latent Factor Models"의 latent factor map 및 $R \approx QP^T$ 도식.
   - 출처: [Stanford CS246 2012 slides, https://snap.stanford.edu/class/cs246-2012/slides/08-recsys2.pdf]
   - 라이선스/주의: Stanford/Jure Leskovec course material. 명시적 오픈 라이선스 확인 전 직접 이미지 삽입보다 자체 도식 재작성 권장.

3. Matrix factorization official paper figure
   - 후보: Koren, Bell & Volinsky 2009의 latent factor model 설명 그림.
   - 출처: [Koren, Bell & Volinsky, "Matrix Factorization Techniques for Recommender Systems", IEEE Computer, https://doi.org/10.1109/MC.2009.263]
   - 라이선스/주의: IEEE 저작권 자료. 직접 재배포는 IEEE permission/fair use 검토 필요. 노트에는 수식과 자체 도식으로 대체 권장.

4. NCF architecture figure
   - 후보: He et al. 2017의 GMF/MLP/NeuMF 구조 그림.
   - 출처: [He et al., "Neural Collaborative Filtering", WWW 2017/ACM, https://doi.org/10.1145/3038912.3052569]
   - 라이선스/주의: ACM 저작권 자료. 직접 재배포는 ACM permission/fair use 검토 필요. 노트에는 간단한 Mermaid flowchart 재작성 권장.

5. 교과서/핸드북 그림
   - 후보: Aggarwal textbook의 neighborhood-based CF, content-based, evaluation, model-based CF 관련 그림.
   - 출처: [Aggarwal, *Recommender Systems: The Textbook*, Springer, https://link.springer.com/book/10.1007/978-3-319-29659-3]
   - 라이선스/주의: Springer Nature Switzerland AG 2016. 직접 이미지 재배포는 Springer permission/fair use 검토 필요.

## 9. 사실 충돌/검수 플래그 요약

- item-based CF를 content-based filtering으로 오해하지 말 것.
- cosine similarity는 수학적으로 `[-1,1]`이지만, 양수 rating만 쓰면 보통 `[0,1]`; 음수는 centered vector에서 가능.
- 공통 평가 item이 1개인 사용자는 cosine이 1이 되어 neighbor로 쓰기 어렵고, Pearson은 undefined에 가깝다.
- transcript의 "Min Absolute Error"는 정확히 **Mean Absolute Error**.
- RMSE/MAE는 rating prediction 지표이고, 추천 리스트 품질에는 precision@k/recall@k/nDCG 등 ranking metric을 별도로 설명하는 것이 좋다.
- classical SVD와 recommender MF/FunkSVD를 혼동하지 말 것. missing entry가 있는 행렬에는 관측 entry 기반 최적화로 설명해야 한다.
- latent factor 수를 늘리면 무조건 좋아지는 것이 아니라 overfitting 위험이 커진다.
- NCF가 cold start를 자동 해결하는 것이 아니라, side information을 결합한 확장 구조가 완화책이다.

