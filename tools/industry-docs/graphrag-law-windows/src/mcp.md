# Neo4j MCP 서버 연결

> Claude Code가 Neo4j를 직접 조회하도록 공식 Neo4j MCP 서버 2.1.2를 연결합니다. 비밀번호는 파일 밖에서 환경변수로 전달하고 서버를 읽기 전용으로 실행해, 도구 두 개(get-schema, read-cypher)만으로 그래프에 질의하도록 합니다.

## 무엇을 · 왜

MCP(Model Context Protocol)는 AI 에이전트가 외부 도구와 데이터를 사용하는 표준 인터페이스입니다. MCP 서버가 「이런 도구가 있다」고 알려 주면 Claude Code는 질문에 따라 필요한 도구를 호출하고, 반환된 결과를 읽고 답합니다. [6](ingest.html)·[7장](disambiguation.html)에서는 Claude가 파이썬 스크립트와 cypher-shell을 직접 작성해 Neo4j에 접근했습니다. MCP 서버를 연결하면 Claude가 스키마를 읽고(`get-schema`) Cypher를 작성하고 실행하는(`read-cypher`) 도구를 바로 사용합니다. [2장](how-graphrag.html)에서 본 질의 과정(엔티티 연결 → 스키마를 컨텍스트에 → Cypher 생성 → 실행 → 답)이 이 두 도구로 이루어집니다. 읽기 전용으로 실행하면 질의 중에 그래프가 변경되지 않습니다.

| 항목 | 이 실습 |
|---|---|
| 서버 | 공식 [neo4j/mcp](https://github.com/neo4j/mcp)(Go 바이너리 `neo4j-mcp`), 최신 릴리스 v2.1.2(2026-11-23) |
| 설치·실행 | PyPI 패키지 `neo4j-mcp-server` 2.1.2(바이너리를 담은 휠)를 `uvx neo4j-mcp-server@2.1.2`로 실행합니다. 처음 실행할 때 9.9MiB를 내려받습니다. Windows용 휠(`win_amd64`·`win_arm64`)이 있어 Windows에서도 같은 명령으로 실행됩니다. 릴리스 페이지의 Windows 바이너리로도 설치할 수 있습니다 |
| 연결 방식 | STDIO — Claude Code가 서버를 자식 프로세스로 실행해 표준입출력으로 데이터를 주고받습니다 |
| 문서 | [neo4j.com/docs/mcp/current](https://neo4j.com/docs/mcp/current/)(installation, stdio-configuration) |

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="block">**Claude Code에 `.mcp.json`을 만들게 합니다.** 7장까지 사용하던 세션에서 입력합니다.

**왜 하나요?** MCP 서버를 연결해야 Claude가 파이썬 스크립트 없이 그래프를 직접 조회할 수 있습니다. 공식 문서를 확인하게 하면 버전마다 바뀌는 설정 이름(예: `NEO4J_MCP_` 접두사)을 틀리지 않습니다.

```text
이제 Claude Code 가 Neo4j 를 직접 조회하도록 Neo4j MCP 서버를 붙이자. 공식 서버(github.com/neo4j/mcp)의 문서를 확인해서 이 프로젝트의 .mcp.json 을 만들어 줘.
- uvx 로 실행하고, 읽기 전용(쓰기 도구는 끔), 텔레메트리는 끔.
- 비밀번호는 파일에 쓰지 말고 환경변수 NEO4J_PASSWORD 를 넘겨 받게 해(.mcp.json 은 .gitignore 에 들어 있어).
- 서버 버전과 제공하는 도구 이름도 확인해 줘.
```

Claude는 저장소의 README·`.env.example`·설정 코드(`internal/config/config.go`)를 읽어 변수 이름을 확인하고, `uvx neo4j-mcp-server@2.1.2 --version`으로 `neo4j-mcp version: 2.1.2`를 확인한 뒤 `.mcp.json`을 작성했습니다. 이어서 **그 파일의 명령과 환경변수로 서버를 실행하고 MCP 요청을 직접 보내** 시험했습니다(1분 9초).

```text
serverInfo {'name': 'neo4j-mcp', 'version': '2.1.2'} | protocol 2025-06-18
tool get-schema | {… 'readOnlyHint': True, 'title': 'Get Neo4j Schema'} | []
tool read-cypher | {… 'readOnlyHint': True, 'title': 'Read Cypher'} | ['query', 'params']
read-cypher → {"content": [{"type": "text", "text": "[\n  {\n    \"norms\": 410\n  }\n]"}]}
read-cypher 로 쓰기 시도 → … "read-cypher can only run read-only Cypher statements. For write operations (CREATE, MERGE, DELETE, SET, etc...), schema/admin commands, or PROFILE queries, use write-cypher instead." …
write-cypher 호출 → {"code": -32602, "message": "unknown tool \"write-cypher\""}
```
</li>
<li markdown="block">**생성된 `.mcp.json`을 읽습니다.** 비밀번호 값은 파일에 없습니다.

**왜 하나요?** AI가 만든 설정이라도 비밀번호가 파일에 적히지 않았는지, 읽기 전용으로 되어 있는지 사람이 확인해야 합니다. 읽기 전용이어야 질의 중에 AI가 그래프를 바꾸지 못합니다.

```json
{
  "mcpServers": {
    "neo4j": {
      "type": "stdio",
      "command": "uvx",
      "args": ["neo4j-mcp-server@2.1.2"],
      "env": {
        "NEO4J_MCP_URI": "bolt://localhost:7687",
        "NEO4J_MCP_USERNAME": "neo4j",
        "NEO4J_MCP_PASSWORD": "${NEO4J_PASSWORD}",
        "NEO4J_MCP_DATABASE": "neo4j",
        "NEO4J_MCP_READ_ONLY": "true",
        "NEO4J_MCP_TELEMETRY": "false"
      }
    }
  }
}
```

| 환경변수 | 값 | 이유 |
|---|---|---|
| `NEO4J_MCP_URI` | `bolt://localhost:7687` | [3장](neo4j-windows.html)에서 `neo4j.bat console`로 띄운 Neo4j |
| `NEO4J_MCP_USERNAME` | `neo4j` | |
| `NEO4J_MCP_PASSWORD` | `${NEO4J_PASSWORD}` | Claude Code가 서버를 실행할 때 자신의 환경변수 값으로 치환합니다. 파일에는 비밀번호가 남지 않습니다 |
| `NEO4J_MCP_DATABASE` | `neo4j` | v2.0.0부터 STDIO에서 기본값이 없어져 반드시 지정해야 합니다(`--help`에는 아직 「default: neo4j」로 나옵니다) |
| `NEO4J_MCP_READ_ONLY` | `true` | 쓰기 도구 `write-cypher`를 목록에서 제외합니다. AI가 질의 중에 그래프를 삭제하거나 변경하지 못하게 합니다(기본값 false) |
| `NEO4J_MCP_TELEMETRY` | `false` | 사용 통계 전송을 끕니다(기본값 true) |

변수 이름의 접두사는 `NEO4J_MCP_`입니다. v2.0.0(2026-10-28)에서 접두사가 없는 이전 변수(`NEO4J_URI` 등)가 제거되었으므로, 이전 문서를 보고 `NEO4J_URI`로 지정하면 인식되지 않습니다. 그 밖에 `NEO4J_MCP_SCHEMA_SAMPLE_SIZE`(스키마를 만들 때 레이블마다 확인하는 노드 수, 기본 100), `NEO4J_MCP_LOG_LEVEL`, `NEO4J_MCP_TOOLS`, `NEO4J_MCP_REQUEST_TIMEOUT`(기본 3m) 같은 선택적 설정 변수가 있습니다. `@2.1.2`처럼 버전을 고정해 두면 교재와 같은 서버로 따라 할 수 있습니다.
</li>
<li markdown="block">**git의 추적 대상에서 제외되었는지 확인합니다.** `/exit`로 Claude Code를 종료하고 셸에서 확인합니다. 3장에서 만든 `.gitignore`에 두 파일이 들어 있습니다.

**왜 하나요?** `.env`와 `.mcp.json`은 개인 환경 설정이라 저장소에 올라가면 안 됩니다. 커밋하기 전에 git이 이 파일들을 무시하는지 명령으로 확인합니다.

```powershell
Set-Location C:\lab\law-graph
git check-ignore -v .mcp.json .env
```

```text
.gitignore:2:.mcp.json	.mcp.json
.gitignore:1:.env	.env
```

`.mcp.json`에 비밀번호가 없더라도 개인 환경 설정이므로 저장소에 올리지 않습니다.
</li>
<li markdown="block">**`env.ps1`로 비밀번호를 불러온 창에서 Claude Code를 다시 실행합니다.** Claude Code는 `.env`를 자동으로 읽지 않습니다. `${NEO4J_PASSWORD}`가 치환되려면 `claude`를 실행하는 창에 해당 환경변수가 있어야 합니다. 3장에서 만든 `env.ps1`이 원 교재의 `set -a; . ./.env; set +a` 역할을 합니다.

**왜 하나요?** Claude Code는 `.mcp.json`의 `${NEO4J_PASSWORD}`를 실행한 창의 환경변수로 채웁니다. 변수가 없는 창에서 `claude`를 열면 MCP 서버가 비밀번호 없이 접속하다 실패합니다. 늘 같은 두 줄로 시작하면 「어제는 됐는데 오늘은 안 된다」를 막을 수 있습니다.

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
$env:NEO4J_PASSWORD.Length      # 0 이 아니면 읽힌 것입니다(값은 보이지 않음)
claude
```

`. .\env.ps1`에서 「이 시스템에서 스크립트를 실행할 수 없으므로…」(`running scripts is disabled on this system`) 오류가 나면 3장 2단계의 실행 정책 설정을 하지 않은 것입니다.

MCP 서버가 뜨는지 Claude Code를 열기 전에 확인할 수도 있습니다. 같은 창에서 실행합니다.

```powershell
claude mcp list
```

`neo4j: uvx neo4j-mcp-server@2.1.2 - ✓ Connected`처럼 나오면 됩니다. 이 프로젝트의 MCP 서버를 아직 승인하지 않았다면 다음 단계의 승인 창을 먼저 거쳐야 할 수 있습니다.
</li>
<li markdown="block">**승인 창에서 `Use this MCP server`를 고릅니다.** 프로젝트에서 새 MCP 서버를 찾으면 이 창이 뜹니다. **기본 선택이 맨 아래 `Continue without using this MCP server`**이므로, 그냥 Enter를 누르면 서버 없이 시작됩니다. ↑를 두 번 눌러 고른 뒤 Enter를 누릅니다.

**왜 하나요?** 프로젝트에 들어 있는 MCP 서버는 코드를 실행할 수 있어서 Claude Code가 한 번 확인을 받습니다. 기본 선택이 「사용 안 함」이라 그냥 Enter를 누르면 연결되지 않으므로 직접 골라야 합니다.

```text
  New MCP server found in this project: neo4j

  MCP servers may execute code or access system resources. All tool calls require approval. Learn more in the MCP
  documentation.

    Use this MCP server
    Use this and all future MCP servers in this project
  ❯ Continue without using this MCP server

  Enter to confirm · Esc to cancel
```
</li>
<li markdown="block">**`/mcp`로 연결을 확인합니다.** 목록에서 `neo4j`를 골라 Enter를 누르면 상태가 나옵니다(다른 MCP 서버를 쓰고 있다면 목록에 함께 나옵니다).

**왜 하나요?** 질문하기 전에 서버가 실제로 연결되었는지 확인하면, 답이 이상할 때 원인이 연결 문제인지 질의 문제인지 구분할 수 있습니다.

```text
  MCP servers
    Project MCPs (…/law-graph/.mcp.json)
  ❯ ✔ neo4j   2 tools
```

```text
  neo4j
  MCP server

  Status:           ✔ connected
  Command:          uvx neo4j-mcp-server@2.1.2
  Protocol:         2026-07-28
  Config location:  …/law-graph/.mcp.json
  Capabilities:     2 tools
```
</li>
<li markdown="block">**도구 두 개를 확인합니다.** `View tools`를 고르면 도구 목록이, 도구를 고르면 설명과 파라미터가 나옵니다.

**왜 하나요?** Claude가 쓸 수 있는 도구가 읽기 전용 두 개뿐인지 확인합니다. 쓰기 도구(`write-cypher`)가 보이면 읽기 전용 설정이 빠진 것입니다.

```text
  Tools for neo4j
  2 tools

  ❯ Get Neo4j Schema   read-only · open-world
    Read Cypher        read-only · open-world
```

| 도구 | 이름(Claude가 호출할 때 쓰는 이름) | 하는 일 |
|---|---|---|
| Get Neo4j Schema | `get-schema` (`mcp__neo4j__get-schema`) | 노드 레이블·관계 타입·속성 키를 반환합니다. 파라미터는 없습니다. 레이블마다 표본을 추출해 만듭니다(APOC의 meta 스키마 사용) |
| Read Cypher | `read-cypher` (`mcp__neo4j__read-cypher`) | 읽기 전용 Cypher를 실행합니다. `query`(필수, string)와 `params`(object) |

README에는 도구가 네 개 있지만 이 구성에서는 두 개만 보입니다. `write-cypher`는 `NEO4J_MCP_READ_ONLY=true`라서 목록에서 빠졌습니다(서버 로그 `Ignoring tool 'write-cypher': not available in read-only mode`). 원 교재의 Community 5.26에서는 `list-gds-procedures`도 보이지 않았지만, Windows PC의 Neo4j Desktop(Enterprise 2026.10)에 연결했을 때는 `get-schema`·`read-cypher`·`list-gds-procedures` **세 개**가 등록되었습니다. 세 번째 도구는 GDS(Graph Data Science) 프로시저 목록을 보여 주는 읽기 전용 도구라 이 실습에는 영향이 없습니다.
</li>
<li markdown="block">**첫 질문으로 연결을 확인합니다.** 골든 퀘스천 1번을 넣으면 Claude가 도구를 처음 호출할 때 권한을 요청합니다. 처음에는 `get-schema`, 다음에는 `read-cypher`의 권한을 요청합니다.

**왜 하나요?** 실제 질문 하나로 스키마 조회 → Cypher 실행 → 답까지 전체 흐름이 도는지 확인합니다. 도구 사용 권한도 이때 한 번 정해 두면 9장에서 질문마다 묻지 않습니다.

```text
 Tool use
 neo4j — Read Cypher Tool: (MCP)
 query:
   │ MATCH (n:Norm)-[:BASED_ON]->(p) WHERE n.object CONTAINS '품명' OR …

 Do you want to proceed?
 ❯ 1. Yes
   2. Yes, and don't ask again for neo4j — Read Cypher commands in …/law-graph
   3. No
```

서버가 읽기 전용이므로 `read-cypher`는 2번(이 프로젝트에서 다시 묻지 않기)을 골랐습니다. 화면에 `Called neo4j 5 times`가 나오고 근거 조문이 포함된 답이 나오면 연결된 것입니다. 질문과 답은 [9장](questions.html)에서 하나씩 살펴봅니다.
</li>
</ol>

## 확인

- `/mcp`에서 `✔ neo4j  2 tools`, 상세 화면에 `Status: ✔ connected`가 보입니다.
- 도구 목록에 `get-schema`·`read-cypher` 두 개만 있고 `write-cypher`가 없습니다.
- 첫 질문에서 `neo4j — Get Neo4j Schema`·`neo4j — Read Cypher` 권한 요청이 나오고 답변이 반환됩니다.

!!! note "교재 pptx(Ch.4 Step 4)와 다른 점"
    `uvx neo4j-mcp-server`, 접두사 `NEO4J_MCP_`, `READ_ONLY`·`TELEMETRY`, 공식 서버 v2.1.2는 pptx와 같으며 현재도 유효합니다. 다른 점은 다섯 가지입니다.

    | | 교재 pptx | 이 교재 |
    |---|---|---|
    | Neo4j | Neo4j Desktop | Windows ZIP `neo4j-community-5.26.33` + `labs`의 APOC(원 교재는 Docker) |
    | 비밀번호 | `.mcp.json`에 직접 작성합니다 | `${NEO4J_PASSWORD}`로 파일 밖에서 전달합니다. 대신 `claude`를 실행하는 셸에 변수가 있어야 합니다 |
    | 서버 버전 | `neo4j-mcp-server`(고정 안 함) | `neo4j-mcp-server@2.1.2`로 고정, `"type": "stdio"` 명시 |
    | 도구 | 표에 4개(`write-cypher`, `list-gds-procedures` 포함) | 실제로 보이는 것은 2개(Enterprise에서는 3개) |
    | 연결 순서 | 「프로젝트 MCP 서버 사용 승인」 | 승인 창의 기본 선택이 「Continue without…」이라 ↑로 선택해야 합니다 |

!!! warning "막히면"
    **Enter를 눌렀더니 `/mcp`에 연결이 없습니다 (GL-11).** 증상: `.mcp.json`을 만들고 `claude`를 다시 실행했는데 「New MCP server found in this project: neo4j」 창의 기본 선택이 `❯ Continue without using this MCP server`라서 서버 없이 시작됩니다. 원인: Claude Code의 프로젝트 MCP 승인 창 기본값입니다. 조치: ↑ 두 번으로 `Use this MCP server`(또는 `Use this and all future MCP servers in this project`)를 고르고 Enter를 누르세요. 이미 넘어갔다면 `/mcp`에서 neo4j를 골라 켜거나, `claude mcp reset-project-choices` 뒤 다시 시작합니다.

    **서버가 실행되지 않습니다 — 인증 실패 (GL-12).** 증상: `"NEO4J_MCP_PASSWORD": "${NEO4J_PASSWORD}"`로 썼는데 `claude`를 실행한 창에 `NEO4J_PASSWORD`가 없으면 MCP 서버가 인증 실패로 실행되지 않습니다. Windows PC에서 확인해 보니 서버는 시작할 때(initialize) DB 접속을 먼저 검사해 `impossible to verify connectivity … Unauthorized`로 멈추고, 그 뒤의 도구 목록 요청도 실패합니다. 원인: Claude Code는 `.mcp.json`의 `${변수}`를 claude 프로세스의 환경변수 값으로 치환하고, `.env`는 자동으로 읽지 않습니다. 조치: 새 PowerShell 창마다 `Set-Location C:\lab\law-graph; . .\env.ps1; claude`를 실행하세요. 반대로 비밀번호를 `.mcp.json`에 직접 쓰면 그 파일이 비밀 파일이 되므로 `.gitignore`에서 빠지지 않게 주의하세요.

## 확인 문제

**1.** `.mcp.json`에 비밀번호 대신 `${NEO4J_PASSWORD}`를 썼습니다. 이 값은 언제, 어디서 치환되나요?

<details class="answer" markdown="1">
<summary>정답</summary>

Claude Code가 MCP 서버를 실행할 때, `claude` 프로세스의 환경변수 값으로 치환합니다. 그래서 `claude`를 실행하는 셸에 `NEO4J_PASSWORD`가 있어야 하고(`. .\env.ps1`), 없으면 서버가 인증 실패로 실행되지 않습니다. 파일에는 비밀번호가 남지 않습니다.
</details>

**2.** 공식 README에는 도구가 네 개인데 `/mcp`에는 두 개만 보입니다. 왜 그런가요?

<details class="answer" markdown="1">
<summary>정답</summary>

`NEO4J_MCP_READ_ONLY=true`로 실행해 쓰기 도구 `write-cypher`가 목록에서 빠졌고, `list-gds-procedures`는 이 Neo4j에 GDS 플러그인이 없어서 빠진 것으로 보입니다. 질문에 답하는 데는 스키마를 읽는 `get-schema`와 읽기 전용 Cypher를 실행하는 `read-cypher`로 충분합니다.
</details>

**3.** 서버 승인 창에서 아무것도 고르지 않고 Enter를 눌렀습니다. 어떻게 되고, 어떻게 바로잡나요?

<details class="answer" markdown="1">
<summary>정답</summary>

기본 선택이 `Continue without using this MCP server`라서 서버 없이 시작됩니다. `/mcp`에서 neo4j를 골라 켜거나, `claude mcp reset-project-choices`를 실행한 뒤 다시 실행해 `Use this MCP server`를 고릅니다.
</details>
