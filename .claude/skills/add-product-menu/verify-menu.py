#!/usr/bin/env python3
"""메뉴 추가 후 Playwright 로 실제 메뉴를 열어 검증한다.

add-product-menu / 메뉴를 건드리는 모든 작업의 마지막 단계에서 실행한다.
정적 서버가 떠 있어야 한다:  python3 -m http.server 8123 --bind 127.0.0.1 &

사용:
  python3 .claude/skills/add-product-menu/verify-menu.py \
      --menu "AI-Native Enterprise" --label "Ontology Studio" \
      --path contents/ontologystudio.html [--base http://127.0.0.1:8123] \
      [--headed] [--out <스크린샷 디렉토리>]

하는 일:
  1. index.html 에서 상단 대메뉴에 hover → 서브메뉴가 실제로 열리는지 확인
  2. 열린 서브메뉴 안에 신규 라벨이 보이는지(visible) 확인 + 스크린샷
  3. 그 링크를 클릭해 실제로 제품 페이지로 이동하는지, <h1>/<title> 이 맞는지 확인
  4. 푸터에도 같은 라벨의 링크가 있는지 확인
  5. 콘솔 에러 / 404 리소스 수집
종료코드 0 = 전부 통과. 실패 항목은 stderr 로 출력한다.
"""
import argparse
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

fails: list[str] = []
notes: list[str] = []


def check(ok: bool, msg: str) -> bool:
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok:
        fails.append(msg)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8123")
    ap.add_argument("--menu", required=True, help="상단 대메뉴 라벨 (예: AI-Native Enterprise)")
    ap.add_argument("--label", required=True, help="새로 추가한 메뉴 항목 라벨 (예: Ontology Studio)")
    ap.add_argument("--path", required=True, help="제품 페이지 경로 (예: contents/ontologystudio.html)")
    ap.add_argument("--out", default="/tmp/verify-menu")
    ap.add_argument("--headed", action="store_true", help="브라우저를 눈에 보이게 띄운다")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not a.headed)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}")
                if m.type == "error" else None)
        page.on("response", lambda r: errors.append(f"HTTP {r.status} {r.url}")
                if r.status >= 400 else None)

        # 1. 홈에서 대메뉴 hover
        page.goto(f"{a.base}/index.html", wait_until="load")
        page.wait_for_timeout(1200)
        top = page.locator("nav a.mn-has-sub", has_text=re.compile(re.escape(a.menu))).first
        if not check(top.count() > 0, f"상단 대메뉴 '{a.menu}' 존재"):
            browser.close()
            return report()
        top.hover()
        page.wait_for_timeout(700)

        # 2. 열린 서브메뉴 안에서 신규 라벨이 보이는지
        item = top.locator("xpath=ancestor::li[1]").locator(
            "a", has_text=re.compile(rf"^\s*{re.escape(a.label)}\s*$"))
        check(item.count() > 0, f"서브메뉴에 '{a.label}' 링크 존재")
        visible = item.count() > 0 and item.first.is_visible()
        check(visible, f"hover 시 '{a.label}' 이 실제로 화면에 보임 (메가메뉴 펼침)")
        page.screenshot(path=str(out / "01-menu-open.png"))

        href = item.first.get_attribute("href") if item.count() else None
        check(href == a.path, f"메뉴 링크 경로 = {a.path} (실제: {href})")

        # 3. 클릭해서 이동 확인
        if visible:
            item.first.click()
            page.wait_for_load_state("load")
            page.wait_for_timeout(800)
            check(a.path in page.url, f"클릭 시 {a.path} 로 이동 (실제: {page.url})")
        else:
            page.goto(f"{a.base}/{a.path}", wait_until="load")
            page.wait_for_timeout(800)

        h1 = page.locator("h1")
        check(h1.count() == 1, f"제품 페이지 <h1> 정확히 1개 (실제: {h1.count()})")
        if h1.count():
            notes.append(f"h1 = {h1.first.inner_text().strip()!r}")
        notes.append(f"title = {page.title()!r}")

        # 4. 푸터 링크
        page.mouse.wheel(0, 200000)
        page.wait_for_timeout(900)
        foot = page.locator("footer a, .fw-menu a", has_text=re.compile(re.escape(a.label)))
        check(foot.count() > 0, f"푸터에 '{a.label}' 링크 존재")
        page.screenshot(path=str(out / "02-product-footer.png"))
        page.screenshot(path=str(out / "03-product-full.png"), full_page=True)

        # 5. 제품 페이지에서도 대메뉴가 같은 항목을 갖는지 (nav 복제 누락 탐지)
        page.mouse.wheel(0, -200000)
        page.wait_for_timeout(600)
        top2 = page.locator("nav a.mn-has-sub", has_text=re.compile(re.escape(a.menu))).first
        if top2.count():
            top2.hover()
            page.wait_for_timeout(600)
            item2 = top2.locator("xpath=ancestor::li[1]").locator(
                "a", has_text=re.compile(rf"^\s*{re.escape(a.label)}\s*$"))
            check(item2.count() > 0, f"제품 페이지 nav 에도 '{a.label}' 반영됨")
        else:
            check(False, f"제품 페이지에 대메뉴 '{a.menu}' 없음")

        browser.close()

    hard = [e for e in errors if not e.startswith("HTTP 4") or "favicon" not in e]
    if hard:
        print("\n[리소스/콘솔 이슈]")
        for e in dict.fromkeys(hard):
            print("  - " + e)
    return report()


def report() -> int:
    for n in notes:
        print("  info  " + n)
    if fails:
        print(f"\n실패 {len(fails)}건:", file=sys.stderr)
        for f in fails:
            print("  - " + f, file=sys.stderr)
        return 1
    print("\n메뉴 검증 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
