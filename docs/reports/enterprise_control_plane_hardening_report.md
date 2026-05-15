# Enterprise Control Plane Hardening Report

Branch: `claude/harden-enterprise-control-plane-wOMql`

## Scope

Harden Dealix's enterprise governance layer to a Client-Pilot-Ready
state, proven by a single verify script — not by feeling or file count.
Per the agreed approach: harden the **existing** modules in place (no
new "OS" directories), keep stores in-memory but tenant-scoped (defer
Postgres), and deliver backend + proof system only (no new frontend).

## What was already strong

- Approval Center — in-memory `ApprovalStore` with submit / approve /
  reject / edit and an audit trail.
- Agent Governance — `evaluate_action` with forbidden tools,
  approval-required tools, and an autonomy ladder.
- Agent OS — governed `AgentCard` identity registry.
- Secure Agent Runtime OS — kill switch, risk memory, runtime states.
- Evidence Control Plane OS — `EvidenceObject` schema and types.
- Governance OS — deterministic `approval_matrix` + policy checks.
- Self-Improvement OS router — suggest-only, with hard gates.

## What was broken

- **API import was failing.** `from api.main import app` raised
  `ImportError` — a half-finished "Wave 14B/14F" migration left routers
  importing functions that were never implemented:
  - `value_os.value_ledger` was missing `ValueEvent`, `add_event`,
    `list_events`, `ValueDisciplineError` (the `/api/v1/value` router
    and the Monthly Value Report depend on them).
  - `data_os` was missing `compute_dq`, `import_preview.preview`,
    `source_passport.validate` (the `/api/v1/data-os` router depends on
    them).
  - `governance_os.runtime_decision` was missing `decide()`.
- No `tenant_id` on the operational control-plane objects.
- No stateful control plane — `institutional_control_os` had control
  *metrics* but no run *state*; `evidence_control_plane_os` had a schema
  but no store.
- No single end-to-end test proving the layers work together.
- No single verify gate / CI workflow for the control plane.

## What was fixed

### Stability
- Implemented `value_os.value_ledger` — `ValueEvent`, tiered ledger,
  `add_event` / `list_events`, `ValueDisciplineError`.
- Implemented the missing `data_os` API — `import_preview.preview`
  (typed `CSVPreview`), `data_quality_score.compute_dq` (typed
  `DQScore`), `source_passport.validate`.
- Added `governance_os.runtime_decision.decide()` + `RuntimeDecision`
  — the runtime governance entrypoint (composes the existing
  `approval_matrix` and Source Passport gating). Existing helpers kept.
- Result: `from api.main import app` imports clean (760 routes).

### Tenant isolation
- Added `tenant_id` to `ApprovalRequest`, `AgentCard`, `AgentSpec`,
  `EvidenceObject` (+ `run_id`), `ValueEvent`, `WorkflowRun`.
- Made the in-memory stores tenant-aware — `list_pending`,
  `list_agents`, `get_agent`, `get_run`, `list_runs`, `list_evidence`,
  `list_events` filter/scope by tenant.

### Control-plane state (new files inside existing modules)
- `institutional_control_os/run_registry.py` — tenant-scoped workflow
  run registry: register / pause / resume / `request_rollback` (files
  an approval ticket, parks the run) / `finalize_rollback` (succeeds
  only when the ticket is granted).
- `evidence_control_plane_os/evidence_store.py` — append-only,
  tenant-scoped evidence ledger; `run_trace` reads a run's events back.
- `secure_agent_runtime_os/agent_isolation.py` — `isolate_agent`
  isolates an agent and pauses its run; isolation is recorded as
  evidence.

### Proof system
- 10 proof test files, 47 assertions (see scorecard).
- `tests/test_enterprise_control_plane_e2e.py` — the full flow.
- `scripts/verify_enterprise_control_plane.sh` — single gate.
- `.github/workflows/enterprise-control-plane.yml` — CI gate.
- `readiness/` scorecard + readiness model + gates.

## What remains MVP / deferred

- **Persistence** — stores are in-memory and tenant-keyed; Postgres
  migrations + a repository layer are the next step (tracked in
  `readiness/enterprise_ready.md`).
- **Frontend** — `frontend/` already has `/agents` and `/approvals`;
  control-plane / safety / value pages are out of scope this round.
- **Per-tenant policy overrides** — governance policies stay
  system-wide.
- **Pre-existing test debt** — `tests/test_agent_os.py` and
  `tests/test_secure_agent_runtime.py` target an unfinished "Wave 14F"
  agent API and are a separate, pre-existing issue; they are not part
  of this hardening's verify gate.

## Definition of Done

`bash scripts/verify_enterprise_control_plane.sh` exits 0 and prints:

```
ENTERPRISE CONTROL PLANE: PASS
```
