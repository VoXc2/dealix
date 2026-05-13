# وكيل جودة البيانات — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الذكاء الاصطناعي
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [data_quality_agent.md](./data_quality_agent.md)

## السياق
تبدأ معظم تكليفات ديلكس ببيانات فوضوية. وكيل جودة البيانات هو أول مفتّش
في سير العمل: يصنّف المشكلات، يقيّم البيانات، ويوصي بالإصلاحات — دون
المساس بالمصدر. ينفّذ هذا الوكيل طبقة جاهزية البيانات الموصوفة في
`docs/DEALIX_OPERATING_CONSTITUTION.md` وعقد قوى العمل في
`docs/product/AI_WORKFORCE_OPERATING_MODEL.md`.

## بطاقة الوكيل

- **الدور:** يصنّف ويقيّم مشكلات جودة البيانات في البيانات المرفوعة
  ليبدأ التكليف من خط أساس قابل للقياس.
- **المدخلات المسموحة:** ملفات CSV/JSON (بإذن العميل)، تعريفات المخطط،
  وسوم الحساسية.
- **المخرجات المسموحة:** درجة الجودة، قائمة المشكلات، الإصلاحات الموصى
  بها، لقطة خط الأساس.
- **الممنوع:** تعديل بيانات العميل؛ تصدير بيانات شخصية خام؛ الكتابة على
  أنظمة العميل؛ إرسال إشعارات.
- **الفحوصات المطلوبة:**
  - وجود مصدر وعلامة حساسية للبيانات؛
  - الكشف عن البيانات الشخصية ووسمها؛
  - مطابقة المسطرة المنشورة؛
  - الإصلاحات قابلة للتراجع.
- **مخطط الإخراج:** `DataQualityReport { dataset_id, score, issues[],
  recommended_fixes[], pii_flags[], baseline_snapshot_ref }`.
- **الاعتماد:** مراجعة بشرية قبل التسليم للعميل.

## تصنيف المشكلات

- حقول مفقودة / صفوف فارغة.
- تكرارات وتكرارات شبه متطابقة.
- اختلاف الأنواع وانحراف التنسيق.
- سجلات قديمة (أقدم من العتبة).
- حقول حسّاسة بلا تقنيع.
- معرّفات متناقضة بين المصادر.

## مسطرة التقييم (موجز)

| Dimension | Weight | Notes |
|---|---|---|
| Completeness | 25% | required fields populated |
| Uniqueness | 20% | dedupe ratio |
| Validity | 20% | type and format conformance |
| Freshness | 15% | within engagement window |
| Sensitivity | 10% | PII masked/labeled |
| Consistency | 10% | cross-source agreement |

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Raw dataset + schema | DataQualityReport | Delivery owner | Per engagement |
| Issue list | Fix plan | Delivery owner | Per engagement |
| Score snapshot | Value Ledger baseline | Delivery owner | Per engagement |

## المقاييس
- Time-to-Baseline — دقائق من رفع البيانات إلى أول درجة.
- Score Lift — متوسط الارتفاع من الأساس إلى التسليم.
- False-Flag Rate — نسبة المشكلات المرفوضة من المراجع.
- PII Detection Recall — نسبة الحقول الشخصية الموسومة بصواب.

## ذات صلة
- `docs/AI_STACK_DECISIONS.md` — اختيار النموذج لهذا الوكيل
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — مجموعة التقييم
- `docs/EVALS_RUNBOOK.md` — تشغيل التقييمات
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — القواعد الناظمة
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
