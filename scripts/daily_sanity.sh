#!/usr/bin/env bash
# Daily sanity gate — one command that runs everything CI runs locally.
# Exit 0 = safe to push.  Non-zero = something broke and CI will catch it.
#
# Usage:  ./scripts/daily_sanity.sh          (full)
#         ./scripts/daily_sanity.sh --fast   (skip full pytest, only changed files)

set -euo pipefail

# Color codes (skip if non-TTY)
if [ -t 1 ]; then
  RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[0;33m'; BLUE=$'\033[0;34m'; RESET=$'\033[0m'
else
  RED=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FAST_MODE=0
if [ "${1:-}" = "--fast" ]; then
  FAST_MODE=1
fi

failed_steps=()
step() {
  local name="$1"; shift
  printf "%b▶%b %s ... " "$BLUE" "$RESET" "$name"
  if "$@" > /tmp/sanity.out 2>&1; then
    printf "%b✓%b\n" "$GREEN" "$RESET"
  else
    printf "%b✗%b\n" "$RED" "$RESET"
    failed_steps+=("$name")
    sed 's/^/    /' /tmp/sanity.out | tail -20
  fi
}

step "compile-all (api + auto_client_acquisition)" \
  python -m compileall -q api auto_client_acquisition

step "service readiness matrix verify" \
  python scripts/verify_service_readiness_matrix.py

step "service readiness JSON freshness" bash -c '
  python scripts/export_service_readiness_json.py > /dev/null 2>&1
  git diff --exit-code -- landing/assets/data/service-readiness.json
'

step "SEO audit JSON freshness" bash -c '
  python scripts/seo_audit.py > /dev/null 2>&1
  git diff --exit-code -- docs/SEO_AUDIT_REPORT.json
'

if [ "$FAST_MODE" = "0" ]; then
  step "pytest (full)" \
    pytest -q --no-cov tests/
else
  CHANGED=$(git diff --name-only --diff-filter=ACMRTUXB HEAD origin/main 2>/dev/null | grep -E '^tests/.*\.py$' || true)
  if [ -z "$CHANGED" ]; then
    echo "${YELLOW}▶${RESET} pytest (fast) — no test changes vs main, skipping"
  else
    step "pytest (changed only)" \
      pytest -q --no-cov $CHANGED
  fi
fi

step "preflight (dev mode)" \
  python scripts/preflight_check.py --dev --json

echo
if [ ${#failed_steps[@]} -eq 0 ]; then
  printf "%b✓ ALL SANITY CHECKS PASSED%b — safe to push\n" "$GREEN" "$RESET"
  exit 0
else
  printf "%b✗ %d STEP(S) FAILED:%b\n" "$RED" "${#failed_steps[@]}" "$RESET"
  for s in "${failed_steps[@]}"; do
    printf "  - %s\n" "$s"
  done
  exit 1
fi
