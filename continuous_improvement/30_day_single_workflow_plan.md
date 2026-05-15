# 30-Day Implementation Plan — Single Proof Workflow

## Workflow target

`Inbound Lead -> Sales Agent -> Knowledge Retrieval -> Governance Check -> Human Approval -> CRM/Sheet Update -> Observability Trace -> Eval Report -> Executive ROI Report`

## Rule of execution

- Build only what is required to make this one workflow complete and governed.
- Do not expand horizontally into multiple unfinished workflows.

## Day 1-5: Baseline and contracts

1. Freeze baseline architecture and acceptance gates for the workflow.
2. Define workflow input/output contract and step schema.
3. Map each step to required tenant/RBAC/policy checks.
4. Define trace/event naming and correlation standard.
5. Define eval case format and pass threshold.

Exit gate:

- Workflow contract approved.
- Layer owners confirmed.
- Gate checklist approved.

## Day 6-10: Platform controls in path

1. Enforce tenant context requirement on all workflow-relevant APIs.
2. Enforce RBAC checks for each workflow action.
3. Ensure audit event coverage for each step outcome.
4. Prepare rollback runbook for workflow-related deployments/config.

Exit gate:

- Tenant/RBAC/audit checks pass for workflow API surface.
- Rollback drill scenario defined.

## Day 11-15: Agent + workflow runtime completion

1. Register Sales Agent with explicit permission and risk profile.
2. Implement workflow execution sequence with retry/fallback policy.
3. Add high-risk stop-points before external actions.
4. Add human approval integration for high-risk offer send.

Exit gate:

- Workflow completion rate reaches target in test scenarios.
- High-risk steps are blocked without approval.

## Day 16-20: Knowledge and governance hardening

1. Bind knowledge retrieval to tenant and user permissions.
2. Require citations for customer-facing knowledge answers.
3. Wire governance runtime sequence:
   - risk score
   - policy check
   - approval requirement
   - execution
   - audit

Exit gate:

- No cross-tenant retrieval in test set.
- No uncited critical response in test set.

## Day 21-25: Observability + eval gates

1. Ensure each workflow run emits end-to-end `trace_id`.
2. Ensure each step emits structured logs and metrics.
3. Implement workflow eval suite and quality thresholds.
4. Block release on eval gate failure.

Exit gate:

- Eval report generated and passing.
- Observability dashboard shows workflow health and policy violations.

## Day 26-30: Executive outputs + release rehearsal

1. Generate executive ROI report from workflow outcomes.
2. Generate weekly executive brief template with pilot KPIs.
3. Execute rollback drill and record recovery metrics.
4. Run full acceptance scenario end-to-end and produce evidence pack.

Exit gate:

- Complete workflow run passes all gates.
- ROI report generated.
- Rollback drill executed successfully.

## Success criteria for this 30-day plan

1. One fully governed and observable workflow in production-ready pilot form.
2. Release gating active (tests + evals + governance + rollback).
3. Executive-facing business impact artifacts available.
4. No expansion to additional workflows before this path is complete.
