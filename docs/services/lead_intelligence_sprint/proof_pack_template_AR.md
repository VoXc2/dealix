# قالب حزمة الإثبات — سبرنت ذكاء العملاء المحتملين

**الطبقة:** كتالوج الخدمات · العدّة التشغيلية
**المالك:** مراجِع الجودة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [proof_pack_template.md](./proof_pack_template.md)

## السياق
حزمة الإثبات هي **القطعة الوحيدة القابلة للتدقيق** التي تحوّل سبرنت Dealix من فاتورة مزوّد إلى دليل شركاتي قابل للدفاع عنه. هذا الملف يُخصِّص القالب الرئيس `docs/templates/PROOF_PACK_TEMPLATE.md` لسبرنت ذكاء العملاء المحتملين. يفرض ما يُقاس، وكيف يُجهَّل، وما يمكن إعادة نشره على صفحة الثقة. يرتبط بسجل ادعاءات الاستراتيجية في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` ونظام الجودة في `docs/quality/QUALITY_STANDARD_V1.md`.

## هيكل الحزمة
حزمة الإثبات مجلد يحتوي:
1. `events.jsonl` — سجل أحداث للإلحاق فقط.
2. `summary.md` — ملخص بشري قابل للقراءة للأحداث.
3. `evidence/` — ملفات داعمة (تصديرات مُجهَّلة، لقطات، تقارير موقَّعة).
4. `signoff.md` — كتلة توقيع DL + QA + CS.
5. `anonymization_rules.md` — القواعد المُطبَّقة لأي استخدام خارجي.

## الأحداث المطلوبة
يجب أن يلتقط كل سبرنت، كحد أدنى، هذه الأحداث. كل حدث له المخطط:
```
{
  "event": "<name>",
  "timestamp": "<ISO8601>",
  "actor_role": "DL|AN|CL|QA|CS|CR",
  "value": <number|bool|string>,
  "notes": "<short freetext>"
}
```

| الحدث | نوع القيمة | يُلتقَط بواسطة | المرحلة |
|---|---|---|---|
| `intake_completed` | bool | مهندس المبيعات | قبل الإطلاق |
| `sprint_initialized` | bool | DL | T-1 |
| `rows_imported` | integer | AN | اليوم 1 |
| `duplicates_removed` | integer | AN | اليوم 2 |
| `accounts_scored` | integer | AN | اليوم 3 |
| `top_50_locked` | bool | DL | اليوم 4 |
| `top_10_action_plan_complete` | bool | DL | اليوم 4 |
| `drafts_generated` | integer | CL | اليوم 5 |
| `mini_crm_provisioned` | bool | DL | اليوم 6 |
| `qa_round_1_complete` | bool | QA | اليوم 7 |
| `qa_round_1_failures` | integer | QA | اليوم 7 |
| `client_preview_held` | bool | DL | اليوم 9 |
| `qa_round_2_complete` | bool | QA | اليوم 10 |
| `sprint_delivered` | bool | DL | اليوم 10 |
| `proof_pack_signed_off` | bool | CS | اليوم 10 |
| `upsell_motion_triggered` | bool | DL/CSM | اليوم 10 |

## أحداث اختيارية (عند الانطباق)
- `sensitive_data_masked` (integer) — الحقول المُخفاة.
- `cross_border_flag_resolved` (bool).
- `pdpl_pre_check_completed` (bool).
- `revision_requests` (integer).

## قواعد التجهيل
يجري التجهيل **فقط** عند توقيع العميل موافقة نشر صريحة في SOW أو بعد التسليم.

### القواعد
1. **اسم العميل** → استبدل بـ `<Sector> client (<Region>)` (مثلًا: "B2B SaaS client (Riyadh)").
2. **أسماء الحسابات** في أعلى 50 → لا تُنشَر أبدًا؛ أعداد مُجمَّعة فقط.
3. **المقاييس الرقمية** → تقريب لأقرب 5% عند النشر.
4. **دقة التاريخ** → تقريب للشهر، لا اليوم، عند النشر الخارجي.
5. **PII** → لا تُنشَر أبدًا بأي شكل.
6. **علامات القطاع الحساس** (صحة، حكومة، مالية، قاصرون) → تُنشَر فقط بموافقة خطية إضافية.

### ما يمكن نشره
- الأعداد: rows imported, duplicates removed, accounts scored, drafts generated.
- زمن التسليم (أيام).
- معدّل التحويل (نسبة قبول أعلى 10).
- شهادة المُشتري (بموافقة مُسمّاة).

### ما لا يمكن نشره
- قائمة أعلى 50.
- أسماء حسابات فردية.
- مسوّدات التواصل حرفيًا.
- قيم الدرجات لكل صف.
- منشأ البيانات المصدري.

## إعادة الاستخدام للتسويق
تُغذّي حزمة الإثبات صفحة ثقة Dealix فقط عبر **سكربت التصدير المُجهَّل** في `docs/templates/PROOF_PACK_TEMPLATE.md`. لا استخراج يدوي. يقرأ مُنشِئ صفحة الثقة التصدير لا حزمة الإثبات الخام.

## التخزين والاحتفاظ
- تُخزَّن مُشفَّرة في السكون في خزنة Dealix.
- الوصول: قائد التسليم، مراجِع الجودة، مدير نجاح العميل، قائد القدرة.
- الاحتفاظ: المشروع + 365 يومًا، أو المشروع + 30 يومًا إن وضعت علامة بيانات حساسة في الاستلام.
- الحذف: آلي عند انتهاء الاحتفاظ؛ يُسجَّل الحذف.

## كتلة التوقيع
قالب ملف `signoff.md`:
```
## Signoff

- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Client Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the work delivered in the Lead
Intelligence Sprint for <Client>. Publication is bounded by the
anonymization rules above.
```

## مثال عملي (توضيحي — ليس عميلًا حقيقيًا)
```
{"event":"intake_completed","timestamp":"2026-05-07T10:00:00Z","actor_role":"SE","value":true,"notes":""}
{"event":"rows_imported","timestamp":"2026-05-13T09:12:00Z","actor_role":"AN","value":6431,"notes":"Single XLSX, 11 columns"}
{"event":"duplicates_removed","timestamp":"2026-05-14T16:30:00Z","actor_role":"AN","value":872,"notes":"Email + domain dedupe"}
{"event":"accounts_scored","timestamp":"2026-05-15T18:00:00Z","actor_role":"AN","value":5559,"notes":"Rubric v1.2"}
{"event":"top_50_locked","timestamp":"2026-05-16T17:00:00Z","actor_role":"DL","value":true,"notes":""}
{"event":"drafts_generated","timestamp":"2026-05-17T15:00:00Z","actor_role":"CL","value":16,"notes":"4 seq × 2 lang × 2 versions"}
{"event":"qa_round_1_complete","timestamp":"2026-05-19T17:00:00Z","actor_role":"QA","value":true,"notes":"1 gate failure on tone"}
{"event":"sprint_delivered","timestamp":"2026-05-22T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| إصدار أحداث في الوقت الحقيقي | events.jsonl | كل الأدوار | مستمر |
| مراجعة اليوم 10 | signoff.md | DL + QA + CS | اليوم 10 |
| موافقة النشر | تصدير مُجهَّل | DL + التسويق | بعد التسليم |

## المقاييس
- **اكتمال التقاط الأحداث** — `% required events present at signoff`. الهدف = 100%.
- **تأخر توقيع حزمة الإثبات** — `business days between Day 10 and signoff`. الهدف ≤ 3.
- **تدقيق التجهيل** — `% packs where anonymization rules apply correctly`. الهدف = 100%.

## ذات صلة
- `docs/templates/PROOF_PACK_TEMPLATE.md` — الهيكل الرئيس
- `docs/quality/QUALITY_STANDARD_V1.md` — نظام الجودة
- `docs/capabilities/revenue_capability.md` — مخطط القدرة
- `docs/company/CAPABILITY_VALUE_MAP.md` — خريطة القدرات
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — كتاب لعب الإيرادات
- `docs/DATA_RETENTION_POLICY.md` — الاحتفاظ
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — الرصد
- `docs/COMPANY_SERVICE_LADDER.md` — سُلَّم الخدمات
- `docs/OFFER_LADDER_AND_PRICING.md` — سُلَّم التسعير
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
