# قدرة العمليات — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** مسؤول العمليات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [operations_capability.md](./operations_capability.md)

## السياق

قدرة العمليات تُخفّض الخطوات اليدوية والوقت والأخطاء في الأعمال
الداخلية. وهي البوّابة الأكثر استخدامًا لـ"AI Quick Win" والأساس
للأتمتة بين الفِرَق. مرجعها `docs/V14_FOUNDER_DAILY_OPS.md` وحلقة
التشغيل اليومية في `docs/ops/DAILY_OPERATING_LOOP.md`. يُقاس النضج عبر:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

تقليل الخطوات اليدوية والوقت والأخطاء في الأعمال المتكرّرة.

## المشكلات الشائعة

- إدخال بيانات يدوي بين الأدوات.
- أعمال متكرّرة بلا أتمتة.
- أدوات مبعثرة وتسليمات مكسورة بينها.

## المدخلات المطلوبة

- خرائط الأعمال (الحالة الحالية والمسؤول).
- ملفات المصدر (نماذج، صادرات، جداول).
- الأنظمة الهدف (CRM، محاسبة، صندوق وارد).

## وظائف الذكاء الاصطناعي

- استخراج البيانات من المستندات والرسائل.
- تحويل البيانات بين المخطّطات والصيَغ.
- تصنيف العناصر بقاعدة أو نموذج.
- تلخيص المحتوى الطويل للتسليم.
- توجيه العمل إلى النظام أو المالك الصحيح.

## ضوابط الحوكمة

- تحديد مالك لكل سير عمل.
- بوّابة اعتماد لأي إرسال أو كتابة خارجية.
- سجلّ تدقيق لكل تشغيلة ومدخل ومخرج.
- إجراء استرداد موثَّق.

## مؤشّرات الأداء

- Hours saved — لكل سير عمل أسبوعيًا.
- Steps reduced — قبل/بعد.
- Error rate — نسبة التشغيلات التي ترسب في الجودة.

## الخدمات

- AI Quick Win — سبرنت لسير عمل واحد.
- Workflow Automation Sprint — بناء أكثر من سير عمل.
- Monthly AI Ops — اشتراك تشغيلي متكرّر.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Workflow map | Designed automation | Delivery | Per sprint |
| Source files | Extracted / transformed data | Delivery | Per run |
| Approved output | Write to target system | Client | Per run |
| Run logs | Hours saved report | Delivery | Weekly |

## المقاييس

- Hours saved و Steps reduced (كما في المؤشّرات).
- Error rate لكل سير عمل.
- Workflow uptime — نسبة التشغيلات المجدوَلة المكتملة.

## ذات صلة

- `docs/V14_FOUNDER_DAILY_OPS.md` — مرجع التشغيل اليومي.
- `docs/ops/DAILY_OPERATING_LOOP.md` — حلقة التشغيل اليومية.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — البنية التشغيلية الحاضنة.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
