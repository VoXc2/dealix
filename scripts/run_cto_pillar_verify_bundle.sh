#!/usr/bin/env bash
# CTO pillar verify: full transformation bundle + control plane + gap matrix checks.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"

cd "$ROOT"

echo "== Pillar bundle: global AI transformation =="
bash "${ROOT}/scripts/run_global_ai_transformation_bundle.sh"

echo ""
echo "== Pillar bundle: enterprise control plane =="
bash "${ROOT}/scripts/verify_enterprise_control_plane.sh"

echo ""
echo "== Pillar bundle: gap matrix spot checks =="
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-jsonl
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-observability
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-reliability
"$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-enterprise-package

echo ""
echo "CTO_PILLAR_VERIFY_BUNDLE: PASS"
