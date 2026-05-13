# Capacity Model — Founder-Solo Cap

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPACITY_MODEL_AR.md](./CAPACITY_MODEL_AR.md)

## Context
This file is the *simple* founder-solo capacity cap — the rule for how
many active engagements one founder can carry without breaking
delivery quality. It is a sibling, not a replacement, to the detailed
scaling model in `docs/company/DELIVERY_CAPACITY_MODEL.md` (L1). When
in doubt, this file governs the day-to-day decision; the L1 file
governs the headcount plan. It plugs into the constitution in
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Capacity Units

A capacity unit is the standard unit of concurrent founder attention.

| Service | Capacity units |
|---|---:|
| Revenue Diagnostic | 1 |
| Lead Intelligence Sprint | 2 |
| AI Quick Win Sprint | 2 |
| Company Brain Sprint | 4 |
| Support Desk Sprint | 3 |
| Governance Program | 4 |
| Retainer (monthly) | 1 - 2 / month |

## The Cap

> Founder-solo maximum active load = 4 - 5 units.

When the active load reaches 5:

1. Do not accept new work at the same price.
2. Choose one of:
   - Raise the price for the next accepted unit.
   - Extend the schedule (start later).
   - Bring in a contractor.

This is the *capacity gate* — every new SOW must clear it before the
founder signs.

## Computing Active Load

Active load = sum of capacity units for every engagement that is in
intake, scoping, delivery, or QA. Retainers count their monthly unit
even in weeks where the delivery is light.

Worked example:
- 1 Lead Intel Sprint (2) + 1 AI Quick Win (2) + 1 monthly retainer (1)
  = **5 units → at the cap.** Reject or reprice.

## When to Bring a Contractor

Use a contractor (not a hire) when:
- The over-cap demand is bounded — one specific sprint, not an ongoing
  flow.
- The role is well-scoped (engineering for Company Brain, content for
  reporting).
- Margin will hold (contractor cost ≤ 25% of sprint price — see
  `docs/company/UNIT_ECONOMICS.md`).

When the same contractor role is needed three months in a row, that is
the trigger to hire — see `docs/HIRING_CSM_FIRST.md`.

## Relationship to L1 Capacity Model

| File | Purpose | Use when |
|---|---|---|
| `docs/company/DELIVERY_CAPACITY_MODEL.md` (L1) | Detailed scaling model | Planning headcount, multi-quarter |
| `docs/company/CAPACITY_MODEL.md` (this, L7) | Founder-solo daily cap | Deciding whether to accept this SOW |

Both files share the same capacity-unit definitions. When they diverge,
escalate.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Pipeline, signed SOWs, retainer roster | Active load (units) | Founder | Weekly |
| Active load vs cap | Accept / reprice / extend / contractor | Founder | Per SOW |
| Repeated contractor demand | Hire trigger | Founder | Quarterly |

## Metrics
- Active load — units in flight (target ≤ 5 solo).
- Cap-hit weeks — count per quarter where load ≥ 5.
- Contractor utilization — contractor hours ÷ sprint hours.
- Reprice acceptance rate — % of SOWs accepted at the higher price after cap.

## Related
- `docs/company/DELIVERY_CAPACITY_MODEL.md` — sibling L1 scaling model.
- `docs/HIRING_CSM_FIRST.md` — hire trigger logic.
- `docs/V14_FOUNDER_DAILY_OPS.md` — daily ops that consume capacity.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
