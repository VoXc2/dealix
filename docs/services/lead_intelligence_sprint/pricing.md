# Pricing — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Margin Controller
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [pricing_AR.md](./pricing_AR.md)

## Context
Pricing is the **single most leverageable margin lever** in the Dealix entry tier. This file enforces the price band, premiums, minimum acceptable price, and the cost envelope behind the Lead Intelligence Sprint. It implements the rules in `docs/company/MARGIN_CONTROL.md` and `docs/company/RISK_ADJUSTED_PRICING.md` and is the operational expression of the pricing ladder published in `docs/OFFER_LADDER_AND_PRICING.md`.

## Price Band
**SAR 9,500 – SAR 18,000 per Sprint** (fixed fee, exclusive of VAT).

The price within the band is determined by intake answers, not by negotiation. The Sales Engineer computes the price automatically; the Margin Controller validates.

## Band Anchors
| Tier | Indicative Price (SAR) | When |
|---|---|---|
| Light | 9,500 | ≤ 1,500 rows, no premiums, simple ICP, 1 sector |
| Standard | 12,500 | 1,500–5,000 rows, 1 mild premium triggered |
| Complex | 15,500 | 5,000–10,000 rows, or 2 premiums triggered |
| Heavy | 18,000 | Multi-source merge, multi-region scoring, 3+ premiums |

## Premiums (Stack Multiplicatively With Care)
| Trigger | Premium | Source |
|---|---|---|
| Sensitive data (Q14 = yes) | +20% to +40% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Urgency < 10 calendar days | +20% to +50% | Same |
| Stakeholder count > 3 | +15% to +30% | Same |
| Multi-source merge (per extra source) | +SAR 2,500 flat | This file |
| Bilingual delivery beyond AR + EN | +SAR 1,500 per language | This file |
| CRM integration add-on | +SAR 6,000 starting | This file (Scope) |
| Saturday/holiday delivery | +SAR 1,500 flat | This file |

**Stacking rule**: maximum total premium = +100% over the band anchor.

## Minimum Acceptable Price
**SAR 7,500.** No Sprint may be sold below this regardless of negotiation pressure.

Reasons the minimum exists:
- Direct delivery cost ≈ SAR 3,200 (3.5 person-days of senior labour).
- Indirect (tooling, infra, AI cost) ≈ SAR 600.
- QA + proof pack overhead ≈ SAR 800.
- Target contribution margin floor = 60%, which sets minimum at SAR 7,500 (round figure).

Below the minimum, the Sprint loses money or pushes the margin floor of the firm.

## Gross Margin Target
- **Target gross margin: ≥ 65%** at the Standard band anchor.
- **Floor gross margin: ≥ 60%** at the minimum acceptable price.
- Variance below the floor triggers an after-action review with the capability owner.

## Cost Envelope (Reference)
| Cost Item | Light | Standard | Complex | Heavy |
|---|---|---|---|---|
| Delivery Lead time | 1.0 d | 1.5 d | 2.0 d | 2.5 d |
| Analyst time | 1.5 d | 2.5 d | 3.5 d | 4.5 d |
| Copy Lead time | 0.5 d | 1.0 d | 1.0 d | 1.5 d |
| QA Reviewer time | 0.5 d | 0.5 d | 0.5 d | 1.0 d |
| AI tooling | SAR 80 | SAR 150 | SAR 250 | SAR 400 |
| Infra (vault, SFTP) | SAR 50 | SAR 50 | SAR 50 | SAR 50 |
| Indirect overhead | 15% | 15% | 15% | 15% |

## Discounts
- **Volume discount**: 3 sprints prepaid → 10% off list. 6 sprints prepaid → 15% off list. Never below the SAR 7,500 floor.
- **Trust-page consent discount**: client signs publication consent in SOW → 5% off list. Stackable with volume.
- **Cancellation penalty**: 50% of fee if cancelled within 5 days of kickoff.

## Payment Terms
- **50% deposit** at SOW signature, **50% on Day 10 acceptance**.
- ZATCA-compliant invoicing per `docs/INVOICING_ZATCA_READINESS.md`.
- VAT applied at the prevailing KSA rate.
- Cross-border clients: see `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` for billing entity selection.

## Quote Validity
- **30 calendar days** from issue.
- After expiry, intake premium triggers are re-evaluated.

## Worked Examples (Illustrative — Not Negotiated Prices)
1. **B2B SaaS, 4,200 rows, no premiums** → Standard anchor SAR 12,500.
2. **Health clinic chain, 2,800 rows, sensitive premium 30%** → SAR 12,500 × 1.30 = SAR 16,250.
3. **B2B export, 9,500 rows, urgent (7-day delivery, +25%), 4 stakeholders (+15%)** → SAR 15,500 × 1.40 = SAR 21,700 (above band → escalate to scoped engagement).
4. **B2B fintech, 1,200 rows, light** → SAR 9,500.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake answers | Computed price | Sales Engineer | Same day as intake |
| Computed price | Margin validation | Margin Controller | Within 4 hours |
| Validated price | SOW + invoice | Ops | Within 1 business day |
| Day 10 acceptance | Final invoice | Finance | Day 10 |

## Metrics
- **Realized gross margin** — `(price − direct cost) / price`. Target ≥ 65%.
- **Discount rate** — `% sprints with any discount applied`. Target ≤ 20%.
- **Floor breaches** — `count of sprints sold under SAR 7,500`. Target = 0.

## Related
- `docs/company/MARGIN_CONTROL.md` — margin enforcement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics
- `docs/COST_OPTIMIZATION.md` — cost levers
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy
- `docs/INVOICING_ZATCA_READINESS.md` — invoicing
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/capabilities/revenue_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
