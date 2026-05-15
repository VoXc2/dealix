# Cross-Layer Validation — Dealix Revenue OS

## الهدف

ضمان أن كل تشغيل للـ workflow يمر عبر جميع الطبقات الحرجة وليس فقط طبقة الذكاء.

## الطبقات المطلوبة لكل تشغيل

1. Trigger layer
2. Workflow orchestration layer
3. Agent decision layer
4. Governance layer
5. Execution integration layer (CRM)
6. Observability layer
7. Evals layer
8. ROI reporting layer

## مصفوفة التحقق

| Layer | Validation سؤال | Evidence مطلوب |
|------|------------------|----------------|
| Trigger | هل الـ trigger موثق ومعروف المصدر؟ | event id + trigger payload |
| Workflow | هل جميع steps نفذت بالترتيب والسياسات؟ | workflow run log |
| Agent | هل القرار مدعوم بـ citations؟ | decision + citations list |
| Governance | هل مرّ عبر risk/policy/approval؟ | risk score + policy result + approval record |
| Execution | هل تم تنفيذ التحديث في CRM بشكل صحيح؟ | CRM response + idempotency key |
| Observability | هل يوجد trace كامل؟ | trace id + metrics snapshot |
| Evals | هل quality/compliance pass؟ | eval report id |
| ROI | هل تم تحديث metric business impact؟ | ROI delta record |

## قواعد إلزامية

- أي تشغيل بدون `trace_id` يعتبر فشل حوكمة.
- أي قرار بدون citation للمعرفة يعتبر "نقص جودة" ويمنع auto-execution.
- أي تنفيذ CRM بدون `approval_ref` في الحالات عالية المخاطر يعتبر مخالفة.

## سيناريو الاختبار المرجعي (Reference Drill)

يجب تشغيل السيناريو التالي في كل بيئة:

1. إدخال lead جديد.
2. تشغيل qualification + scoring.
3. إنشاء رد مقترح.
4. طلب موافقة بشرية.
5. تنفيذ تحديث CRM.
6. التحقق من trace + eval + ROI record.

النجاح لا يُحتسب إلا عند نجاح الخطوات الست جميعًا.
