# 설치와 실행

> Auto Ontology를 이루는 서비스 다섯 가지와 포트를 살펴보고, NVIDIA README의 공식 Quickstart(Docker Compose) 순서를 따라갑니다. 이 교재의 화면은 Docker 없이 같은 서비스를 직접 띄우고 OpenAI 모델을 연결해 찍었으므로, 공식 방법과 무엇이 다른지도 함께 밝힙니다.

## 무엇을 · 왜

Auto Ontology는 프로그램 하나가 아니라 여러 서비스가 함께 동작하는 구조입니다. README의 구성표를 옮기면 이렇습니다.

| 구성 요소 | 기술 | 하는 일 | 공식 포트 | 이 교재 |
|---|---|---|---|---|
| 웹 앱(Frontend) | Next.js, Better Auth, Prisma | 웹 화면, 로그인, 공개 API 관문 | 3000 | 3100 |
| 백엔드(Backend) | FastAPI, LangChain | 질문 → SQL 에이전트, 카탈로그·온톨로지 API | 3001 | 3101 |
| 적재 서비스(Ingestion) | FastAPI | 원천 적재와 의미 계층 컴파일 | 3002 | 3102 |
| MCP 서버 | FastMCP | 에이전트용 읽기 전용 도구 | 3003 | 3103 |
| PostgreSQL + pgvector | PostgreSQL | 카탈로그·온톨로지·앱 데이터·벡터 | 5432 | 28930 |

외부에서 접속하는 창구는 웹 앱(3000) 하나입니다. README는 백엔드(3001)와 적재 서비스(3002)를 사설망에 두라고 적고 있습니다. 백엔드는 웹 앱이 넘겨주는 사용자 헤더(`x-auto-ontology-user-id`)을 그대로 신뢰하고, 적재 서비스의 적재·삭제·초기화·컴파일 엔드포인트에는 인증이 없기 때문입니다.

모델의 역할은 네 가지로 나뉘며, 역할마다 `<접두사>_ENDPOINT`·`<접두사>_API_KEY`·`<접두사>_MODEL` 세 값으로 설정합니다. 비워 둔 값은 `DEFAULT_MODELS_*`를 따릅니다.

| 역할(접두사) | 기본 모델 | 하는 일 |
|---|---|---|
| `REASONING` | `nvidia/nemotron-3.5-lightning-30b-a3b` | 온톨로지(용어·관계·SQL 속성)를 만들고, 답의 SQL과 설명을 쓰고, 답변 가능성을 평가합니다 |
| `NON_REASONING` | `nvidia/nemotron-3.5-lightning-30b-a3b` | 질문 의도·개체 추출, 후보 고르기, SQL 검사·수정처럼 빠른 단계 |
| `EMBED` | `nvidia/nemotron-3.5-embed-1b` | 표·열·용어·SQL 속성을 pgvector에 색인하고 질문과 맞춰 봅니다 |
| `RERANK` | `nvidia/nemotron-3.5-rerank-8b` | 컴파일 중 다리(bridge) 테이블 SQL 속성 후보의 순위를 매깁니다 |

README는 NIM 대신 OpenAI 호환 엔드포인트도 쓸 수 있다고 하면서, 구조화 출력을 지원하는 모델을 쓰고 적재와 질문에 같은 임베딩 모델을 쓰라고 당부합니다.

## 따라 하기: 공식 Quickstart

공식 방법은 Docker Compose입니다. Docker(Compose v2), [uv](https://docs.astral.sh/uv/), NVIDIA API 키(`nvapi-…`)가 필요합니다. 아래 명령은 README를 그대로 옮긴 것입니다.

<ol class="steps" markdown="1">
<li markdown="1">**저장소를 받고 `.env`를 만듭니다.**

```bash
git clone https://github.com/NVIDIA/auto-ontology.git && cd auto-ontology
cp .env.example .env
```

`.env`에서 다음 값을 채웁니다. Compose는 PostgreSQL·pgAdmin·웹 앱을 호스트에 열어 두므로 기본 비밀번호는 모두 바꿉니다. `.env.example`의 역할별 `nvapi-your-api-key-here`는 지우면 `DEFAULT_MODELS_API_KEY`를 따릅니다.

```dotenv
DEFAULT_MODELS_API_KEY=nvapi-...
AUTH_SECRET=<a long random string, e.g. from openssl rand -base64 32>
APP_URL=http://localhost:3000
POSTGRES_PASSWORD=<a new password>
CONNECTION_STRINGS=postgresql://postgres:<the same password>@postgres:5432/wideworldimporters
AUTO_ONTOLOGY_ADMIN_PASSWORD=<a new password>
PGADMIN_PASSWORD=<a new password>
```
</li>
<li markdown="1">**PostgreSQL을 띄우고 예제 데이터를 넣습니다.** 데이터를 넣는 스크립트는 `auto-ontology-eval` 저장소에 있습니다.

```bash
docker compose up -d --wait postgres
git clone https://github.com/NVIDIA/auto-ontology-eval.git ../auto-ontology-eval
(cd ../auto-ontology-eval && uv sync && cp .env.example .env && \
  POSTGRES_PASSWORD='<the same password>' \
  uv run python scripts/seed/seed_wwi.py --database-name wideworldimporters --drop)
```
</li>
<li markdown="1">**나머지 서비스를 빌드해 띄웁니다.**

```bash
docker compose up -d --build
```
</li>
<li markdown="1">**로그인합니다.** <http://localhost:3000>을 열고 `.env`의 `AUTO_ONTOLOGY_ADMIN_EMAIL`·`AUTO_ONTOLOGY_ADMIN_PASSWORD`로 로그인합니다. 가입 화면은 없고, 첫 계정은 이 관리자 계정입니다.

![로그인 화면 — 이메일과 비밀번호(가려짐)를 넣은 상태](img/nv-login.webp)

로그인하면 Chat 화면이 열립니다. 아직 연결한 데이터가 없어서 대화 목록이 비어 있습니다. 왼쪽 세로 메뉴는 위에서부터 Chat · Discovery(검색) · Terms(용어) · Analysis · Exploration(그래프) · Data(카탈로그) · Analytics · Settings입니다.

![로그인 직후의 Chat 화면](img/nv-home.webp)
</li>
</ol>

공식 Quickstart는 이어서 Settings → Semantic Compilation을 켜고 Chat에 질문합니다. 이 교재는 그 사이에 **연결을 화면에서 직접 만드는 과정**을 넣었습니다([2장](connect.html)). 공식 방법처럼 `.env`의 `CONNECTION_STRINGS`로 연결하면 2장의 화면 대신 시작할 때 자동으로 적재되고, [3장](compile.html)으로 바로 가면 됩니다.

## 이 교재의 화면은 어떻게 띄웠나

이 교재를 만든 PC는 다른 작업의 Docker 컨테이너가 이미 메모리를 많이 쓰고 있었고, NVIDIA API 키도 없었습니다. 그래서 공식 Quickstart와 같은 소스(1.2.0, 커밋 c447003)를 쓰되 다음처럼 바꿔 띄웠습니다. 화면과 동작은 같지만 **권장하는 설치 방법은 아닙니다.** 따라 할 때는 공식 Docker Compose를 쓰세요.

| 항목 | 공식 Quickstart | 이 교재의 실행 |
|---|---|---|
| 띄우는 방법 | `docker compose up` | 각 서비스를 직접 실행(Python 3.12 가상환경, `next start`, `uv run auto-ontology-mcp`) |
| 포트 | 3000 · 3001 · 3002 · 3003 · 5432 | 3100 · 3101 · 3102 · 3103 · 28930 |
| PostgreSQL | PostgreSQL 17 + pgvector 이미지 | PostgreSQL 16 + pgvector에 `pg_trgm` 확장을 직접 빌드해 넣음 |
| 모델 | NVIDIA Nemotron(NIM) | OpenAI `gpt-6.1-sol`(채팅 역할 전부), `text-embedding-3-large`(임베딩) — 작은 중계기(:3109)를 거침 |
| 연결 | `.env`의 `CONNECTION_STRINGS` | 비워 두고 화면(Settings → Connections)에서 연결 |
| 예제 데이터 | `seed_wwi.py` | 같은 스크립트(`auto-ontology-eval` ec41b2c)로 넣은 데이터 |

이 교재의 실행에서 `.env`의 모델 부분은 다음과 같습니다(키는 지웠습니다). `openai/` 접두사는 Auto Ontology가 OpenAI 클라이언트를 고르게 하는 표시입니다.

```dotenv
DEFAULT_MODELS_ENDPOINT=http://127.0.0.1:3109/v1
DEFAULT_MODELS_MODEL=openai/gpt-6.1-sol
REASONING_MODEL=openai/gpt-6.1-sol
NON_REASONING_MODEL=openai/gpt-6.1-sol
EMBED_MODEL=text-embedding-3-large
RERANK_ENDPOINT=http://127.0.0.1:3109/v1/rerank
CONNECTION_STRINGS=
```

중계기가 하는 일은 네 가지입니다. OpenAI가 인식하지 못하는 `openai/` 접두사를 떼고, `gpt-6.1-sol`이 받지 않는 `max_tokens`를 `max_completion_tokens`로 바꾸고, 임베딩을 저장소 차원(2048)에 맞춰 요청하고, OpenAI에 없는 재순위(rerank)를 임베딩 유사도로 흉내 냅니다. 5장에서 쓰는 추론 강도(`reasoning_effort`)도 중계기에서 붙였습니다. Auto Ontology 1.2.0에는 이 값을 지정하는 설정이 없습니다.

![이 교재의 실행 — 서비스를 내렸다 다시 띄우고 포트를 확인한 터미널](img/nv-start.webp)

포트를 확인해 보면 웹 앱(3100)과 적재 서비스(3102)는 모든 주소(`*`)에서, 백엔드(3101)와 MCP(3103)는 `127.0.0.1`에서만 열렸습니다. 적재 서비스는 소스에서 `0.0.0.0`으로 고정되어 있어, Docker 없이 띄울 때는 방화벽으로 막아야 합니다. Docker Compose도 3001·3002를 호스트에 그대로 열어 두므로, 공유망에서는 [부록](troubleshooting.html)의 조치를 보세요.

## 막히면

!!! warning "막히면"
    - **`invalid model ID`** — 모델 이름의 `openai/` 접두사가 OpenAI까지 그대로 갔습니다. → Auto Ontology는 이 접두사로 OpenAI 경로를 고르므로 이름에서 빼면 안 됩니다. → 게이트웨이나 중계기에서 접두사를 떼고 넘깁니다.
    - **`Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.`** — gpt-5·6 계열 OpenAI 모델을 연결했습니다. → 최신 추론 모델은 `max_completion_tokens`만 받습니다. → 게이트웨이나 중계기에서 이름을 바꿔 넘깁니다.
    - **재순위 호출이 404** — OpenAI에는 rerank API가 없습니다. → `RERANK_ENDPOINT`·`RERANK_MODEL`을 재순위 모델이 있는 곳(NVIDIA NIM 등)으로 따로 줍니다.
    - **다시 띄운 뒤 화면 왼쪽 메뉴가 안 보임** — 브라우저에 이전 로그인 쿠키가 남았습니다(README 안내). → `localhost:3000`의 사이트 데이터를 지우고 다시 로그인합니다.

    전체 목록은 [부록 「문제 해결」](troubleshooting.html)에 있습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>1. 외부 사용자와 스크립트가 접근하는 창구는 어느 서비스이고, 왜 3001·3002는 사설망에 두어야 하나요?</summary>

웹 앱(3000)입니다. 로그인·토큰 확인과 권한 검사가 여기에서 일어납니다. 백엔드(3001)는 웹 앱이 넘긴 사용자 헤더을 검증 없이 신뢰하고, 적재 서비스(3002)의 엔드포인트에는 인증이 없어서, 외부에 공개하면 누구나 다른 사람 행세를 하거나 의미 계층을 지울 수 있습니다.
</details>

<details class="answer" markdown="1">
<summary>2. NVIDIA 키 없이 OpenAI 모델을 쓰려면 무엇을 바꾸나요?</summary>

역할별 `*_ENDPOINT`·`*_API_KEY`·`*_MODEL`을 OpenAI 호환 엔드포인트로 바꿉니다. 모델 이름에 `openai/` 접두사를 붙이고, 그 접두사를 떼어 주는 게이트웨이를 앞에 둡니다. 임베딩은 2048차원으로 받고, 재순위는 따로 마련합니다.
</details>

다음 장에서는 Wide World Importers를 화면에서 연결해 적재합니다.
