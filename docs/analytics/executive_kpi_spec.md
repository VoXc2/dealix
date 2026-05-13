---
title: Executive KPI Spec — dashboard wireframe, metric definitions, sources, cadences, owners
doc_id: W4.T13.executive-kpi-spec
owner: CEO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T12.event-taxonomy, W4.T14.revenue-os-policy-rules, W4.T23.slo-framework, W4.T24.model-cost-governance, W4.T25.data-quality-gates]
kpi: { metric: dashboard_refresh_freshness_minutes, target: 60, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 5pw, score: engineering }
---

# Executive KPI Spec

## 1. Purpose

Define the executive dashboard that the CEO and the leadership team use to run Dealix: which tiles exist, what each metric means, where the number comes from, how often it refreshes, who owns it, and what drill-down it links to. Cross-links the existing `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` operational dashboard.

The exec dashboard answers four questions:

1. **Are we growing revenue durably?** (ARR, MRR, NRR, pipeline coverage)
2. **Are we converting?** (win rate, time-to-value)
3. **Are we delivering profitably?** (gross margin, LLM cost per workflow)
4. **Is the engine healthy?** (Lead Engine throughput, SLO compliance, DQ pass rate)

## 2. Wireframe

```
+================================================================+
|  DEALIX EXECUTIVE DASHBOARD       Refresh: 60 min | Window: 28d|
+================================================================+
|  Row 1 — REVENUE (CEO)                                         |
|  [ARR]              [MRR]             [NRR]      [Pipe Cover.] |
+----------------------------------------------------------------+
|  Row 2 — CONVERSION (HoSales)                                  |
|  [Win Rate]   [Time-to-Value]    [Pilot→Paid]   [Avg Deal SAR] |
+----------------------------------------------------------------+
|  Row 3 — UNIT ECONOMICS (CEO + CTO)                            |
|  [Gross Margin] [LLM Cost/Workflow] [CAC]       [Payback Mo.]  |
+----------------------------------------------------------------+
|  Row 4 — PRODUCT HEALTH (HoData + CTO)                         |
|  [Lead Engine Throughput] [Passport p95] [SLO Compl.] [DQ Pass]|
+================================================================+
```

Each tile is **clickable**, linking to a drill-down view defined in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`.

## 3. Metric Definitions

### 3.1 ARR — Annual Recurring Revenue (SAR)

- **Definition**: sum of MRR × 12 across all active subscriptions on the report date. Excludes one-time fees, services revenue, and trial subscriptions.
- **Source**: `billing_subscription_renewed` and `billing_invoice_paid` events; reconciled with Moyasar daily.
- **Refresh**: daily 06:00 KSA.
- **Owner**: CEO.
- **Drill-down**: by tier, by vertical, by region.
- **Target Y1**: 1.8M SAR by 2026-12-31.

### 3.2 MRR — Monthly Recurring Revenue (SAR)

- **Definition**: sum of normalized monthly subscription value on the report date.
- **Components reported separately**: New, Expansion, Contraction, Churn, Reactivation.
- **Source**: same as ARR.
- **Refresh**: daily 06:00 KSA.
- **Owner**: CEO.
- **Drill-down**: MRR waterfall by month, by cohort.
- **Target**: monotonically increasing month-over-month for 6 consecutive months.

### 3.3 Pipeline Coverage

- **Definition**: `(sum_of_open_pipeline_SAR_by_stage_weighted / quarterly_quota_SAR)` for the current and next quarter combined.
- **Stage weights**: Lead 0.05, Qualified 0.15, Demo Booked 0.35, Negotiation 0.65, Verbal 0.85.
- **Source**: CRM (own DB); fed by `lead_disposition_set` and downstream sales events.
- **Refresh**: daily 06:00 KSA.
- **Owner**: HoSales (proxied to CEO until role hired).
- **Drill-down**: per stage, per AE, per vertical.
- **Target**: ≥ 3.0× current-quarter quota.

### 3.4 Win Rate

- **Definition**: `(deals_won / (deals_won + deals_lost))` over the rolling 90-day window for closed-out deals.
- **Excludes**: deals still open, deals churned.
- **Source**: CRM closed-deal events.
- **Refresh**: weekly Monday 06:00 KSA.
- **Owner**: HoSales / CEO.
- **Drill-down**: by deal size band, by vertical, by lead source.
- **Target**: ≥ 22% in Y1; ≥ 28% in Y2.

### 3.5 Time-to-Value (days)

- **Definition**: median days between `billing_subscription_renewed` (initial) and first `passport_outcome_recorded` where `outcome=positive` for that tenant.
- **Source**: event store; computed in the daily roll-up.
- **Refresh**: daily 06:00 KSA.
- **Owner**: Head of CS.
- **Drill-down**: by tier; per-tenant TTV table; cohort retention curve.
- **Target**: ≤ 14 days (Starter), ≤ 10 days (Growth), ≤ 7 days (Sovereign).

### 3.6 NRR — Net Revenue Retention

- **Definition**: `((starting_MRR + expansion - contraction - churn) / starting_MRR)` measured on a 12-month rolling cohort.
- **Source**: subscription change events.
- **Refresh**: monthly on day 5.
- **Owner**: CEO.
- **Drill-down**: cohort by start month; expansion vs. churn split.
- **Target**: ≥ 110% by month 12.

### 3.7 Gross Margin

- **Definition**: `(revenue - COGS) / revenue` where COGS = LLM spend + hosting + 3rd-party APIs + support delivery cost.
- **Source**: monthly close from finance; LLM portion from `llm_cost_sar_total` metric.
- **Refresh**: monthly on day 7.
- **Owner**: CEO.
- **Drill-down**: COGS components (LLM / infra / data / support / other).
- **Target**: ≥ 65% by month 18; ≥ 75% steady state.

### 3.8 LLM Cost per Workflow (SAR, median)

- **Definition**: median across all paid workflows in the 28-day window.
- **Source**: `llm_cost_sar_total` metric (per FinOps doc).
- **Refresh**: hourly.
- **Owner**: CTO.
- **Drill-down**: by workflow type, by model, by cache hit rate, by tenant.
- **Target**: ≤ 1.20 SAR median; ≤ 3.00 SAR p95.

### 3.9 CAC — Customer Acquisition Cost (SAR)

- **Definition**: `(total_sales_and_marketing_spend / new_customers_acquired)` in the trailing 90-day window.
- **Source**: finance close; CRM new-customer count.
- **Refresh**: monthly on day 7.
- **Owner**: CEO.
- **Drill-down**: by channel, by vertical.
- **Target**: Starter ≤ 3,000 SAR; Growth ≤ 12,000 SAR; Sovereign ≤ 60,000 SAR.

### 3.10 Payback Months

- **Definition**: `CAC / (monthly_gross_margin_per_customer)`.
- **Source**: derived from 3.7 and 3.9.
- **Refresh**: monthly.
- **Owner**: CEO.
- **Target**: ≤ 9 months for Starter, ≤ 12 months for Growth, ≤ 18 months for Sovereign.

### 3.11 Lead Engine Throughput

- **Definition**: `(leads_qualified_with_passport_emitted / day)` across all tenants, 7-day moving average.
- **Source**: `passport_emission_completed` events filtered to `evidence_level >= medium`.
- **Refresh**: hourly.
- **Owner**: HoData.
- **Drill-down**: per tenant, per vertical, per region.
- **Target**: ≥ 300/day at end of Q2 2026; ≥ 1,200/day at end of Y1.

### 3.12 Passport p95 Latency (ms)

- **Definition**: p95 of `POST /api/v1/decision-passport` over the 28-day window.
- **Source**: SLI from SLO framework.
- **Refresh**: live (≤ 1 min).
- **Owner**: CTO.
- **Target**: per SLO framework tier targets.

### 3.13 SLO Compliance

- **Definition**: percent of SLOs (across all SLIs and tiers) currently within target.
- **Source**: SLO framework dashboards.
- **Refresh**: live.
- **Owner**: CTO.
- **Target**: 100%.

### 3.14 Data Quality Pass Rate

- **Definition**: aggregate DQ pass rate per data quality gates doc.
- **Source**: DQ gate metrics.
- **Refresh**: hourly.
- **Owner**: HoData.
- **Target**: per data quality gates tier thresholds.

## 4. Tile Metadata Table

| Tile | Metric ID | Owner | Refresh | Source | Drill-down doc |
|---|---|---|---|---|---|
| ARR | `kpi.arr.sar` | CEO | daily | event store + Moyasar | BUSINESS_KPI_DASHBOARD_SPEC.md §1 |
| MRR | `kpi.mrr.sar` | CEO | daily | event store + Moyasar | §2 |
| NRR | `kpi.nrr.pct` | CEO | monthly | subscription events | §3 |
| Pipeline Coverage | `kpi.pipe_cov.x` | HoSales | daily | CRM | §4 |
| Win Rate | `kpi.win_rate.pct` | HoSales | weekly | CRM | §5 |
| Time-to-Value | `kpi.ttv.days` | HoCS | daily | passport events | §6 |
| Pilot→Paid | `kpi.pilot_conv.pct` | HoSales | weekly | CRM | §7 |
| Avg Deal SAR | `kpi.avg_deal.sar` | HoSales | weekly | CRM | §8 |
| Gross Margin | `kpi.gm.pct` | CEO | monthly | finance close | §9 |
| LLM Cost/Workflow | `kpi.llm_cost.sar` | CTO | hourly | metrics | §10 |
| CAC | `kpi.cac.sar` | CEO | monthly | finance + CRM | §11 |
| Payback Months | `kpi.payback.mo` | CEO | monthly | derived | §12 |
| Lead Engine TPS | `kpi.lead_engine.per_day` | HoData | hourly | passport events | §13 |
| Passport p95 | `kpi.passport_p95.ms` | CTO | live | OTel | §14 |
| SLO Compliance | `kpi.slo_compl.pct` | CTO | live | SLO framework | §15 |
| DQ Pass | `kpi.dq_pass.pct` | HoData | hourly | DQ gates | §16 |

## 5. Anti-Patterns

- **Vanity metrics on the exec dashboard**: total leads in DB, page views — none of these belong here. Each tile must be tied to a decision.
- **Mismatched window**: don't show a 7-day metric next to a 28-day metric without labeling the window.
- **Hidden definitions**: every tile has a tooltip with the definition and a link to this doc.
- **Per-tile alerts that aren't actionable**: tile alerts are reserved for the four metrics that have explicit thresholds (ARR target slipping, gross margin below floor, LLM cost above cap, SLO compliance below 100%).

## 6. Refresh Architecture

- **Live tiles** (Passport p95, SLO Compliance): pulled from Prometheus on render; cached 30 s.
- **Hourly tiles**: a scheduled job materializes a `kpi_snapshot` table from event store + Moyasar + CRM; dashboard reads the table.
- **Daily / weekly / monthly tiles**: nightly job at 06:00 KSA writes a `kpi_daily_snapshot` row.
- **Source of truth**: every tile's number must be re-derivable from raw events; the snapshot tables are caches, not authority.

## 7. Access and Audit

- Dashboard access: CEO, CTO, HoData, HoSales, HoCS by default; explicit invite for others.
- Every dashboard view is logged (event `dashboard_viewed`) for compliance.
- Sovereign tenant breakdowns are visible only to roles with `sovereign_view` permission.
- Sharing externally requires a redacted export (no per-tenant rows).

## 8. Cross-Link to BUSINESS_KPI_DASHBOARD_SPEC

`docs/BUSINESS_KPI_DASHBOARD_SPEC.md` is the operational specification — column-by-column, query-by-query — for the same metrics. Reconciliation rule:

- Every tile here MUST map to a section in the operational spec.
- Every metric in the operational spec is either on this exec dashboard or is justified as operational-only (out of exec scope).
- Quarterly reconciliation between this doc and the operational spec.

## 9. Change Management

- Adding a new tile: requires CEO sign-off; metric must already be defined in `analytics/metric_catalog.yaml`.
- Changing a metric definition: requires CEO + CTO sign-off; old definition is retained for trailing 12 months for historical comparisons.
- Removing a tile: requires CEO sign-off; reason logged.

## 10. References

- Operational dashboard: `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` (kept in sync).
- Event taxonomy: `docs/analytics/event_taxonomy.md`.
- SLO framework: `docs/sre/slo_framework.md`.
- Model cost governance: `docs/finops/model_cost_governance.md`.
- Data quality gates: `docs/data/data_quality_gates.md`.
- Pricing: `docs/PRICING_AND_PACKAGING_V6.md`.
- Unit economics: `docs/UNIT_ECONOMICS_AND_MARGIN.md`.
- Business model: `docs/BUSINESS_MODEL.md`.

## 11. Review Cadence

Quarterly. CEO + CTO + HoData review the metrics list for relevance; tiles that no longer drive a decision are removed.
