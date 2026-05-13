# قدرة البيانات — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** مسؤول البيانات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [data_capability.md](./data_capability.md)

## السياق

تهيّئ قدرة البيانات بيانات العميل لاستخدام الذكاء الاصطناعي ولاتّخاذ
القرارات. وهي البوّابة التي تعتمد عليها بقيّة القدرات: بيانات فوضى =
ذكاء غير آمن. مرجعها `docs/BEAST_LEVEL_ARCHITECTURE.md` و
`docs/DPA_DEALIX_FULL.md` و`docs/DATA_RETENTION_POLICY.md`. يُقاس
النضج عبر:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

تهيئة البيانات للذكاء والقرار: حقول معروفة، مصادر معروفة، مالكون معروفون.

## المشكلات الشائعة

- تكرارات وسجلّات غير متّسقة.
- حقول ناقصة.
- مصادر مبعثرة بلا مالك معتمد.
- لا سياسات احتفاظ أو بيانات أفراد.

## المدخلات المطلوبة

- مجموعات بيانات خام (CSV، صادرات، جداول).
- مخطّطات (أو الإشارة إلى غيابها).
- وسوم الحسّاسية.

## وظائف الذكاء الاصطناعي

- تسجيل جودة لكل سجلّ وحقل.
- إزالة التكرار.
- تصنيف بحسب نوع السجلّ.
- اقتراح إغناء مع اقتباس المصدر.

## ضوابط الحوكمة

- معالجة بيانات الأفراد وفق `docs/DPA_DEALIX_FULL.md`.
- إدراج كل مجموعة في سجلّ المصادر.
- قاعدة احتفاظ لكل مجموعة وفق `docs/DATA_RETENTION_POLICY.md`.

## مؤشّرات الأداء

- Quality score قبل/بعد — مركّب من 0 إلى 100.
- Gap closure rate — نسبة الفجوات المُغلَقة لكل سبرنت.

## الخدمات

- Data Readiness Assessment — تقييم مدفوع.
- Data Cleanup — سبرنت إصلاح.
- Data OS — اشتراك تشغيلي للبيانات.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Raw datasets | Quality score + gap list | Delivery | Per sprint |
| Approved fixes | Cleaned dataset | Delivery | Per sprint |
| Source list | Source registry entries | Delivery | Per dataset |
| Retention rule | Applied retention | Delivery | Monthly |

## المقاييس

- Quality score lift (كما في المؤشّرات).
- Gap closure rate.
- PII-flagged records resolved.

## ذات صلة

- `docs/BEAST_LEVEL_ARCHITECTURE.md` — البنية الحاضنة للبيانات.
- `docs/DPA_DEALIX_FULL.md` — اتفاقية المعالجة وقواعد بيانات الأفراد.
- `docs/DATA_RETENTION_POLICY.md` — سياسة الاحتفاظ.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
