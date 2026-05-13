# قالب حزمة الإثبات — سبرنت دماغ الشركة

**الطبقة:** كتالوج الخدمات · العدّة التشغيلية
**المالك:** مراجِع الجودة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [proof_pack_template.md](./proof_pack_template.md)

## السياق
القطعة الوحيدة القابلة للتدقيق لسبرنت دماغ الشركة. يُخصِّص القالب الرئيس `docs/templates/PROOF_PACK_TEMPLATE.md` لخدمة طبقة المعرفة. يرتبط بـ `docs/governance/AI_INFORMATION_GOVERNANCE.md` وسجل ادعاءات الاستراتيجية في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## هيكل الحزمة
مجلد يحتوي:
1. `events.jsonl` — سجل أحداث للإلحاق فقط.
2. `summary.md` — ملخص بشري.
3. `evidence/` — خريطة التغطية، عيّنات مراجع (مُجهَّلة)، مقتطفات سجل الحوكمة.
4. `signoff.md` — توقيع DL + QA + GR + KO + الراعي.
5. `anonymization_rules.md`.

## الأحداث المطلوبة
| الحدث | نوع القيمة | يُلتقَط بواسطة | المرحلة |
|---|---|---|---|
| `intake_completed` | bool | مهندس المبيعات | قبل الإطلاق |
| `sprint_initialized` | bool | DL | T-1 |
| `documents_indexed` | integer | KE | الأسبوع 1 |
| `source_registry_complete` | bool | KE + GR | الأسبوع 1 |
| `index_tuned` | bool | KE | الأسبوع 2 |
| `permission_model_implemented` | bool | GR | الأسبوع 2 |
| `answers_with_sources` | integer | KE | الأسبوع 3 |
| `insufficient_evidence_responses` | integer | KE | الأسبوع 3 |
| `hallucinated_citations` | integer | QA | الأسبوع 3 |
| `blocked_unauthorized_accesses` | integer | GR | الأسبوع 4 |
| `qa_round_1_complete` | bool | QA | نهاية الأسبوع 3 |
| `qa_round_2_complete` | bool | QA | نهاية الأسبوع 4 |
| `sprint_delivered` | bool | DL | الأسبوع 4 |
| `proof_pack_signed_off` | bool | الراعي | الأسبوع 4 |
| `upsell_motion_triggered` | bool | DL/CSM | الأسبوع 4 |

## أحداث اختيارية
- `sensitive_data_masked` (integer).
- `freshness_flags_raised` (integer).
- `cross_border_flag_resolved` (bool).

## قواعد التجهيل
تجري فقط على موافقة نشر صريحة.

### القواعد
1. اسم العميل → `<Sector> client (<Region>)`.
2. عناوين المستندات → لا تُنشَر حرفيًا.
3. هويات أنظمة المصدر (اسم workspace في Notion، مسار Drive) → مَخْفِية.
4. عيّنات المراجع → معاد صياغتها لتجنب اقتباس نصوص السياسة حرفيًا.
5. الأعداد → تقريب لأقرب 5.
6. PII → لا تُنشَر أبدًا.

### ما يمكن نشره
- عدد المستندات المُفهرَسة (مُقرَّب).
- نسبة الإجابات بمراجع (مُقرَّبة).
- معدّل أدلّة-غير-كافية (مُقرَّب).
- شهادة المُشتري (بموافقة).
- شكل خريطة التغطية (مستقل عن القطاع).

### ما لا يمكن نشره
- عناوين المستندات.
- نص المراجع حرفيًا.
- معرّفات أنظمة المصدر الداخلية.
- تفاصيل نموذج الصلاحيات.
- تعريفات مجموعات المستخدمين.

## إعادة الاستخدام للتسويق
تُغذّي الحزمة صفحة الثقة فقط عبر سكربت التصدير المُجهَّل. لا استخراج يدوي.

## التخزين والاحتفاظ
- مُشفَّرة في السكون.
- الوصول: DL، QA، GR، CSM، قائد القدرة.
- الاحتفاظ: المشروع + 365 يومًا؛ علامة الحساسية = المشروع + 30 يومًا.
- يُسجَّل الحذف.

## قالب كتلة التوقيع
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Knowledge Owner: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the Company Brain Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## مثال عملي (توضيحي)
```
{"event":"documents_indexed","timestamp":"2026-05-15T17:00:00Z","actor_role":"KE","value":142,"notes":"3 source systems"}
{"event":"source_registry_complete","timestamp":"2026-05-16T16:00:00Z","actor_role":"KE","value":true,"notes":""}
{"event":"index_tuned","timestamp":"2026-05-22T17:00:00Z","actor_role":"KE","value":true,"notes":"chunk=512, top_k=5"}
{"event":"answers_with_sources","timestamp":"2026-05-29T17:00:00Z","actor_role":"KE","value":287,"notes":"out of 300 test queries"}
{"event":"insufficient_evidence_responses","timestamp":"2026-05-29T17:00:00Z","actor_role":"KE","value":13,"notes":""}
{"event":"hallucinated_citations","timestamp":"2026-05-29T17:00:00Z","actor_role":"QA","value":0,"notes":""}
{"event":"blocked_unauthorized_accesses","timestamp":"2026-06-05T15:00:00Z","actor_role":"GR","value":7,"notes":"test users"}
{"event":"sprint_delivered","timestamp":"2026-06-08T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| إصدار أحداث في الوقت الحقيقي | events.jsonl | كل الأدوار | مستمر |
| مراجعة نهاية الأسبوع 4 | signoff.md | كل الموقّعين | نهاية الأسبوع 4 |
| موافقة النشر | تصدير مُجهَّل | DL + التسويق | بعد التسليم |

## المقاييس
- **اكتمال التقاط الأحداث** — الهدف = 100%.
- **تأخر التوقيع** — الهدف ≤ 3 أيام عمل.
- **تدقيق التجهيل** — الهدف = 100%.

## ذات صلة
- `docs/templates/PROOF_PACK_TEMPLATE.md` — الهيكل الرئيس
- `docs/quality/QUALITY_STANDARD_V1.md` — نظام الجودة
- `docs/capabilities/knowledge_capability.md` — مخطط القدرة
- `docs/company/CAPABILITY_VALUE_MAP.md` — خريطة القدرات
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — الحوكمة
- `docs/ledgers/SOURCE_REGISTRY.md` — سجل المصادر
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — التوجيه
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — الرصد
- `docs/DATA_RETENTION_POLICY.md` — الاحتفاظ
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
