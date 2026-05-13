# Unit Economics — Per-Sprint Margin Model

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [UNIT_ECONOMICS_AR.md](./UNIT_ECONOMICS_AR.md)

## Context
This file is the per-sprint unit-economics view. It does not replace
`docs/UNIT_ECONOMICS_AND_MARGIN.md` (the company-level margin treatment)
— it operationalizes it down to each individual sprint type so that a
founder can decide on pricing in a single look. It enforces the
discipline of `docs/DEALIX_OPERATING_CONSTITUTION.md` that no service
may be sold without a written margin target.

## Sprint Unit Economics

### Lead Intelligence Sprint
| Line | Value |
|---|---|
| Price | SAR 12,000 |
| Founder hours | 12 |
| AI / tool cost | SAR 100 - 300 |
| Contractor cost | SAR 0 - 1,500 |
| Gross margin target | ≥ 70% |

### AI Quick Win Sprint
| Line | Value |
|---|---|
| Price | SAR 10,000 |
| Founder hours | 10 - 15 |
| AI / tool cost | SAR 100 - 300 |
| Contractor cost | SAR 0 |
| Gross margin target | ≥ 70% |

### Company Brain Sprint
| Line | Value |
|---|---|
| Price | SAR 35,000 |
| Founder hours | 30 - 50 |
| AI / tool cost | SAR 500 - 1,500 |
| Contractor / engineering | SAR 3,000 - 8,000 |
| Gross margin target | ≥ 60% |

## Pricing Rule

> If a service eats time without building an asset, raise the price or
> stop selling it. If a service builds both proof and product asset,
> you may accept a pilot at a small discount.

The asset test is binary: does this delivery leave behind (a) an
anonymizable proof artifact and (b) a reusable module, prompt, or
template? If yes to both, the work compounds and a discount is
defensible. If no to either, raise the price.

## Margin Watchpoints

- Founder hours over budget by > 25% — escalate to pricing review.
- AI / tool cost over budget by > 50% — escalate to LLM gateway / model routing.
- Contractor cost above price × 25% — margin breach.

## Anti-pattern: the silent cost

The most common margin killer is unbilled rework caused by missing
intake or weak data readiness. Track rework hours separately and
attribute them to root cause before declaring a sprint profitable.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint definition, expected effort | Price + margin target | Founder | Per sprint type |
| Actual hours, AI cost, contractor cost | Realized margin | Founder | Per sprint close |
| Margin breaches | Pricing or scope adjustment | Founder | Monthly |

## Metrics
- Realized gross margin per sprint type — vs. target.
- Founder hour adherence — actual ÷ budget.
- AI cost adherence — actual ÷ budget.
- Rework hours per sprint — count and root cause.

## Related
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — company-level margin model this file ladders into.
- `docs/FINANCE_DASHBOARD.md` — finance reporting surface that reads these numbers.
- `docs/COST_OPTIMIZATION.md` — AI cost controls referenced by margin watchpoints.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
