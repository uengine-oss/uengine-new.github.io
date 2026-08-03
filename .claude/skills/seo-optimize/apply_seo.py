#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
uEngine 홈페이지 SEO 메타 일괄 적용기.

하는 일
  1. 모든 HTML 페이지의 <head> 에 SEO 블록을 멱등하게(idempotent) 주입
     - <title>, meta description, canonical, robots
     - Open Graph (og:*), Twitter Card
     - JSON-LD 구조화 데이터 (Organization / BlogPosting / SoftwareApplication / …)
     - <meta charset> 을 head 최상단으로 승격
     - <html lang="ko"> 보정
  2. sitemap.xml / robots.txt 생성
  3. 문제 리포트 (중복 title·description, 길이 초과, 레지스트리 누락, h1 이상 등)

메타데이터 출처 (우선순위 순)
  1. .claude/skills/seo-optimize/seo-meta.json 의 pages[경로]   ← 큐레이션된 값
  2. contents/bloglist.html 의 카드          ← 블로그 글은 목록에서 제목·날짜·요약 자동 수집
  3. contents/newsroom.html 의 카드          ← 뉴스룸 글도 동일
  4. 페이지의 <h1> + 첫 문단                  ← 최후 폴백 (경고 표시)

사용법
  python3 .claude/skills/seo-optimize/apply_seo.py            # 적용
  python3 .claude/skills/seo-optimize/apply_seo.py --check    # 검사만 (파일 미변경, 문제 있으면 exit 1)
  python3 .claude/skills/seo-optimize/apply_seo.py --only contents/blog/foo.html
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import html as html_mod
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
META_PATH = os.path.join(HERE, "seo-meta.json")

BEGIN = "<!-- SEO:BEGIN — 자동 생성됨. 직접 수정하지 마세요. " \
        ".claude/skills/seo-optimize/seo-meta.json 을 고치고 apply_seo.py 를 다시 실행하세요. -->"
END = "<!-- SEO:END -->"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june",
     "july", "august", "september", "october", "november", "december"])}

warnings: list[str] = []
notes: list[str] = []


def warn(msg): warnings.append(msg)
def note(msg): notes.append(msg)


# ──────────────────────────────────────────────────────────── helpers

def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def esc(s: str) -> str:
    """HTML 속성값 이스케이프."""
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def head_span(src: str):
    m = re.search(r"<head\b[^>]*>", src, re.I)
    e = re.search(r"</head\s*>", src, re.I)
    if not m or not e:
        return None
    return m.end(), e.start()


def parse_date(text: str) -> str | None:
    """'July 23, 2026' / '2026-07-23' / '2026.07.23' → '2026-07-23'."""
    if not text:
        return None
    text = text.strip()
    m = re.match(r"^(\d{4})[-.\/](\d{1,2})[-.\/](\d{1,2})", text)
    if m:
        return "%04d-%02d-%02d" % tuple(int(g) for g in m.groups())
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", text)
    if m and m.group(1).lower() in MONTHS:
        return "%04d-%02d-%02d" % (int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    return None


_git_cache: dict[str, str | None] = {}


def git_last_modified(relpath: str) -> str | None:
    if relpath in _git_cache:
        return _git_cache[relpath]
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", relpath],
            cwd=ROOT, capture_output=True, text=True, timeout=15)
        val = out.stdout.strip() or None
    except Exception:
        val = None
    _git_cache[relpath] = val
    return val


def truncate(text: str, limit: int) -> str:
    """단어 경계에서 자르고 말줄임표."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    for sep in (". ", "다. ", " "):
        i = cut.rfind(sep)
        if i > limit * 0.6:
            cut = cut[:i + (len(sep) if sep != " " else 0)]
            break
    return cut.rstrip(" ,·—-") + "…"


# ──────────────────────────────────────────────────── 목록 페이지에서 카드 수집

def harvest_cards(list_page: str, link_prefix: str) -> dict[str, dict]:
    """블로그/뉴스룸 목록 페이지의 카드에서 제목·날짜·요약을 수집.

    두 가지 카드 마크업을 지원합니다.
      · blog-item  … bloglist.html (제목 h2 + blog-item-data 날짜 + p.mb-0 요약)
      · post-prev  … newsroom.html (제목 h4.post-prev-title + post-prev-text + post-prev-info 날짜)
    """
    path = os.path.join(ROOT, list_page)
    if not os.path.exists(path):
        return {}
    src = open(path, encoding="utf-8").read()
    base_dir = os.path.dirname(list_page)
    found: dict[str, dict] = {}

    def record(href, title, date_text, desc_html):
        rel = os.path.normpath(os.path.join(base_dir, href)).replace(os.sep, "/")
        if rel in found:
            return
        found[rel] = {
            "title": strip_tags(title),
            "datePublished": parse_date(date_text or ""),
            "description": strip_tags(desc_html or ""),
        }

    # blog-item 패턴
    for block in re.findall(r'<div class="blog-item[^"]*"[^>]*>(.*?)<!-- End Post -->', src, re.S):
        a = re.search(r'<a href="(' + re.escape(link_prefix) + r'[^"]+\.html)"[^>]*>(.*?)</a>', block, re.S)
        if not a:
            continue
        d = re.search(r'blog-item-data[^>]*>(?:.*?</i>)?\s*([^<]+)', block, re.S)
        p = re.search(r'<p class="mb-0"[^>]*>(.*?)</p>', block, re.S)
        record(a.group(1), a.group(2), d.group(1) if d else "", p.group(1) if p else "")

    # post-prev 패턴
    for m in re.finditer(
            r'<h\d[^>]*class="post-prev-title"[^>]*>\s*<a href="('
            + re.escape(link_prefix) + r'[^"]+\.html)"[^>]*>(.*?)</a>', src, re.S):
        tail = src[m.end():m.end() + 4000]
        t = re.search(r'<div class="post-prev-text"[^>]*>(.*?)</div>', tail, re.S)
        d = re.search(r'post-prev-info.*?float-end"[^>]*>([^<]+)<', tail, re.S)
        record(m.group(1), m.group(2), d.group(1) if d else "", t.group(1) if t else "")

    return found


# ──────────────────────────────────────────────────── 페이지 자체에서 유추

def derive_from_page(src: str) -> dict:
    out = {}
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", src, re.S)
    for h in h1s:
        t = strip_tags(h)
        if t and "개인정보" not in t:
            out["title"] = t
            break
    for p in re.findall(r"<p\b[^>]*>(.*?)</p>", src, re.S):
        t = strip_tags(p)
        if len(t) >= 60:
            out["description"] = t
            break
    return out


def social_safe(root_path: str) -> str:
    """og:image 는 WebP 를 피하고 같은 이름의 PNG/JPEG 원본을 쓴다.

    카카오톡·일부 링크 프리뷰 크롤러가 아직 WebP 썸네일을 렌더링하지 못한다.
    성능을 위해 페이지 <img> 는 .webp 를 참조하더라도, 공유 카드용 이미지는
    나란히 남아 있는 원본 래스터 파일을 가리키게 한다.
    """
    if not root_path.lower().endswith(".webp"):
        return root_path
    stem = os.path.splitext(root_path)[0]
    for ext in (".png", ".jpg", ".jpeg"):
        if os.path.exists(os.path.join(ROOT, (stem + ext).lstrip("/"))):
            return stem + ext
    return root_path


IMG_REF = re.compile(r'["\(]((?:\.\./)*images/[^"\')\s]+\.(?:jpg|jpeg|png|webp))', re.I)

# og:image 로 절대 쓰면 안 되는 것 — 파비콘/로고/프로필은 공유 카드에서 흉하다.
NEVER_OG = ("logo", "favicon", "icon", "author")
# 콘텐츠 이미지가 하나도 없을 때만 최후 수단으로 허용하는 것 (실제 사진이라 카드로는 쓸 만함).
LAST_RESORT_OG = ("section-bg", "page-title-bg", "decoration")

# 지연 로딩이 아닌 본문 이미지(=LCP 후보)가 이 크기를 넘으면 경고한다.
LCP_IMAGE_KB_LIMIT = 200


def first_local_image(src: str, page: str) -> str | None:
    """페이지가 참조하는 첫 로컬 이미지를 사이트 루트 기준 경로로."""
    _ = page
    last_resort = None
    for m in IMG_REF.finditer(src):
        p = "/" + re.sub(r"^(\.\./)+", "", m.group(1))
        low = p.lower()
        if any(k in low for k in NEVER_OG):
            continue
        if any(k in low for k in LAST_RESORT_OG):
            if last_resort is None:
                last_resort = p
            continue
        return social_safe(p)
    # 콘텐츠 이미지가 없으면 최후 수단, 그것도 없으면 호출부가 기본 이미지로 처리한다.
    return social_safe(last_resort) if last_resort else None


# ──────────────────────────────────────────────────────────── 블록 생성

def build_block(page: str, meta: dict, site: dict) -> str:
    base = site["baseUrl"].rstrip("/")
    url = base + "/" + ("" if page == "index.html" else page)
    title = meta["title"]
    desc = meta["description"]
    image = base + (meta.get("image") or site["defaultImage"])
    otype = meta.get("type", "website")

    L = [BEGIN]
    L.append(f"<title>{esc(title)}</title>")
    L.append(f'<meta name="description" content="{esc(desc)}">')

    if meta.get("noindex"):
        L.append('<meta name="robots" content="noindex, follow">')
    else:
        L.append('<meta name="robots" content="index, follow, max-image-preview:large, '
                 'max-snippet:-1, max-video-preview:-1">')

    canonical = url
    if meta.get("canonicalTo"):
        canonical = base + "/" + meta["canonicalTo"]
    L.append(f'<link rel="canonical" href="{esc(canonical)}">')

    L.append(f'<meta property="og:type" content="{otype}">')
    L.append(f'<meta property="og:site_name" content="{esc(site["brand"])}">')
    L.append(f'<meta property="og:locale" content="{site["locale"]}">')
    L.append(f'<meta property="og:title" content="{esc(title)}">')
    L.append(f'<meta property="og:description" content="{esc(desc)}">')
    L.append(f'<meta property="og:url" content="{esc(canonical)}">')
    L.append(f'<meta property="og:image" content="{esc(image)}">')
    L.append(f'<meta property="og:image:alt" content="{esc(title)}">')
    if otype == "article":
        if meta.get("datePublished"):
            L.append(f'<meta property="article:published_time" content="{meta["datePublished"]}">')
        if meta.get("dateModified"):
            L.append(f'<meta property="article:modified_time" content="{meta["dateModified"]}">')
        L.append(f'<meta property="article:publisher" content="{esc(base + "/")}">')

    L.append('<meta name="twitter:card" content="summary_large_image">')
    if site.get("twitterHandle"):
        L.append(f'<meta name="twitter:site" content="{esc(site["twitterHandle"])}">')
    L.append(f'<meta name="twitter:title" content="{esc(title)}">')
    L.append(f'<meta name="twitter:description" content="{esc(desc)}">')
    L.append(f'<meta name="twitter:image" content="{esc(image)}">')

    a = site.get("analytics", {})
    if a.get("googleSiteVerification"):
        L.append(f'<meta name="google-site-verification" content="{esc(a["googleSiteVerification"])}">')
    if a.get("naverSiteVerification"):
        L.append(f'<meta name="naver-site-verification" content="{esc(a["naverSiteVerification"])}">')

    for obj in build_jsonld(page, meta, site, canonical, image):
        L.append('<script type="application/ld+json">'
                 + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
                 + "</script>")

    if a.get("ga4MeasurementId"):
        gid = a["ga4MeasurementId"]
        L.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>')
        L.append("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                 f"gtag('js',new Date());gtag('config','{gid}');</script>")

    L.append(END)
    return "\n        ".join(L)


def build_jsonld(page: str, meta: dict, site: dict, canonical: str, image: str) -> list[dict]:
    base = site["baseUrl"].rstrip("/")
    publisher = {
        "@type": "Organization",
        "name": site["orgName"],
        "url": base + "/",
        "logo": {"@type": "ImageObject", "url": base + site["logo"]},
    }
    out: list[dict] = []
    kind = meta.get("schema", "WebPage")
    # 구조화 데이터의 name/headline 은 브랜드 접미사를 뗀 순수 제목을 쓴다.
    name = (meta.get("breadcrumb") or [None])[-1] \
        or re.split(r"\s+[—|]\s+", meta.get("cleanTitle", meta["title"]))[0]
    headline = meta.get("cleanTitle", meta["title"])

    if kind == "Organization":
        out.append({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": site["orgName"],
            "alternateName": [site["orgNameEn"], site["brand"]],
            "url": base + "/",
            "logo": base + site["logo"],
            "description": meta["description"],
            "foundingDate": "2003",
            "sameAs": site.get("sameAs", []),
        })
        out.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": site["brand"],
            "url": base + "/",
            "inLanguage": site["lang"],
            "publisher": publisher,
        })
        return out

    if kind in ("BlogPosting", "NewsArticle", "Article"):
        obj = {
            "@context": "https://schema.org",
            "@type": kind,
            "headline": truncate(headline, 110),
            "description": meta["description"],
            "image": [image],
            "url": canonical,
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "inLanguage": site["lang"],
            "author": {"@type": "Organization", "name": site["orgName"], "url": base + "/"},
            "publisher": publisher,
        }
        if meta.get("datePublished"):
            obj["datePublished"] = meta["datePublished"]
        obj["dateModified"] = meta.get("dateModified") or meta.get("datePublished") or ""
        if not obj["dateModified"]:
            del obj["dateModified"]
        out.append(obj)
    elif kind == "SoftwareApplication":
        out.append({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "description": meta["description"],
            "url": canonical,
            "image": image,
            "applicationCategory": meta.get("appCategory", "BusinessApplication"),
            "operatingSystem": "Web",
            "inLanguage": site["lang"],
            "publisher": publisher,
        })
    elif kind == "Course":
        out.append({
            "@context": "https://schema.org",
            "@type": "Course",
            "name": name,
            "description": meta["description"],
            "url": canonical,
            "image": image,
            "inLanguage": site["lang"],
            "provider": publisher,
        })
    else:
        out.append({
            "@context": "https://schema.org",
            "@type": kind,
            "name": name,
            "description": meta["description"],
            "url": canonical,
            "image": image,
            "inLanguage": site["lang"],
            "isPartOf": {"@type": "WebSite", "name": site["brand"], "url": base + "/"},
            "publisher": publisher,
        })

    # 빵부스러기 — 홈 › (상위 목록) › 현재 페이지
    crumbs = [{"name": site["brand"], "url": base + "/"}]
    if page.startswith("contents/blog/"):
        crumbs.append({"name": "블로그", "url": base + "/contents/bloglist.html"})
    elif page.startswith("contents/newsroom/"):
        crumbs.append({"name": "뉴스룸", "url": base + "/contents/newsroom.html"})
    if page != "index.html":
        crumbs.append({"name": name, "url": canonical})
    if len(crumbs) > 1:
        out.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": c["name"], "item": c["url"]}
                for i, c in enumerate(crumbs)
            ],
        })
    return out


# ──────────────────────────────────────────────────────── head 정리 + 주입

CLEAN_PATTERNS = [
    re.compile(re.escape(BEGIN[:16]) + r".*?" + re.escape(END), re.S),
    re.compile(r"<!--\s*SEO:BEGIN.*?<!--\s*SEO:END\s*-->", re.S),
    re.compile(r"<title\b[^>]*>.*?</title\s*>", re.S | re.I),
    re.compile(r'<meta\s+name=["\']description["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+name=["\']keywords["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+name=["\']robots["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+(?:property|name)=["\']og:[^"\']*["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+(?:property|name)=["\']article:[^"\']*["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+(?:name|property)=["\']twitter:[^"\']*["\'][^>]*>\s*', re.I),
    re.compile(r'<link\s+rel=["\']canonical["\'][^>]*>\s*', re.I),
    re.compile(r'<meta\s+name=["\'](?:google|naver)-site-verification["\'][^>]*>\s*', re.I),
    re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script\s*>', re.S | re.I),
    re.compile(r'<script[^>]+googletagmanager\.com/gtag[^>]*>\s*</script\s*>\s*', re.I),
    re.compile(r"<script>\s*window\.dataLayer\s*=.*?</script\s*>\s*", re.S | re.I),
    re.compile(r'<meta\s+charset=[^>]*>\s*', re.I),
]


SKIP_LAZY = ("logo", "favicon")

# 순수 장식용 이미지 — alt="" 가 정답이며 스크린리더에서도 숨긴다.
DECORATIVE = re.compile(r"(decoration|divider|spacer|shape-|/dot|blank)", re.I)


def add_lazy_loading(src: str, eager_count: int = 2) -> tuple[str, int]:
    """<main> 이후의 이미지에 loading="lazy" decoding="async" 를 붙인다.

    · <main> 이전(네비게이션/로고)은 건드리지 않는다.
    · <main> 직후 eager_count 개(히어로/LCP 후보)는 즉시 로드로 남긴다.
      LCP 이미지를 lazy 로 만들면 오히려 지표가 나빠지기 때문.
    · 이미 loading 속성이 있으면 그대로 둔다.
    """
    m = re.search(r"<main\b", src, re.I)
    if not m:
        return src, 0
    head_part, body_part = src[:m.start()], src[m.start():]

    seen = 0
    changed = 0

    def repl(mo):
        nonlocal seen, changed
        tag = mo.group(0)
        low = tag.lower()
        if any(k in low for k in SKIP_LAZY):
            return tag
        seen += 1
        # 이미 처리된 이미지 — seen 은 세되 다시 손대지 않는다 (멱등성).
        if "loading=" in low or "decoding=" in low:
            return tag
        changed += 1
        extra = ' decoding="async"' if seen <= eager_count else ' loading="lazy" decoding="async"'
        if DECORATIVE.search(tag) and "aria-hidden" not in low:
            extra += ' aria-hidden="true"'
        stripped = tag.rstrip()
        self_closing = stripped.endswith("/>")
        inner = (stripped[:-2] if self_closing else stripped[:-1]).rstrip()
        return inner + extra + (" />" if self_closing else ">")

    body_part = re.sub(r"<img\b[^>]*?/?>", repl, body_part)
    return head_part + body_part, changed


def apply_to_file(page: str, meta: dict, site: dict, dry: bool) -> bool:
    path = os.path.join(ROOT, page)
    src = open(path, encoding="utf-8").read()
    span = head_span(src)
    if not span:
        warn(f"{page}: <head> 를 찾지 못해 건너뜀")
        return False
    hs, he = span
    head, rest_before, rest_after = src[hs:he], src[:hs], src[he:]

    for pat in CLEAN_PATTERNS:
        head = pat.sub("", head)
    head = re.sub(r"\n\s*\n\s*\n+", "\n\n", head)

    block = ('\n        <meta charset="utf-8">\n        '
             + build_block(page, meta, site) + "\n")
    new_head = block + head.lstrip("\n")
    new_src = rest_before + new_head + rest_after

    # 본문 이미지 지연 로딩
    new_src, lazied = add_lazy_loading(new_src)
    if lazied:
        note(f"{page}: 이미지 {lazied}개에 지연 로딩/디코딩 속성 추가")

    # <html lang> 보정
    if not re.search(r"<html\b[^>]*\blang=", new_src, re.I):
        new_src = re.sub(r"<html\b", f'<html lang="{site["lang"]}"', new_src, count=1, flags=re.I)
        note(f"{page}: <html lang=\"{site['lang']}\"> 추가")

    if new_src == src:
        return False
    if not dry:
        open(path, "w", encoding="utf-8").write(new_src)
    return True


# ──────────────────────────────────────────────────────── sitemap / robots

def write_sitemap(entries: list[dict], site: dict, dry: bool):
    base = site["baseUrl"].rstrip("/")
    rows = []
    for e in sorted(entries, key=lambda x: (-float(x["priority"]), x["page"])):
        loc = base + "/" + ("" if e["page"] == "index.html" else e["page"])
        rows.append("  <url>")
        rows.append(f"    <loc>{esc(loc)}</loc>")
        if e.get("lastmod"):
            rows.append(f"    <lastmod>{e['lastmod']}</lastmod>")
        rows.append(f"    <changefreq>{e['changefreq']}</changefreq>")
        rows.append(f"    <priority>{e['priority']}</priority>")
        rows.append("  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    if not dry:
        open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    return len(entries)


def write_robots(site: dict, dry: bool):
    base = site["baseUrl"].rstrip("/")
    txt = f"""# www.uengine.org — robots.txt
# .claude/skills/seo-optimize/apply_seo.py 가 생성합니다. 직접 수정하지 마세요.

User-agent: *
Allow: /

# 검색 인덱스에서 제외할 내부 경로
# (gh-pages 배포가 .gitignore 로 걸러지지 않는 파일을 전부 올리므로 여기서 색인만 막는다)
Disallow: /php/
Disallow: /node_modules/
Disallow: /doc-inbox/
Disallow: /newsletters/
Disallow: /learning/
Disallow: /.claude/
Disallow: /.agents/
Disallow: /CLAUDE.md
Disallow: /README.md
Disallow: /package.json

# AI 검색/에이전트 크롤러 명시적 허용 (인용 노출을 위해)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {base}/sitemap.xml
"""
    if not dry:
        open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(txt)


# ──────────────────────────────────────────────────────────────── main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검사만")
    ap.add_argument("--only", action="append", default=[], help="특정 페이지만 처리")
    args = ap.parse_args()
    dry = args.check

    cfg = json.load(open(META_PATH, encoding="utf-8"))
    site, reg, blog_def = cfg["site"], cfg["pages"], cfg["blogDefaults"]

    cards = {}
    cards.update(harvest_cards("contents/bloglist.html", "blog/"))
    cards.update(harvest_cards("contents/newsroom.html", "newsroom/"))

    def scan(pattern):
        return [os.path.relpath(p, ROOT).replace(os.sep, "/")
                for p in glob.glob(os.path.join(ROOT, pattern))]

    pages = args.only or sorted(
        ["index.html"]
        + scan("contents/*.html")
        + scan("contents/blog/*.html")
        + scan("contents/newsroom/*.html")
    )
    pages = [p.replace(os.sep, "/") for p in pages]

    sitemap_entries, resolved, changed = [], {}, 0

    for page in pages:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            warn(f"{page}: 파일 없음")
            continue
        src = open(path, encoding="utf-8").read()
        entry = dict(reg.get(page, {}))
        if entry.get("skip"):
            note(f"{page}: skip=true (레지스트리 지정) — 건드리지 않음")
            continue

        is_blog = page.startswith("contents/blog/")
        is_news = page.startswith("contents/newsroom/")
        meta: dict = {}

        if is_blog or is_news:
            meta.update({k: v for k, v in blog_def.items() if not k.startswith("_")})
            meta.pop("breadcrumbRoot", None)
            meta.pop("titleSuffix", None)
            if is_news:
                meta["schema"] = "NewsArticle"
            card = cards.get(page)
            if card:
                meta.update({k: v for k, v in card.items() if v})
            else:
                warn(f"{page}: 목록 페이지에 카드가 없습니다 "
                     f"({'bloglist.html' if is_blog else 'newsroom.html'} 에 항목을 추가하세요)")
        meta.update({k: v for k, v in entry.items() if not k.startswith("_")})

        derived = derive_from_page(src)
        source_note = []
        if not meta.get("title"):
            meta["title"] = derived.get("title") or site["brand"]
            source_note.append("title")
        if not meta.get("description"):
            meta["description"] = derived.get("description") or ""
            source_note.append("description")
        if source_note and not meta.get("noindex"):
            warn(f"{page}: {', '.join(source_note)} 을(를) 페이지 본문에서 자동 유추했습니다. "
                 f"seo-meta.json 의 pages[\"{page}\"] 에 직접 작성하는 편이 좋습니다.")

        # 브랜드 접미사 (구조화 데이터용 순수 제목은 따로 보관)
        meta["cleanTitle"] = meta["title"]
        suffix = blog_def.get("titleSuffix") if (is_blog or is_news) else site["titleSuffix"]
        if suffix and suffix.strip(" |") not in meta["title"]:
            room = site["titleMaxLen"] - len(suffix)
            meta["title"] = truncate(meta["title"], room) + suffix

        meta["description"] = truncate(meta["description"], site["descMaxLen"])
        if not meta.get("image"):
            meta["image"] = (first_local_image(src, page)
                             or meta.get("fallbackImage")
                             or site["defaultImage"])
        meta.pop("fallbackImage", None)
        if (is_blog or is_news) and "type" not in meta:
            meta["type"] = "article"

        lastmod = git_last_modified(page)
        if lastmod:
            meta["dateModified"] = lastmod

        # 품질 점검
        if not meta.get("noindex"):
            if len(meta["description"]) < site["descMinLen"]:
                warn(f"{page}: description 이 너무 짧습니다 ({len(meta['description'])}자, "
                     f"권장 {site['descMinLen']}~{site['descMaxLen']}자)")
            if len(meta["title"]) > site["titleMaxLen"]:
                warn(f"{page}: title 이 깁니다 ({len(meta['title'])}자, 권장 {site['titleMaxLen']}자 이하)")
            h1n = len(re.findall(r"<h1\b", src))
            if h1n == 0:
                warn(f"{page}: <h1> 이 없습니다")
            elif h1n > 1:
                warn(f"{page}: <h1> 이 {h1n}개입니다 (1개만 두고 나머지는 <h2> 로)")

            # LCP 후보(= 지연 로딩이 아닌 본문 이미지)가 무겁지 않은지
            body = src[re.search(r"<main\b", src).start():] if re.search(r"<main\b", src) else src
            for tag in re.findall(r"<img\b[^>]*>", body):
                if 'loading="lazy"' in tag:
                    continue
                m2 = re.search(r'src="((?:\.\./)*images/[^"]+)"', tag)
                if not m2:
                    continue
                rel = re.sub(r"^(\.\./)+", "", m2.group(1))
                full = os.path.join(ROOT, rel)
                if not os.path.exists(full):
                    continue
                kb = os.path.getsize(full) / 1024
                if kb > LCP_IMAGE_KB_LIMIT and not rel.lower().endswith(".webp"):
                    warn(f"{page}: LCP 후보 이미지가 {kb:.0f}KB 입니다 — {rel} "
                         f"(WebP 로 변환하면 보통 75~90% 줄어듭니다. "
                         f"convert_webp.py 참고)")

            imgs = re.findall(r"<img\b[^>]*>", src)
            no_alt = [i for i in imgs if not re.search(r'\balt\s*=', i)]
            empty_alt = [i for i in imgs
                         if re.search(r"""\balt\s*=\s*(""|'')""", i) and not DECORATIVE.search(i)]
            if no_alt:
                warn(f"{page}: alt 속성이 없는 <img> {len(no_alt)}개")
            if empty_alt:
                warn(f"{page}: alt 가 빈 <img> {len(empty_alt)}개 "
                     f"(순수 장식용이면 그대로 두고, 내용이 있는 이미지면 설명을 넣으세요)")
            resolved.setdefault(("title", meta["title"]), []).append(page)
            resolved.setdefault(("desc", meta["description"]), []).append(page)
            sitemap_entries.append({
                "page": page,
                "priority": str(meta.get("priority", "0.5")),
                "changefreq": meta.get("changefreq", "monthly"),
                "lastmod": lastmod,
            })

        if apply_to_file(page, meta, site, dry):
            changed += 1

    for (kind, val), pgs in resolved.items():
        if len(pgs) > 1:
            warn(f"{kind} 중복 ({len(pgs)}개): {val[:50]}… → {', '.join(pgs)}")

    # --only 는 부분 실행이므로 sitemap 을 덮어쓰면 안 된다 (전체 목록이 아니기 때문).
    if args.only:
        sitemap_msg = "sitemap 은 부분 실행이라 건너뜀"
    else:
        sitemap_msg = f"sitemap 항목 {write_sitemap(sitemap_entries, site, dry)}개"
        write_robots(site, dry)

    a = site.get("analytics", {})
    if not a.get("ga4MeasurementId"):
        note("GA4 측정 ID 미설정 — seo-meta.json 의 site.analytics.ga4MeasurementId 를 채우면 자동 삽입됩니다.")
    if not a.get("googleSiteVerification"):
        note("Google Search Console 확인 코드 미설정 — site.analytics.googleSiteVerification")
    if not a.get("naverSiteVerification"):
        note("네이버 웹마스터도구 확인 코드 미설정 — site.analytics.naverSiteVerification")

    mode = "검사" if dry else "적용"
    print(f"[seo] {mode} 완료 — 페이지 {len(pages)}개 중 {changed}개 갱신, {sitemap_msg}")
    for m in notes:
        print(f"  · {m}")
    if warnings:
        print(f"\n[seo] 확인 필요 {len(warnings)}건:")
        for w in warnings:
            print(f"  ! {w}")
    _ = dt
    return 1 if (dry and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
