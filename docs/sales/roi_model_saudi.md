---
title: Saudi ROI Model — BFSI / Retail / Healthcare
doc_id: W2.T02.roi-model
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, internal]
language: en
ar_companion: docs/sales/roi_model_saudi.ar.md
related: [W0.T00, W1.T05, W1.T01, W1.T31, W2.T03, W2.T04, W2.T08, W2.T16, W2.T28]
kpi:
  metric: roi_calc_attach_rate_on_opps_above_100k
  target: 100%
  window: 60d
rice:
  reach: 200
  impact: 2
  confidence: 0.8
  effort: 1
  score: 320
---

# Saudi ROI Model — BFSI / Retail / Healthcare

## 1. Context

Saudi enterprise procurement teams do not approve software based on demos — they approve based on a defensible business case denominated in SAR with a CFO-readable bridge from current-state cost to future-state cost. Existing Dealix ROI material (`docs/ROI_PROOF_PACK.md`, scattered pitch slides) is in USD, generic, and not procurement-grade. This document is the canonical Saudi ROI model: the formula, the scenarios (conservative / mid / optimistic), the inputs collected during discovery, and a fully worked BFSI example a rep can paste into a proposal.

Owner is CRO. The model is attached to every opportunity above SAR 100K within 60 days of opportunity creation; that is the operational KPI for this artifact.

## 2. Audience

- **Customer**: CFO, CRO, procurement — defensible ROI bridge.
- **Partner / SI**: shared with co-selling partners to use in joint deals.
- **Internal**: AEs run the model in discovery; CRO reviews every >SAR 500K calculation.

## 3. Decisions / Content

### 3.1 The formula

```
Net ROI (SAR/year) = (Cost Savings + Revenue Uplift) - Dealix Cost
ROI %              = Net ROI / Dealix Cost × 100
Payback (months)   = (Dealix Cost / 12) ÷ (Monthly Cost Savings + Monthly Revenue Uplift)
```

All inputs are denominated in SAR, exclude VAT for like-for-like comparison, and assume 12-month horizon unless stated.

### 3.2 Cost Savings (CS) — three buckets

1. **BDR research & list-build labor avoided.**
   - Inputs: `# BDRs`, `% time on research today` (default 60%), `loaded annual cost per BDR` (default SAR 180K).
   - Formula: `CS_labor = BDRs × loaded_cost × research_pct × Dealix_automation_pct` (Dealix automates 50–80% of research; default 65%).

2. **Lead-list / data-vendor spend avoided.**
   - Inputs: `current annual spend on Apollo / ZoomInfo / agencies / one-off lists`.
   - Formula: `CS_data = current_data_spend × 0.7` (Dealix replaces 70% of fragmented data spend conservatively).

3. **Procurement / compliance overhead avoided.**
   - Inputs: `hours spent per PDPL/DPO review per outbound campaign × campaigns per year × loaded hourly rate`.
   - Formula: `CS_compliance = campaigns × review_hours × hourly_rate × 0.6` (Decision Passport reduces review prep by 60%).

### 3.3 Revenue Uplift (RU) — two levers

1. **Pipeline expansion → more closed-won.**
   - Inputs: `# AEs`, `avg deal size (SAR)`, `current win rate`, `current cycle length (days)`, `% increase in qualified pipeline from Dealix` (default 50% conservative, 100% mid, 150% optimistic).
   - Formula: `RU_pipeline = AEs × current_deals_per_year × pipeline_lift × win_rate × avg_deal_size`.

2. **Cycle compression → faster cash, more deals per AE-year.**
   - Inputs: `cycle reduction %` (default 20% conservative, 30% mid, 40% optimistic from Decision Passport pre-positioned evidence).
   - Formula: `RU_cycle = AEs × incremental_deals_from_shorter_cycle × win_rate × avg_deal_size`.

### 3.4 Dealix Cost

Direct list-price from `docs/pricing/pricing_packages_sa.md`. Use annual-prepay rate (15% discount) for ROI calc. Include realistic add-ons (premium source pack, custom connector if needed). Exclude one-time onboarding from year-1 ROI unless customer insists (then amortize over 3 years).

### 3.5 The three scenarios

Every ROI calc must show **three scenarios** side-by-side. Conservative is the "worst credible case" the CFO can defend; mid is the planning case; optimistic is the stretch.

| Lever | Conservative | Mid | Optimistic |
|-------|--------------|-----|-----------|
| Research automation | 40% | 65% | 80% |
| Data-spend replacement | 50% | 70% | 85% |
| Compliance review reduction | 40% | 60% | 75% |
| Pipeline lift | 30% | 50% | 100% |
| Cycle compression | 15% | 25% | 40% |
| Win-rate lift | 0pp | +3pp | +6pp |

If the conservative case shows < 2.0× ROI, the deal is not ROI-defensible — the AE should re-scope or disqualify.

### 3.6 Worked example — BFSI Mid-market (Tier-1 finance company)

**Customer profile**: SAR 800M revenue finance company, 12 BDRs, 8 AEs, avg deal size SAR 350K (business banking acquisition), 18% win rate, 120-day cycle, currently spending SAR 220K/year on Apollo + ZoomInfo + boutique agencies, 8 outbound campaigns/year requiring DPO review.

**Inputs**:
- BDRs = 12, loaded cost SAR 180K each, 60% research time.
- Data-vendor spend = SAR 220K/year.
- Compliance: 8 campaigns × 16 hours × SAR 350/hr loaded.
- AEs = 8, current deals/year = 8 × (365/120) × 0.18 ≈ 4.4 deals/AE = ~35 closed-won/year, SAR 12.3M revenue from new logos.

**Cost Savings (Mid scenario)**:
- `CS_labor` = 12 × 180,000 × 0.60 × 0.65 = **SAR 842,400**.
- `CS_data` = 220,000 × 0.70 = **SAR 154,000**.
- `CS_compliance` = 8 × 16 × 350 × 0.60 = **SAR 26,880**.
- **Total CS = SAR 1,023,280**.

**Revenue Uplift (Mid scenario)**:
- `RU_pipeline` = pipeline lifts 50%, win-rate +3pp → incremental deals = 35 × 0.50 × (0.21/0.18) − 35 = ~17 incremental deals × 350K avg = **SAR 5.95M**.
- `RU_cycle` = 25% cycle compression frees 25% more AE capacity → 8 × 4.4 × 0.25 ≈ 9 incremental deals × 0.21 win × 350K = **SAR 661K** (capacity-constrained; conservative haircut applied).
- **Total RU = SAR 6.6M (gross-revenue terms)**. CFO bridge: apply 30% gross-margin assumption → **SAR 1.98M margin uplift** for net-ROI defensibility.

**Dealix Cost (Enterprise base, annual prepay)**:
- SAR 35,000/mo × 12 × 0.85 = **SAR 357,000/year**.
- Add custom connector (Sectoral chamber data) SAR 12K one-time + 2K/mo × 12 = **SAR 36,000**.
- **Total Dealix cost year-1 = SAR 393,000**.

**Net ROI (Mid, margin basis)**:
- `Net ROI = (1,023,280 + 1,980,000) − 393,000 = SAR 2.61M`.
- `ROI % = 2,610,280 / 393,000 = 664%`.
- `Payback = 393,000 / (250,273/month) ≈ 1.6 months`.

**Net ROI (Conservative)**:
- CS = ~SAR 540K, RU (margin) = ~SAR 800K, Net = SAR 947K, ROI = 241%, payback ≈ 3.5 months.

**Net ROI (Optimistic)**:
- CS = ~SAR 1.25M, RU (margin) = ~SAR 3.6M, Net = SAR 4.46M, ROI = 1,135%, payback ≈ 1.0 month.

**Procurement-defensible headline**: "Conservative net SAR 947K, mid SAR 2.6M, payback under 4 months in the worst credible case."

### 3.7 Discovery inputs to collect (the 7 numbers)

The AE must collect these 7 numbers during discovery to run the model. If any is missing, mark the opportunity at Discovery stage, not Opportunity stage.

1. # BDRs and their loaded annual cost (HR or proxy).
2. % of BDR time spent on research and list-build today.
3. Annual spend on data vendors / agencies / list buys (procurement record).
4. # AEs, avg deal size in SAR, current win rate, current cycle length in days.
5. # outbound campaigns per year and current DPO/compliance review hours per campaign.
6. Gross margin % on incremental new-logo revenue (CFO input).
7. Quota and pipeline coverage ratio (sanity bound on incremental deals).

### 3.8 Sensitivity sanity rails

- If mid-case ROI > 1,500%, halve inputs and rerun — the model is overheated.
- If conservative ROI < 200%, the deal is not ROI-defensible at current pricing — engage CRO for scope reduction or stop pursuit.
- If payback > 9 months, escalate to CRO before sending the proposal.

## 4. KPIs

- ROI calculation attached to **100% of opportunities > SAR 100K within 60 days** of opportunity creation.
- Win rate on opps with a sent ROI deck ≥ 1.5× win rate on opps without one (T26 A/B framework tracks this).
- CFO/procurement objection on "ROI not defensible" ≤ 10% of late-stage deals.

## 5. Dependencies

- T3 pricing (Dealix cost input) — `docs/pricing/pricing_packages_sa.md`.
- T16 value metrics (overage pricing in scenario modeling) — `docs/pricing/value_metrics.md`.
- T5 ICP (deal-size and cycle baselines) — `docs/go-to-market/icp_saudi.md`.
- T1 verticals (vertical-specific assumptions) — `docs/go-to-market/saudi_vertical_positioning.md`.
- T8 persona matrix (which numbers to ask which persona) — `docs/sales/persona_value_matrix.md`.
- T28 sales enablement (rep training to run the model) — `docs/sales/enablement_program.md`.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- AR companion: `docs/sales/roi_model_saudi.ar.md`
- ROI deck outline: `docs/sales/roi_deck_outline.md`
- Existing: `docs/ROI_PROOF_PACK.md` (cross-link only; not replaced).

## 7. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: quarterly with CFO; default assumptions refreshed every 6 months against win/loss data (T17).

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial SAR ROI model with BFSI worked example, three scenarios, discovery inputs |
