# Cross-Layer Validation Model

## Objective

Validate that Dealix layers operate together safely under realistic business flow, without:
- permission leakage,
- governance bypass,
- missing citations,
- missing observability,
- un-audited execution.

## Cross-Layer Critical Gates

| Gate ID | Gate | Pass Condition |
|---|---|---|
| G-CLV-001 | Identity continuity | same tenant/user context survives full workflow |
| G-CLV-002 | Permission safety | unauthorized role cannot trigger restricted action |
| G-CLV-003 | Knowledge safety | retrieval returns citation-backed, permission-scoped data |
| G-CLV-004 | Governance enforcement | high-risk actions always paused for approval |
| G-CLV-005 | Execution integrity | approved action executes once, idempotently |
| G-CLV-006 | Observability continuity | end-to-end trace graph exists for all steps |
| G-CLV-007 | Eval gating | quality/policy scores written and threshold-checked |
| G-CLV-008 | Rollback readiness | rollback drill succeeds and is auditable |

## End-to-End Test Matrix

| Test ID | Scenario | Expected Result |
|---|---|---|
| T-CLV-001 | Inbound lead with normal risk | executes with full trace + audit |
| T-CLV-002 | Inbound lead with high-risk action | workflow pauses pending approval |
| T-CLV-003 | Unauthorized role attempts restricted tool | request denied and audited |
| T-CLV-004 | Cross-tenant retrieval attempt | blocked with policy reason |
| T-CLV-005 | Approval granted path | external action runs once and logs evidence |
| T-CLV-006 | Approval denied path | no external action, closure recorded |
| T-CLV-007 | Observability failure simulation | alert fired + incident record created |
| T-CLV-008 | Release rollback drill | prior version restored with validation pass |

## Evidence Contract

Every cross-layer test must attach:
1. Trace link or trace export (`trace_id`, `span_id` chain).
2. Governance decision record (`risk_score`, `policy_result`, `approval_state`).
3. Execution artifact (CRM/task/message result or explicit block reason).
4. Eval report (quality + compliance).
5. Audit log record.

## Readiness Decision for Cross-Layer

Cross-layer score is:

`Score = 100 x (Passed Critical Tests / Total Critical Tests)`

Rules:
- Any failed critical test -> score capped at 59 (`Prototype`).
- To claim enterprise posture -> score >= 90 and no critical gate failed in last release cycle.

## Final Acceptance Protocol

Protocol ID: `CLV-PROTOCOL-001`

- Run all `T-CLV-*` tests in staging.
- Repeat `T-CLV-001` and `T-CLV-002` in production-safe sandbox.
- Verify evidence completeness.
- Sign-off requires engineering lead + governance owner.
