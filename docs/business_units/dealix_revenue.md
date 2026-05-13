# Dealix Revenue — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Revenue GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_revenue_AR.md](./dealix_revenue_AR.md)

## Context
Dealix Revenue is the Business Unit that turns customer data and opportunities into qualified pipeline and closed revenue. It is the **wedge BU** of the holding — the one that opens conversations with new accounts, then hands off broader work to other BUs. It implements the strategy in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), and is paired with the capability spec in `docs/capabilities/revenue_capability.md`.

## Function
Dealix Revenue takes a target list and a CRM, scores accounts, drafts the right next touch with full source citations, manages governed approval, and ships a pipeline-ready set of accounts and drafts to the customer's revenue team — all auditable, all PDPL-aligned.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| Revenue Diagnostic | 1–2 weeks | Scored account list, top 25 opportunities, pipeline gap analysis |
| Lead Intelligence Sprint | 2–4 weeks | Account-scoring model in production, draft pack live, training |
| Pilot Conversion | 1–3 months | First closed deals from drafts, ROI proof pack |
| Monthly RevOps OS (retainer) | Ongoing | Continuous account scoring, draft refresh, pipeline reporting |

Aligned with `docs/OFFER_LADDER_AND_PRICING.md` and `docs/COMPANY_SERVICE_LADDER.md`.

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Revenue Workspace | Tenant UX for the revenue team |
| Account Scoring | Configurable scoring model with governance approval |
| Draft Pack | LLM-generated outreach drafts with source citations |
| Pipeline Board | Stage funnel, owner, next action |
| Revenue Proof Pack | ROI evidence per cohort |

## KPIs

- **Accounts scored** — # accounts processed per period.
- **Qualified accounts** — # accounts above threshold score with valid data.
- **Pipeline value created** — SAR/USD pipeline added in window.
- **Follow-up actions completed** — # outreach drafts approved + sent.
- **Sprint-to-Pilot conversion** — % of sprints converting to pilots within 60 days.
- **Pilot-to-Retainer conversion** — % of pilots converting to monthly retainer.

## Core OS dependencies

| OS module | How Revenue consumes it |
|---|---|
| Data OS | Source registry (CRM + enrichment), PII tagging, quality score |
| LLM Gateway | All draft generation routed through gateway, prompt registry, eval scoring |
| Governance Runtime | Approval flow on outreach drafts; audit log of every send |
| Proof Ledger | Revenue Proof Pack per project |
| Capital Ledger | Reusable scoring features, prompts, sector templates |
| AI Control Tower | Cost per draft, eval pass rate, drift alerts |
| Client Workspace | Revenue tenant UI, RBAC for sales managers |

## Owner

| Role | Responsibility |
|---|---|
| Revenue BU GM | P&L, service ladder, retainer pull-through |
| Revenue Delivery Lead | Sprint execution and QA |
| Revenue CSM | Pilot → retainer conversion |
| Revenue Product Owner | Module backlog & roadmap into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client CRM + targets | Scored accounts | Revenue Delivery | Per sprint |
| Sprint output | Drafts + governance approvals | Revenue Delivery | Per sprint |
| Proof Pack | Capital assets + case study | Revenue GM | Per project |
| Retainer renewal | Monthly OS retainer | Revenue CSM | Monthly |

## Metrics
- **MRR (Revenue BU)** — retainer monthly recurring revenue.
- **Gross margin (Revenue BU)** — service margin after delivery cost.
- **Win rate** — pipeline → closed-won.
- **Approved-draft ratio** — % drafts approved at first review.
- **Audit completeness** — % outreach actions with audit log entry.

## Related
- `docs/capabilities/revenue_capability.md` — capability spec for this BU.
- `docs/COMPANY_SERVICE_LADDER.md` — group service ladder.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing of Revenue services.
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — sell + convert playbook.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
