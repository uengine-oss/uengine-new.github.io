#!/usr/bin/env python3
"""issues.json → src/troubleshooting.md (부록 「문제 해결」).

    python3 tools/industry-docs/graphrag-law/make_troubleshooting.py [issues.json]

issues.json 은 교재를 만들며 막힌 곳을 한 건씩 적은 기록이다
({id, 단계, 증상, 원인, 조치, 확인, 범위, 제품결함여부}). 경로를 주지 않으면
환경변수 GRAPHRAG_LAW_ISSUES, 그다음 ~/uengine-platform/course-graphrag-law/issues.json 을 읽는다.

- 「학습자도 겪음」 항목은 단계별 절에, 「우리 환경에서만」 항목은 「이 교재를 찍은 환경」 절에 넣는다.
- 제목·관련 장·확인 여부 꼬리표와 코드 표시(백틱)만 여기서 덧붙이고, 증상·원인·조치·확인 글은 기록 그대로 쓴다.
- 「예외 상황」·「알려진 제약」·「이 교재를 찍은 환경」 머리글은 손으로 다듬은 고정 글이다(아래 상수).
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "src" / "troubleshooting.md"

# 단계별 절 — 순서대로. 여기 없는 「학습자도 겪음」 항목은 「그 밖」 절로 간다.
GROUPS = [
    ("설치·실행", ["GL-05"]),
    ("Cypher·색인", ["GL-02", "GL-03"]),
    ("스키마 설계", ["GL-04"]),
    ("인제스천", ["GL-06", "GL-07", "GL-08", "GL-09"]),
    ("중의성 해소", ["GL-10"]),
    ("MCP 연결", ["GL-11", "GL-12"]),
    ("질의", ["GL-14"]),
]

TITLES = {
    "GL-01": "tmux로 보낸 명령에서 세미콜론이 사라진다",
    "GL-02": "전문 색인을 만들었는데 「없는 색인」이라고 나온다",
    "GL-03": "기본 전문 색인이 「선임」으로 「선임하여야」를 못 찾는다",
    "GL-04": "커밋을 부탁했더니 실습 폴더 밖 메모리 파일을 고치려 한다",
    "GL-05": "claude를 처음 띄우면 Enter 한 번에 꺼진다",
    "GL-06": "적재한 조문의 띄어쓰기가 PDF와 다르다",
    "GL-07": "같은 조 번호가 두 번 나와 서로 덮는다",
    "GL-08": "다시 적재했는데 없어져야 할 관계가 남아 있다",
    "GL-09": "가운뎃점을 「·」로 통일했더니 「도지사」 검색이 1건뿐이다",
    "GL-10": "LLM 중의성 해소가 다른 주체를 합치고 약칭은 못 묶는다",
    "GL-11": ".mcp.json을 만들었는데 MCP 서버가 연결되지 않는다",
    "GL-12": "`${NEO4J_PASSWORD}`를 쓴 MCP 서버가 인증 실패로 뜨지 않는다(예방)",
    "GL-13": "claude가 auto mode로 뜨고 /mcp에 다른 서버가 함께 보인다",
    "GL-14": "답변 중에 「 밖의 관계기관」이라는 이상한 Actor가 보고됐다",
}

CHAPTERS = {
    "GL-01": [("3장", "neo4j-docker.html")],
    "GL-02": [("4장", "cypher-basics.html")],
    "GL-03": [("4장", "cypher-basics.html")],
    "GL-04": [("5장", "schema.html")],
    "GL-05": [("5장", "schema.html")],
    "GL-06": [("6장", "ingest.html")],
    "GL-07": [("6장", "ingest.html")],
    "GL-08": [("6장", "ingest.html")],
    "GL-09": [("6장", "ingest.html")],
    "GL-10": [("7장", "disambiguation.html")],
    "GL-11": [("8장", "mcp.html")],
    "GL-12": [("8장", "mcp.html")],
    "GL-13": [("5장", "schema.html"), ("8장", "mcp.html")],
    "GL-14": [("7장", "disambiguation.html"), ("9장", "questions.html")],
}

# 확인 여부 꼬리표. 없으면 「확인함」.
STATUS = {
    "GL-04": "확인함 — 메모 파일 1개는 남음",
    "GL-06": "확인함 — 규칙으로 못 정한 자리 약 9%는 남음",
    "GL-10": "확인함 — 남은 한계 있음",
    "GL-12": "확인함(예방 조치로 띄워 봄)",
    "GL-14": "고치지 않음 — 남아 있음을 확인, 고친 판은 재현 안 함",
}

# 기록 글을 그대로 쓰되 명령·코드만 백틱으로 감싼다. (id, 칸, 원래 글, 바꿀 글)
FIXES = [
    ("GL-01", "조치", "tmux send-keys -t gl -l '\\;'", "`tmux send-keys -t gl -l '\\;'`"),
    ("GL-02", "증상", "`CREATE FULLTEXT INDEX zz_cjk IF NOT EXISTS FOR (n:ZzT) ON EACH [n.text] OPTIONS {indexConfig: {`fulltext.analyzer`: 'cjk'}}`",
     "`` CREATE FULLTEXT INDEX zz_cjk IF NOT EXISTS FOR (n:ZzT) ON EACH [n.text] OPTIONS {indexConfig: {`fulltext.analyzer`: 'cjk'}} ``"),
    ("GL-02", "조치", "DROP INDEX zz_std IF EXISTS;", "`DROP INDEX zz_std IF EXISTS;`"),
    ("GL-02", "조치", "SHOW INDEXES YIELD name, type, labelsOrTypes, properties;", "`SHOW INDEXES YIELD name, type, labelsOrTypes, properties;`"),
    ("GL-03", "조치", "CREATE FULLTEXT INDEX … OPTIONS {indexConfig: {`fulltext.analyzer`: 'cjk'}};",
     "`` CREATE FULLTEXT INDEX … OPTIONS {indexConfig: {`fulltext.analyzer`: 'cjk'}}; ``"),
    ("GL-03", "조치", "CALL db.index.fulltext.listAvailableAnalyzers()", "`CALL db.index.fulltext.listAvailableAnalyzers()`"),
    ("GL-04", "증상", "~/.claude/projects/-Users-…-lab-law-graph/memory/commit-directly-on-main.md",
     "`~/.claude/projects/-Users-…-lab-law-graph/memory/commit-directly-on-main.md`"),
    ("GL-06", "조치", "uv run parse_law.py && uv run ingest.py --prune", "`uv run parse_law.py && uv run ingest.py --prune`"),
    ("GL-07", "조치", "MATCH (a:Article) WHERE NOT a.isCurrent RETURN a.pid, a.effectiveFrom",
     "`MATCH (a:Article) WHERE NOT a.isCurrent RETURN a.pid, a.effectiveFrom`"),
    ("GL-08", "조치", "uv run ingest.py --prune (data/", "`uv run ingest.py --prune` (`data/`"),
    ("GL-08", "조치", "처음부터 다시: uv run ingest.py --reset", "처음부터 다시: `uv run ingest.py --reset`"),
    ("GL-10", "조치", "STAND_ALONE 목록에 넣고 uv run ingest_semantic.py --reset",
     "`STAND_ALONE` 목록에 넣고 `uv run ingest_semantic.py --reset`"),
    ("GL-11", "조치", "claude mcp reset-project-choices", "`claude mcp reset-project-choices`"),
    ("GL-12", "증상", "\"NEO4J_MCP_PASSWORD\": \"${NEO4J_PASSWORD}\"", "`\"NEO4J_MCP_PASSWORD\": \"${NEO4J_PASSWORD}\"`"),
    ("GL-12", "조치", "cd law-graph && set -a; . ./.env; set +a; claude", "`cd law-graph && set -a; . ./.env; set +a; claude`"),
    ("GL-14", "조치", "uv run ingest_semantic.py --reset", "`uv run ingest_semantic.py --reset`"),
    ("GL-14", "확인", "MATCH (a:Actor) WHERE a.name STARTS WITH ' ' OR a.name CONTAINS '관계기관' RETURN a.name, a.aliases",
     "`MATCH (a:Actor) WHERE a.name STARTS WITH ' ' OR a.name CONTAINS '관계기관' RETURN a.name, a.aliases`"),
    # 녹화 이름(gl-0N, 마크)을 장 이름으로
    ("GL-01", "확인", "해당 장면(gl-01 106~164초)은 다시 찍음(-2 마크)", "3장 녹화의 해당 장면은 다시 찍음"),
    ("GL-03", "확인", "(gl-02 녹화 fulltext 마크)", "(4장 녹화의 전문 색인 장면)"),
    ("GL-05", "확인", "녹화 gl-03 claude-start 마크 뒤 장면에 그대로 있음", "5장 녹화의 Claude Code 첫 실행 장면에 그대로 있음"),
    ("GL-11", "확인", "녹화 gl-05 approve-mcp 마크 뒤 /mcp 에서", "8장 녹화에서 서버를 승인한 뒤 /mcp 에서"),
    ("GL-12", "확인", "connected 확인(gl-05)", "connected 확인(8장)"),
    ("GL-12", "원인", "${변수} 를", "`${변수}`를"),
]

# 영어·코드 뒤 조사는 붙여 쓴다(「`claude` 를」 → 「`claude`를」). 코드 칸 안은 건드리지 않는다.
PARTICLE = r"(에서|에게|으로|부터|까지|로만|처럼|라서|라고|라는|이라|이다|을|를|이|가|은|는|의|에|로|와|과|도|만)"
CODE = re.compile(r"(``.+?``|`[^`\n]+`)")


def tidy(text: str) -> str:
    parts = CODE.split(text)
    for k in range(0, len(parts), 2):
        seg = re.sub(r"(?<=[A-Za-z0-9)])\s+" + PARTICLE + r"(?=[\s,.)」·(]|$)", r"\1", parts[k])
        if k:
            seg = re.sub(r"^\s+" + PARTICLE + r"(?=[\s,.)」·(]|$)", r"\1", seg)
        parts[k] = seg
    return "".join(parts)

HEAD = """# 문제 해결

> 이 교재를 만들며 실제로 막힌 곳 14건을 단계별로 모았습니다. 오류 문구는 기록 그대로 옮겼으니 화면에 나온 글로 검색하세요. 기록에서 겪지 않은 예외 상황은 확인한 것과 확인하지 못한 것을 나눠 따로 적었습니다.

## 이 부록을 읽는 법

항목마다 **증상 → 원인 → 조치 → 확인**을 적었습니다. 「확인」은 조치한 뒤 실제로 고쳐졌는지 본 결과입니다. 각 장의 「막히면」 상자에는 그 장에서 학습자도 겪을 항목만 옮겼고, 여기에는 전부 있습니다. 이 교재를 찍은 환경에서만 생긴 항목은 맨 끝 「이 교재를 찍은 환경」에 따로 두었습니다.
"""

EXCEPTIONS = """## 예외 상황

이 기록에서는 겪지 않았지만 따라 하다 만날 수 있는 상황입니다. 기록으로 확인한 사실은 「확인함」, 짐작이거나 해 보지 않은 것은 「확인 못 함」으로 나눴습니다. 「확인 못 함」은 단정이 아니니 공식 문서와 함께 보세요.

### 네트워크·프록시와 이미지 내려받기

- **확인함** 인터넷이 필요한 곳: `docker pull neo4j:5.26`([3장](neo4j-docker.html)), uv가 Python 3.12와 패키지(PyMuPDF·neo4j·python-dotenv)를 받을 때([6장](ingest.html)), `uvx neo4j-mcp-server@2.1.2` 첫 실행 때 약 9.9MiB([8장](mcp.html)), Claude Code 자체. APOC 플러그인은 이미지 안의 `labs` 폴더에서 복사되므로 이미지를 받은 뒤에는 따로 내려받지 않습니다.
- **확인 못 함** 회사 프록시 뒤라면 Docker Desktop의 프록시 설정(Settings → Resources → Proxies)과 셸의 `HTTPS_PROXY`를 맞춰야 할 수 있습니다. 이미지 받기가 막히면 인터넷이 되는 PC에서 `docker save neo4j:5.26 -o neo4j-5.26.tar`로 저장해 옮긴 뒤 `docker load -i neo4j-5.26.tar`로 올리는 방법이 있습니다.

### 포트 7474·7687 충돌

- **확인 못 함** Neo4j Desktop(PBL 특강 교재의 방식)이나 다른 Neo4j 컨테이너가 이미 켜져 있으면 `docker run`이 포트를 잡지 못해 컨테이너가 시작되지 않습니다(이 기록에서는 겪지 않아 오류 문구가 없습니다). 누가 쓰는지는 macOS·Linux에서 `lsof -i :7687`, Windows에서 `netstat -ano | findstr 7687`, 컨테이너라면 `docker ps`로 봅니다.
- **확인 못 함** 쓰던 것을 멈추거나 `-p 17474:7474 -p 17687:7687`처럼 바깥 포트를 바꿉니다. 바꾸면 Bolt 주소를 쓰는 곳을 모두 고쳐야 합니다: Neo4j Browser 로그인 창의 Connection URL, 6장 `ingest.py`의 `URI`(코드에 `bolt://localhost:7687`로 적혀 있음), 8장 `.mcp.json`의 `NEO4J_MCP_URI`.

### 메모리 부족과 힙 설정

- **확인함** 이 교재의 설정(힙 512m~1G, 페이지 캐시 512M, 컨테이너 상한 `--memory 2g`)으로 모든 장을 마쳤습니다. 컨테이너 메모리는 시작 직후 926.4MiB / 2GiB, 의미층 적재와 질의까지 마친 뒤 1.49GiB / 2GiB였습니다. 그때 DB 폴더(`neo4j/data`)는 트랜잭션 로그를 포함해 약 530MB였습니다.
- **확인 못 함** Docker Desktop의 VM 메모리(Settings → Resources)가 작거나 다른 컨테이너가 많으면 Neo4j가 느려지거나 꺼질 수 있습니다. 꺼졌다면 `docker ps -a`로 상태를, `docker inspect -f '{{.State.OOMKilled}}' graphrag-law-neo4j`로 메모리 초과 때문인지 봅니다. 힙과 페이지 캐시의 합이 `--memory` 상한보다 넉넉히 작게 두세요.

### Apple Silicon·Intel, Windows 경로 차이

- **확인함** Apple Silicon macOS에서 `neo4j:5.26`은 arm64 판으로 받아져 그대로 돌았습니다(`docker image inspect neo4j:5.26 --format '{{.Architecture}}'` → `arm64`). 마운트한 폴더의 주인을 바꾼다는 경고(`Changing folder owner to neo4j`)는 무해했습니다.
- **확인 못 함** Intel Mac, Windows, Linux에서는 실행해 보지 않았습니다. Windows PowerShell에서 바꿔 써야 할 줄은 [3장](neo4j-docker.html)의 「Windows(PowerShell)에서 달라지는 줄」 상자에 모았습니다. WSL2 안에서 따라 하면 이 교재의 bash 명령을 그대로 쓸 수 있을 것으로 보이며, 실습 폴더는 WSL 파일 시스템 안(예: `~/law-graph`)에 두는 편이 볼륨 마운트에 유리하다고 알려져 있습니다.

### Claude 플랜 한도·느린 응답

- **확인함** 실제로 걸린 시간: 스키마 설계 4분 56초와 고치기 4분 36초([5장](schema.html)), 적재 코드 14분 35초와 띄어쓰기 고치기 5분 39초([6장](ingest.html)), 엔티티 추출 157번 호출 약 6분([7장](disambiguation.html)), 골든 퀘스천 한 개 약 20~50초([9장](questions.html)). 생각하는 동안 화면이 오래 멈춘 듯 보여도 기다리면 됩니다. `claude -p`가 돌려주는 비용(`total_cost_usd`)은 API 요금 환산치이며, 구독 로그인에서는 따로 청구되지 않고 사용 한도에 잡힙니다.
- **확인 못 함** 이 기록은 Claude Ultra 플랜에서 Fable 5.2(medium effort)로 찍었습니다. 더 작은 플랜에서 사용 한도에 걸리는지는 확인하지 못했습니다. 한도에 걸리면 화면에 나오는 초기화 시각까지 기다리거나, 7장의 추출처럼 많이 부르는 단계는 법령 범위를 줄여 나눠 돌리세요.

### 한글·가운뎃점·인코딩

- **확인함** 조문은 가운뎃점을 `ㆍ`(U+318D)로, 질문은 보통 `·`(U+00B7)로 씁니다. 눈에는 같아 보여도 `CONTAINS`와 열쇠 비교에서는 다른 글자입니다. 그래서 [5장](schema.html)에서 가운뎃점 7종을 `·`로 맞추는 정규화를 두었고, 전문 색인에서는 `·`를 공백으로 바꿉니다(GL-09). cypher-shell 표는 한글 폭 때문에 세로줄이 어긋나지만 값은 맞습니다. Python 3.12와 PyMuPDF로 한글 PDF 글을 그대로 읽었습니다.
- **확인 못 함** Windows 콘솔에서 한글이 깨지면 `chcp 65001`을 쓰거나 Windows Terminal과 PowerShell 7을 쓰세요. `.env`를 만들 때 UTF-8 BOM이 붙으면 읽는 쪽이 첫 줄의 변수 이름을 알아보지 못할 수 있습니다.

### law.go.kr 접속과 법령 판본

- **확인함** 이 교재는 국가법령정보센터(law.go.kr)에서 미리 받아 둔 PDF 9개를 썼습니다. 파일 이름에 법령 종류·번호·시행일이 들어 있습니다(예: `위험물안전관리법(법률)(제20231호)(20250807).pdf`). PDF에는 시행 예정 판본이 함께 실리고(GL-07), 별표·서식 본문은 없습니다.
- **확인 못 함** 내려받는 화면과 절차는 기록하지 않았습니다. 받는 날에 따라 판본이 바뀌면 조·항·호 수와 9장의 답이 이 교재와 달라질 수 있습니다. 참고한 PBL 특강 교재에는 클라우드 환경(해외 IP)에서 law.go.kr 접속이 막혀 내 PC에서 실행했다는 내용이 있으나, 이 교재에서는 확인하지 못했습니다.

### 공식 설치법과 다르게 한 것

- PBL 특강 교재와 달리 Neo4j Desktop 대신 Docker를, `pip install` 대신 uv를 썼습니다. Neo4j MCP 서버는 공식 저장소(github.com/neo4j/mcp)가 PyPI에 올린 `neo4j-mcp-server`를 `uvx`로 실행했습니다([8장](mcp.html)).
"""

LIMITS = """## 알려진 제약

- **별표·서식 본문이 없습니다.** PDF에 이름만 있어 과태료 세부 금액(시행령 별표 9), 행정처분 기준, 신고서 서식 내용은 답할 수 없고 상한(예: 500만원 이하)까지만 나옵니다.
- **줄바꿈 자리 띄어쓰기의 약 9%는 정하지 못했습니다.** 9개 법령의 줄바꿈 자리 3,871곳 가운데 규칙으로 정하지 못한 자리는 붙여 두었습니다. 위험물안전관리법 3종의 표본 3개 조만 PDF와 글자 단위로 맞췄고 전체를 다 보지는 않았습니다.
- **화학물질관리법·폐기물관리법은 대조하지 않았습니다.** 두 법의 벌칙 연결(`PENALIZES`)과 `Term`은 원문과 맞춰 보지 않았고, 「변경」「용기」 같은 흔한 낱말이 괄호 정의로 잡혀 용어가 된 경우가 있습니다. 풀지 못한 인용 7건도 들여다보지 않았습니다.
- **법령마다 시행일이 다릅니다.** 위험물안전관리법은 2025-08-07, 시행령·시행규칙은 2026-07-01 기준입니다. 답변에는 `Law.effectiveOn`을 함께 보여 주세요.
- **의미층은 검수 전입니다.** 위험물안전관리법 3종만 넣었고 `Norm`은 모두 `reviewed=false`입니다. GL-14(「 밖의 관계기관」 Actor)는 기록을 같은 데이터로 남기려고 고치지 않았습니다. 주체가 아닌 말이 `Actor`로 남은 것(kind=기타 51개), 수식절을 떼고 넓게 합친 이름 14가지, 조문 글자와 달라 값을 비운 `Norm` 속성(trigger 104건·deadline 6건, `uncheckedFields`에 표시)도 남아 있습니다. `DELEGATED_TO`·`NEXT`·`ON_BREACH_OF`·`SANCTIONED_BY` 관계는 아직 뽑지 않았습니다.
- **비용 수치는 환산치입니다.** `claude -p`의 `total_cost_usd`는 API 요금 환산치이며 구독 로그인이라 실제 청구액이 아닙니다. 9개 법령 전체를 추출할 때의 비용은 글자 수에 비례해 어림한 값입니다.
- **법령 해석은 원문으로 확인하세요.** 그래프와 모델의 답은 근거 조문을 찾아 주는 도구이며, 판단은 원문과 담당자의 몫입니다.
"""

ENV = """## 이 교재를 찍은 환경

본문의 화면과 수치는 아래 환경에서 얻었습니다. 이 절의 항목은 수강생의 기본 설치에서는 생기지 않는 것들입니다.

- **기록일과 판:** 2026-11-24, macOS(Apple Silicon), Docker Desktop 29.1.2, Neo4j 5.26.33 Community(`neo4j:5.26`), Claude Code 2.1.331(Fable 5.2, medium effort, Claude Ultra 플랜), uv 0.9.18, Python 3.12.12, PyMuPDF 2.1, Neo4j MCP 서버 2.1.2.
- **Docker VM:** 이 맥의 Docker Desktop VM(메모리 약 31GiB)은 다른 작업의 컨테이너와 함께 쓰는 환경이었습니다. Neo4j 컨테이너는 `--memory 2g` 상한 안에서 돌았고, 다른 컨테이너 때문에 생긴 문제는 기록에 없습니다.
- **녹화:** 터미널은 tmux 세션(126×30)을 웹 화면으로 그려 Playwright로 녹화했고, Neo4j Browser도 Playwright로 찍었습니다. 녹화용 셸에서는 언어 설정(LANG)을 맞추고 claude.ai 커넥터 MCP를 껐습니다(`ENABLE_CLAUDEAI_MCP_SERVERS=false`). 모델이 생각하는 긴 시간은 영상에서 잘랐습니다.
- **Claude Code 설정:** 프로젝트 `.claude/settings.local.json`에 `disableAllHooks: true`(이 맥의 명령 변환 훅을 끄려고)와 `effortLevel: medium`을 두었습니다. 권한 물음은 녹화 도구가 화면을 읽어 승인했고(위험한 명령과 실습 폴더 밖 경로에서는 멈춤), 지우는 명령(`ingest.py --prune`)과 실습 폴더 밖 메모리 색인 쓰기는 사람이 읽고 골랐습니다.
- **git:** 녹화 전에 실습 폴더에 `.git`이 이미 있어 `git init`이 「빈 깃 저장소를 다시 초기화했습니다」라고 나왔습니다. 새로 시작하면 「초기화했습니다」가 나옵니다.
- **남겨 둔 것:** 5장에서 생긴 자동 메모리 파일 하나(GL-04)는 실습 폴더 밖에 그대로 두었습니다.

이 환경에서만 생긴 문제는 두 건입니다.
"""

LABELS = ["증상", "원인", "조치", "확인"]


def load(path: Path) -> list[dict]:
    issues = json.loads(path.read_text(encoding="utf-8"))
    by_id = {i["id"]: i for i in issues}
    for iid, field, old, new in FIXES:
        item = by_id.get(iid)
        if not item or old not in item.get(field, ""):
            print(f"! FIXES 가 맞지 않는다: {iid} {field} — 기록이 바뀌었으면 FIXES 를 고칠 것", file=sys.stderr)
            continue
        item[field] = item[field].replace(old, new, 1)
    return issues


def chapter_links(iid: str) -> str:
    return ", ".join(f"[{n}]({u})" for n, u in CHAPTERS.get(iid, []))


def render_issue(i: dict) -> str:
    iid = i["id"]
    title = TITLES.get(iid, i["증상"][:40])
    out = [f"### {iid} · {title}", ""]
    links = chapter_links(iid)
    if links:
        out += [f"관련 장: {links}", ""]
    for label in LABELS:
        text = tidy(i.get(label, "").strip())
        if label == "확인":
            text = f"*{STATUS.get(iid, '확인함')}* — {text}"
        out.append(f"- **{label}** {text}")
    out.append("")
    return "\n".join(out)


def main() -> None:
    src = Path(sys.argv[1]) if sys.argv[1:] else Path(
        os.environ.get("GRAPHRAG_LAW_ISSUES", Path.home() / "uengine-platform/course-graphrag-law/issues.json"))
    issues = load(src)
    learner = [i for i in issues if i.get("범위") != "우리 환경에서만"]
    ours = [i for i in issues if i.get("범위") == "우리 환경에서만"]
    placed = {iid for _, ids in GROUPS for iid in ids}
    groups = [(name, [i for iid in ids for i in learner if i["id"] == iid]) for name, ids in GROUPS]
    rest = [i for i in learner if i["id"] not in placed]
    if rest:
        groups.append(("그 밖", rest))
    defects = [i["id"] for i in issues if i.get("제품결함여부")]

    parts = [HEAD]
    rows = ["| 단계 | 항목 | 관련 장 | 확인 |", "|---|---|---|---|"]
    for name, items in groups:
        for i in items:
            rows.append(f"| {name} | [{i['id']}](#{i['id'].lower()}) {TITLES.get(i['id'], '')} | {chapter_links(i['id'])} | {STATUS.get(i['id'], '확인함')} |")
    for i in ours:
        rows.append(f"| 이 교재를 찍은 환경 | [{i['id']}](#{i['id'].lower()}) {TITLES.get(i['id'], '')} | {chapter_links(i['id'])} | {STATUS.get(i['id'], '확인함')} |")
    parts.append("\n".join(rows) + "\n")
    parts.append(f"학습자도 겪을 항목 {len(learner)}건, 이 교재를 찍은 환경에서만 생긴 항목 {len(ours)}건입니다. "
                 + (f"제품 결함으로 본 항목: {', '.join(defects)}.\n" if defects else "제품 결함으로 본 항목은 없습니다.\n"))

    for name, items in groups:
        if not items:
            continue
        parts.append(f"## {name}\n")
        parts += [render_issue(i) for i in items]

    parts += [EXCEPTIONS, LIMITS, ENV]
    parts += [render_issue(i) for i in ours]
    text = "\n".join(parts).rstrip() + "\n"
    # 제목 앵커를 id 로 고정한다(목차 링크용): '### GL-06 · …' → attr_list 로 {#gl-06}
    lines = []
    for line in text.split("\n"):
        if line.startswith("### GL-"):
            iid = line[4:9]
            line = f"{line} {{#{iid.lower()}}}"
        lines.append(line)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(issues)}건 → {OUT}")


if __name__ == "__main__":
    main()
