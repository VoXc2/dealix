#!/usr/bin/env bash
# Global AI Company Transformation — full verification bundle (blueprint execution gate).
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="$(command -v python3 2>/dev/null || command -v py 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python3 not found" >&2
  exit 1
fi
if [[ "${PYTHON_BIN}" == *py ]]; then
  PYTHON_BIN="py -3"
fi

echo "== Global AI Transformation (artifacts + modules) =="
$PYTHON_BIN scripts/verify_global_ai_transformation.py

echo "== Per-initiative checks (12) =="
for id in doctrine-lock gap-closure enterprise-package governance-expansion \
  data-flywheel reliability-program observability-contracts gtm-system \
  unit-economics delivery-control-tower org-operating-system category-dominance; do
  $PYTHON_BIN scripts/verify_global_ai_transformation.py --check "$id"
done

echo "== Specialized gates =="
$PYTHON_BIN scripts/verify_global_ai_transformation.py --check-jsonl
$PYTHON_BIN scripts/verify_global_ai_transformation.py --check-observability
$PYTHON_BIN scripts/verify_global_ai_transformation.py --check-enterprise-package
$PYTHON_BIN scripts/verify_global_ai_transformation.py --check-reliability
$PYTHON_BIN scripts/verify_global_ai_transformation.py --check-category-expansion

echo "== Weekly proof pack (sanity) =="
$PYTHON_BIN scripts/generate_weekly_operating_proof_pack.py >/dev/null

echo "== Reliability drills scorecard =="
$PYTHON_BIN scripts/reliability_drills_scorecard.py

echo "== Enterprise control plane =="
bash scripts/verify_enterprise_control_plane.sh

echo "== Revenue OS spine =="
bash scripts/revenue_os_master_verify.sh

echo "GLOBAL_AI_TRANSFORMATION_BUNDLE: PASS"
