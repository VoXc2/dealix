# معالجة الارتداد وإلغاء الاشتراك (Bounce & Unsubscribe Handling)

## الارتداد (Bounce)
- ارتداد صلب (hard) → كبح فوري بسبب `bounce` أو `invalid_email`.
- ارتداد ليّن متكرر (soft ×3) → كبح `invalid_email`.
- مراقبة المعدل: تحذير 2–5%، **إيقاف** > 5%.
- مفروض عبر `classify_reply` → `route_reply` (السبب: `bounce`).

## إلغاء الاشتراك (Unsubscribe)
- أي طلب إلغاء (بريد/رد/رابط) → كبح فوري بسبب `unsubscribe`.
- تأكيد إيقاف للمستلم؛ لا رسائل لاحقة.
- إلزامي وجود مسار إلغاء واضح في كل بريد بارد.

## الردود الغاضبة / السبام
- "سبام/مزعج/بلاغ" → كبح `angry_reply` + مراجعة المؤسس.

## التوثيق
كل كبح يُسجَّل (الجهة، السبب، الوقت، المصدر) وفق `schemas/suppression.schema.json`.
الاختبارات: `test_reply_classification_actions.py`.
