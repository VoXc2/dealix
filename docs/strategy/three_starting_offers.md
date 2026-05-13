---
title: Dealix Three Starting Offers — Productized Entry Points
doc_id: W6.T35.starting-offers
owner: CRO
status: approved
last_reviewed: 2026-05-13
audience: [customer, partner, internal]
language: en
ar_companion: docs/strategy/three_starting_offers.ar.md
related: [W0.T00, W6.T32, W6.T33, W6.T34, W1.T31]
kpi:
  metric: starting_offer_customers_closed
  target: 25
  window: 90d
rice:
  reach: 500
  impact: 3
  confidence: 0.9
  effort: 2
  score: 675
---

# Dealix Three Starting Offers

## 1. Context

Dealix has 30+ catalog services across 5 customer pillars. To accelerate first revenue and prove repeatability per pillar, we open with **three productized starting offers**. Every prospect lands on one of these three; nothing custom in the first conversation.

The three offers are intentionally spread across pillars (Grow / Automate / Brain) to test which pillar pulls the strongest in early market response. Outputs are fixed; prices are SAR-anchored; durations are bounded.

## 2. Audience

- **Customer**: choose one of three entry points.
- **Sales**: first-meeting positioning script — no bespoke quotes in conversation 1.
- **CS / Delivery**: fixed scope keeps margins healthy.

## 3. The three offers

### 3.1 Offer 1 — Revenue Intelligence Sprint

- **Price**: SAR 9,500 (single payment, 10-day delivery).
- **Pillar**: Grow Revenue.
- **Promise**: "We turn your messy data into clear sales opportunities."
- **Scope (fixed)**:
  - Ingest up to 5,000 records (CRM export, spreadsheet, or seed list).
  - Data cleanup + dedupe + Saudi entity normalization.
  - Scoring against your ICP (we co-define ICP if missing in day 1).
  - Top 50 ranked accounts + top 10 prioritized actions.
  - Outreach drafts (AR + EN) for the top 10.
  - Mini CRM board (Trello-style) with stages.
  - 60-min handoff session.
- **Outputs delivered**: dataset, scoring report, outreach drafts, mini-CRM, recorded handoff.
- **Best fit**: B2B sales teams with messy data and unclear priorities.
- **Modules used**: Data Quality + Scoring + Outreach + Reporting + Governance.
- **Upsell path**: Sales Pipeline Setup (8K–25K) → Monthly RevOps Retainer (15K–60K/mo) → Saudi Lead Engine (Growth tier).

### 3.2 Offer 2 — AI Quick Win Sprint

- **Price**: SAR 12,000 (single payment, 7-day delivery).
- **Pillar**: Automate Operations.
- **Promise**: "We pick one painful recurring process and automate it in a week."
- **Scope (fixed)**:
  - 30-min discovery call — pick ONE use case from a pre-curated list (executive weekly report / lead routing / ticket triage / proposal generator / inbox summarization).
  - Build the automation.
  - 2 rounds of customer feedback within the week.
  - Approval workflow + audit log baked in.
  - Documentation + 1-hour training session.
- **Outputs delivered**: live automation, runbook, training recording, ROI baseline.
- **Best fit**: operations leaders frustrated by recurring manual work.
- **Modules used**: Workflow + Reporting + Governance (+ Knowledge if RAG-based).
- **Upsell path**: SOP Automation (15K–60K) → Monthly AI Ops Retainer (15K–60K/mo) → Enterprise AI OS.

### 3.3 Offer 3 — Company Brain Sprint

- **Price**: SAR 20,000 (single payment, 21-day delivery).
- **Pillar**: Build Company Brain.
- **Promise**: "We turn your files into an internal assistant with cited answers."
- **Scope (fixed)**:
  - Ingest up to 500 documents (PDFs, Docs, knowledge articles, policies).
  - PII detection + scrubbing for sensitive content.
  - RAG indexing with citation tracking.
  - Web/Slack/Teams query interface for one team (up to 20 seats).
  - Access rules (3 permission tiers).
  - Freshness tracking (auto-flag docs > 90 days).
  - 2-hour team training.
- **Outputs delivered**: live assistant, access matrix, doc inventory report, training recording.
- **Best fit**: teams with rich documents (sales, HR, support, ops) suffering from "where is that PDF" syndrome.
- **Modules used**: Knowledge + Governance + Reporting (+ Intake on day 1).
- **Upsell path**: Sales Knowledge Assistant (15K–60K) → Policy Assistant (20K–100K) → Enterprise Company Brain (per enterprise pricing).

## 4. Why these three?

- **Cross-pillar coverage**: tests demand in Grow / Automate / Brain simultaneously.
- **Fixed scope**: no scope creep; CS margins protected.
- **Compounding**: each sprint produces a customer dataset that feeds the next sprint (data quality scores, automation library, document index).
- **Price ladder**: 9.5K → 12K → 20K — friction-free entry, with the right "anchor" feel.
- **Saudi-fit**: all three deliver bilingual outputs, PDPL-compliant data handling, ZATCA-compliant invoicing.

## 5. KPIs

- 25 starting-offer customers closed in first 90 days (split: 12 Revenue / 8 Quick Win / 5 Company Brain).
- Conversion to Phase-2 retainer or upsell: ≥ 40% within 60 days post-sprint.
- Sprint margin: ≥ 55% (cost includes engineer + CS time + LLM costs).
- NPS at sprint close: ≥ 50.

## 6. Sales motion (mandatory)

1. **First meeting (30 min)**: discovery + map to one of three offers. Do not bespoke-quote.
2. **Decision (within 7 days)**: customer picks one offer (or none).
3. **Sprint kickoff**: signed SOW from the 3 fixed templates.
4. **Sprint close**: handoff + upsell conversation.
5. **Day 30 post-close**: retainer / next-sprint conversation.

Anti-pattern: never start with "what do you need?" — start with "which of three outcomes is most valuable to you right now?"

## 7. Dependencies

- W6.T33 portfolio catalog (these are the entry-points to the full catalog).
- W6.T34 OS modules (the three offers map to specific module compositions).
- W2.T03 pricing packages (these one-shot offers complement the SaaS tier structure).
- W5.T18 pilot framework (the SAR 60K paid pilot is the Enterprise version of these sprints).

## 8. Cross-links

- Positioning: `docs/strategy/dealix_operating_partner_positioning.md`
- Portfolio catalog: `docs/strategy/service_portfolio_catalog.md`
- OS modules: `docs/product/internal_os_modules.md`
- Pricing packages (SaaS): `docs/pricing/pricing_packages_sa.md`
- Pilot framework (Enterprise version): `docs/delivery/pilot_framework.md`

## 9. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: monthly during first 90 days; sunset/replace any offer with < 5 closes in 90 days.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial three starting offers: Revenue (9.5K), Quick Win (12K), Company Brain (20K) |
