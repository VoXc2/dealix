#!/usr/bin/env bash
set -euo pipefail

echo "== Compile =="
python3 -m compileall api auto_client_acquisition

echo "== API import =="
python3 -c "from api.main import app; print('api import ok')"

echo "== Ruff =="
ruff check \
  auto_client_acquisition/governance_os/runtime_decision.py \
  auto_client_acquisition/value_os/value_ledger.py \
  auto_client_acquisition/data_os/data_quality_score.py \
  auto_client_acquisition/data_os/import_preview.py \
  auto_client_acquisition/data_os/source_passport.py \
  auto_client_acquisition/control_plane_os \
  auto_client_acquisition/agent_mesh_os \
  auto_client_acquisition/assurance_contract_os \
  auto_client_acquisition/runtime_safety_os \
  auto_client_acquisition/value_engine_os \
  auto_client_acquisition/self_evolving_os \
  tests/test_api_imports.py \
  tests/test_tenant_isolation_systems_26_35.py \
  tests/test_control_plane_rollback_flow.py \
  tests/test_control_plane_policy_edit_flow.py \
  tests/test_agent_mesh_tenant_and_routing.py \
  tests/test_assurance_contracts_enterprise_rules.py \
  tests/test_runtime_safety_propagation.py \
  tests/test_value_engine_source_discipline.py \
  tests/test_self_evolving_approval_gate.py \
  tests/test_postgres_control_ledger.py \
  tests/test_enterprise_control_plane_e2e.py

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
pytest tests/test_postgres_control_ledger.py -q
pytest tests/test_enterprise_control_plane_e2e.py -q

echo "== Revenue OS Master Verify =="
bash scripts/revenue_os_master_verify.sh

echo "ENTERPRISE CONTROL PLANE: PASS"
