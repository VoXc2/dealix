# Service-to-KPI Map — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SERVICE_KPI_MAP_AR.md](./SERVICE_KPI_MAP_AR.md)

## Context
Every Dealix service must be tied to a measurable KPI before it is
sold. This file is the canonical mapping from service to primary KPI,
secondary KPI, and proof type. It enforces the rule, set out in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, that we never sell work
whose impact cannot be proven. It is the upstream constraint for
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md` and the
`docs/COMPANY_SERVICE_LADDER.md`.

## The map

| Service | Primary KPI | Secondary KPI | Proof Type |
|---|---|---|---|
| Lead Intelligence Sprint | Qualified accounts ranked | Data quality improvement | Revenue / Quality |
| AI Quick Win Sprint | Hours saved | Error reduction | Time / Quality |
| Company Brain Sprint | Answers with sources | Search time reduction | Knowledge / Quality |
| AI Support Desk | Response time reduction | Reply consistency | Time / Quality |
| Governance Program | Risk controls implemented | Approvals logged | Risk |

## The rule

> Any service without a clear KPI is not sold.

If a prospect's situation cannot be expressed in one of the proof
types above (Revenue / Time / Knowledge / Quality / Risk), the
engagement is reframed, scoped down to a diagnostic, or declined. This
preserves trust capital and protects the proof-pack pipeline.

## Proof types and what they look like

- **Revenue** — Closed pipeline value, qualified accounts, win-rate
  delta, new revenue per channel.
- **Time** — Hours saved per week, response-time reduction, cycle-time
  reduction.
- **Knowledge** — Answers with sources, search-time reduction,
  retrieval accuracy.
- **Quality** — Error rate, consistency rate, Arabic QA score.
- **Risk** — Controls implemented, audit-log coverage, incidents
  prevented or contained.

## KPI definition discipline

For every service the team writes the KPI in the form:

> *Metric, baseline, target, measurement method, owner.*

Without all five fields the KPI is treated as undefined and the
service is not eligible for sale until the gap is closed.

## Adding a new service to the map

1. Define the primary KPI in the five-field form above.
2. Define a secondary KPI in the same form.
3. Map both to one of the five proof types.
4. Confirm a Proof Pack template exists or can be produced.
5. Add a row to this table.
6. Cross-reference in
   `docs/COMPANY_SERVICE_LADDER.md` and
   `docs/OFFER_LADDER_AND_PRICING.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| New service proposal | KPI definition record | Founder | Per service |
| Closure report | KPI actuals | Delivery lead | Per project |
| Quarterly review | KPI revision proposals | Founder | Quarterly |
| Sales pipeline | Discarded undefined-KPI deals | Founder | Weekly |

## Metrics
- KPI-defined service share — share of saleable services with full 5-field KPI; target 100%.
- Proof-pack production rate — share of closed projects that produce a proof pack tied to the mapped KPI; target ≥ 95%.
- KPI achievement rate — share of projects that meet or exceed primary KPI target; target ≥ 75%.
- Discarded deals — count of deals rejected for missing-KPI fit; tracked, not capped.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard surface for these KPIs.
- `docs/COMPANY_SERVICE_LADDER.md` — service catalog this map governs.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing layer that depends on the KPI map.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model the KPI map feeds.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
