# Revenue Funnel Model — Arabic
## نموذج قمع الإيرادات

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Revenue Funnel Overview

```
Pipeline Created (Deal > 10K SAR)
      ↓
Qualified Pipeline (Proposal Sent)
      ↓
Committed Pipeline (Negotiation Started)
      ↓
Closed Won (Payment Confirmed)
```

---

## 2. Pipeline Stages

### Stage 1: Pipeline Created

| Attribute | Value |
|-----------|-------|
| Criteria | Deal value > 10,000 SAR |
| Event | `deal.created` |
| Key Metrics | Pipeline Created Value, Count |
| Owner | Sales Agent |
| Stage Duration | Days to proposal |

### Stage 2: Qualified Pipeline

| Attribute | Value |
|-----------|-------|
| Criteria | Proposal sent to client |
| Event | `deal.proposal_sent` |
| Key Metrics | Qualified Value, Proposal Rate |
| Owner | Sales Agent |
| Stage Duration | Days to negotiation |

### Stage 3: Committed Pipeline

| Attribute | Value |
|-----------|-------|
| Criteria | Active negotiation, verbal commitment |
| Event | `deal.stage_changed` (to=negotiation) |
| Key Metrics | Committed Value, Commit Rate |
| Owner | Sales Lead |
| Stage Duration | Days to close |

### Stage 4: Closed Won

| Attribute | Value |
|-----------|-------|
| Criteria | Payment confirmed, contract signed |
| Event | `deal.won` |
| Key Metrics | Won Value, Win Rate, ARR |
| Owner | Sales Lead |
| Stage Duration | N/A (terminal) |

---

## 3. Revenue Metrics

### 3.1 Pipeline Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| pipeline_created | Total new pipeline value | SUM(value_sar) WHERE deal.created this period |
| pipeline_qualified | Pipeline with proposals sent | SUM(value_sar) WHERE proposal_sent = true |
| pipeline_committed | Pipeline in negotiation | SUM(value_sar) WHERE stage = negotiation |
| pipeline_won | Closed won value | SUM(value_sar) WHERE stage = won |
| pipeline_lost | Closed lost value | SUM(value_sar) WHERE stage = lost |

### 3.2 Conversion Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| qualify_rate | Pipeline → Qualified | pipeline_qualified / pipeline_created |
| commit_rate | Qualified → Committed | pipeline_committed / pipeline_qualified |
| win_rate | Committed → Won | pipeline_won / pipeline_committed |
| overall_rate | Created → Won | pipeline_won / pipeline_created |

### 3.3 Velocity Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| avg_days_to_qualify | Days from created to proposal | < 14 days |
| avg_days_to_commit | Days from qualified to negotiation | < 21 days |
| avg_days_to_close | Days from committed to won | < 30 days |
| avg_sales_cycle | Full cycle from created to won | < 60 days |

---

## 4. Cohort Analysis

### 4.1 Monthly Cohort Table

| Metric | Jan | Feb | Mar | Apr | May | Jun |
|--------|-----|-----|-----|-----|-----|-----|
| Deals Created | 20 | 25 | 30 | 28 | 35 | 40 |
| Created Value (K SAR) | 800 | 1,000 | 1,200 | 1,120 | 1,400 | 1,600 |
| Qualified | 15 | 20 | 24 | 22 | 28 | 32 |
| Qualified Value (K SAR) | 600 | 800 | 960 | 880 | 1,120 | 1,280 |
| Committed | 10 | 14 | 18 | 16 | 21 | 24 |
| Committed Value (K SAR) | 400 | 560 | 720 | 640 | 840 | 960 |
| Won | 8 | 11 | 14 | 13 | 17 | 19 |
| Won Value (K SAR) | 320 | 440 | 560 | 520 | 680 | 760 |
| Win Rate (vs Created) | 40% | 44% | 47% | 46% | 49% | 48% |
| Avg Deal Size (K SAR) | 40 | 40 | 40 | 40 | 40 | 40 |

### 4.2 Sector Cohort Analysis

| Sector | Pipeline | Qualified | Won | Win Rate |
|--------|----------|-----------|-----|----------|
| Technology | 500K | 400K (80%) | 200K (50%) | 40% |
| Healthcare | 400K | 280K (70%) | 140K (50%) | 35% |
| Finance | 300K | 240K (80%) | 150K (62%) | 50% |
| Retail | 200K | 120K (60%) | 48K (40%) | 24% |
| Manufacturing | 150K | 105K (70%) | 52K (50%) | 35% |

---

## 5. Funnel Health Indicators

### 5.1 Green Flags

- Win rate stable or increasing
- Sales cycle shortening
- Average deal size stable or increasing
- Pipeline coverage > 3x target
- Sector diversification improving

### 5.2 Yellow Flags

- Win rate declining < 10%
- Sales cycle extending > 20%
- Pipeline coverage 2-3x target
- Concentration in single sector > 40%

### 5.3 Red Flags

- Win rate declining > 20%
- Sales cycle > 90 days average
- Pipeline coverage < 2x target
- Single sector concentration > 60%
- Discount rate increasing > 30%
- Price exceptions doubling

---

## 6. Revenue Forecasting

### 6.1 Commit Probabilities

| Stage | Probability | Confidence |
|-------|-------------|------------|
| Pipeline Created | 10% | Low |
| Qualified | 20% | Low-Medium |
| Proposal Sent | 30% | Medium |
| Negotiation | 60% | Medium-High |
| Payment Handoff | 90% | High |
| Closed Won | 100% | Certain |

### 6.2 Weighted Pipeline

```
Weighted Pipeline = 
  (Pipeline Created × 10%) +
  (Qualified × 20%) +
  (Proposal Sent × 30%) +
  (Negotiation × 60%) +
  (Payment Handoff × 90%)
```

---

## 7. Pipeline Coverage

### 7.1 Coverage Ratio

```
Coverage = Pipeline / Target Revenue

Good: > 3x
Acceptable: 2-3x
Warning: 1.5-2x
Critical: < 1.5x
```

### 7.2 Coverage by Sector

| Sector | Target ARR | Pipeline | Coverage | Status |
|--------|------------|----------|----------|--------|
| Technology | 500K | 1.5M | 3.0x | Good |
| Healthcare | 300K | 900K | 3.0x | Good |
| Finance | 200K | 800K | 4.0x | Excellent |
| Retail | 100K | 200K | 2.0x | Warning |
| Manufacturing | 100K | 150K | 1.5x | Critical |

---

**Next:** See `CLIENT_LIFECYCLE_FUNNEL_AR.md` for client lifecycle funnel.
