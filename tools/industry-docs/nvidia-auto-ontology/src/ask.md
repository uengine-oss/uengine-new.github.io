# 질문하기

> Chat에 튜토리얼의 질문 네 개를 입력하고, 모델이 실제로 낸 답과 SQL·걸린 시간을 확인합니다. README가 적은 Q1의 답은 $588.80인데, 이 교재의 실행(gpt-6.1-sol)은 컴파일 직후의 의미 계층으로는 그 값을 내지 못했습니다. 그 이유를 SQL로 확인하고, 「매출」의 정의를 SQL 속성으로 만든 뒤 다시 물어 588.80을 얻습니다.

## 무엇을 · 왜

README는 질문 하나에 에이전트가 하는 일을 다섯 단계로 적습니다. 질문의 의도를 분류하고 개체를 추출하고 → 임베딩 검색으로 후보 용어·열·SQL 속성을 찾고 → SQL을 쓰고 → 필터 값과 질의를 DB와 대조해 검사하고, 검사에 실패하면 SQL을 고치고 → 실행해 SQL·단계와 함께 답합니다. Chat 화면의 답 상자에는 진행 단계, 설명 문장, **SQL**, **Query results**가 차례로 나옵니다. 답이 맞는지는 SQL을 읽어야 알 수 있습니다.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**새 대화를 엽니다.** Chat(왼쪽 맨 위) → **New Chat**. 질문마다 새 대화를 열어야 앞선 질문이 다음 질문에 영향을 주지 않습니다. 이 화면의 대화는 앞선 다섯 턴까지를 맥락으로 사용해 후속 질문을 재작성합니다.
</li>
<li markdown="1">**Q1을 묻습니다.** 입력칸에 질문을 넣고 Enter를 누릅니다.

```text
What was revenue for the USB food flash drive - sushi roll in Pennsylvania in June 2015?
```

답을 만드는 동안 「Classifying the question → Understanding the question → Retrieving candidates → Preparing candidates …」 단계가 하나씩 체크되고, 오른쪽 빨간 정지 단추로 멈출 수 있습니다.

![Q1을 묻는 중 — 진행 단계와 정지 단추](img/nv-ask-working.webp)
</li>
<li markdown="1">**답의 SQL을 읽습니다.** 아래 「모델이 실제로 낸 답」 표와 견줘 봅니다.

![Q1의 답 — 설명, SQL, 결과(이번 실행에서는 빈 값)](img/nv-ask-q1.webp)
</li>
<li markdown="1">**나머지 질문도 새 대화에서 묻습니다.** Q1 한국어, Q2, ROAS 순서로 묻습니다.

```text
2015년 6월 펜실베이니아에서 USB food flash drive - sushi roll 의 매출은 얼마였나?
Which products drive the most revenue and highest customer count?
What was return on ad spend for the sushi roll flash drive in June 2015?
```

![Q2의 답 — 매출 순 상품 목록](img/nv-ask-q2.webp)

![ROAS의 답 — 광고비 데이터가 없어 계산할 수 없다고 답함](img/nv-ask-roas.webp)
</li>
</ol>

## 모델이 실제로 낸 답

화면의 모든 답은 OpenAI **gpt-6.1-sol**(추론 강도 기본값)이 냈습니다. 중계기 기록으로 질문마다 모델 이름을 확인했습니다. 정답 $588.80은 원천에서 README의 SQL을 그대로 돌려 다시 확인한 값입니다(송장 줄 3개, 세금 포함 합계 588.80, 세금 76.80, 세금 뺀 합계 512.00).

| 질문 | 걸린 시간 | 모델 호출 | 답 | 판정 |
|---|---|---|---|---|
| Q1 | 68.6초 | 10번 | 「Customers 표가 없어 펜실베이니아 매출을 계산할 수 없다」며 빈 값 | 틀림 |
| Q1 한국어 | 79.4초 | 11번 | 512 | 틀림(세금 뺀 값) |
| Q2 | 38.6초 | 7번 | 상품 227개를 매출 순으로 나열(1위 Air cushion machine (Blue)) | 대체로 맞음(매출·고객 수 숫자는 안 보여 줌) |
| ROAS | 224.6초 | 33번 | 광고비와 광고 기여 매출이 없어 계산할 수 없다 | 맞음(지어내지 않음) |

**Q1이 틀린 까닭.** 두 가지가 겹쳤습니다.

1. **매출의 정의.** 화면과 API에서 물은 네 번 모두 매출을 `extendedprice - taxamount`(세금 뺀 값)로 계산했습니다. README의 답은 `SUM(extendedprice)`(세금 포함, 열 속성 이름도 「Line Total Including Tax」)입니다. 512.00은 세금 76.80을 뺀 값입니다. 의미 계층에 「매출」을 정한 SQL 속성이 없어서([3장](compile.html)) 모델이 고른 것입니다.
2. **연결 경로.** 영어 Q1은 `sales.customers`가 있고 `customers.deliverycityid → cities` 조인도 있는데 「Customers 표가 없다」고 판단해 `AND FALSE`로 빈 값을 냈습니다. 검색 단계에서 Customer 용어가 후보에 오르지 않은 것으로 보입니다. 한국어 Q1은 반대로 website 스키마의 고객 배송 좌표를 주(州) 경계 다각형과 대조하는 SQL을 짜서, 경로는 달랐지만 같은 512를 냈습니다.

같은 질문을 API로 따로 물었을 때도 Q1은 영어·한국어 모두 512.0이었습니다. 11월 14일에는 gpt-4.1이 물을 때마다 다른 오답(1,373.68 · 147.20 · 빈 결과 · 0.00 · 128)을, gpt-6.1-sol이 「답 없음」과 441.60을 냈습니다. **SQL 속성을 더하기 전에는 README의 $588.80이 한 번도 나오지 않았습니다.** README의 예시는 NVIDIA 기본 모델로 만든 것이고, 모델이 바뀌면 답이 달라질 수 있습니다.

### 걸린 시간과 추론 강도

gpt-6.1-sol은 답을 작성하다 검사에 실패하면 SQL을 다시 짜는데, 이 과정이 반복되면 질문 하나에 몇 분이 걸립니다. 추론 강도(`reasoning_effort`)를 낮추면 나아지는지 같은 질문 네 개를 API로 한 번씩 측정해 보았습니다.

| 질문 | 기본 강도 | `low` |
|---|---|---|
| Q1 | 238.4초 · SQL 다시 짜기 8번 · 512.0 | 39.9초 · 1번 · 128.0 |
| Q1 한국어 | 90.2초 · 1번 · 512.0 | 34.1초 · 0번 · 빈 값 |
| Q2 | 47.7초 · 0번 · 목록 | 37.2초 · 0번 · 목록 |
| ROAS | 121.6초 · 5번 · 계산 못 함(이유 설명) | 204.9초 · 14번 · 「SQL can't be constructed from the data.」 |

`low`는 쉬운 질문의 응답 속도를 높였지만 답이 더 나빠졌고, ROAS는 오히려 재작성을 더 오래 반복했습니다. 그래서 이 교재의 화면은 **기본 강도**로 찍었습니다. 한 번씩만 측정한 값이라 편차는 모릅니다. Auto Ontology 1.2.0에는 추론 강도 설정이 없어서, 이 값은 모델 앞의 중계기에서 붙였습니다.

## 매출의 정의를 SQL 속성으로 정하기

README의 인증 단계는 "Refine terms, descriptions, and SQL attributes"입니다. Q1이 틀린 첫째 까닭인 「매출의 정의」를 SQL 속성으로 정하고 다시 물어봅니다.

<ol class="steps" markdown="1">
<li markdown="1">**Invoice Line 용어에 SQL 속성을 만듭니다.** Terms → Invoice Line → **Create New SQL Attribute**. 이름·설명·SQL을 넣고 **Validate SQL**로 「SQL is valid.」를 확인한 뒤 **Create**를 누릅니다.

| 칸 | 값 |
|---|---|
| Attribute Name | `Revenue` |
| Description | `Revenue of invoice lines including tax: the sum of extendedprice (Line Total Including Tax). Use this measure whenever a question asks for revenue or sales.` |
| SQL | `SELECT SUM(il.extendedprice) AS revenue FROM sales.invoicelines AS il` |

![SQL 속성 만들기 — 검사 결과 「SQL is valid.」](img/nv-fix-attr.webp)
</li>
<li markdown="1">**인증합니다.** SQL Attributes 표의 Revenue 줄에서 방패 단추 → **Certified**를 선택합니다.

![Revenue SQL 속성을 Certified로](img/nv-fix-certified.webp)
</li>
<li markdown="1">**Q1을 새 대화에서 다시 묻습니다.**

이번에는 **176.0초**(모델 호출 23번, gpt-6.1-sol 기본 강도) 만에 **REVENUE 588.80**이 나왔습니다. SQL은 `SUM(extendedprice)`이고, 연결 경로도 README와 같습니다(송장 줄 → 송장 → 고객 → 도시 → 주). 설명 문장에는 여전히 「Customers 표가 허용된 정의에 없으니 접근 권한을 확인하라」는 단서가 붙었지만, 질의는 그 표를 조인해 실행되었습니다.

![SQL 속성을 만든 뒤의 Q1 — REVENUE 588.80](img/nv-fix-q1.webp)

지표의 정의 하나를 사람이 정해 주자 답이 README와 같아졌습니다. 반대로 말하면, 컴파일이 만든 초안만으로는 「매출」처럼 정의가 갈리는 질문을 믿고 맡기기 어렵습니다. README가 「만들기 → 인증하기 → 답하기」에서 가운데 단계를 사람의 몫으로 둔 까닭입니다. 다만 한 번 물어본 결과이므로, 실제로 쓸 때는 같은 질문을 여러 번 물어 답이 흔들리지 않는지 확인하세요.
</li>
</ol>

## 막히면

!!! warning "막히면"
    - **답이 몇 분째 안 옴, 단계에 SQL 다시 짜기가 되풀이됨** — 추론 모델이 검사를 통과하지 못하는 SQL을 거듭 냅니다. → 기다리거나 빨간 정지 단추로 멈추고 질문을 더 구체적으로(열·조건 이름을 넣어) 다시 묻습니다. API·MCP의 시간 제한은 넉넉히(900초) 둡니다. `reasoning_effort=low`는 빨라지지만 답이 나빠질 수 있습니다.
    - **같은 질문인데 물을 때마다 답이 다름** — 모델이 지표 정의와 연결 경로를 질문마다 새로 고릅니다. → 자주 묻는 지표는 SQL 속성으로 정의하고 설명에 언제 쓰는지 적습니다.
    - **`Unsupported value: 'reasoning_effort' does not support 'none' with this model.`** — gpt-6.1-sol은 `low`·`medium`·`high`·`xhigh`만 받습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>1. 512.00과 588.80은 무엇이 다른가요? 어느 값이 맞는지는 무엇으로 정해야 하나요?</summary>

588.80은 `extendedprice`(세금 포함 줄 합계)의 합이고, 512.00은 거기서 세금 76.80을 뺀 값입니다. 둘 다 「매출」로 부를 수 있으므로 데이터만으로는 정할 수 없습니다. 회사의 정의를 SQL 속성으로 적고 인증해 두어야 합니다.
</details>

<details class="answer" markdown="1">
<summary>2. ROAS 질문에서 「계산할 수 없다」는 답이 왜 맞는 답인가요?</summary>

WWI에는 광고비 데이터가 없습니다. 있는 데이터로 숫자를 지어내지 않고 무엇이 없어서 계산할 수 없는지를 밝힌 것이 맞는 답입니다. README 6단계가 기대하는 동작이기도 합니다.
</details>

다음 장에서는 같은 의미 계층을 MCP 서버로 Claude Code에 붙입니다.
