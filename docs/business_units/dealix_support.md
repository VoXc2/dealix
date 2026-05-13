# Dealix Support — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Support GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_support_AR.md](./dealix_support_AR.md)

## Context
Dealix Support is the Business Unit that raises the quality and speed of customer service in the client's existing channels (email, WhatsApp, web chat, ticketing). It does not replace the support team — it **gives the support team an AI-assisted desk** with classification, suggested replies, escalation rules, and SLA tracking. It sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), is paired with `docs/capabilities/customer_capability.md`, and inherits playbooks from `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`.

## Function
Support ingests historical and live tickets, builds a classifier for intent + sentiment, suggests replies grounded in the customer's knowledge base (via Dealix Brain), routes escalations via the Governance Runtime, and reports SLA performance back to operations.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| AI Support Desk | 2–4 weeks | Classifier + Suggested Replies live for top intents |
| Feedback Intelligence | 1–2 weeks | Themes + sentiment trends from last 6 months |
| Monthly Support AI (retainer) | Ongoing | Tuning, new intents, escalation refinement |

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Message Classifier | Intent + sentiment + urgency tagging |
| Suggested Replies | Drafts grounded in customer knowledge |
| Escalation Rules | Configurable routing with audit log |
| SLA Tracker | Per-channel SLAs and breach alerts |

## KPIs

- **First-response time** — median.
- **Reply consistency** — agreement rate between draft and final reply.
- **Ticket categories** — % tickets correctly categorized.
- **Escalation accuracy** — % escalations routed correctly on first hop.
- **Deflection rate** — % messages resolved without human intervention (where allowed).
- **CSAT lift** — customer satisfaction delta vs baseline.

## Core OS dependencies

| OS module | How Support consumes it |
|---|---|
| Data OS | Source registry for ticket history, PII tagging |
| LLM Gateway | Classifier + draft inference through gateway |
| Governance Runtime | Escalation routing + audit log per ticket |
| Proof Ledger | Support Proof Pack: response time delta, CSAT delta |
| Capital Ledger | Intent libraries, reply templates per sector |
| AI Control Tower | Cost per reply, eval scores, drift |
| Client Workspace | Agent UI overlay on top of existing helpdesk |

## Owner

| Role | Responsibility |
|---|---|
| Support BU GM | P&L, service ladder, retainer pull-through |
| Support Delivery Lead | Sprint execution + QA |
| Support CSM | Adoption + retainer health |
| Support Product Owner | Module backlog into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Helpdesk history + live tickets | Classifier + suggested replies | Support Delivery | Per sprint |
| Live messages | Tagged tickets + drafts | LLM Gateway | Realtime |
| SLA breaches | Alerts + escalation | Escalation Rules | Realtime |
| Monthly value report | Proof Pack | Support GM | Monthly |

## Metrics
- **MRR (Support BU).**
- **Gross margin.**
- **Median first-response time.**
- **Audit log completeness** — % AI-assisted replies logged.
- **Agent satisfaction with the AI** — internal survey.

## Related
- `docs/capabilities/customer_capability.md` — capability spec for this BU.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — playbook.
- `docs/CUSTOMER_SUCCESS_SOP.md` — SOPs.
- `docs/COMPANY_SERVICE_LADDER.md` — group service ladder.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
