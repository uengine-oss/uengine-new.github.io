#!/usr/bin/env python3
"""Batch driver.
  batch.py extract          -> seg/<page>.json for every in-scope page (+ js files)
  batch.py packets [N]      -> packets/pNN.json  (strings not yet in tm.json, grouped by page, ~N hangul chars each)
  batch.py merge            -> merge packets/pNN.out.json into tm.json
  batch.py apply            -> build en/ tree
  batch.py status           -> coverage report
"""
import os, sys, json, glob, re, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
# tools/en-edition/ lives two levels below the site root
ROOT = os.path.dirname(os.path.dirname(HERE))
SEG = os.path.join(HERE, 'seg'); PK = os.path.join(HERE, 'packets'); TM = os.path.join(HERE, 'tm.json')
os.makedirs(SEG, exist_ok=True); os.makedirs(PK, exist_ok=True)
HANGUL = re.compile(r'[가-힣]')
SKIP = {'contents/consultingMSAcopy.html', 'contents/supplychain-risk-before-edit.html',
        'contents/blog/supplychain-risk-before-edit.html', 'contents/vibeCodingRental.html', 'contents/openingSoon.html'}
JS_FILES = ['js/product-ontology.js', 'js/contact-form.js', 'js/register-form.js']


def pages():
    g = lambda pat: sorted(os.path.relpath(f, ROOT) for f in glob.glob(os.path.join(ROOT, pat)))
    ps = ['index.html'] + g('contents/*.html') + g('contents/blog/*.html') + g('contents/newsroom/*.html')
    return [p for p in ps if p not in SKIP]


def segfile(p):
    return os.path.join(SEG, p.replace('/', '__') + '.json')


def load_tm():
    return json.load(open(TM, encoding='utf-8')) if os.path.exists(TM) else {}


def cmd_extract():
    ex = os.path.join(HERE, 'extract.py')
    for p in pages() + JS_FILES:
        subprocess.run([sys.executable, ex, os.path.join(ROOT, p), segfile(p)], check=True)


def cmd_packets(target=9000):
    tm = load_tm()
    seen = set(tm)
    packets, cur, cur_n = [], {}, 0
    order = ['index.html'] + JS_FILES + [p for p in pages() if p != 'index.html']
    for p in order:
        segs = json.load(open(segfile(p), encoding='utf-8'))
        for s in segs:
            ko = s['ko']
            if ko in seen:
                continue
            seen.add(ko)
            n = len(HANGUL.findall(ko))
            if cur_n + n > target and cur:
                packets.append(cur); cur, cur_n = {}, 0
            cur[f'{len(packets):02d}-{len(cur):04d}'] = ko
            cur_n += n
    if cur:
        packets.append(cur)
    for f in glob.glob(os.path.join(PK, 'p*.json')):
        if not f.endswith('.out.json'):
            os.remove(f)
    for i, pk in enumerate(packets):
        json.dump(pk, open(os.path.join(PK, f'p{i:02d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'p{i:02d}.json  {len(pk)} strings  {sum(len(HANGUL.findall(v)) for v in pk.values())} hangul')


def cmd_merge():
    tm = load_tm()
    added = 0
    for f in sorted(glob.glob(os.path.join(PK, 'p*.out.json'))):
        src = json.load(open(f.replace('.out.json', '.json'), encoding='utf-8'))
        try:
            out = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('BAD JSON', f, e); continue
        for k, en in out.items():
            if k in src and isinstance(en, str) and en.strip():
                if src[k] not in tm:
                    added += 1
                tm[src[k]] = en
    json.dump(tm, open(TM, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'tm.json now {len(tm)} entries (+{added})')


def cmd_status():
    tm = load_tm()
    tot = miss = 0
    for p in pages() + JS_FILES:
        segs = json.load(open(segfile(p), encoding='utf-8'))
        m = [s for s in segs if s['ko'] not in tm]
        tot += len(segs); miss += len(m)
        if m:
            print(f'{p}: {len(m)}/{len(segs)} missing')
    print(f'TOTAL {tot} segments, {miss} missing')


def cmd_apply():
    spec = importlib.util.spec_from_file_location('ap', os.path.join(HERE, 'apply.py'))
    ap = importlib.util.module_from_spec(spec); spec.loader.exec_module(ap)
    ap.SITE_ROOT = ROOT  # so English screenshots under images/en/ are picked up
    tm = load_tm()
    bad = 0
    for p in pages():
        src = open(os.path.join(ROOT, p), encoding='utf-8').read()
        segs = json.load(open(segfile(p), encoding='utf-8'))
        s, missing, ns = ap.build(p, src, segs, tm)
        out = os.path.join(ROOT, 'en', p)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        if missing or ns[0] == 0:
            bad += 1
            print(f'{p}: missing={len(missing)} switch={ns}')
    for js in JS_FILES:
        src = open(os.path.join(ROOT, js), encoding='utf-8').read()
        segs = json.load(open(segfile(js), encoding='utf-8'))
        missing = []
        s = ap.splice(src, segs, tm, missing)
        out = os.path.join(ROOT, js.replace('js/', 'js/en/'))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        if missing:
            print(f'{js}: missing={len(missing)}')
    print('apply done; pages with issues:', bad)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'extract': cmd_extract()
    elif c == 'packets': cmd_packets(int(sys.argv[2]) if len(sys.argv) > 2 else 9000)
    elif c == 'merge': cmd_merge()
    elif c == 'status': cmd_status()
    elif c == 'apply': cmd_apply()
