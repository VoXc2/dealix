---
title: ROI Deck Outline — 10-Slide Saudi Enterprise Deck
doc_id: W2.T02.roi-deck
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, internal]
language: en
ar_companion: docs/sales/roi_deck_outline.ar.md
related: [W0.T00, W1.T05, W1.T01, W1.T17, W1.T31, W2.T02, W2.T03, W2.T04, W2.T08, W2.T28]
kpi:
  metric: roi_deck_attach_rate_on_late_stage_opps
  target: 100%
  window: 60d
rice:
  reach: 200
  impact: 2
  confidence: 0.8
  effort: 1
  score: 320
---

# ROI Deck Outline — 10-Slide Saudi Enterprise Deck

## 1. Context

The ROI model (`docs/sales/roi_model_saudi.md`) defines the math; this document defines the **narrative wrapper** — the 10-slide deck a Dealix AE uses to walk a Saudi enterprise buying committee from problem to commitment in a single 45-minute meeting. The deck is the artifact procurement scans and the CFO defends to the board. It is purposely short, numbers-first, and bilingual-ready: each EN slide has an AR companion slide at the same index in the Arabic deck.

## 2. Audience

- **Customer**: late-stage buying committee — CFO, CRO/CCO, CIO/CTO, DPO, Procurement.
- **Partner**: SI / channel partners running joint deals.
- **Internal**: AEs use this as a teleprompter; CRO reviews any deviation > 1 slide.

## 3. Decisions / Content

### 3.1 Slide-by-slide map

**Slide 1 — Title and meeting frame.**
- Title: "Dealix × [Customer]: Saudi Revenue OS Business Case".
- Subtitle: "[Date] · Prepared for [CFO + CRO names]".
- Visual: customer logo + Dealix logo, single SAR-headline tagline ("Net SAR X.YM in 12 months, payback under 4 months").
- Talk track: 60 seconds — state the meeting goal (decision today on pilot scope), the artifact (this deck plus the model spreadsheet), and the success criterion (CFO can defend the number internally).

**Slide 2 — The problem in their words.**
- Three bullets quoting back the buyer's own discovery answers: pain on pipeline coverage, pain on cycle length, pain on BDR research time.
- Numbers from discovery: current win rate, current cycle, current data spend.
- Visual: a clean SAR-denominated cost-of-status-quo number — calculated live in discovery, frozen here.
- Talk track: "These are your numbers, not ours. We are not selling against generic pain — we are pricing exactly this gap."

**Slide 3 — Saudi market context.**
- Vision 2030 budget, BFSI digital licensing, ZATCA Phase 2, NUPCO procurement, PDPL enforcement.
- One stat per relevant vertical from `docs/go-to-market/saudi_vertical_positioning.md`.
- Visual: timeline 2025–2027 with regulatory milestones the customer must satisfy.
- Talk track: "The gap is widening, not narrowing. Every quarter without a Saudi-native revenue engine increases your CAC and your audit risk."

**Slide 4 — Status-quo cost (today, no change).**
- The CS_labor + CS_data + CS_compliance numbers from the ROI model, summed.
- Plus opportunity cost: "deals lost to slow cycle = X SAR/year" — computed from `(cycle_today − cycle_industry_median) × pipeline × win_rate`.
- Visual: stacked SAR bar showing the four cost buckets.
- Talk track: "Doing nothing is not zero cost — it is SAR Y million per year that the CFO is already paying."

**Slide 5 — How Dealix changes the math.**
- Two-pillar visual: Saudi Lead Engine (left) + Decision Passport (right).
- Lead Engine: 25+ Saudi sources, seed → enriched → ranked, PDPL Art. 5 lawful basis, bilingual entity resolution.
- Decision Passport: every outreach action carries L0–L5 evidence, DPO-readable audit trail, blocks non-compliant sends at policy gate.
- Visual: arrow from "seed" through enrichment to "ranked-A lead with passport".
- Talk track: "Two products. One replaces three data vendors. The other replaces three compliance reviewers. Together they compress your sales cycle."

**Slide 6 — The ROI math (conservative / mid / optimistic).**
- The three-scenario table from `docs/sales/roi_model_saudi.md` section 3.5.
- Customer-specific numbers populated from discovery — never generic.
- Visual: three bars (Net ROI SAR, ROI %, Payback months) side-by-side per scenario.
- Talk track: "Conservative is the worst credible case. If conservative doesn't defend itself to your CFO, we will not ask for the order today."

**Slide 7 — Peer logo proof.**
- 3 anchor logos per relevant vertical (BFSI / Retail / Healthcare).
- Per logo: one outcome sentence ("Bank A: +52% qualified pipeline in 90 days, audit-clean on SAMA cycle 1").
- Visual: logo grid with one-line metric beneath each.
- Talk track: "These are Saudi customers operating under the same PDPL, same procurement constraints, same bilingual reality. Their CFO defended a number very close to yours."

**Slide 8 — Deployment plan (the path from yes to value).**
- Day 0: Order form + DPA signed.
- Days 1–14: Provisioning, source connection, persona import.
- Days 15–30: First 100 enriched leads delivered, AE training, Decision Passport calibrated to DPO.
- Days 31–60: First ranked-A cohort in CRM, KPI dashboard live, first revenue attribution measured.
- Days 60–90: Expansion review per `docs/customer-success/expansion_playbook.md` (when it lands).
- Visual: 4-stage horizontal Gantt.
- Talk track: "We are accountable to the CFO at day 60 for the first measurable ROI checkpoint."

**Slide 9 — Pricing teaser (not a quote).**
- Refer to `docs/pricing/pricing_packages_sa.md`: which tier we propose, why this tier, what is included, what is add-on.
- The annual-prepay SAR figure as a single number — no per-seat breakdowns, no add-on noise.
- Visual: one box "Recommended: Enterprise — SAR X / year, annual prepay".
- Talk track: "This is a recommendation, not a quote. The quote follows the procurement form per your standard. The number is consistent with the conservative ROI on slide 6."

**Slide 10 — Next steps.**
- Three bullets, each with a name and a date:
  1. CFO defends number internally by [date + 7 days].
  2. Procurement form issued by [date + 14 days].
  3. Order form + DPA signed by [date + 30 days].
- Visual: simple owner/date table.
- Talk track: "We do not leave this meeting without one of these dates committed. If you cannot commit, tell us what is blocking — we either fix it now or we walk away."

### 3.2 Bilingual and accessibility rules

- Every slide has an AR mirror in the Arabic deck — same index, same chart, AR-localized copy.
- SAR numbers always written with thousand separators (e.g., 1,023,000) and never abbreviated to "K"/"M" without spelling out at first occurrence.
- Charts are colorblind-safe, no decorative gradients, no animation.
- Deck is exported as PDF for procurement (no .pptx in customer hands).

### 3.3 Owner-of-each-slide

| Slide | Authoring AE | Reviewer |
|-------|--------------|----------|
| 1 | AE | Manager |
| 2 | AE (uses discovery notes) | CRO if deal > SAR 500K |
| 3 | Marketing-supplied template | Marketing |
| 4 | AE (model output) | CRO |
| 5 | Marketing-supplied template | Product |
| 6 | AE (model output) | CRO |
| 7 | Marketing-supplied logo bank | Marketing |
| 8 | Solutions Engineer / CS | HoCS |
| 9 | AE | CRO if deal > SAR 500K |
| 10 | AE | Manager |

### 3.4 What is explicitly NOT in this deck

- No product UI screenshots beyond slide 5 (this is a business-case deck, not a feature tour).
- No future roadmap (use `docs/product/revenue_weighted_roadmap.md` separately if asked).
- No competitor logos (counter-positioning lives in objection handling, not in print).
- No testimonials without written customer permission (per `docs/BRAND_PRESS_KIT.md` standards).

### 3.5 Anchor logos to cite (slide 7)

Subject to permission and refreshed quarterly. Default citation set at launch:
- BFSI: 1 SAMA-licensed bank (case anonymized as "Top-5 SAMA bank") + 1 fintech.
- Retail: 1 top-10 retail chain + 1 Salla/Zid platform-level customer.
- Healthcare: 1 cluster + 1 medtech distributor.

If permission is not yet secured, slide 7 cites the vertical-aggregate number ("3 BFSI customers averaging +47% qualified pipeline") with a footnote pointing to `docs/ROI_PROOF_PACK.md`.

## 4. KPIs

- Deck attached to 100% of late-stage opportunities (> SAR 100K) within 60 days.
- Time-to-close on opps with deck shown ≤ 60% of time-to-close on opps without (measured at quarterly review).
- Procurement objection rate on "business case not defensible" ≤ 10%.

## 5. Dependencies

- T2 ROI model (`docs/sales/roi_model_saudi.md`) — supplies the numbers on slides 4 and 6.
- T3 pricing (`docs/pricing/pricing_packages_sa.md`) — supplies slide 9.
- T17 competitive landscape (`docs/strategy/competitive_landscape_sa.md`) — supplies objection prep, not slides.
- T7 trust pack (lands W3) — supplies the DPA referenced in slide 10.
- T28 enablement (`docs/sales/enablement_program.md`) — reps certified on this deck before they may present.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- AR companion: `docs/sales/roi_deck_outline.ar.md`
- ROI model: `docs/sales/roi_model_saudi.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Persona-value matrix: `docs/sales/persona_value_matrix.md`

## 7. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: monthly with sales leadership; logo bank refreshed quarterly; full re-template every 6 months.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial 10-slide outline with owner map and exclusion rules |
