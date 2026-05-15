# Dealix Enterprise Control Plane Scorecard

| Gate | Required | Status | Evidence |
|---|---:|---|---|
| API Import | 100% | Pass | `python3 -c "from api.main import app"` |
| Tenant Isolation | 100% | Pass | `tests/test_tenant_isolation_systems_26_35.py` |
| Control Plane | 95% | Pass | `tests/test_control_plane_rollback_flow.py` + `tests/test_control_plane_policy_edit_flow.py` |
| Approval Gate | 95% | Pass | `tests/test_control_plane_rollback_flow.py` |
| Agent Mesh | 90% | Pass | `tests/test_agent_mesh_tenant_and_routing.py` |
| Assurance Contracts | 95% | Pass | `tests/test_assurance_contracts_enterprise_rules.py` |
| Runtime Safety | 95% | Pass | `tests/test_runtime_safety_propagation.py` |
| Value Engine | 90% | Pass | `tests/test_value_engine_source_discipline.py` |
| E2E Workflow | 100% | Pass | `tests/test_enterprise_control_plane_e2e.py` |
| Frontend Control UI | 80% | Pass | `apps/web/app/*` + walkthrough artifacts |
| CI Gates | 100% | Pass | `.github/workflows/enterprise-control-plane.yml` |
