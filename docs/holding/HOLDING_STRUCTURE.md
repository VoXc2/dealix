# Holding Structure — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO / Group COO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [HOLDING_STRUCTURE_AR.md](./HOLDING_STRUCTURE_AR.md)

## Context
This file specifies the formal org structure of the Dealix Group: who reports to whom, where the P&Ls sit, and how Shared Services are billed back to Business Units. It is the operational expansion of [`DEALIX_HOLDING_OS.md`](./DEALIX_HOLDING_OS.md) and must be read alongside the financial model in `docs/UNIT_ECONOMICS_AND_MARGIN.md` and the revenue ladder in `docs/BUSINESS_MODEL.md`. Reporting lines defined here are the only valid ones — any escalation or accountability outside this chart is, by construction, a process failure.

## Top-level org chart

```
                       CEO / Group Strategy
                                │
        ┌───────────────────────┼─────────────────────────────┐
        │                       │                             │
    Dealix Core            Dealix Services            Group Finance / Ops
    (Platform P&L)         (Delivery P&L)             (Cost center)
        │                       │                             │
   ┌────┼────┬────┬────┐    ┌───┼───┐                  ┌──────┼──────┐
 Product Platform Gov Data  CSM  QA  Delivery        Fin   Legal   People
  AI Infra                                          /Acct  /Comp   /Talent
                                │
                                │
                       Business Units (BU P&Ls)
                                │
   ┌────────┬────────┬────────┬─────────┬───────────┬─────────┐
 Revenue  Operations  Brain   Support  Governance   Data
                                │
                       Growth Engines (Compounding)
                                │
        ┌──────────┬──────────┬──────────┬──────────┐
       Academy   Partners    Labs       Ventures
```

## Reporting lines

| Role | Reports to | Owns |
|---|---|---|
| CEO / Group Strategy | Board | Group P&L, strategy, holding shape |
| Group COO | CEO | Shared Services SLAs, internal billing |
| Head of Dealix Core | CEO | Core OS platform P&L and roadmap |
| Head of Dealix Services | CEO | Delivery P&L, QA, CSM |
| BU GM (×6) | Head of Dealix Services + CEO (dotted) | BU P&L, service ladder, retainers |
| Head of Growth Engines | CEO | Academy, Partners, Labs, Ventures |
| Group CFO | CEO | Finance, billing, treasury |
| Group GC / DPO | CEO | Legal, PDPL compliance |

## P&L map

| Entity | P&L type | Revenue source | Cost source |
|---|---|---|---|
| Dealix Core (Platform) | Platform P&L | Internal Core OS billing + external API revenue (future) | R&D, infra, governance staff |
| Dealix Services (Delivery) | Service P&L | Project fees, retainers (collected via BUs) | Delivery staff, CSM, QA |
| BU Revenue, Operations, Brain, Support, Governance, Data | BU sub-P&L | Service ladder + retainers + productized fees | Allocated delivery, allocated Core OS, BU GM |
| Academy | Compounding P&L | Course fees, certification | Curriculum, instructor cost |
| Partners | Compounding P&L | Revenue share, partner program fees | Partner ops staff |
| Labs | R&D cost center first, then P&L | Vertical pilots | Research staff |
| Ventures | Equity / co-build P&L | Equity proceeds, co-build fees | Diligence, legal |
| Group Finance / Ops | Cost center | n/a | Shared overhead |

## Shared Services billing model

Shared Services are funded from BU revenue via a transparent internal billing scheme. The rules:

1. **Sales** — billed as a % of net new ARR closed for a BU (default 8%).
2. **Delivery / CSM** — billed at fully-loaded internal day rate per delivered day.
3. **Product / QA** — billed as a fixed monthly platform fee per BU (covers Core OS usage and quality gates).
4. **Finance / Legal / Compliance** — billed as a % of BU revenue (default 4% combined).
5. **Brand / Content** — billed as a fixed monthly fee per BU; outsized campaigns billed separately.

The BU GM is responsible for staying within the implied margin envelope. See `docs/FINANCE_DASHBOARD.md` for the live unit economics view.

## Decision rights

| Decision | Owner | Consulted | Informed |
|---|---|---|---|
| New BU spin-up | CEO | Group COO, BU GMs | Board |
| Core OS feature commit | Head of Dealix Core | BU GMs, Head of Services | All BUs |
| Service ladder change in a BU | BU GM | Head of Services, Brand | CEO |
| Hiring above L5 | CEO | Group COO, hiring manager | Board |
| Pricing change > 15% | CEO | BU GM, CFO | Board |
| New partner tier | Head of Growth | CFO, Legal | CEO |
| Capital ledger reuse policy | Head of Dealix Core | Legal, BU GMs | CEO |

## Hiring sequence
The CSM-first hiring posture in `docs/HIRING_CSM_FIRST.md` is the group default: first hires into a new BU are CSMs, then Delivery, then Sales, then GM, then specialists. This keeps proof and retention high before scaling pipeline.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| BU monthly P&L | Group consolidated P&L | Group CFO | Monthly |
| Shared Services usage logs | Internal billing line items | Group COO | Monthly |
| Hiring requisitions | Approved org changes | CEO | Weekly |
| New BU proposals | Spin-up / reject decisions | CEO + Board | Quarterly |
| BU GM 1:1 | Coaching, escalations | Head of Services | Weekly |

## Metrics
- **BU contribution margin** — BU revenue minus direct + allocated cost.
- **Shared Services cost ratio** — Shared Services cost ÷ group revenue.
- **Span of control** — direct reports per manager (target 5–8).
- **Time-to-fill** — days from requisition to signed offer.
- **GM bench depth** — number of named successors per BU GM seat.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan driving the org shape.
- `docs/BUSINESS_MODEL.md` — revenue model the BUs implement.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — margin envelope per service.
- `docs/FINANCE_DASHBOARD.md` — live unit economics view.
- `docs/HIRING_CSM_FIRST.md` — hiring sequence policy.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
