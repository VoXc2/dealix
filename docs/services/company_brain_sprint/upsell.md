# Upsell — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Customer Success Manager
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [upsell_AR.md](./upsell_AR.md)

## Context
Every Company Brain Sprint creates a knowledge graph that decays daily without maintenance. The upsell motion is therefore primarily a continuation motion. This file maps proof signals to next-tier offers, implementing the ladder logic in `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and `docs/COMPANY_SERVICE_LADDER.md`.

## Operating Principle
> A live Brain that nobody maintains becomes a misleading Brain. The upsell is the maintenance contract.

## Proof → Next-Offer Mapping

### Proof: Documents will need weekly updates
**Signal**:
- Client mentioned policies change ≥ monthly.
- Knowledge owner cannot allocate ≥ 8h/month to maintenance.
- `freshness_flags_raised` > 0 during the Sprint.

**Recommended next offer**: **Monthly Brain Management** (SAR 12,000–30,000/mo).
- Continuous ingestion, freshness checks, retrieval tuning, governance log review.
- Talking point: "Your Brain is a living system. We keep it sharp every week so it never lies."

### Proof: Sales team is heaviest user
**Signal**:
- Sales group asked the most test questions.
- Sales sponsor mentioned answer-consistency pain across reps.
- Outreach references became more accurate during the Sprint.

**Recommended next offer**: **Sales Knowledge Assistant** (SAR 25,000–55,000 build + retainer).
- Branded slim assistant for sales reps with curated playbook + objection-handling content.
- Integrates with the main Brain but with sales-focused prompts.
- Talking point: "Your reps are answering the same buyer questions 50 times a week. Give them a Brain that speaks their language."

### Proof: Policy team is heaviest user
**Signal**:
- Policy group asked the most precise questions.
- Audit log shows the highest insufficient-evidence rate in policy questions.
- Sponsor mentioned regulatory pressure.

**Recommended next offer**: **Policy Assistant** (SAR 25,000–55,000 build + retainer).
- Curated assistant on policies, with versioning and "what changed since X" capability.
- Talking point: "Your policy work is changing faster than your team can read. Give them a Policy Brain."

### Proof: Cross-team interest emerged
**Signal**:
- During the Sprint, additional groups requested access.
- Sponsor mentioned other departments.

**Recommended next offer**: **Group Expansion Sprint** (incremental fee per added group).
- Add 1–2 user groups with their own access scopes.
- Talking point: "More groups want in. Let's add them with proper access boundaries."

### Proof: Knowledge gaps revealed
**Signal**:
- Coverage map showed several thin areas.
- Insufficient-evidence rate concentrated in specific topics.

**Recommended next offer**: **Knowledge Acquisition Sprint** (SAR 15,000–30,000).
- Hunt down, normalize, and ingest the missing documents.
- Talking point: "Your Brain has known gaps. Let's close the top 3."

### Proof: Sensitive-data process exposed
**Signal**:
- Sensitivity premium triggered.
- Several sensitivity tags applied.

**Recommended next offer**: **AI Governance Program** (SAR 35,000–150,000).
- Full governance OS, approval matrix, audit, risk register.
- Talking point: "You handled the Brain well. The next step is governing AI usage across the company."

### Proof: Strong proof pack + publication consent
**Signal**:
- Hallucinated citations = 0.
- Strong coverage and insufficient-evidence discipline.
- Client agrees to publication.

**Recommended next offer**: **Co-marketing case study slot** on the Dealix Trust Page (value exchange).
- Talking point: "Your Brain is a publishable proof of governance. With your consent, we co-publish."

## CSM Motion

| Week / Day | Action | Owner |
|---|---|---|
| Week 4, end | Final delivery + handoff signed | DL |
| Week 4 + 2 | CSM reviews proof pack + sends recommendation | CSM |
| Week 4 + 4 | Sponsor meeting on next step | CSM + DL |
| Week 4 + 7 | Decision logged in CRM | CSM |
| Day 60 | Final follow-up if not converted | CSM |

## Conversion Targets
- **Sprint → Monthly Brain Management** within 60 days: ≥ 40%.
- **Sprint → Group-specific assistant** within 90 days: ≥ 20%.
- **Any conversion** within 6 months: ≥ 55%.

## Anti-Patterns
- Selling Monthly Brain Management without freshness signals.
- Promising a "live and accurate" Brain without maintenance.
- Pitching Group Assistant before the original Brain is stable.
- Discounting the retainer below floor.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proof pack + coverage map | Recommendation | CSM | Week 4 + 2 |
| Executive output Section 8 | Sponsor CTA | CSM + DL | Week 4 + 2 |
| CRM | Conversion tracking | CSM | Weekly |

## Metrics
- **60-day conversion** — Target ≥ 40%.
- **Average upsell size** — Target ≥ SAR 18,000 (mo-equivalent).
- **First follow-up time** — Target ≤ 3 days.

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CSM baseline
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance regime
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/HIRING_CSM_FIRST.md` — CSM hiring rationale
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
