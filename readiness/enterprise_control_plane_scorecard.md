# Dealix Enterprise Control Plane Scorecard

| Layer | Required Score | Current | Evidence | Status |
|---|---:|---:|---|---|
| API import health | 100 | 100 | `python3 -c "from api.main import app; print('api import ok')"` | PASS |
| Tenant isolation | 95 | 88 | `tests/test_tenant_isolation_systems_26_35.py` | PARTIAL |
| Control plane | 90 | 86 | `tests/test_control_plane_rollback_flow.py`, `tests/test_control_plane_policy_edit_flow.py` | PARTIAL |
| Approval gate | 95 | 90 | approval flow tests + `control_plane_os.approval_gate` | PARTIAL |
| Agent mesh | 90 | 87 | `tests/test_agent_mesh_tenant_and_routing.py` | PARTIAL |
| Assurance contracts | 95 | 91 | `tests/test_assurance_contracts_enterprise_rules.py` | PARTIAL |
| Runtime safety | 95 | 88 | `tests/test_runtime_safety_propagation.py` | PARTIAL |
| Sandbox/replay | 85 | 70 | tenant schemas added, replay pending | PARTIAL |
| Org graph | 80 | 68 | tenant-aware schema in place, runtime integration pending | PARTIAL |
| Human-AI oversight | 90 | 82 | approval queue + escalation schemas/tests in E2E | PARTIAL |
| Value engine | 90 | 88 | `tests/test_value_engine_source_discipline.py` | PARTIAL |
| Self-evolving | 90 | 85 | `tests/test_self_evolving_approval_gate.py` | PARTIAL |
| Frontend control surfaces | 80 | 55 | pages/components planned and partially scaffolded | TODO |
| CI release gates | 95 | 80 | `.github/workflows/enterprise-control-plane.yml` | PARTIAL |
