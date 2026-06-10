# Client Lifecycle Funnel — Arabic
## قمع دورة حياة العميل

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Client Lifecycle Overview

```
Active Delivery
      ↓
Health Monitoring (Ongoing)
      ↓
Renewal Candidate
      ↓
Renewal Initiated
      ↓
Renewed (or Churned)
```

---

## 2. Lifecycle Stages

### Stage 1: Active Delivery

| Attribute | Value |
|-----------|-------|
| Event | `customer.onboarded` |
| Criteria | Successfully onboarded, receiving service |
| Key Metrics | Active clients, delivery tasks completed |
| Owner | Delivery Team |
| Duration | Initial 90 days + ongoing |

### Stage 2: Health Monitoring

| Attribute | Value |
|-----------|-------|
| Event | `customer.health_changed` |
| Criteria | Continuous health scoring |
| Key Metrics | Health score, engagement, satisfaction |
| Owner | Customer Success |
| Duration | Ongoing |

### Stage 3: Renewal Candidate

| Attribute | Value |
|-----------|-------|
| Event | Renewal window opens (90 days before expiry) |
| Criteria | Contract ending within 90 days |
| Key Metrics | Renewal candidates count, ARR at risk |
| Owner | Customer Success |
| Duration | 90 days |

### Stage 4: Renewal Initiated

| Attribute | Value |
|-----------|-------|
| Event | Renewal conversation started |
| Criteria | CSM has contacted client about renewal |
| Key Metrics | Renewal pipeline value |
| Owner | Customer Success |

### Stage 5: Renewed / Churned

| Attribute | Value |
|-----------|-------|
| Events | `deal.won` (renewal) or `customer.churned` |
| Outcomes | Renewed, Expanded, Churned, Downgraded |
| Key Metrics | Renewal rate, NRR, Churn rate |
| Owner | CS + Sales |

---

## 3. Health Score Model

### 3.1 Health Components

| Component | Weight | Indicators |
|-----------|--------|------------|
| Engagement | 40% | Login frequency, feature usage, QBR attendance |
| Delivery | 30% | Task completion, milestone hit, blockers |
| Satisfaction | 30% | NPS, feedback, escalations |

### 3.2 Health Bands

| Band | Score | Color | Action |
|------|-------|-------|--------|
| Thriving | 80-100 | Green | Nurture for expansion |
| Healthy | 60-79 | Green | Maintain |
| Needs Attention | 40-59 | Yellow | Develop improvement plan |
| At Risk | 20-39 | Orange | Immediate intervention |
| Critical | 0-19 | Red | Escalate to leadership |

### 3.3 Health Thresholds

```python
HEALTH_THRESHOLDS = {
    "thriving": {"min": 80, "action": "expansion_candidate"},
    "healthy": {"min": 60, "action": "maintain"},
    "attention": {"min": 40, "action": "create_plan"},
    "risk": {"min": 20, "action": "immediate_intervention"},
    "critical": {"min": 0, "action": "escalate"},
}
```

---

## 4. Client Metrics

### 4.1 Engagement Metrics

| Metric | Definition | Good | Warning | Critical |
|--------|------------|------|---------|----------|
| login_frequency | Logins per week | > 5 | 3-5 | < 3 |
| feature_adoption | Features used / available | > 60% | 40-60% | < 40% |
| qbr_attendance | QBRs attended / scheduled | 100% | 80-99% | < 80% |
| response_time | Avg hours to respond | < 24h | 24-48h | > 48h |

### 4.2 Delivery Metrics

| Metric | Definition | Good | Warning | Critical |
|--------|------------|------|---------|----------|
| task_completion | Tasks completed / assigned | > 90% | 70-90% | < 70% |
| milestone_hit | Milestones on time | > 80% | 60-80% | < 60% |
| blockers | Open blockers | 0 | 1-2 | > 2 |
| escalation_rate | Escalations per quarter | 0 | 1-2 | > 2 |

### 4.3 Satisfaction Metrics

| Metric | Definition | Good | Warning | Critical |
|--------|------------|------|---------|----------|
| nps | Net Promoter Score | > 50 | 30-50 | < 30 |
| csat | Customer Satisfaction | > 4.5 | 3.5-4.5 | < 3.5 |
| feedback_score | Avg feedback (1-5) | > 4 | 3-4 | < 3 |

---

## 5. Renewal Process

### 5.1 Renewal Timeline

| Timeline | Action |
|----------|--------|
| T-90 days | Identify as renewal candidate |
| T-90 to T-60 | Prepare renewal package |
| T-60 days | Initial renewal conversation |
| T-60 to T-30 | Present renewal proposal |
| T-30 days | Decision deadline |
| T-0 | Contract expiry |

### 5.2 Renewal Indicators

| Indicator | Positive | Negative |
|-----------|----------|----------|
| Health Score Trend | Increasing | Decreasing |
| Usage Trend | Stable/Increasing | Declining |
| Engagement | High | Low/Sporadic |
| Escalations | None/Resolved | Increasing |
| Expansion History | Has expanded | Only core usage |
| Stakeholder Access | Multiple contacts | Single contact |
| Competitive Pressure | None | Active evaluation |

---

## 6. Churn Analysis

### 6.1 Churn Risk Factors

| Factor | Weight | Indicators |
|--------|--------|------------|
| Health Score | High | Score < 40 |
| Engagement | High | No login > 30 days |
| Delivery Issues | Medium | Open blockers > 14 days |
| Escalation | Medium | > 2 escalations |
| Competition | Medium | Mentioned competitors |
| Price | Low | Price sensitivity flagged |
| Support Issues | Medium | Low CSAT scores |

### 6.2 Churn Prediction Model

```python
CHURN_PROBABILITY = (
    health_score * 0.30 +
    engagement_score * 0.25 +
    delivery_score * 0.20 +
    escalation_count * 0.15 +
    competitive_pressure * 0.10
)

# Churn Risk Levels
HIGH_RISK = churn_probability > 0.7
MEDIUM_RISK = churn_probability > 0.4
LOW_RISK = churn_probability <= 0.4
```

---

## 7. Net Revenue Retention (NRR)

### 7.1 NRR Components

```
NRR = (Starting ARR + Expansion - Contraction - Churn) / Starting ARR × 100
```

### 7.2 NRR Targets

| NRR | Classification |
|-----|----------------|
| > 120% | World Class |
| 110-120% | Excellent |
| 100-110% | Good |
| 90-100% | Fair |
| < 90% | At Risk |

### 7.3 NRR Breakdown

| Client | Starting ARR | Expansion | Contraction | Churn | Ending ARR | NRR |
|--------|--------------|-----------|-------------|-------|-----------|-----|
| Client A | 100K | +20K | 0 | 0 | 120K | 120% |
| Client B | 80K | 0 | -10K | 0 | 70K | 87.5% |
| Client C | 60K | +5K | 0 | -60K | 5K | 8.3% |
| Total | 240K | +25K | -10K | -60K | 195K | 81.25% |

---

**Next:** See `FUNNEL_REVIEW.md` for funnel analysis report template.
