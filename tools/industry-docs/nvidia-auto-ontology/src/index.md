# 시작하기: 무엇을 배우나

> NVIDIA Auto Ontology는 데이터베이스의 메타데이터를 읽어 용어·관계·SQL 속성으로 구성된 의미 계층(온톨로지)을 만들고, 에이전트가 그 의미 계층을 참조해 SQL을 작성하고 답하게 하는 오픈소스 라이브러리입니다. NVIDIA README의 Quickstart 예제(Wide World Importers)를 처음부터 따라 하며 연결 → 의미 계층 컴파일 → 둘러보기 → 질문 → MCP·API 연동까지 실제로 실행해 봅니다.

!!! note "uEngine의 독립 교육 자료입니다"
    이 교재는 uEngine AX School이 만든 독립 교육 자료입니다. NVIDIA와 제휴하거나 NVIDIA의 승인·후원을 받은 자료가 아닙니다. NVIDIA는 NVIDIA Corporation의 상표이며, 그 밖의 제품 이름과 상표는 각 소유자에게 귀속됩니다. NVIDIA Auto Ontology는 Apache License 2.0으로 공개된 소프트웨어이고, 이 교재에 인용한 문장은 출처를 밝혀 원문 그대로 옮겼습니다.

## 무엇을 · 왜

에이전트에게 데이터베이스를 열어 주면 SQL을 작성해 답합니다. 문제는 그 숫자가 맞는지입니다. 「매출」이 어떤 표의 어떤 열을 뜻하는지, 고객과 도시를 어떤 열로 이어야 하는지를 모르면 그럴듯하지만 틀린 숫자가 나옵니다. NVIDIA는 README 첫머리에서 이 문제를 이렇게 설명합니다.

> "Agents need a context layer that tells them where data lives, what it means, whether to use it, how to use it, where it came from, and what is similar. NVIDIA Auto Ontology is an open library that builds that layer from enterprise metadata, reconciles definitions across systems, and exposes it to any agent harness through MCP, CLI, and API."
>
> — [NVIDIA/auto-ontology README](https://github.com/NVIDIA/auto-ontology) (1.2.0, 커밋 c447003)

우리말로 옮기면 이렇습니다. 에이전트에게는 데이터가 어디에 있는지, 무엇을 뜻하는지, 사용해도 되는지, 어떻게 쓰는지, 어디서 왔는지, 비슷한 데이터는 무엇인지 알려 주는 맥락 계층이 필요합니다. Auto Ontology는 기업 메타데이터에서 그 계층을 만들고, 시스템마다 다른 정의를 조정하고, MCP·CLI·API로 어떤 에이전트에게나 제공합니다.

## Auto Ontology가 하는 일

README는 동작을 세 단계로 나눕니다. "Auto-Ontology works in three stages: it generates an ontology, people certify it, and the agent answers questions from it."

| 단계 | 하는 일 | 이 교재의 장 |
|---|---|---|
| **만들기**(Generate) | 원천 DB의 스키마를 읽고 열을 표본 조사한 뒤, 표마다 업무 용어(Term)를 추출하고 표 사이의 조인을 추론해 의미 계층 초안을 작성합니다 | [2장 연결](connect.html) · [3장 컴파일](compile.html) |
| **인증하기**(Certify) | 사람이 초안을 실제 질문으로 시험하고, 설명·SQL 속성을 고친 뒤 인증합니다 | [3장](compile.html) · [4장 둘러보기](explore.html) |
| **답하기**(Answer) | 질문에서 개체를 뽑아 용어·열·SQL 속성을 찾고, SQL을 짜서 검사·실행한 뒤 SQL과 단계를 함께 돌려줍니다 | [5장 질문](ask.html) |

의미 계층에는 세 가지가 들어갑니다.

| 정의 | 뜻 | 예 (Wide World Importers) |
|---|---|---|
| **용어**(Term) | 업무 개념 하나. 설명·동의어와 그 개념을 담은 열이 붙습니다 | Invoice Line, Customer, Stock Item |
| **SQL 속성**(SQL attribute) | 용어에 연결된 검토 완료 SQL 식. 에이전트가 같은 식을 다시 써서 지표를 늘 같은 방법으로 계산합니다 | 이익률, 누적 합계 |
| **관계**(Relationship) | 표를 연결하는 방법. 키와 데이터에서 추론합니다 | invoicelines.invoiceid → invoices.invoiceid |

만든 의미 계층은 웹 화면(Chat·용어·그래프)뿐 아니라 [MCP 서버](mcp.html)와 [REST API](api.html)로도 다른 도구에 제공합니다.

## 예제: Wide World Importers

Microsoft가 공개한 가상 도매 회사의 판매·구매·창고 데이터입니다. NVIDIA는 이 데이터를 PostgreSQL에 넣는 스크립트(`auto-ontology-eval`의 `seed_wwi.py`)를 함께 공개했습니다. 데이터를 넣으면 스키마 5개(application·purchasing·sales·warehouse·website)에 표 48개와 뷰 3개가 생깁니다. 외래 키는 선언되어 있지 않아서, 표를 어떻게 이을지는 Auto Ontology가 데이터에서 추론해야 합니다.

이 교재에서 묻는 질문은 넷입니다. README Quickstart의 두 질문과, 11월 14일 비교에서 함께 사용한 두 질문입니다.

| 번호 | 질문 | 기대하는 답 |
|---|---|---|
| Q1 | What was revenue for the USB food flash drive - sushi roll in Pennsylvania in June 2015? | **$588.80**, 송장 줄 3개 (README에 적힌 답) |
| Q1 한국어 | 2015년 6월 펜실베이니아에서 USB food flash drive - sushi roll의 매출은 얼마였나? | 위와 같음 |
| Q2 | Which products drive the most revenue and highest customer count? | 매출 상위 상품과 고객 수 (README 그림의 질문) |
| ROAS | What was return on ad spend for the sushi roll flash drive in June 2015? | 광고비 데이터가 없으므로 **답할 수 없다**고 해야 맞습니다 (README 6단계) |

## 장 목록

| 장 | 하는 일 |
|---|---|
| [1. 설치와 실행](setup.html) | 공식 Quickstart(Docker Compose)와, 이 교재의 화면을 찍은 방식(Docker 없이 직접 실행·OpenAI 모델) |
| [2. 데이터베이스 연결](connect.html) | 읽기 전용 계정을 만들고 Settings → Connections에서 WWI를 연결해 적재 |
| [3. 의미 계층 컴파일](compile.html) | Semantic Compilation을 켜고 용어·조인이 자동으로 생기는 과정과 검토할 곳 |
| [4. 그래프·용어 둘러보기](explore.html) | 용어 목록, 용어 상세, 의미 그래프, 데이터 카탈로그 |
| [5. 질문하기](ask.html) | 질문 네 개를 Chat에 묻고, 모델이 실제로 낸 답과 SQL·시간을 확인 |
| [6. MCP로 다른 도구에 붙이기](mcp.html) | Claude Code를 OAuth로 MCP 서버에 연결해 `check_answerable`·`ask_question` 호출 |
| [7. API로 다른 시스템과 연동](api.html) | API 토큰을 만들고 짧은 파이썬 스크립트로 용어 검색·답변 가능성·질문 스트림 받기 |
| [8. Ontological Studio 소개와 비교](studio.html) | 같은 원천·같은 질문으로 해 본 uEngine Ontological Studio와의 가벼운 비교 |
| [부록. 문제 해결](troubleshooting.html) | 따라 하다 막히는 곳과 조치, 예외 상황, 이 교재를 찍은 환경 |

## 준비물

| 구분 | 공식 Quickstart 기준 |
|---|---|
| 실행 | Docker(Compose v2), [uv](https://docs.astral.sh/uv/), Git |
| 모델 | NVIDIA API 키(`nvapi-…`, [build.nvidia.com](https://build.nvidia.com)) — 또는 구조화 출력을 지원하는 OpenAI 호환 엔드포인트 |
| 연동 실습 | MCP 클라이언트(Claude Code·Cursor·Claude Desktop 중 하나), Python 3과 `requests` |

## 이 교재의 화면과 숫자

화면과 수치는 2026년 11월 15일에 NVIDIA Auto Ontology 1.2.0(커밋 c447003)을 실제로 실행해 얻었습니다. 공식 Quickstart와 다른 점이 두 가지 있습니다. NVIDIA API 키 없이 **OpenAI `gpt-6.1-sol` 모델**을 연결했고, Docker 대신 **각 서비스를 이 PC에서 직접** 띄웠습니다. 그래서 화면의 주소가 공식 문서의 `:3000` 대신 `:3100`입니다. 자세한 차이는 [1장](setup.html)과 [부록의 「이 교재를 찍은 환경」](troubleshooting.html)에 적었습니다.

모델이 작성하는 SQL과 답은 실행할 때마다 달라질 수 있습니다. 그래서 5장의 답 화면마다 그 답을 낸 모델과 추론 강도를 함께 표시했습니다. 기본 모델인 NVIDIA Nemotron으로 실행하면 결과가 다를 수 있습니다.

먼저 [1장 설치와 실행](setup.html)에서 서비스 구성과 공식 설치 순서를 봅니다.
