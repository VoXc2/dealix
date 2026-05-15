# Dealix Enterprise Readiness Model (Release 0 Baseline)

## Purpose

This model converts Dealix from feature growth into release-driven enterprise execution.
It aligns three references into one operating model:

- McKinsey agentic organization pillars: business model, operating model, governance, workforce/culture, technology/data.
- NIST AI RMF functions: Govern, Map, Measure, Manage.
- OpenTelemetry-first observability for traces, metrics, and logs.

## Release policy

- Current scope in this cycle: **Release 0 + Release 1 only**.
- No speculative platform build-out in this release.
- Preserve all existing API behavior while adding structure and controls.

## Layer registry (location + owner + readiness checklist)

| Layer | Path | Primary owner | McKinsey pillar | NIST AI RMF focus | Release 0 readiness checklist |
|---|---|---|---|---|---|
| Readiness | `/readiness` | PMO / Product Strategy Lead | Operating model | Govern | Model defined, scoring defined, cross-layer validation documented |
| Platform | `/platform` | Platform Engineering Lead | Technology & data | Govern + Manage | Tenant isolation spec, RBAC spec, audit spec, rollback spec |
| Agents | `/agents` | Agent Engineering Lead | Operating model | Map + Manage | Agent registry convention, permissions contract, risk profile template |
| Workflows | `/workflows` | Workflow Engineering Lead | Business model | Map + Manage | Workflow schema conventions, state/step ownership, failure-handling pattern |
| Evals | `/evals` | AI Quality Lead | Governance | Measure | Test cases by workflow, thresholds, pass/fail gate ownership |
| Governance | `/governance` | Trust & Compliance Lead | Governance | Govern + Manage | Policy matrix, approval rules, audit traceability requirements |
| Observability | `/observability` | SRE / Reliability Lead | Technology & data | Measure + Manage | Trace/log/metric minimums, dashboards, alert ownership |
| Playbooks | `/playbooks` | Delivery Operations Lead | Workforce & culture | Govern + Manage | Onboarding, QA, delivery, monthly review playbooks |
| Continuous Improvement | `/continuous_improvement` | Release Manager | Operating model | Measure + Manage | Release gates, rollback policy, post-release review loop |
| Executive | `/executive` | Revenue Operations Lead | Business model | Map + Measure | ROI report template, weekly executive brief, decision cadence |

## Definition of “layer is real”

A layer is accepted only when it includes all of the following:

1. Code/runtime behavior
2. Tests
3. Evals
4. Observability
5. Governance controls
6. Rollback path
7. Metrics
8. Business impact evidence

If any one element is missing, the layer is not release-ready.

## Acceptance criteria for Release 0

1. Each layer has a clear path in the repository.
2. Each layer has a named owner role.
3. Each layer has a readiness checklist entry point.
4. Existing endpoints remain intact (verified by focused regression tests).
