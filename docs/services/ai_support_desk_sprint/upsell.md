# Upsell — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Customer Success Manager
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [upsell_AR.md](./upsell_AR.md)

## Context
Every Support Desk Sprint creates a categorized inbox that decays without maintenance and reveals adjacent problems (workflow gaps, sentiment patterns, regulatory exposure). This file maps proof signals to next-tier offers, implementing the ladder logic in `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and `docs/COMPANY_SERVICE_LADDER.md`. Strategic path: `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Operating Principle
> The categories tell you where the next sprint lives. The escalations tell you where the next program lives.

## Proof → Next-Offer Mapping

### Proof: Categories validated, agents adopted the desk
**Signal**:
- `category_coverage` ≥ 90%.
- Suggested-reply acceptance ≥ 70%.
- Sponsor mentions team productivity.

**Recommended next offer**: **Monthly Support AI** (SAR 15,000–35,000/mo).
- Ongoing tuning, new categories, FAQ refresh, SLA review.
- Talking point: "Your inbox is categorized. Next month it drifts again unless someone maintains it. We maintain."

### Proof: Sentiment pattern emerged
**Signal**:
- During the Sprint, recurring complaint themes appeared.
- Sponsor mentioned NPS or churn pain.

**Recommended next offer**: **Feedback Intelligence Sprint** (SAR 18,000–35,000).
- Sentiment + theme analytics, weekly digest, root-cause drill-down.
- Talking point: "Your customers are telling you something. Let's read it systematically."

### Proof: Process gaps appeared
**Signal**:
- Many categories pointed at the same upstream process (e.g., billing issues, shipping confusion, login problems).
- Sponsor mentioned "if only Operations would fix X".

**Recommended next offer**: **AI Quick Win Sprint** (SAR 7,500–15,000).
- Fix the upstream process that's generating the support load.
- Talking point: "Your top complaint is a 2-hour fix in Operations. Let's fix the cause, not just the response."

### Proof: Multi-channel volume detected
**Signal**:
- Client supports 3+ channels with inconsistent answers.
- Suggested replies needed channel-specific tone.

**Recommended next offer**: **Multi-Channel Standardization Sprint** (custom).
- Unify tone, FAQ, and escalation across channels.
- Talking point: "Your team is giving 3 different answers on 3 channels. Let's unify."

### Proof: Clinics / regulated industry
**Signal**:
- `clinics_playbook_applied = true` OR regulatory pressure mentioned.

**Recommended next offer**: **AI Governance Program** (SAR 35,000–150,000).
- Full governance OS for AI usage in regulated context.
- Talking point: "Healthcare and AI need a governance layer before scale. Let's build it."

### Proof: Customer satisfaction win demonstrated
**Signal**:
- Response time improved measurably during the Sprint pilot.
- Sponsor agrees this is publishable.

**Recommended next offer**: **Co-marketing slot on the Dealix Trust Page** (value exchange).
- Anonymized case study published.
- Talking point: "Your customers got faster help. Other founders need this story."

## CSM Motion (Day 14 onwards)

| Day | Action | Owner |
|---|---|---|
| Day 14 | Final delivery + handoff signed | DL |
| Day 16 | CSM reviews proof pack | CSM |
| Day 18 | Recommendation embedded in executive output Section 8 | CSM + DL |
| Day 21 | CSM emails sponsor + meeting link | CSM |
| Day 30 | Day-30 review meeting (if scheduled) | CSM + DL |
| Day 45 | Follow-up if no conversion | CSM |
| Day 60 | Re-categorize as nurture if still no conversion | CSM |

## Conversion Targets
- **Sprint → Monthly Support AI** within 60 days: ≥ 40%.
- **Sprint → Feedback Intelligence** within 90 days: ≥ 15%.
- **Any conversion** within 6 months: ≥ 55%.

## Anti-Patterns
- Selling Monthly Support AI without category-validation signal.
- Pitching Feedback Intelligence before basic categorization is stable.
- Discounting the retainer below floor.
- Promising sentiment-based commercial decisions.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proof pack + insights report | Recommendation | CSM | Day 16 |
| Executive output Section 8 | Sponsor CTA | CSM + DL | Day 18 |
| CRM | Conversion tracking | CSM | Weekly |

## Metrics
- **60-day conversion** — Target ≥ 40%.
- **Average upsell size** — Target ≥ SAR 22,000 (mo-equivalent).
- **First follow-up time** — Target ≤ 3 days.

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CSM baseline
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/HIRING_CSM_FIRST.md` — CSM hiring rationale
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
