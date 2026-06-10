# Dealix Analytics OS — Arabic
## نظام تحليلات ديلوكس التشغيلي

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview — نظرة عامة

Dealix Analytics OS هو الطبقة المركزية لتحويل جميع أنشطة ديلوكس إلى قرارات Founder قابلة للتنفيذ.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEALIX ANALYTICS OS                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │
│  │ Event Layer │→ │Metrics Layer│→ │ Decision Intelligence  │   │
│  │ (54 events) │  │ (100+ KPIs) │  │ (Founder Rules Engine)  │   │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  OUTPUT LAYER                               │   │
│  │  Daily Decision • Weekly Review • Funnel Review            │   │
│  │  Decision Queue • Experiment Results • Data Quality        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Principles — المبادئ الأساسية

### 2.1 Event-First Architecture
- كل إجراء ينتج حدث
- الأحداث immutable
- Metrics مشتقة من الأحداث

### 2.2 Privacy by Design
- لا PII في التقارير
- تجميع حسب القطاع/القناة فقط
- تشفير البيانات الحساسة

### 2.3 Decision-Focused
- كل Metric لها قرار مرتبط
- قواعد Stop/Scale/Fix واضحة
- Founder هو صاحب القرار النهائي

---

## 3. Event Taxonomy — تصنيف الأحداث

### 3.1 Event Categories

| الفئة | Count | الوصف |
|-------|-------|-------|
| Lead Lifecycle | 5 | created, qualified, disqualified, enriched, merged |
| Company State | 3 | created, enriched, scored |
| Signals | 3 | detected, expired, confirmed |
| Outreach | 8 | drafted, approved, rejected, sent, bounced, opened, clicked, replied |
| Reply Classification | 2 | received, classified |
| Meetings | 4 | requested, booked, held, no_show |
| Deal Lifecycle | 6 | created, stage_changed, proposal_sent, won, lost, stalled |
| Customer | 6 | onboarded, health_changed, qbr_generated, expansion_detected, churn_predicted, churned |
| Compliance | 6 | consent_recorded, opt_out_received, blocked, dsr_received, dsr_completed |
| Agent Lifecycle | 5 | action_requested, approved, rejected, executed, failed |
| AI Quality | 2 | eval_run, regression_detected |
| Pulse | 1 | published |

### 3.2 Event Envelope

```json
{
  "event_id": "evt_abc123",
  "event_type": "message.sent",
  "customer_id": "cust_xyz",
  "occurred_at": "2026-06-03T10:00:00Z",
  "subject_type": "company",
  "subject_id": "comp_123",
  "payload": {
    "sector": "technology",
    "offer_id": "offer_diagnostic",
    "channel": "email",
    "funnel_stage": "contacted"
  },
  "causation_id": "evt_abc000",
  "correlation_id": "corr_123",
  "actor": "agent_1",
  "schema_version": 1,
  "redacted": false
}
```

---

## 4. Metric Layers — طبقات المؤشرات

### 4.1 GTM Metrics

| Metric | الوصف | Source Event |
|--------|-------|--------------|
| prospects_researched | عدد العملاء المحتملين الذين تم بحثهم | company.scored |
| prospects_qualified | عدد المؤهلين حسب ICP | lead.qualified |
| signals_detected | إشارات السوق المكتشفة | signal.detected |
| drafts_generated | المسودات الناتجة | message.drafted |
| drafts_passed_quality | المسودات التي اجتازت QA | ai.eval_run |
| drafts_approved | المسودات المعتمدة من Founder | message.approved |
| emails_sent | الإيميلات المرسلة | message.sent |
| replies_received | جميع الردود | message.replied |
| positive_replies | الردود الإيجابية | reply.classified |
| meetings_booked | الاجتماعات المحجوزة | meeting.booked |
| proposals_requested | طلبات الاقتراح | deal.proposal_sent |
| won_deals | الصفقات الرابحة | deal.won |

### 4.2 Deliverability Metrics

| Metric | الوصف | Target |
|--------|-------|--------|
| send_volume | حجم الإرسال اليومي | < 500/day |
| bounce_rate | نسبة الارتداد | < 2% |
| unsubscribe_rate | نسبة إلغاء الاشتراك | < 0.5% |
| spam_warning_count | تحذيرات Spam | < 5/week |
| domain_health_status | صحة المجال (0-100) | > 80 |
| suppressed_recipient_count | عدد المحظورين | > 0 |

### 4.3 Reply Classification Metrics

| Reply Type | الوصف |
|------------|-------|
| positive | اهتمام فوري |
| interested_later | مهتم لاحقاً |
| price_question | سؤال عن السعر |
| send_more_info | يريد معلومات إضافية |
| wrong_person | شخص خاطئ |
| unsubscribe | إلغاء اشتراك |
| angry | رد سلبي |
| bounce | بريد مرتد |

### 4.4 WhatsApp Metrics

| Metric | الوصف |
|--------|-------|
| post_reply_sessions | جلسات WhatsApp النشطة |
| readiness_scans_started | scans البدء |
| readiness_scans_completed | scans الاكتمال |
| action_cards_clicked | نقرات على بطاقات الإجراءات |
| human_handoffs | التحويل للإنسان |
| proposal_cards_viewed | مشاهدات الاقتراح |
| payment_handoffs_requested | طلبات الدفع |

### 4.5 Commercial Metrics

| Metric | الوصف |
|--------|-------|
| pipeline_value | قيمة خط الأنابيب |
| qualified_opportunities | الفرص المؤهلة |
| proposal_rate | نسبة الاقتراحات |
| close_rate | نسبة الإغلاق |
| average_deal_size | متوسط حجم الصفقة |
| discount_rate | نسبة الخصم |
| price_exception_count | استثناءات السعر |

### 4.6 Delivery Metrics

| Metric | الوصف |
|--------|-------|
| active_clients | العملاء النشطون |
| onboarding_complete | إكمال onboarding |
| delivery_tasks_completed | المهام المكتملة |
| blockers_open | العوائق المفتوحة |
| weekly_reports_sent | التقارير الأسبوعية |
| acceptance_checkpoints | نقاط القبول |

### 4.7 Customer Success Metrics

| Metric | الوصف |
|--------|-------|
| client_health_score | درجة صحة العميل (0-100) |
| renewal_candidates | مرشحي التجديد |
| churn_risk_count | مخاطر المغادرة |
| expansion_opportunities | فرص التوسع |
| client_escalations | التصعيدات |

### 4.8 Finance Metrics

| Metric | الوصف |
|--------|-------|
| cost_per_draft | التكلفة لكل مسودة |
| cost_per_reply | التكلفة لكل رد |
| cost_per_meeting | التكلفة لكل اجتماع |
| cost_per_proposal | التكلفة لكل اقتراح |
| CAC | تكلفة اكتساب العميل |
| payback_period | فترة استرداد التكلفة |
| gross_margin_by_offer | الهامش حسب العرض |
| tool_cost | تكاليف الأدوات |
| founder_time_cost | تكلفة وقت Founder |

### 4.9 Agent Productivity Metrics

| Metric | الوصف |
|--------|-------|
| agent_tasks_completed | المهام المكتملة |
| files_changed_by_agent | الملفات المعدلة |
| tests_run | الاختبارات |
| safety_gate_failures | فشل Safety Gate |
| rework_count | إعادة العمل |
| collision_count | تعارضات الوكلاء |

---

## 5. Reporting Cadence — دورة التقارير

### 5.1 Daily (Every Morning)
**File:** `reports/analytics/DAILY_DECISION_INTELLIGENCE.md`

```
07:00 - تحديث الأحداث
07:05 - حساب Metrics اليومية
07:10 - تشغيل Decision Rules
07:15 - إنتاج Decision Queue
07:20 - Founder Review
```

### 5.2 Weekly (Every Sunday)
**File:** `reports/analytics/WEEKLY_ANALYTICS_REVIEW.md`

```
Funnel Performance
  - Conversion rates by stage
  - Sector performance
  - Channel performance

Commercial Health
  - Pipeline value changes
  - Win/loss analysis
  - Pricing compliance

Operational Metrics
  - Agent productivity
  - Quality metrics
  - Tool costs

Decisions Required
  - Campaign adjustments
  - Resource reallocation
  - Experiment decisions
```

### 5.3 Real-Time Monitoring
- Safety gate failures → Immediate alert
- Bounce rate spike → Pause sending
- Churn prediction → Customer success escalation

---

## 6. Data Quality Gates — بوابات جودة البيانات

### 6.1 Required Fields
- `sector` — Always required
- `offer_id` — Required for deal events
- `funnel_stage` — Required for all events
- `evidence_level` — Required (L0-L5)
- `approval_status` — Required for outreach events

### 6.2 Validation Rules
1. No duplicate prospect (dedupe on email_domain + company_name)
2. No suppressed prospect in send list
3. Funnel stage progression only (no backward jumps except to nurture)
4. All timestamps in UTC

---

## 7. Privacy Requirements — متطلبات الخصوصية

### 7.1 PII Handling
- Email addresses: Hash in events, redact in reports
- Phone numbers: Mask all but last 4 digits
- Names: Use company names only, no personal names
- Financial data: Aggregate only, no per-deal amounts in Founder reports

### 7.2 Data Retention
- Raw events: 90 days
- Aggregated metrics: Indefinite
- Decision logs: 2 years
- Audit logs: 5 years

---

## 8. Implementation Commands

### 8.1 Event Collection
```bash
# Start event collector
python auto_client_acquisition/intelligence_compounding_os/event_collector.py

# Validate event stream
python scripts/validate_event_stream.py

# Check data quality
python scripts/run_data_quality_checks.py
```

### 8.2 Metric Calculation
```bash
# Calculate daily metrics
python scripts/calculate_daily_metrics.py

# Generate decision intelligence
python scripts/generate_decision_queue.py
```

### 8.3 Report Generation
```bash
# Daily decision report
python scripts/generate_daily_decision_report.py

# Weekly analytics review
python scripts/generate_weekly_review.py

# Funnel review
python scripts/generate_funnel_review.py
```

---

## 9. File Structure

```
docs/analytics/
├── DEALIX_ANALYTICS_OS_AR.md           # This document
├── METRIC_DICTIONARY_AR.md             # Complete metric definitions
├── EVENT_TAXONOMY_AR.md                # Extended event taxonomy
├── DATA_QUALITY_POLICY_AR.md           # Data quality policy
├── PRIVACY_AWARE_ANALYTICS_AR.md       # Privacy guidelines
├── DECISION_INTELLIGENCE_AR.md         # Decision framework
├── GTM_FUNNEL_MODEL_AR.md              # GTM funnel
├── REVENUE_FUNNEL_MODEL_AR.md          # Revenue funnel
├── CLIENT_LIFECYCLE_FUNNEL_AR.md       # Client lifecycle
├── FOUNDER_DECISION_RULES_AR.md        # Decision rules
├── STOP_SCALE_FIX_RULES_AR.md          # Stop/Scale/Fix rules
├── EXPERIMENTATION_SYSTEM_AR.md         # A/B testing system
├── DATA_QUALITY_CHECKS_AR.md           # Quality checks
└── ANALYTICS_PRIVACY_REDACTION_AR.md   # Privacy redaction rules

schemas/
├── metric_event.schema.json            # Metric event schema
├── funnel_event.schema.json            # Funnel event schema
├── founder_decision.schema.json        # Decision schema
└── experiment.schema.json              # Experiment schema

data/analytics/
├── events.jsonl                        # Event stream sample
├── funnel_events.jsonl                 # Funnel events
├── founder_decisions.jsonl             # Decision logs
└── experiments.jsonl                   # Experiment results

reports/analytics/
├── ANALYTICS_GAP_AUDIT.md              # Gap audit
├── DAILY_DECISION_INTELLIGENCE.md      # Daily decisions
├── WEEKLY_ANALYTICS_REVIEW.md          # Weekly review
├── DATA_QUALITY_REVIEW.md              # Quality report
├── FUNNEL_REVIEW.md                    # Funnel analysis
├── FOUNDER_DECISION_QUEUE.md           # Decision queue
├── PRIVACY_AWARE_ANALYTICS_REVIEW.md   # Privacy review
├── EXPERIMENT_REVIEW.md                # Experiment results
└── ANALYTICS_FINAL_REPORT.md           # Final report
```

---

## 10. Success Criteria

### 10.1 Founder Outcomes
- [ ] Daily decision report ready by 07:30
- [ ] All metrics calculable from event stream
- [ ] Decision rules cover 90% of common scenarios
- [ ] Zero PII in reports

### 10.2 Operational Outcomes
- [ ] 100+ metrics defined and calculable
- [ ] Funnel conversion visible in real-time
- [ ] Data quality score > 95%
- [ ] Experiment tracking operational

---

**Next:** See `METRIC_DICTIONARY_AR.md` for complete metric definitions.
