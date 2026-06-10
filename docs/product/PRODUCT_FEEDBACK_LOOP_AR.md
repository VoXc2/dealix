# Dealix — حلقة Feedback للمنتج

## المبدأ الأساسي

**كل منتج decision يجب أن يمر عبر العميل.**

حلقة feedback تحول:
- إشارات السوق → قرارات منتج
- Pain points → opportunities
- churn risks → retention wins

---

## مصادر Feedback

### 1. من Pipeline (أعلى الـ funnel)

| المصدر | النوع | الأهمية |
|--------|-------|---------|
| **Replies** | Signal | عالية جداً |
| **Discovery calls** | Insight | عالية |
| **Proposal objections** | Pain | عالية |
| **Demo feedback** | Interest | متوسطة |

### 2. من Delivery (وسط الـ funnel)

| المصدر | النوع | الأهمية |
|--------|-------|---------|
| **Delivery blockers** | Risk | حرجة |
| **Scope changes** | Pain | عالية |
| **Quality issues** | Risk | عالية |
| **Timeline delays** | Risk | متوسطة |

### 3. من Success (أسفل الـ funnel)

| المصدر | النوع | الأهمية |
|--------|-------|---------|
| **Renewal reasons** | Value | عالية جداً |
| **Churn risks** | Alert | حرجة |
| **Upsell opportunities** | Revenue | عالية |
| **Referral signals** | Growth | عالية |

### 4. من السوق

| المصدر | النوع | الأهمية |
|--------|-------|---------|
| **Partner feedback** | Signal | متوسطة |
| **Competitor moves** | Context | متوسطة |
| **Founder decisions** | Strategic | عالية |

---

## هيكل Feedback Item

كل feedback يجب أن يتضمن:

```json
{
  "id": "feedback_001",
  "source": "reply | discovery_call | proposal_objection | delivery_blocker | success_report | renewal | churn_risk | partner_feedback | founder_decision",
  "quote_summary": "النص أو الملخص",
  "affected_module": "control_room | gtm_factory | approval_queue | reply_handling | portal | handoff | reports | renewal | metrics",
  "revenue_impact": "high | medium | low | none",
  "urgency": "critical | high | medium | low",
  "evidence_level": "high | medium | low",
  "product_decision": "build | backlog | do_not_build | investigate",
  "decision_date": "2026-01-15",
  "decided_by": "founder | product_manager"
}
```

---

## مستويات Evidence

| المستوى | الوصف | مثال |
|---------|-------|------|
| **High** | متكرر من مصادر متعددة | 3+ عملاء طلبوا نفس الشيء |
| **Medium** | واضح من مصدر واحد | عميل واحد أوضح pain بوضوح |
| **Low** | إشارة غامضة | mention في conversation |

---

## Process

### Phase 1: الجمع (Continuous)

```
1.1 Team members يسجلون feedback في real-time
1.2 System يجمع من:
    - CRM notes
    - Call recordings
    - Email threads
    - Slack/WhatsApp
    - Meeting notes
1.3 Automated alerts لـ critical feedback
```

### Phase 2: التحليل (Weekly)

```
2.1 Product manager يراجع كل feedback
2.2 يسجل في: data/product/feedback.jsonl
2.3 يجمعimilar feedback
2.4 يحدد patterns
2.5 يقيّم الأثر
```

### Phase 3: التصنيف (Bi-weekly)

```
3.1 Product review meeting
3.2 كل feedback يُصنف:
    - Build now (P0)
    - Backlog (P1-P2)
    - Do not build (P3-P5)
    - Investigate more
3.3 موافقة founder على P0
```

### Phase 4: التنفيذ (Sprint-based)

```
4.1 Build items يضاف للـ sprint
4.2 Progress يتتبع أسبوعياً
4.3 Stakeholders يُبلغون بالقرارات
4.4闭环: نتائج تُغذي next feedback
```

---

## Decision Framework

### Build Now (P0-P1)

| Condition | Decision |
|-----------|----------|
| High evidence + High revenue impact | Build now |
| Critical + Churn risk | Build now |
| 3+ customers same request | Build now |

### Backlog (P2-P3)

| Condition | Decision |
|-----------|----------|
| Medium evidence + Medium impact | Backlog |
| Good idea but no urgency | Backlog |
| Complex but valuable | Backlog |

### Do Not Build (P4-P5)

| Condition | Decision |
|-----------|----------|
| Low evidence + High risk | Do not build |
| No customer signal | Do not build |
| Outside ICP | Do not build |
| Technical complexity > value | Do not build |

---

## Governance

### Weekly Product Review

** attendees: ** Founder + Product + Engineering lead

**Agenda:**
1. Review new feedback (15 min)
2. Discuss patterns (15 min)
3. Make decisions (15 min)
4. Update backlog (15 min)

### Monthly Roadmap Review

** attendees: ** Full team

**Agenda:**
1. Review feedback trends
2. Assess backlog health
3. Prioritize for next month
4. Communicate decisions

---

##闭环 (Closed Loop)

### مهم: كل قرار يُرجع للعميل

```
1. Decision made
2. Communicate to relevant customers
3. Track impact of decision
4. Measure if pain was solved
5. Close loop with data
```

### Example:

```
Customer: "أبي weekly reports"
↓ Feedback logged
↓ Prioritized as P1
↓ Built in Sprint 3
↓ Reports deployed
↓ Customer gets reports
↓ Feedback: "ممتاز! هذه بالضبط ما أحتاج"
↓ Closed loop
```

---

## Reporting

### Weekly Feedback Report

```markdown
## Feedback Summary - Week 4

### New Feedback: 12 items
- 5 from pipeline
- 4 from delivery
- 3 from success

### Patterns Identified:
1. 3 customers want WhatsApp integration
2. 2 customers requested sector-specific reports
3. 1 customer flagged data privacy concern

### Decisions Made:
- WhatsApp: Backlog (P2) - needs consent flow
- Sector reports: Backlog (P2) - lower priority
- Data privacy: Build now (P1) - compliance risk

### Actions:
- [ ] Start consent flow design
- [ ] Update security documentation
- [ ] Communicate decisions to customers
```

---

## _links

- Product Strategy: `PRODUCT_STRATEGY_AR.md`
- Feature Prioritization: `FEATURE_PRIORITIZATION_AR.md`
- Release Criteria: `RELEASE_CRITERIA_AR.md`
- Data: `data/product/feedback.jsonl`
