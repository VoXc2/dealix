# قالب حزمة الإثبات — سبرنت مكتب الدعم بالذكاء الاصطناعي

**الطبقة:** كتالوج الخدمات · العدّة التشغيلية
**المالك:** مراجِع الجودة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [proof_pack_template.md](./proof_pack_template.md)

## السياق
القطعة الوحيدة القابلة للتدقيق لسبرنت مكتب الدعم. يُخصِّص القالب الرئيس `docs/templates/PROOF_PACK_TEMPLATE.md` لخدمة طبقة العملاء. يرتبط بـ `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` وسجل ادعاءات الاستراتيجية في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## هيكل الحزمة
يحتوي المجلد:
1. `events.jsonl` — سجل أحداث للإلحاق فقط.
2. `summary.md` — ملخص بشري.
3. `evidence/` — نماذج فئات مُجهَّلة، لقطات مكتبة الردود، سجل التصعيد.
4. `signoff.md` — توقيع DL + QA + GR + SL + الراعي.
5. `anonymization_rules.md`.

## الأحداث المطلوبة
| الحدث | نوع القيمة | يُلتقَط بواسطة | المرحلة |
|---|---|---|---|
| `intake_completed` | bool | مهندس المبيعات | قبل الإطلاق |
| `sprint_initialized` | bool | DL | T-1 |
| `messages_classified` | integer | AN | الأيام 1–3 |
| `category_coverage` | decimal (%) | AN | الأيام 1–3 |
| `replies_drafted` | integer | CL | الأيام 4–7 |
| `escalations_routed` | integer | GR | الأيام 8–10 |
| `sensitive_blocks` | integer | GR | الأيام 8–10 |
| `auto_send_incidents` | integer | QA | مستمر |
| `qa_round_1_complete` | bool | QA | اليوم 12 |
| `qa_round_2_complete` | bool | QA | اليوم 14 |
| `sprint_delivered` | bool | DL | اليوم 14 |
| `proof_pack_signed_off` | bool | الراعي | اليوم 14 |
| `upsell_motion_triggered` | bool | DL/CSM | اليوم 14 |

## أحداث اختيارية
- `sensitive_data_masked` (integer).
- `clinics_playbook_applied` (bool) — حين تُحفَّز علاوة العيادات.
- `cross_border_flag_resolved` (bool).

## قواعد التجهيل
تجري فقط على موافقة نشر صريحة.

### القواعد
1. اسم العميل → `<Sector> client (<Region>)`.
2. نص رسالة العميل → لا يُقتبَس حرفيًا.
3. نص مكتبة الردود → لا يُقتبَس حرفيًا.
4. الأعداد → تقريب لأقرب 5.
5. PII → لا تُنشَر أبدًا.
6. الفئات الحساسة (عيادات، مالية، شكاوى) → تُنشَر فقط بموافقة إضافية.

### ما يمكن نشره
- الفئات المُغطّاة (عدد مُقرَّب).
- نسبة التغطية (مُقرَّبة).
- الردود المُصاغة (عدد مُقرَّب).
- التصعيدات المُوجَّهة (عدد مُقرَّب).
- شهادة المُشتري (بموافقة).

### ما لا يمكن نشره
- نص رسالة العميل.
- نص مكتبة الردود حرفيًا.
- أمثلة الحالات الحساسة.
- هويات اتصال التصعيد.

## إعادة الاستخدام للتسويق
تُغذّي الحزمة صفحة الثقة فقط عبر سكربت التصدير المُجهَّل. لا استخراج يدوي.

## التخزين والاحتفاظ
- مُشفَّرة في السكون.
- الوصول: DL، QA، GR، CSM، قائد القدرة.
- الاحتفاظ: المشروع + 365 يومًا؛ علامة الحساسية أو علاوة العيادات = المشروع + 30 يومًا.
- يُسجَّل الحذف.

## قالب كتلة التوقيع
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Support Lead: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the AI Support Desk Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## مثال عملي (توضيحي)
```
{"event":"messages_classified","timestamp":"2026-05-15T17:00:00Z","actor_role":"AN","value":4823,"notes":""}
{"event":"category_coverage","timestamp":"2026-05-15T17:00:00Z","actor_role":"AN","value":92.4,"notes":"holdout"}
{"event":"replies_drafted","timestamp":"2026-05-19T16:00:00Z","actor_role":"CL","value":78,"notes":"39 categories × 2 langs"}
{"event":"escalations_routed","timestamp":"2026-05-22T15:00:00Z","actor_role":"GR","value":6,"notes":"sensitive types"}
{"event":"sensitive_blocks","timestamp":"2026-05-22T15:00:00Z","actor_role":"GR","value":0,"notes":"no auto-reply to sensitive in tests"}
{"event":"auto_send_incidents","timestamp":"2026-05-26T12:00:00Z","actor_role":"QA","value":0,"notes":""}
{"event":"sprint_delivered","timestamp":"2026-05-26T15:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| إصدار أحداث في الوقت الحقيقي | events.jsonl | كل الأدوار | مستمر |
| مراجعة اليوم 14 | signoff.md | كل الموقّعين | اليوم 14 |
| موافقة النشر | تصدير مُجهَّل | DL + التسويق | بعد التسليم |

## المقاييس
- **اكتمال التقاط الأحداث** — الهدف = 100%.
- **تأخر التوقيع** — الهدف ≤ 3 أيام عمل.
- **تدقيق التجهيل** — الهدف = 100%.
- **حوادث إرسال تلقائي في عقد الإنتاج** — الهدف = 0.

## ذات صلة
- `docs/templates/PROOF_PACK_TEMPLATE.md` — الهيكل الرئيس
- `docs/quality/QUALITY_STANDARD_V1.md` — نظام الجودة
- `docs/capabilities/customer_capability.md` — مخطط القدرة
- `docs/company/CAPABILITY_VALUE_MAP.md` — خريطة القدرات
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — قواعد HITL
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — كتاب لعب CS
- `docs/playbooks/clinics_playbook.md` — علاوة العيادات
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — الرصد
- `docs/DATA_RETENTION_POLICY.md` — الاحتفاظ
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
