# قدرة الحوكمة — طبقة مصنع قدرات الذكاء الاصطناعي

**الطبقة:** L4 · مصنع قدرات الذكاء الاصطناعي
**المالك:** المؤسس / الالتزام
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [governance_capability.md](./governance_capability.md)

## السياق

تُمكِّن قدرة الحوكمة الشركة من استخدام الذكاء الاصطناعي بأمان وبموافقات
صريحة وسجلّ تدقيق كامل. وهي التعبير التشغيلي عن
`docs/DEALIX_OPERATING_CONSTITUTION.md` وانضباط الحوادث في
`docs/ops/INCIDENT_RUNBOOK.md` والموقف أمام الجهات التنظيمية في
`docs/ops/PDPL_BREACH_RUNBOOK.md`. يُقاس النضج عبر:
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## الغاية التجارية

استخدام الذكاء الاصطناعي بأمان — موافقات وسجلّات واستجابة حوادث — بحيث
يمكن الدفاع عن كل إجراء أمام جهة تنظيم أو مدقّق أو مجلس.

## المشكلات الشائعة

- لا سياسة استخدام للذكاء الاصطناعي.
- لا مسار موافقات قبل الإجراء الخارجي.
- لا سجلّ تدقيق.
- لا سجلّ مخاطر.

## المدخلات المطلوبة

- الأدوات المستخدمة حاليًا.
- تدفّقات البيانات والتكاملات.
- مالكون لكل نظام وكل سير عمل.

## وظائف الذكاء الاصطناعي

- تطبيق قواعد كأكواد على كل تشغيلة.
- مراقبة انتهاكات السياسات.
- إخفاء بيانات الأفراد قبل التخزين أو الإرسال.
- التصعيد عند تعارض القاعدة.

## ضوابط الحوكمة

- Rules-as-code داخل بيئة التشغيل.
- اختبارات قبل أي ترقية.
- Playbook حوادث جاهز للتشغيل.
- مراجعة حوكمة ربع سنوية.

## مؤشّرات الأداء

- Blocked actions — العدد وتوزيع الأسباب.
- Approvals logged — عدد الموافقات البشرية.
- Incident count — الإجمالي وبحسب الخطورة.

## الخدمات

- AI Readiness Review — تقييم مدفوع.
- AI Usage Policy — سياسة مكتوبة + تدريب.
- Governance Program — اشتراك حوكمة متكرّر.

## الواجهات

| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| Tool / data inventory | Risk register | Delivery | Per assessment |
| Policy draft | Approved policy + training | Client | Per engagement |
| Runtime events | Blocked actions report | Runtime | Real-time |
| Incident | Postmortem + fix | Delivery | Per incident |

## المقاييس

- Blocked actions و Approvals logged (كما في المؤشّرات).
- Mean time to detect / respond / resolve.
- Policy coverage — نسبة الاستخدام المُغطَّى بسياسة مكتوبة.

## ذات صلة

- `docs/DEALIX_OPERATING_CONSTITUTION.md` — الدستور الذي تُنفّذه القدرة.
- `docs/ops/INCIDENT_RUNBOOK.md` — انضباط الحوادث.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — الاستجابة أمام الجهات التنظيمية.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — مرساة النضج (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي للطبقات.

## سجل التغييرات

| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
