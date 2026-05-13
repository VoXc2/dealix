# Productization Ledger — Dealix Growth Layer

**Layer:** L6 · Growth Machine
**Owner:** Head of Product / Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PRODUCTIZATION_LEDGER_AR.md](./PRODUCTIZATION_LEDGER_AR.md)

## Context
The Productization Ledger is Dealix's discipline against premature
product building. Instead of imagining features, we record every manual
delivery step, count how many times it repeats, attach a time / risk
cost, and only then decide to build. It enforces the build-from-market
principle from `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and constrains
the architecture choices in `docs/BEAST_LEVEL_ARCHITECTURE.md` and the
reliability ceiling in `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`.
Removes the constraint of "engineers building untested features."

## Core Rule

> **Repeated ≥ 3 times + revenue link + time / risk = build the feature.**
>
> Product is born from market, not imagination.

A step is eligible for productization only when **all three** conditions
are present. Two-of-three keeps the step in the manual ledger.

## Ledger Format

Every Sprint delivery contributes rows. The full ledger lives in the
delivery tracker; this file holds the schema, sample rows, and the
decision policy.

### Schema

| Column | Meaning |
|---|---|
| Manual Step | Concrete operational step performed by hand. |
| Repeated Count | Number of times this step has been executed across deliveries. |
| Time Cost | Average hours per project this step consumes. |
| Risk | low / medium / high — based on error blast radius. |
| Revenue Link | Which offer / Sprint depends on this step. |
| Decision | Build / Defer / Drop. |

### Sample Rows

| Manual Step | Repeated Count | Time Cost | Risk | Revenue Link | Decision |
|---|---:|---:|---|---|---|
| CSV cleanup | 3 | 6h/project | medium | Lead Sprint | Build `import_preview` |
| Proof report writing | 3 | 4h/project | low | all sprints | Build report generator |
| Claims review | 5 | 1h/project | high | outreach | Build `forbidden_claims` |
| Mini CRM board setup | 2 | 2h/project | low | Lead Sprint | Defer |
| Document classification | 1 | 5h/project | medium | Company Brain | Defer |

## Decision Policy

1. **Build** — meets all three criteria; feature added to product
   roadmap with a name + owner + ship date.
2. **Defer** — fewer than 3 occurrences OR no clear revenue link;
   re-evaluated each quarter.
3. **Drop** — repeated only because of misscoping; close the loop by
   updating the relevant sales page or proposal template, not by
   building.

## What NOT to Productize

- Anything blocked by the "Do NOT" list in
  `docs/growth/GROWTH_MACHINE.md` (autonomous agents, mass automation,
  guaranteed-result tooling).
- Anything that violates the AI stance in
  `docs/AI_STACK_DECISIONS.md`.
- Anything that increases attack surface beyond the limits in
  `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`.

## Cadence

| When | Action | Owner |
|---|---|---|
| End of every Sprint | Add new rows / increment counts | Delivery Lead |
| Weekly | Triage Build / Defer / Drop | Head of Product |
| Monthly | Promote Build decisions to product roadmap | Head of Product |
| Quarterly | Review all Defer rows | Founder + Product |

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint delivery logs | New / incremented ledger rows | Delivery Lead | Per Sprint |
| Ledger rows | Build / Defer / Drop decisions | Head of Product | Weekly |
| Build decisions | Product roadmap items | Head of Product | Monthly |
| Drop decisions | Sales-asset corrections | Growth | Monthly |

## Metrics

- **Productization rate** — Build decisions per quarter.
- **Time-cost reduction** — hours saved per productized step.
- **Drop rate** — share of steps closed via sales-asset correction.
- **Backlog age** — average age of Defer rows.

## Related

- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural target for builds.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — non-negotiable constraints.
- `docs/AI_STACK_DECISIONS.md` — AI-side stance the ledger respects.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
