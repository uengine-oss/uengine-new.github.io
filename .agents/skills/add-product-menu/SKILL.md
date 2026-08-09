---
name: add-product-menu
description: 유엔진 홈페이지(uengine-new.github.io)에 유튜브 데모 영상 하나만 주면 신규 제품/메뉴를 자동으로 추가합니다. 영상 트랜스크립트로 기능을 추출하고, 영상에서 핵심 화면을 캡처하며, roboarchitect.html 템플릿 기반의 상세 페이지를 생성하고, 전체 페이지의 상단 네비/푸터 메뉴와 메인 스플래시 슬라이드까지 일괄 반영합니다. "유튜브로 메뉴 추가", "새 제품 페이지 만들어", "홈페이지에 메뉴 추가", "이 영상으로 제품 페이지", "/add-product-menu", "제품 메뉴 신설", "스플래시에 추가" 등의 표현이 있을 때 트리거.
---

# add-product-menu — 유튜브 영상 → 홈페이지 제품 메뉴 자동 추가

유엔진 홈페이지(정적 HTML, `index.html` + `contents/*.html`)에 신규 제품을 추가하는
전 과정을 자동화한다. 사용자가 **유튜브 데모 URL** 하나만 주면 나머지를 알아서 채운다.

## 대상 리포지토리
- 루트: 홈페이지 프로젝트 루트 (`index.html`, `contents/`, `images/` 존재)
- 템플릿: `contents/roboarchitect.html` (제품 상세 페이지 표준 레이아웃)
- 모든 페이지(`index.html` + `contents/*.html`)는 **각자 nav/footer를 하드코딩**으로 복제한다.
  → 메뉴 변경은 전체 파일에 일괄 반영해야 한다.

## 입력 (없으면 AskUserQuestion 으로 확인)
1. **유튜브 URL** (필수) — 데모/소개 영상. 영상 대신 **doc-inbox/의 NotebookLM류 워터마크 PDF**
   (슬라이드/인포그래픽)가 소스로 주어지면, `doc-inbox-rebrand` 스킬로 워터마크를 uEngine 로고로
   교체한 아키텍처/다이어그램 이미지를 만든 뒤 2~3단계의 스크린샷 대신 사용한다.
2. **제품명** (예: `Ontology Studio`) — 페이지 제목/메뉴 라벨/파일 slug의 근거
3. **파일 slug** (예: `ontologystudio`) → `contents/<slug>.html`, `images/<slug>/`
4. **외부 링크** — GitHub 또는 제품 사이트 (헤더/CTA 버튼 및 설명 소스)
5. **배치 위치** 둘 중 하나:
   - (A) 기존 top-level 메뉴의 `<Products>` 밑에 제품 링크 추가
   - (B) **신규 top-level 메뉴 신설** (예: `Ontology`) — Ontology 추가 때 했던 방식
6. **한 줄 한국어 소개** (스플래시/헤더용) — 없으면 트랜스크립트/README로 초안 작성 후 확인

## 사전 도구 확인
```bash
which yt-dlp ffmpeg   # 둘 다 필요. 없으면: brew install yt-dlp ffmpeg
```

---

## 절차

### 0. doc-inbox 자동 스캔 (다운로드 첨부 자료)
작업 시작 전 `doc-inbox/`(단 `doc-inbox/logo/`는 로고 자산이므로 제외)에 처리 안 된 파일이
있는지 항상 먼저 확인한다:
```bash
find doc-inbox -maxdepth 1 -type f
```
파일이 있으면 두 갈래로 나눠 처리한다:
- **워터마크 슬라이드(NotebookLM 등 내보내기)** — 표지 등 한 페이지를 렌더링해 우하단에
  외부 워터마크가 보이면 `doc-inbox-rebrand` 스킬로 로고를 uEngine 것으로 교체한 뒤, 결과
  이미지를 상세 페이지에 반영한다(2~3단계의 스크린샷 대신 사용).
- **그대로 배포 가능한 자료(강의자료·백서·소개서 등 자체 저작물)** — 워터마크가 없으면
  로고 처리 없이 원본 그대로 `images/`에 복사해 "자료(PDF) 다운로드" 버튼으로 상세 페이지에
  연결한다. 파일명은 `images/<Product-Name>-<구분>.pdf` 형태의 ASCII로 통일한다
  (`processgpt.html`의 "소개서(PDF) 다운로드" 버튼 패턴 참고).

두 경우 모두, **페이지·nav/footer 반영이 끝나고 6단계(로컬 서버 렌더 검증)까지 통과한 뒤**
`doc-inbox/`의 원본 파일(로고 제외)을 삭제한다. 확인 절차 없이 자동으로 지운다 —
doc-inbox는 임시 수신함이므로 반영이 끝난 원본을 남겨둘 이유가 없다. 단, 반영/검증에
실패했거나 결과가 불확실하면 삭제하지 않고 사용자에게 알린다.

### 1. 자료 수집 (병렬)
- `WebFetch` 로 GitHub/사이트 README → 제품 설명·핵심 기능·YouTube 링크 확인
- 스크래치패드에서 트랜스크립트 다운로드:
```bash
cd <SCRATCH>/onto && \
yt-dlp --write-auto-subs --write-subs --sub-langs "ko,en" --skip-download \
  --sub-format vtt -o "onto.%(ext)s" "<YOUTUBE_URL>"
```
- VTT → 타임스탬프 텍스트 정리 (auto-sub 롤링 중복 제거):
```bash
python3 - <<'EOF'
import re
lines=open('onto.ko.vtt',encoding='utf-8').read().splitlines()
out=[];last=None;t=None
for l in lines:
    m=re.match(r'(\d\d:\d\d:\d\d)\.\d+ -->',l)
    if m: t=m.group(1); continue
    if not l.strip() or l.startswith(('WEBVTT','Kind:','Language:')): continue
    x=re.sub(r'<[^>]+>','',l).strip()
    if x and x!=last: out.append((t,x)); last=x
for t,x in out: print(t,x)
EOF
```
- 트랜스크립트를 읽고 **핵심 기능 5~6개**와 각 기능이 **화면에 보이는 타임스탬프**를 정리한다.

### 2. 스크린샷 추출
```bash
yt-dlp -f "best[height<=720]" --no-update -o "video.%(ext)s" "<YOUTUBE_URL>"
mkdir -p frames
for t in 00:00:06 00:01:05 00:03:14 ... ; do   # 1단계에서 고른 타임스탬프들
  fn=$(echo $t|tr ':' '-'); ffmpeg -loglevel error -ss $t -i video.mp4 -frames:v 1 -q:v 3 "frames/f_$fn.jpg" -y
done
```
- 추출한 프레임을 `Read` 로 직접 보고 **가장 잘 나온 컷들**을 고른다(전환 중/모션블러 프레임 제외; 필요시 ±1~2초 재추출).
  기능이 많으면 **캡처 10~12장**까지 늘려도 좋다(기능 카드 한 장에 하나씩).
- 선정본을 기능 카드용으로 복사한다. 브라우저 크롬(macOS 메뉴바·주소창)과 하단 Dock 은
  `ffmpeg crop` 으로 잘라내 앱 화면만 남긴다(예: 상단 82px 제거, Dock 있으면 하단도):
```bash
mkdir -p images/<slug>
ffmpeg -loglevel error -i frames/f_XXX.jpg -vf "crop=1114:638:0:82" images/<slug>/<slug>-기능명.jpg -y
```
- **스플래시용 png 는 단순 복사가 아니라 “2장 겹침 + 보라빛 라운드 테두리”로 합성한다.**
  다른 슬라이드(Process GPT·Robo Modernizer 등)와 동일한 룩이며, `main-slide-img > img` 에는
  CSS 테두리가 없으므로 **테두리/겹침은 PNG 에 구워 넣어야 한다.** 헬퍼 스크립트 사용:
```bash
# BACK = 제품 UI/목록 화면, FRONT = 색감이 강한 캔버스/그래프 화면(대비되게)
python3 .claude/skills/add-product-menu/compose-splash.py \
  images/full-width-images/main-img-<slug>.png \
  images/<slug>/<back>.jpg images/<slug>/<front>.jpg [--crop-top 30] [--crop-bottom 38]
```
  결과: 투명 배경 1120×860 PNG(우상단·좌하단 대각선 겹침, 보라 테두리 #7C5CFF, 드롭섀도우).
  `Read` 로 확인해 Dock/크롬이 남으면 `--crop-top/--crop-bottom` 을 조정한다.

### 3. 제품 상세 페이지 생성
```bash
cp contents/roboarchitect.html contents/<slug>.html
```
그다음 다음을 교체한다:
- `<title>` / `<meta name="description">` → 제품 내용
- `<main id="main"> … </main>` 전체를 새 콘텐츠로 교체 (아래 구조 유지)
- 문의 폼 `<input type="hidden" name="classification" value="RoboArchitect">` → 제품명

**main 구조(템플릿과 동일 클래스 재사용):**
1. Header Section — `hs-title-1` 제품명 + 버튼(GitHub/영상 링크)
2. About Section — `.video-box > iframe src="https://www.youtube.com/embed/<VIDEO_ID>"` + 소개 문단
3. 주요 기능 — `feature-card` 그리드. **각 카드 상단에 `images/<slug>/*.jpg` 캡처**를 넣고
   (`padding:0 0 30px; overflow:hidden`, `img width:100%`), 아래 제목·설명·체크 불릿(`feature-item`) 3개
4. 동작 방식 — `features-2-item` 4단계
5. 비교표 — `tbl-default` (해당 제품의 차별점)
6. Call Action — CTA 버튼(GitHub/영상)
7. Contact — 템플릿 폼 그대로, `classification` 값만 변경

main 교체는 파이썬 슬라이스로 안전하게:
```python
s=open(f).read(); i=s.index('            <main id="main">'); j=s.index('</main>')+len('</main>')
s=s[:i]+open('newmain.html').read().rstrip('\n')+s[j:]; open(f,'w').write(s)
```
> 주의: `roboarchitect.html`을 복사하면 nav/footer는 이미 최신 상태. 새 제품 메뉴 항목은 4단계에서 전체 파일에 일괄 삽입되므로 이 파일도 포함된다.

### 4. 전체 페이지 nav + footer 일괄 반영
`index.html` 은 링크 경로 접두사 `contents/`, `contents/*.html` 은 접두사 없음.

**(B) 신규 top-level 메뉴 신설** — About 메뉴 앞에 삽입. 앵커(28/32스페이스, 전 파일 공통):
```
                            <!-- Item With Sub -->
                            <li>
                                <a href="#" class="mn-has-sub active">About
```
이 앵커 문자열 앞에 신규 `<li>…megamenu…</li>` 블록을 끼워 넣는다. 푸터는
`<h3 class="fw-title">About</h3>` 위젯 바로 앞(`<!-- Footer Widget -->`)에 신규 컬럼을 삽입하고,
5열이 되면 Insights 컬럼을 `col-sm-3`→`col-sm-2`로 줄여 합계 12를 맞춘다(SDD3+BPM3+신규2+About2+Insights2).

**(A) 기존 메뉴에 제품만 추가** — 해당 메뉴 `<Products>` `<ul>` 안에 `<li><a href="{P}<slug>.html">제품명</a></li>` 한 줄 추가. 푸터도 같은 위젯의 `<ul class="fw-menu clearlist">` 에 동일 링크 추가.

**일괄 처리 스크립트 골격** (파일별 접두사 처리 + 앵커 존재 검증):
```python
import glob
files=glob.glob('contents/*.html')+['index.html']
NAV_ABOUT='                            <!-- Item With Sub -->\n                            <li>\n                                <a href="#" class="mn-has-sub active">About'
def block(P): return f'''<Ontology-style megamenu 문자열, {P}<slug>.html 링크 포함>'''
for f in files:
    P='contents/' if f=='index.html' else ''
    s=open(f,encoding='utf-8').read()
    assert NAV_ABOUT in s, f  # 앵커 검증
    s=s.replace(NAV_ABOUT, block(P)+NAV_ABOUT, 1)
    if '<h3 class="fw-title">About</h3>' in s:   # openingSoon.html 처럼 푸터 없는 페이지는 건너뜀
        pos=s.index('<h3 class="fw-title">About</h3>'); fw=s.rindex('<!-- Footer Widget -->',0,pos)
        s=s[:fw]+footer_block(P)+s[fw:]
        # (신규 top-level일 때만) Insights col-sm-3 -> col-sm-2
    open(f,'w',encoding='utf-8').write(s)
```
> **중요(부분쓰기 방지):** 루프 도중 `assert`/`index` 실패로 일부 파일만 저장되면 리포가 반쯤 바뀐다.
> 먼저 전 파일에 대해 앵커 존재를 검사한 뒤 쓰거나, 실패 시 `git checkout -- index.html contents/*.html` 로 되돌리고 스크립트를 고쳐 재실행한다.
> `contents/openingSoon.html` 은 nav만 있고 footer 위젯이 없으니 footer 단계는 조건부로 건너뛴다.

### 5. 메인 스플래시 슬라이드 추가 (index.html)
`<!-- Fullwidth Slider -->` 컨테이너 안, 첫 슬라이드로 삽입(가장 먼저 노출). 기존 슬라이드
(`<!-- Slide Item - process gpt -->`)와 동일 구조:
- `main-slide-img > img src="images/full-width-images/main-img-<slug>.png" class="wow scaleOutIn"`
  → 이미지는 2단계에서 `compose-splash.py` 로 만든 **보라빛 라운드 테두리 + 2장 겹침** PNG 여야 한다.
    단순 화면 캡처 1장을 그대로 넣지 말 것(테두리가 안 들어가 다른 슬라이드와 튄다).
  → `scaleOutIn` 클래스가 있어야 다른 슬라이드처럼 등장 애니메이션이 붙는다.
- `hs-title-11` = 카테고리(신규 메뉴명 또는 기존 카테고리)
- `hs-title-12 > span.owl-animate-chars` = 제품명
- `hs-title-11i` = 한 줄 한국어 소개
- `Learn More` → `contents/<slug>.html`

### 6. SEO 메타 등록 — **필수**
제품 페이지는 목록 카드가 없으므로 **레지스트리에 직접 써야 한다.** 안 쓰면 본문에서 유추한
빈약한 메타가 붙는다. `.claude/skills/seo-optimize/seo-meta.json` 의 `pages` 에 추가:

```jsonc
"contents/<slug>.html": {
  "title": "제품명 — 한 줄 가치제안",        // 70자 이내. " | uEngine" 접미사는 자동
  "description": "무엇을 하는 제품인지 …",   // 60~160자. 핵심은 앞 78자 안에 (한국어 SERP 절삭 지점)
  "image": "/images/full-width-images/main-img-<slug>.png",   // 5단계 스플래시 이미지 재사용
  "schema": "SoftwareApplication",
  "appCategory": "BusinessApplication",      // 개발자 도구면 "DeveloperApplication"
  "breadcrumb": ["<상단 카테고리>", "제품명"],
  "priority": "0.9"
}
```

그 다음 실행하고 **경고를 0건으로 만든다**:
```bash
python3 .claude/skills/seo-optimize/apply_seo.py
```

이 단계가 `<title>`·description·canonical·OG/Twitter 카드·`SoftwareApplication` JSON-LD·
`sitemap.xml` 등록·이미지 지연 로딩까지 한 번에 처리한다. 자세한 규칙은 `seo-optimize` 스킬 참고.

> `<h1>` 은 제품 페이지 전체에서 **1개**여야 한다. 템플릿의 문의 모달 제목은 `<h2>` 로 둘 것.

### 7. 검증
```bash
python3 -m http.server 8123 --bind 127.0.0.1 &   # 8000이 사용 중이면 다른 포트
```
- `grep` 으로 남은 옛 라벨 0, 신규 링크 경로(파일 타입별 접두사) 확인
- `<main>`/`<section>` 여는/닫는 태그 수 일치 확인
- Chrome headless 스크린샷으로 페이지·nav·footer(열 정렬)·스플래시 렌더 확인:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --hide-scrollbars --window-size=1400,3000 --screenshot=out.png "http://127.0.0.1:8123/contents/<slug>.html"
```
- 브라우저로 `open http://127.0.0.1:8123/contents/<slug>.html` 및 `index.html` 열어 사용자에게 확인 요청

### 8. Playwright 로 메뉴 열어보기 — **메뉴를 건드렸으면 필수**
헤드리스 스크린샷은 **닫힌 상태의 nav** 만 찍는다. 메가메뉴는 hover 해야 펼쳐지므로,
링크를 넣고도 안 보이는 상태(부모 `<li>` 오배치, 컬럼 폭 붕괴, 경로 오타)를 스크린샷으로는 못 잡는다.
그래서 메뉴 추가·변경 작업의 **마지막 단계는 항상 Playwright 로 그 메뉴를 실제로 열어보는 것**이다.

```bash
python3 .claude/skills/add-product-menu/verify-menu.py \
  --menu "<상단 대메뉴 라벨>" --label "<새 메뉴 항목 라벨>" --path contents/<slug>.html
# 눈으로 같이 보려면 --headed, 스크린샷 위치는 --out <dir> (기본 /tmp/verify-menu)
```

검사 항목(전부 통과해야 종료코드 0):
1. 상단 대메뉴 존재 → hover 시 서브메뉴가 **실제로 펼쳐지는지**
2. 펼친 메뉴 안에서 신규 라벨이 `is_visible()` 인지 + `href` 가 지정 경로와 일치하는지
3. 클릭 시 제품 페이지로 이동하는지, `<h1>` 이 1개인지
4. 푸터에도 같은 링크가 있는지
5. **제품 페이지의 nav 에도** 같은 항목이 반영됐는지 (전 파일 일괄 삽입 누락 탐지)
6. 콘솔 에러 / 4xx 리소스 수집

실패하면 `01-menu-open.png` / `02-product-footer.png` / `03-product-full.png` 을 `Read` 로 열어
어디가 깨졌는지 확인하고 고친 뒤 재실행한다.

> 사전 준비: `python3 -c "import playwright"` 로 존재 확인.
> 없으면 `pip3 install playwright && python3 -m playwright install chromium`.

## 산출물
- `contents/<slug>.html` (신규)
- `images/<slug>/*.jpg` (기능 캡처, 5~12장) + `images/full-width-images/main-img-<slug>.png` (테두리 합성 스플래시)
- 전체 `*.html` 의 nav/footer 메뉴 반영
- `index.html` 스플래시 슬라이드
- `seo-meta.json` 신규 항목 + `sitemap.xml` 갱신 + 페이지 SEO 메타 블록 (6단계)

## 산출물 헬퍼
- `.claude/skills/add-product-menu/compose-splash.py` — 스플래시 이미지 합성기.
  캡처 2장 → 보라빛 라운드 테두리 + 대각선 겹침 + 드롭섀도우 투명 PNG. (2·5단계에서 사용)
- `.claude/skills/add-product-menu/verify-menu.py` — Playwright 메뉴 검증기.
  대메뉴 hover → 신규 항목 노출·경로·이동·푸터·제품페이지 nav 반영까지 확인. (8단계에서 사용)

## 체크리스트
- [ ] doc-inbox/ (logo/ 제외) 잔여 파일 확인 — 워터마크면 rebrand, 아니면 원본 그대로 다운로드 자료화
- [ ] yt-dlp/ffmpeg 존재
- [ ] 트랜스크립트로 기능 도출(기능 많으면 10~12개까지)
- [ ] 캡처 프레임 육안 선별(블러/전환 제외), 크롬·Dock 크롭
- [ ] `<slug>.html` head/main/폼 classification 교체
- [ ] **선언부**에 제품의 근본 정체성(예: Spec-Driven Development) 명시, 필요 시 사상(DDD/BDD 등) "왜 좋은지" 종합 섹션 추가
- [ ] nav 앵커 전 파일 존재 검증 후 일괄 삽입 (부분쓰기 시 git 복구)
- [ ] 신규 top-level이면 footer 5열 폭 재조정
- [ ] **스플래시 이미지 = compose-splash.py 로 테두리+겹침 합성** (단순 캡처 1장 금지), `scaleOutIn` 클래스, Learn More 링크
- [ ] `seo-meta.json` 에 신규 페이지 항목 추가 후 `apply_seo.py` 실행 → 경고 0건
- [ ] 로컬 서버 + headless 스크린샷으로 렌더 검증
- [ ] **`verify-menu.py` 로 메뉴를 실제로 열어 검증 — 메뉴 작업의 마지막 단계, 생략 금지**
- [ ] 검증 통과 후 doc-inbox/ 원본 파일(로고 제외) 삭제
