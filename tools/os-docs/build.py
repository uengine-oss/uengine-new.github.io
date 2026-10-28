#!/usr/bin/env python3
"""Ontological Studio 튜토리얼 사이트 빌드.

    python3 tools/os-docs/build.py

src/*.md (장마다 하나) → docs/ontological-studio/*.html. 목차·순서는 아래 CHAPTERS 가 정한다.
이미지는 docs/ontological-studio/img/ 에 두고 본문에서 img/<이름>.webp 로 부른다.
videos.json 에 장의 유튜브 영상({"<slug>": {"id": …, "len": "2:51"}})이 있으면 장 요약 아래에 넣는다.
"""
import html
import json
import re
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE.parents[1] / "docs" / "ontological-studio"
VIDEOS = HERE / "videos.json"
SITE = "https://www.uengine.org/docs/ontological-studio/"

# (파일, 파트) — 제목은 각 md 의 첫 줄(# …)에서 읽는다.
CHAPTERS = [
    ("index", "시작하기"),
    ("install", "시작하기"),
    ("tour", "시작하기"),
    ("ontology-basics", "온톨로지 개념"),
    ("architecture", "온톨로지 개념"),
    ("datasource", "데이터 연결"),
    ("virtual-graph", "데이터 연결"),
    ("cypher-basics", "Cypher 익히기"),
    ("cypher-relations", "Cypher 익히기"),
    ("cypher-advanced", "Cypher 익히기"),
    ("time-travel", "Cypher 익히기"),
    ("golden", "온톨로지 구축"),
    ("build", "온톨로지 구축"),
    ("ask", "온톨로지 구축"),
    ("systems", "액션"),
    ("actions-build", "액션"),
    ("actions-run", "액션"),
    ("dashboard", "애플리케이션"),
    ("code-app", "애플리케이션"),
    ("sdk", "애플리케이션"),
    ("app-actions", "애플리케이션"),
    ("project", "마무리"),
    ("cheatsheet", "부록"),
    ("faq", "부록"),
]


def page_name(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def render(md_text):
    md = markdown.Markdown(extensions=[
        "fenced_code", "tables", "attr_list", "admonition", "def_list", "md_in_html",
        TocExtension(permalink="#", permalink_class="anchor", toc_depth="2-3", slugify=slug_ko),
        "codehilite",
    ], extension_configs={"codehilite": {"guess_lang": False, "css_class": "hl"}})
    body = md.convert(md_text)
    return body, md.toc_tokens


def slug_ko(value, separator):
    value = re.sub(r"[^\w\s가-힣-]", "", value).strip().lower()
    return re.sub(r"[\s]+", separator, value)


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
    return re.sub(r"<p><img([^>]*)></p>", fig, body)


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
    videos = json.loads(VIDEOS.read_text(encoding="utf-8")) if VIDEOS.exists() else {}
    pages = []
    for slug, part in CHAPTERS:
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
            num = f'<span class="n">{i:02d}</span>' if i else '<span class="n">·</span>'
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
        chap = str(i) if i else ""
        out = (tpl.replace("{{title}}", html.escape(p["title"]))
               .replace("{{desc}}", html.escape(p["summary"] or "Ontological Studio 튜토리얼"))
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

    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "search.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    light = HtmlFormatter(style="friendly").get_style_defs(".hl")
    dark = HtmlFormatter(style="monokai").get_style_defs("[data-theme=dark] .hl")
    (OUT / "assets" / "code.css").write_text(light + "\n" + dark, encoding="utf-8")
    for f in ("docs.css", "docs.js"):
        (OUT / "assets" / f).write_text((HERE / f).read_text(encoding="utf-8"), encoding="utf-8")
    print(f"{len(pages)} pages → {OUT}")


if __name__ == "__main__":
    main()
