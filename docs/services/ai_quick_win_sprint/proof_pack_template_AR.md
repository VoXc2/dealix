# قالب حزمة الإثبات — سبرنت المكسب السريع للذكاء الاصطناعي

**الطبقة:** كتالوج الخدمات · العدّة التشغيلية
**المالك:** مراجِع الجودة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [proof_pack_template.md](./proof_pack_template.md)

## السياق
حزمة الإثبات هي القطعة الوحيدة القابلة للتدقيق التي تحوّل مكسب سير عمل 7 أيام إلى دليل شركاتي قابل للدفاع عنه. هذا الملف يخصّص القالب الرئيس `docs/templates/PROOF_PACK_TEMPLATE.md` لسبرنت AI Quick Win. يفرض ما يُقاس ويُجهَّل ويُعاد نشره. يرتبط بسجل الادعاءات الاستراتيجي في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## هيكل الحزمة
يحتوي مجلد حزمة الإثبات:
1. `events.jsonl` — سجل أحداث للإلحاق فقط.
2. `summary.md` — ملخص بشري.
3. `evidence/` — لقطات مُجهَّلة، SOP النهائي، التوقيتات قبل/بعد.
4. `signoff.md` — كتلة توقيع DL + QA + مالك سير العمل + الراعي.
5. `anonymization_rules.md` — قواعد لأي استخدام خارجي.

## الأحداث المطلوبة
| الحدث | نوع القيمة | يُلتقَط بواسطة | المرحلة |
|---|---|---|---|
| `intake_completed` | bool | مهندس المبيعات | قبل الإطلاق |
| `sprint_initialized` | bool | DL | T-1 |
| `workflow_mapped` | bool | DS | اليوم 1 |
| `baseline_measured` | decimal (ساعات/دورة) | DS | اليوم 2 |
| `ai_step_designed` | bool | DS | اليوم 3 |
| `draft_built` | bool | DS | اليوم 4 |
| `owner_reviewed` | bool | WO | اليوم 5 |
| `test_cycle_complete` | bool | WO | اليوم 6 |
| `manual_steps_reduced` | integer | WO + DS | اليوم 6 |
| `hours_saved` | decimal | DL | اليوم 7 |
| `workflow_created` | bool | DS | اليوم 7 |
| `qa_complete` | bool | QA | اليوم 7 |
| `sprint_delivered` | bool | DL | اليوم 7 |
| `proof_pack_signed_off` | bool | SP | اليوم 7 |
| `upsell_motion_triggered` | bool | DL/CSM | اليوم 7 |

## أحداث اختيارية
- `sensitive_data_masked` (integer).
- `cross_border_flag_resolved` (bool).
- `revisions_applied` (integer).

## قواعد التجهيل
تجري فقط على موافقة نشر صريحة.

### القواعد
1. اسم العميل → `<Sector> client (<Region>)`.
2. اسم سير العمل → وصف عام ("مراجعة الفوترة"، "تقرير KPI الشهري").
3. المقاييس الرقمية → تقريب لأقرب 0.5 ساعة أو 5%.
4. دقة التاريخ → تقريب للشهر.
5. PII → لا تُنشَر أبدًا.
6. أسماء الأدوات → تُبقى فقط بموافقة.

### ما يمكن نشره
- الساعات المُوفَّرة لكل دورة (مُقرَّبة).
- الدورات المُشغَّلة على التدفّق الجديد.
- دور المالك (مثلًا: "مدير المالية")، لا اسم المالك أبدًا.
- شهادة المُشتري (بموافقة).

### ما لا يمكن نشره
- منطق سير العمل الداخلي.
- الـ prompts المُستخدَمة.
- اعتمادات الأدوات أو أسماء مساحات العمل.
- توقيتات قبل/بعد المفصّلة خارج التجميعات.

## إعادة الاستخدام للتسويق
تُغذّي الحزمة صفحة الثقة فقط عبر سكربت التصدير المُجهَّل. لا استخراج يدوي.

## التخزين والاحتفاظ
- مُشفَّرة في السكون في خزنة Dealix.
- الوصول: DL، QA، CSM، قائد القدرة.
- الاحتفاظ: المشروع + 365 يومًا؛ علامة الحساسية = المشروع + 30 يومًا.
- يُسجَّل الحذف عند انتهاء الاحتفاظ.

## قالب كتلة التوقيع
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Workflow Owner: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the AI Quick Win Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## مثال عملي (توضيحي)
```
{"event":"workflow_mapped","timestamp":"2026-05-13T11:00:00Z","actor_role":"DS","value":true,"notes":"Monthly KPI review workflow"}
{"event":"baseline_measured","timestamp":"2026-05-14T16:00:00Z","actor_role":"DS","value":3.5,"notes":"hours per cycle, n=1"}
{"event":"ai_step_designed","timestamp":"2026-05-15T15:00:00Z","actor_role":"DS","value":true,"notes":"Approval gate before report send"}
{"event":"draft_built","timestamp":"2026-05-16T17:00:00Z","actor_role":"DS","value":true,"notes":""}
{"event":"owner_reviewed","timestamp":"2026-05-17T15:00:00Z","actor_role":"WO","value":true,"notes":"3 revisions"}
{"event":"test_cycle_complete","timestamp":"2026-05-18T17:00:00Z","actor_role":"WO","value":true,"notes":"new cycle = 1.2h"}
{"event":"hours_saved","timestamp":"2026-05-19T12:00:00Z","actor_role":"DL","value":2.3,"notes":"per monthly cycle"}
{"event":"sprint_delivered","timestamp":"2026-05-19T16:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| إصدار أحداث في الوقت الحقيقي | events.jsonl | كل الأدوار | مستمر |
| مراجعة اليوم 7 | signoff.md | DL + QA + WO + SP | اليوم 7 |
| موافقة النشر | تصدير مُجهَّل | DL + التسويق | بعد التسليم |

## المقاييس
- **اكتمال التقاط الأحداث** — الهدف = 100%.
- **تأخر التوقيع** — الهدف ≤ يومَيْ عمل.
- **تدقيق التجهيل** — الهدف = 100%.

## ذات صلة
- `docs/templates/PROOF_PACK_TEMPLATE.md` — الهيكل الرئيس
- `docs/quality/QUALITY_STANDARD_V1.md` — نظام الجودة
- `docs/capabilities/operations_capability.md` — مخطط القدرة
- `docs/company/CAPABILITY_VALUE_MAP.md` — خريطة القدرات
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — تصميم وقت التشغيل
- `docs/product/PRODUCTIZATION_LEDGER.md` — سجل التحويل لمنتج
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — الرصد
- `docs/DATA_RETENTION_POLICY.md` — الاحتفاظ
- `docs/AI_STACK_DECISIONS.md` — الكومة المعتمَدة
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
