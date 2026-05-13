# Pricing Engine — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PRICING_ENGINE_AR.md](./PRICING_ENGINE_AR.md)

## Context

Dealix does not negotiate. Dealix prices. A formula-driven pricing
engine removes the founder anxiety loop, prevents premium pricing
slippage, and aligns sales, delivery, and finance on the same number.
This document extends `docs/OFFER_LADDER_AND_PRICING.md` with the
underlying formula and operationalizes the margin floor in
`docs/UNIT_ECONOMICS_AND_MARGIN.md` and
`docs/company/MARGIN_GUARD.md`. Every proposal generated from
`docs/sales/PROPOSAL_LIBRARY.md` derives its price here.

## The Formula

```
Price = Base
      + Data Complexity Premium
      + Governance Risk Premium
      + Urgency Premium
      + Integration Premium
      + Stakeholder Complexity Premium
```

- **Base** — the listed price of the productized offer (Lead
  Intelligence Sprint, AI Quick Win Sprint, Company Brain Sprint,
  RevOps Retainer, etc.).
- **Premiums** — applied as percentages of the Base, additive, not
  multiplicative. The sum of premiums caps at 150% of Base.

## Premium Bands

### Data Complexity Premium

| Situation | Premium |
|---|---:|
| Clean CSV/CRM export, one source, structured | 0% |
| Multi-source, mixed structure, light cleaning | 15% |
| Messy, partial, multi-system, heavy ETL, Arabic noise | 30-50% |

### Governance Risk Premium

| Situation | Premium |
|---|---:|
| Internal-only, no PII, no external action | 0% |
| Limited PII, internal approval workflows | 15-25% |
| Heavy PII, regulated industry, external action with approval | 30-50% |

### Urgency Premium

| Situation | Premium |
|---|---:|
| Standard timeline (≥4 weeks) | 0% |
| Tightened timeline (2-3 weeks) | 20% |
| Rush (≤1-2 weeks, displaces other work) | 50% |

### Integration Premium

| Situation | Premium |
|---|---:|
| No integration (file delivery, dashboard) | 0% |
| One mature integration (Salesforce, HubSpot, sheets) | 10-20% |
| Custom or legacy integration (ERP, in-house CRM) | 25-40% |

### Stakeholder Complexity Premium

| Situation | Premium |
|---|---:|
| One executive sponsor, one operator | 0% |
| 2-3 stakeholders aligned | 10% |
| 4+ stakeholders, cross-department, board-watched | 20-30% |

## Worked Example

A bank wants the Lead Intelligence Sprint with:

- Base: SAR 60,000.
- Data: messy multi-source → 30% = +18,000.
- Governance: heavy PII, regulated → 30% = +18,000.
- Urgency: 2 weeks → 20% = +12,000.
- Integration: custom CRM → 25% = +15,000.
- Stakeholders: 5 (board-watched) → 20% = +12,000.

Total premium = 125% of Base.
**Price = 60,000 + 75,000 = SAR 135,000.**

## Discount Rule

> **Never discount without strategic value.**

A discount may be applied only if the client provides one of:

- A **signed case study release** (within 60 days).
- A **public logo placement** with named quote.
- A **partner co-pitch** with documented commitment.
- A **proof asset** we can publish (anonymized metrics, benchmark).
- A **lighthouse contract** in a target vertical, signed off by CEO.

Discount sizing rules:

| Strategic value | Max discount |
|---|---:|
| Case study + logo + quote | 15% |
| Partner co-pitch only | 10% |
| Lighthouse target vertical | 20% |
| None of the above | **0%** |

Discounts are recorded in the Pricing Log with the strategic asset
delivered date. If the asset is not delivered on time, the discount
is invoiced at next renewal.

## What Is Not Pricing

- **Scope reduction** is not a discount. Reducing scope means the
  Base changes.
- **Payment term shifts** (e.g. 100% upfront) may earn a 3-5%
  process discount but only on standard-priced engagements.
- **Multi-engagement bundles** are priced via Retainer logic in
  `docs/retainers/RETAINER_OPERATING_SYSTEM.md`.

## Workflow

1. COO confirms project is Accepted
   (`docs/company/PROJECT_ACCEPTANCE_SYSTEM.md`).
2. Sales pulls Base from the approved offer list.
3. Sales applies premium bands using intake data; documents each
   premium with one-line justification.
4. CEO signs off on price ≥ SAR 100,000 or any discount.
5. Proposal generated from `docs/sales/PROPOSAL_LIBRARY.md`.
6. Margin projected against `docs/company/MARGIN_GUARD.md`; if below
   floor, premium must rise or scope reduce.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Acceptance scorecard, intake form, data fit notes | Quoted price, premium breakdown | Sales + CEO | Per project |
| Margin guard floor | Price floor | CFO/CEO | Per project |
| Pricing log | Discount audit, premium trends | CEO | Monthly |

## Metrics

- **Average premium % applied** — track quarterly, target ≥30%.
- **Discount rate** — % of proposals discounted (target ≤20%).
- **Strategic-value-honored rate** — % of discounted deals that
  delivered the strategic asset (target 100%).
- **Price-to-margin compliance** — % of projects meeting margin
  floor (target 100%).

## Related

- `docs/OFFER_LADDER_AND_PRICING.md` — public price ladder.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot pricing template.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — margin model under the formula.
- `docs/revenue/PRICING_AND_PACKAGING.md` — packaging detail.
- `docs/company/MARGIN_GUARD.md` — margin floor enforcement.
- `docs/company/RISK_ADJUSTED_PRICING.md` — risk-adjusted pricing sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
