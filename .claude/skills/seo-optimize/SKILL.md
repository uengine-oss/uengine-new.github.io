---
name: seo-optimize
description: 유엔진 홈페이지(uengine-new.github.io)의 SEO 메타데이터를 관리합니다. 모든 페이지의 title·description·canonical·Open Graph·Twitter Card·JSON-LD 구조화 데이터를 일괄 주입하고 sitemap.xml/robots.txt 를 생성하며, h1 구조·이미지 alt·지연 로딩까지 점검합니다. 페이지를 새로 추가하거나 제목·요약을 수정한 직후에는 반드시 실행하세요. "SEO 점검", "SEO 최적화", "메타태그", "sitemap 갱신", "og 태그", "검색 노출", "구조화 데이터", "/seo-optimize" 같은 표현이 있을 때, 그리고 contents/ 아래 HTML 페이지를 추가·수정한 뒤에 트리거.
---

# seo-optimize — 사이트 전체 SEO 메타 관리

유엔진 홈페이지는 정적 HTML 55+ 페이지이고 `<head>` 가 페이지마다 복제되어 있다.
이 스킬은 그 중복을 **하나의 레지스트리 + 하나의 스크립트**로 관리한다.

```
.claude/skills/seo-optimize/
├── SKILL.md          ← 이 문서
├── seo-meta.json     ← 사람이 고치는 유일한 파일 (사이트 설정 + 페이지별 큐레이션 메타)
└── apply_seo.py      ← 레지스트리를 읽어 모든 페이지의 <head> 를 다시 씀 (멱등)
```

## 핵심 규칙

> **`<head>` 안의 SEO 태그를 손으로 고치지 마라.**
> `<!-- SEO:BEGIN --> … <!-- SEO:END -->` 블록은 매 실행마다 통째로 재생성된다.
> 바꾸려면 `seo-meta.json` 을 고치고 스크립트를 다시 돌린다.

## 실행

```bash
# 전체 적용 (sitemap.xml · robots.txt 재생성 포함) — 기본
python3 .claude/skills/seo-optimize/apply_seo.py

# 검사만 (파일 안 건드림, 문제 있으면 exit 1) — 커밋 전 확인용
python3 .claude/skills/seo-optimize/apply_seo.py --check

# 특정 페이지만 (sitemap 은 건드리지 않음)
python3 .claude/skills/seo-optimize/apply_seo.py --only contents/blog/foo.html
```

전체 실행은 1초 이내이고 **멱등**이다. 두 번 돌려도 결과가 같으면 정상.

## 스크립트가 하는 일

각 페이지의 `<head>` 를 다음으로 재작성한다.

| 항목 | 내용 |
|---|---|
| `<meta charset>` | head 최상단으로 승격 (1024바이트 규칙) |
| `<title>` | 페이지 고유 제목 + 브랜드 접미사 (`titleMaxLen` 초과 시 단어 경계에서 절삭) |
| `description` | 페이지 고유 요약 (`descMinLen`~`descMaxLen` 검사) |
| `robots` | 기본 `index, follow, max-image-preview:large`, `noindex: true` 면 `noindex, follow` |
| `canonical` | 절대 URL. `canonicalTo` 지정 시 대표 페이지를 가리킴 (중복 콘텐츠 처리) |
| Open Graph | `og:type/site_name/locale/title/description/url/image/image:alt` + article 은 발행·수정일 |
| Twitter Card | `summary_large_image` + title/description/image |
| JSON-LD | 아래 표 참고 + `BreadcrumbList` |
| 검증·분석 태그 | `site.analytics` 값이 채워져 있으면 GA4 / Search Console / 네이버 확인 태그 삽입 |

그리고 본문에 대해:

- `<html lang="ko">` 누락 시 추가
- `<main>` 이후 이미지에 `loading="lazy" decoding="async"` 부여
  (히어로 후보 2장은 LCP 보호를 위해 즉시 로딩 유지, 네비게이션·로고는 제외)
- 장식용 이미지(`decoration-*.svg` 등)에는 `aria-hidden="true"`

**JSON-LD 스키마 선택** — `seo-meta.json` 의 `schema` 값:

| 값 | 쓰는 곳 |
|---|---|
| `Organization` | 홈(index.html). `WebSite` 도 함께 출력 |
| `SoftwareApplication` | 제품 페이지 (Process GPT, Robo Architect, Ontologic …) |
| `Course` | 교육 페이지 |
| `BlogPosting` / `NewsArticle` | 블로그 글 / 뉴스룸 글 (자동 지정) |
| `CollectionPage` · `Blog` · `ContactPage` · `WebPage` | 목록·기타 페이지 |

## 메타데이터가 정해지는 순서

1. **`seo-meta.json` 의 `pages["경로"]`** — 큐레이션된 값. 가장 우선.
2. **`contents/bloglist.html` 의 카드** — 블로그 글은 목록의 제목·날짜·요약을 그대로 가져온다.
3. **`contents/newsroom.html` 의 카드** — 뉴스룸 글도 동일.
4. **페이지 본문** — `<h1>` 과 첫 문단에서 유추. **이 경우 경고를 띄운다.**

즉 **블로그·뉴스 글은 목록 페이지만 제대로 채우면 SEO가 자동으로 붙는다.**
제품·서비스 페이지는 목록이 없으므로 `seo-meta.json` 에 직접 써야 한다.

## 페이지를 새로 추가했을 때 (체크리스트)

1. 블로그/뉴스 글이면 → `bloglist.html` / `newsroom.html` 에 카드(제목·날짜·요약)를 먼저 추가한다.
   제품·서비스 페이지면 → `seo-meta.json` 의 `pages` 에 항목을 추가한다.

   ```jsonc
   "contents/newproduct.html": {
     "title": "제품명 — 한 줄 가치제안",        // 브랜드 접미사는 자동, 70자 이내
     "description": "무엇을 하는 제품인지 …",   // 60~160자, 핵심은 앞 78자 안에
     "image": "/images/full-width-images/main-img-newproduct.png",  // 사이트 루트 기준
     "schema": "SoftwareApplication",
     "appCategory": "BusinessApplication",
     "breadcrumb": ["AI-Native Enterprise", "제품명"],
     "priority": "0.9"
   }
   ```

2. `python3 .claude/skills/seo-optimize/apply_seo.py` 실행.
3. 출력된 **경고를 0건으로 만든다.** 남아 있으면 SEO가 덜 된 것이다.

## 한국어 카피 작성 규칙

- **title**: 70자 이내. `제품명 — 핵심 가치` 형태. 브랜드 접미사(` | uEngine`)는 스크립트가 붙이므로 쓰지 않는다.
- **description**: 60~160자. 구글 한국어 SERP는 **약 78자에서 잘리므로** 핵심 메시지를 앞부분에 둔다.
- **모든 페이지의 title·description 은 서로 달라야 한다.** 중복이면 스크립트가 경고한다.
- 키워드를 나열하지 말고 사람이 읽는 문장으로 쓴다. `meta keywords` 는 의도적으로 넣지 않는다(랭킹 신호 아님).

## 경고 종류와 대응

| 경고 | 대응 |
|---|---|
| `… 을(를) 페이지 본문에서 자동 유추했습니다` | `seo-meta.json` 에 제대로 된 title/description 을 쓴다 |
| `목록 페이지에 카드가 없습니다` | `bloglist.html` / `newsroom.html` 에 카드를 추가한다 |
| `title 중복` / `description 중복` | 페이지마다 다르게 다시 쓴다 |
| `description 이 너무 짧습니다` | 60자 이상으로 늘린다 |
| `<h1> 이 없습니다` | 히어로 제목을 `<h1>` 으로 만든다 |
| `<h1> 이 N개입니다` | 대표 제목 하나만 `<h1>`, 나머지는 `<h2>` (모달 제목·캐러셀 슬라이드가 흔한 원인) |
| `alt 속성이 없는/빈 <img>` | 내용이 있는 이미지면 설명을 넣는다. 순수 장식이면 파일명에 `decoration` 을 쓰면 검사에서 제외된다 |

## 아직 사람이 해야 하는 일

`seo-meta.json` 의 `site.analytics` 는 비어 있다. 값을 채우면 다음 실행에서 전 페이지에 자동 삽입된다.

- `ga4MeasurementId` — GA4 측정 ID (`G-XXXXXXXXXX`). analytics.google.com 에서 발급
- `googleSiteVerification` — Google Search Console 소유 확인 메타태그 `content` 값
- `naverSiteVerification` — 네이버 서치어드바이저 소유 확인 값 (국내 B2B 유입에 중요)

등록 후에는 Search Console·서치어드바이저에 `https://www.uengine.org/sitemap.xml` 을 제출한다.

## 자동 실행

`.claude/settings.json` 의 훅이 다음을 자동으로 수행한다.

- **PostToolUse** — `contents/**.html` 또는 `index.html` 을 Write/Edit 하면 그 페이지에 `--only` 로 즉시 적용.
  큐레이션이 필요한 경고가 있으면 그 내용이 Claude 에게 전달된다.
- **Stop** — 응답이 끝날 때 HTML 변경이 있었으면 전체 실행으로 `sitemap.xml` · `robots.txt` 를 갱신한다.

훅이 돌더라도 **새 페이지의 `seo-meta.json` 항목은 사람(또는 Claude)이 써야 한다.** 훅은 누락을 알려줄 뿐이다.
