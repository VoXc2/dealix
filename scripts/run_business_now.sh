#!/usr/bin/env bash
# One command — Business NOW snapshot (verify + KPI platform + markdown evidence).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="${DEALIX_PYTHON_BIN:-}"
if [[ -z "${PYTHON_BIN}" || ! -x "${PYTHON_BIN}" ]]; then
  if [[ -x "${ROOT}/.venv/bin/python" ]]; then
    PYTHON_BIN="${ROOT}/.venv/bin/python"
  else
    COMMON_GIT_DIR="$(git -C "${ROOT}" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
    COMMON_ROOT=""
    if [[ -n "${COMMON_GIT_DIR}" ]]; then
      COMMON_ROOT="$(dirname "${COMMON_GIT_DIR}")"
    fi
    if [[ -n "${COMMON_ROOT}" && -x "${COMMON_ROOT}/.venv/bin/python" ]]; then
      PYTHON_BIN="${COMMON_ROOT}/.venv/bin/python"
    else
      PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
    fi
  fi
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "BUSINESS_NOW: FAIL — python3 not found"
  exit 1
fi

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
