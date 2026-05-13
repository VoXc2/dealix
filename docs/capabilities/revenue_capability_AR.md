# قدرة الإيرادات — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** مسؤول الإيرادات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [revenue_capability.md](./revenue_capability.md)

## السياق

قدرة الإيرادات هي أكثر بوّابات ديلِكس استخدامًا وأسرعها قياسًا. هي
موجودة لمساعدة الشركة على تحديد الفرص الإيرادية وترتيبها والعمل عليها.
يحوّل هذا الملف شكوى "عملاؤنا المحتملون فوضى" إلى سير عمل منظَّم
ومحوكَم. مرجعه `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` و
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`، ويلتزم بقواعد
`docs/DEALIX_OPERATING_CONSTITUTION.md`. يُقاس النضج عبر المرساة:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

مساعدة الشركة على تحديد فرص الإيرادات وترتيبها والعمل عليها بنتيجة
قابلة للقياس على قيمة الـPipeline ومعدّل التحويل.

## المشكلات الشائعة

- بيانات عملاء محتملين فوضى — تكرارات، حقول ناقصة، مصادر مختلطة.
- نظام CRM ضعيف — حقول غير مستخدمة، مراحل بلا انضباط، تحديث يدوي.
- ICP غير واضح — البيع يلاحق الجميع.
- لا أولويات — كل عميل يُعامَل بنفس الطريقة.
- متابعة يدوية — يضيع بين WhatsApp والبريد والاتصال.
- رؤية ضعيفة للـPipeline — قيمة الـPipeline غير موثوقة.

## المدخلات المطلوبة

- قائمة الحسابات / العملاء المحتملين (CSV أو تصدير من CRM).
- تعريف ICP.
- العرض الحالي والتسعير.
- مراحل البيع وتعريف كل مرحلة.
- إسناد المصادر.
- المخرجات السابقة إن وُجدت (فوز / خسارة / لا قرار).

## وظائف الذكاء الاصطناعي

- تنظيف البيانات وإزالة التكرار.
- تسجيل الحسابات مقابل ICP.
- تقسيم الفرص إلى شرائح بحسب المستوى والمرحلة.
- صياغة نسخ تواصل تخضع لاعتماد بشري.
- اقتراح الإجراء التالي لكل حساب.
- توليد تقرير إيرادات عند الطلب.

## ضوابط الحوكمة

- لا WhatsApp بارد، ولا أتمتة LinkedIn.
- مصدر مطلوب لكل ادّعاء في رسالة التواصل.
- مراجعة الادّعاءات قبل أي استخدام خارجي.
- بوّابة اعتماد بشري قبل أي إرسال.
- تُسجَّل في سجلّ التدقيق وفق `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## مؤشّرات الأداء

- Accounts scored — العدد والنسبة من القائمة.
- Qualified accounts — العدد الذي يجتاز عتبة ICP.
- Data quality improvement — قبل/بعد على الاكتمال والتكرار والمصدر.
- Pipeline value — قيمة بالريال مرجَّحة بمراحل الاحتمال.
- Next actions completed — عدد الإجراءات أسبوعيًا مقابل الخطّة.

## الخدمات

- Revenue Diagnostic — تقييم مدفوع للقدرة.
- Lead Intelligence Sprint — أول بناء فعلي للقدرة.
- Pilot Conversion Sprint — تشغيل سير العمل ثلاثين يومًا.
- Monthly RevOps OS — اشتراك تشغيلي متكرّر.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Lead list + ICP | Cleaned + scored list | Delivery | Per sprint |
| Top accounts | Outreach drafts | Delivery | Weekly |
| Approved drafts | Sent outreach (client owns send) | Client | Weekly |
| Pipeline events | Revenue report + next actions | Delivery | Weekly |

## المقاييس

- Accounts scored و Qualified accounts (كما في مؤشّرات الأداء).
- Data quality lift — مؤشّر مركّب من 0 إلى 100.
- Pipeline coverage — قيمة الـPipeline ÷ المستهدف.
- Sprint-to-retainer conversion لعملاء الإيرادات.

## ذات صلة

- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — الـPlaybook الذي تنفّذه القدرة.
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — نظام الإيرادات المؤتمت.
- `docs/V7_REVENUE_FACTORY_LAUNCH_BOARD.md` — لوحة الإطلاق التي تتغذّى من القدرة.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
