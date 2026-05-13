# قدرة المعرفة — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** مسؤول المعرفة / التسليم
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [knowledge_capability.md](./knowledge_capability.md)

## السياق

تحوّل قدرة المعرفة وثائق الشركة المبعثرة إلى إجابات موثَّقة وقابلة
للحوكمة. وهي الصيغة التشغيلية لعرض "Company Brain"، وتعتمد على
خيارات الحزمة في `docs/AI_STACK_DECISIONS.md` واستراتيجية التوجيه في
`docs/AI_MODEL_ROUTING_STRATEGY.md` وانضباط التقييم في
`docs/AI_OBSERVABILITY_AND_EVALS.md`. يُقاس النضج عبر:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

تحويل المعرفة المبعثرة إلى إجابات موثَّقة المصدر يثق بها الموظف والعميل.

## المشكلات الشائعة

- وثائق غير قابلة للاكتشاف بين الأقراص والدردشات.
- معلومات متضاربة بين النسخ.
- إجابات بلا مصدر.

## المدخلات المطلوبة

- وثائق مُعتمَدة مع مالك لكلٍّ منها.
- وسوم حسّاسية لكل وثيقة.
- قواعد وصول (من يرى ماذا).

## وظائف الذكاء الاصطناعي

- استيعاب الوثائق والبيانات الوصفية.
- بناء فهرس للاسترجاع.
- استرجاع أفضل المقاطع لكل استعلام.
- الإجابة مع اقتباس صريح للمقطع المصدر.

## ضوابط الحوكمة

- مصدر مطلوب لكل إجابة، ولا إجابة بلا مصدر.
- مرآة الوصول — لا يعيد الذكاء الاصطناعي محتوى لا يحقّ للمستخدم رؤيته.
- متابعة التحديث — تُعلَّم الوثائق المتقادمة.
- سجلّ تدقيق لكل استرجاع وإجابة.

## مؤشّرات الأداء

- Indexed docs — العدد والنسبة من المجموعة المُعتمَدة.
- Citation rate — نسبة الإجابات ذات الاقتباس الصحيح.
- Search time reduction — دقائق موفَّرة لكل استعلام مقارنة بخطّ الأساس.

## الخدمات

- Company Brain Sprint — أول بناء فعلي.
- Brain Management Retainer — اشتراك تشغيلي متكرّر.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Approved docs | Indexed corpus | Delivery | Per sprint |
| User query | Cited answer | Runtime | Real-time |
| Stale doc flag | Refresh task | Client owner | Weekly |
| Eval results | Answer-quality report | Delivery | Weekly |

## المقاييس

- Indexed docs و Citation rate (كما في المؤشّرات).
- Answer accuracy من نتائج التقييم — نسبة النجاح.
- Freshness — وسيط عمر الوثائق المقتبَسة.

## ذات صلة

- `docs/AI_STACK_DECISIONS.md` — خيارات الحزمة التقنية.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — توجيه النماذج.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — انضباط التقييم.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
