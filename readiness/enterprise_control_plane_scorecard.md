# Dealix Enterprise Control Plane Scorecard

Status as of the control-plane hardening branch. Evidence is the command
or test that proves the gate — run `bash scripts/verify_enterprise_control_plane.sh`
to re-prove the whole row set.

| Gate | Required | Status | Evidence |
|---|---:|---|---|
| API import | 100% | PASS | `python -c "from api.main import app"` (760 routes) |
| Compile sanity | 100% | PASS | `python -m compileall api auto_client_acquisition` |
| Ruff (control-plane scope) | 100% | PASS | `ruff check` on control modules + proof tests |
| Tenant isolation | 100% | PASS | `tests/test_tenant_isolation_systems_26_35.py` |
| Control Plane rollback | 95% | PASS | `tests/test_control_plane_rollback_flow.py` |
| Policy-change approval gate | 95% | PASS | `tests/test_control_plane_policy_edit_flow.py` |
| Agent governance / routing | 90% | PASS | `tests/test_agent_mesh_tenant_and_routing.py` |
| Deny-by-default + evidence | 95% | PASS | `tests/test_assurance_contracts_enterprise_rules.py` |
| Runtime safety propagation | 95% | PASS | `tests/test_runtime_safety_propagation.py` |
| Value source discipline | 90% | PASS | `tests/test_value_engine_source_discipline.py` |
| Self-evolving approval gate | 95% | PASS | `tests/test_self_evolving_approval_gate.py` |
| End-to-end control flow | 100% | PASS | `tests/test_enterprise_control_plane_e2e.py` |
| CI release gate | 100% | PASS | `.github/workflows/enterprise-control-plane.yml` |
| Postgres persistence | — | MVP / DEFERRED | in-memory stores, tenant-keyed; migration is a follow-up |
| Frontend control surfaces | — | DEFERRED | `frontend/` has `/agents` + `/approvals`; control-plane pages not in this round |

## Definition of Done

`bash scripts/verify_enterprise_control_plane.sh` exits 0 and prints
`ENTERPRISE CONTROL PLANE: PASS`.
