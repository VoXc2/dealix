#!/usr/bin/env bash
# Executive weekly checklist: CEO proof pack + transformation verify + audit log line.
# See docs/transformation/README.md (Executive operating checklist).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"
DATE_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG="${ROOT}/docs/transformation/evidence/weekly_ops_checklist.log"
TMP_VERIFY="$(mktemp)"

bash "${ROOT}/scripts/run_ceo_signal_weekly_loop.sh"

VERIFY_STATUS="FAIL"
if "$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" >"$TMP_VERIFY" 2>&1; then
  VERIFY_STATUS="PASS"
else
  cat "$TMP_VERIFY" >&2
  rm -f "$TMP_VERIFY"
  exit 1
fi
rm -f "$TMP_VERIFY"

mkdir -p "$(dirname "$LOG")"
echo "${DATE_UTC} verify_global_ai_transformation=${VERIFY_STATUS}" >>"$LOG"

if [[ "${VERIFY_STATUS}" == "PASS" ]]; then
  "$PYTHON_BIN" "${ROOT}/scripts/sync_weekly_ops_from_checklist_log.py" || true
fi

echo ""
echo "Executive checklist: OK"
echo "Next: fill dealix/transformation/kpi_baselines.yaml (value_numeric + source_ref + updated_period_iso)."
echo "Review: dealix/transformation/ownership_matrix.yaml human_assignee fields."
echo "Audit log appended: ${LOG}"
echo "Optional dry-run sync: python3 scripts/sync_weekly_ops_from_checklist_log.py --dry-run"
