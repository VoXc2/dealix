# Operating Intelligence — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OPERATING_INTELLIGENCE_AR.md](./OPERATING_INTELLIGENCE_AR.md)

## Context
Operating Intelligence is the monthly company-level analysis that turns
ledger and service signals into decisions. Without this practice, Dealix
will collect data without using it to raise prices, retire weak services,
or build the right features. It draws from
`docs/ledgers/VALUE_LEDGER.md`, the daily ops loop
`docs/V14_FOUNDER_DAILY_OPS.md`, and feeds the executive view
`docs/EXECUTIVE_DECISION_PACK.md` and dashboards
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`.

## Seven monthly questions

1. Which services produce highest margin?
2. Which services convert to retainers?
3. Which sectors have best data readiness?
4. Which outputs fail QA most often?
5. Which governance risks repeat?
6. Which features would save most time?
7. Which proof types sell best?

## Metrics surfaced

- Service margin (gross and contribution).
- Delivery time per service.
- QA score by service and agent.
- Retainer conversion by service.
- Risk frequency by rule family.
- Feature repetition (custom work repeated across clients).
- Proof strength (Value Type mix and depth).
- Sector conversion and readiness.

## Decision menu

Each monthly review must produce decisions chosen from a small menu:

- **Raise price** — service consistently over-delivers margin.
- **Stop service** — service repeatedly fails margin / retention.
- **Build feature** — repeated manual step justifies productization.
- **Create playbook** — pattern is reusable across clients.
- **Publish content** — proof type sells; write a public version.
- **Target sector** — readiness + conversion suggest concentration.
- **Hire role** — capacity gap blocks growth.

## Operating cadence

- Monthly: Operating Intelligence session (90 minutes).
- Output: 1–3 decisions per category with owners and dates.
- Closure: decisions appear in
  `docs/meetings/OPERATING_REVIEW_PACK.md` next cycle.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Ledger snapshot | Margin and retainer analysis | Head of Delivery | Monthly |
| QA telemetry | Failing-output decisions | Head of AI | Monthly |
| Risk telemetry | Repeat-risk decisions | Head of Compliance | Monthly |
| Decisions | Review pack entries | CEO | Monthly |

## Metrics
- Decision Volume — number of decisions taken per month.
- Decision Closure — % of decisions executed by next cycle.
- Decision Quality — % of decisions producing the expected uplift.
- Question Coverage — % of seven questions answered with data.

## Related
- `docs/EXECUTIVE_DECISION_PACK.md` — executive pack consuming output
- `docs/V14_FOUNDER_DAILY_OPS.md` — daily ops loop
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI surfaces
- `docs/ledgers/VALUE_LEDGER.md` — primary input source
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
