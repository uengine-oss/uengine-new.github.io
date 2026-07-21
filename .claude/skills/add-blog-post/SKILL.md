---
name: add-blog-post
description: 유엔진 홈페이지(uengine-new.github.io)에 블로그 글을 추가합니다. PDF·문서·URL·주제 아무거나 소스로 주면 기존 블로그 스타일(contents/blog/*.html)에 맞춰 상세 페이지를 생성하고 bloglist.html 목록 맨 위에 카드를 추가합니다. 소스에 텍스트(ASCII)로 그려진 다이어그램이 있으면 스타일링된 HTML 다이어그램으로 다시 그리고, 필요 시 후반부에 자사 제품(Process GPT 등)과의 개념→기능 얼라인 섹션을 붙입니다. "블로그에 추가", "블로그 글 써줘", "이 PDF를 블로그로", "이 내용으로 블로그 포스트", "/add-blog-post", "블로그 올려줘" 등의 표현이 있을 때 트리거.
---

# add-blog-post — 소스 문서 → 홈페이지 블로그 글 추가

유엔진 홈페이지(정적 HTML)에 블로그 글을 추가하는 전 과정. 사용자가 **소스(PDF/문서/URL/주제)**
하나만 주면 상세 페이지 생성 → 목록 반영 → 검증까지 수행한다.

## 대상 구조
- 블로그 상세: `contents/blog/<slug>.html` (asset 경로 접두사 `../../`, contents 페이지 링크는 `../`)
- 블로그 목록: `contents/bloglist.html` (카드 목록, 최신 글이 맨 위)
- 모든 페이지는 nav/footer를 **하드코딩 복제**한다 (CLAUDE.md 참고).

## 입력 (없으면 확인)
1. **소스** (필수) — PDF/마크다운/URL/구술 주제. PDF는 `Read`로 직접 읽는다.
   소스가 **doc-inbox/에 놓인 NotebookLM류 워터마크 PDF**(슬라이드/인포그래픽 내보내기)라면
   본문에 넣을 다이어그램 이미지는 먼저 `doc-inbox-rebrand` 스킬로 워터마크를 uEngine 로고로
   교체한 뒤 가져온다 (직접 캡처해 워터마크가 그대로 노출되지 않도록 한다).
2. **slug** — 파일명 근거 (예: `loopengineering`). 없으면 주제에서 영문 소문자로 제안.
3. **게시 날짜** — 기본값 오늘. 표기 형식: `July 07, 2026` (영문 월, 2자리 일, 콤마, 연도).
4. **제품 얼라인 여부** — 후반부에 자사 제품 마케팅 섹션을 붙일지 (기본: 사용자가 요청할 때만).

---

## 절차

### 1. 템플릿과 최신 메뉴 파악
- 본문 구조 템플릿: `contents/blog/aimemory.html` (blockquote 섹션 헤더 + `.prose` 스타일).
- **주의: 기존 blog/*.html 상세 페이지들의 nav/footer는 구버전일 수 있다.**
  nav/footer는 반드시 **`contents/bloglist.html`의 최신 메뉴**를 기준으로 삼고,
  경로만 blog/ 깊이에 맞게 변환한다:
  - `../images/`, `../css/`, `../js/` → `../../…`
  - `contactus.html` 등 contents 페이지 → `../contactus.html`
  - `bloglist.html` → `../bloglist.html`, `../index.html` → `../../index.html`
- 확인 방법: 최신 메뉴에만 있는 항목(예: `ontologystudio`)을 grep 해서 어느 파일이 최신인지 판별.
```bash
grep -c "ontologystudio" contents/bloglist.html contents/blog/*.html
```

### 2. 상세 페이지 생성 — `contents/blog/<slug>.html`
`Write`로 전체 파일을 새로 작성한다 (head/loader/nav/header/본문/footer/JS 순서는 aimemory.html과 동일).

**헤더 섹션** (다크 배경 타이틀):
```html
<section class="page-section bg-dark-1 bg-dark-alpha-70 light-content parallax-5" style="background-image: url(../../images/full-width-images/section-bg-1.jpg)">
  ... <h1 class="hs-title-0 mb-20"><span class="wow charsAnimIn" data-splitting="chars">글 제목</span></h1>
  ... <i class="mi-clock size-16"></i> ... July 07, 2026
```

**본문 스타일 문법** (`.blog-item-body.chat-gpt` 내부):
- 섹션 제목: `<blockquote><p>&nbsp; 1. 섹션 제목</p></blockquote>`
- 문단 블록: `<div class="mb-50 prose"> <p>…</p> </div>`
- 강조 목록: `<li><b style="font-weight: bold;">🔄 키워드:</b> 설명</li>` (이모지 불릿 적극 사용)
- 소제목: `<p style="text-decoration: underline;"><b>소제목</b></p>`
- 인용/하이라이트 박스: `<div class="mb-50 prose" style="border-left: 5px solid #ddd;"><p style="margin-left: 20px;">…</p></div>`
- 표: `<div style="overflow-x: auto;">` 로 감싸고 인라인 스타일 —
  헤더행 `style="background-color: #1a1a2e; color: #fff;"`, 홀수행 줄무늬 `background-color: #f7f7fa;`,
  셀 `padding: 12px 16px; border: 1px solid #ddd;`
- 참고 자료: 마지막 `.prose` 에 `<ul style="font-size: 14px;">` 링크 목록 (`target="_blank"`).
  소스에 참고문헌이 수십 개면 **본문에서 실제 인용된 핵심만** 추린다.
- 본문 마지막 뒤: `<a href="../bloglist.html" class="blog-item-more left"><i class="mi-chevron-left"></i>&nbsp;Back to blog</a>`

### 3. 텍스트 다이어그램 → 그래픽 재작성
소스에 ASCII 아트/텍스트 박스 다이어그램이 있으면 **그대로 옮기지 말고** 스타일링된
중첩 div 다이어그램으로 다시 그린다. 이 사이트 톤: 그라데이션 배경 + 라운드 박스 +
드롭섀도우 + pill 배지, 캡션 포함. 예 (중첩 아키텍처):
```html
<div class="mb-50">
  <div style="max-width: 640px; margin: 0 auto; border: 2px solid #1a1a2e; border-radius: 14px; background: linear-gradient(180deg, #f4f6fb 0%, #eceff7 100%); padding: 24px 22px; box-shadow: 0 8px 24px rgba(26,26,46,0.08);">
    <div style="text-align: center; font-weight: 700; ...">바깥 계층 이름</div>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; ...">
      <span style="background:#fff; border:1px solid #c3cbe0; border-radius:20px; padding:5px 14px; font-size:13px;">🛡️ 항목 배지</span>
    </div>
    <div style="border: 2px dashed #5b6b9e; border-radius: 12px; ...">  <!-- 중간 계층: 점선 -->
      <div style="border: 2px solid #7c4dbc; ...">  <!-- 안쪽 계층: 포인트 컬러(보라) -->
```
캡션: `<p class="text-center mt-20" style="font-size: 14px; color: #888;">설명</p>`

### 4. (선택) 자사 제품 얼라인 섹션
사용자가 원하면 글의 마지막 본문 섹션(참고 자료 앞)에 **"이 청사진을 이미 제품으로: <제품명>"**
섹션을 추가한다. 제품 소재는 해당 제품 소개 페이지(예: `contents/processgpt.html`)에서 추출:
- 소개/차별점/FEATURES 섹션의 `feature-card`, `features-2-descr`, `testimonials-6-author` 텍스트를 grep/sed로 수집.
- 구성 패턴:
  1. 독자 질문형 전환 문단 ("그래서 이걸 지금 어디서 경험할 수 있는가?") — 글의 다이어그램/개념이 제품의 실제 설계라는 연결.
  2. **개념 → 제품 기능 매핑 표** (2열, 위 표 스타일). 글의 핵심 개념마다 제품 기능을 1:1 대응.
  3. 글에서 제시한 제언/원칙에 제품이 어떻게 답하는지 불릿 목록.
  4. 인용 박스로 긴장감 있는 수치(예: "AI 도입 성공률 5% 미만") 인용.
  5. CTA 문단 — `../processgpt.html` 등 내부 페이지와 외부 사이트(`target="_blank"`) 링크.
- 관련 제품 페이지(`../ontologystudio.html` 등) 내부 링크도 자연스럽게 삽입.

- **[필수] 딥링크 규칙 — 기능을 언급하면 그 기능 소개 섹션으로 직접 링크한다.**
  개념→기능 매핑 표(또는 본문)에서 제품 기능을 거론할 때, 제품 소개 페이지의 **전체**가 아니라
  **그 기능을 설명하는 정확한 섹션**으로 앵커 링크(`#앵커`)를 항상 함께 건다.
  1. 제품 소개 페이지에서 대상 기능 섹션(예: `processgpt.html`의 "핵심 차별점" 카드)에
     앵커가 없으면 먼저 심는다 — 제목 `<h4>` 바로 앞에 `<a id="diff-<key>" name="diff-<key>"></a>`
     (`diff-nocode`, `diff-selflearning`, `diff-reverse`, `diff-agent`, `diff-bpmn`, `diff-ontology` 가 현재 존재).
  2. 매핑 표의 기능 셀(우측 열) 끝에 소개 섹션으로 가는 링크를 붙인다:
     ```html
     <br><a href="../processgpt.html#diff-<key>" style="font-size: 13px; font-weight: 600; text-decoration: underline; color: #7c4dbc;">↗ 소개 페이지에서 보기</a>
     ```
  3. 대응되는 소개 섹션이 없는 기능은 억지 링크를 만들지 말고 링크 없이 둔다.
  4. 심은 앵커와 건 링크가 1:1로 맞는지 grep 으로 검증:
     `grep -o 'id="diff-[a-z]*"' contents/processgpt.html` ↔
     `grep -o 'processgpt.html#diff-[a-z]*' contents/blog/<slug>.html`

### 5. 목록 반영 — `contents/bloglist.html`
목록 첫 카드(`<!-- Content --> <div class="col-lg-8 offset-lg-2">` 바로 아래 첫 `<!-- Post -->`)
**앞에** 새 카드를 삽입한다 (최신 글이 맨 위):
```html
<!-- Post -->
<div class="blog-item box-shadow round p-4 p-md-5">
    <h2 class="blog-item-title"><a href="blog/<slug>.html">글 제목</a></h2>
    <div class="blog-item-data"><i class="mi-clock size-16"></i> July 07, 2026</div>
    <div class="mb-30"><p class="mb-0">2~3문장 소개문 (제품 얼라인 섹션이 있으면 그 언급 포함)</p></div>
    <div class="blog-item-foot"><a href="blog/<slug>.html" class="btn btn-mod btn-round btn-medium btn-gray">Read More</a></div>
</div>
<!-- End Post -->
```

### 6. 검증
- HTML 태그 균형 검사 (python HTMLParser 스택 방식):
```python
from html.parser import HTMLParser
# start/end 태그 스택 대조, void={'meta','link','img','br','hr','input','source'}
```
  > **알려진 무해 경고:** footer 전화번호/이메일 옆 잉여 `</a>` 2건은 전 페이지 공통의
  > 기존 마크업이다. 템플릿과 동일하게 유지하고 무시한다. 그 외 mismatch는 실제 오류.
- (선택) 로컬 렌더 확인:
```bash
python3 -m http.server 8123 --bind 127.0.0.1 &
open http://127.0.0.1:8123/contents/blog/<slug>.html
```
- 커밋은 사용자가 요청할 때만.

## 산출물
- `contents/blog/<slug>.html` (신규, 최신 nav/footer 적용)
- `contents/bloglist.html` 맨 위 카드 추가

## 체크리스트
- [ ] 소스 전체를 읽고 구조(섹션/표/다이어그램/참고문헌) 파악
- [ ] nav/footer는 bloglist.html 최신 버전 기준 + blog/ 깊이 경로 변환 (`../../`, `../`)
- [ ] blockquote 헤더 + `.prose` 블록 + 인라인 표 스타일로 본문 변환
- [ ] ASCII 다이어그램은 스타일링된 div 다이어그램으로 재작성 (+캡션)
- [ ] 제품 소개 페이지에서 기능 추출 → 개념-기능 매핑 표 + CTA 섹션
- [ ] 매핑 표의 각 기능 셀 → 제품 소개 페이지의 해당 섹션 앵커(`#diff-…`)로 딥링크 (앵커 없으면 심고, 1:1 검증)
- [ ] bloglist.html 첫 카드로 삽입, 날짜 형식 `Month DD, YYYY`
- [ ] 태그 균형 검사 통과 (footer `</a>` 2건 제외)
