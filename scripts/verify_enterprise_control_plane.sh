#!/usr/bin/env bash
# Enterprise Control Plane — single proof gate.
#
# Exits 0 and prints "ENTERPRISE CONTROL PLANE: PASS" only when every
# check below passes. This is the Definition of Done for the control
# plane hardening: code compiles, the API imports, the control modules
# lint clean, and all 10 proof tests pass.
#
# Opt-in: set RUN_REVENUE_OS_MASTER=1 to also chain the existing
# scripts/revenue_os_master_verify.sh (slower, broader).
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"

# Control-plane modules touched by the hardening — ruff is scoped to
# these (plus the proof tests) so pre-existing lint debt elsewhere in
# the repo does not mask a regression here.
CP_MODULES=(
  auto_client_acquisition/governance_os/runtime_decision.py
  auto_client_acquisition/institutional_control_os/run_registry.py
  auto_client_acquisition/evidence_control_plane_os/evidence_store.py
  auto_client_acquisition/evidence_control_plane_os/evidence_object.py
  auto_client_acquisition/secure_agent_runtime_os/agent_isolation.py
  auto_client_acquisition/value_os/value_ledger.py
  auto_client_acquisition/data_os/import_preview.py
  auto_client_acquisition/data_os/data_quality_score.py
  auto_client_acquisition/data_os/source_passport.py
  auto_client_acquisition/agent_os/agent_card.py
  auto_client_acquisition/agent_os/agent_registry.py
  auto_client_acquisition/agent_governance/schemas.py
  auto_client_acquisition/approval_center/schemas.py
  auto_client_acquisition/approval_center/approval_store.py
)

CP_TESTS=(
  tests/test_api_imports.py
  tests/test_tenant_isolation_systems_26_35.py
  tests/test_control_plane_rollback_flow.py
  tests/test_control_plane_policy_edit_flow.py
  tests/test_agent_mesh_tenant_and_routing.py
  tests/test_assurance_contracts_enterprise_rules.py
  tests/test_runtime_safety_propagation.py
  tests/test_value_engine_source_discipline.py
  tests/test_self_evolving_approval_gate.py
  tests/test_enterprise_control_plane_e2e.py
)

echo "== 1/4 Compile sanity =="
"$PYTHON" -m compileall -q api auto_client_acquisition
echo "compileall ok"

echo "== 2/4 API import =="
"$PYTHON" -c "from api.main import app; print('api import ok -', len(app.routes), 'routes')"

echo "== 3/4 Ruff (control-plane scope) =="
ruff check "${CP_MODULES[@]}" "${CP_TESTS[@]}"
echo "ruff ok"

echo "== 4/4 Control Plane proof tests =="
"$PYTHON" -m pytest "${CP_TESTS[@]}" -q --no-cov

if [[ "${RUN_REVENUE_OS_MASTER:-0}" == "1" ]]; then
  echo "== Optional: Revenue OS master verify =="
  bash scripts/revenue_os_master_verify.sh
fi

echo ""
echo "ENTERPRISE CONTROL PLANE: PASS"
