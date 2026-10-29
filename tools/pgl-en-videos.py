#!/usr/bin/env python3
"""Swap the Korean-narrated videos on the English Process GPT Lite page for their English re-recordings.

    python3 tools/pgl-en-videos.py           # rewrite en/contents/processgptlite.html in place
    python3 tools/pgl-en-videos.py --check   # report only, change nothing

tools/pgl-en-videos.json maps every Korean YouTube id used on the page (in page order) to
{"title_en": ..., "en_id": null}. Fill in "en_id" once the English recording is on YouTube and run
this script. Each filled entry replaces the Korean id everywhere it appears on the English page:
the embedded player, the gallery buttons (data-yt), the thumbnails (i.ytimg.com), the gallery
anchors (id="v-<id>") and the in-place player links (href="#v-<id>").

Only en/contents/processgptlite.html is written. The Korean page is never touched, and the en-edition
build (tools/en-edition/apply.py) applies the same map when it rebuilds the English page, so a rebuild
keeps the English videos. To correct an en_id that was already applied, fix it in the JSON and rebuild
the page with the en-edition build (the script only sees Korean ids still present on the page).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, 'tools', 'pgl-en-videos.json')
PAGE = os.path.join(ROOT, 'en', 'contents', 'processgptlite.html')
YT_ID = re.compile(r'^[A-Za-z0-9_-]{11}$')
# every place a YouTube id appears on the page; the id must end at a non-id character
PREFIXES = (r'youtube(?:-nocookie)?\.com/embed/', r'youtu\.be/', r'youtube\.com/watch\?v=',
            r'i\.ytimg\.com/vi/', r'data-yt="', r'id="v-', r'href="#v-')
AT = '(' + '|'.join(PREFIXES) + ')'


def load_map(path=MAP):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def pairs(mapping):
    """(korean_id, english_id) for every entry whose en_id is filled in and valid."""
    out = []
    for ko, entry in mapping.items():
        en = (entry or {}).get('en_id')
        if not en:
            continue
        if not YT_ID.match(en) or en == ko:
            print(f'  skip {ko}: en_id {en!r} is not a different 11-character YouTube id', file=sys.stderr)
            continue
        out.append((ko, en))
    return out


def rewrite(html, mapping):
    """Return (html, {korean_id: replacements}) with every filled-in Korean id swapped for its English id."""
    counts = {}
    for ko, en in pairs(mapping):
        html, n = re.subn(AT + re.escape(ko) + r'(?![A-Za-z0-9_-])', lambda m: m.group(1) + en, html)
        counts[ko] = n
    return html, counts


def main():
    check = '--check' in sys.argv[1:]
    mapping = load_map()
    with open(PAGE, encoding='utf-8') as f:
        html = f.read()
    new, counts = rewrite(html, mapping)
    on_page = lambda vid: re.search(AT + re.escape(vid) + r'(?![A-Za-z0-9_-])', html) is not None
    pending = [ko for ko, e in mapping.items() if not (e or {}).get('en_id')]
    done = [ko for ko, e in mapping.items() if (e or {}).get('en_id') and not on_page(ko)]
    for ko, n in counts.items():
        if n:
            print(f'{ko} -> {mapping[ko]["en_id"]}: {n} place(s){" (would change)" if check else ""}')
    print(f'{len(mapping)} videos: {sum(1 for n in counts.values() if n)} to swap now, '
          f'{len(done)} already English, {len(pending)} still waiting for an English id')
    if not check and new != html:
        with open(PAGE, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f'wrote {os.path.relpath(PAGE, ROOT)}')


if __name__ == '__main__':
    main()
