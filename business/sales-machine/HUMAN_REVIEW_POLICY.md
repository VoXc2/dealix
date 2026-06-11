# Human Review Policy (Dealix)

## القاعدة الذهبية
**لا مسوّدة تُرسل قبل أن يوافق عليها المؤسس.** هذه ليست توصية، هذه قاعدة معمارية.

## من يوافق
- **المؤسس فقط.** لا وكيل، لا بوت، لا script.

## ما يحتاج موافقة
- أي رسالة WhatsApp تنوي إرسالها
- أي رسالة بريد إلكتروني لعميل محتمل
- أي رسالة LinkedIn لشخص لا تعرفه
- أي رسالة SMS أو ما يعادلها

## ما لا يحتاج موافقة
- تحديث stage في CRM
- إضافة note لملف حساب
- توليد تقرير داخلي
- أي عملية على بيانات demo
- أي قراءة لبيانات عامة

## كيف نسجّل القرار
- `review_status = "approved"` + `reviewer` + `reviewed_at`
- `review_status = "rejected"` + `reviewer` + `rejection_reason`
- لا يُحذف أي draft — نُؤرشف لنتعلم منه

## كيف نمنع الإرسال التلقائي
- لا يوجد import لـ `twilio`, `sendgrid`, أو ما يعادلها في sales scripts
- لا `send_*` بدون `review_status == "approved"`
- لا `auto_send=True` في أي مكان
- اختبار CI: `tests/test_no_auto_send.py` يفشل البناء إذا لقي إرسال آلي
