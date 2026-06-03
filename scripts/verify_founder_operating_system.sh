#!/usr/bin/env bash
# Verify Founder Operating System wiring (dry-run + pytest bundle).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
  echo "python3 not found"
  exit 1
fi

FAIL=0

echo "== 1/2 Founder commercial day dry-run =="
if ! bash "$ROOT/scripts/run_founder_commercial_day.sh" --dry-run; then
  FAIL=1
fi

echo ""
echo "== 2/2 pytest bundle =="
TESTS=(
  tests/test_founder_revenue_day_script.py
  tests/test_targeting_rotation.py
  tests/test_outreach_drafts.py
  tests/test_generate_weekly_content_drafts.py
  tests/test_commercial_ops_digest.py
)
if ! "$PYTHON_BIN" -m pytest "${TESTS[@]}" -q --no-cov; then
  FAIL=1
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo ""
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=PASS"
  exit 0
fi

echo ""
echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
exit 1
