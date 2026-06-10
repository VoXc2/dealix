#!/usr/bin/env bash
# Unified official commercial launch gate — Founder OS + commercial launch + company ready + daily ops dry-run.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

FAIL=0

echo "== Dealix commercial go-live (unified) =="
echo ""

echo "== 1/4 Founder operating system =="
if bash "$ROOT/scripts/verify_founder_operating_system.sh"; then
  echo ""
else
  FAIL=1
  echo ""
fi

echo "== 2/4 Commercial soft launch =="
PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "  FAIL: python not found"
  FAIL=1
else
  LAUNCH_ARGS=()
  if [[ "${DEALIX_VERIFY_WITH_API:-}" == "1" ]]; then
    LAUNCH_ARGS+=(--with-api)
  fi
  if [[ "${DEALIX_VERIFY_WITH_FRONTEND_BUILD:-}" == "1" ]]; then
    LAUNCH_ARGS+=(--with-frontend-build)
  fi
  if "$PYTHON_BIN" "$ROOT/scripts/verify_commercial_launch_ready.py" "${LAUNCH_ARGS[@]}"; then
    echo ""
  else
    FAIL=1
    echo ""
  fi
fi

echo "== 3/4 Company ready (skip founder go-live) =="
if bash "$ROOT/scripts/company_ready_verify.sh" --skip-go-live; then
  echo ""
else
  FAIL=1
  echo ""
fi

echo "== 4/4 Daily ops dry-run =="
if [[ -n "${PYTHON_BIN:-}" ]]; then
  if "$PYTHON_BIN" "$ROOT/scripts/run_dealix_daily_ops.py" --dry-run --skip-api; then
    echo ""
  else
    FAIL=1
    echo ""
  fi
else
  FAIL=1
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "DEALIX_COMMERCIAL_GO_LIVE_VERDICT=PASS"
  echo "DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS"
  echo "Next: bash scripts/run_founder_commercial_day.sh"
  echo "Doc: docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md"
  exit 0
fi

echo "DEALIX_COMMERCIAL_GO_LIVE_VERDICT=FAIL"
echo "DEALIX_OFFICIAL_LAUNCH_VERDICT=FAIL"
exit 1
