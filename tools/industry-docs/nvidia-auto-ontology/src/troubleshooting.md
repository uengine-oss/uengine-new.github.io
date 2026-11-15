# 문제 해결

> 이 교재를 만들며 설치·실행·연결·컴파일·질문·MCP·API·녹화 단계에서 실제로 막혔던 곳과 조치를 모았습니다. 증상의 오류 문구는 화면과 기록에 나온 그대로 옮겼고, 조치를 다시 일으켜 확인했는지도 함께 적었습니다.

모두 24건입니다. 학습자도 겪을 수 있는 것 17건, 이 교재를 찍은 환경에서만 생긴 것 7건, 조치를 다시 확인하지 못한 것 11건, 제품 결함 후보 3건입니다. 원자료는 이 교재 원고 옆의 `issues.json`입니다.

## 단계별

### 설치·실행

- **모델 설정(.env)을 OpenAI로 바꿀 때** (1장)  
  증상: OpenAI가 `invalid model ID` 로 거절한다(모델 이름에 `openai/` 접두사를 붙였을 때).  
  원인: Auto Ontology는 모델 이름이 `openai/`·`azure/`·`aws/`로 시작해야 ChatOpenAI(구조화 출력 지원) 경로를 사용한다(auto_ontology/utils/llm_invoke.py). 그 이름을 그대로 OpenAI로 보내면 OpenAI는 접두사가 붙은 이름을 인식하지 못한다.  
  조치: OpenAI 호환 게이트웨이(LiteLLM 등)나 작은 중계기에서 `openai/` 접두사를 떼고 넘긴다. 이 교재는 run/openai_shim.py(:3109)를 썼고, .env는 `DEFAULT_MODELS_ENDPOINT=http://127.0.0.1:3109/v1`, `REASONING_MODEL=openai/gpt-6.1-sol`.  
  확인: 확인함 — 2026-11-15 OpenAI API에 model=openai/gpt-4.1로 보내 `invalid model ID` 확인, 중계기 경유로 컴파일·질문 성공

- **gpt-5/6 계열 OpenAI 모델을 연결할 때** (1장)  
  증상: `Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.`  
  원인: Auto Ontology가 쓰는 ChatOpenAI 클라이언트가 `max_tokens`를 보낸다. 최신 추론 모델은 `max_completion_tokens`만 받는다(temperature는 NVIDIA 코드가 이미 빼고 보낸다).  
  조치: 중계기·게이트웨이에서 `max_tokens`를 `max_completion_tokens`로 바꿔 넘긴다(이 교재의 run/openai_shim.py가 하는 일). 같은 모델에 `temperature: 0`을 보내면 `Only the default (1) value is supported.`로도 거절되니 함께 뺀다.  
  확인: 확인함 — 2026-11-15 gpt-6.1-sol에 max_tokens·temperature=0을 보내 두 오류 원문 확인, 중계기 경유로 정상

- **재순위(RERANK) 모델** (1장)  
  증상: OpenAI 에 `/v1/rerank` 를 보내면 HTTP 404.  
  원인: OpenAI에는 재순위 API가 없다. Auto Ontology는 컴파일 중 다리(bridge) 테이블 SQL 속성 후보를 고를 때 RERANK를 부른다.  
  조치: 재순위 모델이 있는 엔드포인트(NVIDIA NIM 등)를 `RERANK_ENDPOINT`·`RERANK_MODEL`에 따로 준다. 이 교재는 중계기가 임베딩 코사인 유사도로 흉내 냈다(RERANK_ENDPOINT=http://127.0.0.1:3109/v1/rerank).  
  확인: 확인함 — 2026-11-15 api.openai.com/v1/rerank → 404 확인. WWI는 이번 컴파일에서 다리 테이블 후보가 없어 재순위가 쓰이지 않았다

- **임베딩 모델을 OpenAI로 바꿀 때** (1장)  
  증상: 임베딩을 저장하는 단계에서 벡터 차원이 맞지 않는다는 오류로 적재가 실패한다(오류 원문은 이번 실행에서 다시 확인하지 못했다).  
  원인: Auto Ontology의 벡터 저장소는 2048차원을 기본으로 쓴다(auto_ontology/vdb/postgres.py `vector_size` 2048). text-embedding-3-large의 기본 출력은 3072차원이다.  
  조치: 임베딩 요청에 `dimensions: 2048`을 붙여 보낸다(중계기에서). 적재와 질문에 같은 임베딩 모델을 쓴다 — 바꾸면 의미 계층을 초기화(Settings → Semantic Compilation → Reset)하고 다시 컴파일한다.  
  확인: **확인 못 함** — 2026-11-09 실험에서 겪고 중계기로 고침. 이번(11-15)에는 다시 재현하지 않았다 — 오류 원문은 기억에 의존

- **다시 띄운 뒤 웹 화면 열기** (1장)  
  증상: 웹 화면이 왼쪽 세로 메뉴 없이 뜬다.  
  원인: README 안내: 브라우저에 이전 세션 쿠키가 남아 있다.  
  조치: 브라우저에서 localhost:3000(이 교재는 :3100)의 사이트 데이터를 지우고 다시 로그인한다. 그 밖의 설치 문제는 skills/nvidia-ontology-setup/references/troubleshooting.md.  
  확인: **확인 못 함** — README의 안내를 옮김. 이번 실행에서는 겪지 않았다

- **docker compose up** (1장 · 제품 결함 후보)  
  증상: docker-compose.yml 이 백엔드 "3001:3001"·적재 서비스 "3002:3002" 를 호스트에 그대로 연다.  
  원인: README는 3001·3002를 사설망에 두라고 하지만(백엔드는 사용자 머리글을 검증 없이 신뢰하고, 적재 서비스는 인증이 없다) Compose 파일은 두 포트를 모든 주소에 공개한다.  
  조치: 공유망·서버에서 돌릴 때는 docker-compose.yml의 두 줄을 "127.0.0.1:3001:3001"·"127.0.0.1:3002:3002"로 바꾸거나 ports를 지우고, 방화벽으로 막는다.  
  확인: **확인 못 함** — compose 파일(1.2.0)을 읽어 확인. Docker로 띄워 바깥에서 접속해 보지는 않았다


### 연결

- **연결을 화면과 .env 두 곳에서 줄 때** (2장)  
  증상: 화면(Settings → Connections)에서 만든 연결이 적재되지 않거나, 질문은 다른 연결로 답한다.  
  원인: 공식 문서(docs/connections.md): 질문은 화면 연결이 있으면 그것을, 적재는 `CONNECTION_STRINGS`가 있으면 그것만 쓴다. 두 방식을 섞으면 우선순위가 엇갈린다.  
  조치: 한 배포에서 한 가지만 쓴다. 화면으로 연결하려면 .env의 `CONNECTION_STRINGS=`를 비운다(이 교재). 공식 Quickstart처럼 .env로 주면 화면에서는 연결을 만들지 않는다.  
  확인: **확인 못 함** — 문서와 적재 로그(`ingest: no connections configured`)로 확인. 둘을 섞어 의도적으로 충돌을 일으켜 보지는 않았다

- **Docker Compose에서 화면으로 연결 만들기** (2장)  
  증상: Test Connection 이 실패한다(Host 에 localhost 를 넣었을 때).  
  원인: 웹 앱·백엔드가 컨테이너 안에서 실행된다. 컨테이너 안의 localhost는 그 컨테이너 자신이다.  
  조치: Compose의 PostgreSQL은 Host postgres, Port 5432로 넣는다(공식 CONNECTION_STRINGS 예 postgresql://postgres:…@postgres:5432/wideworldimporters와 같은 값).  
  확인: **확인 못 함** — Docker를 쓰지 않아 겪어 보지 못했다. 공식 .env 예와 Compose 구성으로 추론


### 구축

- **용어·SQL 속성 인증** (3장 · 제품 결함 후보)  
  증상: 용어·SQL 속성을 인증(Certified)해도 질문 답이 인증된 정의를 우선해 쓰는지 화면에서 알 수 없다.  
  원인: 1.2.0 질문 에이전트 코드(auto_ontology/retrieval)에서 인증 상태를 참조하는 곳을 찾지 못했다. 인증은 사람에게 보이는 검토 표시로 쓰인다. README의 Validate 항목은 "check generated queries against certified definitions"라고 적었다.  
  조치: 답을 고정하려면 인증 표시만으로는 부족하다 — 지표는 SQL 속성으로 정의하고 설명에 사용 조건을 적는다(5장 끝). 인증은 검토가 끝났다는 기록으로 쓴다.  
  확인: **확인 못 함** — 2026-11-15 retrieval 코드를 grep해 확인(literal_check.py 주석 한 곳뿐). 인증 전후로 같은 질문을 돌려 비교하지는 않았다


### 질의

- **추론 강도(reasoning_effort)를 낮출 때** (5장)  
  증상: `Unsupported value: 'reasoning_effort' does not support 'none' with this model. Supported values are: 'low', 'medium', 'high', and 'xhigh'.`  
  원인: gpt-6.1-sol은 none·minimal을 받지 않는다. Auto Ontology 1.2.0에는 추론 강도 설정이 없어 중계기에서 붙여야 한다.  
  조치: 중계기·게이트웨이에서 `reasoning_effort: "low"`처럼 지원하는 값만 붙인다. 이 교재: `SHIM_REASONING_EFFORT=low bash run/start-course.sh shim`  
  확인: 확인함 — 2026-11-15 none·minimal 거절, low·medium 정상 응답 확인

- **Chat에 질문(추론 모델 gpt-6.1-sol)** (5장)  
  증상: 답이 몇 분 걸린다. 진행 단계에 SQL 다시 짜기(reconstruct_sql)·검사(validate_sql_query)가 여러 번 되풀이된다. 이번 실행: Q1 영어 238.4초(다시 짜기 8번), ROAS 121.6초(5번).  
  원인: Auto Ontology의 질문 에이전트는 SQL을 검사하고 실패하면 다시 짠다. 추론 모델은 한 번 호출할 때마다 추론에 시간이 걸리고, 검사를 통과하지 못하는 SQL을 거듭 내면 반복 과정이 길어진다. 1.2.0에는 추론 강도 설정이 없다.  
  조치: ① 게이트웨이·중계기에서 reasoning_effort=low를 붙이면 간단한 질문은 34~40초로 빨라진다(이번 실행). 다만 답이 달라졌고(Q1 128.0·빈 값), ROAS는 오히려 다시 짜기 14번·204.9초 끝에 "SQL can't be constructed from the data."로 끝났다 — 이 교재는 기본 강도를 썼다. ② MCP·API의 시간 제한은 넉넉히(README 예 timeout=900초, MCP AUTO_ONTOLOGY_MCP_CHAT_TIMEOUT_S 기본 900). ③ 빠른 비추론 모델을 NON_REASONING에 따로 준다(이번에는 재지 않음).  
  확인: 확인함 — 2026-11-15 같은 질문 4개를 기본 강도·low로 한 번씩 측정해 비교(measure/sol-default.json · sol-low.json). 한 번씩만 측정해 편차는 알 수 없다

- **README Quickstart의 Q1 묻기** (5장)  
  증상: README 의 답 $588.80 대신 512(세금 뺀 값)나 빈 값이 나온다. 빈 값일 때 설명: "Pennsylvania revenue cannot be calculated from the supplied tables because the Customers table needed to link invoices to delivery locations is missing."  
  원인: 의미 계층에 「매출」을 정한 SQL 속성이 없어(컴파일은 질의 기록이 없으면 SQL 속성을 만들지 않는다) 모델이 extendedprice - taxamount를 매출로 골랐다. 영어 질문에서는 Customer 용어가 후보에 오르지 않아 표가 없다고 판단했다.  
  조치: Terms → Invoice Line → Create New SQL Attribute: 이름 Revenue, 설명 "Revenue of invoice lines including tax: the sum of extendedprice (Line Total Including Tax). Use this measure whenever a question asks for revenue or sales.", SQL `SELECT SUM(il.extendedprice) AS revenue FROM sales.invoicelines AS il` → Validate SQL → Create → Certified. 새 대화에서 다시 묻는다.  
  확인: 확인함 — 2026-11-15 SQL 속성을 만들기 전 Q1을 네 번 질문한 결과(화면 2·API 2) 모두 512.0 또는 빈 값, 속성을 만든 뒤 한 번 물어 REVENUE 588.80(176초). 속성을 만든 뒤에는 한 번만 물어 편차는 알 수 없다

- **Revenue SQL 속성을 만든 뒤 Q1 다시 묻기(화면·API·MCP)** (6장)  
  증상: 같은 Q1 이 화면(176.0초)과 API(102.7초)에서는 588.80, MCP ask_question(83.4초)에서는 빈 값(deliveryinstructions LIKE '%Pennsylvania%' 로 거름). 세 답의 설명 모두 "Customers is absent from the allowed table list" 같은 단서가 붙었다.  
  원인: 지표 정의(SQL 속성)는 쓰였지만, 주(州)를 찾는 경로는 여전히 모델이 질문마다 고른다. 질의 후보에 sales.customers가 잘 오르지 않는 것으로 보인다 — website 스키마의 고객 뷰가 따로 용어 'Customer (wideworldimporters.website.customers)' 가 된 것이 원인일 수 있다(확인 못 함).  
  조치: 자주 묻는 질문은 여러 번 물어 답이 일관되는지 확인한다. 필요한 경로를 담은 SQL 속성(예: 주별 매출)을 더 만들거나, 연결의 스키마 허용 목록에서 website 뷰를 빼고 다시 컴파일해 본다(이번에는 해 보지 않음).  
  확인: **확인 못 함** — 2026-11-15 세 경로로 한 번씩 물은 결과. 뷰를 뺀 재컴파일은 시험하지 않았다


### 연동

- **API 토큰 메뉴 찾기** (7장)  
  증상: 설정(Settings) 메뉴에 API 토큰 항목이 없다.  
  원인: API 토큰은 설정이 아니라 오른쪽 위 사용자 메뉴(동그란 머리글자 단추, 접근성 이름 "User menu") 안에 있다.  
  조치: 오른쪽 위 머리글자 단추 → API Tokens → New Token. 만료(Never·30 days·90 days·1 year)를 고르고 Create token. 토큰은 이때 한 번만 보인다.  
  확인: 확인함 — 2026-11-15 녹화 스크립트가 처음엔 "A" 글자로 단추를 찾다가 검색 단추를 눌렀고, "User menu"로 고쳐 성공

- **API 토큰 복사** (7장)  
  증상: 토큰 목록에는 `auto_ontol…` 앞부분만 보이고 전체 값을 다시 볼 수 없다.  
  원인: Auto Ontology는 토큰의 SHA-256 해시만 저장한다. 값은 만들 때 「Copy your token now」 상자에 한 번만 보인다.  
  조치: 즉시 복사해 비밀 관리 도구나 권한 0600 파일에 둔다. 잃어버리면 새로 만들고 기존 토큰은 휴지통 단추(Revoke)로 지운다.  
  확인: 확인함 — 2026-11-15 화면 확인

- **MCP 서버에 API 토큰으로 붙이기** (6장)  
  증상: MCP 요청이 `HTTP/1.1 401 Unauthorized` 와 `www-authenticate: Bearer … resource_metadata="http://localhost:3103/.well-known/oauth-protected-resource/mcp"` 로 거절된다(x-api-key 머리글이나 API 토큰을 Bearer 로 넣었을 때).  
  원인: MCP 서버는 Auto Ontology가 OAuth로 발급한 토큰만 받는다. 문서(docs/mcp.md): "There is no way to configure a token for the server itself." — 모든 호출이 로그인한 사람의 권한으로 동작하게 하려는 설계다.  
  조치: MCP 클라이언트 설정에는 주소(`http://localhost:3003/mcp`)만 넣고, 클라이언트가 띄우는 로그인·승인(Authorize MCP access)을 사람이 한 번 한다. 사람의 개입 없이 실행되는 스크립트·배치는 MCP 대신 REST API와 API 토큰을 쓴다(7장).  
  확인: 확인함 — 2026-11-15 curl로 x-api-key·Bearer(API 토큰) 둘 다 401 확인, Claude Code OAuth로는 연결됨

- **MCP 서버 주소를 다른 이름으로 부를 때** (6장)  
  증상: 클라이언트가 "Protected resource ... does not match expected ..." 오류를 낸다(공식 문서 docs/mcp.md 의 문제 해결 항목).  
  원인: MCP 서버는 자신이 바인딩된 주소를 보호 자원 주소로 알리는데, 클라이언트가 같은 호스트를 다른 철자(대개 127.0.0.1 대 localhost)로 불렀다.  
  조치: AUTO_ONTOLOGY_MCP_PUBLIC_URL을 클라이언트가 쓰는 주소로 맞추거나 AUTO_ONTOLOGY_MCP_HOST를 비운다. 웹 앱(프런트엔드)에도 같은 값을 준다.  
  확인: **확인 못 함** — 공식 문서의 안내를 옮김. 이번 실행은 처음부터 localhost로 맞춰 겪지 않았다


## 예외 상황

따라 하는 환경이 이 교재와 다를 때 자주 생기는 일입니다. 이번 실행에서 실제로 겪은 항목은 위 단계별 목록에도 있고, 겪지 않은 항목은 일반 안내로만 적었습니다.

### 네트워크·프록시

- 이번에 겪음: **docker compose up** — docker-compose.yml 이 백엔드 "3001:3001"·적재 서비스 "3002:3002" 를 호스트에 그대로 연다. → 공유망·서버에서 돌릴 때는 docker-compose.yml의 두 줄을 "127.0.0.1:3001:3001"·"127.0.0.1:3002:3002"로 바꾸거나 ports를 지우고, 방화벽으로 막는다.

- 함께 볼 것: 회사망에서는 모델 엔드포인트(build.nvidia.com·OpenAI)로 나가는 HTTPS가 막히거나 프록시를 거쳐야 할 수 있습니다. 컨테이너에도 `HTTPS_PROXY`·`NO_PROXY`(localhost·postgres 등 내부 이름 포함)를 넘겨야 합니다.

### API 키 만료·한도·요금

- 일반 안내(이번 실행에서는 겪지 않음): 모델 키가 만료되거나 한도를 넘으면 컴파일·질문이 모델 호출 단계에서 실패합니다. 먼저 키만으로 `curl <엔드포인트>/v1/models -H "Authorization: Bearer $KEY"`가 200인지 봅니다(키 값은 화면·기록에 남기지 않습니다). 이 교재의 한 번 컴파일은 gpt-6.1-sol 호출 318번(입력 약 34만 토큰)이었고, 질문 하나는 10~15번 호출이었습니다.

### 포트 충돌

- 일반 안내(이번 실행에서는 겪지 않음): 3000~3003·5432를 다른 프로그램이 쓰고 있으면 서비스가 뜨지 않습니다. `lsof -nP -iTCP:3000 -sTCP:LISTEN`으로 확인하고, Compose의 포트 매핑이나 `POSTGRES_PORT`를 바꿉니다. 웹 주소를 바꾸면 `APP_URL`·`AUTO_ONTOLOGY_MCP_PUBLIC_URL`도 함께 바꿉니다.

### 메모리·디스크 부족

- 일반 안내(이번 실행에서는 겪지 않음): Compose는 PostgreSQL·pgAdmin·백엔드·적재·웹 앱 컨테이너를 함께 띄웁니다. Docker 가상 머신의 메모리가 모자라면 PostgreSQL이 복구 모드에 들어가거나 빌드가 멈출 수 있습니다. 쓰지 않는 컨테이너를 내리고 Docker 메모리를 늘립니다.

### 칩·OS 차이(Apple Silicon·Intel·Windows)

- 일반 안내(이번 실행에서는 겪지 않음): 이 교재는 Apple Silicon macOS에서만 실행했습니다. Windows는 WSL 2의 Docker Desktop을 권합니다. README의 여러 줄 명령(`\` 줄바꿈, `(cd … && …)`)은 PowerShell에서 그대로 돌지 않습니다.

### 느린 모델·시간 초과

- 이번에 겪음: **추론 강도(reasoning_effort)를 낮출 때** — `Unsupported value: 'reasoning_effort' does not support 'none' with this model. Supported values are: 'low', 'medium', 'high', and 'xhigh'.` → 중계기·게이트웨이에서 `reasoning_effort: "low"`처럼 지원하는 값만 붙인다. 이 교재: `SHIM_REASONING_EFFORT=low bash run/start-course.sh shim`
- 이번에 겪음: **Chat에 질문(추론 모델 gpt-6.1-sol)** — 답이 몇 분 걸린다. 진행 단계에 SQL 다시 짜기(reconstruct_sql)·검사(validate_sql_query)가 여러 번 되풀이된다. 이번 실행: Q1 영어 238.4초(다시 짜기 8번), ROAS 121.6초(5번). → ① 게이트웨이·중계기에서 reasoning_effort=low를 붙이면 간단한 질문은 34~40초로 빨라진다(이번 실행). 다만 답이 달라졌고(Q1 128.0·빈 값), ROAS는 오히려 다시 짜기 14번·204.9초 끝에 "SQL can't be constructed from the data."로 끝났다 — 이 교재는 기본 강도를 썼다. ② MCP·API의 시간 제한은 넉넉히(README 예 timeout=900초, MCP AUTO_ONTOLOGY_MCP_CHAT_TIMEOUT_S 기본 900). ③ 빠른 비추론 모델을 NON_REASONING에 따로 준다(이번에는 재지 않음).

### 한글 입력·인코딩

- 일반 안내(이번 실행에서는 겪지 않음): 한국어 질문도 받습니다(5장 Q1 한국어). 용어·설명은 영어로 생성되므로, 한국어 동의어를 용어에 더하면 찾기 쉬워집니다. 터미널에서 한국어 질문을 넘길 때는 UTF-8 로케일(`LANG=ko_KR.UTF-8`)인지 확인합니다.

### 공식 설치법과 다르게 돌린 경우(NVIDIA 키 없이)

- 이번에 겪음: **모델 설정(.env)을 OpenAI로 바꿀 때** — OpenAI가 `invalid model ID` 로 거절한다(모델 이름에 `openai/` 접두사를 붙였을 때). → OpenAI 호환 게이트웨이(LiteLLM 등)나 작은 중계기에서 `openai/` 접두사를 떼고 넘긴다. 이 교재는 run/openai_shim.py(:3109)를 썼고, .env는 `DEFAULT_MODELS_ENDPOINT=http://127.0.0.1:3109/v1`, `REASONING_MODEL=openai/gpt-6.1-sol`.
- 이번에 겪음: **gpt-5/6 계열 OpenAI 모델을 연결할 때** — `Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.` → 중계기·게이트웨이에서 `max_tokens`를 `max_completion_tokens`로 바꿔 넘긴다(이 교재의 run/openai_shim.py가 하는 일). 같은 모델에 `temperature: 0`을 보내면 `Only the default (1) value is supported.`로도 거절되니 함께 뺀다.
- 이번에 겪음: **재순위(RERANK) 모델** — OpenAI 에 `/v1/rerank` 를 보내면 HTTP 404. → 재순위 모델이 있는 엔드포인트(NVIDIA NIM 등)를 `RERANK_ENDPOINT`·`RERANK_MODEL`에 따로 준다. 이 교재는 중계기가 임베딩 코사인 유사도로 흉내 냈다(RERANK_ENDPOINT=http://127.0.0.1:3109/v1/rerank).
- 이번에 겪음: **임베딩 모델을 OpenAI로 바꿀 때** — 임베딩을 저장하는 단계에서 벡터 차원이 맞지 않는다는 오류로 적재가 실패한다(오류 원문은 이번 실행에서 다시 확인하지 못했다). → 임베딩 요청에 `dimensions: 2048`을 붙여 보낸다(중계기에서). 적재와 질문에 같은 임베딩 모델을 쓴다 — 바꾸면 의미 계층을 초기화(Settings → Semantic Compilation → Reset)하고 다시 컴파일한다.

## 이 교재를 찍은 환경

공식 Quickstart(Docker Compose·NVIDIA NIM)를 따르면 겪지 않는 것들입니다. 이 교재의 화면을 찍은 환경이 공식 설치와 어떻게 다른지 밝히려고 따로 적었습니다.

| 항목 | 이 교재의 실행 |
|---|---|
| 소스 | NVIDIA/auto-ontology 1.2.0 (커밋 c447003), 예제 데이터는 auto-ontology-eval ec41b2c의 `seed_wwi.py` |
| 띄우는 방법 | Docker 없이 서비스마다 직접 실행 — 백엔드는 포트가 3001로 고정되어 있어 `create_app()`을 uvicorn으로 3101에 띄움, 웹 앱은 `next start -p 3100`, MCP는 `uv run auto-ontology-mcp` |
| PostgreSQL | 다른 앱에 들어 있는 PostgreSQL 16 + pgvector 사본에 `pg_trgm`을 소스에서 빌드해 추가, 포트 28930 |
| 모델 | NVIDIA 키 없이 OpenAI `gpt-6.1-sol`(채팅 역할 전부)·`text-embedding-3-large`(임베딩 2048차원) — 작은 중계기(:3109)가 형식을 맞춤, 재순위는 임베딩 유사도로 흉내 |
| 추론 강도 | 기본값(5장의 비교 측정에서만 `low`) |
| 그래프 화면 녹화 | 헤드리스 Chromium에 `--use-angle=swiftshader` |
| MCP 클라이언트 | Claude Code 2.1.325를 사용자 설정과 분리한 설정 폴더(`CLAUDE_CONFIG_DIR`)로 띄우고 사내 Frentis 모델에 연결, 브라우저 열기는 녹화 브라우저가 대신함 |
| PC | Apple Silicon macOS, 2026년 11월 15일 |

- **Docker 없이 적재(ingestion) 서비스를 띄울 때** (1장 · 제품 결함 후보)  
  증상: 적재 서비스가 `Uvicorn running on http://0.0.0.0:3102` — 모든 네트워크 주소에서 들린다.  
  원인: auto_ontology/ingestion_service/__main__.py가 host를 0.0.0.0으로 고정한다. README는 3001·3002를 사설망에 두라고 하는데(인증 없음), Docker Compose에서는 컨테이너 망 안이라 괜찮지만 직접 띄우면 PC의 모든 주소에 열린다.  
  조치: 직접 띄울 때는 방화벽으로 3102(이 교재의 포트, 공식 3002)를 막거나 공용 Wi-Fi에서 띄우지 않는다. 운영은 공식 Docker Compose·Helm을 쓴다.  
  확인: 확인함 — 2026-11-15 ingestion.log의 바인딩 주소와 소스 확인

- **그래프 화면을 헤드리스 브라우저로 찍을 때** (4장)  
  증상: Exploration 그래프가 빈 화면으로 찍힌다(WebGL 없음).  
  원인: 헤드리스 Chromium에 GPU가 없으면 WebGL 그래프가 그려지지 않는다.  
  조치: Chromium을 `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`로 띄운다. 일반 브라우저에서 직접 보면 겪지 않는다.  
  확인: **확인 못 함** — 2026-11-09 실험 기록. 이번 녹화는 처음부터 이 옵션으로 찍었다

- **Docker 없이 PostgreSQL을 직접 띄울 때** (1장)  
  증상: 마이그레이션(`alembic upgrade head`)이 pg_trgm 확장을 만들지 못해 멈춘다(오류 원문은 이번 실행에서 다시 확인하지 못했다).  
  원인: Docker Compose의 PostgreSQL 17 + pgvector 이미지와 달리, 우리가 쓴 앱 번들 PostgreSQL 16 + pgvector 사본에는 pg_trgm(contrib)이 빠져 있었다.  
  조치: PostgreSQL 소스의 contrib/pg_trgm을 빌드해 같은 설치본에 넣는다(`make -C contrib/pg_trgm && make -C contrib/pg_trgm install`). 공식 Quickstart(Docker Compose)를 쓰면 겪지 않는다.  
  확인: **확인 못 함** — 2026-11-09 실험에서 겪고 고침(nvidia-backend/run/start.sh prepare). 이번에는 다시 재현하지 않았다

- **녹화용 터미널에서 따로 둔 Claude Code 띄우기** (6장)  
  증상: 녹화용 tmux 창에서 `claude` 가 녹화용 래퍼가 아니라 평소의 Claude Code(사용자 계정·설정)로 떠서 `claude mcp add` 가 사용자 설정(~/.claude.json)에 MCP 서버를 더했다.  
  원인: `tmux new-session -e PATH=…`로 준 PATH가 새 셸에 적용되지 않았다(tmux가 PATH를 따로 다룸).  
  조치: 세션마다 rc 파일에 `export PATH=…`를 적고 `bash --noprofile --rcfile <rc> -i`로 띄운다. 녹화 스크립트는 시작 전에 `type claude` 결과·설정 폴더 경로·모델 이름을 확인하고 다르면 멈춘다. 잘못 더한 서버는 `claude mcp remove auto-ontology -s local`로 지웠다(대화는 보내지 않아 비용 0).  
  확인: 확인함 — 2026-11-15 rc 방식으로 `claude is …/course/bin/claude` 확인, 잘못 더한 서버 제거 확인

- **tmux send-keys로 명령 입력** (6장)  
  증상: `;` 가 빠진 채 입력되어 셸이 `>` 이어 쓰기 상태로 멈췄다.  
  원인: tmux는 인자 끝의 `;`를 명령 구분자로 처리한다.  
  조치: `;`는 `\;`로 보낸다(term.py의 type()).  
  확인: 확인함 — 2026-11-15 echo a; echo b로 확인

- **컴파일 녹화를 이어 지켜보기** (3장)  
  증상: 같은 장면 폴더에 녹화기 두 개가 같은 번호의 그림을 쓰고, frames.json 을 서로 덮어썼다.  
  원인: nohup으로 띄운 첫 녹화기가 실행 중인 줄 모르고 이어 보기 녹화기를 하나 더 띄웠다.  
  조치: 녹화기는 한 번에 하나만(`pgrep -fl rec_nv.py`로 확인). 끝난 뒤 frames.json에 없는 그림은 쓰지 않는다.  
  확인: 확인함 — 2026-11-15 두 번째 녹화기를 멈추고 첫 녹화기로 끝까지 찍음

- **Claude Code(사내 모델 게이트웨이)로 MCP 도구 부르기** (6장)  
  증상: `API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check your inference gateway (<사내 게이트웨이 주소>).` — 재시도 10번 끝에 실패. MCP 서버 연결·OAuth·도구 목록은 정상이었다.  
  원인: 이 교재의 Claude Code는 사용자 계정과 분리하려고 사내 Frentis 모델 게이트웨이(Anthropic 호환)에 붙였다. 도구를 부르게 하는 요청에서 게이트웨이가 500을 냈다(같은 게이트웨이에 도구 없는 짧은 요청은 200). 원인은 게이트웨이 쪽으로 보이며 추가로 조사하지 않았다.  
  조치: 도구 호출 장면은 공식 MCP Python SDK(mcp 1.29.0)로 만든 작은 클라이언트(lab/mcp_client.py)로 찍었다 — 같은 OAuth 흐름과 같은 도구. 평소처럼 Anthropic 계정에 로그인한 Claude Code로 쓰면 이 게이트웨이를 거치지 않는다(이 교재에서 확인하지 못함).  
  확인: **확인 못 함** — 2026-11-15 같은 요청을 대화형·claude -p로 세 번 시도해 모두 500. 다른 모델로 Claude Code 도구 호출은 시험하지 못함


## 알려진 제약

1.2.0에서 확인한 제약과 제품 결함 후보입니다. 교재에는 우회법만 적었습니다.

- **Docker 없이 적재(ingestion) 서비스를 띄울 때** — 적재 서비스가 `Uvicorn running on http://0.0.0.0:3102` — 모든 네트워크 주소에서 들린다. 우회: 직접 띄울 때는 방화벽으로 3102(이 교재의 포트, 공식 3002)를 막거나 공용 Wi-Fi에서 띄우지 않는다. 운영은 공식 Docker Compose·Helm을 쓴다.
- **docker compose up** — docker-compose.yml 이 백엔드 "3001:3001"·적재 서비스 "3002:3002" 를 호스트에 그대로 연다. 우회: 공유망·서버에서 돌릴 때는 docker-compose.yml의 두 줄을 "127.0.0.1:3001:3001"·"127.0.0.1:3002:3002"로 바꾸거나 ports를 지우고, 방화벽으로 막는다.
- **용어·SQL 속성 인증** — 용어·SQL 속성을 인증(Certified)해도 질문 답이 인증된 정의를 우선해 쓰는지 화면에서 알 수 없다. 우회: 답을 고정하려면 인증 표시만으로는 부족하다 — 지표는 SQL 속성으로 정의하고 설명에 사용 조건을 적는다(5장 끝). 인증은 검토가 끝났다는 기록으로 쓴다.
- **조인 하나를 끄는 기능 없음** — 화면과 공개 API에서 추론된 조인 하나를 끄거나 지우는 방법을 찾지 못했습니다(3장). 표를 통째로 빼려면 연결의 Table Denylist와 Reset Semantic Layer를 씁니다.
- **추론 강도 설정 없음** — 모델 호출에 `reasoning_effort` 같은 값을 넘기는 설정이 없어 게이트웨이에서 붙여야 합니다(5장).
- **MCP는 OAuth만** — MCP 서버는 API 토큰을 받지 않고 사람이 로그인해 승인한 OAuth 토큰만 받습니다. 사람 없이 도는 작업은 REST API와 API 토큰을 씁니다(6·7장).
