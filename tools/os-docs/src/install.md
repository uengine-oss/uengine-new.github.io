# 설치와 첫 실행

> 설치 파일을 내려받아 실행하고, 첫 실행 과정에서 준비되는 항목을 살펴봅니다. 코딩 에이전트를 연결하는 방법도 다룹니다.

## 설치 파일 받기

[릴리스 페이지](https://github.com/uengine-oss/ontological-studio-releases/releases/latest)에서 운영체제에 맞는 파일을 받습니다.

| 운영체제 | 파일 |
|---|---|
| macOS (Apple Silicon) | `Ontological-Studio-mac-arm64.dmg` |
| Windows 10/11 (x64) | `Ontological-Studio-Setup-win-x64.exe` |

Intel 칩 Mac은 아직 지원하지 않습니다.

## macOS에 설치하기

<ol class="steps" markdown="1">
<li>DMG를 열고 <b>Ontological Studio</b> 아이콘을 <b>Applications</b> 폴더로 끌어다 놓습니다.</li>
<li>응용 프로그램 폴더에서 앱을 <b>오른쪽 클릭 › 열기</b>로 처음 실행합니다.</li>
<li>“확인되지 않은 개발자” 경고가 나오면 「열기」를 누릅니다. 한 번 허용하면 다음부터는 그냥 열립니다.</li>
</ol>

!!! warning "왜 경고가 나오나요?"
    지금 배포판은 Apple 개발자 인증서로 서명·공증되지 않았습니다. 경고 창에 「열기」 버튼이 없으면 **시스템 설정 › 개인정보 보호 및 보안**의 아래쪽에서 「그래도 열기」를 누르세요. 그래도 막히면 터미널에서 다음을 실행합니다.

    ```bash
    xattr -dr com.apple.quarantine "/Applications/Ontological Studio.app"
    ```

## Windows에 설치하기

<ol class="steps" markdown="1">
<li>EXE를 실행합니다. 관리자 권한 없이 현재 사용자에게만 설치됩니다.</li>
<li>SmartScreen이 “Windows의 PC 보호” 창을 띄우면 <b>추가 정보 › 실행</b>을 누릅니다.</li>
<li>설치가 끝나면 시작 메뉴에서 Ontological Studio를 엽니다.</li>
</ol>

!!! note "Windows에서 아직 안 되는 것"
    MySQL·Oracle·SQL Server 원천 연결은 macOS판에만 있습니다(PostgreSQL은 둘 다 됩니다). Claude Code를 Windows에서 쓰려면 Git for Windows가 먼저 설치돼 있어야 합니다.

## 첫 실행에 일어나는 일

앱을 열면 부팅 화면이 단계별 진행 상황을 보여 줍니다.

| 단계 | 하는 일 | 걸리는 시간(M 시리즈 기준) |
|---|---|---|
| PostgreSQL | 내 컴퓨터 안에서 데이터베이스 서버를 띄웁니다 | 1초 안쪽 |
| 첫 실행 준비 | 예제 업무 DB(ERP·WMS·CRM)를 만들고 데이터 패브릭에 등록합니다 | 처음 한 번만 |
| Ontological | 그래프 엔진(Ontological DB), Bolt 게이트웨이, 포털을 띄웁니다 | 1초 안쪽 |
| Studio | 구축·질의 화면, 액션 실행기, 예제 업무 시스템 3개를 띄웁니다 | 약 4~5초 |

처음 실행할 때는 예제 온톨로지 「공급망 운영 (예제)」도 함께 만들어 둡니다. 클래스 7개, 관계 6개, 액션 3개, 골든 퀘스천 3개, 골든 커맨드 4개가 들어 있어서, 설치하자마자 질의와 액션을 해 볼 수 있습니다.

모든 서버는 `127.0.0.1`(내 컴퓨터)에서만 접근할 수 있습니다.

## 코딩 에이전트 연결하기

온톨로지 구축, 자연어 질의, 대시보드 구성안, 코드 앱은 **에이전트**가 합니다. Ontological Studio는 다음 순서로 에이전트를 찾습니다.

1. 이 컴퓨터에 설치된 **Claude Code** 또는 **Codex CLI** — CLI의 로그인 정보를 사용하므로 별도의 API 키가 필요 없습니다. 기본값입니다.
2. CLI가 없으면 **내장 에이전트** — 이때는 `studio.env` 파일에 `OPENAI_API_KEY`를 넣어야 대화가 됩니다.

홈 화면 왼쪽 아래에 지금 쓰는 에이전트가 보입니다. 바꾸려면 메뉴 **런타임 › 에이전트**를 고릅니다. 「설정」 카드를 누르면 `studio.env`가 열립니다.

!!! tip "에이전트 없이도 할 수 있는 것"
    데이터소스 연결, 가상 노드 만들기, 포털에서 Cypher 쓰기는 에이전트 없이 동작합니다. 이 튜토리얼의 3·4부는 에이전트가 없어도 끝까지 따라 할 수 있습니다.

## 데이터는 어디에 저장되나요

| 항목 | 위치 (macOS) |
|---|---|
| 사용자 데이터 전체 | `~/Library/Application Support/Ontological Studio/` |
| 데이터베이스 | 위 폴더의 `pgdata` |
| 비밀번호(설치마다 무작위로 생성) | 위 폴더의 `secrets.json` |
| 로그 | 위 폴더의 `logs/` — 홈 화면 「로그 폴더」로 바로 열 수 있습니다 |

처음 상태로 되돌리고 싶으면 앱을 끈 뒤 이 폴더를 지우고 다시 실행합니다. 예제 DB와 예제 온톨로지가 새로 만들어집니다.

!!! exercise "확인"
    앱을 실행해 홈 화면이 뜨는지 확인하고, 왼쪽 아래에 「Ontological 연결됨」과 에이전트 이름이 나오는지 보세요.
