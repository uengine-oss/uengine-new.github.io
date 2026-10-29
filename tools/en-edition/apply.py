#!/usr/bin/env python3
"""Assemble an English page from a Korean source page + translations.

  apply.py <src.html> <segments.json> <tm.json> <out.html>

- splices the English text into the exact byte ranges recorded by extract.py
- rewrites relative asset paths (one directory deeper: en/ mirrors the tree)
- html lang / og:locale / canonical / hreflang / JSON-LD inLanguage
- swaps Korean-only JS helpers for their en/ variants
- inserts a KO/EN language switch in the nav
"""
import hashlib
import base64
import importlib.util
import re, json, sys, os, html as htmlmod

ASSET_DIRS = ('images', 'css', 'js', 'webfonts', 'php', 'docs', 'fonts', 'learning', 'newsletters')
JS_EN = {'js/product-ontology.js', 'js/contact-form.js', 'js/register-form.js'}
SITE = 'https://www.uengine.org/'


def splice(src, segs, tm, missing):
    out = src
    for sg in sorted(segs, key=lambda s: s['start'], reverse=True):
        assert src[sg['start']:sg['end']] == sg.get('raw', sg['ko']), ('segment drift', sg['id'], sg['kind'])
        en = tm.get(sg['ko'])
        if en is None:
            missing.append(sg['ko'])
            continue
        k = sg['kind']
        if k == 'attr':
            q = sg.get('quote', '"')
            en = en.replace('"', '&quot;') if q == '"' else en.replace("'", '&#39;')
            en = en.replace('\n', ' ')
        elif k == 'json':
            en = json.dumps(en, ensure_ascii=False)[1:-1]
        elif k in ('js', 'jsfile'):
            q = sg['quote']
            if q == '`':
                en = en.replace('`', '\\`')
            else:
                # keep existing escapes; escape bare quote chars of the same kind
                en = re.sub(r'(?<!\\)' + re.escape(q), '\\' + q, en)
                en = en.replace('\n', '\\n')
        out = out[:sg['start']] + en + out[sg['end']:]
    return out


SITE_ROOT = os.path.dirname(os.path.abspath(__file__))  # overridden by batch.py


def fix_asset_paths(s, root):
    """Point relative asset URLs one level deeper, and prefer an English screenshot
    at images/en/<path> whenever one has been captured."""
    dirs = '|'.join(ASSET_DIRS)
    pat = re.compile(r'(?P<q>["\'(])(?P<rel>(?:\.\./)*)(?P<dir>' + dirs + r')/(?P<rest>[^"\')]*)')

    def repl(m):
        d, rest = m.group('dir'), m.group('rest')
        if d == 'docs' and root:
            # a doc site with its own English edition (en/docs/...) stays inside en/
            path, _, anchor = rest.partition('#')
            if path.split('/')[0] in EN_DOCS or os.path.exists(os.path.join(root, 'en', 'docs', path.split('?')[0])):
                anchor = DOC_ANCHORS.get(anchor, anchor)
                return m.group('q') + m.group('rel') + 'docs/' + path + ('#' + anchor if anchor else '')
        if d == 'images' and root:
            candidate = os.path.join(root, 'images', 'en', rest.split('?')[0].split('#')[0])
            if os.path.isfile(candidate):
                return m.group('q') + m.group('rel') + '../images/en/' + rest
        return m.group('q') + m.group('rel') + '../' + d + '/' + rest

    return pat.sub(repl, s)


# Doc sites whose English edition (en/docs/<name>/) ships together with the English pages that
# link to it, even while it is still being built and is not on disk yet.
EN_DOCS = {'process-gpt-lite'}

# Heading anchors differ between a Korean doc page and its English edition.
DOC_ANCHORS = {
    'macos에-설치하기': 'installing-on-macos',
}


def rel_prefix(page):
    depth = page.count('/')
    return '../' * depth


def add_lang_switch(s, page, to_en):
    """Insert a KO/EN switch in the desktop nav and mobile header."""
    if to_en:
        target = rel_prefix(page) + 'en/' + page
        label, title = 'EN', 'English'
    else:
        # the English page lives one directory deeper (en/<page>), so climb one extra level
        target = '../' * (page.count('/') + 1) + page
        label, title = 'KO', 'Korean'
    desktop = (f'<li class="pc-chat lang-switch"><a href="{target}" class="opacity-1 no-hover" title="{title}" hreflang="{"en" if to_en else "ko"}">'
               f'<span class="link-hover-anim underline" data-link-animate="y">{label}</span></a></li>\n                            ')
    n = 0
    s, n = re.subn(r'(<ul class="items-end clearlist">\s*)', lambda m: m.group(1) + desktop, s, count=1)
    # wrapped in comments so the switch never merges into the neighbouring text run
    mobile = (f'<!--lang-switch--><a href="{target}" class="opacity-1 no-hover mobile-chat lang-switch" '
              f'title="{title}">{label}</a><!--/lang-switch-->\n                        ')
    s, n2 = re.subn(r'(<div class="mobile-nav"[^>]*>\s*(?:<!--[^>]*-->\s*)?)', lambda m: m.group(1) + mobile, s, count=1)
    return s, n, n2


def to_en_url(u):
    """https://www.uengine.org/contents/x.html -> .../en/contents/x.html (html pages and root only)."""
    m = re.match(r'^' + re.escape(SITE) + r'(?!en/)(?P<p>(?:[A-Za-z0-9_./-]*\.html)?)$', u)
    if not m:
        return u
    return SITE + 'en/' + m.group('p')


def seo_fixes(s, page):
    s = re.sub(r'<html\s+lang="ko"', '<html lang="en"', s, count=1)
    s = s.replace('<meta property="og:locale" content="ko_KR">', '<meta property="og:locale" content="en_US">')
    s = s.replace('"inLanguage":"ko"', '"inLanguage":"en"')
    # canonical / og:url / breadcrumb items
    s = re.sub(r'(<link rel="canonical" href=")([^"]+)(")', lambda m: m.group(1) + to_en_url(m.group(2)) + m.group(3), s)
    s = re.sub(r'(<meta property="og:url" content=")([^"]+)(")', lambda m: m.group(1) + to_en_url(m.group(2)) + m.group(3), s)
    s = re.sub(r'("item":")([^"]+)(")', lambda m: m.group(1) + to_en_url(m.group(2)) + m.group(3), s)
    s = re.sub(r'("@type":"(?:SoftwareApplication|Article|BlogPosting|WebPage|Product|Service|Course|Event|NewsArticle|TechArticle|CollectionPage|AboutPage|ContactPage)"[^{}]*?"url":")([^"]+)(")',
               lambda m: m.group(1) + to_en_url(m.group(2)) + m.group(3), s)
    # Social/search preview images are absolute URLs, so the relative-path pass never sees
    # them; point them at the English capture whenever one exists.
    def en_image(m):
        rest = m.group(1)
        if SITE_ROOT and os.path.isfile(os.path.join(SITE_ROOT, 'images', 'en', rest)):
            return SITE + 'images/en/' + rest
        return m.group(0)

    s = re.sub(re.escape(SITE) + r'images/(?!en/)([^"\'\s)]+)', en_image, s)

    ko_url = SITE + ('' if page == 'index.html' else page)
    en_url = SITE + 'en/' + ('' if page == 'index.html' else page)
    alt = (f'\n        <link rel="alternate" hreflang="ko" href="{ko_url}">'
           f'\n        <link rel="alternate" hreflang="en" href="{en_url}">'
           f'\n        <link rel="alternate" hreflang="x-default" href="{ko_url}">')
    if '<!-- SEO:END -->' in s:
        s = s.replace('<!-- SEO:END -->', '<!-- SEO:END -->' + alt, 1)
    else:
        s = re.sub(r'(<meta charset="utf-8">)', lambda m: m.group(1) + alt, s, count=1)
    return s


def localize_youtube(s):
    """Force the YouTube player chrome into English. Without hl= the embed follows the
    viewer's browser locale, so a Korean visitor saw "다음에서 보기" over an English page."""
    def repl(m):
        url = m.group(0)
        if 'hl=' in url:
            return url
        return url + ('&' if '?' in url else '?') + 'hl=en&cc_lang_pref=en'
    return re.sub(r'https://www\.youtube(?:-nocookie)?\.com/embed/[A-Za-z0-9_-]+(?:\?[^"\'\s<>]*)?', repl, s)


# Some posts embed their figures as base64 data URIs rather than files, so no path-based
# pass can reach them. These are Korean-lettered diagrams redrawn in English; keyed by the
# md5 of the decoded Korean bytes so the swap survives an edit elsewhere in the page.
INLINE_IMAGE_OVERRIDES = {
    '327420ee5110fd8bf32fb0a2077f2289': 'images/en/blog/aidevoutlook/fig1.png',
    '7ed64f6c53f526ae9f1c65a201c561e3': 'images/en/blog/aidevoutlook/fig2.png',
    'dd1396b9e1757c65c0908482e2a5c119': 'images/en/blog/aidevoutlook/fig3.png',
    'ea790220a8172dfd583a2e364b643086': 'images/en/blog/aidevoutlook/fig4.png',
    '499eaeac89db29b5321c3274d18867ec': 'images/en/blog/aidevoutlook/fig5.png',
}

INLINE_IMAGE = re.compile(r'data:image/(?:png|jpeg|jpg|gif|webp);base64,([A-Za-z0-9+/=]{500,})')


def swap_inline_images(s, page):
    """Replace a base64-inlined Korean figure with the English redraw held on disk."""
    up = '../' * (page.count('/') + 1)

    def repl(m):
        try:
            digest = hashlib.md5(base64.b64decode(m.group(1))).hexdigest()
        except Exception:
            return m.group(0)
        local = INLINE_IMAGE_OVERRIDES.get(digest)
        return up + local if local else m.group(0)

    return INLINE_IMAGE.sub(repl, s)


# A Korean-narrated YouTube demo is replaced on the English site wherever an English
# recording of the same walkthrough exists. Keyed by YouTube id.
VIDEO_OVERRIDES = {
    'U_21lPKoGOI': 'images/en/video/prompt-chaining-demo-en.mp4',
}


# Korean-narrated YouTube video -> an English-narrated YouTube video of the same walkthrough.
YOUTUBE_OVERRIDES = {
    'qRZ8bE8Ffsg': 'ckduR9oRtuE',  # Ontological Studio: build from a document (tutorial ch. 12)
    'np3Q9484lYo': 'ajoW9Oxf83g',  # Ontological Studio: run actions (tutorial ch. 16)
    'Lq4ZL_8vMtk': 'gAZZTiakdAA',  # Ontological Studio: code apps (tutorial ch. 18)
    'HBk3WCvYx2c': 'TNdTiwJD8-s',  # 메인 전체 소개 영상(Showcase 나레이션판)
}


def swap_videos(s, page):
    """Swap a Korean-narrated YouTube video for its English counterpart (on YouTube or hosted here)."""
    for vid, en in YOUTUBE_OVERRIDES.items():
        s = re.sub(r'(youtube(?:-nocookie)?\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)' + re.escape(vid) + r'\b',
                   lambda m: m.group(1) + en, s)
    up = '../' * (page.count('/') + 1)
    for vid, local in VIDEO_OVERRIDES.items():
        src = up + local
        # <iframe ... src="https://www.youtube.com/embed/<id>..." ...></iframe>
        s = re.sub(r'<iframe\b[^>]*?(?:youtube\.com/embed|youtube-nocookie\.com/embed)/' + re.escape(vid) +
                   r'[^>]*?>\s*</iframe>',
                   f'<video class="vd-box" src="{src}" controls playsinline preload="metadata" '
                   f'style="width:100%;aspect-ratio:16/9;border:0;"></video>', s)
        # plain links to the same recording
        s = re.sub(r'https://youtu\.be/' + re.escape(vid) + r'\b', src, s)
    return s


def pgl_rules(s, page):
    """English Process GPT Lite page (see tools/pgl-en-images.md and tools/pgl-en-videos.json).

    - screenshots: images/processgptlite/en/<name>.jpg, falling back to the Korean capture until the
      English one exists
    - the Lite practitioner AX course has no English page: its links open the English AX training page
    - the in-place player shows YouTube's chrome and captions in English
    - Korean videos are swapped for their English re-recordings as tools/pgl-en-videos.json fills up
    """
    s = re.sub(r'src="((?:\.\./)*)images/processgptlite/([A-Za-z0-9_-]+\.jpg)"',
               lambda m: (f'src="{m.group(1)}images/processgptlite/en/{m.group(2)}" '
                          f'onerror="this.onerror=null;this.src=\'{m.group(1)}images/processgptlite/{m.group(2)}\'"'), s)
    s = re.sub(r'href="ax-lite-course\.html(?:#[^"]*)?"', 'href="educationax.html"', s)
    s = s.replace("'?autoplay=1&rel=0'", "'?autoplay=1&rel=0&hl=en&cc_lang_pref=en'")
    tool = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pgl-en-videos.py')
    if os.path.isfile(tool):
        spec = importlib.util.spec_from_file_location('pgl_en_videos', tool)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        s, _ = mod.rewrite(s, mod.load_map())
    return s


# Page-specific rules, applied after the generic passes and before links are resolved.
PAGE_RULES = {
    'contents/processgptlite.html': pgl_rules,
}


def swap_js(s):
    for js in JS_EN:
        s = re.sub(r'((?:\.\./)*)' + re.escape(js), lambda m: m.group(1) + js.replace('js/', 'js/en/'), s)
    return s


def link_untranslated(s, page, root):
    """A linked page that has no English edition yet opens in Korean instead of a 404."""
    if not root:
        return s
    here = os.path.dirname(page)
    up = '../' * (page.count('/') + 1)

    def repl(m):
        target = os.path.normpath(os.path.join(here, m.group(2)))
        if os.path.isfile(os.path.join(root, target)) and not os.path.isfile(os.path.join(root, 'en', target)):
            return m.group(1) + up + target + m.group(3)
        return m.group(0)

    return re.sub(r'(href=")((?!https?:|/|#|\.\./|mailto:)[A-Za-z0-9_./-]+\.html)((?:#[^"]*)?")', repl, s)


STRIP_SWITCH = (re.compile(r'<li class="pc-chat lang-switch">.*?</li>\s*'), re.compile(r'<a [^>]*class="[^"]*lang-switch"[^>]*>[^<]*</a>\s*'))


def build(page, src, segs, tm):
    missing = []
    s = splice(src, segs, tm, missing)
    # the Korean source now carries an "EN" link; drop it before adding the "KO" one
    for pat in STRIP_SWITCH:
        s = pat.sub('', s)
    s = fix_asset_paths(s, SITE_ROOT)
    s = swap_js(s)
    s = swap_videos(s, page)
    s = swap_inline_images(s, page)
    s = localize_youtube(s)
    # Korean pages link into the English tree as "en/contents/x.html"; inside that tree the
    # same link must stay relative to en/ itself, or it would resolve to /en/en/contents/.
    s = re.sub(r'((?:\.\./)*)en/(contents/|index\.html)', lambda m: m.group(1) + m.group(2), s)
    if page in PAGE_RULES:
        s = PAGE_RULES[page](s, page)
    s = link_untranslated(s, page, SITE_ROOT)
    s = seo_fixes(s, page)
    s, n1, n2 = add_lang_switch(s, page, to_en=False)
    return s, missing, (n1, n2)


if __name__ == '__main__':
    page, segp, tmp, outp = sys.argv[1:5]
    src = open(page, encoding='utf-8').read()
    segs = json.load(open(segp, encoding='utf-8'))
    tm = json.load(open(tmp, encoding='utf-8'))
    s, missing, ns = build(page, src, segs, tm)
    os.makedirs(os.path.dirname(outp) or '.', exist_ok=True)
    open(outp, 'w', encoding='utf-8').write(s)
    print(f'{page} -> {outp}: missing={len(missing)} switch={ns}')
    for m in missing[:5]:
        print('   MISSING', repr(m[:100]))
