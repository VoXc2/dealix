# قدرة العملاء — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** مسؤول نجاح العملاء
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [customer_capability.md](./customer_capability.md)

## السياق

تُمكِّن قدرة العملاء الشركة من الاستجابة بأسرع وقت وبأعلى اتّساق وباللغة
والنبرة المناسبتين. تستهدف واقع زحام WhatsApp والبريد والنماذج لدى
المنشآت السعودية، ومرجعها `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` وقواعد
المؤشّرات في `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`. يُقاس النضج عبر:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

استجابة أسرع وأكثر اتّساقًا وبلغة ونبرة سليمتين دون التفريط بالأمان.

## المشكلات الشائعة

- زحام WhatsApp — تتوقّف الردود بعد الدوام.
- FAQ مبعثرة — كل موظّف يردّ بطريقة.
- استجابة بطيئة — أول ردّ يتأخّر ساعات.
- ردود غير متّسقة — تتفاوت بين الموظّفين.

## المدخلات المطلوبة

- سجلّ الدعم (محادثات، تذاكر، بريد).
- قاعدة المعرفة (FAQ، السياسات، معلومات المنتج).
- القنوات المستخدمة (WhatsApp، بريد، ويب).
- قواعد التصعيد وتغطية المناوبة.

## وظائف الذكاء الاصطناعي

- تصنيف الرسائل بحسب القصد والأولوية.
- صياغة الردّ من قاعدة المعرفة مع اقتباس المصدر.
- التصعيد إلى البشر عند اشتراط القواعد.
- تلخيص المحادثات الطويلة لتسليم سلس.
- اقتراح إضافات لقاعدة المعرفة من الأسئلة المتكرّرة.

## ضوابط الحوكمة

- لا إرسال آلي دون اعتماد بشري (قاعدة MVP).
- الحالات الحسّاسة (قانونية، مدفوعات، شكاوى) تُحوَّل للبشر.
- كل ردّ مُصاغ يستند إلى مصدر من قاعدة المعرفة.
- سجلّ تدقيق لكل تصنيف وصياغة وإرسال.

## مؤشّرات الأداء

- Response time — دقائق حتى أول ردّ.
- Resolution time — دقائق من الورود إلى الحلّ.
- Reply quality — تقييم الجودة على النبرة والدقّة والاستشهاد.
- Escalation rate — نسبة المحادثات المُصعَّدة.

## الخدمات

- AI Support Desk — أول بناء فعلي.
- Monthly Support AI — اشتراك تشغيلي متكرّر.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Inbound message | Classification + draft | Delivery (agent) | Real-time |
| Draft + approval | Sent reply | Client agent | Real-time |
| Resolved tickets | Quality + escalation report | Delivery | Weekly |
| Repeated questions | KB proposals | Delivery | Monthly |

## المقاييس

- Response time و Resolution time (كما في المؤشّرات).
- Reply QA score من 0 إلى 100.
- Escalation rate بحسب الفئة.
- KB freshness — الأيام منذ آخر مراجعة.

## ذات صلة

- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — الـPlaybook الذي تنفّذه القدرة.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — تعريف المؤشّرات.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — السياق الاستراتيجي.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
