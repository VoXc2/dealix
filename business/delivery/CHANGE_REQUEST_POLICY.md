# Change Request Policy (Dealix)

## القاعدة
كل تغيير في النطاق لازم يمر بسجل، حتى لو صغير.

## متى يفتح Change Request
- إضافة output جديد لم يكن في الـ Proposal
- تمديد الجدول الزمني
- تغيير في owners
- تغيير في owners بعد بدء التنفيذ

## متى لا يفتح
- تعديل copy داخل output موجود
- إعادة ترتيب مراحل
- إضافة metric كان مذكور ضمناً

## كيف نسجل
- `business/_data/change_requests.json`
- Status: open / accepted / rejected / implemented
- Impact: time / cost / risk
- Owner: المؤسس

## كيف نتفاوض
- نظهر trade-off: وقت أو تكلفة أو نطاق
- القرار خلال 48 ساعة، لا تأجيل
- لا تغيير بدون توقيع العميل
