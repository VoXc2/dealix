# Dealix Governance — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Governance GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_governance_AR.md](./dealix_governance_AR.md)

## Context
Dealix Governance is the Business Unit that enables enterprises to use AI **safely, accountably, and PDPL-aligned**. It is the BU that converts every enterprise's worry — privacy, audit, approvals, model risk — into a concrete control surface that lives inside Core OS. It sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), is paired with `docs/capabilities/governance_capability.md`, and integrates the legal stack in `docs/legal/COMPLIANCE_CERTIFICATIONS.md` and `docs/DPA_DEALIX_FULL.md`.

## Function
Governance assesses the client's AI readiness; designs and publishes an AI Usage Policy; runs a PDPL-aware data review; instruments a policy registry, approval matrix, AI risk register, and audit log inside Core OS; and runs a monthly AI Governance Program.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| AI Readiness Review | 1–2 weeks | Readiness scorecard + remediation plan |
| AI Usage Policy | 2–3 weeks | Published policy + employee comms |
| PDPL-Aware Data Review | 2–4 weeks | Data map, residency, retention, DSR readiness |
| AI Governance Program (retainer) | Ongoing | Policy updates, audits, incident response |

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Policy Registry | Versioned policies + bindings to workflows |
| Approval Matrix | Per-policy approval routing |
| AI Risk Register | Ranked risks with owners + mitigations |
| Audit Log | Immutable record of model calls, approvals, exports |

## KPIs

- **Policies created** — # active policies.
- **Risks detected** — # entries in AI Risk Register.
- **Approvals logged** — count over period.
- **Incidents prevented** — # near-misses caught by policy.
- **Critical incidents** — target 0.
- **DSR turnaround time** — median for Data Subject Requests.

## Core OS dependencies

| OS module | How Governance consumes it |
|---|---|
| Governance Runtime | Native consumer of policies, approvals, audit log |
| Data OS | PII tagging, residency, retention enforcement |
| LLM Gateway | Policy id attached to every inference |
| Proof Ledger | Governance Proof Pack: incidents avoided, audit coverage |
| Capital Ledger | Policy templates, risk taxonomies |
| AI Control Tower | Drift, anomaly, and policy-violation telemetry |

## Owner

| Role | Responsibility |
|---|---|
| Governance BU GM | P&L, service ladder, retainer pull-through |
| DPO (Group) | PDPL alignment, breach response |
| Governance Delivery Lead | Sprint execution + QA |
| Governance Product Owner | Module backlog into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Customer policy + data inventory | Readiness scorecard | Governance Delivery | Per sprint |
| New workflows | Policy bindings | Approval Matrix | Per workflow |
| Audit events | Audit log entries | Audit Log | Realtime |
| Incident | Response + remediation | DPO | Per incident |

## Metrics
- **MRR (Governance BU).**
- **Gross margin.**
- **Audit log completeness** — % model calls audited.
- **Policy coverage** — % workflows bound to at least 1 policy.
- **PDPL conformance** — checklist score from `docs/PRIVACY_PDPL_READINESS.md`.

## Related
- `docs/capabilities/governance_capability.md` — capability spec for this BU.
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance stack.
- `docs/DPA_DEALIX_FULL.md` — DPA.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — breach runbook.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
