#!/usr/bin/env python3
"""
compose-splash.py — 메인 스플래시용 제품 이미지 합성기.

다른 스플래시 슬라이드(Process GPT, Robo Modernizer 등)와 동일한 룩:
캡처 2장을 대각선으로 겹치고, 각 패널에 보라빛 라운드 테두리 + 드롭섀도우를 입혀
투명 배경 PNG로 저장한다. (main-slide-img > img 는 CSS 테두리가 없으므로
이 테두리/겹침은 이미지에 구워 넣어야 한다.)

사용:
  python3 compose-splash.py OUT.png BACK.jpg FRONT.jpg [--crop-top N] [--crop-bottom N]

  OUT   : 저장 경로 (예: images/full-width-images/main-img-<slug>.png)
  BACK  : 뒤(우상단)에 놓일 캡처 — 보통 제품 UI/목록 화면
  FRONT : 앞(좌하단)에 놓일 캡처 — 보통 색감이 강한 캔버스/그래프 화면
  --crop-top/--crop-bottom : 브라우저 크롬(주소창)·macOS Dock 등 잘라낼 픽셀

권장: 두 캡처는 서로 다른 화면(리스트 UI vs 컬러풀한 캔버스)으로 골라 대비를 준다.
"""
import sys, argparse
from PIL import Image, ImageDraw, ImageFilter

PURPLE = (124, 92, 255, 255)   # 보라빛 테두리
RADIUS = 22
BORDER = 6
PANEL_W = 770                   # 각 패널 폭(px)

def rounded(img, r):
    img = img.convert('RGBA')
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=r, fill=255)
    img.putalpha(m)
    return img

def bordered(path, w, crop_top=0, crop_bottom=0):
    im = Image.open(path).convert('RGB')
    if crop_top or crop_bottom:
        im = im.crop((0, crop_top, im.width, im.height - crop_bottom))
    h = int(im.height * w / im.width)
    im = rounded(im.resize((w, h), Image.LANCZOS), RADIUS)
    bw, bh = w + 2*BORDER, h + 2*BORDER
    c = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle([0, 0, bw-1, bh-1], radius=RADIUS+BORDER, fill=PURPLE)
    c.alpha_composite(im, (BORDER, BORDER))
    return c

def shadow(panel, pad=46, blur=26, alpha=110, dy=16):
    c = Image.new('RGBA', (panel.size[0]+2*pad, panel.size[1]+2*pad), (0, 0, 0, 0))
    a = panel.split()[3]
    solid = Image.new('RGBA', panel.size, (30, 15, 70, alpha))
    solid.putalpha(a.point(lambda p: int(p*alpha/255)))
    sl = Image.new('RGBA', c.size, (0, 0, 0, 0))
    sl.alpha_composite(solid, (pad, pad+dy))
    c.alpha_composite(sl.filter(ImageFilter.GaussianBlur(blur)))
    c.alpha_composite(panel, (pad, pad))
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('back'); ap.add_argument('front')
    ap.add_argument('--crop-top', type=int, default=0)
    ap.add_argument('--crop-bottom', type=int, default=0)
    a = ap.parse_args()
    back  = shadow(bordered(a.back,  PANEL_W, a.crop_top, a.crop_bottom))
    front = shadow(bordered(a.front, PANEL_W, a.crop_top, a.crop_bottom))
    CW, CH = 1120, 860
    out = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    out.alpha_composite(back,  (CW - back.size[0] + 10, 0))     # 뒤: 우상단
    out.alpha_composite(front, (-30, CH - front.size[1]))       # 앞: 좌하단
    out.save(a.out)
    print('saved', a.out, out.size)

if __name__ == '__main__':
    main()
