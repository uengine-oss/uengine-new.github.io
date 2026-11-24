#!/usr/bin/env python3
"""issues.json → src/troubleshooting.md (부록 「문제 해결」). issues.json 을 고친 뒤 다시 돌린다.

    python3 tools/industry-docs/nvidia-auto-ontology/make_troubleshooting.py

이 교재를 만들며 실제로 겪은 것만 issues.json 에 적는다(tutorial-video-studio 스킬 1-1). 이 스크립트는 그 기록을
단계별 표·예외 상황·이 교재를 찍은 환경·알려진 제약으로 나눠 옮길 뿐, 내용을 지어 넣지 않는다. 예외 상황 가운데
이번에 겪지 않은 것은 EXCEPTION_NOTES 의 일반 안내(「겪지 않음」 표시)로만 싣는다.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS = json.loads((HERE / "issues.json").read_text(encoding="utf-8"))
STAGES = ["설치·실행", "연결", "구축", "질의", "연동", "영상·화면"]
CH = {"index": "0장", "setup": "1장", "connect": "2장", "compile": "3장", "explore": "4장", "ask": "5장", "mcp": "6장",
      "api": "7장", "studio": "8장"}
EXCEPTIONS = ["네트워크·프록시", "API 키 만료·한도·요금", "포트 충돌", "메모리·디스크 부족", "칩·OS 차이(Apple Silicon·Intel·Windows)",
              "느린 모델·시간 초과", "한글 입력·인코딩", "공식 설치법과 다르게 돌린 경우(NVIDIA 키 없이)"]
# 이번 실행에서 겪지 않은 예외 상황의 일반 안내 — 측정한 사실이 아니므로 「겪지 않음」으로 표시한다.
EXCEPTION_NOTES = {
    "네트워크·프록시": "회사망에서는 모델 엔드포인트(build.nvidia.com·OpenAI)로 나가는 HTTPS가 막히거나 프록시를 거쳐야 할 수 있습니다. "
                    "컨테이너에도 `HTTPS_PROXY`·`NO_PROXY`(localhost·postgres 등 내부 이름 포함)를 넘겨야 합니다.",
    "API 키 만료·한도·요금": "모델 키가 만료되거나 한도를 넘으면 컴파일·질문이 모델 호출 단계에서 실패합니다. 먼저 키만으로 "
                         "`curl <엔드포인트>/v1/models -H \"Authorization: Bearer $KEY\"`가 200인지 봅니다(키 값은 화면·기록에 남기지 않습니다). "
                         "이 교재의 한 번 컴파일은 gpt-6.1-sol 호출 318번(입력 약 34만 토큰)이었고, 질문 하나는 10~15번 호출이었습니다.",
    "포트 충돌": "3000~3003·5432를 다른 프로그램이 쓰고 있으면 서비스가 뜨지 않습니다. `lsof -nP -iTCP:3000 -sTCP:LISTEN`으로 확인하고, "
              "Compose의 포트 매핑이나 `POSTGRES_PORT`를 바꿉니다. 웹 주소를 바꾸면 `APP_URL`·`AUTO_ONTOLOGY_MCP_PUBLIC_URL`도 함께 바꿉니다.",
    "메모리·디스크 부족": "Compose는 PostgreSQL·pgAdmin·백엔드·적재·웹 앱 컨테이너를 함께 띄웁니다. Docker 가상 머신의 메모리가 모자라면 "
                     "PostgreSQL이 복구 모드에 들어가거나 빌드가 멈출 수 있습니다. 쓰지 않는 컨테이너를 내리고 Docker 메모리를 늘립니다.",
    "칩·OS 차이(Apple Silicon·Intel·Windows)": "이 교재는 Apple Silicon macOS에서만 실행했습니다. Windows는 WSL 2의 Docker Desktop을 권합니다. "
                                            "README의 여러 줄 명령(`\\` 줄바꿈, `(cd … && …)`)은 PowerShell에서 그대로 돌지 않습니다.",
    "한글 입력·인코딩": "한국어 질문도 받습니다(5장 Q1 한국어). 용어·설명은 영어로 생성되므로, 한국어 동의어를 용어에 더하면 찾기 쉬워집니다. "
                   "터미널에서 한국어 질문을 넘길 때는 UTF-8 로케일(`LANG=ko_KR.UTF-8`)인지 확인합니다.",
}


def item_md(x):
    ok = "확인함" if x["verified"] else "**확인 못 함**"
    note = f" — {x['verify_note']}" if x.get("verify_note") else ""
    defect = " · 제품 결함 후보" if x.get("product_defect") else ""
    return (f"- **{x['step']}** ({CH.get(x['chapter'], x['chapter'])}{defect})  \n"
            f"  증상: {x['symptom']}  \n"
            f"  원인: {x['cause']}  \n"
            f"  조치: {x['fix']}  \n"
            f"  확인: {ok}{note}\n")


def main():
    learners = [x for x in ITEMS if x["scope"] == "learners"]
    ours = [x for x in ITEMS if x["scope"] == "ours"]
    out = ["# 문제 해결", "",
           "> 이 교재를 만들며 설치·실행·연결·컴파일·질문·MCP·API·녹화 단계에서 실제로 막혔던 곳과 조치를 모았습니다. "
           "증상의 오류 문구는 화면과 기록에 나온 그대로 옮겼고, 조치를 다시 일으켜 확인했는지도 함께 적었습니다.", "",
           f"모두 {len(ITEMS)}건입니다. 학습자도 겪을 수 있는 것 {len(learners)}건, 이 교재를 찍은 환경에서만 생긴 것 {len(ours)}건, "
           f"조치를 다시 확인하지 못한 것 {sum(1 for x in ITEMS if not x['verified'])}건, 제품 결함 후보 {sum(1 for x in ITEMS if x.get('product_defect'))}건입니다. "
           "원자료는 이 교재 원고 옆의 `issues.json`입니다.", ""]
    out += ["## 단계별", ""]
    for st in STAGES:
        rows = [x for x in learners if x["stage"] == st]
        if rows:
            out += [f"### {st}", ""] + [item_md(x) for x in rows] + [""]
    out += ["## 예외 상황", "",
            "따라 하는 환경이 이 교재와 다를 때 자주 생기는 일입니다. 이번 실행에서 실제로 겪은 항목은 위 단계별 목록에도 있고, "
            "겪지 않은 항목은 일반 안내로만 적었습니다.", ""]
    for ex in EXCEPTIONS:
        rows = [x for x in ITEMS if x.get("exception") == ex]
        out += [f"### {ex}", ""]
        if rows:
            out += [f"- 이번에 겪음: **{x['step']}** — {x['symptom']} → {x['fix']}" for x in rows] + [""]
        if ex in EXCEPTION_NOTES:
            out += [("- 일반 안내(이번 실행에서는 겪지 않음): " if not rows else "- 함께 볼 것: ") + EXCEPTION_NOTES[ex], ""]
    out += ["## 이 교재를 찍은 환경", "",
            "공식 Quickstart(Docker Compose·NVIDIA NIM)를 따르면 겪지 않는 것들입니다. 이 교재의 화면을 찍은 환경이 공식 설치와 어떻게 "
            "다른지 밝히려고 따로 적었습니다.", "",
            "| 항목 | 이 교재의 실행 |", "|---|---|",
            "| 소스 | NVIDIA/auto-ontology 1.2.0 (커밋 c447003), 예제 데이터는 auto-ontology-eval ec41b2c의 `seed_wwi.py` |",
            "| 띄우는 방법 | Docker 없이 서비스마다 직접 실행 — 백엔드는 포트가 3001로 고정되어 있어 `create_app()`을 uvicorn으로 3101에 띄움, 웹 앱은 `next start -p 3100`, MCP는 `uv run auto-ontology-mcp` |",
            "| PostgreSQL | 다른 앱에 들어 있는 PostgreSQL 16 + pgvector 사본에 `pg_trgm`을 소스에서 빌드해 추가, 포트 28930 |",
            "| 모델 | NVIDIA 키 없이 OpenAI `gpt-6.1-sol`(채팅 역할 전부)·`text-embedding-3-large`(임베딩 2048차원) — 작은 중계기(:3109)가 형식을 맞춤, 재순위는 임베딩 유사도로 흉내 |",
            "| 추론 강도 | 기본값(5장의 비교 측정에서만 `low`) |",
            "| 그래프 화면 녹화 | 헤드리스 Chromium에 `--use-angle=swiftshader` |",
            "| MCP 클라이언트 | Claude Code 2.1.325를 사용자 설정과 분리한 설정 폴더(`CLAUDE_CONFIG_DIR`)로 띄우고 사내 Frentis 모델에 연결, 브라우저 열기는 녹화 브라우저가 대신함 |",
            "| PC | Apple Silicon macOS, 2026년 11월 15일 |", ""]
    out += [item_md(x) for x in ours] + [""]
    defects = [x for x in ITEMS if x.get("product_defect")]
    out += ["## 알려진 제약", "",
            "1.2.0에서 확인한 제약과 제품 결함 후보입니다. 교재에는 우회법만 적었습니다.", ""]
    out += [f"- **{x['step']}** — {x['symptom']} 우회: {x['fix']}" for x in defects]
    out += ["- **조인 하나를 끄는 기능 없음** — 화면과 공개 API에서 추론된 조인 하나를 끄거나 지우는 방법을 찾지 못했습니다(3장). "
            "표를 통째로 빼려면 연결의 Table Denylist와 Reset Semantic Layer를 씁니다.",
            "- **추론 강도 설정 없음** — 모델 호출에 `reasoning_effort` 같은 값을 넘기는 설정이 없어 게이트웨이에서 붙여야 합니다(5장).",
            "- **MCP는 OAuth만** — MCP 서버는 API 토큰을 받지 않고 사람이 로그인해 승인한 OAuth 토큰만 받습니다. 사람 없이 도는 작업은 REST API와 API 토큰을 씁니다(6·7장).", ""]
    (HERE / "src" / "troubleshooting.md").write_text("\n".join(out), encoding="utf-8")
    print(f"{len(ITEMS)}건 → src/troubleshooting.md")


if __name__ == "__main__":
    main()
