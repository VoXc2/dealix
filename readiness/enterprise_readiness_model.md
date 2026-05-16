# Dealix Enterprise Readiness Model (v1)

## Purpose

This model defines objective maturity evidence for Dealix as an **Agentic Enterprise Operating Infrastructure**, not an AI wrapper.  
Readiness is accepted only when the cross-layer operating test passes with auditable evidence.

## Maturity Bands

| Score | Band |
|---|---|
| 0–59 | Prototype |
| 60–74 | Internal Beta |
| 75–84 | Client Pilot |
| 85–94 | Enterprise Ready |
| 95–100 | Mission Critical |

## Layer Score Thresholds (Required to claim readiness)

| Layer | Minimum Score |
|---|---:|
| Foundation | 90 |
| Agent Runtime | 85 |
| Workflow Engine | 85 |
| Knowledge / Memory | 85 |
| Governance | 90 |
| Execution / Integrations | 85 |
| Observability | 90 |
| Evals | 85 |
| Delivery Playbooks | 85 |
| Executive Intelligence | 80 |
| Continuous Evolution | 85 |
| Cross-Layer Validation | 90 |

## Readiness Gate Logic

A layer score is valid only if:
1. All mandatory gates for that layer are `PASS`.
2. Each gate has at least one evidence item.
3. Each evidence item has at least one executable test with a stable Test ID.
4. Test output is timestamped and linked to release version.

Global readiness states:
- `NOT_READY`: any required layer below threshold.
- `CLIENT_PILOT_READY`: all layers at threshold and cross-layer test scenario passes once.
- `ENTERPRISE_READY`: `CLIENT_PILOT_READY` + scenario repeated across 3 tenants with no governance bypass.
- `MISSION_CRITICAL_TRAJECTORY`: `ENTERPRISE_READY` + rollback drill + incident drill + SLO adherence verified.

## Canonical End-to-End Validation Scenario

Scenario ID: `CLV-E2E-001`

1. New lead enters WhatsApp or website.
2. System resolves tenant and user permissions.
3. Sales agent qualifies lead.
4. Knowledge retrieval returns company data with citations.
5. Workflow engine scores lead and drafts action.
6. Governance checks risk and policy.
7. High-risk action is paused for human approval.
8. Approved action updates CRM / sends message / creates task.
9. Observability records traces, logs, metrics, cost, and latency.
10. Evaluation layer scores quality and policy compliance.
11. Executive dashboard displays business impact.
12. Release/change rollback is executed and audited safely.

Readiness is rejected if any step is missing traceability, approval, or audit records.

## Standards Mapping (Operational, not document-only)

- **NIST AI RMF**:
  - Govern -> policy ownership, control accountability, audit ownership.
  - Map -> use-case inventory, data lineage, risk context.
  - Measure -> evaluation metrics, drift/error rates, policy violations.
  - Manage -> approval gates, mitigations, rollback and incident response.
- **OpenTelemetry**:
  - Distributed trace propagation (`trace_id`, `span_id`) across intake -> agent -> governance -> execution.
  - Metrics for reliability, latency, and business outcomes.
  - Structured logs correlated with traces for investigations.

## Minimum Pilot Configuration (Must pass before external pilot)

Configuration ID: `MPC-001`

- 1 tenant
- 3 users
- 2 roles
- 1 sales agent
- 1 governed sales workflow
- 1 knowledge base
- 1 approval rule
- 1 CRM or sheet integration
- 1 observability trace
- 1 evaluation report
- 1 executive ROI report
- 1 rollback drill

If `MPC-001` fails, Dealix is not `CLIENT_PILOT_READY`.
