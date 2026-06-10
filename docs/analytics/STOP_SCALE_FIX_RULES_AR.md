# Stop Scale Fix Rules — Arabic
## قواعد الإيقاف والتوسع والإصلاح

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. STOP Rules — قواعد الإيقاف

STOP = Immediate halt required. Execute immediately without waiting for approval.

### 1.1 Safety Stops

| Metric | Trigger | Action | Auto-Execute |
|--------|---------|--------|--------------|
| safety_gate_failures | > 5/hour | Pause agent, alert CS | YES |
| pii_detected_in_logs | Any occurrence | Stop logging, alert | YES |
| compliance_blocked | > 10/hour | Pause outreach | YES |
| data_breach_indicators | Any | Stop all data ops | YES |

### 1.2 Quality Stops

| Metric | Trigger | Action | Auto-Execute |
|--------|---------|--------|--------------|
| bounce_rate | > 10% | Pause all email | YES |
| spam_complaints | > 5/day | Pause sending | YES |
| unsubscribe_rate | > 2% | Review list quality | NO |
| hard_bounce_rate | > 3% | Clean list immediately | NO |

### 1.3 Business Stops

| Metric | Trigger | Action | Auto-Execute |
|--------|---------|--------|--------------|
| delivery_blockers_critical | > 3 | Escalate, mobilize | NO |
| clients_at_risk | > 5 | Stop new sales | NO |
| payback_period | > 24 months | Review pricing | NO |
| CAC | > 3x target | Pause acquisition | NO |

---

## 2. SCALE Rules — قواعد التوسع

SCALE = Increase investment. Requires Founder approval within 48 hours.

### 2.1 Growth Scaling

| Metric | Trigger | Action | Evidence Level |
|--------|---------|--------|----------------|
| reply_rate | > 10% + positive > 40% | Double volume | L3 |
| close_rate | > 25% | Increase pipeline | L3 |
| CAC | Decreasing > 20% | Increase acquisition | L3 |
| sector_performance | > 1.5x average | Double sector allocation | L3 |
| tool_ROI | > 200% | Increase tool budget | L3 |

### 2.2 Performance Scaling

| Metric | Trigger | Action | Evidence Level |
|--------|---------|--------|----------------|
| email_CPL | < 50% of target | Increase email budget | L3 |
| whatsapp_response | > 2x email | Shift to WhatsApp | L3 |
| meeting_rate | > 50% of positive | Add sales capacity | L3 |
| renewal_rate | > 90% | Expand CS team | L3 |

### 2.3 Scaling Thresholds

```
SCALE when:
  - Metric exceeds target by > 50%
  - Trend is consistent (> 2 weeks)
  - Evidence level is L3 or higher
  - No counter-indicators
```

---

## 3. FIX Rules — قواعد الإصلاح

FIX = Address issue. Requires action within 48 hours.

### 3.1 GTM Fixes

| Metric | Trigger | Action | Owner |
|--------|---------|--------|-------|
| reply_rate | < 5% | Review targeting | Head of GTM |
| positive_rate | < 20% | Review message quality | Head of GTM |
| meeting_rate | < 30% | Improve CTA/booking | Head of Sales |
| close_rate | < 15% | Review proposal/offer | Head of Sales |
| approval_delay | > 24 hours | Streamline approval | Founder |

### 3.2 Quality Fixes

| Metric | Trigger | Action | Owner |
|--------|---------|--------|-------|
| bounce_rate | 5-10% | Clean list | Head of GTM |
| draft_quality | < 70% | Improve templates | Head of GTM |
| QA_failure_rate | > 30% | Review QA process | Head of QA |
| rework_count | Increasing | Review agent prompts | Head of Engineering |

### 3.3 Commercial Fixes

| Metric | Trigger | Action | Owner |
|--------|---------|--------|-------|
| pipeline_value | Decline > 15% | Increase prospecting | Head of Sales |
| avg_deal_size | Decline > 10% | Review pricing | Head of Sales |
| discount_rate | > 15% | Enforce policy | Head of Sales |
| price_exceptions | Increasing | Review process | Head of Sales |

### 3.4 Delivery Fixes

| Metric | Trigger | Action | Owner |
|--------|---------|--------|-------|
| clients_at_risk | > 0 | Immediate intervention | Head of CS |
| blockers_critical | > 0 | Assign resolution | Head of Delivery |
| weekly_reports_missed | > 20% | Review CS process | Head of CS |
| QBR_attendance | < 80% | Follow-up protocol | Head of CS |

### 3.5 Financial Fixes

| Metric | Trigger | Action | Owner |
|--------|---------|--------|-------|
| CPL | > 1.25x target | Optimize targeting | Head of GTM |
| CAC | Increasing > 15% | Review funnel | Head of GTM |
| tool_cost | > 15% of revenue | Review tool stack | Head of Ops |
| founder_time | > 20 hrs/week on review | Automate reporting | Founder |

---

## 4. Decision Matrix

### 4.1 GTM Decision Matrix

| Metric | < Threshold | Threshold-Normal | Normal-Good | > Excellent |
|--------|-------------|------------------|------------|-------------|
| bounce_rate | STOP | FIX | CONTINUE | SCALE |
| reply_rate | FIX | CONTINUE | SCALE | SCALE |
| positive_rate | FIX | CONTINUE | SCALE | SCALE |
| meeting_rate | FIX | FIX | CONTINUE | SCALE |
| close_rate | FIX | CONTINUE | CONTINUE | SCALE |

### 4.2 Commercial Decision Matrix

| Metric | < Threshold | Threshold-Normal | Normal-Good | > Excellent |
|--------|-------------|------------------|------------|-------------|
| pipeline_value | STOP | FIX | CONTINUE | SCALE |
| avg_deal_size | FIX | CONTINUE | CONTINUE | SCALE |
| discount_rate | STOP | FIX | CONTINUE | CONTINUE |
| win_rate | FIX | CONTINUE | SCALE | SCALE |

### 4.3 Delivery Decision Matrix

| Metric | < Threshold | Threshold-Normal | Normal-Good | > Excellent |
|--------|-------------|------------------|------------|-------------|
| clients_at_risk | STOP | FIX | CONTINUE | CONTINUE |
| blockers_critical | STOP | FIX | CONTINUE | CONTINUE |
| health_score | FIX | CONTINUE | CONTINUE | SCALE |
| renewal_rate | FIX | FIX | CONTINUE | SCALE |

### 4.4 Financial Decision Matrix

| Metric | < Threshold | Threshold-Normal | Normal-Good | > Excellent |
|--------|-------------|------------------|------------|-------------|
| CPL | STOP | FIX | CONTINUE | SCALE |
| CAC | STOP | FIX | CONTINUE | SCALE |
| payback_period | STOP | FIX | CONTINUE | SCALE |
| tool_cost_% | FIX | FIX | CONTINUE | SCALE |

---

## 5. Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════════╗
║                    FOUNDER QUICK DECISION GUIDE                  ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🔴 STOP IMMEDIATELY (Auto-execute where marked)                  ║
║  • Bounce rate > 10% → Pause all email                           ║
║  • Safety gate failures > 5/hour → Pause agent                    ║
║  • Critical blockers > 3 → Escalate immediately                  ║
║  • Clients at risk > 5 → Stop new sales                           ║
║  • CAC > 3x target → Pause acquisition                           ║
║  • Payback > 24 months → Review pricing                           ║
║                                                                   ║
║  🟢 SCALE (Get approval within 48 hours)                          ║
║  • Reply rate > 10% + positive > 40% → Double volume             ║
║  • CAC decreasing > 20% → Increase acquisition                   ║
║  • Sector outperforming 1.5x → Double allocation                  ║
║  • Close rate > 25% → Increase pipeline                           ║
║                                                                   ║
║  🟡 FIX (Action within 48 hours)                                 ║
║  • Reply rate < 5% → Review targeting                            ║
║  • Pipeline declining > 15% → Increase prospecting               ║
║  • Clients at risk > 0 → Immediate intervention                 ║
║  • CPL > 1.25x target → Optimize targeting                       ║
║                                                                   ║
║  🔵 CONTINUE (Monitor only)                                      ║
║  • Metrics within normal range                                   ║
║  • Stable trends                                                 ║
║  • No immediate action required                                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 6. Threshold Defaults

| Metric | STOP | FIX | CONTINUE | SCALE |
|--------|------|-----|----------|-------|
| bounce_rate | >10% | 5-10% | 2-5% | <2% |
| reply_rate | <1% | 1-5% | 5-10% | >10% |
| positive_rate | <10% | 10-20% | 20-40% | >40% |
| meeting_rate | <15% | 15-30% | 30-50% | >50% |
| close_rate | <5% | 5-15% | 15-25% | >25% |
| clients_at_risk | >5 | 1-5 | 0 | 0 |
| CAC_trend | +50% | +15-50% | ±15% | -15% |
| pipeline_trend | -30% | -15-30% | ±15% | +15% |

---

**Next:** See `EXPERIMENTATION_SYSTEM_AR.md` for A/B testing framework.
