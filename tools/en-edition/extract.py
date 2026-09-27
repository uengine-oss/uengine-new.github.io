#!/usr/bin/env python3
"""Position-based extraction of translatable Korean segments from a raw HTML file.

Nothing is re-serialised: every segment records (start, end) byte offsets into the
original text so apply.py can splice translations back in verbatim.

Segment kinds
  text   : a run of text + inline tags inside one block element (inner HTML, may contain <a>, <strong>, <br> ...)
  attr   : the value of alt/title/placeholder/aria-label/content/value/... attributes
  js     : a JS string literal inside an inline <script> (quote char recorded)
  json   : a JSON string value inside <script type="application/ld+json">
  jsfile : same as js, but for a standalone .js file
"""
import re, json, sys, os

HANGUL = re.compile(r'[가-힣]')
INLINE = {'a','abbr','b','strong','i','em','span','br','code','small','sub','sup','u','mark','label',
          'font','s','del','ins','q','cite','time','wbr','kbd','var','samp','big','tt','nobr'}
ATTRS = ('alt','title','placeholder','aria-label','content','value','data-caption','data-title',
         'data-text','label','data-tooltip','data-hover','data-placeholder','data-alt-text','data-description')

TOKEN = re.compile(r'(?P<comment><!--.*?-->)'
                   r'|(?P<script><script\b[^>]*>.*?</script\s*>)'
                   r'|(?P<style><style\b[^>]*>.*?</style\s*>)'
                   # HTML only starts a tag when '<' is followed by an ASCII letter or / ! ?;
                   # "<드림바이브 분석 과정>" is therefore literal text, exactly as browsers render it.
                   r'|(?P<tag><(?=[a-zA-Z/!?])(?:[^<>"\']|"[^"<]*"|\'[^\'<]*\')*>)'
                   r'|(?P<text>[^<]+)', re.S)

JS_STR = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`", re.S)
JSON_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')


def tag_name(tok):
    m = re.match(r'<\s*/?\s*([a-zA-Z0-9]+)', tok)
    return m.group(1).lower() if m else ''


def js_segments(src, base, kind):
    """String literals containing Hangul inside JS source `src` (offset `base`)."""
    out = []
    # strip comments so that Korean code comments are ignored (positions kept via masking)
    masked = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group(0)), src, flags=re.S)
    masked = re.sub(r'(^|[^:\\])//[^\n]*', lambda m: m.group(1) + ' ' * (len(m.group(0)) - len(m.group(1))), masked)
    for m in JS_STR.finditer(masked):
        g = m.group(1) if m.group(1) is not None else (m.group(2) if m.group(2) is not None else m.group(3))
        if g is None or not HANGUL.search(g):
            continue
        q = masked[m.start()]
        out.append({'kind': kind, 'quote': q, 'start': base + m.start() + 1, 'end': base + m.end() - 1, 'ko': g})
    return out


def json_segments(src, base):
    out = []
    for m in JSON_STR.finditer(src):
        g = m.group(1)
        if HANGUL.search(g):
            out.append({'kind': 'json', 'start': base + m.start() + 1, 'end': base + m.end() - 1,
                        'raw': g, 'ko': json.loads('"' + g + '"')})
    return out


def extract_html(html):
    tokens = [(m.lastgroup, m.start(), m.end(), m.group(0)) for m in TOKEN.finditer(html)]
    segs = []
    covered = []  # (start,end) of text segments, to avoid overlapping attr segments

    chunk = []

    def flush():
        nonlocal chunk
        if not chunk:
            return
        toks = chunk
        chunk = []
        # trim whitespace-only text tokens at both ends
        while toks and toks[0][0] == 'text' and not toks[0][3].strip():
            toks = toks[1:]
        while toks and toks[-1][0] == 'text' and not toks[-1][3].strip():
            toks = toks[:-1]
        if not toks:
            return
        if not any(t[0] == 'text' and HANGUL.search(t[3]) for t in toks):
            return
        s, e = toks[0][1], toks[-1][2]
        raw = html[s:e]
        ls = len(raw) - len(raw.lstrip())
        rs = len(raw) - len(raw.rstrip())
        s += ls
        e -= rs
        segs.append({'kind': 'text', 'start': s, 'end': e, 'ko': html[s:e]})
        covered.append((s, e))

    for typ, s, e, tok in tokens:
        if typ == 'text':
            chunk.append((typ, s, e, tok))
        elif typ == 'tag':
            name = tag_name(tok)
            # the injected language switch must never merge into a neighbouring text run,
            # otherwise it changes that run's string and invalidates its translation
            if 'lang-switch' in tok:
                flush()
            elif name in INLINE:
                chunk.append((typ, s, e, tok))
            else:
                flush()
        else:
            flush()
    flush()

    def is_covered(pos):
        return any(a <= pos < b for a, b in covered)

    # attributes
    for typ, s, e, tok in tokens:
        if typ != 'tag' or is_covered(s):
            continue
        for m in re.finditer(r'\s(' + '|'.join(re.escape(a) for a in ATTRS) + r')\s*=\s*("([^"]*)"|\'([^\']*)\')', tok):
            val = m.group(3) if m.group(3) is not None else m.group(4)
            if HANGUL.search(val):
                vs = s + m.start(2) + 1
                segs.append({'kind': 'attr', 'attr': m.group(1), 'quote': m.group(2)[0], 'start': vs, 'end': vs + len(val), 'ko': val})

    # scripts
    for typ, s, e, tok in tokens:
        if typ != 'script':
            continue
        open_tag = re.match(r'<script\b[^>]*>', tok, re.S).group(0)
        if re.search(r'\bsrc\s*=', open_tag):
            continue
        body_start = s + len(open_tag)
        body = html[body_start: e - len(re.search(r'</script\s*>$', tok).group(0))]
        if 'ld+json' in open_tag:
            segs.extend(json_segments(body, body_start))
        else:
            segs.extend(js_segments(body, body_start, 'js'))

    segs.sort(key=lambda x: x['start'])
    # sanity: no overlaps
    last = -1
    for sg in segs:
        assert sg['start'] >= last, ('overlap', sg)
        last = sg['end']
    for i, sg in enumerate(segs):
        sg['id'] = i
    return segs


def extract_js_file(src):
    segs = js_segments(src, 0, 'jsfile')
    for i, sg in enumerate(segs):
        sg['id'] = i
    return segs


if __name__ == '__main__':
    path = sys.argv[1]
    src = open(path, encoding='utf-8').read()
    segs = extract_js_file(src) if path.endswith('.js') else extract_html(src)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    data = json.dumps(segs, ensure_ascii=False, indent=1)
    if out:
        open(out, 'w', encoding='utf-8').write(data)
        print(f'{path}: {len(segs)} segments, {sum(len(HANGUL.findall(s["ko"])) for s in segs)} hangul chars')
    else:
        print(data)
