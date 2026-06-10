# Experimentation System — Arabic
## نظام التجارب

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

The Experimentation System enables systematic testing of GTM, commercial, and operational hypotheses to drive data-backed decisions.

---

## 2. Experiment Types

### 2.1 Outreach Experiments

| Type | Description | Primary Metric |
|------|-------------|----------------|
| Subject Line | Test different subject lines | open_rate |
| Preview Text | Test preview text variations | open_rate |
| CTA | Test different CTAs | click_rate |
| Send Time | Test different send times | reply_rate |
| Personalization | Test personalization levels | reply_rate |
| Sector Targeting | Test different sectors | positive_rate |
| Offer Framing | Test different offer angles | meeting_rate |

### 2.2 Commercial Experiments

| Type | Description | Primary Metric |
|------|-------------|----------------|
| Pricing Anchor | Test different price points | close_rate |
| Proposal Format | Test proposal layouts | close_rate |
| Proof Pack Angle | Test different proof types | proposal_request_rate |
| Discount Test | Test discount levels | close_rate + deal_size |
| Payment Terms | Test payment options | close_rate |

### 2.3 WhatsApp Experiments

| Type | Description | Primary Metric |
|------|-------------|----------------|
| Action Card | Test different action cards | click_rate |
| Message Length | Test message length | response_rate |
| Media | Test with/without media | engagement_rate |
| Timing | Test send timing | response_rate |

---

## 3. Experiment Structure

### 3.1 Experiment Record

```json
{
  "experiment_id": "EXP_20260603_001",
  "name": "Subject Line: Urgency vs Value",
  "type": "subject_line",
  "hypothesis": "Subject lines with urgency will outperform value-focused subject lines",
  "owner": "Head of GTM",
  "created_at": "2026-06-03T00:00:00Z",
  "start_date": "2026-06-10",
  "end_date": "2026-06-24",
  "status": "planned",
  "segment": {
    "sector": "technology",
    "tier": "A",
    "size": "all"
  },
  "variants": [
    {
      "variant_id": "A",
      "name": "Control (Value-focused)",
      "description": "Subject line focuses on business value",
      "traffic_allocation": 50
    },
    {
      "variant_id": "B",
      "name": "Treatment (Urgency-focused)",
      "description": "Subject line creates urgency",
      "traffic_allocation": 50
    }
  ],
  "primary_metric": "open_rate",
  "secondary_metrics": ["click_rate", "reply_rate"],
  "sample_size_target": 1000,
  "minimum_detectable_effect": 10,
  "statistical_significance": 0.95,
  "result": null,
  "decision": null,
  "next_action": null
}
```

### 3.2 Required Fields

| Field | Required | Description |
|-------|----------|-------------|
| experiment_id | Yes | Unique identifier |
| name | Yes | Experiment name |
| hypothesis | Yes | Clear hypothesis statement |
| variants | Yes | At least 2 variants |
| primary_metric | Yes | Main success metric |
| sample_size_target | Yes | Required sample per variant |
| start_date | Yes | Experiment start date |
| end_date | Yes | Experiment end date |

---

## 4. Experiment Rules

### 4.1 Safety Rules

⚠️ **NEVER experiment with:**
- Guaranteed claims or false statements
- Fake urgency or artificial scarcity
- Misleading subject lines
- Discriminatory targeting
- Non-compliant content

### 4.2 Statistical Requirements

| Requirement | Value |
|-------------|-------|
| Minimum sample size | 100 per variant |
| Minimum runtime | 7 days |
| Statistical significance | 95% |
| Minimum detectable effect | 10% relative |

### 4.3 Compliance Rules

```python
COMPLIANCE_RULES = {
    "no_guaranteed_claims": True,
    "no_fake_urgency": True,
    "no_misleading_subjects": True,
    "no_discrimination": True,
    "no_pii_exposure": True,
    "consent_required": True
}
```

---

## 5. Experiment Process

### 5.1 Lifecycle

```
1. Hypothesis → 2. Design → 3. Review → 4. Launch → 5. Monitor → 6. Analyze → 7. Decide
```

### 5.2 Step 1: Hypothesis

```
Format: "We believe that [change] will result in [improvement] because [reason]"

Example: "We believe that adding a calendar link to the email CTA will result 
          in a 20% increase in meeting bookings because it removes friction 
          in the booking process."
```

### 5.3 Step 2: Design

- Define variants (control + treatment)
- Set traffic allocation
- Define success metrics
- Calculate required sample size
- Set minimum detectable effect

### 5.4 Step 3: Review

Required approvals:
- Founder: All experiments
- Compliance: Content changes
- Legal: Pricing changes

### 5.5 Step 4: Launch

- Implement variants
- Set up tracking
- Start experiment
- Announce to team

### 5.6 Step 5: Monitor

Daily checks:
- Sample size reached
- No statistical errors
- No compliance issues
- Metrics trending as expected

### 5.7 Step 6: Analyze

```
Statistical Test: Two-proportion z-test

Z = (p_treatment - p_control) / sqrt(p_pooled * (1 - p_pooled) * (1/n_treatment + 1/n_control))

Significant if: |Z| > 1.96 (95% confidence)
```

### 5.8 Step 7: Decide

| Result | Decision | Action |
|--------|----------|--------|
| Winner (95% sig) | IMPLEMENT | Ship winner |
| Loser | DISCARD | Keep control |
| Inconclusive | REPEAT | Extend or redesign |
| Negative | STOP | Revert if shipped |

---

## 6. A/B Test Policy

### 6.1 Subject Line Policy

| Allowed | NOT Allowed |
|---------|-------------|
| Different value propositions | Different sender names |
| Different urgency levels (genuine) | Fake urgency or scarcity |
| Different questions | Misleading statements |
| Different lengths | False claims |
| Different personalization | Spam trigger words |

### 6.2 Pricing Policy

| Allowed | NOT Allowed |
|---------|-------------|
| Different anchoring | Hidden fees |
| Different payment terms | Bait and switch |
| Different bundling | False discounts |
| Different packaging | Misleading pricing |

### 6.3 Targeting Policy

| Allowed | NOT Allowed |
|---------|-------------|
| Different sectors | Discriminatory criteria |
| Different company sizes | Protected characteristics |
| Different seniority levels | Non-compliant targeting |
| Different geographies | Embargoed regions |

---

## 7. Experiment Results Template

```
# Experiment Results: {experiment_name}
**Date:** {completion_date}
**Duration:** {days}

## Hypothesis
{hypothesis}

## Results

| Metric | Control | Treatment | Difference | Significance |
|--------|---------|-----------|------------|--------------|
| open_rate | 25% | 32% | +28% | p < 0.01 |
| click_rate | 5% | 7% | +40% | p < 0.05 |
| reply_rate | 8% | 10% | +25% | p < 0.10 |

## Statistical Analysis
- Sample size: 1,024 / 1,018
- Z-score: 3.42
- P-value: 0.0006
- Confidence: 99.9%
- **Result: SIGNIFICANT WINNER**

## Decision
- **IMPLEMENT** treatment
- Roll out to all segments

## Next Action
- Update email templates
- Document learnings
- Plan follow-up experiments
```

---

## 8. Experimentation Calendar

### 8.1 Active Experiments

| Experiment | Start | End | Status |
|------------|-------|-----|--------|
| Subject Line: Urgency vs Value | Jun 10 | Jun 24 | Planned |
| CTA: Calendar Link vs Button | Jun 17 | Jun 30 | Planned |

### 8.2 Planned Experiments

| Experiment | Target Start | Priority |
|------------|--------------|----------|
| Send Time: Morning vs Afternoon | Jul 1 | High |
| WhatsApp: Text vs Media | Jul 15 | Medium |
| Pricing: Monthly vs Annual | Aug 1 | High |

### 8.3 Completed Experiments

| Experiment | Result | Decision |
|------------|--------|----------|
| Personalization: Name vs Company | +15% reply rate | IMPLEMENT |
| Proof Pack: Case Study vs ROI | +10% meeting rate | IMPLEMENT |

---

## 9. Learning Repository

### 9.1 What Works

| Tactic | Impact | Confidence |
|--------|--------|------------|
| Personalized subject lines | +15% open rate | High |
| Calendar link in CTA | +20% meeting rate | High |
| Value-focused messaging | +10% positive rate | Medium |
| Morning sends (8-10am) | +12% reply rate | Medium |

### 9.2 What Doesn't Work

| Tactic | Impact | Confidence |
|--------|--------|------------|
| Generic mass emails | -25% reply rate | High |
| Heavy discounting | -15% deal size | High |
| Long emails (> 200 words) | -18% read rate | Medium |
| Multiple CTAs | -10% click rate | Medium |

---

**Next:** See `EXPERIMENT_REVIEW.md` for experiment results reporting.
