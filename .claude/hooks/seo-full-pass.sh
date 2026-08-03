#!/usr/bin/env bash
# Stop 훅 — 응답이 끝날 때 HTML 이 바뀐 게 있으면 전체 SEO 패스를 돌려
# sitemap.xml / robots.txt 까지 최신 상태로 맞춘다.
#
# 항상 exit 0 (루프 방지). 결과는 systemMessage 로 사용자에게 보여준다.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT" || exit 0

# 변경된 HTML 이 없으면 조용히 종료
if ! git status --porcelain -- '*.html' 2>/dev/null | grep -q .; then
    exit 0
fi

out=$(python3 .claude/skills/seo-optimize/apply_seo.py 2>&1) || true

changed=$(printf '%s' "$out" | sed -n 's/.*중 \([0-9]*\)개 갱신.*/\1/p')
[ -z "$changed" ] && changed=0

# 아무것도 안 바뀌었고 경고도 없으면 조용히 종료
if [ "$changed" = "0" ] && ! printf '%s' "$out" | grep -q '확인 필요'; then
    exit 0
fi

msg=$(printf '%s' "$out" | grep -E '완료|확인 필요|^  !' | head -20)
jq -n --arg m "[seo-optimize] 전체 패스 완료 (sitemap.xml · robots.txt 갱신)
$msg" '{systemMessage: $m, suppressOutput: true}'
exit 0
