#!/usr/bin/env python3
"""validate.py packets/pNN.json packets/pNN.out.json  -> prints problems, exit 1 if any."""
import json, re, sys
src = json.load(open(sys.argv[1], encoding='utf-8'))
try:
    out = json.load(open(sys.argv[2], encoding='utf-8'))
except Exception as e:
    print('INVALID JSON:', e); sys.exit(1)
TAG = re.compile(r'<[^>]+>')
probs = 0
missing = [k for k in src if k not in out or not isinstance(out.get(k), str) or not out[k].strip()]
if missing:
    print(f'MISSING {len(missing)} keys:', missing[:10]); probs += len(missing)
extra = [k for k in out if k not in src]
if extra:
    print(f'EXTRA keys:', extra[:10]); probs += len(extra)
for k, ko in src.items():
    en = out.get(k)
    if not isinstance(en, str):
        continue
    if re.search(r'[가-힣]', en):
        print(f'{k}: Korean left in output: {en[:80]!r}'); probs += 1
    t1, t2 = TAG.findall(ko), TAG.findall(en)
    if t1 != t2:
        # allow attribute text (alt/title) to differ; compare tag skeletons
        sk = lambda ts: [re.sub(r'\s(alt|title|placeholder|aria-label)="[^"]*"', '', t) for t in ts]
        if sk(t1) != sk(t2):
            print(f'{k}: TAG MISMATCH\n   ko: {t1}\n   en: {t2}'); probs += 1
    if ko.count('${') != en.count('${'):
        print(f'{k}: ${{}} placeholder count differs'); probs += 1
    if ko.count('\n') != en.count('\n') and abs(ko.count('\n') - en.count('\n')) > 2:
        print(f'{k}: newline count differs a lot ({ko.count(chr(10))} vs {en.count(chr(10))})'); probs += 1
print('OK' if not probs else f'{probs} problem(s)')
sys.exit(1 if probs else 0)
