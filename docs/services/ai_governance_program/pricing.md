# Pricing — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** Margin Controller
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [pricing_AR.md](./pricing_AR.md)

## Context
Pricing enforcement for the top-tier AI Governance Program. Implements `docs/company/MARGIN_CONTROL.md`, `docs/company/RISK_ADJUSTED_PRICING.md`, the pricing ladder in `docs/OFFER_LADDER_AND_PRICING.md`, and the enterprise overlay logic in `docs/enterprise/CONTROLS_MATRIX.md`. Computed by Sales Engineer + Margin Controller; the wider band reflects the wider risk surface and the sector-specific overlays.

## Price Band
**SAR 35,000 – SAR 150,000 per Program** (fixed fee, exclusive of VAT).

The Program is the highest-tier service on the ladder; band is wide because company size, sector, and regulatory exposure vary dramatically.

## Band Anchors
| Tier | Indicative Price (SAR) | When |
|---|---|---|
| Light | 35,000 | 50–200 employees, 5–10 AI uses, low sensitivity, target Level 3 |
| Standard | 65,000 | 200–1,000 employees, 10–20 AI uses, moderate sensitivity, target Level 3–4 |
| Complex | 100,000 | 1,000–5,000 employees, 20–30 AI uses, sensitive sector, target Level 4 |
| Heavy | 150,000 | 5,000+ employees, 30 AI uses, regulated sector, target Level 4–5 |

## Premiums
| Trigger | Premium | Source |
|---|---|---|
| Enterprise (5,000+ employees) | +50% to +100% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Healthcare sector | +30% to +50% | This file + `docs/playbooks/clinics_playbook.md` |
| Government sector | +30% to +50% | This file |
| Finance sector | +20% to +40% | This file |
| Multi-jurisdiction (GCC + non-GCC) | +20% to +40% | This file |
| Active regulatory engagement | +50% to +100% | This file |
| Urgency < 8 weeks | +20% to +40% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| > 30 AI uses requested | scope out, not premium | This file |

**Stacking rule**: max total premium = +150% (governance programs can stack higher than sprints).

## Minimum Acceptable Price
**SAR 25,000.** Cost envelope:
- Delivery direct cost ≈ SAR 12,500.
- AI tooling + infra ≈ SAR 800.
- Compliance specialist time ≈ SAR 2,500.
- QA + GR + capability lead overhead ≈ SAR 3,000.
- Target floor margin 55% → minimum SAR 25,000.

Below this, the Program loses money or destroys senior team morale.

## Gross Margin Target
- **Target ≥ 55%** at Standard anchor.
- **Floor ≥ 50%** at minimum.

The margin floor is intentionally lower than the other services because governance programs require senior, expensive talent.

## Cost Envelope (Reference)
| Cost Item | Light | Standard | Complex | Heavy |
|---|---|---|---|---|
| DL time | 5 d | 10 d | 15 d | 22 d |
| Governance Reviewer time | 12 d | 22 d | 32 d | 45 d |
| Compliance Specialist time | 4 d | 8 d | 12 d | 18 d |
| Capability Lead time | 1 d | 2 d | 3 d | 5 d |
| QA time | 1.5 d | 2.5 d | 4 d | 6 d |
| AI tooling | SAR 500 | SAR 1,000 | SAR 1,800 | SAR 2,500 |
| Infra | SAR 300 | SAR 400 | SAR 500 | SAR 700 |
| Indirect overhead | 15% | 15% | 15% | 15% |

## Discounts
- **Bundle with Monthly Governance retainer** (committed 12-month) → 10% off list.
- **3 prepaid programs (multi-entity) ** → 12% off list. Never below floor.
- **Trust-page publication consent (with sector consent)** → 5% off list. Stackable.
- **Cancellation penalty**: 25% if cancelled within 14 days of kickoff; 50% if within 7 days.

## Payment Terms
- 30% deposit at SOW; 30% at Phase 2 milestone; 30% at Phase 4 milestone; 10% at final acceptance.
- ZATCA-compliant invoicing.
- VAT applied at prevailing KSA rate.
- Multi-jurisdiction clients: billing entity selection per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Quote Validity
- 45 calendar days. Premiums re-evaluated after expiry.

## Worked Examples
1. Mid-market B2B SaaS, 300 employees, 12 AI uses, no sensitivity → Standard SAR 65,000.
2. Hospital group, 800 employees, 18 AI uses, healthcare +40% → 65,000 × 1.40 = SAR 91,000.
3. Bank, 2,500 employees, 22 AI uses, finance +30%, multi-jurisdiction +30% → 100,000 × 1.60 = SAR 160,000 (above band → scoped enterprise engagement).
4. Govt-adjacent, 1,500 employees, 25 AI uses, government +40%, active regulatory engagement +60% → 100,000 × 2.00 = SAR 200,000 (above band → scoped).
5. Family-office holding, 80 employees, 6 AI uses, Light → SAR 35,000.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake answers | Computed price | Sales Engineer | Within 2 days |
| Computed price | Margin validation + sector check | Margin Controller + Capability Lead | Within 1 day |
| Validated price | SOW + invoice | Ops | Within 2 days |
| Phase milestones | Phase invoices | Finance | At each milestone |
| Final acceptance | Final invoice | Finance | Final week |

## Metrics
- **Realized gross margin** — Target ≥ 55%.
- **Discount rate** — Target ≤ 15%.
- **Floor breaches** — Target = 0.
- **Sector premium accuracy** — `% programs where applied sector premium matches delivered work`. Target ≥ 90%.

## Related
- `docs/company/MARGIN_CONTROL.md` — margin enforcement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics
- `docs/COST_OPTIMIZATION.md` — cost levers
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy
- `docs/INVOICING_ZATCA_READINESS.md` — invoicing
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
