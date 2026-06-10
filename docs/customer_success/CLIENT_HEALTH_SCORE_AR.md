# Client Health Score — نقاط صحة العميل
**Dealix — Agent #3**

> **الغرض:** درجة صحية (0-100) لكل عميل، 8 مكونات، tiers، وإجراءات لكل tier.

---

## 1. The 8 Components

### 1.1 Onboarding Complete (10 pts)
- **0:** not started
- **5:** in progress
- **10:** complete

### 1.2 Access Complete (10 pts)
- **0:** no access
- **5:** partial
- **10:** full

### 1.3 First Workflow Delivered (15 pts)
- **0:** not started
- **5:** in design
- **10:** in test
- **15:** in production

### 1.4 Weekly Report Delivered (10 pts)
- **0:** no report
- **5:** missed last week
- **10:** on schedule

### 1.5 Client Engagement (15 pts)
- **0:** no response
- **5:** low (slow replies)
- **10:** medium (engaged)
- **15:** high (active)

### 1.6 Value Proof (15 pts)
- **0:** no metric
- **5:** metric identified
- **10:** metric tracked
- **15:** metric achieved

### 1.7 Unresolved Risks (15 pts)
- **0:** multiple critical
- **5:** 1 critical
- **10:** 1-2 medium
- **15:** none

### 1.8 Renewal Fit (10 pts)
- **0:** no path
- **5:** possible
- **10:** clear path

---

## 2. Total Score

| Score | Tier | Color | Action |
|-------|------|-------|--------|
| 80+ | Healthy | Green | Continue |
| 60-79 | Attention | Yellow | Founder attention |
| 40-59 | At Risk | Orange | Escalation |
| < 40 | Critical | Red | Save or exit |

---

## 3. Per-Tier Actions

### 3.1 Green (80+)
- Continue normal cadence
- Look for expansion
- Reference request (with permission)

### 3.2 Yellow (60-79)
- Founder check-in
- Address risks
- Increase communication
- Path to Green

### 3.3 Orange (40-59)
- Same-day founder call
- Recovery plan
- Increase support
- Decision: continue or exit

### 3.4 Red (< 40)
- Emergency
- Save attempt or graceful exit
- Refund consideration
- Founder decision

---

## 4. Update Cadence

- **Weekly** (after weekly report)
- **Daily** if at-risk
- **Real-time** if critical
- **Trigger** on any major change

---

## 5. Triggers That Lower Score

- Missed check-in (-5)
- Unresolved issue (-5)
- Negative feedback (-10)
- Usage drop (-5)
- Renewal hesitation (-10)
- Payment late (-5)
- DM change (-5)

---

## 6. Triggers That Raise Score

- Value milestone (+5)
- Expansion interest (+5)
- Positive feedback (+5)
- Reference provision (+5)
- New stakeholder engaged (+5)
- Quick resolution (+2)

---

## 7. The Health Score Record

```yaml
- health_id: "health_001"
- client_id: "client_001"
- date: "2026-06-03"
- onboarding_complete: 10
- access_complete: 10
- first_workflow_delivered: 15
- weekly_report_delivered: 10
- client_engagement: 12
- value_proof: 10
- unresolved_risks: 10
- renewal_fit: 5
- total: 82
- tier: green
- trend: stable
- next_action: "continue_normal_cadence"
- notes: "All on track, expansion opportunity surfaced"
```

---

## 8. Dashboard View

```
┌────────────────────────────────────────────┐
│  Client Health (this week)                 │
│  Green: 5                                  │
│  Yellow: 3                                 │
│  Orange: 1                                 │
│  Red: 0                                    │
│                                            │
│  Top 3 Yellow:                             │
│  - [Client 1]: 65 - usage drop             │
│  - [Client 2]: 70 - renewal hesitate       │
│  - [Client 3]: 68 - unresolved issue       │
└────────────────────────────────────────────┘
```

---

## 9. The Save Plan

### 9.1 When Yellow
- Same-day outreach
- Founder call within 3 days
- Address risks
- Document

### 9.2 When Orange
- Same-day founder call
- Recovery plan within 1 week
- Founder-led recovery
- Decision: continue or exit

### 9.3 When Red
- Emergency escalation
- Save attempt or exit
- Refund consideration
- Founder decision
- Post-mortem

---

## 10. The Exit Plan

### 10.1 When to Exit
- Red for 2+ weeks
- Client refuses to engage
- Legal/compliance issue
- Payment issues
- Mutual decision

### 10.2 Process
- Founder call
- Documentation
- Knowledge transfer
- Final report
- Case study ask (if good)
- Offboarding

---

## 11. Cohort Analysis

Monthly:
- Health by ICP
- Health by offer
- Health by tenure
- Health by owner

---

## 12. Companion Files

- OS: `CUSTOMER_SUCCESS_OS_AR.md`
- First 30: `FIRST_30_DAYS_AR.md`
- Weekly: `WEEKLY_VALUE_REPORT_AR.md`
- Renewal: `RENEWAL_PLAYBOOK_AR.md`
- Expansion: `EXPANSION_PLAYBOOK_AR.md`
- Schema: `schemas/client_health.schema.json`
- Data: `data/customer_success/client_health.jsonl`
- Report: `reports/customer_success/CLIENT_HEALTH_REVIEW.md`

---

**Health score = pulse. كل أسبوع = درجة. founder يراقب، CS ينفّذ، العميل يبقى أو يخرج بكرامة.**
