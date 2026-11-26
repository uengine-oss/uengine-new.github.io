# 시작하기

> Windows PC에서 따라 하는 「법령 GraphRAG 실습」입니다. 위험물안전관리법(법률·시행령·시행규칙 PDF 3개)을 그래프로 만들고, Neo4j는 내려받아 직접 설치하며, 모든 명령은 Windows에 기본으로 들어 있는 PowerShell로 입력합니다. 명령은 실제 Windows PC에서 실행해 확인했습니다. 준비(3장)부터 질의(9장)까지 다룹니다.

## 무엇을 만드나요

국가법령정보센터의 위험물안전관리법 PDF를 조·항·호 단위의 Neo4j 그래프로 적재하고, Claude Code가 Neo4j MCP 서버로 그래프를 조회해 골든 퀘스천 다섯 개에 근거 조문과 함께 답하게 합니다.

| 항목 | 이 교재에서 쓰는 것 |
|---|---|
| 법령 | **위험물안전관리법** 법률·시행령·시행규칙 = PDF 3개 |
| Neo4j | **Neo4j 5.26 Community**를 Windows용 ZIP으로 내려받아 설치(JDK 21 필요) |
| 셸 | **Windows PowerShell 5.1**(기본 포함)과 PowerShell 7 모두에서 동작하는 명령 |

골든 퀘스천 다섯 개는 모두 위험물안전관리법 법률·시행령·시행규칙 안에서 답이 나옵니다. 법령이 하나라 파싱·적재·질의가 빨리 끝납니다.

그래프가 왜 필요한지(1장)와 GraphRAG가 질문에 답하는 과정(2장)은 운영체제와 상관없는 이론입니다. 실습 전에 아래 두 페이지를 먼저 읽어 두면 좋습니다.

- [1. 왜 그래프인가](https://www.uengine.org/docs/graphrag-law/why-graph.html)
- [2. GraphRAG 동작 과정](https://www.uengine.org/docs/graphrag-law/how-graphrag.html)

![위험물안전관리법 제15조(위험물안전관리자)의 항(파란색)과, 그 항에 대응하는 하위법령 조문(IMPLEMENTS)·벌칙과 과태료의 호(PENALIZES) — 적재한 그래프를 Neo4j Browser로 본 모습(노드 26 · 관계 26)](img/article15-graph.webp)

## 골든 퀘스천

구축 의도는 「위험물 안전관리 매뉴얼 내부 구축」입니다. 스키마 설계(5장)의 출발점이자 9장에서 답을 채점하는 시험지입니다.

1. 제조소등에서 위치·구조·설비 변경 없이 저장·취급하는 위험물의 품명·수량(지정수량 배수)을 바꾸려면 언제까지 누구에게 신고해야 하는가?
2. 위험물안전관리자가 해임되거나 퇴직하면 관계인은 며칠 안에 다시 선임해야 하고, 선임한 뒤에는 어떤 절차를 밟아야 하는가?
3. 정기점검을 마친 제조소등의 관계인은 점검 결과를 언제까지 누구에게 제출해야 하는가?
4. 제조소등에서 위험물 유출 사고가 발생했을 때 관계인과 이를 발견한 사람은 각각 무엇을 해야 하며, 관계인이 응급조치를 하지 않으면 누가 명령할 수 있는가?
5. 안전관리자 선임 의무(제15조)나 정기점검 의무(제18조)를 지키지 않으면 어느 벌칙·과태료 조항이 적용되는가?

## 장 안내

| 장 | 하는 일 | 주로 쓰는 것 |
|---|---|---|
| [3. Windows에 Neo4j 설치하기](neo4j-windows.html) | JDK 21, Neo4j ZIP, APOC, 메모리 상한, 비밀번호, 접속 확인 | `winget`, `neo4j.bat`, Neo4j Browser |
| [4. Cypher 기초](cypher-basics.html) | `CREATE`·`MERGE`·`MATCH`, 가변 길이 경로, 제약과 전문 색인 | Neo4j Browser, `cypher-shell.bat -f` |
| [5. 골든 퀘스천에서 스키마 설계하기](schema.html) | 질문에서 레이블·관계·속성 정하기 | Claude Code |
| [6. 인제스천 바이브 코딩](ingest.html) | PDF 3개 → 조·항·호 → Neo4j, 원문 대조 검증 | uv, PyMuPDF, Claude Code |
| [7. 엔티티 추출과 중의성 해소](disambiguation.html) | LLM 방식과 규칙·사전 방식, 사람 검토 | `claude -p` |
| [8. Neo4j MCP 서버 연결](mcp.html) | 읽기 전용으로 연결하기 | `uvx`, `.mcp.json` |
| [9. 골든 퀘스천 5개 묻기](questions.html) | 다섯 질문과 답, 원문 대조, 헤드리스 반복 실행 | `get-schema`, `read-cypher` |

실습을 마친 뒤 더 읽을거리: [10. 벡터 RAG로 같은 질문](https://www.uengine.org/docs/graphrag-law/vector-vs-graph.html) · [11. 마무리](https://www.uengine.org/docs/graphrag-law/wrap-up.html) · [부록: 문제 해결](https://www.uengine.org/docs/graphrag-law/troubleshooting.html)

## 필요한 기술 스택

이 실습은 아래 구성 요소가 서로 맞물려 동작합니다. 그림으로 보면 **PDF → (파이썬 코드) → Neo4j ← (MCP 서버) ← Claude Code**입니다. 각 요소가 무엇이고 왜 필요한지, 어느 버전을 써야 하는지, 이미 설치되어 있는지 확인하는 방법과 공식 내려받기 주소를 정리했습니다. 실제 설치는 [3장](neo4j-windows.html)에서 순서대로 따라 합니다.

### 꼭 준비할 것

준비물은 여섯 가지입니다. 1~4는 실습 자체에, 5·6은 Neo4j를 이 PC에서 직접 실행하는 데 필요합니다.

| | 준비물 | 한 줄 설명 |
|---|---|---|
| 1 | **Claude Code**(Claude Pro 이상 **유료 플랜**으로 로그인) | 스키마 설계·코드 작성·그래프 질의를 맡는 AI 에이전트 |
| 2 | **uv** | 파이썬과 패키지를 설치·실행하는 도구. **Python 3.12도 uv가 알아서 내려받습니다** |
| 3 | **Git for Windows** | 단계마다 커밋. Claude Code가 명령을 실행할 때 쓰는 Git Bash 포함 |
| 4 | **위험물안전관리법 PDF 3개**(법률·시행령·시행규칙) | 그래프로 만들 법령 원문(국가법령정보센터) |
| 5 | **JDK 21** | Neo4j를 실행하는 자바 런타임 |
| 6 | **Neo4j 5.26 Community**(APOC 포함) | 그래프 DB(ZIP으로 내려받아 설치) |

!!! note "Python은 따로 설치하지 않아도 되나요?"
    네, 따로 설치하지 않아도 됩니다. 6장에서 `uv init --python 3.12`로 프로젝트를 만들면 uv가 Python 3.12를 찾고, 없으면 자동으로 내려받아 그 프로젝트 전용으로 씁니다. 이미 다른 버전(예: Python 3.13)이 설치되어 있어도 서로 충돌하지 않습니다. 실습 PC(Python 3.13 설치됨)에서도 `uv init --bare --python 3.12`가 `Using CPython 3.12.12`로 3.12를 따로 준비했습니다. 다만 파이썬 코드를 실행할 때는 `python …`이 아니라 `uv run …`을 써야 그 3.12와 설치한 패키지가 쓰입니다.

### 한눈에 보기

| 구성 요소 | 무엇을 하나 | 필요한 버전 | 설치 확인 명령 |
|---|---|---|---|
| Windows | 실습 PC | Windows 10(21H2 이상) 또는 11, 64비트, 메모리 8GB 이상 권장 | `winver` |
| PowerShell | 이 교재의 모든 명령을 입력하는 셸 | Windows PowerShell 5.1(기본 포함) 또는 PowerShell 7.4 이상 | `$PSVersionTable.PSVersion` |
| JDK(자바) | Neo4j를 실행하는 런타임 | **Java 21**(17도 가능). 22 이상은 쓰지 않습니다 | `java -version` |
| Neo4j Community | 법령 그래프를 저장·조회하는 그래프 DB | **5.26.x**(이 교재는 5.26.33) | `C:\lab\neo4j\bin\neo4j.bat version` |
| APOC | Neo4j 확장 프로시저. MCP의 `get-schema`가 사용 | Neo4j와 같은 버전(ZIP에 포함) | `RETURN apoc.version();` |
| uv | 파이썬 설치·가상환경·패키지 관리 | 0.9 이상 | `uv --version` |
| Python | PDF 파싱·적재 코드 실행 | 3.12 — **따로 설치하지 않음**, uv가 자동으로 내려받음 | `uv python list` |
| Git for Windows | 단계별 커밋. Claude Code가 명령을 실행할 때 쓰는 Git Bash 포함 | 2.4x 이상 | `git --version` |
| Claude Code | 스키마 설계·코드 작성·질의를 맡는 AI 에이전트 | 2.1 이상, Claude Pro 이상 플랜 | `claude --version` |
| Neo4j MCP 서버 | Claude Code와 Neo4j를 잇는 통로 | 2.1.2(`uvx`로 실행, 설치 불필요) | `uvx neo4j-mcp-server@2.1.2 --version` |
| 웹 브라우저 | Neo4j Browser(`http://localhost:7474`) 화면 | Edge·Chrome 최신판 | |


!!! warning "JDK는 21을 쓰세요 — 「21 이상」이 아닙니다"
    Neo4j 5.26이 공식 지원하는 자바는 **Java 17과 Java 21뿐**입니다. Java 22·23·25처럼 더 높은 버전은 지원 목록에 없어 시작하지 않거나 예상치 못한 오류가 날 수 있습니다. 이미 다른 버전의 자바가 설치되어 있어도 괜찮습니다. JDK 21을 함께 설치하고 Neo4j를 띄우는 창에서만 `$env:JAVA_HOME`을 JDK 21로 지정하면 됩니다(3장 1단계). 참고로 Neo4j 2025.x 이후 판은 Java 21 이상을 요구하므로, 두 계열 모두에 맞는 21이 가장 안전합니다.

### 구성 요소별 설명과 내려받기

**PowerShell** — 이 교재의 모든 명령을 입력하는 셸입니다. Windows 10/11에 기본으로 들어 있는 **Windows PowerShell 5.1**로 충분하고, 따로 설치한 **PowerShell 7**(`pwsh`)에서도 같은 명령이 동작합니다. 두 버전은 한글 파일 저장(BOM), 빈 문자열 인자, 파이프 인코딩이 다르게 동작해서, 이 교재는 양쪽에서 똑같이 동작하는 방법만 골라 썼습니다(예: 파일은 `-Encoding ascii`나 `Write-Utf8`로 저장, `--tools ""` 대신 `--tools=`).

- 확인: 시작 메뉴에서 「Windows PowerShell」(파란 아이콘)을 열고 `$PSVersionTable.PSVersion`을 실행합니다. `5.1` 또는 `7.x`이면 됩니다.
- PowerShell 7을 원하면(선택): `winget install --id Microsoft.PowerShell -e` · [learn.microsoft.com/powershell/scripting/install/installing-powershell-on-windows](https://learn.microsoft.com/powershell/scripting/install/installing-powershell-on-windows)
- 「PowerShell ISE」는 쓰지 마세요. 외부 프로그램의 한글 출력과 대화형 입력이 일반 창과 다르게 동작합니다.

**JDK 21** — Neo4j는 자바로 만든 프로그램이라 자바 런타임이 있어야 실행됩니다. 이 교재는 Microsoft Build of OpenJDK 21을 씁니다. Eclipse Temurin 21 등 다른 배포판의 JDK 21도 됩니다.

- 설치: `winget install --id Microsoft.OpenJDK.21 -e`
- 내려받기: [learn.microsoft.com/java/openjdk/download#openjdk-21](https://learn.microsoft.com/java/openjdk/download#openjdk-21) · 대안 [adoptium.net/temurin/releases/?version=21](https://adoptium.net/temurin/releases/?version=21)
- 확인: `java -version`의 첫 줄이 `openjdk version "21.…"`. 다른 숫자가 나오면 `where.exe java`로 어느 자바가 먼저 잡히는지 봅니다.

**Neo4j 5.26 Community** — 노드와 관계로 데이터를 저장하는 그래프 데이터베이스입니다. 5.26은 장기 지원(LTS) 판이라 이 교재는 이 버전으로 검증했습니다. 설치 프로그램 없이 ZIP을 풀면 되고, 웹 화면 Neo4j Browser와 명령줄 도구 `cypher-shell`이 함께 들어 있습니다.

- 내려받기: [neo4j.com/deployment-center](https://neo4j.com/deployment-center/) → Graph Database Self-Managed → Community → 5.26.x → Windows
- 직접 주소: `https://dist.neo4j.org/neo4j-community-5.26.33-windows.zip`
- 확인: 이미 설치되어 있다면 그 폴더에서 `bin\neo4j.bat version`. Neo4j Desktop을 쓰고 있다면 3장의 안내 상자를 보세요.

**APOC** — Neo4j용 확장 프로시저 모음입니다. 8장의 MCP 서버가 `apoc.meta.schema`로 그래프 스키마를 읽으므로 반드시 켭니다. Community ZIP의 `labs` 폴더에 같은 버전의 jar가 들어 있어 따로 내려받지 않습니다.

- 문서: [neo4j.com/docs/apoc/5/installation](https://neo4j.com/docs/apoc/5/installation/)
- 확인: Neo4j를 띄운 뒤 `RETURN apoc.version();`

**uv와 Python 3.12** — uv는 파이썬 자체와 가상환경, 패키지를 한 번에 관리하는 도구입니다. 파이썬을 따로 설치하지 않아도 `uv`가 프로젝트에 맞는 Python 3.12를 내려받습니다. 6장에서 PDF 파싱(PyMuPDF)과 Neo4j 적재(neo4j 드라이버) 코드를 `uv run`으로 실행하고, 8장의 MCP 서버도 `uvx`로 실행합니다.

- 설치: `winget install --id astral-sh.uv -e` 또는 `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- 내려받기: [docs.astral.sh/uv/getting-started/installation](https://docs.astral.sh/uv/getting-started/installation/)
- 6장에서 쓰는 패키지: [PyMuPDF](https://pypi.org/project/PyMuPDF/) · [neo4j 드라이버](https://pypi.org/project/neo4j/) · [python-dotenv](https://pypi.org/project/python-dotenv/)
- 확인: `uv --version`, `uv python list`

**Git for Windows** — 단계마다 결과를 커밋해 되돌릴 수 있게 합니다. Windows용 Claude Code는 명령을 실행할 때 이 안에 들어 있는 Git Bash를 쓰므로 Claude Code보다 먼저 설치합니다.

- 설치: `winget install --id Git.Git -e`
- 내려받기: [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
- 확인: `git --version`

**Claude Code** — 터미널에서 동작하는 Claude의 코딩 에이전트입니다. 5~7장에서 스키마 설계와 적재 코드 작성을, 9장에서 MCP로 그래프 질의를 맡습니다. Claude Pro 이상 유료 플랜 계정으로 로그인합니다.

- 설치: `irm https://claude.ai/install.ps1 | iex`
- 문서: [docs.claude.com/en/docs/claude-code/setup](https://docs.claude.com/en/docs/claude-code/setup)
- 확인: `claude --version`

**Neo4j MCP 서버** — MCP(Model Context Protocol)로 Claude Code에 Neo4j 조회 도구(`get-schema`, `read-cypher`)를 제공하는 공식 서버입니다. PyPI의 `neo4j-mcp-server` 2.1.2에 Windows용 휠(`win_amd64`·`win_arm64`)이 있어 `uvx`가 처음 실행할 때 알아서 내려받습니다.

- 저장소·문서: [github.com/neo4j/mcp](https://github.com/neo4j/mcp) · [neo4j.com/docs/mcp/current](https://neo4j.com/docs/mcp/current/) · [pypi.org/project/neo4j-mcp-server](https://pypi.org/project/neo4j-mcp-server/)
- 확인: `uvx neo4j-mcp-server@2.1.2 --version`

### 한 번에 확인하기

이미 설치한 것이 있는지 PowerShell 창에 아래를 붙여 넣어 한 번에 봅니다. 없는 프로그램은 `없음`으로 나옵니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
foreach ($c in 'powershell','pwsh','java','git','uv','claude') {
  $p = Get-Command $c -ErrorAction SilentlyContinue
  '{0,-11} {1}' -f $c, ($(if ($p) { $p.Source } else { '없음' }))
}
java -version
```

`java -version`은 결과를 표준 오류로 내보내므로 빨간 글씨로 보일 수 있지만 오류가 아닙니다.


### 실습 폴더 위치

이 교재는 모든 파일을 `C:\lab` 아래에 둡니다.

| 경로 | 내용 |
|---|---|
| `C:\lab\neo4j` | Neo4j 설치 폴더(ZIP을 푼 곳). DB 파일은 이 안의 `data`에 생깁니다 |
| `C:\lab\law-graph` | 실습 폴더(git 저장소). PDF, 파이썬 코드, `.env`, `.mcp.json` |

사용자 폴더(`C:\Users\<이름>`)를 써도 되지만, 사용자 이름에 한글이나 공백이 있으면 자바·배치 파일이 경로를 잘못 읽는 일이 있어 짧은 영문 경로를 권합니다. 다른 드라이브를 쓰려면 명령의 `C:\lab`만 바꾸면 됩니다.

### 법령 PDF 받기

1. 국가법령정보센터([law.go.kr](https://www.law.go.kr))에서 `위험물안전관리법`으로 검색해 현행 법령 본문을 엽니다.
2. 본문 화면의 저장 기능에서 파일 형식으로 PDF를 선택해 내려받습니다.
3. 시행령과 시행규칙도 같은 방법으로 내려받습니다. 법률·시행령·시행규칙으로 3개입니다.

이 교재에서 쓴 판본은 다음과 같습니다. 파일 이름은 사이트에서 지정한 그대로 「법령명(종류)(번호)(시행일)」입니다.

| 법령 | 판본 | 파일 이름 |
|---|---|---|
| 법률 | 제20231호, 2025-08-07 시행 | `위험물안전관리법(법률)(제20231호)(20250807).pdf` |
| 시행령 | 대통령령 제36432호, 2026-07-01 시행 | `위험물안전관리법 시행령(대통령령)(제36432호)(20260701).pdf` |
| 시행규칙 | 행정안전부령 제628호, 2026-07-01 시행 | `위험물안전관리법 시행규칙(행정안전부령)(제00628호)(20260701).pdf` |

!!! note "판본이 다르면 숫자가 달라집니다"
    나중에 내려받으면 번호와 시행일이 달라지고 조·항·호 수도 조금씩 달라질 수 있습니다. 같은 결과를 확인하려면 위 판본을 연혁에서 찾아 내려받으세요. 이 PDF에는 별표·서식의 본문이 들어 있지 않습니다.

## 이 교재의 수치와 검증 범위

이 교재의 화면 출력과 수치는 두 종류입니다. 장마다 어느 쪽인지 밝혀 둡니다.

- **Windows에서 실행한 기록** — 3·4장의 설치·접속·Cypher, 6장의 uv 환경, 8장의 MCP 서버 기동처럼 운영체제에 따라 달라지는 명령은 Windows 11 PC에서 실제로 실행해 확인했습니다.
- **미리 실행해 둔 기록** — Claude Code가 쓰는 코드·설계·답(5~9장)은 모델이 실행할 때마다 달라집니다. 이 장들의 화면과 수치는 같은 PDF 3개로 미리 실행해 둔 기록이며, 여러분의 결과와 비교하는 기준으로 씁니다. 위험물안전관리법 3종의 조·항·호 수(조 157 · 항 276 · 호 357 · 목 67)는 판본이 같으면 같아야 합니다.

## 걸리는 시간과 비용

| 단계 | 예상 시간 | 비용(API 요금 환산) |
|---|---|---|
| 도구 설치와 Neo4j 첫 실행(3장) | 20~30분(내려받기 속도에 따라) | |
| Cypher 실습(4장) | 30분 | |
| 스키마 설계(5장) | Claude 작업 5~10분 | |
| 인제스천 코드 작성·검증(6장) | Claude 작업 15~20분 + 사람 대조 | |
| 엔티티 추출(7장) | 조 157개, 6개 동시 처리로 약 6분 | 기록 $0.268 |
| MCP 연결(8장) | 5분 | |
| 질문 하나(9장) | 20~40초 | 헤드리스 기록 평균 $0.45~0.88 |

비용 칸은 `claude -p`가 돌려준 API 요금 환산치입니다. 구독 플랜으로 로그인한 Claude Code에서는 따로 청구되지 않고 플랜 사용 한도에서 차감됩니다.

!!! warning "법령 해석은 원문으로"
    모델이 쓰는 문장과 Cypher는 실행할 때마다 달라질 수 있습니다. 실무에서 쓸 때는 답에 붙은 근거 조문을 반드시 원문으로 확인하세요.

## 정리와 다음 장

**이 장에서 한 일**

| 한 일 | 어디서 | 남은 것 |
|---|---|---|
| 실습 목표와 골든 퀘스천 다섯 개를 읽었습니다 | 이 페이지 | 마지막(9장)에 확인할 질문 |
| 필요한 도구(Claude Code 유료 플랜, uv, Git, JDK 21, Neo4j 5.26)와 버전을 확인했습니다 | 작업 창(Windows PowerShell) | 한 번에 확인 스크립트의 결과 |
| 위험물안전관리법 PDF 3개(법률·시행령·시행규칙)를 받았습니다 | 웹 브라우저 | `다운로드` 폴더의 PDF 3개 |

**왜 중요한가요?** 목표(골든 퀘스천)를 먼저 정해 두어야 5장에서 스키마를 설계할 때 「무엇을 답하려고 만드는 그래프인가」를 Claude에게 설명할 수 있습니다.

**다음 장(3장)에서 할 일:** 아직 설치되지 않은 도구를 설치하고, Neo4j를 ZIP으로 내려받아 설치하고 APOC를 켠 뒤, 매번 쓸 `env.ps1`을 만들어 Neo4j를 실행합니다. 모든 명령은 **작업 창(Windows PowerShell)** 에 입력합니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>위험물안전관리법 하나(PDF 3개)만 적재해도 골든 퀘스천 다섯 개에 모두 답할 수 있는 이유는 무엇인가요?</summary>

다섯 질문의 근거 조문(법 제6조·제15조·제18조·제27조와 벌칙 제35~39조, 이를 받는 시행령·시행규칙 조문)이 모두 위험물안전관리법 3종 안에 있기 때문입니다. 9장의 기록에서도 다섯 답의 근거 조문은 모두 위험물안전관리법·시행령·시행규칙이었습니다.
</details>

<details class="answer" markdown="1">
<summary>이 교재에서 도구를 모두 끌 때 `--tools ""`가 아니라 `--tools=`로 쓰는 까닭은 무엇인가요?</summary>

Windows PowerShell 5.1은 외부 프로그램에 빈 문자열 인자(`""`)를 넘기지 못하고 빼 버립니다. 그러면 `--tools` 뒤의 다음 인자가 값으로 잘못 들어갑니다. `--tools=`는 5.1과 7 모두에서 「빈 값」으로 정확히 전달됩니다(Windows PC에서 확인).
</details>
