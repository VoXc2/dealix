# Founder Decision Rules — Arabic
## قواعد قرارات المؤسس

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Decision Rules Overview

These rules transform metrics into specific, actionable decisions for the Founder.

---

## 2. GTM Decision Rules

### Rule 2.1: Bounce Rate Spike

```yaml
Rule ID: GTM_001
Name: Bounce Rate Spike Response
Metric: del_bounce_rate

Conditions:
  - trigger: bounce_rate > 5%
    decision: STOP
    action: Pause email sending immediately
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: Immediate
    
  - trigger: bounce_rate 2-5%
    decision: FIX
    action: Review list quality, verify email formats
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 48 hours
    
  - trigger: bounce_rate < 2%
    decision: CONTINUE
    action: No action needed
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: None
```

### Rule 2.2: Reply Rate Analysis

```yaml
Rule ID: GTM_002
Name: Reply Rate Response
Metric: gtm_reply_rate

Conditions:
  - trigger: reply_rate > 10% AND positive_rate > 40%
    decision: SCALE
    action: Increase volume, double sector allocation
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 72 hours
    
  - trigger: reply_rate > 10% AND positive_rate < 40%
    decision: FIX
    action: Improve targeting, review message quality
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 72 hours
    
  - trigger: reply_rate 5-10%
    decision: CONTINUE
    action: Monitor, test subject lines
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: Weekly review
    
  - trigger: reply_rate < 5%
    decision: FIX
    action: Review ICP, improve personalization
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: 48 hours
```

### Rule 2.3: Positive Reply Rate

```yaml
Rule ID: GTM_003
Name: Positive Reply Analysis
Metric: gtm_positive_rate

Conditions:
  - trigger: positive_rate > 40%
    decision: SCALE
    action: Double allocation to high-performing sector
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: 72 hours
    
  - trigger: positive_rate 20-40%
    decision: CONTINUE
    action: Maintain current approach
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: None
    
  - trigger: positive_rate < 20%
    decision: FIX
    action: Review message content, sector targeting
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: 48 hours
```

### Rule 2.4: Meeting Conversion

```yaml
Rule ID: GTM_004
Name: Meeting Conversion Analysis
Metric: Meeting Booked / Positive Replies

Conditions:
  - trigger: meeting_rate > 50% of positive replies
    decision: CONTINUE
    action: Good discovery flow, maintain
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: None
    
  - trigger: meeting_rate 30-50% of positive replies
    decision: FIX
    action: Improve CTA, booking flow
    evidence_level: L3
    risk_level: Medium
    owner: Head of Sales
    due: 72 hours
    
  - trigger: meeting_rate < 30% of positive replies
    decision: FIX
    action: Major review of discovery process
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 48 hours
```

### Rule 2.5: Close Rate Analysis

```yaml
Rule ID: GTM_005
Name: Close Rate Analysis
Metric: gtm_win_rate

Conditions:
  - trigger: close_rate > 25%
    decision: SCALE
    action: Increase pipeline, hire sales capacity
    evidence_level: L3
    risk_level: Medium
    owner: Head of Sales
    due: 72 hours
    
  - trigger: close_rate 15-25%
    decision: CONTINUE
    action: Maintain current
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: None
    
  - trigger: close_rate < 15%
    decision: FIX
    action: Review proposal, pricing, competitive position
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 48 hours
```

---

## 3. Commercial Decision Rules

### Rule 3.1: Pipeline Value Decline

```yaml
Rule ID: COM_001
Name: Pipeline Decline Response
Metric: com_pipeline_value (trend)

Conditions:
  - trigger: pipeline_decline > 20% week-over-week
    decision: STOP
    action: Emergency prospecting, review pipeline health
    evidence_level: L3
    risk_level: Critical
    owner: Head of Sales
    due: Immediate
    
  - trigger: pipeline_decline 10-20% week-over-week
    decision: FIX
    action: Increase prospecting activity
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 48 hours
    
  - trigger: pipeline_decline < 10% week-over-week
    decision: CONTINUE
    action: Monitor, small adjustment
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: Weekly review
```

### Rule 3.2: Average Deal Size

```yaml
Rule ID: COM_002
Name: Deal Size Analysis
Metric: com_average_deal_size (trend)

Conditions:
  - trigger: deal_size_increasing > 20%
    decision: CONTINUE
    action: Good signal, monitor sustainability
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: None
    
  - trigger: deal_size_decreasing > 10%
    decision: FIX
    action: Review pricing, positioning, ICP
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 72 hours
```

### Rule 3.3: Discount Rate

```yaml
Rule ID: COM_003
Name: Discount Rate Analysis
Metric: com_discount_rate

Conditions:
  - trigger: discount_rate > 25%
    decision: STOP
    action: Immediate discount policy review
    evidence_level: L3
    risk_level: Critical
    owner: Head of Sales
    due: Immediate
    
  - trigger: discount_rate 15-25%
    decision: FIX
    action: Enforce discount approval process
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 48 hours
    
  - trigger: discount_rate < 15%
    decision: CONTINUE
    action: Good discipline, maintain
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: None
```

---

## 4. Delivery Decision Rules

### Rule 4.1: Client Health Risk

```yaml
Rule ID: DEL_001
Name: Client Health Risk Response
Metric: del_clients_at_risk

Conditions:
  - trigger: clients_at_risk > 3
    decision: STOP
    action: Stop new sales, prioritize CS
    evidence_level: L3
    risk_level: Critical
    owner: Head of CS
    due: Immediate
    
  - trigger: clients_at_risk 1-3
    decision: FIX
    action: Immediate intervention for each
    evidence_level: L3
    risk_level: High
    owner: Head of CS
    due: 24 hours
    
  - trigger: clients_at_risk = 0
    decision: CONTINUE
    action: Healthy state, continue
    evidence_level: L3
    risk_level: Low
    owner: Head of CS
    due: None
```

### Rule 4.2: Delivery Blockers

```yaml
Rule ID: DEL_002
Name: Blocker Response
Metric: del_blockers_critical

Conditions:
  - trigger: critical_blockers > 2
    decision: STOP
    action: Escalate to leadership, mobilize resources
    evidence_level: L3
    risk_level: Critical
    owner: Head of Delivery
    due: Immediate
    
  - trigger: critical_blockers 1-2
    decision: FIX
    action: Assign owners, set resolution timeline
    evidence_level: L3
    risk_level: High
    owner: Head of Delivery
    due: 24 hours
    
  - trigger: blockers_open > 5
    decision: FIX
    action: Resource delivery block resolution
    evidence_level: L3
    risk_level: Medium
    owner: Head of Delivery
    due: 72 hours
```

---

## 5. Financial Decision Rules

### Rule 5.1: Cost Per Lead

```yaml
Rule ID: FIN_001
Name: Cost Per Lead Analysis
Metric: fin_cost_per_lead

Conditions:
  - trigger: CPL > budget * 1.5
    decision: STOP
    action: Pause campaign, review targeting
    evidence_level: L3
    risk_level: Critical
    owner: Head of GTM
    due: Immediate
    
  - trigger: CPL > budget
    decision: FIX
    action: Optimize targeting, improve conversion
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: 48 hours
    
  - trigger: CPL < budget
    decision: SCALE
    action: Increase volume
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: 72 hours
```

### Rule 5.2: Customer Acquisition Cost

```yaml
Rule ID: FIN_002
Name: CAC Analysis
Metric: fin_cac (trend)

Conditions:
  - trigger: CAC_increasing > 25%
    decision: FIX
    action: Review entire funnel for efficiency
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: 72 hours
    
  - trigger: CAC_stable
    decision: CONTINUE
    action: Monitor, maintain efficiency
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: None
    
  - trigger: CAC_decreasing
    decision: SCALE
    action: Increase acquisition
    evidence_level: L3
    risk_level: Low
    owner: Head of GTM
    due: 72 hours
```

### Rule 5.3: Payback Period

```yaml
Rule ID: FIN_003
Name: Payback Period Analysis
Metric: fin_payback_period

Conditions:
  - trigger: payback > 18 months
    decision: STOP
    action: Review pricing, increase deal size
    evidence_level: L3
    risk_level: Critical
    owner: CEO
    due: Immediate
    
  - trigger: payback 12-18 months
    decision: FIX
    action: Improve unit economics
    evidence_level: L3
    risk_level: High
    owner: Head of Sales
    due: 72 hours
    
  - trigger: payback < 12 months
    decision: CONTINUE
    action: Healthy, maintain
    evidence_level: L3
    risk_level: Low
    owner: Head of Sales
    due: None
```

---

## 6. Cross-Functional Rules

### Rule 6.1: Sector Performance

```yaml
Rule ID: XFN_001
Name: Sector Performance Response
Metric: Sector-specific metrics

Conditions:
  - trigger: sector_positive_rate > avg * 1.5
    decision: SCALE
    action: Double sector allocation next week
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 72 hours
    
  - trigger: sector_performance < avg * 0.5
    decision: FIX
    action: Review sector strategy, consider pause
    evidence_level: L3
    risk_level: High
    owner: Head of GTM
    due: 48 hours
```

### Rule 6.2: Channel Efficiency

```yaml
Rule ID: XFN_002
Name: Channel Performance Response
Metric: Channel-specific metrics

Conditions:
  - trigger: email_CPL < whatsapp_CPL * 0.5
    decision: SCALE
    action: Shift budget to email
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 72 hours
    
  - trigger: whatsapp_response_rate > email * 2
    decision: SCALE
    action: Increase WhatsApp volume
    evidence_level: L3
    risk_level: Medium
    owner: Head of GTM
    due: 72 hours
```

### Rule 6.3: Agent Quality

```yaml
Rule ID: XFN_003
Name: Agent Quality Response
Metric: agent_safety_gate_failures

Conditions:
  - trigger: safety_gate_failures > 5 in 1 hour
    decision: STOP
    action: Pause agent, review prompt
    evidence_level: L3
    risk_level: Critical
    owner: Head of Engineering
    due: Immediate
    
  - trigger: safety_gate_failures > 10 in 1 day
    decision: FIX
    action: Review safety gate thresholds
    evidence_level: L3
    risk_level: High
    owner: Head of Engineering
    due: 24 hours
```

---

## 7. Rule Implementation

### 7.1 Rule Engine

```python
class DecisionRuleEngine:
    def evaluate(self, metric: str, value: float, context: dict) -> Decision:
        rule = self.get_rule(metric)
        condition = self.match_condition(rule, value)
        
        return Decision(
            rule_id=rule.id,
            metric=metric,
            value=value,
            condition=condition,
            decision=condition.decision,
            action=condition.action,
            evidence_level=condition.evidence_level,
            risk_level=condition.risk_level,
            owner=condition.owner,
            due=condition.due,
            created_at=datetime.utcnow()
        )
```

### 7.2 Escalation Matrix

| Risk Level | Notification | Approval | SLA |
|------------|--------------|----------|-----|
| Critical | Immediate Slack + SMS | Founder | Immediate |
| High | Slack + Email | Founder | 24 hours |
| Medium | Email | Head | 48 hours |
| Low | Dashboard only | Self | 72 hours |

---

**Next:** See `STOP_SCALE_FIX_RULES_AR.md` for consolidated STOP/SCALE/FIX rules.
