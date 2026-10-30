#!/usr/bin/env python3
"""Robo Architect 튜토리얼 사이트 빌드.

    python3 tools/ra-docs/build.py

src/*.md (장마다 하나) → docs/robo-architect/*.html. 목차·순서는 아래 CHAPTERS 가 정한다.
이미지는 docs/robo-architect/img/ 에 두고 본문에서 img/<이름>.webp 로 부른다.
videos.json 에 장의 유튜브 영상({"<slug>": {"id": …, "len": "2:51"}})이 있으면 장 요약 아래에 넣는다.

    python3 tools/ra-docs/build.py en

영문판: src-en/*.md → en/docs/robo-architect/ (template-en.html · videos-en.json · files-en/ · 영문 그림은
en/docs/robo-architect/img/). 장 순서는 같고, 파트 이름만 EN_PARTS 로 바꾼다.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).resolve().parent
LANG = "en" if sys.argv[1:] == ["en"] else "ko"
EN = LANG == "en"
SRC = HERE / ("src-en" if EN else "src")
OUT = HERE.parents[1] / ("en/docs" if EN else "docs") / "robo-architect"
VIDEOS = HERE / ("videos-en.json" if EN else "videos.json")
SITE = f"https://www.uengine.org/{'en/' if EN else ''}docs/robo-architect/"
EN_PARTS = {"시작하기": "Getting started", "프로포절 라이프사이클": "The proposal lifecycle",
            "설계와 변경": "Design and change", "레거시와 데이터": "Legacy and data",
            "마무리": "Final project", "부록": "Appendix"}
# 「준비 중」 장의 영문 제목 (CHAPTERS 의 세 번째 값이 한국어라)
EN_SOON = {"ingest": "Start from a requirements document", "legacy": "Analyze legacy code", "constitution": "Set the project constitution", "plan": "Plan — tactical design and architecture", "implement": "Implement in a sandbox", "verify": "Validate and accept", "design": "Tour the design", "change": "A second proposal — change impact", "skills": "Change the engine with skill files", "fabric": "Connect data sources — the data fabric", "project": "Final project", "cheatsheet": "Cheat sheet", "faq": "FAQ"}

# (파일, 파트[, "준비 중" 제목]) — 제목은 각 md 의 첫 줄(# …)에서 읽는다. 장 번호 = 이 목록의 순서(index = 0장).
# 세 번째 값은 「준비 중」일 때 사이드바에 보일 제목 — 그 언어의 md(src/·src-en/)가 생기면 그 장을 만든다.
# 장을 나중에 써도 번호가 바뀌지 않게(영상 제목의 「NN장」과 맞게) 미리 자리를 둔다.
CHAPTERS = [
    ("index", "시작하기"),
    ("install", "시작하기"),
    ("tour", "시작하기"),
    ("proposal", "프로포절 라이프사이클"),
    ("constitution", "프로포절 라이프사이클", "프로젝트 헌장 정하기"),
    ("plan", "프로포절 라이프사이클", "Plan — 전술 설계와 아키텍처"),
    ("implement", "프로포절 라이프사이클", "샌드박스에서 구현하기"),
    ("verify", "프로포절 라이프사이클", "검증하고 수락하기"),
    ("design", "설계와 변경", "설계 둘러보기 — 요구사항 · 프로세스 · 설계 · 데이터"),
    ("change", "설계와 변경", "두 번째 프로포절 — 변경 영향도"),
    ("skills", "설계와 변경", "스킬 파일로 엔진 바꾸기"),
    ("fabric", "레거시와 데이터", "데이터 소스 연결 — 데이터 패브릭"),
    ("ingest", "레거시와 데이터", "요구사항 문서로 설계 시작하기"),
    ("legacy", "레거시와 데이터", "레거시 코드 분석"),
    ("project", "마무리", "종합 과제"),
    ("cheatsheet", "부록", "치트시트"),
    ("faq", "부록", "자주 묻는 질문"),
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
        return (f'<figure><a href="{src}" target="_blank" rel="noopener" title="{"View larger" if EN else "크게 보기"}">'
                f'<img{attrs} loading="lazy" decoding="async"></a>'
                + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
    return re.sub(r"<p><img([^>]*)></p>", fig, body)


def video(body, v, title):
    # 장 요약(첫 인용문) 바로 아래, 없으면 맨 위
    frame = (f'<div class="video"><iframe src="https://www.youtube.com/embed/{v["id"]}" '
             f'title="{html.escape(title)} — {"video" if EN else "영상"} {v.get("len", "")}" loading="lazy" allow="accelerometer; clipboard-write; '
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
    tpl = (HERE / ("template-en.html" if EN else "template.html")).read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    videos = json.loads(VIDEOS.read_text(encoding="utf-8")) if VIDEOS.exists() else {}
    pages = []
    for slug, part, *soon in CHAPTERS:
        # 그 언어의 md 가 아직 없으면 「준비 중」 — 한국어판이 먼저 나가고 영문판은 뒤에 올 수 있다
        if not (SRC / f"{slug}.md").exists():
            title = EN_SOON.get(slug, slug) if EN else (soon[0] if soon else slug)
            pages.append(dict(slug=slug, part=EN_PARTS.get(part, part) if EN else part, title=title, soon=True))
            continue
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
        pages.append(dict(slug=slug, part=EN_PARTS.get(part, part) if EN else part, title=title, summary=summary, body=body, toc=toc))

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
            if p.get("soon"):
                out.append(f'<li><span class="soon">{num}{html.escape(p["title"])}<em>{"Coming soon" if EN else "준비 중"}</em></span></li>')
                continue
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
    ready = [p for p in pages if not p.get("soon")]
    for p in ready:
        i = pages.index(p)
        k = ready.index(p)
        prev = ready[k - 1] if k else None
        nxt = ready[k + 1] if k + 1 < len(ready) else None
        pager = '<nav class="pager">'
        pager += (f'<a class="prev" href="{page_name(prev["slug"])}"><span>{"Previous" if EN else "이전"}</span>{html.escape(prev["title"])}</a>' if prev else "<span></span>")
        pager += (f'<a class="next" href="{page_name(nxt["slug"])}"><span>{"Next" if EN else "다음"}</span>{html.escape(nxt["title"])}</a>' if nxt else "<span></span>")
        pager += "</nav>"
        chap = str(i) if i else ""
        out = (tpl.replace("{{title}}", html.escape(p["title"]))
               .replace("{{desc}}", html.escape(p["summary"] or ("Robo Architect Tutorial" if EN else "Robo Architect 튜토리얼")))
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
    files = HERE / ("files-en" if EN else "files")
    if files.is_dir():  # 실습에 쓰는 내려받기 파일
        shutil.copytree(files, OUT / "files", dirs_exist_ok=True)
    for f in ("docs.css", "docs.js"):
        (OUT / "assets" / f).write_text((HERE / f).read_text(encoding="utf-8"), encoding="utf-8")
    print(f"{len(ready)} pages ({len(pages) - len(ready)} coming soon) → {OUT}")


if __name__ == "__main__":
    main()
