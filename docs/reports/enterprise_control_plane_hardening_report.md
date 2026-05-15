# Enterprise Control Plane Hardening Report

## What was broken

- Import/API compatibility issues (`value_os.value_ledger` API mismatch).
- Missing `governance_os.runtime_decision.decide`.
- No unified tenant-aware control-plane modules for Systems 26–35.
- No dedicated hardening tests for rollback/policy/agent mesh/contracts/safety/value/self-evolving E2E.

## What was fixed

- Added `RuntimeDecision` + `decide()` in `governance_os.runtime_decision`.
- Restored `value_os.value_ledger` compatibility (`add_event`, `list_events`, `summarize`, discipline checks).
- Added enterprise modules:
  - `control_plane_os`
  - `agent_mesh_os`
  - `assurance_contract_os`
  - `runtime_safety_os`
  - `value_engine_os`
  - `self_evolving_os`
- Added targeted tests including `test_enterprise_control_plane_e2e.py`.
- Added verification script and CI workflow for release gates.

## What remains MVP

- Agent mesh/contracts/control-plane stores are still in-memory by default.
- JSONL fallback is still used when Postgres is not configured.
- Frontend control surfaces are still partial/TODO.
- Sandbox replay and org-graph integration need deeper runtime wiring.

## Production readiness status

| Area | Status | Evidence |
|---|---|---|
| API import | PASS | `python3 -c "from api.main import app"` |
| Control plane | PASS | rollback/policy + e2e tests |
| Tenant isolation | PASS | `tests/test_tenant_isolation_systems_26_35.py` |
| Approval gate | PASS | rollback/policy/self-evolving tests |
| Postgres persistence | PARTIAL | `PostgresControlLedger` + pending full DB rollout |
| Frontend | TODO | pending control-surface pages rollout |

## Next milestones

1. Switch runtime stores to Postgres-backed repositories in production paths.
2. Build/ship frontend control surfaces (`/control-plane`, `/approvals`, `/agents`, `/safety`, `/value-engine`, `/self-evolving`).
3. Add sandbox replay + org-graph incident impact test coverage.
4. Expand CI to include integration tests against real Postgres.
