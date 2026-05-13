# AI Operating Model — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** Capability Owner — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_OPERATING_MODEL_AR.md](./AI_OPERATING_MODEL_AR.md)

## Context
Each Dealix client gets their own **AI Operating Model**: a one-page
declaration of what AI does (and does not do) for `<CLIENT_NAME>`,
under which governance, on which data, for which outcomes. This is
the client-side counterpart of
`docs/product/AI_WORKFORCE_OPERATING_MODEL.md` and the contract under
which `docs/governance/RUNTIME_GOVERNANCE.md` evaluates production
runs. Without it, scope creep is inevitable.

## Header
- **Client:** `<CLIENT_NAME>` · `<SECTOR>` · `<CITY>`
- **Capability Owner (Dealix):** `<OWNER_NAME>`
- **Client AI sponsor:** `<role>`
- **Dealix role:** `<Diagnostic / Sprint / Pilot / Retainer / Enterprise>`
- **Production status:** `<dev / pilot / prod>`

## 1. Business goals
List **at most 3** business outcomes AI is expected to move at
`<CLIENT_NAME>` this quarter. Each must be measurable in
`VALUE_DASHBOARD.md`.
1. `<goal 1>` — KPI: `<metric>` — owner: `<role>`
2. `<goal 2>` — KPI: `<metric>` — owner: `<role>`
3. `<goal 3>` — KPI: `<metric>` — owner: `<role>`

## 2. AI use cases
| # | Use case | Capability | Status | Workflow ID | Agent / model |
|---|---|---|---|---|---|
| 1 | `<lead triage / RFP draft / ticket reply>` | `<capability>` | `<dev / pilot / prod>` | `<workflow id>` | `<agent>` |
| 2 | `<>` | `<>` | `<>` | `<>` | `<>` |
| 3 | `<>` | `<>` | `<>` | `<>` | `<>` |

Out of scope (explicitly):
- `<use case explicitly NOT covered, with reason>`

## 3. Data sources
| Source | Type | Owner | Sensitivity | PDPL classification | Refresh |
|---|---|---|---|---|---|
| `<CRM>` | Structured | `<role>` | `<PII / commercial / public>` | `<class>` | `<live / daily / weekly>` |
| `<Helpdesk>` | Structured | `<role>` | `<>` | `<>` | `<>` |
| `<Docs / SOPs>` | Unstructured | `<role>` | `<>` | `<>` | `<>` |
| `<>` | `<>` | `<role>` | `<>` | `<>` | `<>` |

All sources are read via approved connectors per
`docs/LLM_PROVIDERS_SETUP.md` and routed under
`docs/AI_MODEL_ROUTING_STRATEGY.md`.

## 4. Human-in-the-loop (HITL) approval points
| Decision | Confidence threshold | Approver role | SLA |
|---|---|---|---|
| Send external email / message | < 0.85 confidence | `<role>` | 1 business hour |
| Update CRM record | < 0.90 | `<role>` | 4 business hours |
| Refund / commercial concession | always HITL | `<role>` | 24 hours |
| Publish public content | always HITL | `<role>` | 24 hours |
| Trigger payment / contract | always HITL + dual control | `<role>` + `<role>` | 24 hours |

## 5. Governance rules
- All workflows run under `docs/governance/RUNTIME_GOVERNANCE.md`.
- All prompts and outputs logged for 12 months
  (`docs/DATA_RETENTION_POLICY.md`).
- PDPL breach handling per `docs/ops/PDPL_BREACH_RUNBOOK.md`.
- Cross-border data transfer follows
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
- All commercial decisions logged for audit.

## 6. Reports
| Report | Audience | Frequency | Owner | Source |
|---|---|---|---|---|
| Operational metrics | Ops team | Weekly | Delivery Lead | Observability stack |
| Value dashboard | Client sponsor | Monthly | CSM Lead | `VALUE_DASHBOARD.md` |
| Risk / governance | Client GRC | Monthly | Governance Lead | Audit log |
| QBR pack | Exec sponsor | Quarterly | Account Director | Aggregated |

## 7. Metrics (production)
- AI eval pass rate
- HITL override rate
- Workflow success rate
- Mean cost per run (band)
- Mean latency per workflow

## 8. Operating cadence
Defined in `OPERATING_CADENCE.md`. AI-specific items:
- Daily: workflow queue + approvals review.
- Weekly: eval failures, drift, cost anomalies.
- Monthly: governance findings, retraining decisions.

## 9. Dealix role
Pick **one** primary mode:
- **Diagnostic** — observe and report only, no production agents.
- **Sprint** — first build, evidence-gathering, baseline.
- **Pilot** — controlled production with daily eyes-on.
- **Retainer** — operate and improve under SLA.
- **Enterprise** — multi-capability operator + governance owner.

Mode change is a written event; record date and reason here:
| Date | From → To | Reason | Approver |
|---|---|---|---|
| `<YYYY-MM-DD>` | `<X> → <Y>` | `<reason>` | `<role>` |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Goals, data sources, HITL rules | This operating model | Capability Owner | At kickoff, then quarterly |
| Eval data, incidents | Updates to use cases & HITL | Delivery Lead + Governance | Weekly |
| Mode changes | Recorded events | Account Director | As needed |
| Audit log | Governance findings | Governance Lead | Monthly |

## Metrics
- **Scope adherence** — % of production runs within declared use cases.
- **HITL fidelity** — % of HITL approvals captured in audit log
  (target 100%).
- **Mode-change discipline** — % of mode changes with written record.
- **Goal alignment** — % of value dashboard moves tied to declared goals.

## How to fill this
1. Fill jointly with the client AI sponsor at kickoff.
2. Use no more than 3 goals; trade off ruthlessly.
3. Restrict to current quarter; revise at QBR.
4. Treat "out of scope" as a feature, not a weakness — clarity prevents
   creep and protects margins.

## Related
- `docs/product/AI_WORKFORCE_OPERATING_MODEL.md` — global operating model
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
