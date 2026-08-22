#!/usr/bin/env bash
# Verify Founder Operating System wiring (dry-run + pytest bundle).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ensure_runtime="$ROOT/scripts/ops/ensure_founder_automation_python.sh"
if [[ ! -f "$ensure_runtime" ]]; then
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
  echo "automation python bootstrap is missing: $ensure_runtime"
  exit 1
fi

# Scheduled VPS verification must not silently fall back to a system Python that
# lacks the repository's declared test/application dependencies. The bootstrap
# is idempotent and syncs only when requirements-dev.txt changes or imports fail.
RUNTIME_OUT="$(bash "$ensure_runtime" 2>&1)" || {
  printf '%s\n' "$RUNTIME_OUT"
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
  exit 1
}
printf '%s\n' "$RUNTIME_OUT"

PYTHON_BIN="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
  echo "automation python is not executable: $PYTHON_BIN"
  exit 1
fi
if ! "$PYTHON_BIN" -c 'import pydantic, pytest' >/dev/null 2>&1; then
  echo "FOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
  echo "automation python does not provide pydantic + pytest: $PYTHON_BIN"
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
