# Enterprise Control Plane Hardening Report

## Scope
- Stabilization-only iteration (no new product features).
- Objective: reduce compatibility breaks, enforce tenant-aware operational contracts, and prove governed end-to-end flow.

## What was broken
- Runtime governance compatibility drift: mixed callers expected `decide(action_type=...)` while others used `decide(action=...)`, and metadata fields were inconsistent.
- Auditability runtime contracts were incomplete: `AuditEventKind`, `record_event`, `list_events`, `clear_for_test`, and `build_chain` were missing from active compatibility surface.
- Tenant scope was not explicit in key operational records used by execution and governance workflows.
- Hardening runbook test names existed in operational instructions but not in repository (`test_systems_26_35_routers_register.py`, `test_value_engine_os_tier_discipline.py`, `test_revenue_os_control_plane_e2e.py`).

## What was fixed
- Extended `auto_client_acquisition/governance_os/runtime_decision.py`:
  - Added dual-signature compatibility (`action` and `action_type`).
  - Added risk-aware metadata fields (`reason`, `risk_level`, `approval_required`, `evidence`).
  - Kept existing `GovernanceDecision` semantics for backward compatibility.
- Rebuilt `auto_client_acquisition/auditability_os/audit_event.py` compatibility facade:
  - Added `AuditEventKind`, append-only JSONL persistence, PII-redacted summaries, list/clear helpers.
- Extended `auto_client_acquisition/auditability_os/evidence_chain.py`:
  - Added `build_chain`, `EvidenceNode`, and `EvidenceChain` (`to_dict`, `to_markdown`) used by API endpoints/tests.
- Added tenant-aware defaults to operational objects:
  - `WorkflowRun.tenant_id`
  - `ValueEvent.tenant_id`
  - `agent_os.AgentCard.tenant_id`
  - `approval_center.schemas.ApprovalRequest.tenant_id`
  - `dealix.governance.approvals.ApprovalRequest.tenant_id`
- Added requested hardening test gates:
  - `tests/test_systems_26_35_routers_register.py`
  - `tests/test_value_engine_os_tier_discipline.py`
  - `tests/test_revenue_os_control_plane_e2e.py`
- Expanded `scripts/check_runtime_contracts.py` with auditability contract checks.

## What remains MVP / in-memory
- Approval store (`auto_client_acquisition/approval_center/approval_store.py`) remains in-memory singleton.
- Agent registry (`auto_client_acquisition/agent_os/agent_registry.py`) remains in-memory dictionary.
- Value and audit ledgers are file-backed JSONL (append-only) and not relationally indexed.
- End-to-end workflow proof currently orchestrates contracts inside tests; it is not yet backed by a unified runtime workflow engine + queue.

## What is production-ready now
- API import path is stable (`from api.main import app` succeeds).
- Core compatibility contracts for runtime decisioning, audit recording, and evidence chain export are deterministic and tested.
- Tenant-aware fields now exist on key operational records with safe defaults for dev/test.
- New E2E governance proof validates escalation, approval, value capture discipline, and audit trace generation in one flow.

## Production readiness status
| Area | Status | Evidence |
|---|---|---|
| API import | PASS | `python3 -c "from api.main import app; print('api import ok')"` |
| Control plane | PARTIAL | rollback/policy-edit approval tests |
| Tenant isolation | PARTIAL | tenant schema sweep tests |
| Approval gate | PASS | approval-gated finalize tests |
| Postgres persistence | TODO | migrations added, runtime wiring pending |
| Frontend | TODO/PARTIAL | control surface scaffolding pending full wiring/screenshots |

## What requires Postgres persistence
- Control/event ledger: move audit/control events from JSONL to Postgres JSONB tables with tenant/run indexes.
- Approval tickets and state transitions: durable storage with queryable status history and actor attribution.
- Agent registry: persistent agent descriptors with tenant partitioning and policy metadata.
- Workflow run state + transitions: durable run records with correlation IDs and replay-safe transitions.
- Value metrics ledger: tenant-scoped fact table for monthly proof and ROI rollups.

## Exact next milestones
1. Create migration set for tenant-scoped operational tables:
   - `control_events`, `approval_tickets`, `workflow_runs`, `agent_registry`, `assurance_contracts`, `value_metrics`.
2. Introduce storage interfaces (`*_store.py`) and swap in Postgres implementations behind existing APIs.
3. Wire approval + decision + value + trace pipeline through one runtime workflow entrypoint (service layer).
4. Add rollback/policy-edit approval transition tests in control-plane module when the control-plane core module is present on this branch.
5. Add minimal UI control surfaces for runs, approvals, agents, safety, and value once API contracts are finalized.
6. Promote release gate to require:
   - compile/import smoke,
   - router registration tests,
   - value discipline tests,
   - governed E2E workflow test,
   - runtime contract script.
