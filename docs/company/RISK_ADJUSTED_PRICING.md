# Risk-Adjusted Pricing — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [RISK_ADJUSTED_PRICING_AR.md](./RISK_ADJUSTED_PRICING_AR.md)

## Context
Not all engagements carry the same risk. Dealix prices risk
explicitly: when a deal has higher data sensitivity, more complex
approvals, tighter timeline, or compliance burden, the price moves to
match. This file declares the premiums and the scope-splits used.
It works alongside `docs/revenue/PRICING_AND_PACKAGING.md`, the margin
rules in `docs/UNIT_ECONOMICS_AND_MARGIN.md`, and the data-processing
boundaries in `docs/DPA_DEALIX_FULL.md`.

## Premium table

| Risk Factor | Adjustment |
|---|---|
| High data sensitivity | +20–40% |
| Complex stakeholder approvals | +15–30% |
| Tight timeline | +20–50% |
| Integration required | Separate scope |
| Enterprise compliance required | Separate enterprise pricing |
| No clean data | Start with diagnostic or data cleanup |

The bands give the founder room to negotiate within bounded judgment.
The decision and the chosen percentage are recorded in the proposal
and in the Capital Ledger comment field.

## The core rule

> Never absorb extra risk at the same price.

Absorbed risk is hidden cost. It depletes margin invisibly until
delivery cracks. The premium is what makes the engagement honest.

## Factor definitions

- **High data sensitivity** Healthcare records, government data,
  financial PII, payroll, regulated identity data, or anything
  triggering the controls in
  `docs/DPA_DEALIX_FULL.md`.
- **Complex stakeholder approvals** More than three decision makers,
  legal involved, board sign-off required, or cross-functional
  coordination above two departments.
- **Tight timeline** Calendar window less than 60% of the typical
  delivery duration for that service.
- **Integration required** Anything that needs sustained engineering
  effort against a third-party system; priced as a separate scope so
  the sprint price stays clean.
- **Enterprise compliance** External audits, certifications, or
  regulator-facing artifacts; never folded into a sprint price.
- **No clean data** A diagnostic or data-cleanup engagement is
  inserted upstream rather than absorbing the cost into the sprint.

## Stacking and limits

- Premiums stack additively, with a maximum total premium of +80%.
- Above +80% the deal is reframed as Enterprise.
- Below the band (e.g., low risk) no discount is applied; the floor
  rule in `docs/company/MARGIN_CONTROL.md` still binds.

## Workflow

1. Risk factors are checked on the intake brief.
2. The founder writes the chosen premium in the proposal.
3. The proposal must reference this file by name and the specific
   factor(s) triggering the adjustment.
4. At closure, the actual incurred risk is compared against the
   premium; misalignments inform the next quarterly pricing review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake brief | Risk factor list | Founder | Per deal |
| Risk premium | Proposal price | Founder | Per deal |
| Closure report | Realized risk vs. premium | Founder | Per project |
| Quarterly review | Band recalibration | Founder | Quarterly |

## Metrics
- Premium application rate — share of qualifying deals priced with a premium; target ≥ 90%.
- Premium realization — share of premium-priced deals that delivered without absorbing extra unpaid risk; target ≥ 80%.
- Reframe rate — deals reframed as Enterprise due to ≥ +80% premium; tracked, no cap.
- Diagnostic upstreaming — share of "no clean data" deals correctly preceded by a diagnostic; target 100%.

## Related
- `docs/revenue/PRICING_AND_PACKAGING.md` — pricing layer where premiums land.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — economics that contextualize premiums.
- `docs/DPA_DEALIX_FULL.md` — data-processing rules behind sensitivity premium.
- `docs/company/MARGIN_CONTROL.md` — floor rule that always remains binding.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
