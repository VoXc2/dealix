# Pricing — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Margin Controller
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [pricing_AR.md](./pricing_AR.md)

## Context
Pricing enforcement for the Company Brain Sprint. Implements `docs/company/MARGIN_CONTROL.md`, `docs/company/RISK_ADJUSTED_PRICING.md`, and the pricing ladder in `docs/OFFER_LADDER_AND_PRICING.md`. Sales Engineer computes; Margin Controller validates; ZATCA-compliant invoices.

## Price Band
**SAR 20,000 – SAR 60,000 per Sprint** (fixed fee, exclusive of VAT).

The Sprint is medium-length (3–4 weeks) with substantial governance content, hence the wider band.

## Band Anchors
| Tier | Indicative Price (SAR) | When |
|---|---|---|
| Light | 20,000 | 50–75 docs, 1 source system, 1 user group, no sensitivity |
| Standard | 35,000 | 75–125 docs, 2–3 source systems, 2 user groups |
| Complex | 47,500 | 125–200 docs, 3+ source systems, 3 user groups |
| Heavy | 60,000 | 200 docs, multi-jurisdiction, sensitive data, 3 user groups |

## Premiums
| Trigger | Premium | Source |
|---|---|---|
| Sensitive data | +20% to +40% | `docs/company/RISK_ADJUSTED_PRICING.md` |
| Urgency (< 3 weeks delivery) | +20% to +50% | Same |
| Stakeholders > 3 | +15% to +30% | Same |
| Integration required (Slack/Teams/Notion bot) | +SAR 5,000 flat | This file |
| Additional language (beyond AR + EN) | +SAR 3,000/lang | This file |
| Multi-jurisdiction processing | +SAR 8,000 flat | This file |

**Stacking rule**: max total premium = +100%.

## Minimum Acceptable Price
**SAR 16,000.** Cost envelope:
- Delivery direct cost ≈ SAR 7,800.
- AI tooling + infra (embeddings, vector DB, model API) ≈ SAR 1,500.
- QA + GR + proof pack ≈ SAR 2,000.
- Target floor margin 60% → minimum SAR 16,000.

Below this, the Sprint loses money.

## Gross Margin Target
- **Target ≥ 60%** at Standard anchor.
- **Floor ≥ 55%** at minimum acceptable.

## Cost Envelope (Reference)
| Cost Item | Light | Standard | Complex | Heavy |
|---|---|---|---|---|
| DL time | 3 d | 5 d | 7 d | 9 d |
| Knowledge Engineer time | 7 d | 10 d | 13 d | 16 d |
| Governance Reviewer time | 1.5 d | 2.5 d | 3.5 d | 4 d |
| QA time | 1 d | 1.5 d | 2 d | 2.5 d |
| AI tooling | SAR 800 | SAR 1,500 | SAR 2,500 | SAR 3,500 |
| Vector DB | SAR 400 | SAR 600 | SAR 800 | SAR 1,000 |
| Indirect overhead | 15% | 15% | 15% | 15% |

## Discounts
- **Bundle with AI Quick Win Sprint** → 8% off list.
- **3 prepaid sprints** → 10% off list. **6 prepaid** → 15%. Never below floor.
- **Trust-page publication consent** → 5% off list.
- **Cancellation penalty**: 30% if cancelled within 7 days of kickoff.

## Payment Terms
- 50% deposit at SOW; 30% at Week 2 milestone; 20% at Week 4 acceptance.
- ZATCA-compliant invoicing.
- VAT applied at prevailing KSA rate.

## Quote Validity
- 30 calendar days. After expiry, premiums re-evaluated.

## Worked Examples
1. 80-doc operations corpus, 2 user groups, no sensitivity → Standard SAR 35,000.
2. 150-doc policy + finance corpus, sensitivity +30%, 3 groups → 47,500 × 1.30 = SAR 61,750 (above band → scoped engagement).
3. 200-doc cross-jurisdiction corpus, sensitivity +40%, multi-jurisdiction +SAR 8,000 → 60,000 × 1.40 + 8,000 = SAR 92,000 (scoped engagement).
4. 60-doc sales playbook, 1 group, Light → SAR 20,000.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake answers | Computed price | Sales Engineer | Same day |
| Computed price | Margin validation | Margin Controller | ≤ 4 hours |
| Validated price | SOW + invoice | Ops | ≤ 1 day |
| Week 4 acceptance | Final invoice | Finance | Week 4 |

## Metrics
- **Realized gross margin** — Target ≥ 60%.
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
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
