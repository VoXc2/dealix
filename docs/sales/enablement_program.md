---
title: Sales Enablement Program — Saudi GTM 30/60/90 Ramp
doc_id: W2.T28.enablement
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T05, W1.T01, W1.T17, W1.T31, W2.T02, W2.T03, W2.T04, W2.T08, W2.T09, W2.T16, W3.T07, W3.T20]
kpi:
  metric: rep_ramp_time_to_first_sql
  target: 30d
  window: 90d
rice:
  reach: 20
  impact: 2
  confidence: 0.9
  effort: 1
  score: 36
---

# Sales Enablement Program — Saudi GTM 30/60/90 Ramp

## 1. Context

Dealix's Saudi GTM thesis depends on a small number of reps (6–10 in year one) hitting Tier-1 enterprise quota in three priority verticals. Generic "new-hire training" is not enough: reps must be certified bilingual, fluent in PDPL/SAMA framing, capable of running the ROI model live, and able to multi-thread a 7-persona buying committee. This document defines the program — onboarding, certification (3 levels), role-play cadence, win-story library, objection bank, and bilingual asset gating — and links every component to its source artifact so the program does not drift from the rest of the W2 commit.

## 2. Audience

CRO, Head of Sales, sales managers, the rep cohort, and Sales Ops. Internal only — never shared with customers or partners. (Partner enablement is a separate document under T6 partner program.)

## 3. Decisions / Content

### 3.1 The 30/60/90 ramp

**Day 0 — preboarding (before first day).**
- Reading list mailed: T5 ICP, T1 verticals, T17 competitive landscape, T9 Arabic playbook (links below in section 6).
- Tooling provisioned: CRM, Decision Passport sandbox, Lead Engine sandbox, recording tool, deck library.
- Sponsor manager assigned + buddy AE assigned.

**Day 1–30 — Foundations (Certification Level 1: "Conversationally fluent").**
- Week 1: product + verticals. Live walkthrough of `docs/product/saudi_lead_engine.md`; verticals tour from `docs/go-to-market/saudi_vertical_positioning.md`.
- Week 2: ICP + persona matrix. Memorize Tier 1/2/3 cutoffs, the 7-persona × 3-vertical cells they will see.
- Week 3: ROI model. Run the BFSI worked example from `docs/sales/roi_model_saudi.md` end-to-end three times with a manager; reach < 5% deviation from reference.
- Week 4: certification exam (Level 1). Pass criteria: 80% on written, 7/10 on role-play, ROI model run live in 25 min with no manager assistance.
- **Exit KPI**: first SQL handed off to AE (if BDR) or first qualified discovery booked (if AE) within 30 days of start.

**Day 31–60 — Application (Certification Level 2: "Deal-ready").**
- Week 5–6: shadow 4 live discovery calls (1 per vertical + 1 unfamiliar). Submit notes scored by manager.
- Week 7: lead 2 live discovery calls under manager observation. Use the 10-question discovery list from `docs/SALES_PLAYBOOK.ar.md`.
- Week 8: run a full ROI deck (`docs/sales/roi_deck_outline.md`) in role-play with the CRO playing CFO. Pass = "deck would survive a Saudi CFO on first viewing."
- **Exit KPI**: at least one opportunity > SAR 100K with ROI calc attached and persona matrix complete on stage advance.

**Day 61–90 — Independence (Certification Level 3: "Quota-bearing").**
- Week 9–10: own 1 deal end-to-end from discovery to verbal commitment under manager observation.
- Week 11: bilingual demo certification — deliver the demo from `docs/SALES_PLAYBOOK.ar.md` section 2 in Arabic and in English in the same week, recorded.
- Week 12: live procurement-objection drill with HoLegal playing DPO and CFO. Pass = "answers PDPL Art. 13/14, cross-border transfer, and data residency without a slide."
- **Exit KPI**: rep promoted to full quota; rep accepted to lead deals > SAR 500K with co-pilot from CRO only as escalation.

### 3.2 The three certification levels

| Level | Name | Test | Privileges | Re-test cadence |
|-------|------|------|-----------|-----------------|
| L1 | Conversationally fluent | Written + ROI run + 1 role-play | May run discovery calls, may not run ROI deck without manager | annual |
| L2 | Deal-ready | Live discovery + ROI deck role-play | May run any deal ≤ SAR 500K solo; > SAR 500K with manager | annual |
| L3 | Quota-bearing | Bilingual demo + procurement drill | Full quota; may lead any deal; named coach for L1/L2 cohort | every 18 months or after 3 lost deals > SAR 500K |

Certifications are reverse-revocable: any rep who fails twice in a row to attach the ROI calc on > SAR 100K opps demotes one level until re-certified.

### 3.3 Monthly role-play cadence (post-ramp)

- **First Monday of each month**: 90-minute role-play session. Two reps run a live scenario (rotating: discovery, ROI deck, procurement drill, hostile competitor swap, AR-only demo). All other reps grade against a public rubric.
- **Third Monday**: win-story exchange. Each rep brings one closed-won and one closed-lost from the prior 4 weeks; manager extracts the lesson into the win-story library (3.5).
- Recordings stored in `sales/role_plays/yyyy_mm/` (folder created under T20 bilingual asset index when it lands).

### 3.4 Win-story library — structure

Every closed-won opportunity > SAR 100K must be written up within 14 days of close into a standard 1-page format:

- **Header**: vertical, deal size, cycle length, buying committee size, primary competitor displaced.
- **The trigger**: which buying trigger from `docs/go-to-market/icp_saudi.md` section 3.4 fired.
- **The unlocking moment**: one paragraph on the specific Dealix capability or evidence that turned the deal.
- **The ROI numbers**: the three scenarios as actually presented; the one the CFO defended.
- **The objection map**: stated objections per persona and the counter that worked.
- **The handoff**: how CS picked up from sales, with link to handoff doc (T10 once it lands).

Library lives at `docs/sales/win_stories/<vertical>/<account_codename>.md`. Stories are gated by persona — never share full details with partners until customer permission is on file.

### 3.5 Objection bank — linkage to T17 competitive

The objection bank is **not** a separate artifact — it is the union of:
- T17 competitive landscape (`docs/strategy/competitive_landscape_sa.md`) section 3.1 competitor counter-positions.
- T8 persona matrix (`docs/sales/persona_value_matrix.md`) section 3.3 per-persona top objections.
- The "stated_objection" CRM custom field, refreshed monthly into the matrix.

Reps are trained to look these up live during a call (acceptable; we are not testing memory) — but must close the loop by updating the CRM field within 24h of the call so the bank stays current.

### 3.6 Bilingual asset gating

Every asset shared with a Saudi customer is gated by language preference:
- **AR preference (recorded in contact's `preferred_language` field)**: rep sends the AR variant first; EN follows only if requested.
- **EN preference**: EN first; AR companion linked at footer.
- **Mixed committee**: both at the same time, never weeks apart (per T20 bilingual freshness KPI — AR within 14 days of EN).

Rep is responsible for verifying that an AR companion exists before sending an EN-only doc to a Saudi customer. If no AR companion exists, escalate to Marketing for production within 5 business days; for highly compressed deals, escalate to CRO for an inline translation memo.

### 3.7 Compensation and incentive alignment

- L1 reps: salary only, no quota.
- L2 reps: 70/30 (salary/variable), quota SAR 1.5M ARR annual.
- L3 reps: 60/40, quota SAR 3M ARR annual; SPIFFs on:
  - First logo per vertical (SAR 20K).
  - Win against a named US-stack competitor (SAR 15K) per T17.
  - Customer-permission for case study (SAR 10K).
- Clawback: 50% of variable on any deal where ROI calc was not attached (enforces T2 KPI).

### 3.8 Tooling and content stack

- **Knowledge base**: this docs tree. The W2 commit is the source of truth — slide libraries reference back to these markdown docs.
- **Recording / coaching**: Gong or Chorus (decision deferred to W3 launch).
- **Practice sandbox**: Lead Engine sandbox seeded with anonymized real-account data; AE practices without touching live CRM.
- **Deck builder**: AE composes from a frozen template per `docs/sales/roi_deck_outline.md`; no off-template decks shared with customers.

### 3.9 What this program does NOT replace

- It does not replace AE judgment in a live call; the matrices and decks are scaffolding, not scripts.
- It does not replace CS handoff training (T10) or expansion training (T19).
- It does not replace partner enablement (T6).
- It does not replace ethics or trust training (covered separately in `docs/DEALIX_OPERATING_CONSTITUTION.md`).

### 3.10 Quality and dropout rules

- Any rep who fails L1 twice exits the program; the bar exists to protect the brand.
- Any rep flagged for non-compliance (PDPL, hostile-tone, off-message claims) by the CRO or HoLegal is removed from the deal immediately and re-routed to remediation. Two flags within a quarter is termination.

## 4. KPIs

- Rep ramp time to first SQL: < 30 days.
- L2 certification by day 60: 80% of cohort.
- L3 certification by day 90: 60% of cohort.
- ROI-calc attach rate by reps off ramp: ≥ 95%.
- Persona-matrix completeness on > SAR 200K opps: 100%.

## 5. Dependencies

- T5 ICP — discovery and qualification baseline.
- T1 verticals — vertical-specific drill content.
- T2 ROI model — primary certification artifact.
- T8 persona matrix — multi-thread training spine.
- T9 AR sales playbook — bilingual demo source.
- T16 value metrics — used in expansion drills.
- T17 competitive — objection-bank source.
- T7 trust pack (lands W3) — procurement-drill source.
- T20 bilingual asset index (lands W3) — gating mechanism.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ROI model: `docs/sales/roi_model_saudi.md`
- ROI deck: `docs/sales/roi_deck_outline.md`
- Persona matrix: `docs/sales/persona_value_matrix.md`
- AR playbook: `docs/SALES_PLAYBOOK.ar.md`
- Competitive: `docs/strategy/competitive_landscape_sa.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Verticals: `docs/go-to-market/saudi_vertical_positioning.md`
- Trust pack (existing): `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`

## 7. Owner & Review Cadence

- **Owner**: CRO. Head of Sales is operating co-owner; HoLegal owns the procurement-drill module.
- **Review**: monthly cohort review; quarterly program-level review with CEO; certification curriculum re-baselined every 6 months against win/loss data (T17).

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial 30/60/90 program with 3-level certification, monthly role-play cadence, win-story structure, bilingual gating |
