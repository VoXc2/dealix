# Pricing — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Margin Controller
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [pricing_AR.md](./pricing_AR.md)

## Context
Pricing enforcement for the AI Quick Win Sprint. The band, premiums, minimum, and cost envelope below implement `docs/company/MARGIN_CONTROL.md`, `docs/company/RISK_ADJUSTED_PRICING.md`, and the pricing ladder in `docs/OFFER_LADDER_AND_PRICING.md`. Computed by the Sales Engineer, validated by the Margin Controller, paid via ZATCA-compliant invoices.

## Price Band
**SAR 7,500 – SAR 15,000 per Sprint** (fixed fee, exclusive of VAT).

## Band Anchors
| Tier | Indicative Price (SAR) | When |
|---|---|---|
| Light | 7,500 | Simple workflow, ≤ 1 hour current cycle, no premiums |
| Standard | 10,000 | 1–3 hour current cycle, low risk |
| Complex | 12,500 | 3+ hour current cycle, multiple tools, 1 premium |
| Heavy | 15,000 | Cross-tool, 2 premiums, sensitive data |

## Premiums
| Trigger | Premium | Source |
|---|---|---|
| Sensitive data | +20% to +40% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Urgency < 7 days | +20% to +50% | Same |
| Stakeholders > 3 | +15% to +30% | Same |
| Saturday/holiday delivery | +SAR 1,500 flat | This file |
| Languages beyond AR + EN | +SAR 1,500/lang | This file |

**Stacking rule**: max total premium = +100%.

## Minimum Acceptable Price
**SAR 5,000.** Cost envelope:
- Delivery direct cost ≈ SAR 2,100.
- AI tooling + infra ≈ SAR 250.
- QA + proof pack ≈ SAR 500.
- Target floor margin = 60% → minimum SAR 5,000.

Below this, the Sprint loses money.

## Gross Margin Target
- **Target ≥ 65%** at the Standard anchor.
- **Floor ≥ 60%** at the minimum.

## Cost Envelope (Reference)
| Cost Item | Light | Standard | Complex | Heavy |
|---|---|---|---|---|
| DL time | 0.5 d | 1.0 d | 1.5 d | 2.0 d |
| Designer time | 1.5 d | 2.0 d | 3.0 d | 3.5 d |
| QA time | 0.3 d | 0.4 d | 0.5 d | 0.8 d |
| AI tooling | SAR 80 | SAR 120 | SAR 200 | SAR 350 |
| Infra | SAR 40 | SAR 40 | SAR 50 | SAR 60 |
| Indirect overhead | 15% | 15% | 15% | 15% |

## Discounts
- **Bundle with Lead Intelligence Sprint** → 8% off list.
- **3 prepaid sprints** → 10% off list. **6 prepaid** → 15% off list. Never below floor.
- **Trust-page consent** → 5% off list.
- **Cancellation penalty**: 40% if within 3 days of kickoff.

## Payment Terms
- 50% deposit at SOW; 50% on Day 7 acceptance.
- ZATCA-compliant invoicing.
- VAT applied at prevailing KSA rate.

## Quote Validity
- 30 calendar days. After expiry, intake premiums re-evaluated.

## Worked Examples
1. Operations team, monthly report workflow, 3h baseline → Standard SAR 10,000.
2. Finance team, sensitive premium 30%, monthly invoice review → 10,000 × 1.30 = SAR 13,000.
3. HR team, urgent 5-day delivery (+30%), complex workflow → 12,500 × 1.30 = SAR 16,250 (escalate to scoped engagement).
4. Marketing team, simple weekly digest, Light tier → SAR 7,500.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake answers | Computed price | Sales Engineer | Same day |
| Computed price | Margin validation | Margin Controller | ≤ 4 hours |
| Validated price | SOW + invoice | Ops | ≤ 1 day |
| Day 7 acceptance | Final invoice | Finance | Day 7 |

## Metrics
- **Realized gross margin** — Target ≥ 65%.
- **Discount rate** — Target ≤ 20%.
- **Floor breaches** — Target = 0.

## Related
- `docs/company/MARGIN_CONTROL.md` — margin enforcement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics
- `docs/COST_OPTIMIZATION.md` — cost levers
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy
- `docs/INVOICING_ZATCA_READINESS.md` — invoicing
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
