# درجة جودة البيانات — الدستور · المعايير التأسيسية

**الطبقة:** الدستور · المعايير التأسيسية
**المالك:** قائد البيانات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [DATA_QUALITY_SCORE.md](./DATA_QUALITY_SCORE.md)

## السياق
هذا الملف الدليل التشغيلي لاحتساب درجة جاهزية البيانات (DRS) المعرَّفة
في `docs/data/DATA_READINESS_STANDARD.md`. يُحدد الصيغ والحالات الحدية،
وكيفية تسجيل النتائج في سجل تشغيل الذكاء الاصطناعي، وكيفية تغذية فحص
الحوكمة. يُكمّله `docs/AI_OBSERVABILITY_AND_EVALS.md` و
`docs/EVALS_RUNBOOK.md` لقصة الرصد، و
`docs/services/data_readiness_assessment/scoring_model.md` لخدمة
التقييم المنتَجة.

## الصيغة
درجة الجاهزية الإجمالية مجموع مرجَّح لسبعة مكوّنات. الأوزان معيارية
ولا يجوز تغييرها بلا تعديل دستوري.

```
DRS = (
  source_coverage_score   * 0.20 +
  completeness_score      * 0.15 +
  consistency_score       * 0.15 +
  freshness_score         * 0.10 +
  dedup_score             * 0.10 +
  pii_handling_score      * 0.15 +
  business_mapping_score  * 0.15
)
```

كل مكوّن على مقياس 0-100، والنتيجة محصورة في `[0, 100]`.

## صيغ المكونات
- `source_coverage_score = 100 * records_with_known_source / records_total`
- `completeness_score = 100 * required_fields_filled / required_fields_total`
- `consistency_score = 100 * records_passing_type_and_enum_checks / records_total`
- `freshness_score = 100 * records_updated_within_180_days / records_total`
- `dedup_score = 100 * (records_total - duplicate_records) / records_total`
- `pii_handling_score = 100` ثم خصم لكل ضابط مفقود:
  - `−40` إذا حقل شخصي بلا `allowed_use`.
  - `−30` إذا حقل شخصي بلا `source_type`.
  - `−20` إذا سجل بلا `relationship_status`.
  - `−10` إذا ظهرت بيانات شخصية في أي حدث مُسجَّل.
- `business_mapping_score = 100 * records_mapped_to_capability / records_total`

## الحالات الحدية
| الحالة | السلوك |
|---|---|
| `records_total = 0` | الدرجة غير معرَّفة؛ القرار `not_ready` |
| بيانات شخصية بلا `allowed_use` | تخفيض تلقائي إلى `not_ready` |
| مكوّن واحد أقل من 30 | يُعلَّم `bottleneck` ويظهر في حزمة الإثبات |
| `freshness_score < 40` | فتح تذكرة تحديث قبل استخدام الذكاء |
| المخطط ليس في المكتبة | رفض؛ معالجة تفرع المخطط |

## التسجيل — سجل تشغيل الذكاء
كل احتساب يُسجَّل في سجل تشغيل الذكاء. السجل يحمل الدرجة والمدخلات
والقرار.

```json
{
  "ai_run_id": "AIR-DRS-001",
  "agent": "DataReadinessAgent",
  "task": "score_dataset",
  "dataset_id": "DS-001",
  "drs_components": {
    "source_coverage_score": 90,
    "completeness_score": 78,
    "consistency_score": 82,
    "freshness_score": 65,
    "dedup_score": 70,
    "pii_handling_score": 40,
    "business_mapping_score": 80
  },
  "overall_data_readiness": 76,
  "decision": "usable_with_review",
  "bottlenecks": ["pii_handling_score"],
  "audit_event_id": "AUD-1042"
}
```

## التغذية في فحص الحوكمة
يأخذ `governance_check` الدرجة مدخلًا ويطبّق التوجيه التالي:

- DRS ≥ 85 وبلا اختناق حرج → `ALLOW`
- DRS 70-84 → `ALLOW_WITH_REVIEW`
- DRS 50-69 → `BLOCK` بسبب `cleanup_required`
- DRS < 50 → `BLOCK` بسبب `not_ready`
- اختناق بيانات شخصية → `REQUIRE_APPROVAL` بصرف النظر عن الرقم

راجع `docs/governance/RUNTIME_GOVERNANCE.md` لتعريفات الأفعال.

## إعادة التقييم
يجب إعادة تقييم أي مجموعة عند:
- تحديث المجموعة.
- مرور 30 يومًا على آخر تقييم.
- تغيّر إصدار المخطط.
- تعديل حوكمي للأوزان أو العتبات.

## الواجهات
| المدخلات | المخرجات | المالك | الوتيرة |
|---|---|---|---|
| مجموعة + مخطط | سجل DRS | قائد البيانات | لكل مجموعة |
| سجل DRS | قرار توجيه حوكمي | قائد الحوكمة | لكل تشغيل |
| قائمة الاختناقات | خطة تنظيف/معالجة | قائد التسليم | لكل اكتشاف |

## المقاييس
- **حداثة الدرجات** — نسبة المجموعات المستخدمة بدرجة أحدث من 30 يومًا.
  المستهدف: 100%.
- **زمن إغلاق الاختناقات** — ≤ 14 يومًا.
- **انجراف الدرجات** — تغير DRS ربعًا بربع لكل مجموعة. المستهدف: ≥ 0
  (لا تراجع).

## ذات صلة
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — رصد تشغيلات الذكاء والدرجات.
- `docs/EVALS_RUNBOOK.md` — دليل التقييم.
- `docs/services/data_readiness_assessment/scoring_model.md` — نموذج
  التقييم المنتَج.
- `docs/data/DATA_READINESS_STANDARD.md` — المعيار المرجعي.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
