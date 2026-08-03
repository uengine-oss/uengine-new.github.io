#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LCP 후보 이미지 → WebP 변환기 (Core Web Vitals 개선용).

무엇을 대상으로 하나
  지연 로딩(loading="lazy")이 아닌 본문 이미지 = 화면에 바로 보이는 히어로/상단 이미지.
  이것들만 LCP(Largest Contentful Paint)에 잡히고, LCP 만 랭킹 신호(Core Web Vitals)에 들어간다.
  스크롤 아래 이미지는 이미 지연 로딩되므로 변환해도 SEO 이득이 없다.

원본은 지우지 않는다
  · 참조를 하나 놓쳐도 원본이 남아 있어 깨지지 않는다 (안전한 실패).
  · og:image 는 일부 링크 프리뷰 크롤러(카카오톡 등)가 WebP 를 못 읽어
    원본 PNG/JPEG 를 계속 써야 한다. apply_seo.py 의 social_safe() 가 이를 처리한다.

사용법
  python3 .claude/skills/seo-optimize/convert_webp.py            # 검사만 (변환 대상 목록)
  python3 .claude/skills/seo-optimize/convert_webp.py --apply    # 변환 + HTML 참조 갱신
  python3 .claude/skills/seo-optimize/convert_webp.py --apply --min-kb 150 --quality 90

변환 후에는 반드시 apply_seo.py 를 실행해 og:image 를 재계산할 것.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# 변환해도 의미 없거나 건드리면 안 되는 것
SKIP = re.compile(r"(favicon|logo|\.svg$|\.gif$)", re.I)


def pages() -> list[str]:
    out = ["index.html"]
    for pat in ("contents/*.html", "contents/blog/*.html", "contents/newsroom/*.html"):
        out += [os.path.relpath(p, ROOT).replace(os.sep, "/") for p in glob.glob(os.path.join(ROOT, pat))]
    return sorted(set(out))


def find_targets(min_bytes: int) -> dict[str, list[str]]:
    """지연 로딩이 아닌 본문 로컬 이미지 중 min_bytes 이상인 것 → 참조 페이지 목록."""
    found: dict[str, list[str]] = {}
    for page in pages():
        src = open(os.path.join(ROOT, page), encoding="utf-8").read()
        m = re.search(r"<main\b", src)
        body = src[m.start():] if m else src

        refs = []
        for tag in re.findall(r"<img\b[^>]*>", body):
            if 'loading="lazy"' in tag:
                continue
            u = re.search(r'src="([^"]+)"', tag)
            if u:
                refs.append(u.group(1))
        # 히어로 섹션의 CSS 배경도 LCP 요소가 될 수 있다
        for m2 in re.finditer(r'(?:data-bg-src|background-image:\s*url\()["\']?((?:\.\./)*images/[^"\')\s]+)',
                              body[:20000]):
            refs.append(m2.group(1))

        for u in refs:
            if u.startswith(("http", "data:")):
                continue
            rel = re.sub(r"^(\.\./)+", "", u)
            if SKIP.search(rel) or rel.lower().endswith(".webp"):
                continue
            full = os.path.join(ROOT, rel)
            if os.path.exists(full) and os.path.getsize(full) >= min_bytes:
                found.setdefault(rel, []).append(page)
    return found


def convert(targets: list[str], quality: int) -> list[tuple[str, str, int, int]]:
    from PIL import Image
    done = []
    for rel in targets:
        src = os.path.join(ROOT, rel)
        dst_rel = os.path.splitext(rel)[0] + ".webp"
        dst = os.path.join(ROOT, dst_rel)
        try:
            im = Image.open(src)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if ("A" in im.mode or im.mode == "P") else "RGB")
            im.save(dst, "WEBP", quality=quality, method=6)
        except Exception as e:                                   # noqa: BLE001
            print(f"  건너뜀 {rel} — {e}")
            continue
        b, a = os.path.getsize(src), os.path.getsize(dst)
        if a >= b:                       # 이미 최적화된 JPEG 등은 WebP 가 더 클 수 있다
            os.remove(dst)
            print(f"  건너뜀 {rel} — WebP 가 더 큼 ({a:,} >= {b:,})")
            continue
        done.append((rel, dst_rel, b, a))
    return done


def rewrite_refs(done: list[tuple[str, str, int, int]]) -> tuple[int, int]:
    # 부분문자열 오치환 방지
    names = [d[0] for d in done]
    for a in names:
        for b in names:
            if a != b and a in b:
                sys.exit(f"경로 충돌로 중단: {a} ⊂ {b}")
    files = hits = 0
    for page in pages():
        p = os.path.join(ROOT, page)
        s = o = open(p, encoding="utf-8").read()
        for src_rel, dst_rel, _, _ in done:
            if src_rel in s:
                hits += s.count(src_rel)
                s = s.replace(src_rel, dst_rel)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            files += 1
    return files, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제로 변환하고 HTML 참조를 갱신")
    ap.add_argument("--min-kb", type=int, default=80, help="이 크기 이상만 대상 (기본 80KB)")
    ap.add_argument("--quality", type=int, default=90, help="WebP 품질 (기본 90)")
    args = ap.parse_args()

    targets = find_targets(args.min_kb * 1024)
    if not targets:
        print(f"[webp] {args.min_kb}KB 이상인 LCP 후보 이미지가 없습니다. 할 일 없음.")
        return 0

    total = sum(os.path.getsize(os.path.join(ROOT, t)) for t in targets)
    print(f"[webp] 대상 {len(targets)}개, 합계 {total:,} bytes")
    for rel, refs in sorted(targets.items(), key=lambda kv: -os.path.getsize(os.path.join(ROOT, kv[0]))):
        print(f"  {os.path.getsize(os.path.join(ROOT, rel)):>9,}  {rel}  ({len(refs)}개 페이지)")

    if not args.apply:
        print("\n검사 모드입니다. 실제로 바꾸려면 --apply 를 붙이세요.")
        return 0

    done = convert(sorted(targets), args.quality)
    if not done:
        print("[webp] 변환된 파일이 없습니다.")
        return 0
    files, hits = rewrite_refs(done)
    b = sum(d[2] for d in done)
    a = sum(d[3] for d in done)
    print(f"\n[webp] 변환 {len(done)}개 — {b:,} → {a:,} bytes "
          f"(-{(1 - a / b) * 100:.1f}%, {(b - a) / 1024 / 1024:.1f}MB 절감)")
    print(f"[webp] HTML 참조 갱신 — {files}개 파일, {hits}건")
    print("\n다음: python3 .claude/skills/seo-optimize/apply_seo.py  (og:image 재계산 — 필수)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
