#!/usr/bin/env bash
# =============================================================================
# CEO one-session readiness wrapper
# =============================================================================
# Pure orchestration of EXISTING checks — no new verification logic. Runs the
# Gate-2 readiness surface in one command and prints a single pass/fail summary.
#
# Order:
#   1. verify_global_ai_transformation.py  — governance imports + KPI honesty
#   2. business_readiness_verify.sh        — business readiness
#   3. check_alembic_single_head.py        — single migration head
#   4. verify_dealix_ready.py              — Dealix stage gates
#
# Every check runs even if an earlier one fails, so the founder sees the full
# picture. Exit 0 only if all checks pass.
#
# Usage:
#   bash scripts/run_ceo_one_session_readiness.sh
# =============================================================================
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PASS=()
FAIL=()

run_check() {
  local label="$1"
  shift
  echo ""
  echo "== ${label} =="
  if "$@"; then
    PASS+=("$label")
  else
    FAIL+=("$label")
  fi
}

run_check "verify_global_ai_transformation" \
  python3 scripts/verify_global_ai_transformation.py
run_check "business_readiness_verify" \
  bash scripts/business_readiness_verify.sh
run_check "check_alembic_single_head" \
  python3 scripts/check_alembic_single_head.py
run_check "verify_dealix_ready" \
  python3 scripts/verify_dealix_ready.py

echo ""
echo "=============================================================="
echo "READINESS SUMMARY"
for c in "${PASS[@]:-}"; do [ -n "$c" ] && echo "  PASS  $c"; done
for c in "${FAIL[@]:-}"; do [ -n "$c" ] && echo "  FAIL  $c"; done
echo "=============================================================="

if [ "${#FAIL[@]}" -gt 0 ]; then
  echo "RESULT: NOT READY — fix the failing checks above."
  exit 1
fi
echo "RESULT: READY"
exit 0
