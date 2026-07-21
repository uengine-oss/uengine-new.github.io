---
name: doc-inbox-rebrand
description: doc-inbox/ 폴더에 PDF(주로 NotebookLM "Slides"/Infographic 내보내기)를 넣어두면, 페이지를 렌더링해 우하단 NotebookLM 워터마크 로고를 doc-inbox/logo/ 의 uEngine 로고로 교체하고, 결과 이미지를 홈페이지 images/<slug>/ 에 배치한 뒤 원본 PDF도 images/ 에 복사해 다운로드 버튼으로 연결한다. "doc-inbox에 넣어둔 pdf 처리해줘", "notebooklm 로고 지워줘", "이 PDF 슬라이드를 사이트에 넣어줘", "/doc-inbox-rebrand" 같은 표현이 있을 때, 또는 add-product-menu/add-blog-post 스킬 실행 중 소스가 NotebookLM류 워터마크가 박힌 PDF/슬라이드일 때 하위 단계로 트리거.
---

# doc-inbox-rebrand — NotebookLM 워터마크 PDF → uEngine 브랜드 이미지

`doc-inbox/`에 던져 넣은 PDF(주로 NotebookLM이 생성한 슬라이드/인포그래픽 내보내기)를
홈페이지에 쓸 수 있는 형태로 정리한다: 페이지를 이미지로 렌더링하고, 우하단
NotebookLM 로고를 `doc-inbox/logo/`의 uEngine 로고로 바꿔치기하고, 적절한
`images/<slug>/` 폴더에 배치한 뒤 원본 PDF도 다운로드용으로 사이트에 반영한다.

이 스킬은 **독립적으로도**, **add-product-menu/add-blog-post 같은 다른 스킬의
하위 단계로도** 호출될 수 있다 (예: 유튜브 대신 NotebookLM PDF가 소스로 주어졌을 때).

## 입력 (없으면 AskUserQuestion으로 확인)
1. **PDF 경로** — 기본적으로 `doc-inbox/*.pdf` 중 최근 추가된 파일.
2. **uEngine 로고** — 기본적으로 `doc-inbox/logo/*.png` (없으면 `images/logo-b.png` 등 기존 로고로 대체 확인).
3. **slug / 대상 위치** — 결과 이미지를 넣을 `images/<slug>/` 폴더명. 이미 진행 중인 제품/블로그 작업이 있으면 그 slug를 그대로 쓴다.
4. **선별 기준** — 14페이지 전부가 아니라 "중요 아키텍처/핵심 다이어그램만" 골라야 하는 경우가 많으므로, 각 페이지를 `Read`로 직접 훑어보고 상세 페이지 서사에 도움이 되는 페이지만 고른다.

## 절차

### 1. PDF → 페이지 이미지 렌더링
동일 해상도로 전 페이지를 렌더링해야 워터마크 위치가 모든 페이지에서 동일한 픽셀 좌표에 고정된다:
```bash
pdftoppm -png -r 100 "doc-inbox/<file>.pdf" <SCRATCH>/page
```
`pdftoppm`이 없으면 `brew install poppler`.

### 2. 페이지 훑어보기 & 중요 페이지 선별
각 `<SCRATCH>/page-NN.png`를 `Read`로 직접 열어본다. 표지/클로징 슬라이드(텍스트만 있거나 로고 아트만 있는 페이지)는 보통 제외하고, **아키텍처 다이어그램·레이어 구조·비교표·로드맵**처럼 정보 밀도가 높은 페이지를 고른다.

### 3. 워터마크 위치 확인 (최초 1회, 페이지 크기가 바뀌면 재확인)
NotebookLM 워터마크는 슬라이드 콘텐츠가 아니라 템플릿 크롬이라 **모든 페이지에서 완전히 동일한 픽셀 박스**에 나타난다. 콘텐츠가 적은 페이지(표지/클로징) 하나를 크롭해 정확한 박스를 잡는다:
```python
from PIL import Image
im = Image.open("<SCRATCH>/page-01.png")
im.crop((im.width-260, im.height-70, im.width, im.height)).save("/tmp/logo-check.png")
```
`Read`로 확인 후 필요하면 박스를 좁혀 `debrand-slide.py --box`에 넘긴다.
(100 DPI, 1912x1067 렌더 기준 기본값은 `1758,1032,1902,1059` — Ontologic PDF 처리 시 측정된 값이며 페이지 크기가 같은 다른 NotebookLM 내보내기에도 재사용 가능하다.)

### 4. 로고 교체 실행
```bash
for p in 03 04 05 06 13; do
  python3 .claude/skills/doc-inbox-rebrand/debrand-slide.py \
    "<SCRATCH>/page-$p.png" doc-inbox/logo/uengine.png \
    "images/<slug>/arch-XX-설명.png"
done
```
스크립트는 박스 바로 위 한 줄에서 배경색을 **페이지마다 새로 샘플링**하므로 크림색/연회색/흰색 배경이 섞여 있어도 자연스럽게 채워진다. 결과를 `Read`로 반드시 육안 확인한다 (겹침·색 튐 여부).

### 5. 용량 최적화
NotebookLM 렌더는 페이지당 1MB 이상으로 무겁다. `pngquant`/`optipng`이 없는 환경에서는 PIL 팔레트 양자화로 용량을 절반 이하로 줄인다:
```python
from PIL import Image
im = Image.open(f).convert("RGB")
im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG).save(f, optimize=True)
```

### 6. 원본 PDF를 다운로드 리소스로 반영
사이트 관례상 PDF는 `images/` 루트에 두고 버튼으로 연결한다 (`contents/processgpt.html` 참고):
```bash
cp "doc-inbox/<file>.pdf" "images/<Product-Name>.pdf"
```
```html
<a target="_blank" href="../images/<Product-Name>.pdf" class="btn btn-mod btn-w btn-large btn-round btn-hover-anim" style="border: 2px solid #111;">
    <span style="font-size: 16px;">소개서(PDF) 다운로드</span>
</a>
```

### 7. 원본 정리
전 단계가 성공적으로 끝나 이미지/PDF가 홈페이지 안으로 옮겨지고, 상위 스킬(add-product-menu 등)의
로컬 서버 렌더 검증까지 통과했다면 **자동으로** `doc-inbox/`의 원본 PDF(`doc-inbox/logo/` 제외)를
삭제한다 — 확인을 구할 필요 없이 바로 지운다. doc-inbox는 임시 수신함이며, 반영이 끝난 원본을
남겨둘 이유가 없다. 단, 반영/검증 단계가 실패했거나 결과가 불확실하면 삭제하지 않고 사용자에게
알린다 (되돌리기 어려운 삭제이므로 확신이 없을 때만 예외적으로 확인을 구한다).

## 산출물
- `images/<slug>/arch-*.png` — 로고 교체된 아키텍처/다이어그램 이미지
- `images/<Product-Name>.pdf` — 다운로드용 원본 PDF 사본
- (호출한 상위 스킬이 있다면) 해당 상세 페이지에 이미지 섹션 + PDF 다운로드 버튼 삽입

## 헬퍼
- `.claude/skills/doc-inbox-rebrand/debrand-slide.py` — 워터마크 박스를 배경색으로 덮고 uEngine 로고를 같은 자리에 합성.

## 체크리스트
- [ ] 전 페이지 동일 DPI로 렌더링 (워터마크 좌표 고정 전제)
- [ ] 워터마크 박스 좌표를 콘텐츠 적은 페이지에서 먼저 검증
- [ ] 교체 결과 전부 `Read`로 육안 확인 (겹침/이색 없는지)
- [ ] 큰 PNG는 팔레트 양자화로 용량 절감
- [ ] 원본 PDF도 `images/`에 복사해 "소개서(PDF) 다운로드" 버튼으로 연결
- [ ] 반영 + 렌더 검증까지 통과하면 원본 doc-inbox PDF 자동 삭제 (실패/불확실할 때만 확인 후 보류)
