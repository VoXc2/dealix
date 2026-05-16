# Cross-Layer Validation (Release 0 Baseline)

## Goal

Validate one complete workflow across layers instead of validating layers in isolation.

## Canonical proof workflow

`Inbound Lead -> Sales Agent -> Knowledge Retrieval -> Governance Check -> Human Approval -> CRM/Sheet Update -> Observability Trace -> Eval Report -> Executive ROI Report`

## Validation matrix

| Layer | Validation question | Required evidence |
|---|---|---|
| Readiness | Are gates, owners, and score rules defined? | Readiness docs + scoring records |
| Platform | Is tenant/RBAC/security/rollback enforced? | Tenant + RBAC tests, audit logs, rollback drill |
| Agents | Is the sales agent permissioned and risk-scoped? | Agent manifest + permission/risk docs |
| Workflows | Does the workflow execute with retries/fallback? | Workflow run logs + completion metrics |
| Evals | Is quality measured before release? | Eval cases + gate outcome |
| Governance | Are high-risk actions blocked pending approval? | Approval decision logs + policy outcomes |
| Observability | Does every run have trace/log/metric linkage? | Trace IDs, step logs, alert behavior |
| Playbooks | Can operators execute and hand over reliably? | Delivery/onboarding/QA checklists |
| Continuous Improvement | Is release + rollback process followed? | Release checklist + rollback report |
| Executive | Is business impact visible to leadership? | Weekly brief + ROI report |

## Release 0 validation steps

1. Confirm all layer directories exist and are documented.
2. Confirm owner role is assigned for each layer.
3. Confirm checklist entry point exists for each layer.
4. Run focused regression tests to verify API stack remains healthy.
5. Capture current-state gap analysis by layer.
6. Publish 30-day plan for one end-to-end proof workflow.

## Release 1 validation steps

1. Confirm one tenant pilot model is documented.
2. Confirm 3-user / 2-role minimum RBAC operating pattern is documented.
3. Confirm audit requirements include actor, action, tenant, time, trace_id, result.
4. Confirm rollback runbook includes rehearsal and acceptance criteria.
5. Confirm every API operation requires tenant context in the design standard.

## Exit criteria for this phase

Release 0 and Release 1 are accepted only when:

- structure + docs are complete,
- focused regression tests pass,
- gap analysis is published,
- single-workflow 30-day implementation plan is published.
