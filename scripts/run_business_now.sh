#!/usr/bin/env bash
# One command — Business NOW snapshot (verify + KPI platform + markdown evidence).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"

cd "$ROOT"

echo "== Business NOW: platform KPI signals =="
"$PYTHON_BIN" "${ROOT}/scripts/populate_kpi_baselines_platform_signals.py"

echo ""
echo "== Business NOW: commercial registry status =="
"$PYTHON_BIN" "${ROOT}/scripts/apply_kpi_founder_commercial.py" --status || true

echo ""
echo "== Business NOW: enterprise control plane (optional) =="
if [[ -f "${ROOT}/scripts/verify_enterprise_control_plane.sh" ]]; then
  bash "${ROOT}/scripts/verify_enterprise_control_plane.sh" || true
fi

echo ""
echo "== Business NOW: generate snapshot =="
"$PYTHON_BIN" "${ROOT}/scripts/generate_business_now_snapshot.py"

echo ""
echo "== Business NOW: commercial strategy doc =="
"$PYTHON_BIN" "${ROOT}/scripts/generate_commercial_strategy_doc.py"

echo ""
echo "BUSINESS_NOW: OK"
echo "UI: /ar/business-now"
echo "API: GET /api/v1/business-now/snapshot"
