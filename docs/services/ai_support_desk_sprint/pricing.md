# Pricing — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Margin Controller
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [pricing_AR.md](./pricing_AR.md)

## Context
Pricing enforcement for the AI Support Desk Sprint. Implements `docs/company/MARGIN_CONTROL.md`, `docs/company/RISK_ADJUSTED_PRICING.md`, the pricing ladder in `docs/OFFER_LADDER_AND_PRICING.md`, and the clinics premium in `docs/playbooks/clinics_playbook.md`.

## Price Band
**SAR 12,000 – SAR 30,000 per Sprint** (fixed fee, exclusive of VAT).

## Band Anchors
| Tier | Indicative Price (SAR) | When |
|---|---|---|
| Light | 12,000 | ≤ 500 msg/wk, 2 channels, no sensitivity |
| Standard | 18,000 | 500–1,000 msg/wk, 3 channels, mild premium |
| Complex | 24,000 | 1,000–1,500 msg/wk, multi-channel, 1 premium |
| Heavy | 30,000 | 1,500–2,000 msg/wk, sensitive sector, multilingual |

## Premiums
| Trigger | Premium | Source |
|---|---|---|
| Clinics / healthcare | +30% to +50% | `docs/playbooks/clinics_playbook.md` |
| Other sensitive data | +20% to +40% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Multilingual (> 2 languages) | +15% | This file |
| Urgency < 14 days | +20% to +50% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Volume > 1,500/wk | +15% | This file |
| Agent count > 5 | +10% to +20% | This file |
| Multi-jurisdiction processing | +SAR 5,000 flat | This file |

**Stacking rule**: max total premium = +100%.

## Minimum Acceptable Price
**SAR 9,500.** Cost envelope:
- Delivery direct cost ≈ SAR 4,200.
- AI tooling + infra ≈ SAR 500.
- QA + GR + proof pack ≈ SAR 1,000.
- Target floor margin 60% → minimum SAR 9,500.

Below this, the Sprint loses money.

## Gross Margin Target
- **Target ≥ 60%** at Standard anchor.
- **Floor ≥ 55%** at minimum.

## Cost Envelope (Reference)
| Cost Item | Light | Standard | Complex | Heavy |
|---|---|---|---|---|
| DL time | 1.5 d | 2.5 d | 3.5 d | 4.5 d |
| Analyst time | 2.5 d | 3.5 d | 4.5 d | 5.5 d |
| Copy Lead time | 1.5 d | 2.5 d | 3.0 d | 4.0 d |
| Governance Reviewer time | 1.0 d | 1.5 d | 2.0 d | 2.5 d |
| QA time | 0.5 d | 0.8 d | 1.0 d | 1.5 d |
| AI tooling | SAR 250 | SAR 450 | SAR 700 | SAR 1,000 |
| Infra | SAR 100 | SAR 100 | SAR 150 | SAR 200 |
| Indirect overhead | 15% | 15% | 15% | 15% |

## Discounts
- **Bundle with Lead Intelligence Sprint** → 8% off list.
- **3 prepaid sprints** → 10%. **6 prepaid** → 15%. Never below floor.
- **Trust-page consent** → 5%. Stackable.
- **Cancellation penalty**: 40% if within 5 days of kickoff.

## Payment Terms
- 50% deposit at SOW; 50% on Day 14 acceptance.
- ZATCA-compliant invoicing.
- VAT applied at prevailing KSA rate.

## Quote Validity
- 30 calendar days. Premiums re-evaluated after expiry.

## Worked Examples
1. B2B SaaS, 700 msg/wk, 3 channels, no sensitivity → Standard SAR 18,000.
2. Clinic chain, 1,200 msg/wk, clinics premium +40% → 24,000 × 1.40 = SAR 33,600 (above band → scoped engagement).
3. Insurance, 1,500 msg/wk, sensitive +30%, multilingual +15% → 24,000 × 1.45 = SAR 34,800 (above band → scoped engagement).
4. SaaS, 400 msg/wk, Light → SAR 12,000.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake answers | Computed price | Sales Engineer | Same day |
| Computed price | Margin validation | Margin Controller | ≤ 4 hours |
| Validated price | SOW + invoice | Ops | ≤ 1 day |
| Day 14 acceptance | Final invoice | Finance | Day 14 |

## Metrics
- **Realized gross margin** — Target ≥ 60%.
- **Discount rate** — Target ≤ 20%.
- **Floor breaches** — Target = 0.
- **Clinics premium application accuracy** — Target = 100%.

## Related
- `docs/company/MARGIN_CONTROL.md` — margin enforcement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics
- `docs/COST_OPTIMIZATION.md` — cost levers
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy
- `docs/INVOICING_ZATCA_READINESS.md` — invoicing
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
