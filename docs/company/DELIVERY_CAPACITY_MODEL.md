# Delivery Capacity Model — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DELIVERY_CAPACITY_MODEL_AR.md](./DELIVERY_CAPACITY_MODEL_AR.md)

## Context
Founder time is the binding constraint of the first phase. The
Delivery Capacity Model converts services into capacity units and
declares the founder's hard ceiling. It is the operational discipline
that supports the 90-day plan in
`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`, the daily ops loop in
`docs/V14_FOUNDER_DAILY_OPS.md`, and the hiring sequence in
`docs/HIRING_CSM_FIRST.md`.

## Capacity units per service

| Service | Units |
|---|---:|
| Lead Intelligence Sprint | 2 |
| AI Quick Win Sprint | 2 |
| Company Brain Sprint | 4 |
| Support Desk Sprint | 3 |
| Governance Program | 4 |

A unit is the amount of weekly founder attention required to keep one
parallel sprint on track at quality. The numbers are conservative
defaults; they are re-baselined after every fifth project of that
service.

## Founder solo capacity ceiling

> Max 4–5 units active at one time.

Above this ceiling, quality deteriorates, proof pack generation slows,
and the capital deposits expected for each project become unreliable.
The ceiling is intentionally below the absolute working ceiling so
that founder time also covers strategy, sales, and content.

## Permitted exceptions to the ceiling

Capacity may exceed the ceiling only when one of the following is in
place:

- **Delivery support exists** — a vetted contractor or analyst already
  onboarded for that service.
- **Scope is reduced** — explicit, written reduction agreed with the
  client.
- **Timeline is extended** — calendar window widened so per-week unit
  cost falls below the ceiling.

Any other reason is treated as overrun and routed to the Capacity
Ledger.

## Application

- At deal qualification, the founder checks the current units used in
  `docs/ledgers/CAPACITY_LEDGER.md`.
- A new deal is accepted only if projected units stay ≤ 5.
- If projected units > 5, one of the three exceptions must be in place
  before signature.
- Capacity is re-evaluated weekly during the daily-ops loop.

## Capacity vs. cash trade-off

Capacity discipline sometimes refuses revenue that the company could
technically book. This is intentional: revenue without proof-grade
delivery is a future trust-capital loss. The model values delivery
quality above near-term cash, in line with
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Pipeline forecast | Projected unit load | Founder | Weekly |
| Capacity Ledger | Current units used | Founder | Weekly |
| Hiring roster | Available contractor units | Founder | Monthly |
| Closure report | Re-baseline of unit costs | Founder | Per service, every 5th project |

## Metrics
- Units used vs. ceiling — weekly utilization; target ≤ 100% baseline, ≤ 120% with documented exception.
- Overrun rate — share of weeks above ceiling without documented exception; target 0%.
- Quality incidents on overrun weeks — count of proof-grade failures on weeks > 100%; target 0.
- Re-baseline cadence — services re-baselined on schedule; target 100%.

## Related
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — phase plan the capacity model sizes.
- `docs/HIRING_CSM_FIRST.md` — hiring sequence triggered when capacity tightens.
- `docs/V14_FOUNDER_DAILY_OPS.md` — daily loop where capacity is re-evaluated.
- `docs/ledgers/CAPACITY_LEDGER.md` — operational ledger.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
