#!/usr/bin/env python3
"""Showcase 무음 클립 — Ontological Studio 시연 녹화의 프레임(capture/)을 장면 순서대로 이어 짧은 mp4 로.

시연 영상(나레이션·자막 있음)과 같은 실제 실행 화면이지만, showcase 는 글자를 따로 얹으므로 자막 없이 만든다.
장면마다 정해 둔 초를 그 장면의 프레임 수로 나눠 보여 준다(구축처럼 프레임이 많은 장면은 타임랩스가 된다).

    python3 tools/showcase/os_clips.py            # 한국어 → images/showcase/, 영어(capture-en) → images/en/showcase/
"""
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

DEMO = Path("/Users/uengine/uengine-platform/ontology-studio-desktop/demo")
SITE = Path(__file__).resolve().parents[2]
W, H = 1600, 900

# 클립 이름 → (시연 폴더, [(장면 번호, 초)], 포스터로 쓸 장면)
CLIPS = {
    "os-build": ("doc-build-ask", [(3, 1.2), (4, 1.6), (5, 1.0), (6, 2.6), (7, 2.6), (9, 2.4)], 9),
    "os-golden": ("golden-command-action", [(5, 1.2), (6, 2.2), (7, 2.2), (8, 1.4), (10, 1.6), (11, 1.6), (12, 1.6)], 10),
    "os-app": ("ontology-app", [(3, 1.4), (4, 1.2), (5, 1.6), (6, 1.6), (9, 2.0), (10, 1.8), (11, 1.4)], 10),
    "os-app-action": ("app-actions", [(6, 1.4), (7, 1.6), (8, 1.8), (12, 1.4), (13, 1.6), (14, 1.6), (15, 1.4)], 8),
}


def window(cap, frame):
    if frame.get("tab"):
        strip = Image.open(cap / frame["strip"]).convert("RGB")
        tab = Image.open(cap / frame["tab"]).convert("RGB")
        win = Image.new("RGB", (strip.width, strip.height + tab.height))
        win.paste(strip, (0, 0))
        win.paste(tab, (0, strip.height))
    else:
        win = Image.open(cap / frame["full"]).convert("RGB")
    return win.resize((W, H), Image.LANCZOS)


def scene_frames(frames, scene):
    return frames[str(scene)]["frames"]


def build(name, folder, plan, poster_scene, lang):
    cap = DEMO / folder / ("capture-en" if lang == "en" else "capture")
    frames = json.loads((cap / "frames.json").read_text())
    out_dir = SITE / "images" / ("en/showcase" if lang == "en" else "showcase")
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        lines, n = [], 0
        for scene, sec in plan:
            fs = scene_frames(frames, scene)
            for f in fs:
                n += 1
                p = tmp / f"{n:04d}.png"
                window(cap, f).save(p)
                lines += [f"file '{p}'", f"duration {sec / len(fs):.3f}"]
        lines.append(f"file '{p}'")  # concat 은 마지막 항목의 duration 을 쓰려면 한 번 더 적어야 한다
        (tmp / "list.txt").write_text("\n".join(lines) + "\n")
        mp4 = out_dir / f"{name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                        "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
                        "-movflags", "+faststart", "-an", str(mp4)], check=True)
    pf = scene_frames(frames, poster_scene)[-1]
    window(cap, pf).save(out_dir / f"{name}-poster.webp", quality=82, method=6)
    print(lang, name, f"{sum(s for _, s in plan):.1f}s", f"{mp4.stat().st_size / 1e6:.2f}MB")


if __name__ == "__main__":
    for lang in ("ko", "en"):
        for name, (folder, plan, poster) in CLIPS.items():
            build(name, folder, plan, poster, lang)
