# Neo4j Desktop 설치하기

> 실습에 쓸 도구(Git, uv, Claude Code)를 설치하고, Neo4j Desktop을 내려받아 설치합니다. Desktop에서 실습용 인스턴스를 만들어 시작한 뒤, 비밀번호를 .env 파일로 전달하고 Neo4j Browser로 준비가 끝났는지 확인합니다.

## 무엇을 · 왜

**Neo4j Desktop**은 내 PC에서 Neo4j 데이터베이스를 만들고, 켜고, 끄고, 플러그인을 설치하는 일을 화면에서 할 수 있게 해 주는 프로그램입니다. Neo4j를 실행하는 데 필요한 자바(Java)가 Desktop 안에 들어 있어 **JDK를 따로 설치하지 않아도 됩니다.** 질의는 Desktop에서 여는 **Neo4j Browser**에 붙여 넣어 실행합니다.

| 할 일 | 방법 |
|---|---|
| Neo4j 설치 | Neo4j Desktop 설치 파일을 내려받아 실행 |
| 데이터베이스 만들기 | Desktop에서 인스턴스 만들기(이름·버전·비밀번호) |
| 메모리 상한 | Desktop 기본값(힙 최대 1G, 페이지 캐시 512M) 그대로 |
| 실행과 멈춤 | Desktop의 Start · Stop 버튼 |
| 질의 도구 | Neo4j Browser(`http://localhost:7474`) |
| 비밀번호 전달 | `.env` 파일과 `env.ps1`(6장의 파이썬 코드, 8장의 MCP 서버가 사용) |

확장 플러그인 APOC는 처음 필요해지는 [8장](mcp.html)에서 설치합니다.

## 따라 하기

PowerShell 명령은 Windows에 기본으로 들어 있는 **Windows PowerShell 5.1**(시작 메뉴 「Windows PowerShell」)과 **PowerShell 7**(`pwsh`) 어느 쪽에서든 그대로 동작합니다. 관리자 권한으로 열 필요는 없습니다. 이 교재에서는 명령을 입력하는 PowerShell 창을 「**작업 창**」이라고 부릅니다.

<ol class="steps" markdown="1">
<li markdown="1">**도구를 설치합니다.** 이미 설치된 것은 건너뜁니다. `winget`은 Windows 10/11에 기본으로 들어 있는 패키지 관리자입니다.

**왜 하나요?** 6장 이후의 파이썬 코드(uv), 단계별 커밋(Git), 스키마 설계와 코드 작성(Claude Code)을 모두 이 도구로 합니다. Claude Code는 명령을 실행할 때 Git for Windows에 들어 있는 Git Bash를 쓰므로 Git을 먼저 설치합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
winget install --id Git.Git -e                   # Git for Windows (Claude Code보다 먼저)
winget install --id astral-sh.uv -e              # uv (Python 3.12는 uv가 나중에 받습니다)
```

`winget`이 처음 실행될 때 원본 약관 동의(`Y`)를 물을 수 있습니다. 설치가 끝나면 **PowerShell 창을 닫고 새로 엽니다.** 새 창이어야 바뀐 `Path`가 적용됩니다. 그다음 Claude Code를 설치합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
irm https://claude.ai/install.ps1 | iex
```

설치가 끝나면 다시 **창을 닫고 새로 연 뒤** 버전을 모두 확인합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
$PSVersionTable.PSVersion
git --version
uv --version
claude --version
```

`claude`를 찾을 수 없다고 나오면 설치 스크립트가 알려 준 폴더(보통 `%USERPROFILE%\.local\bin`)가 `Path`에 들어갔는지 확인하고 창을 새로 엽니다. Claude 계정 로그인은 5장에서 `claude`를 처음 실행할 때 브라우저로 합니다. **Claude Pro 이상 유료 플랜** 계정이어야 합니다. PowerShell 7을 쓰고 싶다면 `winget install --id Microsoft.PowerShell -e`로 따로 설치할 수 있지만 필수는 아닙니다.
</li>
<li markdown="1">**PowerShell 스크립트 실행을 허용합니다.** 이 교재는 이 장에서 만드는 `env.ps1`이라는 작은 스크립트로 비밀번호와 한글 설정을 창마다 불러옵니다. Windows의 기본 실행 정책(`Restricted`)은 모든 스크립트를 막으므로, 현재 사용자에 한해 로컬 스크립트를 허용합니다.

**왜 하나요?** Windows는 기본으로 모든 `.ps1` 스크립트를 막습니다. 비밀번호를 코드에 쓰지 않고 환경변수로 넘기고 한글 설정을 한 번에 적용하려면 `env.ps1`을 실행할 수 있어야 하므로, 내 계정에서 내가 만든 스크립트만 허용합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Get-ExecutionPolicy -List
```

`CurrentUser`가 `RemoteSigned`(또는 이미 `Unrestricted`)이면 됩니다. 인터넷에서 받은 서명 없는 스크립트는 여전히 막힙니다. 정책이 `Restricted`인 채로 `. .\env.ps1`을 실행하면 `running scripts is disabled on this system` 오류가 납니다. 회사 PC처럼 정책을 바꿀 수 없다면 창을 열 때마다 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`를 먼저 실행하세요. 그 창에서만 적용되고 창을 닫으면 사라집니다.
</li>
<li markdown="1">**실습 폴더를 git 저장소로 만듭니다.** 이 폴더(`C:\lab\law-graph`)에서 5장부터 Claude Code를 열고 단계마다 커밋합니다. `.gitignore`에는 비밀번호가 담긴 `.env`, 8장의 `.mcp.json`, 파이썬 가상환경, Claude Code 개인 설정을 넣습니다.

**왜 하나요?** 5장부터 Claude Code가 파일을 만들고 고칩니다. 단계마다 커밋해 두면 AI가 잘못 고쳤을 때 바로 되돌릴 수 있고, `.gitignore`로 비밀번호 파일이 실수로 공유되는 것을 처음부터 막습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
New-Item -ItemType Directory -Force C:\lab\law-graph | Out-Null
Set-Location C:\lab\law-graph
git init
Set-Content -Encoding ascii .gitignore ".env`n.mcp.json`n.venv/`n__pycache__/`ndata/`n.claude/settings.local.json"
Get-Content .gitignore
git add .gitignore; git commit -qm "실습 폴더 시작"
```

`git add`에서 `warning: in the working copy of '.gitignore', LF will be replaced by CRLF the next time Git touches it`가 나올 수 있습니다. Git for Windows가 기본 설정(`core.autocrlf=true`)으로 줄바꿈을 Windows 방식으로 맞춰 준다는 안내이며 오류가 아닙니다. 같은 블록을 두 번 실행하면 `Reinitialized existing Git repository`와 `nothing to commit, working tree clean`이 나오는데, 이미 커밋해 두었다는 뜻이니 그대로 넘어갑니다.

PowerShell 문자열 안의 `` `n``은 줄바꿈입니다. 내용이 영문뿐인 설정 파일은 `-Encoding ascii`로 저장하면 Windows PowerShell 5.1과 7에서 똑같은 파일이 만들어집니다(5.1의 `-Encoding utf8`은 파일 맨 앞에 BOM이라는 보이지 않는 3바이트를 붙입니다). 6장에서 `uv init --bare`는 `.gitignore`를 만들지 않으므로 이 단계의 `.gitignore`가 `.env`를 지키는 장치입니다. `data/`는 6장에서 PDF로 다시 만들 수 있는 중간 파일 폴더라 미리 넣었습니다. Neo4j의 DB 파일은 Neo4j Desktop이 따로 관리하므로 실습 폴더에 들어오지 않습니다.
</li>
<li markdown="1">**Neo4j Desktop을 내려받아 설치합니다.** [Neo4j Deployment Center](https://neo4j.com/deployment-center/)에서 **Neo4j Desktop**의 최신 버전과 **Windows (x86 exe)**를 고르고 Download를 누릅니다. 이름·이메일 같은 간단한 양식을 채우면 내려받기가 시작됩니다. 파일은 `neo4j-desktop-<버전>-x64.exe`(약 620MB)입니다.

**왜 하나요?** Desktop 하나로 Neo4j 설치, 인스턴스 만들기, 플러그인 설치, 시작·중지를 모두 화면에서 할 수 있습니다. Neo4j를 실행하는 자바도 함께 들어 있어 따로 준비할 것이 없습니다.

내려받은 `.exe`를 실행해 설치합니다. 「현재 사용자만」 설치를 고르면 관리자 권한이 필요 없습니다. 설치가 끝나면 Neo4j Desktop이 열립니다. 처음 실행할 때 나오는 라이선스 동의 화면을 읽고 동의하면 첫 화면이 나옵니다. Desktop에서 실행하는 Neo4j는 내 PC에서 개발·학습용으로 무료로 쓸 수 있습니다.
</li>
<li markdown="1">**실습용 인스턴스를 만듭니다.** Desktop 왼쪽 메뉴의 **Instances** 화면에서 **Create instance**를 누릅니다. **Instance details** 창이 열리면 다음과 같이 채우고 **Create Instance**를 누릅니다.

**왜 하나요?** 인스턴스는 Desktop이 관리하는 Neo4j 데이터베이스 서버 하나입니다. 실습 전용 인스턴스를 따로 만들어 두면 다른 프로젝트의 데이터와 섞이지 않고, 문제가 생기면 이 인스턴스만 지우고 다시 만들 수 있습니다.

| 항목 | 입력할 값 | 설명 |
|---|---|---|
| Instance name | `law-graph` | 화면에 보이는 이름입니다 |
| Neo4j version | 목록에서 맨 위의 최신 버전(예: `2026.10.2`) | 처음이면 Desktop이 그 버전을 내려받습니다 |
| Database user | `neo4j`(그대로 둡니다) | 데이터베이스에 접속할 사용자 이름입니다 |
| Password | 영문과 숫자로 **8자 이상** | 확인 입력칸이 없으니 오타 없이 입력합니다. 이 비밀번호를 6단계에서 한 번 더 입력합니다 |

비밀번호에는 **영문과 숫자만** 쓰세요. 6장의 파이썬 코드와 8장의 MCP 서버가 환경변수로 이 값을 받는데, 특수문자가 있으면 셸에 따라 다르게 해석될 수 있습니다. 만들기가 끝나면 목록에 `law-graph`가 **Local instance**로 나타납니다. `law-graph`의 **Start**를 눌러 시작하고, 상태가 **Running**(실행 중)으로 바뀌는지 봅니다. Desktop은 한 번에 인스턴스 **하나만** 실행합니다. 다른 인스턴스가 켜져 있으면 먼저 그것을 Stop 합니다.
</li>
<li markdown="1">**비밀번호를 .env 파일로 전달합니다.** 5단계에서 정한 비밀번호를 한 번 더 입력합니다. `Read-Host -AsSecureString`은 입력한 글자를 `*`로 가립니다. 두 번째 줄은 가린 값을 일반 문자열로 바꿔 환경변수에 넣습니다(Windows PowerShell 5.1과 7 모두 동작).

**왜 하나요?** 같은 비밀번호를 6장의 파이썬 코드와 8장의 MCP 서버가 함께 씁니다. 화면과 명령 기록에 남기지 않고 `.env` 한 곳에만 두면, 코드와 설정 파일을 공유해도 비밀번호는 새지 않습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
$s = Read-Host -AsSecureString 'Neo4j 비밀번호(5단계에서 정한 것)'
$env:NEO4J_PASSWORD = [Net.NetworkCredential]::new('', $s).Password
Set-Content -Encoding ascii .env "NEO4J_PASSWORD=$env:NEO4J_PASSWORD"
$env:NEO4J_PASSWORD.Length
```

마지막 줄이 비밀번호 글자 수를 출력하면 됩니다. 명령 기록(`Get-History`, PSReadLine 기록)에는 변수 이름만 남고 값은 남지 않습니다.
</li>
<li markdown="1">**창마다 쓸 설정 스크립트 env.ps1을 만듭니다.** `.env`의 비밀번호를 환경변수로 읽고, 한글이 깨지지 않도록 콘솔·파이프·파이썬의 출력 인코딩을 UTF-8로 맞춥니다.

**왜 하나요?** 새 PowerShell 창은 환경변수도 인코딩 설정도 모두 기본값으로 시작합니다. 창을 열 때마다 여러 줄을 손으로 치면 하나쯤 빠뜨리기 쉽고, 그러면 「어제는 됐는데 오늘은 비밀번호 오류」나 「한글이 깨진다」가 생깁니다. 한 파일로 만들어 두면 한 줄로 같은 상태를 만들 수 있습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
Set-Content -Encoding ascii env.ps1 @'
# Load .env (KEY=VALUE) into this PowerShell session
Get-Content "$PSScriptRoot\.env" | ForEach-Object {
  if ($_ -match '^\s*([^#=]+?)\s*=(.*)$') { Set-Item -Path "env:$($Matches[1])" -Value $Matches[2] }
}
# UTF-8 for console, pipes and Python
chcp.com 65001 > $null
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$OutputEncoding = [Text.UTF8Encoding]::new($false)
$env:PYTHONUTF8 = '1'
'@
. .\env.ps1
$env:NEO4J_PASSWORD.Length
git add env.ps1; git commit -qm "env.ps1: .env 와 UTF-8 설정"
```

`.Length`가 0이 아닌 숫자를 출력하면 됩니다. 이제부터 **새 PowerShell 창을 열 때마다** 이 두 줄로 시작합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
```

맨 앞의 `.`과 공백은 「이 창 안에서 실행하라」(점 소싱)는 뜻입니다. 빼면 스크립트가 따로 실행되어 설정이 남지 않습니다. `env.ps1`에는 비밀번호가 없으므로 커밋해도 됩니다. 스크립트를 영문으로만 쓰고 `ascii`로 저장한 것은, Windows PowerShell 5.1이 BOM 없는 UTF-8 스크립트의 한글을 잘못 읽기 때문입니다.

| 설정 | 하는 일 |
|---|---|
| `chcp.com 65001`, `[Console]::OutputEncoding` | 콘솔이 한글을 UTF-8로 주고받게 합니다(한국어 Windows의 기본은 CP949) |
| `$OutputEncoding` | PowerShell이 다른 프로그램(`claude` 등)에 파이프로 넘기는 글자를 UTF-8로 맞춥니다. 5.1의 기본값은 ASCII라 한글이 `?`가 됩니다 |
| `PYTHONUTF8=1` | 파이썬이 파일과 출력을 UTF-8로 다루게 합니다 |
</li>
<li markdown="1">**Neo4j Browser로 접속합니다.** `law-graph`가 Running 상태인지 확인한 뒤 웹 브라우저로 `http://localhost:7474`를 엽니다(Desktop에서 `law-graph`의 **Connect**를 눌러 여는 **Query** 도구도 같은 데이터베이스에 접속하며, 질의를 붙여 넣고 실행하는 방법은 같습니다). 「Connect to instance」 창에 연결 주소 `neo4j://localhost:7687`이 채워져 있습니다. Database user에 `neo4j`, Password에 5단계의 비밀번호를 입력하고 Connect를 누릅니다.

**왜 하나요?** 4장부터 모든 Cypher 질의를 Neo4j Browser에 붙여 넣어 실행합니다. 6장의 파이썬 코드와 8장의 MCP 서버도 같은 주소(`localhost:7687`)로 접속하므로, 여기서 접속되면 이후 단계의 연결 준비도 끝난 것입니다.

![Neo4j Browser 첫 화면 「Connect to instance」 — 연결 주소 neo4j://localhost:7687, 사용자 neo4j](img/gl-01-browser-login.webp)

위쪽 입력칸에 질의를 입력하고 Run(또는 Ctrl+Enter)을 누르면 결과가 아래에 쌓입니다. 한글은 Browser에서 그대로 입력하고 볼 수 있습니다.
</li>
</ol>

!!! note "비밀번호가 보이는 곳"
    화면과 명령 기록에는 비밀번호가 남지 않지만, `C:\lab\law-graph\.env` 파일에는 값이 들어 있습니다. 여러 사람이 쓰는 PC라면 실습용으로만 쓰는 비밀번호를 정하세요.

## 확인

두 가지를 확인합니다. 모두 확인되면 다음 장으로 넘어갑니다.

### 1. 버전

Neo4j Browser에 붙여 넣고 실행합니다.

**▶ Neo4j Browser(`http://localhost:7474`)에 붙여 넣기**

```cypher
CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition;
```

**출력 예시**

```text
name            versions        edition
"Neo4j Kernel"  ["2026.10.2"]   "enterprise"
"Cypher"        ["5", "25"]     ""
```

`Neo4j Kernel` 행에 인스턴스의 Neo4j 버전과 판(Desktop은 `enterprise`)이 나오면 접속된 것입니다. `Cypher` 행은 이 버전이 쓸 수 있는 Cypher 언어 판입니다. 버전 번호는 인스턴스를 만들 때 고른 것에 따라 다릅니다.

![접속한 뒤 dbms.components() 결과](img/gl-01-browser-connected.webp)

### 2. 작업 창에서 포트 확인

6장의 파이썬 코드와 8장의 MCP 서버는 작업 창 쪽에서 Neo4j에 접속합니다. 작업 창에서도 Neo4j가 응답하는지 확인합니다. `curl.exe`는 Windows 10 1803부터 기본으로 들어 있습니다. Windows PowerShell 5.1에서 `curl`이라고만 쓰면 `Invoke-WebRequest`의 별칭이 실행되므로 반드시 `.exe`까지 씁니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
curl.exe -s http://localhost:7474
```

**출력 예시**

```text
{"query_api":"http://localhost:7474/db/{databaseName}/query/v{queryApiMajorVersion}","bolt_routing":"neo4j://localhost:7687","query":"http://localhost:7474/db/{databaseName}/query/v2","dbms/cluster":"http://localhost:7474/dbms/cluster","db/cluster":"http://localhost:7474/db/{databaseName}/cluster","transaction":"http://localhost:7474/db/{databaseName}/tx","bolt_direct":"bolt://localhost:7687","neo4j_version":"2026.10.2","neo4j_edition":"enterprise","auth_config":{"oidc_providers":[]},"query_api_versions":["2.1"]}
```

버전에 따라 항목의 수와 순서는 다를 수 있습니다. `bolt_direct`가 `bolt://localhost:7687`이면 이후 장에서 쓸 주소가 맞습니다.

## 멈추기 · 다시 켜기 · 지우기

| 하려는 일 | 방법 | 데이터 |
|---|---|---|
| 멈추기 | Desktop에서 `law-graph`의 **Stop** | 그대로 남음 |
| 다시 켜기 | Desktop에서 `law-graph`의 **Start**. 작업 창은 새로 열 때마다 `Set-Location C:\lab\law-graph; . .\env.ps1` | 멈추기 전 그대로 |
| 그래프만 비우기 | Neo4j Browser에서 `MATCH (n) DETACH DELETE n` | 노드·관계만 사라지고 비밀번호·플러그인은 남음 |
| 완전히 처음부터 | Desktop에서 `law-graph`를 Stop 한 뒤 인스턴스 메뉴에서 삭제하고 5단계부터 다시 | 모두 사라짐 |

Desktop 창을 닫아도 실행 중인 인스턴스가 계속 도는지는 Desktop 설정에 따라 다릅니다. 실습하는 동안에는 Desktop을 열어 둡니다.

!!! warning "막히면"
    **Start를 눌렀는데 `port 7687 (bolt) is already in use by another process`처럼 포트(7474·7687)를 이미 쓰고 있다고 나옵니다**

    - 원인: 다른 인스턴스나, Desktop 밖에서 따로 실행한 Neo4j(ZIP 판, 서비스, 다른 프로그램)가 같은 포트를 쓰고 있습니다.
    - 조치 1: Desktop에서 다른 인스턴스를 모두 Stop 하고 다시 Start 합니다.
    - 조치 2: 그래도 같으면 작업 창에서 그 포트를 쓰는 프로그램을 찾습니다.

    **▶ 작업 창(Windows PowerShell)에 입력**

    ```powershell
    Get-NetTCPConnection -LocalPort 7474,7687 -State Listen -ErrorAction SilentlyContinue |
      ForEach-Object { $p = Get-Process -Id $_.OwningProcess; [pscustomobject]@{ Port = $_.LocalPort; Id = $p.Id; Path = $p.Path } }
    ```

    - `Path`가 `java.exe`이면 다른 Neo4j입니다. 내가 띄운 것이면 그 창에서 Ctrl+C로 끄거나 해당 프로그램에서 멈춘 뒤 다시 Start 합니다. 누군가 쓰고 있는 DB라면 끄지 말고, 실습이 끝날 때까지 그 DB를 잠시 멈춰도 되는지 먼저 확인합니다.

    **Neo4j Browser에서 비밀번호가 틀렸다고 나옵니다(`The client is unauthorized due to authentication failure.`)**

    - 원인: 5단계에서 정한 비밀번호와 다르게 입력했습니다. 사용자 이름은 `neo4j`입니다.
    - 조치: 비밀번호가 기억나지 않으면 `law-graph`를 Stop 한 뒤 삭제하고 5단계부터 새로 만듭니다(아직 데이터가 없으므로 잃을 것이 없습니다). 6단계의 `.env`도 새 비밀번호로 다시 만듭니다.

    **`. .\env.ps1`에서 「이 시스템에서 스크립트를 실행할 수 없으므로…」가 나옵니다**

    - 원인: 2단계의 실행 정책 설정을 하지 않았습니다.
    - 조치: 2단계를 실행합니다. 정책을 바꿀 수 없는 PC라면 창을 열 때마다 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`를 먼저 실행합니다.

    **내려받기 페이지에서 Desktop 파일이 받아지지 않습니다**

    - 원인: 양식을 다 채우지 않았거나 브라우저가 큰 파일 내려받기를 막았습니다.
    - 조치: 양식의 필수 칸을 채우고 다시 누릅니다. 브라우저의 내려받기 목록에서 「유지」를 누르면 받아집니다.

## 정리와 다음 장

**이 장에서 한 일**

| 한 일 | 어디서 | 결과물 |
|---|---|---|
| Git·uv·Claude Code 설치와 버전 확인 | 작업 창 | `git --version` 등이 버전을 출력 |
| 실행 정책, 실습 폴더와 git 저장소, `.gitignore` 준비 | 작업 창 | `C:\lab\law-graph` |
| Neo4j Desktop 설치, `law-graph` 인스턴스 만들고 시작 | Neo4j Desktop | Local instance `law-graph`, Running 상태 |
| 비밀번호를 `.env`에 저장, `env.ps1` 작성 | 작업 창 | `.env`(git에 올라가지 않음), `env.ps1` |
| 접속 확인 | Neo4j Browser / 작업 창 | `dbms.components()` 결과, `curl.exe` 응답 |

**기억할 것:** 실습하는 동안 Neo4j Desktop을 열어 두고 `law-graph`를 Running 상태로 둡니다. Cypher 질의는 **Neo4j Browser**에, PowerShell 명령은 **작업 창**에 입력합니다. 새 작업 창을 열면 언제나 `Set-Location C:\lab\law-graph; . .\env.ps1`부터 실행합니다.

**다음 장(4장)에서 할 일:** 지금 접속한 Neo4j Browser에서 작은 연습용 그래프(위험물안전관리법 제15조 일부)를 직접 만들고 조회하면서 `CREATE`·`MERGE`·`MATCH` 같은 Cypher 기본 문법을 익힙니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>Neo4j Desktop을 쓰면 JDK를 따로 설치하지 않아도 되는 까닭은 무엇인가요?</summary>

Neo4j는 자바 프로그램이지만, Neo4j Desktop 안에 Neo4j를 실행하는 자바가 함께 들어 있습니다. Desktop은 인스턴스를 시작할 때 이 자바를 씁니다. 이 교재는 질의도 Neo4j Browser에서 실행하므로 PC에 따로 자바를 설치할 일이 없습니다.
</details>

<details class="answer" markdown="1">
<summary>비밀번호를 Desktop에 한 번, .env에 한 번 입력하는 까닭은 무엇인가요?</summary>

Desktop에 입력한 비밀번호는 Neo4j 데이터베이스의 `neo4j` 사용자 비밀번호입니다. `.env`에 저장한 값은 6장의 파이썬 코드와 8장의 MCP 서버가 그 데이터베이스에 접속할 때 쓰는 값입니다. 둘이 같아야 접속됩니다. `.env`는 `.gitignore`에 들어 있어 커밋되지 않습니다.
</details>
