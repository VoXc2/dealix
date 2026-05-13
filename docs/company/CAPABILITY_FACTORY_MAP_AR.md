# خريطة مصنع القدرات — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** المؤسس / مسؤول المبيعات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [CAPABILITY_FACTORY_MAP.md](./CAPABILITY_FACTORY_MAP.md)

## السياق

يأتي العملاء بمشكلات خام، لا بأسماء قدرات. هذا الملف هو جدول الترجمة
الذي يحوّل المشكلة المُعلَنة إلى القدرة المطلوب بناؤها، وإلى الخدمة
المناسبة من ديلِكس، ونوع الإثبات المنشود، ومسار التوسّع الطبيعي. وهو
العمود الفقري لتسليم المبيعات إلى التسليم، وتطبيق مباشر للقاعدة
المُعرَّفة في `docs/company/AI_CAPABILITY_FACTORY.md` وسلّم الخدمات في
`docs/COMPANY_SERVICE_LADDER.md`. ترتبط مستويات النضج بالمرساة:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الخريطة

| Input Problem | Capability Built | Dealix Service | Proof Type | Expansion |
|---|---|---|---|---|
| Leads are messy | Revenue | Lead Intelligence Sprint | Revenue / Quality | Monthly RevOps |
| Reports are manual | Reporting | Executive Reporting Automation | Time / Quality | Monthly AI Ops |
| Knowledge scattered | Knowledge | Company Brain Sprint | Knowledge | Brain Management |
| Support overloaded | Customer | AI Support Desk | Time / Quality | Monthly Support |
| AI used unsafely | Governance | AI Governance Program | Risk | Governance Retainer |
| Data not ready | Data | Data Readiness Assessment | Quality / Risk | Data OS |

## كيفية الاستخدام

1. عند الاستقبال، وثِّق مشكلة العميل بكلماته.
2. طابق المشكلة مع صفٍّ من الجدول؛ وإن لم تجد، ارفع الأمر للمؤسس قبل
   إرسال أي عرض سعر.
3. سمِّ القدرة والخدمة في العرض المكتوب.
4. حدّد نوع الإثبات المتوقّع ليتحقّق منه فريق الجودة.
5. هيّئ عرض التوسّع (العمود الأخير) منذ مرحلة الإغلاق.

## التموضع التجاري

"نحدّد القدرة التي يجب بناؤها أولًا، ثم نختار الخدمة المناسبة." هذه
الجملة تحلّ محلّ أي قائمة خدمات طويلة في محادثات البيع، وتُسقط أي عملية
لا تنزل على قدرة مسمّاة — وهو ما يتوقّعه `docs/OFFER_LADDER_AND_PRICING.md`
في أعلى القمع.

## العمليات متعدّدة القدرات

قد يلامس السبرنت الواحد أكثر من قدرة (مثلًا: Lead Intelligence يلامس
Data و Revenue). في هذه الحالة:

- اختر القدرة الرئيسية لتحديد نوع الإثبات.
- اذكر القدرات الثانوية في سجلّ العملية.
- اشترط اجتياز جميع القدرات لفحص الحوكمة.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Client problem statement | Mapped capability + service | Sales | Per inbound |
| Mapped service | Quote + proof type | Sales | Per inbound |
| Quote accepted | Delivery brief + expansion plan | Delivery | Per engagement |
| Delivery outcome | Expansion offer | Sales | Post-proof |

## المقاييس

- Map coverage — نسبة المشكلات الواردة التي تجد صفًّا مطابقًا.
- Capability assignment rate — نسبة العمليات ذات قدرة مسمّاة.
- Sprint-to-retainer conversion — نسبة تحوّل السبرنت إلى اشتراك بالمسار المخطّط.
- Time to quote — الساعات من الاستقبال إلى عرض سعر مُسمَّى.

## ذات صلة

- `docs/COMPANY_SERVICE_LADDER.md` — الخدمات المرجعية في الخريطة.
- `docs/OFFER_LADDER_AND_PRICING.md` — التسعير لكل خدمة.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية المُؤطِّرة للفئات.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مستويات النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
