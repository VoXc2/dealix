#!/usr/bin/env bash
# Enterprise Control Plane — stability verification gate.
#
# Phase 1 (Stability) verification: compile health, API import health,
# lint on the stabilized governance/value/data modules, and the targeted
# test suites that prove the runtime decision, value ledger, and data
# quality compatibility layers.
#
# Usage: bash scripts/verify_enterprise_control_plane.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

echo "== Compile =="
python -m compileall -q api auto_client_acquisition

echo "== API import =="
python -c "from api.main import app; print('api import ok')"

echo "== Ruff (stabilized modules) =="
if command -v ruff >/dev/null 2>&1; then
  ruff check \
    auto_client_acquisition/governance_os/runtime_decision.py \
    auto_client_acquisition/value_os/value_ledger.py \
    auto_client_acquisition/data_os/import_preview.py \
    auto_client_acquisition/data_os/data_quality_score.py \
    auto_client_acquisition/data_os/source_passport.py \
    api/routers/data_os.py \
    api/routers/value_os.py
else
  echo "ruff not installed — skip"
fi

echo "== Targeted tests =="
python -m pytest -q --no-cov \
  tests/test_governance_runtime_decision.py \
  tests/test_value_os.py \
  tests/test_data_os_router.py \
  tests/test_data_os_quality.py \
  tests/test_data_os_helpers.py \
  tests/test_data_os_source_passport_bridge.py

echo ""
echo "ENTERPRISE CONTROL PLANE: PASS"
