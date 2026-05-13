# Offer — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Revenue Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
This file defines the public-facing promise of the **Lead Intelligence Sprint**, the entry-tier revenue service in the Dealix service ladder. It removes the ambiguity buyers currently face when comparing Dealix to consultants who promise "leads" but never define the deliverable. The offer plugs into the operating layers via `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` (entry-tier monetization) and `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` (sprint-to-retainer ladder). Every word here is auditable against the proof pack template and the quality standard.

## Promise
> Turn your scattered B2B opportunities into a **ranked, actionable pipeline** within **10 business days** — with a draft outreach pack your team can send the same week.

The Sprint replaces guesswork with a structured, scored, source-cited account list and gives the sales owner an immediate next action for each of the top ten accounts.

## The Problem We Solve
- Sales teams sit on thousands of half-cleaned rows in Excel, HubSpot exports, event lists, and old CRM snapshots.
- Nobody knows which 10 accounts to call this week, and why.
- Outreach drafts are inconsistent across reps, with no Arabic/English tone control.
- There is no proof report executives can show the board.

The Sprint compresses this from a 6-week internal project into a 10-day external delivery with a signed proof pack.

## Deliverables
1. **Cleaned account list** — deduped, normalized, source-tagged. Every row has either a known source or a `source_missing` flag.
2. **Dedupe report** — counts of duplicates removed, merge rules applied, residual ambiguity flagged.
3. **Top 50 ranked accounts** — scored on fit, intent signals, recency, and reachability. Each score includes a one-line explanation.
4. **Top 10 immediate actions** — named owner, recommended channel, suggested first touch, expected objection, fallback.
5. **Outreach draft pack** — 4 sequences (cold intro, warm follow-up, referral ask, re-engagement) in Arabic and English, all labeled `draft_only`.
6. **Mini CRM board** — Notion/Sheets board with stage definitions, ownership column, and weekly review cadence.
7. **Executive proof report** — baseline vs. after-Sprint state, with anonymizable metrics suitable for the trust page.

All deliverables are produced under Dealix `QUALITY_STANDARD_V1` and shipped with a signed `PROOF_PACK_TEMPLATE` instance.

## What's NOT Included
- **Automated sending** of any channel (email, SMS, WhatsApp). Drafts only.
- **Scraping** of LinkedIn, Google Maps, or any source without a written lawful basis.
- **Guaranteed meetings or signed deals.** We deliver the ranked pipeline and the drafts; conversion remains the client's responsibility.
- **Cold WhatsApp outreach drafts.** Dealix refuses these per `AI_INFORMATION_GOVERNANCE.md`.
- **LinkedIn automation** (Sales Navigator bots, connection sprayers, etc.).
- **CRM integration** beyond CSV import/export unless separately scoped (+SAR 6,000 minimum).
- **Paid ad spend or media buying.**
- **Long-term retainership** — this is a fixed-fee sprint. Continuation runs on the Monthly RevOps OS retainer.

## Buyer Profile
- B2B founder, head of sales, or RevOps lead in KSA/GCC.
- 100–10,000 historical accounts available in some structured form.
- Defined ICP (or willing to define one in the intake session).
- Sales team of 1–8 people who can act on the top 10 within a week of delivery.

## Why It Sells
- **Visible in 10 days** — short enough to fit a quarterly board cycle.
- **Proof-backed** — every claim shipped is testable against the proof pack.
- **Bilingual** — Arabic and English drafts, KSA tone, ZATCA-compatible invoicing.
- **Bridge to retainer** — every Sprint cleanly upsells into RevOps OS, Data OS, or AI Support Desk.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Account export (CSV/XLSX) | Cleaned list + scores | Client RevOps + Dealix Analyst | One-time, Day 1 |
| ICP definition | Scoring rubric | Client Head of Sales | Day 2 |
| Sample outreach + tone notes | Draft pack | Dealix Copy Lead | Day 5 |
| Stakeholder list | Top 10 action plan | Dealix Delivery Lead | Day 9 |
| Proof events captured during delivery | Proof pack + report | Dealix QA + Client Sponsor | Day 10 |

## Metrics
- **Sprint completion rate** — `% sprints delivered on or before Day 10`. Target ≥ 95%.
- **Top-10 action acceptance** — `% top-10 accounts accepted by client sales owner`. Target ≥ 80%.
- **Draft acceptance** — `% drafts client uses without rewrite`. Target ≥ 70%.
- **Upsell rate** — `% sprints that convert to a paid follow-on within 60 days`. Target ≥ 35%.
- **Proof pack completeness** — `% sprints with signed proof pack delivered`. Target = 100%.

## Related
- `docs/capabilities/revenue_capability.md` — the capability blueprint behind this service
- `docs/company/CAPABILITY_VALUE_MAP.md` — placement of the sprint in the capability map
- `docs/company/MARGIN_CONTROL.md` — pricing floor enforcement rules
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers used in `pricing.md`
- `docs/quality/QUALITY_STANDARD_V1.md` — quality gates the sprint must satisfy
- `docs/templates/PROOF_PACK_TEMPLATE.md` — the proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic position of the entry tier
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — sprint-to-retainer ladder
- `docs/COMPANY_SERVICE_LADDER.md` — neighbouring services on the ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — canonical pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
