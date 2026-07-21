#!/usr/bin/env python3
"""Replace the NotebookLM watermark in the bottom-right corner of a NotebookLM
"Slides"/Infographic PNG export with the uEngine logo.

The watermark sits at a fixed pixel position (template chrome, not page
content) as long as every page was rendered at the same resolution -- e.g.
via `pdftoppm -png -r 100 deck.pdf out-page`. Default box below was measured
on a 1912x1067 render (100 DPI) of a 14-page NotebookLM export; pass
--box left,top,right,bottom if your render resolution differs.

Usage:
    python3 debrand-slide.py <input.png> <uengine_logo.png> <output.png> \
        [--box 1758,1032,1902,1059] [--logo-h 22]
"""
import argparse
from PIL import Image


def median_color(pixels):
    rs = sorted(p[0] for p in pixels)
    gs = sorted(p[1] for p in pixels)
    bs = sorted(p[2] for p in pixels)
    n = len(pixels)
    return (rs[n // 2], gs[n // 2], bs[n // 2])


def debrand(src_path, logo_path, out_path, box, logo_h=None, pad=5):
    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad

    # Sample local background from a strip just above the watermark box
    # (still inside the slide's flat corner margin) so each page's own
    # background shade (cream / light-gray / white) is matched.
    strip_y = max(0, y0 - 8)
    bg = median_color([im.getpixel((x, strip_y)) for x in range(x0, x1, 3)])

    cover = Image.new("RGB", (x1 - x0, y1 - y0), bg)
    im.paste(cover, (x0, y0))

    logo = Image.open(logo_path).convert("RGBA")
    target_h = logo_h or (y1 - y0 - 2 * pad)
    scale = target_h / logo.size[1]
    target_w = int(logo.size[0] * scale)
    logo = logo.resize((target_w, target_h), Image.LANCZOS)

    lx = x1 - pad - target_w
    ly = y0 + (y1 - y0 - target_h) // 2

    im = im.convert("RGBA")
    im.alpha_composite(logo, (lx, ly))
    im = im.convert("RGB")
    im.save(out_path)
    print(f"  {src_path} -> {out_path}  (bg={bg}, logo@({lx},{ly}) {target_w}x{target_h})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("logo")
    ap.add_argument("out")
    ap.add_argument("--box", default="1758,1032,1902,1059",
                     help="left,top,right,bottom of the watermark, unpadded")
    ap.add_argument("--logo-h", type=int, default=22)
    ap.add_argument("--pad", type=int, default=5)
    args = ap.parse_args()
    box = tuple(int(v) for v in args.box.split(","))
    debrand(args.src, args.logo, args.out, box, args.logo_h, args.pad)
