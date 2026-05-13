# Upsell — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Customer Success Manager (CSM)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [upsell_AR.md](./upsell_AR.md)

## Context
The Sprint is designed as a **proof-bearing entry tier**, not a one-off transaction. This file maps every common proof signal observed during a Sprint to the most fitting next-tier offer. It implements the ladder logic in `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and `docs/COMPANY_SERVICE_LADDER.md`, and the strategic monetization path in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`. Without this file, every Sprint risks ending as a flat invoice; with it, every Sprint becomes a candidate for a 6–12 month retainer.

## Operating Principle
> The proof pack tells you what to upsell. Read the events; recommend the offer.

The CSM reviews the proof pack with the Delivery Lead on Day 10–12 and selects the next-step offer using the mapping below. The recommendation appears in Section 8 of the Executive Report.

## Proof → Next-Offer Mapping

### Proof: Top 50 list is high-fit and client is eager to act
**Signal**:
- `top_10_action_plan_complete = true`
- Client expressed verbal intent to act on top 10 within 1 week.
- Draft acceptance ≥ 70%.

**Recommended next offer**: **Pilot Conversion Sprint** (SAR 18,000–35,000).
- Take top 50 from Sprint, run a 4-week conversion sprint with weekly review.
- Deliverables: meeting bookings tracker, talk-track refinement, conversion proof pack.
- Talking point: "Your top 50 is the input. The Pilot Conversion Sprint turns it into booked meetings."

### Proof: Data quality is poor (high duplicate %, many `source_missing` flags)
**Signal**:
- `duplicates_removed / rows_imported > 15%`, OR
- `source_missing` rate > 30%, OR
- Sprint required > 2 days of manual cleaning.

**Recommended next offer**: **Monthly Data OS** (SAR 12,000–25,000/mo) or **Monthly RevOps OS** (SAR 18,000–40,000/mo).
- Continuous list maintenance, weekly enrichment, deduplication.
- Single source of truth for sales team.
- Talking point: "Your data drifts faster than you can clean it. Data OS keeps it sharp every week."

### Proof: Support themes detected in the lead notes / outreach replies
**Signal**:
- During Sprint, the team noticed clusters of support questions or recurring objections in the dataset.
- Client mentions inbox overload in intake or daily standups.

**Recommended next offer**: **AI Support Desk Sprint** (SAR 12,000–30,000).
- Categorize inbox, build suggested reply library, add escalation rules.
- Talking point: "Your sales team is answering support questions disguised as objections. Let's separate them and build a desk."

### Proof: Workflow gaps visible (manual re-typing, status checks, follow-up reminders)
**Signal**:
- Client mentioned 3+ manual workflows in intake.
- Reviewer feedback during Sprint touched on "this would be easier if…".

**Recommended next offer**: **AI Quick Win Sprint** (SAR 7,500–15,000).
- Pick one weekly workflow, save hours in 7 days.
- Talking point: "We saw at least 3 manual workflows you'd want back. Let's reclaim one."

### Proof: Knowledge gaps visible (team can't find policy answers, sales relies on tribal knowledge)
**Signal**:
- Client mentioned "we have no single source of truth for [policy / pricing / playbooks]".
- Sales team needed multiple Slack/WhatsApp queries to find answers during Sprint.

**Recommended next offer**: **Company Brain Sprint** (SAR 20,000–60,000).
- Source-cited internal assistant for 50–200 documents in 3–4 weeks.
- Talking point: "Your team is reinventing answers. The Brain gives them one source with citations."

### Proof: Multi-stakeholder / regulated environment / sensitive data
**Signal**:
- Sensitivity premium triggered.
- Stakeholder_count > 3.
- Client mentioned PDPL, ZATCA, healthcare regs, or government tenders.

**Recommended next offer**: **AI Governance Program** (SAR 35,000–150,000).
- 4–12 week program: governance OS, approval workflows, audit, risk register, controls matrix.
- Talking point: "Your environment needs a governance layer before any AI scales. Let's build it once."

### Proof: Strong proof pack + publication consent
**Signal**:
- Client signs publication consent.
- Proof pack contains a clean, anonymizable win.

**Recommended next offer**: **Co-marketing slot on the Dealix Trust Page** (no cost, value exchange).
- Anonymized case study published, with mutual logo placement subject to consent.
- Talking point: "Your win is a story other founders need. With your consent, we co-publish."

## CSM Motion (Day 10–14)

| Day | Action | Owner |
|---|---|---|
| Day 10 | Final delivery + handoff signed | DL |
| Day 11 | CSM reviews proof pack, drafts recommendation | CSM |
| Day 12 | Recommendation embedded into Executive Report Section 8 | CSM + DL |
| Day 13 | CSM emails sponsor with recommendation + meeting link | CSM |
| Day 14 | If no response, CSM follows up; logs in CRM | CSM |
| Day 30 | Final follow-up if not converted | CSM |
| Day 60 | Recategorize as "nurture" if still no conversion | CSM |

## Conversion Targets
- **Sprint → Pilot Conversion Sprint**: target ≥ 25% within 60 days.
- **Sprint → Monthly Retainer (any)**: target ≥ 35% within 90 days.
- **Sprint → Higher-Tier Sprint (any)**: target ≥ 50% within 6 months.

## Anti-Patterns (Don't Do This)
- Pitching an offer the proof pack does not justify.
- Upselling without anonymization consent and then anonymizing post-hoc.
- Discounting the retainer below floor to win conversion.
- Promising outcomes that depend on data the client has not provided.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proof pack | Upsell recommendation | CSM | Day 11 |
| Executive Report Section 8 | Sponsor-facing CTA | CSM + DL | Day 12 |
| CRM record | Conversion tracking | CSM | Weekly |
| 60/90-day review | Re-categorization | CSM | Monthly |

## Metrics
- **60-day upsell conversion** — `% sprints converted within 60 days`. Target ≥ 35%.
- **Average upsell size** — `mean SAR value of next-tier offer sold`. Target ≥ SAR 18,000.
- **Time to first follow-up** — `days from Day 10 to first CSM email`. Target ≤ 3.

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CSM motion baseline
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/capabilities/revenue_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/HIRING_CSM_FIRST.md` — CSM hiring rationale
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
