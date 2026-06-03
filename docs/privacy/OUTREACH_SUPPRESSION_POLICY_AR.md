# سياسة الكبح في التواصل (Outreach Suppression Policy)

قائمة الكبح هي بوابة لا يمكن تجاوزها: أي جهة عليها **لا تُراسَل أبداً**.

## أنواع الكبح (مفروضة في `core/safety/constants.py` و`schemas/suppression.schema.json`)
`unsubscribe · bounce · angry_reply · do_not_contact · legal_request ·
privacy_request · duplicate_risky · invalid_email`

## قواعد
1. **إضافة فقط (append-only):** لا يحذف أي وكيل إدخالاً من القائمة.
2. **دائمة للأنواع الحسّاسة:** `do_not_contact / legal_request / privacy_request` دائمة.
3. **تلقائية من الردود:** غاضب/إلغاء/ارتداد → كبح فوري (`route_reply`).
4. **تطبيق قبل أي إرسال:** `SuppressionList.can_send()` تُفحص دائماً.
5. **لا تجاوز:** `bypass_suppression` ضمن الإجراءات الممنوعة لكل الوكلاء.

## التدفق
```
رد/ارتداد/طلب → تحديد السبب → SuppressionList.add(contact, reason) → سجل
أي مسودة لاحقة لنفس الجهة → assess_outreach → recipient_suppressed → block
```

## التحقق
الاختبارات: `test_suppression_blocks_sending.py`,
`test_outreach_suppression_blocks_send.py`. المراجعة:
`reports/privacy/SUPPRESSION_REVIEW.md`.
