#!/usr/bin/env python3
"""Process GPT Lite 튜토리얼 사이트 빌드.

    python3 tools/pgl-docs/build.py

src/*.md (장마다 하나) → docs/process-gpt-lite/*.html. 목차·순서는 아래 CHAPTERS 가 정한다.
이미지는 docs/process-gpt-lite/img/ 에 두고 본문에서 img/<이름>.webp 로 부른다.
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
OUT = HERE.parents[1] / "docs" / "process-gpt-lite"
SITE = "https://www.uengine.org/docs/process-gpt-lite/"

# (파일, 파트) — 제목은 각 md 의 첫 줄(# …)에서 읽는다.
CHAPTERS = [
    ("index", "시작하기"),
    ("install", "시작하기"),
    ("tour", "시작하기"),
    ("first-chat", "나와 AI 비서"),
    ("contexts", "나와 AI 비서"),
    ("mail", "나와 AI 비서"),
    ("browser", "나와 AI 비서"),
    ("office", "문서와 도구"),
    ("craft", "문서와 도구"),
    ("email-to-quote", "문서와 도구"),
    ("skills", "반복 줄이기"),
    ("missions", "반복 줄이기"),
    ("panel-apps", "반복 줄이기"),
    ("folders", "팀으로 일하기"),
    ("sharing", "팀으로 일하기"),
    ("messenger", "팀으로 일하기"),
    ("meetings", "팀으로 일하기"),
    ("process-create", "프로세스로 일하기"),
    ("process-run", "프로세스로 일하기"),
    ("mining", "프로세스로 일하기"),
    ("bottleneck", "프로세스 개선"),
    ("value-stream", "프로세스 개선"),
    ("critical-path", "프로세스 개선"),
    ("workroom", "확장과 운영"),
    ("architecture", "확장과 운영"),
    ("admin", "확장과 운영"),
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


def text_of(body):
    t = re.sub(r"<pre.*?</pre>", " ", body, flags=re.S)
    t = re.sub(r'<a class="anchor"[^>]*>.*?</a>', "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def main():
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    pages = []
    for slug, part in CHAPTERS:
        raw = (SRC / f"{slug}.md").read_text(encoding="utf-8")
        first, rest = raw.split("\n", 1)
        assert first.startswith("# "), slug
        title = first[2:].strip()
        m = re.match(r"\s*>\s*(.+?)\n\n", rest)  # 첫 인용문 = 장 요약(설명 메타)
        summary = m.group(1).strip() if m else ""
        body, toc = render(rest)
        pages.append(dict(slug=slug, part=part, title=title, summary=summary, body=figures(body), toc=toc))

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
               .replace("{{desc}}", html.escape(p["summary"] or "Process GPT Lite 튜토리얼"))
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
