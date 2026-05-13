# Margin Control — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [MARGIN_CONTROL_AR.md](./MARGIN_CONTROL_AR.md)

## Context
Margin discipline is the difference between a consultancy that
compounds capital and one that consumes it. This file declares the
target margins for the canonical Dealix services, the minimum
acceptable prices, and the only conditions under which the floor can
be breached. It is the operational expression of
`docs/UNIT_ECONOMICS_AND_MARGIN.md` and the cost stance in
`docs/COST_OPTIMIZATION.md`, and it directly feeds the metrics surfaced
on `docs/FINANCE_DASHBOARD.md`.

## Margin table (SAR)

| Service | Price | Estimated Hours | Delivery Cost | Gross Margin | Minimum Acceptable Price |
|---|---:|---:|---:|---:|---:|
| Lead Intelligence | 9,500 | 20 | 2,000 | 79% | 7,500 |
| AI Quick Win | 12,000 | 25 | 3,000 | 75% | 9,500 |
| Company Brain | 25,000 | 50 | 6,000 | 76% | 20,000 |

Numbers are starting baselines. They are revised at most once per
quarter following a margin review, with the change recorded in this
file's Change log and reflected in
`docs/revenue/PRICING_AND_PACKAGING.md`.

## The floor rule

> Do not sell below the minimum acceptable price.

The floor exists because below it the engagement does not produce
enough margin to fund the capital deposits Dealix needs (proof packs,
templates, scripts, knowledge graph entries). Selling below the floor
turns the project into pure labor.

## Permitted exceptions

The floor may be breached only when **all** of the following hold:

- There is a strong case-study justification (e.g., flagship logo in
  a new sector).
- The client is strategic (large-scale follow-on potential).
- A meaningful partnership is on the table.
- An important proof asset (Stage-5 candidate) is the byproduct.

Even then the engagement must be **labeled as a pilot**, scoped down
to fit the reduced price, and logged as an exception in the Capital
Ledger. Repeated exceptions for the same justification are not
allowed.

## Estimation discipline

- **Estimated Hours** is the planning number; actual hours are
  measured and compared at closure.
- A delivery that exceeds estimated hours by more than 25% triggers a
  scoping retro and an update to the estimate for future sales.
- Hours are tracked at the service level — not at the line-item level
  — to keep operational overhead low.

## Cost composition

Delivery Cost includes only direct, attributable costs: tooling on the
project, contractor time, sector data licensing, and external review
where applicable. Indirect overhead is handled separately at the
company level in `docs/FINANCE_DASHBOARD.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proposal | Margin check | Founder | Per deal |
| Closure report | Actual margin per project | Delivery lead | Per project |
| Quarterly review | Margin table update | Founder | Quarterly |
| Cost reports | Delivery cost trendline | Founder | Monthly |

## Metrics
- Gross margin (average) — across all services; target ≥ 70%.
- Floor breaches — projects sold below minimum acceptable price; target ≤ 1 per quarter.
- Estimation accuracy — share of projects within ±20% of estimated hours; target ≥ 75%.
- Margin drift — quarter-over-quarter change in average margin; flag if more than ±5 points.

## Related
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — economics that define target margins.
- `docs/FINANCE_DASHBOARD.md` — dashboard surface for margin metrics.
- `docs/COST_OPTIMIZATION.md` — cost levers that protect the floor.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model the margins fund.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
