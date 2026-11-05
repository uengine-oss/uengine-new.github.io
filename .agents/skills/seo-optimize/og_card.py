#!/usr/bin/env python3
"""공유 미리보기 카드(og:image) — 페이지 하나에 1200×630 JPG 를 만든다.

페이스북·카카오톡·슬랙에 주소를 붙이면 og:title 과 og:image 가 보인다. 본문 캡처를 그대로 쓰면
작게 줄어 글자가 안 보이므로, 제목의 한 줄 가치("에이전트에 최적화된 ERP")를 크게 쓴 카드를 만든다.

    python3 .claude/skills/seo-optimize/og_card.py contents/erp.html
    python3 .claude/skills/seo-optimize/og_card.py contents/erp.html --shot path/to/shot.png --crop 892,118,770,550
    python3 .claude/skills/seo-optimize/og_card.py contents/newproduct.html --headline "…" --sub "…" --cap "AI-Native Enterprise"

글은 이 순서로 정한다: 옵션 → seo-meta.json 의 pages[페이지] → 페이지 <head> 의 og:title·og:description.
  title 이 "제품명 — 한 줄 가치" 면 제품명은 작게, 한 줄 가치는 크게 쓴다. sub 는 description 의 첫 문장이다.
그림: --shot 이 없으면 페이지가 쓰는 첫 본문 이미지(apply_seo 의 og:image 고르기와 같은 규칙)를 오른쪽에 넣는다. --no-shot 이면 글만.
영문: tools/en-edition/tm.json 에 제목·설명 번역이 있으면 images/en/og/<slug>.jpg 도 만든다(영문 빌드가 자동으로 바꿔 쓴다).
끝나면 seo-meta.json 의 pages[페이지].image 를 카드로 바꾼다(--keep-meta 면 안 바꾼다). 그다음 apply_seo.py --only <페이지> 와
영문 한 페이지 빌드를 돌린다(SKILL.md 「공유 미리보기 카드」).
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
META_PATH = os.path.join(HERE, "seo-meta.json")
TM_PATH = os.path.join(ROOT, "tools", "en-edition", "tm.json")
W, H = 1200, 630

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{font-family:Pretendard,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;background:linear-gradient(135deg,#f3f3f5 0%,#e4e5ea 100%);display:flex;align-items:center;color:#111}
.l{box-sizing:border-box;padding:0 40px 0 72px;width:__LW__px}
.cap{display:inline-block;border:2px solid #111;border-radius:999px;padding:6px 16px;font-size:20px;font-weight:600;letter-spacing:.5px}
.name{font-size:44px;font-weight:700;margin:24px 0 6px;letter-spacing:-1px}
.t{font-size:62px;font-weight:800;line-height:1.18;letter-spacing:-2px;word-break:keep-all;overflow-wrap:break-word;margin:0 0 22px}
.s{font-size:25px;line-height:1.5;color:#444;word-break:keep-all;margin:0}
.r{flex:1;display:flex;justify-content:center;padding-right:48px}
.r img{max-width:560px;max-height:460px;border-radius:18px;box-shadow:0 18px 50px rgba(20,30,60,.22);object-fit:cover}
</style></head><body>
<div class="l">__CAP__<div class="name">__NAME__</div><p class="t" id="t">__T__</p><p class="s" id="s">__S__</p></div>
__SHOT__
<script>
// 긴 제목은 글자를 줄여 왼쪽 칸 안에 넣는다(네 줄, 설명은 세 줄까지).
const fit = (el, min, lines) => { let f = parseFloat(getComputedStyle(el).fontSize);
  while (f > min && el.getBoundingClientRect().height > parseFloat(getComputedStyle(el).lineHeight) * lines + 1) { f -= 2; el.style.fontSize = f + 'px' } }
fit(document.getElementById('t'), 34, 3); fit(document.getElementById('s'), 18, 3)
</script></body></html>"""


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def slug_of(page: str) -> str:
    """contents/erp.html → erp, contents/blog/foo.html → blog-foo, index.html → home."""
    p = page.replace("\\", "/")
    if p == "index.html":
        return "home"
    p = re.sub(r"^contents/", "", p)
    return re.sub(r"\.html?$", "", p).replace("/", "-")


def head_meta(src: str, prop: str) -> str | None:
    m = re.search(r'<meta\s+property="%s"\s+content="([^"]*)"' % re.escape(prop), src)
    return html.unescape(m.group(1)) if m else None


def split_title(title: str) -> tuple[str, str]:
    for sep in (" — ", " – ", " | ", " - "):
        if sep in title:
            a, b = title.split(sep, 1)
            return a.strip(), b.strip()
    return "", title.strip()


def first_sentence(text: str, limit: int = 70) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    m = re.search(r"^(.+?[.!?。])(\s|$)", text)
    s = m.group(1) if m else text
    if len(s) > limit:
        return s[:limit].rsplit(" ", 1)[0].rstrip(",;:·") + "…"
    return s.rstrip(".。")


IMG_ANY = re.compile(r'["\(]((?:\.\./)*(?:images|docs)/[^"\')\s]+\.(?:jpg|jpeg|png|webp))', re.I)


def resolve_shot(arg: str | None, page: str, src: str, entry: dict) -> str | None:
    """오른쪽 그림: --shot → seo-meta 의 image(카드가 아니면) → 본문의 첫 콘텐츠 이미지(images/·docs/ 아래)."""
    if arg:
        p = arg if os.path.isabs(arg) else os.path.join(ROOT, arg.lstrip("/"))
        if not os.path.exists(p):
            sys.exit(f"그림이 없습니다: {arg}")
        return p
    seo = load_module("apply_seo", os.path.join(HERE, "apply_seo.py"))
    cands = []
    if entry.get("image") and not entry["image"].startswith("/images/og/"):
        cands.append(entry["image"])
    for m in IMG_ANY.finditer(src):
        low = m.group(1).lower()
        if any(k in low for k in seo.NEVER_OG + seo.LAST_RESORT_OG):
            continue
        cands.append("/" + re.sub(r"^(\.\./)+", "", m.group(1)))
    for c in cands:
        p = os.path.join(ROOT, c.lstrip("/"))
        if os.path.exists(p):
            return p
    return None


def crop_to_png(path: str, crop: str | None, out_dir: str) -> str:
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if crop:
        x, y, w, h = (int(v) for v in crop.split(","))
        im = im.crop((x, y, x + w, y + h))
    dst = os.path.join(out_dir, "shot.png")
    im.save(dst)
    return dst


def render(out: str, cap: str, name: str, headline: str, sub: str, shot: str | None, tmp: str) -> None:
    from playwright.sync_api import sync_playwright
    page_html = (TEMPLATE
                 .replace("__LW__", "560" if shot else "1100")
                 .replace("__CAP__", f'<span class="cap">{html.escape(cap)}</span>' if cap else "")
                 .replace("__NAME__", html.escape(name))
                 .replace("__T__", html.escape(headline))
                 .replace("__S__", html.escape(sub))
                 .replace("__SHOT__", f'<div class="r"><img src="{os.path.basename(shot)}"></div>' if shot else ""))
    card = os.path.join(tmp, f"card-{os.getpid()}.html")
    open(card, "w", encoding="utf-8").write(page_html)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto("file://" + card, wait_until="networkidle")
        pg.wait_for_timeout(400)
        pg.screenshot(path=out, type="jpeg", quality=88)
        b.close()


def set_meta_image(page: str, image: str) -> str:
    """seo-meta.json 의 pages[page].image 를 바꾼다. 다른 줄은 건드리지 않게 글자로 고친다."""
    s = open(META_PATH, encoding="utf-8").read()
    key = json.dumps(page, ensure_ascii=False)
    i = s.find(f"    {key}: {{")
    if i < 0:
        j = s.index('"pages": {') + len('"pages": {')
        s = s[:j] + f'\n    {key}: {{\n      "image": {json.dumps(image)}\n    }},' + s[j:]
        how = "새 항목"
    else:
        end = s.index("\n    }", i)
        block = s[i:end]
        if re.search(r'\n      "image": "[^"]*"', block):
            block = re.sub(r'(\n      "image": )"[^"]*"', lambda m: m.group(1) + json.dumps(image), block, count=1)
        else:
            m = re.search(r'\n      "description": "(?:[^"\\]|\\.)*",?', block)
            at = m.end() if m else block.index("{") + 1
            line = f'\n      "image": {json.dumps(image)}'
            rest = block[at:]
            block = block[:at] + (line + "," if rest.strip() else line) + rest
            if m and not m.group(0).endswith(","):
                block = block.replace(m.group(0), m.group(0) + ",", 1)
        s = s[:i] + block + s[end:]
        how = "바꿈"
    json.loads(s)  # 깨뜨리지 않았는지
    open(META_PATH, "w", encoding="utf-8").write(s)
    return how


def main() -> None:
    ap = argparse.ArgumentParser(description="공유 미리보기 카드(1200×630 JPG)")
    ap.add_argument("page", help="사이트 루트 기준 페이지 경로, 예: contents/erp.html")
    ap.add_argument("--headline", help="크게 쓸 한 줄 가치(기본: title 의 — 뒤)")
    ap.add_argument("--name", help="제품·글 이름(기본: title 의 — 앞)")
    ap.add_argument("--sub", help="아래 한 줄(기본: description 의 첫 문장)")
    ap.add_argument("--cap", help="위쪽 알약 글(기본: breadcrumb 첫 칸)")
    ap.add_argument("--shot", help="오른쪽에 넣을 그림(기본: 페이지의 첫 본문 이미지)")
    ap.add_argument("--crop", help="그림에서 잘라 쓸 x,y,w,h (원본 픽셀)")
    ap.add_argument("--no-shot", action="store_true", help="그림 없이 글만")
    ap.add_argument("--en-headline"); ap.add_argument("--en-name"); ap.add_argument("--en-sub"); ap.add_argument("--en-cap")
    ap.add_argument("--no-en", action="store_true", help="영문 카드를 만들지 않는다")
    ap.add_argument("--keep-meta", action="store_true", help="seo-meta.json 을 바꾸지 않는다")
    a = ap.parse_args()

    page = a.page.replace("\\", "/").lstrip("./")
    src = open(os.path.join(ROOT, page), encoding="utf-8").read()
    entry = json.load(open(META_PATH, encoding="utf-8"))["pages"].get(page, {})
    title = entry.get("title") or head_meta(src, "og:title") or ""
    desc = entry.get("description") or head_meta(src, "og:description") or ""
    if not title:
        sys.exit(f"{page}: 제목을 찾지 못했습니다. seo-meta.json 에 title 을 쓰거나 --headline 을 주세요.")
    t_name, t_head = split_title(title)
    crumb = entry.get("breadcrumb") or []
    cap = a.cap if a.cap is not None else (crumb[0] if len(crumb) > 1 else "")
    name = a.name if a.name is not None else t_name
    headline = a.headline or t_head
    sub = a.sub if a.sub is not None else first_sentence(desc)

    slug = slug_of(page)
    rel = f"/images/og/{slug}.jpg"
    with tempfile.TemporaryDirectory() as tmp:
        picked = None if a.no_shot else resolve_shot(a.shot, page, src, entry)
        shot = crop_to_png(picked, a.crop, tmp) if picked else None
        render(os.path.join(ROOT, rel.lstrip("/")), cap, name, headline, sub, shot, tmp)
        print(f"카드: {rel}  ({'그림 ' + os.path.relpath(picked, ROOT) if picked else '글만'})")
        print(f"  제목 {headline!r} · 이름 {name!r} · 아래 {sub!r} · 알약 {cap!r}")

        if not a.no_en:
            tm = json.load(open(TM_PATH, encoding="utf-8")) if os.path.exists(TM_PATH) else {}
            en_title, en_desc = tm.get(title), tm.get(desc)
            if a.en_headline or en_title:
                e_name, e_head = split_title(en_title or "")
                e = {
                    "cap": a.en_cap if a.en_cap is not None else tm.get(cap, cap if cap.isascii() else ""),
                    "name": a.en_name if a.en_name is not None else (e_name or name if (e_name or name).isascii() else ""),
                    "headline": a.en_headline or e_head,
                    "sub": a.en_sub if a.en_sub is not None else first_sentence(en_desc or "", 110),
                }
                en_rel = f"/images/en/og/{slug}.jpg"
                render(os.path.join(ROOT, en_rel.lstrip("/")), e["cap"], e["name"], e["headline"], e["sub"], shot, tmp)
                print(f"영문 카드: {en_rel}  제목 {e['headline']!r}")
            else:
                print("영문 카드: 건너뜀 — tm.json 에 이 제목의 번역이 없습니다. 영문 빌드로 번역을 넣은 뒤 다시 돌리거나 --en-headline 을 주세요.")

    if not a.keep_meta:
        print(f"seo-meta.json: pages[{page!r}].image = {rel} ({set_meta_image(page, rel)})")
    print(f"다음: python3 .claude/skills/seo-optimize/apply_seo.py --only {page}  → 영문 한 페이지 빌드(tools/en-edition/README.md)")


if __name__ == "__main__":
    main()
