# Dealix Decision Intelligence — Arabic
## ذكاء قرارات ديلوكس

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

Decision Intelligence transforms raw metrics into actionable decisions for the Founder. Every metric has a corresponding decision rule, and every decision has a clear owner and approval path.

---

## 2. Decision Framework

### 2.1 Decision Types

| Type | Description | Approval Required |
|------|-------------|-------------------|
| STOP | Immediate halt needed | Automated (safety) |
| SCALE | Increase investment | Founder |
| FIX | Address issue | Founder |
| CONTINUE | Maintain current state | None |
| EXPERIMENT | Test new approach | Founder |

### 2.2 Evidence Levels

| Level | Description | Decision Confidence |
|-------|-------------|---------------------|
| L0 | Guess/Hunch | < 30% |
| L1 | Anecdotal | 30-50% |
| L2 | Observed | 50-70% |
| L3 | Measured | 70-85% |
| L4 | Controlled Test | 85-95% |
| L5 | Proven/Validated | > 95% |

### 2.3 Risk Levels

| Level | Threshold | Action |
|-------|------------|--------|
| Critical | Revenue impact > 50K SAR | Immediate escalation |
| High | Significant trend change | 24-hour action |
| Medium | Moderate deviation | Weekly review |
| Low | Minor variance | Monthly review |

---

## 3. Metric-to-Decision Mapping

### 3.1 GTM Decisions

| Metric | Condition | Decision | Action |
|--------|-----------|----------|--------|
| bounce_rate | > 5% | STOP | Pause sending, review list |
| bounce_rate | 2-5% | FIX | Clean list, verify emails |
| bounce_rate | < 2% | CONTINUE | Maintain current |
| reply_rate | > 10% | SCALE | Increase volume |
| reply_rate | 5-10% | CONTINUE | Maintain current |
| reply_rate | < 5% | FIX | Review targeting |
| positive_rate | > 40% | SCALE | Double down on sector |
| positive_rate | 20-40% | CONTINUE | Maintain current |
| positive_rate | < 20% | FIX | Review message quality |
| meeting_rate | > 30% of replies | CONTINUE | Good discovery flow |
| meeting_rate | < 30% of replies | FIX | Improve CTA/discovery |
| close_rate | > 20% | SCALE | Increase pipeline |
| close_rate | 10-20% | CONTINUE | Maintain current |
| close_rate | < 10% | FIX | Review proposal/offer |

### 3.2 Commercial Decisions

| Metric | Condition | Decision | Action |
|--------|-----------|----------|--------|
| pipeline_value | Decreasing > 20% | FIX | Increase prospecting |
| pipeline_value | Stable | CONTINUE | Monitor |
| pipeline_value | Increasing > 20% | SCALE | Increase close capacity |
| avg_deal_size | Decreasing | FIX | Review pricing |
| avg_deal_size | Stable | CONTINUE | Maintain |
| avg_deal_size | Increasing | CONTINUE | Positive signal |
| discount_rate | > 20% | STOP | Review discount policy |
| discount_rate | 10-20% | FIX | Enforce guidelines |
| discount_rate | < 10% | CONTINUE | Good discipline |
| price_exceptions | Increasing | FIX | Review pricing process |

### 3.3 Delivery Decisions

| Metric | Condition | Decision | Action |
|--------|-----------|----------|--------|
| clients_at_risk | > 3 | STOP new sales | Prioritize CS |
| clients_at_risk | 1-3 | FIX | Immediate action |
| blockers_open | > 5 | FIX | Resource delivery |
| blockers_critical | > 2 | STOP | Escalate immediately |
| weekly_reports_missed | > 20% | FIX | Review CS process |

### 3.4 Financial Decisions

| Metric | Condition | Decision | Action |
|--------|-----------|----------|--------|
| cost_per_lead | > budget + 50% | STOP | Review targeting |
| cost_per_lead | > budget | FIX | Optimize process |
| cost_per_lead | < budget | SCALE | Increase volume |
| CAC | Increasing > 20% | FIX | Review funnel |
| CAC | Stable | CONTINUE | Monitor |
| payback_period | > 12 months | STOP | Review pricing |
| payback_period | 6-12 months | FIX | Increase deal size |
| payback_period | < 6 months | SCALE | Aggressive growth |

---

## 4. Decision Output Format

### 4.1 Decision Record

```json
{
  "decision_id": "DEC_20260603_001",
  "metric_trigger": "bounce_rate",
  "trigger_value": 6.5,
  "threshold": 5.0,
  "decision": "STOP",
  "recommendation": "Pause email sending immediately",
  "evidence_level": "L3",
  "risk_level": "High",
  "owner": "Head of GTM",
  "approval_required": "Founder",
  "approved_at": null,
  "due_date": "2026-06-03",
  "status": "pending_approval",
  "created_at": "2026-06-03T07:00:00Z",
  "notes": "Bounce rate spike detected in technology sector"
}
```

---

## 5. Decision Queue

### 5.1 Daily Decision Queue Structure

```
Founder Decision Queue — 2026-06-03

═══════════════════════════════════════════════════════
🔴 STOP DECISIONS (Immediate Action Required)
═══════════════════════════════════════════════════════

1. [HIGH] Email Sending — Bounce Rate Spike
   Metric: bounce_rate = 6.5% (threshold: 5%)
   Action: Pause sending for affected segment
   Evidence: L3 (Measured over 3 days)
   Owner: Head of GTM
   Due: Today

2. [CRITICAL] Delivery Blockers — 3 Critical Blockers
   Metric: blockers_critical = 3
   Action: Escalate to CEO immediately
   Evidence: L2 (Observed)
   Owner: Head of Delivery
   Due: Immediate

═══════════════════════════════════════════════════════
🟡 FIX DECISIONS (Review Within 48 Hours)
═══════════════════════════════════════════════════════

3. [MEDIUM] Reply Rate — Below Target
   Metric: reply_rate = 4.2% (target: 5%)
   Action: Review targeting criteria
   Evidence: L3 (Measured over 7 days)
   Owner: Head of GTM
   Due: 2026-06-05

═══════════════════════════════════════════════════════
🟢 SCALE DECISIONS (Expansion Opportunities)
═══════════════════════════════════════════════════════

4. [MEDIUM] Technology Sector — Outperforming
   Metric: positive_rate = 45% (avg: 30%)
   Action: Increase technology sector allocation
   Evidence: L3 (Measured over 14 days)
   Owner: Head of GTM
   Due: 2026-06-07

═══════════════════════════════════════════════════════
🔵 EXPERIMENT DECISIONS (Testing Opportunities)
═══════════════════════════════════════════════════════

5. [LOW] WhatsApp CTA — Test Different Timing
   Hypothesis: Evening sends outperform morning
   Metric: click_rate
   Owner: Head of GTM
   Due: 2026-06-14

═══════════════════════════════════════════════════════
✓ PENDING APPROVALS
═══════════════════════════════════════════════════════

None currently pending

═══════════════════════════════════════════════════════
✓ RECENTLY APPROVED
═══════════════════════════════════════════════════════

• 2026-06-02: Increase healthcare sector budget (+20%)
• 2026-06-01: New pricing tier for enterprise
```

---

## 6. Decision Automation

### 6.1 Automated Stops

These decisions are AUTOMATICALLY executed without Founder approval:

| Decision | Trigger | Action |
|----------|---------|--------|
| Safety Gate | `agent.action_failed` > 5 in 1 hour | Pause agent |
| Bounce Spike | bounce_rate > 10% | Pause sending |
| Churn Alert | churn_probability > 0.9 | Alert CS |
| Data Breach | PII detected in logs | Stop logging, alert |

### 6.2 Founder-Required Decisions

| Decision Type | Approval Level | SLA |
|---------------|----------------|-----|
| STOP (non-safety) | Founder | 24 hours |
| SCALE | Founder | 48 hours |
| FIX | Founder | 48 hours |
| EXPERIMENT | Founder | 72 hours |

---

## 7. Decision Review

### 7.1 Daily Review
- Founder reviews decision queue by 08:00
- Approve or modify decisions
- Assign owners and due dates

### 7.2 Weekly Review
- Review decision outcomes
- Assess decision accuracy
- Tune thresholds

### 7.3 Monthly Review
- Full decision audit
- Decision accuracy score
- Process improvements

---

## 8. Decision Effectiveness Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| Decisions implemented on time | > 95% | Weekly |
| Decision accuracy | > 80% | Monthly |
| False positives | < 10% | Monthly |
| Decision cycle time | < 24 hours | Weekly |

---

**Next:** See `FOUNDER_DECISION_RULES_AR.md` for detailed rule definitions.
