# Enterprise Control Plane — Readiness Scorecard

بطاقة جاهزية طبقة التحكم المؤسسية / Hardening status of the control-plane layer.

Companion to [`enterprise_control_plane_module_map.md`](enterprise_control_plane_module_map.md).
This scorecard tracks the **foundation slice** (Sprint 1) and records the
remaining sprints as `DEFERRED` so they are not lost.

## Foundation slice — current gates

| Gate | Evidence | Status |
|---|---|---|
| Container builds (deps install) | `scripts/web_session_setup.sh` | PASS |
| API import | `python -c "from api.main import app"` → 758 routes | PASS |
| Ruff — control-plane scope | `ruff check` over the 12 modules in the module map | PASS |
| Control-plane tests (green set) | `test_evidence_control_plane_os`, `test_institutional_control_os`, `test_governance_runtime_decision`, `test_tenant_isolation_v1`, `test_proof_ledger_postgres_backend`, `test_value_os` — 57 tests | PASS |
| One-command verify | `scripts/verify_enterprise_control_plane.sh` prints `ENTERPRISE CONTROL PLANE: PASS` | PASS |
| CI gate | `.github/workflows/enterprise-control-plane.yml` | PASS |

## Fixed in the foundation slice

- **`value_os/value_ledger.py`** was a half-finished stub. `monthly_report.py`
  and `api/routers/value_os.py` both depend on `ValueEvent`, `add_event`,
  `list_events`, `summarize`, `clear_for_test`, `ValueDisciplineError` — none
  existed. Implemented against the contract in `tests/test_value_os.py`
  (in-memory MVP store; tier sourcing discipline enforced).
- **Ruff** — 63 findings across the 12 control-plane modules cleared
  (autofixes + 6 manual: narrowed broad `except`, removed dead locals,
  inlined a boolean return, `# noqa` for an env-var-name false positive).

## Known issues parked (DEFERRED)

| Item | Detail |
|---|---|
| `api/routers/data_os.py` | Half-landed in commit `4687755`. Imports `compute_dq`, `preview`, `decide` — none exist; the router targets a `data_os` API surface that does not match the modules. **Disabled** (import + `include_router` commented out in `api/main.py`) so the API can start. Re-enable once the Data Pack DQ-scoring object, a CSV-preview object adapter, and a `governance_os` `decide()` engine are implemented with tests. |
| `tests/test_evidence_control_plane.py` | Stale vs. module churn — imports `build_control_graph` from `evidence_graph.py`, which only exports `mini_evidence_chain_complete`. |
| `tests/test_secure_agent_runtime.py` | Stale — imports `RuntimeState`; the module exports `AgentRuntimeState`. Likely more than a rename; needs reconciliation. |
| `scripts/revenue_os_master_verify.sh` | Independently `PARTIAL`: ~11 ruff findings in the revenue spine, and it calls bare `pytest` (the container's PATH `pytest` is an isolated uv-tool install without plugins — use `python -m pytest`). Not chained into the control-plane gate. |

## Remaining sprints (DEFERRED)

| Sprint | Scope | Status |
|---|---|---|
| Tenant isolation | `tenant_id` sweep across control-plane schemas. The DB layer already has `TenantRecord` + `tenant_id`; `ApprovalRequest` uses optional `customer_id` and the proof/value ledgers use `customer_handle` / `customer_id` strings — a real gap. | DEFERRED |
| Governance proof | Rollback-approval flow, policy-edit-approval flow, contract-gated agents, escalation tests. | DEFERRED |
| Safety + value | Kill-switch isolation tests, circuit-breaker tests, value source-discipline coverage. | DEFERRED |
| E2E proof | One complete revenue workflow exercising the full control plane end to end. | DEFERRED |
| Persistence | Postgres tables + repositories for `control_events`, `workflow_runs`, `approval_tickets` (currently in-memory / JSONL). | DEFERRED |
| Frontend control surfaces | Extend the existing Next.js app (`frontend/` already has `agents/`, `approvals/`, `dashboard/`) with run trace, kill-switch, and ROI views. | DEFERRED |
