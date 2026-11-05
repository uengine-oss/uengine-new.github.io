#!/usr/bin/env python3
"""산업별 솔루션·교육 튜토리얼 빌드 (uEngine MES · uEngine WMS · AI 기획·설계 도구 실습).

    python3 tools/industry-docs/build.py mes
    python3 tools/industry-docs/build.py wms
    python3 tools/industry-docs/build.py ai-planning
    python3 tools/industry-docs/build.py erp
    python3 tools/industry-docs/build.py aidlc-handson

<제품>/src/*.md (장마다 하나) → docs/<제품>/*.html. 목차·순서는 아래 PRODUCTS 가 정한다.
이미지는 docs/<제품>/img/ 에 두고 본문에서 img/<이름>.webp 로 부른다.
<제품>/videos.json 에 장의 유튜브 영상({"<slug>": {"id": …, "len": "2:51"}})이 있으면 장 요약 아래에 넣는다.
영문판은 아직 없다. 영문 메뉴는 이 한국어 튜토리얼로 연결된다.
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).resolve().parent
PRODUCTS = {
    "erp": dict(name="uEngine ERP", page="erp.html", og="whatif-policy.webp", search="튜토리얼 검색 (예: 재고 켜기, 되돌리기, what-if)",
                foot="이 튜토리얼의 화면과 수치는 실제 앱을 가상 회사 데이터로 실행해 얻었습니다. 실제 회사의 성능이 아닙니다.",
                chapters=[("index", "시작하기"), ("modules", "모듈 더하기"), ("buy-books", "모듈 더하기"), ("history", "이력과 되돌리기"), ("whatif", "예측과 what-if"), ("connect", "연동"), ("voucher-tax", "세금과 장부"), ("books-assets", "세금과 장부"), ("people", "인사와 급여"), ("payroll", "인사와 급여"), ("mrp", "제조"), ("expense", "경비"), ("crm-project", "영업과 프로젝트"), ("lite", "Process GPT Lite")]),
    "mes": dict(name="uEngine MES", page="mes.html", og="anomaly-monitor.webp", search="튜토리얼 검색 (예: 설비 정지, 시점 조회, 시맨틱 레이어)",
                foot="이 튜토리얼의 화면과 결과는 시연용 참조 구현을 합성 데이터로 실제 실행해 얻었습니다.",
                chapters=[("index", "시작하기"), ("anomaly", "현장 대응"), ("events", "이력과 추적"), ("semantic", "AI 연결"), ("agent", "AI 연결")]),
    "wms": dict(name="uEngine WMS", page="wms.html", og="inbound-po.webp", search="튜토리얼 검색 (예: RFQ, 입고 검수, WCS 설비)",
                foot="이 튜토리얼의 화면과 결과는 공개 저장소의 샘플 앱(커밋 fc82ea2)을 실제 실행해 얻었습니다.",
                chapters=[("index", "시작하기"), ("inbound", "입고와 재고"), ("automation", "창고 자동화"), ("ops", "창고 자동화"), ("agent", "AI 연결")]),
    "bpm": dict(name="uEngine6 BPM", page="uengine6bpm.html", og="erp-process.webp", search="튜토리얼 검색 (예: 선점, 게이트웨이, 이벤트로 끝내기)",
                foot="이 튜토리얼의 화면과 결과는 uEngine6 (bmt/sds-process-test 브랜치)을 로컬에서 실제로 실행해 얻었습니다. 회사와 사람은 가상입니다.",
                chapters=[("index", "시작하기"), ("install-local", "시작하기"), ("quickstart", "시작하기"), ("quickstart-api", "시작하기"), ("modeler-tour", "모델링"), ("process-data", "모델링"), ("lanes-and-roles", "모델링"), ("arguments-and-mapping", "모델링"), ("forms", "사람 작업"), ("tasklist", "사람 작업"), ("return-and-skip", "사람 작업"), ("external-task-screen", "사람 작업"), ("exclusive-gateway", "흐름 제어"), ("parallel-inclusive-gateway", "흐름 제어"), ("script-task", "흐름 제어"), ("business-rule-dmn", "흐름 제어"), ("call-activity", "흐름 제어"), ("multi-instance", "흐름 제어"), ("message-start", "이벤트"), ("event-completion", "이벤트"), ("error-and-compensation", "이벤트"), ("rest-service-task", "시스템 연동"), ("sql-task", "시스템 연동"), ("event-integration-kafka", "시스템 연동"), ("instance-monitoring", "운영"), ("fix-variables", "운영"), ("back-to-here", "운영"), ("test-before-deploy", "운영"), ("versions-and-deploy", "운영"), ("analytics-kpi", "운영"), ("rest-api", "API·보안"), ("security-keycloak", "API·보안"), ("industry-banking-sor", "산업 예제"), ("industry-erp-purchase", "산업 예제"), ("bpmn-coverage", "참고"), ("extend-engine", "참고")]),
    "aidlc-handson": dict(name="Claude Code × AI-DLC 핸즈온", page="axschool.html", pagelabel="AX School", og="run-done.webp", search="검색 (예: aidlc config, 후속 질문, 402, 감사 기록)",
                foot="이 튜토리얼의 화면과 결과는 2026년 11월 5일 Claude Code 2.1.318(Sonnet 5.5)과 AI-DLC 2.11.2로 실제로 실행해 얻었습니다. 모델이 쓰는 문장은 실행할 때마다 달라질 수 있습니다.",
                chapters=[("index", "시작하기"), ("setup", "레벨 1 · poc"), ("requirements", "레벨 1 · poc"), ("construction", "레벨 1 · poc"), ("run", "레벨 1 · poc"), ("concepts", "레벨 2 · classic"), ("level2", "레벨 2 · classic"), ("level2-build", "레벨 2 · classic"), ("artifacts", "레벨 2 · classic")]),
    "ai-planning": dict(name="AI 기획·설계 도구 실습", page="axschool.html", pagelabel="AX School", og="board1b.webp", search="교재 검색 (예: 역질문, 겹침 금지, OpenUI)",
                foot="이 교재의 화면과 결과는 2026년 11월 4일 실제로 실행해 얻었습니다. 실습 주제는 가상의 회사입니다. ChatPRD, Eraser AI, Uizard, bolt.diy 실행 화면은 확인하지 못했습니다.",
                chapters=[("index", "시작하기"), ("interview", "1부"), ("model", "2부"), ("screen", "3부"), ("wrap", "4부")]),
}
KEY = sys.argv[1] if sys.argv[1:] and sys.argv[1] in PRODUCTS else sys.exit(__doc__)
P = PRODUCTS[KEY]
FIRST = 1 if KEY == "erp" else 0
SRC = HERE / KEY / "src"
OUT = HERE.parents[1] / "docs" / KEY
VIDEOS = HERE / KEY / "videos.json"
SITE = f"https://www.uengine.org/docs/{KEY}/"


def page_name(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def slug_ko(value, separator):
    value = re.sub(r"[^\w\s가-힣-]", "", value).strip().lower()
    return re.sub(r"[\s]+", separator, value)


def render(md_text):
    md = markdown.Markdown(extensions=[
        "fenced_code", "tables", "attr_list", "admonition", "def_list", "md_in_html",
        TocExtension(permalink="#", permalink_class="anchor", toc_depth="2-3", slugify=slug_ko),
        "codehilite",
    ], extension_configs={"codehilite": {"guess_lang": False, "css_class": "hl"}})
    body = md.convert(md_text)
    return body, md.toc_tokens


def figures(body):
    # 문단 하나에 이미지만 있으면 figure 로 — alt 가 캡션이 된다.
    def fig(m):
        attrs = m.group(1)
        alt = re.search(r'alt="([^"]*)"', attrs)
        src = re.search(r'src="([^"]*)"', attrs).group(1)
        cap = alt.group(1) if alt else ""
        return (f'<figure><a href="{src}" target="_blank" rel="noopener" title="크게 보기">'
                f'<img{attrs} loading="lazy" decoding="async"></a>'
                + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
    # 목록 항목 안의 그림은 markdown 이 <p> 없이 내보낸다. 둘 다 figure 로.
    return re.sub(r"(?:<p>)?<img([^>]*?)\s*/?>(?:</p>)?", fig, body)


def video(body, v, title):
    # 장 요약(첫 인용문) 바로 아래, 없으면 맨 위
    frame = (f'<div class="video"><iframe src="https://www.youtube.com/embed/{v["id"]}" '
             f'title="{html.escape(title)} — 영상 {v.get("len", "")}" loading="lazy" allow="accelerometer; clipboard-write; '
             f'encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" '
             f'allowfullscreen></iframe></div>')
    i = body.find("</blockquote>")
    return body[:i + 13] + "\n" + frame + body[i + 13:] if i >= 0 else frame + body


def text_of(body):
    t = re.sub(r"<pre.*?</pre>", " ", body, flags=re.S)
    t = re.sub(r'<a class="anchor"[^>]*>.*?</a>', "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def main():
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    videos = json.loads(VIDEOS.read_text(encoding="utf-8")) if VIDEOS.exists() else {}
    pages = []
    for slug, part in P["chapters"]:
        if not (SRC / f"{slug}.md").exists():
            sys.exit(f"원고가 없다: {SRC / (slug + '.md')}")
        raw = (SRC / f"{slug}.md").read_text(encoding="utf-8")
        first, rest = raw.split("\n", 1)
        assert first.startswith("# "), slug
        title = first[2:].strip()
        m = re.match(r"\s*>\s*(.+?)\n\n", rest)  # 첫 인용문 = 장 요약(설명 메타)
        summary = m.group(1).strip() if m else ""
        body, toc = render(rest)
        body = figures(body)
        if slug in videos:
            body = video(body, videos[slug], title)
        pages.append(dict(slug=slug, part=part, title=title, summary=summary, body=body, toc=toc))

    # 사이드바 — 파트별, 장 번호는 index 를 0 으로.
    def sidebar(cur):
        out, last = [], None
        for i, p in enumerate(pages):
            if p["part"] != last:
                if last is not None:
                    out.append("</ul>")
                out.append(f'<div class="nav-part">{html.escape(p["part"])}</div><ul>')
                last = p["part"]
            on = ' class="on" aria-current="page"' if p["slug"] == cur else ""
            num = f'<span class="n">{i + FIRST:02d}</span>' if i + FIRST else '<span class="n">·</span>'
            out.append(f'<li><a href="{page_name(p["slug"])}"{on}>{num}{html.escape(p["title"])}</a></li>')
        out.append("</ul>")
        return "\n".join(out)

    def toc_html(tokens):
        items = []
        for t in tokens:
            items.append(f'<li><a href="#{t["id"]}">{html.escape(html.unescape(t["name"]))}</a>')
            if t["children"]:
                items.append("<ul>" + "".join(
                    f'<li><a href="#{c["id"]}">{html.escape(html.unescape(c["name"]))}</a></li>' for c in t["children"]) + "</ul>")
            items.append("</li>")
        return "<ul>" + "".join(items) + "</ul>" if items else ""

    index = []
    for i, p in enumerate(pages):
        prev = pages[i - 1] if i else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        pager = '<nav class="pager">'
        pager += (f'<a class="prev" href="{page_name(prev["slug"])}"><span>이전</span>{html.escape(prev["title"])}</a>' if prev else "<span></span>")
        pager += (f'<a class="next" href="{page_name(nxt["slug"])}"><span>다음</span>{html.escape(nxt["title"])}</a>' if nxt else "<span></span>")
        pager += "</nav>"
        chap = str(i + FIRST) if i + FIRST else ""
        out = (tpl.replace("{{title}}", html.escape(p["title"]))
               .replace("{{product}}", P["name"])
               .replace("{{key}}", KEY)
               .replace("{{page}}", P["page"])
               .replace("{{pagelabel}}", P.get("pagelabel", "제품 소개"))
               .replace("{{og}}", P["og"])
               .replace("{{search}}", P["search"])
               .replace("{{footnote}}", P["foot"])
               .replace("{{desc}}", html.escape(p["summary"] or f'{P["name"]} 튜토리얼'))
               .replace("{{canonical}}", SITE + ("" if p["slug"] == "index" else page_name(p["slug"])))
               .replace("{{part}}", html.escape(p["part"]))
               .replace("{{chap}}", chap)
               .replace("{{sidebar}}", sidebar(p["slug"]))
               .replace("{{toc}}", toc_html(p["toc"]))
               .replace("{{body}}", p["body"])
               .replace("{{pager}}", pager))
        (OUT / page_name(p["slug"])).write_text(out, encoding="utf-8")
        index.append({"u": page_name(p["slug"]), "t": p["title"], "p": p["part"],
                      "h": [html.unescape(t["name"]) for t in p["toc"]], "x": text_of(p["body"])[:4000]})

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "search.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    light = HtmlFormatter(style="friendly").get_style_defs(".hl")
    dark = HtmlFormatter(style="monokai").get_style_defs("[data-theme=dark] .hl")
    (OUT / "assets" / "code.css").write_text(light + "\n" + dark, encoding="utf-8")
    for f in ("docs.css", "docs.js"):
        (OUT / "assets" / f).write_text((HERE / f).read_text(encoding="utf-8"), encoding="utf-8")
    print(f"{len(pages)} pages → {OUT}")


if __name__ == "__main__":
    main()
