#!/usr/bin/env bash
# PostToolUse 훅 — Write/Edit 로 사이트 HTML 페이지가 바뀌면 그 페이지의 SEO 메타를 즉시 재적용한다.
#
# stdin: Claude Code 훅 JSON
# exit 0 : 조용히 통과 (대상 아님 / 문제 없음)
# exit 2 : stderr 내용이 Claude 에게 전달됨 (큐레이션이 필요한 경고가 있을 때만)
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT" || exit 0

payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)
[ -z "$file" ] && exit 0

# 절대경로를 저장소 상대경로로
rel="${file#"$ROOT"/}"

# 사이트 페이지만 대상 (index.html, contents/**.html)
case "$rel" in
    index.html|contents/*.html) ;;
    *) exit 0 ;;
esac
[ -f "$rel" ] || exit 0

out=$(python3 .claude/skills/seo-optimize/apply_seo.py --only "$rel" 2>&1)
status=$?

if [ $status -ne 0 ]; then
    printf 'SEO 훅 실행 실패 (%s):\n%s\n' "$rel" "$out" >&2
    exit 2
fi

if printf '%s' "$out" | grep -q '확인 필요'; then
    {
        echo "[seo-optimize] $rel 의 SEO 메타를 자동 적용했지만 사람이 채워야 할 항목이 남아 있습니다."
        echo "$out" | sed -n '/확인 필요/,$p'
        echo
        echo "대응: 블로그·뉴스 글이면 contents/bloglist.html 또는 contents/newsroom.html 에 카드를 추가하고,"
        echo "      그 외 페이지면 .claude/skills/seo-optimize/seo-meta.json 의 pages[\"$rel\"] 에 title/description 을 작성한 뒤"
        echo "      python3 .claude/skills/seo-optimize/apply_seo.py 를 실행하세요."
    } >&2
    exit 2
fi

exit 0
