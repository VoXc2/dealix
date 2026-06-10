#!/usr/bin/env bash
#
# CI watch — Wave 15 (A8).
#
# Polls the GitHub Actions runs on the current branch (or `main`) and
# surfaces failed runs with a 1-line root-cause guess. Use to watch
# CI status after pushing a commit; exits 0 when all checks are green.
#
# Requires `gh` CLI (optional) or falls back to git + GitHub-MCP path.
# When `gh` is missing it just prints the URLs the founder should open.
#
# Usage:
#   bash scripts/ci_watch.sh                    # watch current branch
#   bash scripts/ci_watch.sh main               # watch main
#   bash scripts/ci_watch.sh main 30            # poll every 30s instead of 60
set -u

BRANCH="${1:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)}"
INTERVAL="${2:-60}"

if ! command -v gh >/dev/null 2>&1; then
    echo "⚠ gh CLI not installed — cannot watch CI from terminal."
    echo "  Open https://github.com/VoXc2/dealix/actions?query=branch%3A$BRANCH"
    echo "  to inspect CI manually."
    exit 0
fi

remote_url=$(git config --get remote.origin.url 2>/dev/null || echo "")
echo "━━ CI watch — branch=$BRANCH · poll=${INTERVAL}s ━━"
echo "Repo: ${remote_url}"
echo

while true; do
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    runs=$(gh run list --branch "$BRANCH" --limit 6 --json status,conclusion,name,createdAt,databaseId 2>/dev/null || echo "[]")
    if [[ "$runs" == "[]" ]]; then
        echo "[$ts] no recent runs"
        sleep "$INTERVAL"
        continue
    fi

    all_green=true
    in_progress=false
    while IFS=$'\t' read -r status conclusion name id; do
        case "$conclusion" in
            success) emoji="✓" ;;
            failure) emoji="✗"; all_green=false ;;
            cancelled) emoji="○"; all_green=false ;;
            "") emoji="…"; in_progress=true; all_green=false ;;
            *) emoji="?" ;;
        esac
        echo "[$ts] $emoji $name (status=$status conclusion=${conclusion:-pending} id=$id)"
        if [[ "$conclusion" == "failure" ]]; then
            # 1-line root-cause guess by looking at the run logs
            log_tail=$(gh run view "$id" --log-failed 2>/dev/null | tail -5 | tr '\n' ' ' | cut -c -150)
            if [[ -n "$log_tail" ]]; then
                echo "    └─ tail: $log_tail"
            fi
        fi
    done < <(echo "$runs" | jq -r '.[] | [.status,.conclusion,.name,.databaseId] | @tsv')

    echo

    if $all_green; then
        echo "✓ all CI checks green on $BRANCH"
        exit 0
    fi
    if ! $in_progress; then
        echo "⚠ some checks failed and none are running — fix + push to re-trigger"
        exit 1
    fi
    sleep "$INTERVAL"
done
