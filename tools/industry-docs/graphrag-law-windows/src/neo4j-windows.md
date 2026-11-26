# Windows에 Neo4j 설치하기

> JDK 21을 설치하고 Neo4j 5.26 Community를 Windows용 ZIP으로 내려받아 설치한 뒤, ZIP에 들어 있는 APOC 플러그인을 켜고 메모리 상한을 설정합니다. 비밀번호는 화면에 보이지 않게 입력해 환경변수와 .env 파일로 전달하고, 콘솔 로그·cypher-shell·Neo4j Browser로 준비가 끝났는지 확인합니다.

## 무엇을 · 왜

이 장에서는 **Neo4j 5.26 Community**를 Windows용 ZIP으로 내려받아 `C:\lab\neo4j`에 풀어 설치하고, 자바로 직접 실행합니다. 설치 프로그램이나 관리자 권한이 필요 없고, 폴더 하나에 모든 것이 들어 있어 지우고 다시 설치하기도 쉽습니다.

| 할 일 | 방법 |
|---|---|
| Neo4j 설치 | ZIP을 내려받아 `C:\lab\neo4j`에 풀기 |
| APOC 켜기 | `labs\apoc-*-core.jar`를 `plugins\`로 복사하고 `neo4j.conf`에 허용 설정 |
| 메모리 상한 | `neo4j.conf`에 `server.memory.heap.max_size=1G` 등 |
| 비밀번호 | `neo4j-admin dbms set-initial-password` |
| 데이터 위치 | `C:\lab\neo4j\data` |
| 실행과 멈춤 | `neo4j.bat console`을 창 하나에 띄우고 Ctrl+C로 멈춤 |
| 질의 도구 | `C:\lab\neo4j\bin\cypher-shell.bat`, Neo4j Browser |

APOC는 8장에서 연결하는 Neo4j MCP 서버의 `get-schema`가 `apoc.meta.schema`로 스키마를 읽기 때문에 지금 켜 둡니다.

!!! note "Neo4j Desktop을 이미 쓰고 있다면"
    Neo4j Desktop으로 5.26 DBMS를 만들고 APOC 플러그인을 추가해도 이 교재를 따라 할 수 있습니다. 그때는 아래의 `C:\lab\neo4j`를 Desktop의 DBMS 폴더(DBMS 메뉴 ⋯ → Open folder → DBMS)로 바꿔 읽으세요. 이 교재는 명령으로 재현하기 쉬운 ZIP 방식을 기준으로 합니다.

## APOC란 무엇이고 왜 켜나요

**APOC**(Awesome Procedures On Cypher)는 Neo4j 회사가 관리하는 **확장 프로시저 모음**입니다. Cypher만으로는 하기 어려운 일, 예를 들어 그래프에 어떤 레이블·관계·속성이 있는지 요약하기(`apoc.meta.schema`), 문자열·날짜 다루기, 데이터 가져오기·내보내기 등을 `CALL apoc.…` 형태로 부를 수 있게 해 줍니다. Neo4j 본체와 별도의 jar 파일(플러그인)로 배포되며, Neo4j와 **같은 버전**의 APOC를 써야 합니다.

이 실습에서 APOC가 꼭 필요한 곳은 한 군데입니다. 8장에서 연결하는 Neo4j MCP 서버의 `get-schema` 도구가 내부에서 `apoc.meta.schema`를 불러 그래프 구조를 Claude에게 알려 줍니다. APOC가 꺼져 있으면 `get-schema`가 실패하고, Claude는 그래프에 무엇이 있는지 모른 채 Cypher를 짐작으로 쓰게 됩니다.

| 구분 | APOC Core | APOC Extended |
|---|---|---|
| 들어 있는 곳 | Neo4j 설치 폴더의 `labs\apoc-<버전>-core.jar`(Community ZIP·Desktop 모두 포함) | 별도 내려받기 |
| 이 교재 | **씁니다**(`apoc.meta.schema` 등) | 쓰지 않습니다 |

켜는 방법은 두 가지 설치 방식마다 조금 다릅니다. 어느 쪽이든 원리는 같습니다. `labs`에 있는 jar를 `plugins`로 옮기고, 필요한 권한을 `neo4j.conf`에 적은 뒤 Neo4j를 다시 시작합니다.

### ZIP 설치(이 교재의 기본)

아래 「따라 하기」 5단계에서 합니다. 요약하면 다음 두 가지입니다.

1. `Copy-Item C:\lab\neo4j\labs\apoc-*-core.jar C:\lab\neo4j\plugins\` — jar를 플러그인 폴더로 복사합니다. 파일 이름의 버전 번호가 Neo4j 버전과 같은지 봅니다(예: `apoc-5.26.33-core.jar`).
2. `neo4j.conf`에 `dbms.security.procedures.unrestricted=apoc.*` — APOC 프로시저가 Neo4j 내부 기능을 쓰도록 허용합니다. 이 줄이 없으면 일부 APOC 프로시저가 「unrestricted가 아니다」라는 이유로 막힙니다.

### Neo4j Desktop을 쓰는 경우

Neo4j Desktop에서 만든 DBMS도 폴더 구조가 같습니다(`bin`, `conf`, `labs`, `plugins`). 두 방법 중 하나를 고릅니다.

- **화면에서 켜기** — Desktop에서 DBMS를 고르고 플러그인(Plugins) 목록에서 APOC를 찾아 설치(Install)를 누른 뒤 DBMS를 다시 시작합니다. Desktop이 같은 버전의 jar를 `plugins`에 넣고 설정을 맞춰 줍니다.
- **파일로 켜기** — DBMS를 멈춘 상태에서 그 DBMS 폴더(DBMS 메뉴의 폴더 열기 → DBMS)를 PowerShell에서 `$h`로 두고 ZIP과 같은 명령을 실행합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
$h = '<DBMS 폴더 경로>'      # 예: C:\Users\<이름>\.Neo4jDesktop2\Data\dbmss\dbms-…
Copy-Item "$h\labs\apoc-*-core.jar" "$h\plugins\"
Get-ChildItem "$h\plugins"
```

`neo4j.conf`의 `dbms.security.procedures.unrestricted` 줄은 아래 5단계의 「같은 키 지우고 다시 쓰기」 명령에서 `$conf` 경로만 `"$h\conf\neo4j.conf"`로 바꿔 실행합니다. 처음 설치한 Desktop DBMS는 `labs`에 jar만 있고 `plugins`에는 `README.txt`만 있어 APOC가 **꺼진 상태**입니다(실제 PC에서 확인).

### 켜졌는지 확인하기

Neo4j를 (다시) 시작한 뒤 Neo4j Browser나 cypher-shell에서 실행합니다.

**▶ Neo4j Browser(`http://localhost:7474`)에 붙여 넣기** — 작업 창에서 `Write-Utf8`로 파일에 저장해 `& $cs … -f 파일`로 실행해도 됩니다

```cypher
RETURN apoc.version() AS apoc;
SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta' RETURN count(*) AS n;
CALL apoc.meta.schema() YIELD value RETURN size(keys(value)) AS 레이블과관계수;
```

첫 줄이 Neo4j와 같은 버전 번호를, 둘째 줄이 0보다 큰 수를 돌려주면 켜진 것입니다. 셋째 줄은 그래프가 비어 있으면 `0`입니다. `Unknown function 'apoc.version'`이 나오면 jar가 `plugins`에 없거나 Neo4j를 다시 시작하지 않은 것입니다.

## 따라 하기

모든 명령은 PowerShell 창에서 실행합니다. Windows에 기본으로 들어 있는 **Windows PowerShell 5.1**(시작 메뉴 「Windows PowerShell」)과 **PowerShell 7**(`pwsh`) 어느 쪽이든 그대로 동작하도록 썼고, Windows 11 PC의 Windows PowerShell 5.1에서 실행해 확인했습니다. 관리자 권한으로 열 필요는 없습니다.

<ol class="steps" markdown="1">
<li markdown="1">**도구를 설치합니다.** 이미 설치된 것은 건너뜁니다. `winget`은 Windows 10/11에 기본으로 들어 있는 패키지 관리자입니다.

**왜 하나요?** Neo4j는 자바 프로그램이라 JDK가 없으면 실행되지 않고, 6장 이후의 파이썬 코드(uv)·커밋(Git)·명령 입력(PowerShell)도 모두 여기서 설치한 도구로 합니다. 버전을 맞춰 두면 교재의 출력과 여러분의 출력이 같아져 문제를 찾기 쉽습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
winget install --id Microsoft.OpenJDK.21 -e      # JDK 21
winget install --id Git.Git -e                   # Git for Windows (Claude Code보다 먼저)
winget install --id astral-sh.uv -e              # uv (Python 3.12는 uv가 나중에 받습니다)
```

`winget`이 처음 실행될 때 원본 약관 동의(`Y`)를 물을 수 있습니다. 설치가 끝나면 **PowerShell 창을 닫고 새로 엽니다.** 새 창이어야 바뀐 `Path`가 적용됩니다. 그다음 Claude Code를 설치합니다. Git for Windows가 먼저 있어야 Claude Code가 명령을 실행할 Git Bash를 찾습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
irm https://claude.ai/install.ps1 | iex
```

설치가 끝나면 다시 **창을 닫고 새로 연 뒤** 버전을 모두 확인합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
$PSVersionTable.PSVersion
java -version
git --version
uv --version
claude --version
```

`claude`를 찾을 수 없다고 나오면 설치 스크립트가 알려 준 폴더(보통 `%USERPROFILE%\.local\bin`)가 `Path`에 들어갔는지 확인하고 창을 새로 엽니다. Claude 계정 로그인은 5장에서 `claude`를 처음 실행할 때 브라우저로 합니다. **Claude Pro 이상 유료 플랜** 계정이어야 합니다.

`java -version`의 첫 줄에 `21.`이 보이면 됩니다(Microsoft 배포판은 `openjdk version "21.…"`, Oracle JDK는 `java version "21.…"`). Neo4j 5.26은 Java 17 또는 21에서 동작합니다. PowerShell 7을 쓰고 싶다면 `winget install --id Microsoft.PowerShell -e`로 따로 설치할 수 있지만 필수는 아닙니다. 여러 자바가 설치되어 있다면 이 세션에서만 JDK 21을 쓰도록 `JAVA_HOME`을 지정합니다(경로는 설치된 버전에 맞게 고칩니다).

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
where.exe java                                         # 자바가 여러 개면 여러 줄이 나옵니다
Get-ChildItem 'C:\Program Files\Microsoft\jdk-21*' -Directory | Select-Object -ExpandProperty FullName
$env:JAVA_HOME = 'C:\Program Files\Microsoft\jdk-21.0.9.10-hotspot'   # 위 출력으로 바꿉니다
```

winget으로 설치했다면 두 번째 줄이 JDK 21 폴더를 보여 줍니다. 아무것도 나오지 않으면 JDK를 다른 곳에 설치한 것입니다. `where.exe java`가 보여 준 경로 중 `jdk-21`이 들어간 줄에서 끝의 `\bin\java.exe`를 뺀 폴더가 `JAVA_HOME`입니다(예: `D:\Dev_tools\jdk-21.0.8\bin\java.exe` → `D:\Dev_tools\jdk-21.0.8`). 실제 PC에서도 JDK가 `D:\Dev_tools`에 있어 두 번째 줄은 빈 결과였습니다.

이 설정은 지금 창에만 적용됩니다. `java -version`이 처음부터 21을 보여 주었다면 필요 없습니다. 필요한 경우에는 6단계에서 `env.ps1`을 만든 뒤 `Add-Content -Encoding ascii env.ps1 "`$env:JAVA_HOME = '<위 경로>'"`로 한 줄을 덧붙여 두면, Neo4j를 띄우는 창에서도 자동으로 JDK 21이 쓰입니다.
</li>
<li markdown="1">**PowerShell 스크립트 실행을 허용합니다.** 이 교재는 이 장에서 만드는 `env.ps1`이라는 작은 스크립트로 비밀번호와 한글 설정을 창마다 불러옵니다. Windows의 기본 실행 정책(`Restricted`)은 모든 스크립트를 막으므로, 현재 사용자에 한해 로컬 스크립트를 허용합니다.

**왜 하나요?** Windows는 기본으로 모든 `.ps1` 스크립트를 막습니다. 비밀번호를 코드에 쓰지 않고 환경변수로 넘기고 한글 설정을 한 번에 적용하려면 `env.ps1`을 실행할 수 있어야 하므로, 내 계정에서 내가 만든 스크립트만 허용합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Get-ExecutionPolicy -List
```

`CurrentUser`가 `RemoteSigned`(또는 이미 `Unrestricted`)이면 됩니다. 인터넷에서 받은 서명 없는 스크립트는 여전히 막힙니다. 정책이 `Restricted`인 채로 `. .\env.ps1`을 실행하면 `running scripts is disabled on this system` 오류가 납니다(실제로 확인함). 회사 PC처럼 정책을 바꿀 수 없다면 창을 열 때마다 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`를 먼저 실행하세요. 그 창에서만 적용되고 창을 닫으면 사라집니다.
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

PowerShell 문자열 안의 `` `n``은 줄바꿈입니다. `-Encoding ascii`로 쓰는 데는 이유가 있습니다. Windows PowerShell 5.1의 `-Encoding utf8`은 파일 맨 앞에 BOM(보이지 않는 3바이트)을 붙이는데, 그러면 git이 첫 줄을 `.env`가 아닌 다른 글자로 읽어 **비밀번호 파일이 커밋될 수 있습니다.** 내용이 영문뿐인 파일은 `ascii`로 쓰면 5.1과 7 모두 안전합니다. 6장에서 `uv init --bare`는 `.gitignore`를 만들지 않으므로 이 단계의 `.gitignore`가 `.env`를 지키는 유일한 장치입니다. `data/`는 6장에서 PDF로 다시 만들 수 있는 중간 파일 폴더라 미리 넣었습니다. Neo4j의 DB 파일은 `C:\lab\neo4j`에 있어 실습 폴더에 들어오지 않습니다.
</li>
<li markdown="1">**Neo4j ZIP을 내려받아 풉니다.** [Neo4j Deployment Center](https://neo4j.com/deployment-center/)의 Community Edition → Windows 항목과 같은 파일입니다. 아래 `$v`를 Deployment Center에 나온 최신 5.26.x 번호로 바꿔도 됩니다.

**왜 하나요?** Windows에서 Neo4j를 설치하는 가장 단순한 방법입니다. 설치 프로그램이나 관리자 권한 없이 폴더 하나로 끝나므로 지우고 다시 하기도 쉽고, 이 교재가 검증한 5.26 버전을 정확히 고를 수 있습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
$v = '5.26.33'
$ProgressPreference = 'SilentlyContinue'   # 5.1에서 진행 표시줄 때문에 내려받기가 아주 느려지는 것을 막습니다
Invoke-WebRequest "https://dist.neo4j.org/neo4j-community-$v-windows.zip" -OutFile C:\lab\neo4j.zip
if (-not (Test-Path C:\lab\neo4j)) {
  Expand-Archive C:\lab\neo4j.zip -DestinationPath C:\lab -Force
  Rename-Item "C:\lab\neo4j-community-$v" C:\lab\neo4j
}
Get-ChildItem C:\lab\neo4j
```

`if (-not (Test-Path …))`는 이미 `C:\lab\neo4j`가 있으면 압축 풀기와 이름 바꾸기를 건너뜁니다. 이 줄이 없으면 이 단계를 두 번 실행했을 때 `Cannot create a file when that file already exists.` 오류가 납니다(실제 PC에서 확인). 처음부터 다시 설치하고 싶다면 Neo4j를 멈춘 뒤 `C:\lab\neo4j` 폴더를 지우고 다시 실행합니다.

`bin`, `conf`, `data`, `labs`, `lib`, `logs`, `plugins` 폴더가 보이면 됩니다. 이후 명령은 폴더 이름에 버전이 없도록 `C:\lab\neo4j`로 부릅니다.
</li>
<li markdown="1">**APOC를 켜고 메모리 상한을 설정합니다.** APOC jar는 ZIP 안의 `labs` 폴더에 이미 들어 있어 따로 내려받지 않습니다. 설정은 `neo4j.conf`에서 같은 키의 줄을 지우고 원하는 값으로 다시 씁니다.

**왜 하나요?** 8장의 MCP 서버가 그래프 구조를 Claude에게 알려 줄 때 APOC 프로시저를 씁니다. 메모리 상한은 노트북에서 Neo4j가 메모리를 다 차지해 다른 프로그램(브라우저, Claude Code)이 느려지는 것을 막습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Copy-Item C:\lab\neo4j\labs\apoc-*-core.jar C:\lab\neo4j\plugins\
Get-ChildItem C:\lab\neo4j\plugins

$conf = 'C:\lab\neo4j\conf\neo4j.conf'
$want = [ordered]@{
  'server.memory.heap.initial_size'       = '512m'
  'server.memory.heap.max_size'           = '1G'
  'server.memory.pagecache.size'          = '512M'
  'dbms.security.procedures.unrestricted' = 'apoc.*'
}
$lines = Get-Content $conf | Where-Object { -not $want.Contains(($_ -split '=', 2)[0].Trim()) }
$lines += $want.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }
Set-Content -Encoding ascii $conf $lines
C:\lab\neo4j\bin\neo4j-admin.bat server validate-config
```

마지막 명령이 `Configuration file validation successful.`로 끝나면 설정이 올바릅니다. 같은 키를 지우고 다시 쓰므로 여러 번 실행해도 결과가 같습니다. 주석 줄(`#server.memory…`)은 키 이름 앞에 `#`이 붙어 있어 지워지지 않습니다.

파일 끝에 네 줄을 그냥 덧붙이면 안 되는 이유도 확인했습니다. ① 원래 파일이 줄바꿈 없이 끝나면 첫 줄이 앞 줄 끝에 붙고, ② 이미 값이 있는 키(예: `server.memory.pagecache.size`)가 두 번 나오면 `validate-config`가 `declared multiple times`로 실패하고 Neo4j가 시작하지 않습니다.

| 설정 | 뜻 |
|---|---|
| `server.memory.heap.initial_size` · `max_size` | 자바 힙의 초기(512m)·최대(1G) 크기. 실습 PC의 메모리를 Neo4j가 너무 많이 쓰지 않게 막습니다 |
| `server.memory.pagecache.size` | 페이지 캐시(512M). 그래프 파일을 메모리에 올려 두는 공간입니다 |
| `dbms.security.procedures.unrestricted=apoc.*` | APOC 프로시저에 내부 API 접근을 허용합니다. 이 줄이 없으면 `apoc.meta.schema` 같은 프로시저가 막혀 8장의 MCP 서버가 스키마를 읽지 못합니다 |

`[ordered]@{ … }`는 순서를 지키는 키-값 표입니다. `Where-Object`로 같은 키의 기존 줄을 걸러 낸 뒤 새 줄 네 개를 붙여 다시 저장합니다.
</li>
<li markdown="1">**비밀번호를 정해 환경변수와 .env로 전달합니다.** `Read-Host -AsSecureString`은 입력한 글자를 `*`로 가립니다. 두 번째 줄은 가린 값을 일반 문자열로 바꿔 환경변수에 넣습니다(Windows PowerShell 5.1과 7 모두 동작). Neo4j 5의 비밀번호는 **8자 이상**이어야 하고, 배치 파일(`.bat`)에 인자로 넘기므로 **영문과 숫자만** 쓰세요(`&`, `^`, `%`, `!`, `"` 같은 글자는 cmd가 다르게 해석합니다).

**왜 하나요?** 같은 비밀번호를 Neo4j, 6장의 파이썬 코드, 8장의 MCP 서버가 함께 씁니다. 화면과 명령 기록에 남기지 않고 `.env` 한 곳에만 두면, 코드와 설정 파일을 공유해도 비밀번호는 새지 않습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
$s = Read-Host -AsSecureString 'Neo4j 비밀번호(영문·숫자 8자 이상)'
$env:NEO4J_PASSWORD = [Net.NetworkCredential]::new('', $s).Password
Set-Content -Encoding ascii .env "NEO4J_PASSWORD=$env:NEO4J_PASSWORD"
C:\lab\neo4j\bin\neo4j-admin.bat dbms set-initial-password $env:NEO4J_PASSWORD
```

마지막 명령은 `Changed password for user 'neo4j'. IMPORTANT: this change will only take effect if performed before the database is started for the first time.`를 출력합니다. 문구 그대로 **DB를 처음 시작하기 전에만** 적용되므로 Neo4j를 실행하는 단계보다 먼저 합니다. 명령 기록(`Get-History`, PSReadLine 기록)에는 변수 이름만 남고 값은 남지 않습니다.
</li>
<li markdown="1">**창마다 쓸 설정 스크립트 env.ps1을 만듭니다.** `.env`의 비밀번호를 환경변수로 읽고, 한글이 깨지지 않도록 콘솔·파이썬·자바의 출력 인코딩을 UTF-8로 맞추고, cypher-shell 경로를 `$cs`에, 한글 파일을 BOM 없는 UTF-8로 저장하는 `Write-Utf8` 함수를 정의합니다.

**왜 하나요?** 새 PowerShell 창은 환경변수도 인코딩 설정도 모두 기본값으로 시작합니다. 창을 열 때마다 여러 줄을 손으로 치면 하나쯤 빠뜨리기 쉽고, 그러면 「어제는 됐는데 오늘은 비밀번호 오류」나 「한글이 깨진다」가 생깁니다. 한 파일로 만들어 두면 한 줄로 같은 상태를 만들 수 있습니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
Set-Content -Encoding ascii env.ps1 @'
# Load .env (KEY=VALUE) into this PowerShell session
Get-Content "$PSScriptRoot\.env" | ForEach-Object {
  if ($_ -match '^\s*([^#=]+?)\s*=(.*)$') { Set-Item -Path "env:$($Matches[1])" -Value $Matches[2] }
}
# UTF-8 for console, pipes, Python and Java (cypher-shell)
chcp.com 65001 > $null
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$OutputEncoding = [Text.UTF8Encoding]::new($false)
$env:PYTHONUTF8 = '1'
$env:JAVA_OPTS = '-Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8'
# Shortcuts
$cs = 'C:\lab\neo4j\bin\cypher-shell.bat'
function Write-Utf8([string]$Path, [string]$Text) {
  [IO.File]::WriteAllText((Join-Path (Get-Location) $Path), $Text, [Text.UTF8Encoding]::new($false))
}
'@
. .\env.ps1
$env:NEO4J_PASSWORD.Length
git add env.ps1; git commit -qm "env.ps1: .env 와 UTF-8 설정"
```

`.Length`가 0이 아닌 숫자(비밀번호 글자 수)를 출력하면 됩니다. 이제부터 **새 PowerShell 창을 열 때마다** 이 두 줄로 시작합니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
```

맨 앞의 `.`과 공백은 「이 창 안에서 실행하라」(점 소싱)는 뜻입니다. 빼면 스크립트가 따로 실행되어 설정이 남지 않습니다. `env.ps1`에는 비밀번호가 없으므로 커밋해도 됩니다. 스크립트를 영문으로만 쓰고 `ascii`로 저장한 것은, Windows PowerShell 5.1이 BOM 없는 UTF-8 스크립트의 한글을 잘못 읽기 때문입니다.
</li>
<li markdown="1">**Neo4j를 실행합니다.** PowerShell 창을 **하나 더** 열고 아래를 실행합니다. 이 창은 Neo4j 전용으로 두고 실습하는 동안 닫지 않습니다. 앞으로 이 창을 「**Neo4j 창**」, 명령을 입력하는 원래 창을 「**작업 창**」이라고 부릅니다.

**왜 하나요?** 이후 모든 장이 `localhost:7687`(Bolt)과 `localhost:7474`(Browser)에 접속합니다. 전용 창에 띄워 두면 로그를 바로 볼 수 있고, Ctrl+C 한 번으로 깔끔하게 멈출 수 있습니다.

**▶ Neo4j 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
C:\lab\neo4j\bin\neo4j.bat console
```

`env.ps1`을 먼저 읽으면 한글 로그가 깨지지 않고, `JAVA_HOME`을 넣어 두었다면 JDK 21이 쓰입니다. `console`은 Neo4j를 이 창에서 앞쪽 프로세스로 실행합니다. 멈출 때는 이 창에서 Ctrl+C를 누릅니다. 처음 실행할 때 Windows 보안 경고(방화벽)가 나오면 「개인 네트워크」만 허용하거나 취소해도 됩니다. Neo4j 5는 기본으로 `localhost`에서만 연결을 받으므로 이 실습에는 영향이 없습니다.
</li>
</ol>

### 한글이 깨지지 않게 하는 설정

한국어 Windows 콘솔의 기본 문자 집합은 CP949입니다. Windows 11 PC에서 한글이 어디서 깨지는지 직접 측정한 결과입니다.

| 경로 | 측정 결과 | 대응 |
|---|---|---|
| PowerShell → `.bat` → 자바(cypher-shell)로 넘기는 인자 | 한글은 그대로 전달됨. 단 질의 안의 **큰따옴표는 사라짐** | Cypher 문자열은 작은따옴표로 씁니다 |
| `-f`로 넘긴 질의 파일 | Java 21이 BOM 없는 UTF-8 파일을 정상으로 읽음 | `Write-Utf8`로 BOM 없이 저장 |
| 자바·파이썬 출력을 파이프·파일로 받을 때 | 자바는 CP949로, 파이썬은 콘솔 설정에 따라 출력해 서로 어긋나면 깨짐 | `chcp 65001` + `[Console]::OutputEncoding` + `PYTHONUTF8` + `JAVA_OPTS`를 **함께** UTF-8로 |
| PowerShell → 외부 프로그램으로 파이프 | 5.1은 기본이 ASCII라 한글이 `?`로 바뀜 | `$OutputEncoding` |

네 설정 중 일부만 바꾸면 오히려 깨집니다. 예를 들어 콘솔만 UTF-8로 바꾸고 `JAVA_OPTS`를 빼면 cypher-shell 출력이 `�`로 나옵니다. 그래서 `env.ps1`에 모아 항상 함께 적용합니다.

!!! note "비밀번호가 보이는 곳"
    화면과 명령 기록에는 비밀번호가 남지 않지만, `C:\lab\law-graph\.env` 파일에는 값이 들어 있습니다. 여러 사람이 쓰는 PC라면 실습용으로만 쓰는 비밀번호를 정하세요.

## 확인

세 가지 방법으로 확인합니다. 모두 확인되면 다음 장으로 넘어갑니다.

### 1. 콘솔에 Started.가 나오는지

Neo4j를 띄운 창에 다음과 같은 줄이 나옵니다.

**출력 예시**

```text
… INFO  Starting...
… INFO  ======== Neo4j 5.26.33 ========
… INFO  Bolt enabled on localhost:7687.
… INFO  HTTP enabled on localhost:7474.
… INFO  Remote interface available at http://localhost:7474/
… INFO  Started.
```

`Bolt enabled on localhost:7687`처럼 `localhost`로 나오면 이 PC 안에서만 접속을 받는다는 뜻입니다. 같은 로그는 `C:\lab\neo4j\logs\neo4j.log`에도 쌓입니다.

### 2. cypher-shell로 버전과 APOC 확인

처음 창(`C:\lab\law-graph`)으로 돌아와 ZIP에 들어 있는 `cypher-shell.bat`으로 Bolt 포트에 접속합니다. 문장 끝의 `;`를 빠뜨리지 마세요.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
& $cs -u neo4j -p $env:NEO4J_PASSWORD "CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition;"
& $cs -u neo4j -p $env:NEO4J_PASSWORD "RETURN apoc.version() AS apoc;"
& $cs -u neo4j -p $env:NEO4J_PASSWORD "SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta' RETURN count(*) AS n;"
```

**출력 예시**

```text
name, versions, edition
"Neo4j Kernel", ["5.26.33"], "community"
apoc
"5.26.33"
n
10
```

`$cs`는 `env.ps1`이 정해 둔 cypher-shell 경로입니다. 경로를 변수에 넣었을 때는 앞에 `&`(호출 연산자)를 붙여야 실행됩니다.

### 3. Neo4j Browser

먼저 HTTP 포트가 응답하는지 확인합니다. `curl.exe`는 Windows 10 1803부터 기본으로 들어 있습니다. Windows PowerShell 5.1에서 `curl`이라고만 쓰면 `Invoke-WebRequest`의 별칭이 실행되므로 반드시 `.exe`까지 씁니다.

**▶ 작업 창(Windows PowerShell)에 입력**

```powershell
curl.exe -s http://localhost:7474
```

**출력 예시**

```text
{"bolt_routing":"neo4j://localhost:7687","query":"http://localhost:7474/db/{databaseName}/query/v2","transaction":"http://localhost:7474/db/{databaseName}/tx","bolt_direct":"bolt://localhost:7687","neo4j_version":"5.26.33","neo4j_edition":"community"}
```

웹 브라우저로 `http://localhost:7474`를 엽니다. 「Connect to instance」 창에 연결 주소 `neo4j://localhost:7687`이 채워져 있습니다. Database user에 `neo4j`, Password에 정한 비밀번호를 입력하고 Connect를 누릅니다.

![Neo4j Browser 첫 화면 「Connect to instance」 — 연결 주소 neo4j://localhost:7687, 사용자 neo4j](img/gl-01-browser-login.webp)

위쪽 입력칸에 질의를 입력하고 Run(또는 Ctrl+Enter)을 누르면 결과가 아래에 쌓입니다.

**▶ Neo4j Browser(`http://localhost:7474`)에 붙여 넣기** — 작업 창에서 `Write-Utf8`로 파일에 저장해 `& $cs … -f 파일`로 실행해도 됩니다

```cypher
CALL dbms.components() YIELD name, versions, edition
RETURN name, versions, edition
```

![접속한 뒤 dbms.components() 결과 — Neo4j Kernel 5.26.33 community](img/gl-01-browser-connected.webp)

## 멈추기 · 다시 켜기 · 지우기

| 하려는 일 | 방법 | 데이터 |
|---|---|---|
| 멈추기 | Neo4j 창에서 Ctrl+C | `C:\lab\neo4j\data`에 그대로 |
| 다시 켜기 | 새 PowerShell 창에서 `Set-Location C:\lab\law-graph; . .\env.ps1; C:\lab\neo4j\bin\neo4j.bat console` | 멈추기 전 그대로 |
| DB만 처음부터 | 멈춘 뒤 `Remove-Item -Recurse -Force C:\lab\neo4j\data\databases\neo4j, C:\lab\neo4j\data\transactions\neo4j` | 그래프 데이터만 사라지고 비밀번호는 남음 |
| 완전히 처음부터 | 멈춘 뒤 `Remove-Item -Recurse -Force C:\lab\neo4j`, 4단계부터 다시 | 모두 사라짐 |

창을 띄워 두기 번거로우면 `neo4j.bat windows-service install` 뒤 `neo4j.bat start`로 Windows 서비스로 등록할 수 있습니다. 서비스 등록에는 관리자 권한이 필요하고, 실습이 끝난 뒤 `neo4j.bat windows-service uninstall`로 지워야 하므로 이 교재는 `console`을 씁니다.

!!! warning "막히면"
    **`neo4j.bat console`이 `Unable to find any JVMs matching version "17"` 또는 Java 관련 오류로 멈춥니다**

    - 원인: `java`가 `Path`에 없거나, 다른 버전(예: Java 8·11)이 먼저 잡혔습니다.
    - 조치: Neo4j를 띄우는 창에서 `$env:JAVA_HOME`을 JDK 21 폴더로 지정한 뒤 다시 실행합니다(1단계). `& "$env:JAVA_HOME\bin\java.exe" -version`으로 확인합니다.

    **`Lock file has been locked by another process` 또는 `Neo4j web server failed to start`가 나옵니다**

    - 원인: 같은 Neo4j가 이미 다른 창(또는 Neo4j Desktop)에서 실행 중입니다. 실제 PC에서 두 번째로 `console`을 실행하자 이 오류로 끝났고, 먼저 띄운 Neo4j는 계속 정상으로 동작했습니다.
    - 조치: 새로 띄울 필요가 없습니다. 이미 떠 있는 Neo4j 창을 그대로 쓰거나, 그 창에서 Ctrl+C로 멈춘 뒤 다시 실행합니다.

    **포트 7474·7687을 이미 쓰고 있다고 나옵니다**

    - 원인: Neo4j Desktop의 다른 DBMS나 다른 프로그램이 같은 포트로 떠 있습니다.
    - 조치: `Get-NetTCPConnection -LocalPort 7474,7687 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalPort, OwningProcess`로 프로세스를 찾고, 그 프로그램을 멈춘 뒤 다시 실행합니다.

    **비밀번호가 틀렸다고 나옵니다(`The client is unauthorized due to authentication failure.`)**

    - 원인: `set-initial-password`를 DB를 처음 시작한 뒤에 실행해 적용되지 않았거나, 새 창이라 `$env:NEO4J_PASSWORD`가 비어 있습니다.
    - 조치: `$env:NEO4J_PASSWORD.Length`로 값이 있는지 봅니다(0이면 `. .\env.ps1`로 다시 읽습니다). 처음 시작한 뒤라면 Neo4j를 멈추고 `C:\lab\neo4j\data\dbms\auth.ini`를 지운 다음 비밀번호 단계부터 다시 합니다.

    **Invoke-WebRequest가 404를 돌려줍니다**

    - 원인: 5.26의 마지막 자리 번호가 바뀌어 예전 파일이 내려갔습니다.
    - 조치: Deployment Center에서 최신 5.26.x 번호를 확인해 `$v`를 바꿉니다.

## 정리와 다음 장

**이 장에서 한 일**

| 한 일 | 어디서 | 결과물 |
|---|---|---|
| JDK 21·Git·uv·Claude Code 설치와 버전 확인 | 작업 창 | `java -version` 등이 버전을 출력 |
| 실습 폴더와 git 저장소, `.gitignore` 준비 | 작업 창 | `C:\lab\law-graph` |
| Neo4j 5.26 ZIP 설치, APOC jar 복사, `neo4j.conf` 수정 | 작업 창 | `C:\lab\neo4j`, `validate-config` 통과 |
| 비밀번호를 `.env`에 저장하고 초기 비밀번호 설정 | 작업 창 | `.env`(git에 올라가지 않음) |
| `env.ps1` 작성 | 작업 창 | 환경변수·한글(UTF-8)·`$cs`·`Write-Utf8`을 한 번에 준비 |
| Neo4j 실행과 확인 | Neo4j 창 / 작업 창 / Browser | `Started.`, `RETURN apoc.version()` 결과 |

**기억할 것:** PowerShell 창은 두 개를 씁니다. **Neo4j 창**은 `neo4j.bat console`을 띄운 채 그대로 두고, 명령은 **작업 창**에 입력합니다. 새 창을 열면 언제나 `Set-Location C:\lab\law-graph; . .\env.ps1`부터 실행합니다.

**다음 장(4장)에서 할 일:** 지금 띄운 Neo4j에 작은 연습용 그래프(위험물안전관리법 제15조 일부)를 직접 만들고 조회하면서 `CREATE`·`MERGE`·`MATCH` 같은 Cypher 기본 문법을 익힙니다. 주로 **Neo4j Browser**에 붙여 넣습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>Windows ZIP으로 설치한 Neo4j에서 APOC를 켜려면 무엇을 해야 하나요?</summary>

ZIP의 `labs` 폴더에 들어 있는 `apoc-*-core.jar`를 `plugins` 폴더로 복사하고, `neo4j.conf`에 `dbms.security.procedures.unrestricted=apoc.*`를 넣은 뒤 Neo4j를 다시 시작합니다. 따로 내려받을 파일은 없습니다.
</details>

<details class="answer" markdown="1">
<summary>set-initial-password를 Neo4j를 처음 실행하기 전에 해야 하는 까닭은 무엇인가요?</summary>

명령이 출력하는 문구 그대로 「DB를 처음 시작하기 전에 실행했을 때만」 적용되기 때문입니다. 처음 시작한 뒤에는 이미 만들어진 사용자 정보가 우선하므로, 그때는 Neo4j Browser에서 비밀번호를 바꾸거나 `data\dbms\auth.ini`를 지우고 다시 해야 합니다.
</details>

<details class="answer" markdown="1">
<summary>비밀번호에 영문과 숫자만 쓰라고 한 이유는 무엇인가요?</summary>

`neo4j-admin.bat`과 `cypher-shell.bat`은 배치 파일이라 인자를 cmd가 한 번 더 해석합니다. `&`, `^`, `%`, `!`, `"` 같은 글자는 cmd에서 특별한 뜻이 있어 비밀번호가 잘리거나 바뀔 수 있습니다.
</details>
