# Capacity Ledger — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPACITY_LEDGER_AR.md](./CAPACITY_LEDGER_AR.md)

## Context
The Capacity Ledger is the weekly running record of how much delivery
capacity Dealix is actually consuming. It is the operational
counterpart to `docs/company/DELIVERY_CAPACITY_MODEL.md` and the
ground truth that the daily founder loop in
`docs/V14_FOUNDER_DAILY_OPS.md` and the operating loop in
`docs/ops/DAILY_OPERATING_LOOP.md` are run against. It exists to
prevent silent overrun, the single most common failure mode of a
founder-led services company.

## Schema

| Column | Description |
|---|---|
| Week | ISO week or Sunday-anchored week start (KSA convention) |
| Active Projects | Project names or codes |
| Units Used | Sum of capacity units across active projects |
| Max Units | Current ceiling (default 5) |
| Risk | Low / Medium / High |

## Example snapshot

| Week | Active Projects | Units Used | Max Units | Risk |
|---|---|---:|---:|---|
| W18 | Lead Sprint A, Quick Win B | 4 | 5 | Low |
| W19 | Brain C, Lead D | 6 | 5 | High |

W19 in the example triggers the overrun rule: the team either declines
new work, raises price, extends schedule, or brings in a contractor.

## Risk levels

- **Low** Units ≤ 80% of ceiling.
- **Medium** Units 81–100% of ceiling.
- **High** Units > 100% of ceiling.

## Overrun playbook

If the ledger shows units > max:

1. **Do not accept** any new project until capacity normalizes.
2. **Raise price** on the next deal in pipeline; if the deal is
   already signed, escalate the timeline conversation.
3. **Extend schedule** on the current overrunning sprint, with written
   client agreement.
4. **Bring in a contractor** drawn from the pre-vetted roster.

Doing nothing is not an option. Each overrun week without an action is
recorded as a governance breach in
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Operational cadence

- The founder updates the ledger every Sunday during the weekly
  planning hour.
- The risk column triggers the daily ops loop's check-in topic.
- Quarterly, the ceiling and per-service unit costs are re-baselined
  against actual closure data.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Active project list | Units-used calculation | Founder | Weekly |
| New deal forecast | Capacity check decision | Founder | Per deal |
| Contractor roster | Available extra units | Founder | Monthly |
| Closure report | Per-service unit re-baseline | Founder | Quarterly |

## Metrics
- Weeks at green (≤ 80%) — share of weeks at low risk; target ≥ 50%.
- Weeks at red (> 100%) — share of weeks at high risk; target ≤ 10%.
- Action-on-red rate — share of high-risk weeks with a documented action; target 100%.
- Forecast accuracy — share of weeks where projected units matched actual within ±1 unit; target ≥ 80%.

## Related
- `docs/V14_FOUNDER_DAILY_OPS.md` — daily ops loop that reads this ledger.
- `docs/ops/DAILY_OPERATING_LOOP.md` — operating cadence aligned to the ledger.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — phase plan whose pacing depends on this ledger.
- `docs/company/DELIVERY_CAPACITY_MODEL.md` — model the ledger implements.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
