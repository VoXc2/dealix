---
doc_id: company.north_star_metrics
title: Dealix North-Star + Supporting Metrics
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
---

# North-Star + Supporting Metrics

> One metric the company is run by; six families of supporting metrics
> that explain it. Full dashboard wireframe, metric definitions,
> refresh cadences, and owners in `docs/analytics/executive_kpi_spec.md`.

## North-Star

> **Recurring Outcome Revenue (ROR) in SAR per month.**
> **AR:** "الإيرادات المتكررة بالنتائج بالريال السعودي شهرياً."

ROR = MRR from retainers + amortized Sprint revenue tied to a delivered
Proof Pack (recognized over 30 days). It measures the only thing that
matters: **paying customers receiving measurable outcomes, every month.**

**Target trajectory:**
- Month 3: SAR 30,000 MRR (first 2 retainers).
- Month 6: SAR 80,000 MRR.
- Month 12: SAR 300,000 MRR (≈ SAR 3.6M ARR).
- Month 18: SAR 700,000 MRR.

## Supporting metric families

### 1. Revenue (CEO)
- **ARR (SAR)** — daily refresh. Target SAR 1.8M by 2026-12-31.
- **MRR waterfall** — New / Expansion / Contraction / Churn / Reactivation.
- **NRR** — ≥ 110% by Month 12.
- **Pipeline coverage** — ≥ 3.0× current-quarter quota.

### 2. Delivery (HoCS)
- **Quality Score (5-gate)** — floor 80/100 to ship. 100% of projects.
- **Time-to-Value (days)** — ≤ 14 Starter / ≤ 10 Growth / ≤ 7 Sovereign.
- **Sprint-to-retainer conversion** — ≥ 40% within 60 days post-close.
- **Proof Pack capture** — 100% of projects within 14 days of delivery.

### 3. Product (CTO / HoP)
- **Productized revenue share** — ≥ 80% by Month 12 (catalog-hit rate).
- **OS module reuse rate** — every offering uses ≥ 2 shared modules.
- **Lead Engine throughput** — ≥ 300 ranked/day by end of Q2; ≥ 1,200/day by Y1.

### 4. AI Quality (CTO / HoData)
- **Data Quality pass rate** — per `docs/data/data_quality_gates.md` thresholds.
- **LLM cost per workflow (SAR)** — ≤ 1.20 median / ≤ 3.00 p95.
- **Hallucination rate** — 0 incidents with unsourced claims in production
  (Operating Principle #5: no source = no answer).
- **Eval pass rate** — ≥ 95% on Knowledge OS gold set.

### 5. Governance (CTO / HoLegal)
- **PDPL Art. 13/14 enforcement** — 100% outbound passes Approval Matrix.
- **Decision Passport coverage** — every external action emits a passport.
- **SLO compliance** — 100% of SLIs in target (per `docs/sre/slo_framework.md`).
- **Forbidden-claims violations** — 0 in production (auto-blocked).

### 6. Unit Economics (CEO + CFO)
- **Gross Margin** — ≥ 65% by Month 18; ≥ 75% steady state.
- **CAC per tier** — ≤ SAR 3K Starter / ≤ SAR 12K Growth / ≤ SAR 60K Sovereign.
- **Payback months** — ≤ 9 / 12 / 18 by tier.

## Anti-vanity rules

- No tile on the exec dashboard unless tied to a decision.
- Total leads / page views / followers do NOT appear on exec dashboard.
- Every tile has a defined window; never mix windows without labeling.
- Every metric is re-derivable from raw events (snapshots are caches,
  not authority).

## Cadence

- **Live**: Passport p95, SLO compliance.
- **Hourly**: LLM cost / workflow, Lead Engine throughput, DQ pass.
- **Daily 06:00 KSA**: ARR, MRR, Pipeline Coverage, TTV.
- **Weekly Mon 06:00**: Win Rate, Pilot→Paid, Avg Deal SAR.
- **Monthly day 7**: Gross Margin, CAC, Payback, NRR.

## Cross-links

- Canonical KPI spec (W4.T13): `docs/analytics/executive_kpi_spec.md`
- Operational dashboard: `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`
- Event taxonomy: `docs/analytics/event_taxonomy.md`
- SLO framework: `docs/sre/slo_framework.md`
- FinOps / model cost: `docs/finops/model_cost_governance.md`
- Data quality gates: `docs/data/data_quality_gates.md`
- Unit economics: `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- Operating principles: `docs/company/OPERATING_PRINCIPLES.md`
