# خريطة الخدمات إلى KPIs — طبقة رأس المال

**الطبقة:** L1 · Capital Model
**المالك:** المؤسس
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [SERVICE_KPI_MAP.md](./SERVICE_KPI_MAP.md)

## السياق
كل خدمة في ديلكس يجب أن تكون مرتبطة بـ KPI قابل للقياس قبل بيعها.
هذه الوثيقة هي الخريطة المرجعية من الخدمة إلى الـ KPI الأساسي
والثانوي ونوع الدليل. وتُطبّق القاعدة المُحدَّدة في
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` بأن لا نبيع عملاً لا يمكن
إثبات أثره. هذه الوثيقة هي القيد الأعلى لـ
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md` ولـ
`docs/COMPANY_SERVICE_LADDER.md`.

## الخريطة

| Service | Primary KPI | Secondary KPI | Proof Type |
|---|---|---|---|
| Lead Intelligence Sprint | Qualified accounts ranked | Data quality improvement | Revenue / Quality |
| AI Quick Win Sprint | Hours saved | Error reduction | Time / Quality |
| Company Brain Sprint | Answers with sources | Search time reduction | Knowledge / Quality |
| AI Support Desk | Response time reduction | Reply consistency | Time / Quality |
| Governance Program | Risk controls implemented | Approvals logged | Risk |

## القاعدة

> أي خدمة بلا KPI واضح لا تُباع.

إذا تعذّر التعبير عن وضع العميل المحتمل بأحد أنواع الدليل أعلاه
(Revenue / Time / Knowledge / Quality / Risk)، تُعاد صياغة العمل،
أو يُقلَّص النطاق إلى تشخيص، أو يُرفَض. هذا يحفظ رأس مال الثقة
ويحمي خطّ أنابيب Proof Packs.

## أنواع الدليل وكيف تبدو

- **Revenue** — قيمة Pipeline مُغلَقة، حسابات مؤهّلة، تغيّر Win-Rate،
  إيراد جديد لكل قناة.
- **Time** — ساعات مُوفّرة أسبوعياً، تخفيض زمن الردّ، تخفيض دورة
  العمل.
- **Knowledge** — إجابات بمصادر، تخفيض زمن البحث، دقة الاسترجاع.
- **Quality** — معدّل الخطأ، معدّل الاتّساق، نتيجة جودة اللغة
  العربية.
- **Risk** — ضوابط مُطبَّقة، تغطية Audit Log، حوادث تمّ منعها أو
  احتواؤها.

## انضباط تعريف الـ KPI

لكل خدمة يكتب الفريق الـ KPI بالصيغة:

> *المقياس، الخطّ الأساس، الهدف، طريقة القياس، المالك.*

بدون الحقول الخمسة جميعها، يُعتبر الـ KPI غير معرَّف، ولا تكون
الخدمة قابلة للبيع حتى تُسدّ الفجوة.

## إضافة خدمة جديدة إلى الخريطة

1. عرّف الـ KPI الأساسي بصيغة الحقول الخمسة.
2. عرّف الـ KPI الثانوي بالصيغة ذاتها.
3. اربط الاثنين بأحد أنواع الدليل الخمسة.
4. تأكّد من وجود قالب Proof Pack أو إمكانية إنتاجه.
5. أضف صفّاً إلى هذا الجدول.
6. أحِل في `docs/COMPANY_SERVICE_LADDER.md` و
   `docs/OFFER_LADDER_AND_PRICING.md`.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| اقتراح خدمة جديدة | تعريف الـ KPI المُسجَّل | المؤسس | لكل خدمة |
| تقرير الإقفال | قيم KPI الفعلية | قائد التسليم | لكل مشروع |
| مراجعة ربعية | مقترحات تعديل الـ KPI | المؤسس | ربعياً |
| Pipeline المبيعات | صفقات مرفوضة لغياب KPI | المؤسس | أسبوعياً |

## المقاييس
- KPI-defined service share — نسبة الخدمات القابلة للبيع ذات KPI كامل الحقول؛ الهدف 100%.
- Proof-pack production rate — نسبة المشاريع المُغلَقة المُنتجة لـ Proof Pack مرتبط بالـ KPI؛ الهدف ≥ 95%.
- KPI achievement rate — نسبة المشاريع التي حقّقت أو تخطّت هدف الـ KPI الأساسي؛ الهدف ≥ 75%.
- Discarded deals — عدد الصفقات المرفوضة لعدم ملاءمة الـ KPI؛ يُتابع دون سقف.

## ذات صلة
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — لوحة الـ KPIs التي تظهر فيها هذه المقاييس.
- `docs/COMPANY_SERVICE_LADDER.md` — كتالوج الخدمات الذي تحكمه الخريطة.
- `docs/OFFER_LADDER_AND_PRICING.md` — طبقة التسعير المعتمدة على الخريطة.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — نموذج رأس المال الذي تُغذّيه الخريطة.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
