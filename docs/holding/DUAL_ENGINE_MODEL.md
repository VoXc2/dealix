# Dual Engine Model — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DUAL_ENGINE_MODEL_AR.md](./DUAL_ENGINE_MODEL_AR.md)

## Context
Dealix runs on **two engines simultaneously**: a Cash Engine that pays the bills now, and a Compound Engine that builds a defensible asset base for the future. Most early-stage companies fail because they run only one — pure agencies run only the Cash Engine and never compound; pure product startups run only the Compound Engine and run out of money before traction. This file is the operating rule that forces every Dealix project to serve **both engines at once**. It is grounded in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and `docs/BUSINESS_MODEL.md`.

## Engine 1 — Cash Engine

The Cash Engine is the **services-and-retainers business** of Dealix. It funds payroll, hosting, and growth.

| Component | What it does |
|---|---|
| Diagnostic offer | Low-cost, fast (1–2 weeks). Surfaces opportunities. |
| Sprint | Focused 2–6 week paid engagement. Delivers a governed workflow. |
| Pilot | 1–3 month productized pilot. Proves ROI. |
| Retainer | Monthly recurring contract for an Ops capability. |

Cash Engine KPIs: bookings, cash collected, gross margin, retainer conversion, days-to-invoice. The Cash Engine is sized to be **break-even or contribution-positive on every project** — see `docs/UNIT_ECONOMICS_AND_MARGIN.md`.

## Engine 2 — Compound Engine

The Compound Engine is the **asset-and-IP business** of Dealix. Each project contributes to it, but it does not directly bill the client.

| Component | What it accumulates |
|---|---|
| Core OS | Reusable platform capabilities (LLM Gateway, Governance, Data OS) |
| Playbooks | Sector- and capability-specific delivery playbooks |
| Proof Ledger | Documented outcomes from every project |
| Capital Ledger | Reusable prompts, datasets, evals, agents |
| Academy | Training, certification, methodology IP |
| Partners | Distribution leverage via agencies/integrators |
| Platform | Productized workflows sold at SaaS-style economics |

Compound Engine KPIs: assets per project, asset reuse rate, # productized workflows, partner-sourced revenue, Academy graduates.

## The non-negotiable rule

> **Every Dealix project must serve both engines.**
>
> - A project that only serves the Cash Engine = **agency work** — banned at scale because it does not compound.
> - A project that only serves the Compound Engine = **product vacuum** — banned because it does not earn its keep.

The Dual Engine rule is enforced by the [`SUCCESS_ASSURANCE_SYSTEM`](./SUCCESS_ASSURANCE_SYSTEM.md) (Commercial + Capital dimensions both required green) and the [`VALUE_FLYWHEEL`](./VALUE_FLYWHEEL.md) (every project loops through both engines).

## Project intake checklist
Before a project is accepted into delivery, it must pass:

- [ ] Cash Engine: scoped, priced, gross margin ≥ 60%.
- [ ] Compound Engine: at least 1 reusable capital asset planned.
- [ ] Compound Engine: at least 1 proof event planned.
- [ ] Governance: in-scope policies confirmed.
- [ ] Productization candidacy: scored 1–5 against the productization rubric.

Projects failing either engine are rejected, rescoped, or moved to a Growth Engine experiment (Labs).

## Mapping to business units
Each BU runs both engines, with weights:

| BU | Cash Engine weight | Compound Engine weight | Primary compounding artifact |
|---|---|---|---|
| Revenue | High | High | Account-scoring agents, draft pack templates |
| Operations | High | Medium | Workflow library, SOP generator |
| Brain | Medium | High | Source registry, sector knowledge graphs |
| Support | High | Medium | Reply-suggestion models, escalation rules |
| Governance | Medium | Very High | Policy registry, risk register, audit log |
| Data | Medium | High | Data quality models, PII detectors |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| New project intake | Engine-pass / engine-fail decision | BU GM + Head of Core | Per project |
| Project closure | Cash collected + assets registered | BU GM | Per project |
| Capital Ledger | Reuse pull requests | Head of Core | Per project |
| Productization review | Cash-engine retainer / Compound-engine product candidates | Product Council | Bi-weekly |

## Metrics
- **Dual-engine pass rate** — % of accepted projects passing both engines at intake.
- **Cash-only project share** — % of projects with 0 capital assets (target → 0%).
- **Compound contribution per dollar** — capital assets created per $1k revenue.
- **Asset reuse rate** — % of new projects that reuse ≥ 1 existing capital asset.
- **Retainer pull-through** — % of pilots that convert to retainers within 60 days.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/BUSINESS_MODEL.md` — revenue model.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — Cash Engine economics.
- `docs/OFFER_LADDER_AND_PRICING.md` — Cash Engine product ladder.
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — Cash Engine playbook.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
