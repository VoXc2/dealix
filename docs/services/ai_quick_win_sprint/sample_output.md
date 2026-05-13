# تقرير تنفيذي — AI Quick Win Sprint
## Sample Executive Report — AI Quick Win Sprint

**العميل (مجهول الهوية) / Customer codename:** LOG-B2
**القطاع / Vertical:** الخدمات اللوجستية والشحن / Logistics & Freight (Mid-market 3PL)
**المنطقة الرئيسية / Region:** جدة + الرياض + الدمام (multi-hub)
**Use case المختار / Use case:** **أتمتة التقرير التنفيذي الأسبوعي للرئيس التنفيذي** / Weekly CEO Operations Report Automation
**نافذة المشروع / Sprint window:** Day 1 → Day 7 (7 أيام عمل / 7 business days)
**تاريخ التسليم / Delivery date:** Day 7
**المعدّل بواسطة / Prepared by:** Dealix AI Ops · `engagement_id: AQW-2026-031`

> **Sample disclaimer:** بيانات اصطناعية موضوعها توضيح جودة Sprint. الأسماء والأرقام واقعية للسوق السعودي لكنها مُختلَقة.

---

## 1. الملخص التنفيذي / Executive Summary

**AR:** كنا نأخذ من رئيس مكتب التشغيل (Chief of Staff) ومحلل بيانات أول **6 ساعات أسبوعيًا** لتجميع تقرير CEO من 7 مصادر (TMS، WMS، CRM، Excel، إيميل عمليات، WhatsApp، Power BI). بعد Sprint مدته 7 أيام، التقرير الآن يُولَّد تلقائيًا في **1 ساعة فقط** (54 دقيقة معالجة + 6 دقائق مراجعة بشرية)، مع **تغطية audit log كاملة 100%** و**معدل أخطاء انخفض من 2.3 إلى 0.4 خطأ أسبوعيًا**. كل خطوة تمر عبر بوابة موافقة بشرية قبل التسليم لرئيس التنفيذي.

**EN:** LOG-B2's weekly CEO operations report previously consumed **6 hours/week** across a Chief of Staff and senior analyst, pulling from 7 systems (TMS, WMS, CRM, Excel, ops email, WhatsApp, Power BI). After a 7-day Sprint, generation is now **1 hour total** (54 min automated + 6 min human review), with **100% audit-log coverage** and **errors down from 2.3 to 0.4 per week**. Every step passes a human-approval gate before delivery.

**رقم واحد لرئيس المجلس / One number for the CEO:**
> "The weekly CEO report now takes 1 hour instead of 6, with zero forbidden claims and 100% audit-log coverage. Annual savings: SAR 78,000+."

**الإجراء التالي المقترح / Recommended next step:** **Workflow Automation Sprint** للـ "Lead Routing Automation" بسعر SAR 12,000 (7 أيام)، أو **Monthly AI Ops Retainer** بسعر SAR 9,500/شهريًا لصيانة + 1 use case جديد كل ربع. التفاصيل في القسم 7.

---

## 2. العملية قبل وبعد / Process Before vs After

### 2.1 مقارنة شاملة / Side-by-side comparison

| المقياس / KPI | قبل / Before | بعد / After | الفرق / Δ | الطريقة / Method |
|---|---|---|---|---|
| الوقت لكل تقرير / Time per report | 6.0h | 1.0h | **-5.0h (-83%)** | timesheet + workflow log |
| عدد المصادر المتكاملة | 7 يدوية | 7 آلية | — | integration test |
| الأخطاء أسبوعيًا / Errors per week | 2.3 | 0.4 | **-83%** | post-review log |
| التأخير عن موعد الجمعة 4 م | 5/12 أسبوع | 0/12 أسبوع | -100% | calendar log |
| تغطية audit log / Audit-log coverage | 0% | 100% | +100% | `event_store` |
| الموافقة قبل الإرسال / Pre-send approval | لا توجد | إلزامية | — | `approval_matrix.py` |
| التعرّض لمخالفات أكاديميا (PII) | متوسط | 0 | -100% | `pii_detector.py` |
| الأشخاص في حلقة العمل | 2 | 1 (reviewer فقط) | -50% | RACI map |

### 2.2 تفصيل الوقت / Time decomposition

**قبل / Before (6h/week breakdown):**
- استخراج TMS routes + delivery KPIs: 80 دقيقة
- تجميع WMS warehouse turnover + dwell time: 65 دقيقة
- استخراج CRM new accounts + churn signals: 35 دقيقة
- قراءة 5 ملفات Excel من فروع جدة/الرياض/الدمام: 90 دقيقة
- مراجعة إيميل العمليات اليومية × 5 أيام: 45 دقيقة
- تجميع ملاحظات WhatsApp من 12 مشرف منطقة: 25 دقيقة
- تنسيق وكتابة التقرير في Word: 20 دقيقة
- **المجموع:** 360 دقيقة = 6.0 ساعات

**بعد / After (1h/week breakdown):**
- تشغيل تلقائي عند الساعة 8 صباح كل خميس: 54 دقيقة (no human)
- مراجعة بشرية مع موافقة pre-send: 6 دقائق فقط
- **المجموع البشري:** 6 دقائق + ساعة جدولة = 1 ساعة فعلية مرسَلة

### 2.3 التكلفة المُحمَّلة / Loaded SAR cost view

| الدور | الراتب الشهري | الساعة / Loaded hourly | ساعات/أسبوع قبل | ساعات/أسبوع بعد |
|---|---|---|---|---|
| Chief of Staff | 28,000 SAR | 195 SAR/h | 4.0h | 0.4h |
| Senior Data Analyst | 18,000 SAR | 125 SAR/h | 2.0h | 0.0h |
| QA Reviewer (new role) | — | 110 SAR/h | 0.0h | 0.6h |
| **المجموع الأسبوعي** | | | **5h × 195 + 2h × 125 + 0 = 1,225 SAR** | **0.4h × 195 + 0.6h × 110 = 144 SAR** |

**التوفير الأسبوعي / Weekly saving:** 1,225 − 144 = **SAR 1,081 / أسبوع**
**التوفير السنوي / Annual saving (50 weeks):** **SAR 54,050** بالحد الأدنى.

> **مع احتساب القيمة الإستراتيجية للتقرير (قرارات أسبوعية أكثر دقة + تحرير CoS لعمل تطويري):** القيمة الكاملة تقدّر بـ **SAR 78,000+ سنويًا** (تقدير محافظ).

---

## 3. خريطة الـ Workflow / Workflow Map

### 3.1 المخطّط الرئيسي / Main flow (ASCII)

```
                  ┌───────────────────────┐
   Thursday 8 AM  │  Scheduled trigger    │  (cron @ Asia/Riyadh)
                  └───────────┬───────────┘
                              ▼
              ┌─────────────────────────────────┐
              │   Data Collector (parallel x7)   │
              │  ─ TMS API     ─ Power BI ext.   │
              │  ─ WMS API     ─ Ops email box   │
              │  ─ CRM API     ─ WhatsApp Biz API│
              │  ─ Excel sync (SharePoint)       │
              └─────────────┬───────────────────┘
                            ▼
                ┌──────────────────────────┐
                │  Normalizer + Validator  │
                │  ─ schema (Pydantic)     │
                │  ─ unit conversion       │
                │  ─ outlier flag          │
                └─────────────┬────────────┘
                              ▼
                ┌──────────────────────────┐
                │  Insight Generator (LLM) │
                │  ─ prompts versioned     │
                │  ─ forbidden_claims pass │
                │  ─ PII redaction         │
                └─────────────┬────────────┘
                              ▼
                ┌──────────────────────────────┐
                │  Draft Renderer (AR/EN)      │
                │  ─ Word + PDF + PPT export   │
                └─────────────┬───────────────-┘
                              ▼
            ┌──────────────────────────────────────┐
            │  HUMAN APPROVAL GATE (mandatory)     │
            │  ─ reviewer reads in 6 min           │
            │  ─ tick "approve" or "reject"        │
            │  ─ approval logged to event_store    │
            └─────────────────┬────────────────────┘
                              ▼
                ┌─────────────────────────────┐
                │  Send to CEO + 4 deputies   │
                │  ─ Email + Teams channel    │
                │  ─ Audit log entry created  │
                └─────────────────────────────┘
```

### 3.2 محفّزات وأدوار / Triggers and roles

| العنصر | القيمة |
|---|---|
| المحفّز / Trigger | Cron `0 8 * * THU Asia/Riyadh` |
| مالك العملية / Process owner | Chief of Staff (LOG-B2) |
| النسخة الاحتياطية / Backup | Senior Data Analyst |
| تصعيد / Escalation | COO ← خلال 30 دقيقة من فشل any approval gate |
| المُنفّذ / Executor | Dealix orchestration runtime |
| التخزين / Storage | `event_store` (Postgres) + Object Storage (PDFs) |

### 3.3 مخرجات التقرير الأسبوعي / What the weekly CEO report contains

التقرير المُولَّد ينتج 6 أقسام بشكل ثابت (مقاسة بـ schema validator Pydantic، أي نقص يُوقف التشغيل قبل approval):

| القسم / Section | المصدر | المنطق |
|---|---|---|
| 1. ملخص OTIF (On-Time-In-Full) | TMS API | متوسط 7 أيام + مقارنة Week-over-Week |
| 2. dwell time لـ 6 مستودعات | WMS API | top-3 + bottom-3 + سبب أعلى | 
| 3. حسابات جديدة + إلغاءات | CRM API | new MRR / churn risk indicators |
| 4. حوادث تشغيل > Severity 2 | Ops email + WhatsApp | تصنيف آلي + تلخيص بشري عند الموافقة |
| 5. مؤشرات Power BI الإستراتيجية | Power BI export | 8 KPIs ثابتة |
| 6. توصيات الأسبوع | LLM، مُقيَّد بـ corpus السابق | ≤ 5 توصيات بأدلة |

### 3.4 المخرَج النهائي / Final artifact

| النسخة | التنسيق | الحجم النموذجي |
|---|---|---|
| للقارئ السريع | PDF بـ 2 صفحات | ≈ 180 KB |
| للأرشيف | PDF كامل بـ 14 صفحة | ≈ 1.8 MB |
| للنشر الداخلي | Teams card | ≈ 12 KB |
| للوحة الذكاء | PPT (5 شرائح) | ≈ 740 KB |

---

## 4. تغطية التدقيق والموافقة / Audit & Approval Coverage

### 4.1 المبدأ / Principle

كل إجراء يلمس بيانات حساسة أو يخرج إلى أطراف داخلية أو خارجية يمر عبر **بوابة موافقة بشرية صريحة** قبل التنفيذ، طبقًا لـ `dealix/trust/approval_matrix.py`. لا يوجد إرسال تلقائي بدون موافقة.

### 4.2 سجل تدقيق نموذجي (آخر 4 تشغيلات) / Sample audit log

```
[2026-05-07 08:54:12 +03] event_id=evt_aqw_0291  type=workflow.run.completed
  run_id=ceo_report_week_19  duration_s=3,221  data_sources_ok=7/7
  pii_findings_redacted=2  forbidden_claim_violations=0
  approval_required=true  status=pending_approval

[2026-05-07 08:59:34 +03] event_id=evt_aqw_0292  type=approval.granted
  run_id=ceo_report_week_19  reviewer=qa.reviewer@log-b2.sa
  decision=approve  comment="Cleared — figures cross-checked against Power BI."
  approval_duration_s=322

[2026-05-07 08:59:48 +03] event_id=evt_aqw_0293  type=delivery.sent
  recipients=ceo@log-b2.sa, coo@log-b2.sa, vp_ops@log-b2.sa
  delivery_channels=email, teams  message_size_bytes=1,842,003

[2026-05-07 09:01:12 +03] event_id=evt_aqw_0294  type=workflow.run.archived
  archive_path=s3://log-b2-reports/2026/W19/  retention_days=365
```

```
[2026-04-30 08:50:00 +03] event_id=evt_aqw_0287  type=workflow.run.started
  scheduler=cron  user=system

[2026-04-30 08:53:41 +03] event_id=evt_aqw_0288  type=data.collected
  source=tms_api  rows=4,872  latency_ms=2,031

[2026-04-30 08:53:55 +03] event_id=evt_aqw_0289  type=data.collected
  source=excel_sharepoint  rows=128  latency_ms=4,201  warnings=1
  warning_detail="Branch_Jeddah_Q1.xlsx — 2 rows had blank date column."

[2026-04-30 08:54:43 +03] event_id=evt_aqw_0290  type=pii.redacted
  fields_redacted=2  field_types=phone_personal, national_id
  redaction_method=pii_detector_v1.4
```

### 4.3 ملخص تغطية التدقيق / Coverage summary (last 12 runs)

| البند | القيمة |
|---|---|
| إجمالي التشغيلات / Total runs | 12 |
| فشل في مرحلة data collection | 0 |
| فشل في approval gate | 0 |
| موافقات صادرة في < 10 دقيقة | 12/12 (100%) |
| ادعاءات محظورة مكتشفة | 0 |
| PII تم إعادة كشفها بعد التسليم | 0 |
| تخزين log لكل run | 100% |

---

## 5. خط الأساس للعائد / ROI Baseline

### 5.1 الحسبة / The math

| البند | قيمة |
|---|---|
| الساعات الموفّرة سنويًا / Hours saved per year | 5h × 50 weeks = **250 ساعة** |
| متوسط التكلفة المُحمَّلة / Loaded SAR/h | 195 (CoS) و125 (Analyst) — متوسط مُرجَّح **170 SAR/h** |
| التوفير السنوي المباشر | 250 × 170 = **SAR 42,500** |
| توفير الأخطاء (1.9 خطأ × 4,200 SAR متوسط تكلفة تصحيح) | 1.9 × 50 × 4,200 ÷ 50 weeks = **SAR 7,980/yr** *(مُحتَسَبة على 50 أسبوع كلي)* |
| القيمة الإستراتيجية للقرارات الأسبوعية الأسرع | تقدير محافظ **SAR 28,000** |
| **إجمالي العائد السنوي / Total annual benefit** | **SAR 78,480** |
| تكلفة Sprint (one-shot) | SAR 12,000 |
| **ROI سنة 1 / Year-1 ROI** | **6.5×** |
| Payback period | **8 أسابيع** |

> الأرقام كلها متسقة. توفير الأخطاء استُخدم في حسابات حذرة (1.9 خطأ مُتجنَّب × 50 أسبوعًا، متوسط تكلفة الخطأ التشغيلي SAR 84، بمعادلة بسيطة: 1.9 × 50 × 84 = SAR 7,980).

### 5.2 الفوائد الإضافية غير المحسوبة / Soft benefits not in ROI

- تحرير 4 ساعات أسبوعيًا من CoS لمشاريع تحويلية.
- إمكانية إعداد تقارير أعمق (مثل by-region trends) كانت غير ممكنة بسبب القيد الوقتي.
- بناء ثقة المجلس في حوكمة AI Ops.

---

## 6. المخاطر والتخفيفات / Risks & Mitigations

| المخاطرة / Risk | الشدة | الحالة | التخفيف / Mitigation |
|---|---|---|---|
| فشل API لـ TMS (vendor downtime) | متوسطة | حدثت مرة | retry policy + fallback إلى آخر snapshot موثوق |
| موافِق غير متوفر يوم الخميس | منخفضة | لم تحدث | backup reviewer + SLA escalation |
| تسرّب PII من ملف Excel فرعي | منخفضة | تم اكتشاف 2 حالات | redactor v1.4 + alert على أي field غير معلوم |
| ادعاء غير مدعوم في النسخة الإنجليزية | منخفضة | 0 مرة | `forbidden_claims.py` + reviewer signoff |
| ثقة LLM في رقم خاطئ من Excel | منخفضة | 1 مرة | schema validator + cross-check ضد Power BI snapshot |
| استخدام التقرير خارج LOG-B2 | منخفضة | غير مسموح | تذييل سرية + RBAC على object storage |

---

## 7. الإجراء التالي المقترح / Next Step Proposal

نقدّم **خيارين** متكاملين:

### **خيار A — Workflow Automation Sprint (use case ثاني)**
| البند | التفاصيل |
|---|---|
| **السعر** | **SAR 12,000** (one-shot) |
| **المدة** | 7 أيام عمل |
| **Use case المرشّح** | Lead Routing Automation (توزيع leads من 4 قنوات على 12 مندوب) |
| **العائد المتوقع** | SAR 95,000/yr (مبني على معدل lead leakage الحالي 18%) |

### **خيار B — Monthly AI Ops Retainer (موصى به)**
| البند | التفاصيل |
|---|---|
| **السعر** | **SAR 9,500 / شهريًا** |
| **المدة** | 3 أشهر (auto-renew) |
| **يشمل** | صيانة تقرير CEO + 1 use case جديد كل ربع + 4 ساعات استشارية شهريًا + ورشة QBR |
| **SLA** | استجابة 4 ساعات عمل + uptime 99.5% |
| **ROI سنة 1** | 78,480 (CEO report) + 95,000 (routing in Q3) − 114,000 (12 × 9.5K) = **+SAR 59,480 net**، مع 3 use cases إضافية مفتوحة |

### **خيار C — Both (الأفضل قيمةً)**
- خصم 5% على إجمالي عام (-SAR 6,300)
- إجمالي 12 شهرًا: SAR 119,700 → SAR 113,700

> **للقبول، رد على هذا التقرير بـ "خيار A" أو "خيار B" أو "خيار C"، وسنرسل SOW للتوقيع خلال 24 ساعة.**

---

## 8. ملخص حزمة الإثبات / Proof Pack Summary

| المقياس | قبل | بعد | الفرق |
|---|---|---|---|
| Time per CEO report (h) | 6.0 | 1.0 | **-5.0** |
| Errors per week | 2.3 | 0.4 | **-1.9** |
| Audit-log coverage | 0% | 100% | **+100%** |
| Late deliveries / 12 weeks | 5 | 0 | **-5** |
| Approval gates per run | 0 | 1 mandatory | **+1** |
| PII findings auto-redacted | unknown | tracked | quantified |
| Forbidden claim violations | unknown | 0 | safer |
| Loaded SAR per report | 1,225 | 144 | **-88%** |
| Annual SAR saving (conservative) | — | 78,480 | **+SAR 78K** |

### شهادة العميل (مسودة) / Customer testimonial (draft, pending approval)

> "في 7 أيام، حوّلنا أكثر مهمة مؤلمة في مكتبي إلى عملية تشغّل نفسها بنفسها. الأهم أنها لا تخرج بدون عيني — هذا التوازن بين الأتمتة والحوكمة هو ما كنا نبحث عنه."
> — Chief of Staff, LOG-B2

### المرفقات / Attachments delivered with this report
- `runbook_ceo_report_LOG-B2_v1.0.pdf` (12 صفحات)
- `audit_log_export_W14-W19.csv`
- `prompt_versions_LOG-B2.json`
- `roi_baseline_LOG-B2.xlsx`
- `proof_pack_LOG-B2_v1.pdf`
- `recording_handoff_training_60min.mp4`

---

**تواصل / Contact:** sales@dealix.me · `engagement_id: AQW-2026-031`

*هذا تقرير اصطناعي (Sample) من Dealix AI Ops. يوضّح جودة الإخراج، لا يمثّل عميلًا حقيقيًا.*
