#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="$(command -v python3)"

echo "== Compile =="
"$PYTHON_BIN" -m compileall api auto_client_acquisition

echo "== API import =="
"$PYTHON_BIN" -c "from api.main import app; print('api import ok')"

echo "== Ruff =="
ruff check \
  api/routers/control_plane_os.py \
  api/routers/agent_mesh_os.py \
  api/routers/assurance_contract_os.py \
  api/routers/sandbox_os.py \
  api/routers/org_graph_os.py \
  api/routers/runtime_safety_os.py \
  api/routers/simulation_os.py \
  api/routers/human_ai_os.py \
  api/routers/value_engine_os.py \
  api/routers/self_evolving_os.py \
  auto_client_acquisition/governance_os/runtime_decision.py \
  auto_client_acquisition/control_plane_os \
  auto_client_acquisition/agent_mesh_os \
  auto_client_acquisition/assurance_contract_os \
  auto_client_acquisition/runtime_safety_os \
  auto_client_acquisition/value_engine_os \
  auto_client_acquisition/self_evolving_os \
  auto_client_acquisition/sandbox_os \
  auto_client_acquisition/org_graph_os \
  auto_client_acquisition/simulation_os \
  auto_client_acquisition/human_ai_os \
  tests/test_api_imports.py \
  tests/test_tenant_isolation_systems_26_35.py \
  tests/test_control_plane_rollback_flow.py \
  tests/test_control_plane_policy_edit_flow.py \
  tests/test_agent_mesh_tenant_and_routing.py \
  tests/test_assurance_contracts_enterprise_rules.py \
  tests/test_runtime_safety_propagation.py \
  tests/test_value_engine_source_discipline.py \
  tests/test_self_evolving_approval_gate.py \
  tests/test_enterprise_control_plane_e2e.py \
  tests/test_postgres_control_ledger.py

echo "== Control Plane Tests =="
pytest tests/test_api_imports.py -q
pytest tests/test_tenant_isolation_systems_26_35.py -q
pytest tests/test_control_plane_rollback_flow.py -q
pytest tests/test_control_plane_policy_edit_flow.py -q
pytest tests/test_agent_mesh_tenant_and_routing.py -q
pytest tests/test_assurance_contracts_enterprise_rules.py -q
pytest tests/test_runtime_safety_propagation.py -q
pytest tests/test_value_engine_source_discipline.py -q
pytest tests/test_self_evolving_approval_gate.py -q
pytest tests/test_enterprise_control_plane_e2e.py -q
pytest tests/test_postgres_control_ledger.py -q

echo "== Revenue OS Master Verify =="
DEALIX_SKIP_RUFF=1 bash scripts/revenue_os_master_verify.sh

echo "ENTERPRISE CONTROL PLANE: PASS"
