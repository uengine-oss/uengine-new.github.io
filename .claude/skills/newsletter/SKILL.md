---
name: newsletter
description: 직전 뉴스레터 발행 시점(newsletters/state.json 에 기록된 커밋) 이후의 git 변경사항만 모아 이메일 발송용 뉴스레터 HTML을 자동 생성합니다. 주간/월간 모두 지원하며 발행 라벨은 "YYYY년 MM월 N주" 형식을 씁니다. 그 기간 동안 바뀐 제품 페이지·신규 블로그 글·공지 등을 카테고리별로 묶어, 고객이 관심 가질 만한 키워드와 제목으로 재구성한 요약 카드를 만들고, 각 카드에는 실제 사이트 콘텐츠로 가는 절대경로 링크와 기존 repo 이미지를 하나씩 붙입니다. 결과물은 Stibee 등 이메일 서비스에 그대로 붙여넣을 수 있는 인라인 스타일 HTML(newsletters/YYYY-MM-WN.html)로 저장하고, 발행 이력을 state.json 에 추가합니다. "뉴스레터 만들어줘", "이번주 뉴스레터", "주간 뉴스레터 생성", "월간 뉴스레터", "뉴스레터 초안", "/newsletter" 등의 표현이 있을 때 트리거.
---

# newsletter — 직전 발행 이후 변경분 → 이메일 뉴스레터 HTML 생성

**직전 호 발행 시점 이후**의 git 변경사항만을 근거로, 고객에게 발송할 **이메일 호환 HTML
뉴스레터**를 만든다. 사이트 페이지가 아니라 Stibee(`https://uengine.stibee.com/`) 같은
이메일 서비스에 붙여넣는 산출물이므로 `contents/`의 nav/footer 하드코딩 관례를 따르지 않는다
(CLAUDE.md 의 "메뉴 중복" 문제와 무관).

핵심 원칙: **날짜(`--since`)로 자르지 않는다.** 반드시 `newsletters/state.json` 에 기록된
직전 호의 `coversTo` 커밋을 기준점으로 삼는다. 발행 주기가 불규칙해도 콘텐츠가 누락되거나
중복 게재되지 않는다.

---

## 0. 발행 이력 파일 — `newsletters/state.json`

이 스킬의 상태 저장소. 구조:

```json
{
  "baseUrl": "https://www.uengine.org/",
  "issues": [
    {
      "slug": "2026-08-W1",
      "label": "2026년 08월 1주",
      "cadence": "weekly",
      "file": "newsletters/2026-08-W1.html",
      "publishedAt": "2026-08-06",
      "coversFrom": "945366d",
      "coversTo": "9dac7e6",
      "headlines": ["...", "..."],
      "note": "..."
    }
  ]
}
```

- `issues` 는 **오래된 것부터** 시간순. 마지막 항목이 직전 호.
- `coversTo` = 그 호가 다룬 마지막 커밋 해시. **다음 호의 시작점**이 된다.
- 파일이 없으면(최초 실행) `newsletters/` 안의 가장 최근 호 HTML 파일이 커밋된 시점을
  기준으로 삼고, 사용자에게 알린 뒤 state.json 을 새로 만든다.

---

## 1. 범위 결정

```bash
# 직전 호의 coversTo 읽기
python3 -c "import json;d=json.load(open('newsletters/state.json'));print(d['issues'][-1]['coversTo'])"

PREV=<위에서 얻은 해시>
HEAD_NOW=$(git rev-parse --short HEAD)
```

범위는 `$PREV..HEAD`. 오늘 날짜와 무관하게 **직전 호 이후 전부**를 다룬다
(주간 전환 직후 첫 호처럼 2~3주치가 한 번에 들어올 수 있고, 그게 정상이다).

## 2. 발행 라벨 / 파일명

- 라벨 형식: **`YYYY년 MM월 N주`** (예: `2026년 08월 1주`). 월간이라도 이 형식을 쓰되
  한 달 전체를 다뤘다면 `2026년 08월` 처럼 주차를 생략해도 된다.
- 주차 계산: **`N = ceil(오늘 일자 / 7)`** — 1~7일=1주, 8~14일=2주, 15~21일=3주,
  22~28일=4주, 29~31일=5주. 요일 기준 ISO 주차를 쓰지 않는다(설명하기 어렵고 월 경계에서 혼란).
  ```bash
  date +"%Y-%m-%d"   # 오늘 확인 — 절대 추측하지 말 것
  ```
- 파일명: `newsletters/YYYY-MM-WN.html` (예: `2026-08-W1.html`). 월간이면 `YYYY-MM.html`.

## 3. 변경 이력 수집

```bash
# 신규 추가된 파일 (신제품 페이지 · 신규 블로그 글 · 신규 이미지 자산)
git diff --name-status $PREV..HEAD --diff-filter=A

# 삭제 (페이지 통폐합 흔적 — 통합된 새 페이지를 찾아 항목화)
git diff --name-status $PREV..HEAD --diff-filter=D

# 수정된 파일을 변경량 순으로 — 상위만 실제 내용 확인
git diff --numstat $PREV..HEAD --diff-filter=M | sort -k1 -rn | head -30

# 커밋 목록 (제목으로 성격 파악)
git log --pretty=format:'%h|%ad|%s' --date=short $PREV..HEAD

# 로컬 미커밋 변경분
git status --porcelain
```

특정 페이지가 크게 바뀐 이유를 알려면 **커밋별 churn** 을 보고 진짜 내용 커밋을 찾는다
(SEO/nav 일괄 커밋이 churn 상위를 오염시킨다):
```bash
git log --numstat --pretty=format:'%h|%ad|%s' --date=short $PREV..HEAD -- contents/<page>.html
git show <hash> -- contents/<page>.html | grep '^+' | grep -oE '>[^<>]{6,90}<' | sed 's/[<>]//g'
```
신규 페이지/블로그 글은 diff 대신 완성본에서 메타를 뽑는 게 빠르다:
```bash
grep -o '<title>[^<]*</title>' <file>
grep -o '<meta name="description" content="[^"]*"' <file>
grep -oE '<h[12][^>]*>[^<]{4,120}</h[12]>' <file> | sed 's/<[^>]*>//g'
```

## 4. 파일 경로 기준 카테고리 분류

| 패턴 | 분류 | 비고 |
|---|---|---|
| `contents/blog/<slug>.html` (신규, status A) | 새 블로그 글 | 리드 문단·핵심 키워드 추출. 2편 이상이면 한 카드로 묶어도 좋다 |
| `contents/bloglist.html` 만 단독 변경 | (블로그 신규 항목에 흡수) | 별도 항목화하지 않음 |
| `contents/<product>.html` + `images/<slug>/*` 또는 `images/full-width-images/main-img-<slug>.png` | 제품 업데이트/신규 출시 | 신규 페이지(A)면 "출시", 수정(M)이면 "업데이트" |
| 기존 제품 페이지에 **새 섹션**이 통째로 추가(+200줄 이상, 새 `id="..."` 앵커 등장) | 신기능 | 앵커로 딥링크할 것 (`page.html#anchor`) |
| `index.html` 스플래시/대메뉴 구조 변경 | 사이트 개편 | 고객에게 의미 있는 재편만. 사소한 라벨 변경은 생략하거나 "그 밖의 소식"으로 |
| 페이지 삭제(D) + 통합 신규 페이지(A) | 통폐합 개편 | 없어진 페이지가 아니라 **새로 생긴 통합 페이지**를 소개 |
| 동일 패턴이 반복되는 전 페이지 일괄 수정(nav/footer 배치 등) | 노이즈 | **제외** — 최종 결과물에 이미 반영되어 있음 |
| SEO 메타 주입 / 이미지 WebP 변환 / GIF→MP4 / GA·GSC 태그 / `sitemap.xml`·`robots.txt` | 내부 최적화 | 개별 항목화 **금지**. 굳이 넣으려면 "그 밖의 소식"에 한 줄 |
| `.claude/`, `.github/`, `scripts/`, `*.md`(README 등) | 내부 도구/문서 | **제외** — 고객 무관 |
| 같은 페이지를 여러 커밋이 반복 수정 | — | 최종 상태 기준으로 **1개 항목**으로 병합 |

이 표를 기계적으로 따르되, 애매한 파일은 실제 diff 내용을 보고 판단한다.

## 5. 상위 항목 선정 및 카피라이팅

- 전체 커밋을 나열하지 말고, 고객 관점에서 임팩트 있는 **3~6개 항목**만 추린다.
  자잘하지만 알릴 가치가 있는 것들은 마지막 **"그 밖의 소식"** 박스에 불릿 1~2줄로 몰아넣는다.
- 항목마다 다음을 작성:
  - **제목**: 제품명/핵심 키워드가 드러나는 클릭 유도형 한 줄
    (예: "한 번 배운 업무는, 매번 정확하게 — Process GPT 'Deterministic Replay' 공개")
  - **본문 2~3문장**: 무엇이 바뀌었고 고객에게 왜 중요한지. 내부 구현/리팩터링 디테일이 아니라
    사용자가 체감하는 가치 위주로. 페이지에 있는 구체적 숫자·검증 결과가 있으면 인용하면 좋다.
  - **대표 이미지** (6번 참고)
  - **CTA 링크**: 실제 사이트 절대 URL (신기능이면 섹션 앵커까지)
- 직전 호에서 다룬 제품이 이름/구조가 바뀐 경우 "지난 호에서 소개한 ~가 …" 처럼
  **연속성을 명시**한다 (구독자가 중복으로 느끼지 않게).
- 헤더에는 발행 라벨 타이틀 + 1~2문장 인트로. 주기가 바뀐 호라면 그 사실을 인트로에서 알린다.
- 항목이 하나도 없으면(순수 내부 변경만 있던 기간) 사용자에게 알리고 발행 여부를 확인한다 —
  억지로 채우지 않는다. 이 경우 state.json 은 건드리지 않는다.

## 6. 이미지 재사용 (신규 제작 금지 — repo에 있는 것만 재사용)

- **제품 페이지**: `images/full-width-images/main-img-<slug>.png` 우선.
- **신규 기능 섹션**: `images/<feature>/*.jpg` 중 개념도 성격의 것.
- **신규 블로그 글**: 본문 안 첫 번째 콘텐츠 이미지(다이어그램/캡처)를 재사용.
  로고/아이콘/`section-bg-*.jpg`(히어로 배경)는 건너뛴다. 관련 뉴스룸 이미지도 후보.
- 마땅한 이미지가 없으면 **이미지 없이 텍스트만** 넣는다 (억지 매칭 금지).

**필수 제약 3가지:**
1. **절대 URL** — 이메일 클라이언트는 상대경로를 못 읽는다.
   `https://www.uengine.org/images/...`, `https://www.uengine.org/contents/...`
2. **`.webp` 금지** — Outlook 등 다수 클라이언트가 렌더링하지 못한다. 사이트가 WebP로
   전환되었어도 뉴스레터에는 반드시 `.png`/`.jpg` 원본을 쓴다(대개 나란히 남아 있다).
3. **파일명은 ASCII만** — 한글 파일명은 퍼센트 인코딩이 필요해 깨질 위험이 있다.
   한글명 자산밖에 없으면 다른 자산을 찾거나 이미지를 생략한다.

## 7. 자산이 실제로 "라이브"인지 확인 (중요)

이메일은 사이트에서 이미지를 불러온다. **아직 커밋/푸시되지 않은 파일은 404가 난다.**
```bash
git ls-files --error-unmatch <path>          # 추적 중인지
git rev-list --left-right --count origin/main...HEAD   # 0	0 이면 푸시 완료
```
미푸시 상태의 신규 이미지를 쓰려면 사용자에게 "먼저 푸시해야 이미지가 보인다"고 알린다.
(main push = 즉시 배포)

## 8. 이메일 호환 HTML 작성

- `<table>` 기반 레이아웃, 컨테이너 최대폭 640px, **인라인 `style=""`만** 사용
  (Gmail 등 다수 클라이언트가 `<head><style>` 블록을 제거한다).
- 웹폰트 대신 시스템 폰트 스택(`Arial, "Apple SD Gothic Neo", sans-serif`).
- 사이트 톤 유지: 헤더 다크 네이비(`#1a1a2e`) 배경 + 로고, 포인트 컬러 보라(`#7c4dbc`).
- **헤더 로고**: `https://www.uengine.org/images/logo-w.png`, 원본 비율 2170×451(≈4.81:1).
  이메일은 인라인 `width`/`height` 속성이 그대로 적용되므로 **반드시 비율을 지켜서 지정**
  (예: `width="105" height="22"`). `height="34"` 처럼 임의로 늘리면 로고가 찌그러진다 —
  실제로 2026-07호에서 이 실수가 있었다.
- 구조: 헤더(로고 + 발행 라벨 + 인트로) → 항목 카드 반복(뱃지 → 이미지 → 제목 → 본문 →
  "자세히 보기 →" 버튼, 사이사이 `<hr>`) → "그 밖의 소식" 박스(선택) → 푸터(회사 정보 +
  Stibee 구독 링크 + 문의 이메일).
- 카드 뱃지는 성격별로 색을 나눈다: NEW FEATURE(보라 `#f0ebfb`/`#7c4dbc`),
  PRODUCT(파랑 `#e6f0fb`/`#1e6fbc`), 특집(주황 `#fdeee3`/`#c56a1f`),
  교육(초록 `#eaf7ee`/`#2f9e52`), INSIGHT(남색 `#e9edf7`/`#3f4d7a`).
- 링크가 2개인 카드는 주 CTA를 버튼, 보조 CTA를 텍스트 링크로.
- **직전 호 HTML을 열어 구조를 그대로 따르는 것이 가장 빠르고 안전하다.**
- 다크모드 대응 불필요(이메일은 라이트 고정 권장).
- 파일 상단에 HTML 주석으로 발행 라벨·**대상 커밋 범위**·생성 스킬을 남긴다.

## 9. 저장 및 이력 갱신

1. `newsletters/<slug>.html` 저장.
2. `newsletters/state.json` 의 `issues` 배열 **끝에** 이번 호 항목 추가
   (`coversFrom` = 직전 호 `coversTo`, `coversTo` = `git rev-parse --short HEAD`).
   이걸 빼먹으면 다음 호가 같은 내용을 다시 실어버린다.

## 10. 검증

```bash
# 본문의 절대 URL이 실제 존재하는 경로인지 (앵커 제거 후 대조)
grep -o 'https://www\.uengine\.org/[^"]*' newsletters/<slug>.html \
  | sed 's#https://www.uengine.org/##; s/#.*//' | sort -u \
  | while read p; do [ -z "$p" ] && continue; [ -f "$p" ] || echo "MISSING: $p"; done

# 딥링크 앵커가 실제로 존재하는지
grep -c 'id="deterministic-replay"' contents/processgpt.html

# .webp 가 섞이지 않았는지
grep -c '\.webp' newsletters/<slug>.html    # 0 이어야 함

# 로컬 렌더 확인
open newsletters/<slug>.html
```
커밋은 사용자가 요청할 때만.

## 산출물
- `newsletters/<YYYY-MM-WN>.html` (신규, 이메일 호환 인라인 스타일)
- `newsletters/state.json` (이번 호 이력 추가)

## 체크리스트
- [ ] `newsletters/state.json` 의 직전 호 `coversTo` 를 시작점으로 범위 산정 (`--since` 금지)
- [ ] `date` 로 오늘 날짜 확인 후 `N = ceil(일/7)` 로 주차 계산, 라벨 `YYYY년 MM월 N주`
- [ ] `--diff-filter=A/D/M` + 커밋별 churn 으로 진짜 콘텐츠 변경 식별
- [ ] SEO/WebP/GIF→MP4/nav 일괄수정 등 노이즈 제외, 같은 페이지 중복 커밋은 1개로 병합
- [ ] 상위 3~6개 항목만 선정, 나머지는 "그 밖의 소식" 불릿으로
- [ ] 직전 호와 겹치는 제품은 연속성 문구로 처리
- [ ] 이미지는 repo 기존 자산만 재사용 — **`.webp` 금지, 한글 파일명 금지**, 없으면 생략
- [ ] 쓰려는 이미지가 커밋·푸시되어 실제 라이브인지 확인
- [ ] 모든 이미지·링크는 `https://www.uengine.org/...` 절대경로, 신기능은 `#앵커` 딥링크
- [ ] 테이블 레이아웃 + 인라인 style만 사용(이메일 클라이언트 호환)
- [ ] 헤더 로고 `width`/`height`가 원본 비율(2170×451 ≈ 4.81:1)과 일치(찌그러짐 방지)
- [ ] `newsletters/state.json` 에 이번 호 항목 추가 (누락 시 다음 호 중복 게재)
- [ ] 존재하지 않는 경로 없는지 grep 검증 + 로컬에서 열어 렌더 확인
- [ ] 사용자에게 발행 여부 확인 (커밋은 요청 시에만)
