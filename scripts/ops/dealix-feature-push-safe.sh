#!/usr/bin/env bash
# dealix-feature-push-safe — bounded push for feature branches (no force, no main)
set -Eeuo pipefail
BRANCH="${1:-$(git branch --show-current)}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
if [[ "$BRANCH" == "main" ]]; then
  echo "BLOCKED: cannot push main directly"
  exit 1
fi
if [[ "$BRANCH" == "master" || "$BRANCH" == "production" ]]; then
  echo "BLOCKED: protected branch $BRANCH"
  exit 1
fi
if git rev-parse --verify "origin/$BRANCH" >/dev/null 2>&1; then
  # Check fast-forward
  if ! git merge-base --is-ancestor "origin/$BRANCH" HEAD; then
    echo "BLOCKED: non-fast-forward — need rebase/merge first, no --force"
    exit 1
  fi
fi
# Secret check
if git diff origin/main...HEAD | grep -qiE "(sk_live|ghp_|AKIA)"; then
  echo "BLOCKED: possible secret"
  exit 1
fi
echo "SAFE PUSH: $BRANCH -> origin/$BRANCH"
exec git push origin "$BRANCH"
