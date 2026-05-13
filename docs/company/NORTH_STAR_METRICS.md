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

> One metric the company is run by; six supporting families. Full
> dashboard spec, definitions, refresh, and owners in
> `docs/analytics/executive_kpi_spec.md`.

## North-Star

> **Recurring Outcome Revenue (ROR) in SAR per month.**
> **AR:** "الإيرادات المتكررة بالنتائج بالريال شهرياً."

ROR = MRR from retainers + amortized Sprint revenue tied to a delivered
Proof Pack (recognized over 30 days). The only thing that matters:
paying customers receiving measurable outcomes every month.

**Target trajectory:** Month 3: SAR 30K MRR · Month 6: SAR 80K MRR ·
Month 12: SAR 300K MRR (~SAR 3.6M ARR) · Month 18: SAR 700K MRR.

## Supporting metric families (six)

### 1. Revenue (CEO)
ARR (daily) · MRR waterfall · NRR ≥ 110% by M12 · Pipeline coverage
≥ 3.0× quota.

### 2. Delivery (HoCS)
Quality Score 5-gate floor ≥ 80/100 · Time-to-Value ≤ 14d Starter / ≤
10d Growth / ≤ 7d Sovereign · Sprint→retainer conversion ≥ 40% in 60d ·
Proof Pack capture 100% in 14d.

### 3. Product (CTO + HoP)
Productized revenue share ≥ 80% by M12 · OS-module reuse (≥ 2 modules /
offering) · Lead Engine throughput ≥ 300/day end of Q2; ≥ 1,200/day Y1.

### 4. AI Quality (CTO + HoData)
Data Quality pass rate per gates · LLM cost / workflow ≤ SAR 1.20
median, ≤ 3.00 p95 · Hallucination rate 0 (no source = no answer) ·
Eval pass ≥ 95% on Knowledge OS gold set.

### 5. Governance (CTO + HoLegal)
PDPL Art. 13/14 enforcement 100% · Decision Passport on every external
action · SLO compliance 100% · Forbidden-claims violations 0.

### 6. Unit Economics (CEO + CFO)
Gross Margin ≥ 65% by M18 · CAC ≤ SAR 3K / 12K / 60K by tier · Payback
≤ 9 / 12 / 18 months by tier.

## Anti-vanity rules

- No tile on the exec dashboard unless tied to a decision.
- Total leads / page views / followers do NOT appear.
- Every tile has a defined window; never mix windows.
- Every metric is re-derivable from raw events.

## Cadence

Live: Passport p95, SLO compliance. Hourly: LLM cost / workflow, Lead
Engine throughput, DQ pass. Daily 06:00 KSA: ARR, MRR, Pipeline
Coverage, TTV. Weekly Mon: Win Rate, Pilot→Paid, Avg Deal SAR. Monthly
day 7: Gross Margin, CAC, Payback, NRR.

## Cross-links

- Canonical KPI spec (W4.T13): `docs/analytics/executive_kpi_spec.md`
- Operational dashboard: `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`
- Event taxonomy: `docs/analytics/event_taxonomy.md`
- SLO framework: `docs/sre/slo_framework.md`
- FinOps: `docs/finops/model_cost_governance.md`
- Data quality gates: `docs/data/data_quality_gates.md`
- Unit economics: `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- Operating principles: `docs/company/OPERATING_PRINCIPLES.md`
