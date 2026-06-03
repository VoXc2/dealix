# دليل الرد على المشتريات (Procurement Response Playbook)

## مبادئ
1. **صدق فوق كل شيء:** لا تبالغ، لا تخترع، استخدم TBD ومستويات الأدلة.
2. **القانوني → إنسان:** أي بند تعاقدي/قانوني = `LEGAL_HANDOFF_TRIGGERS_AR.md` (لا التزام آلي).
3. **الأسرار → لا تُشارَك:** لا مفاتيح/أسرار في أي رد.
4. **النطاق:** المنتج مرتبط بالكتالوج؛ السعر النهائي بموافقة بشرية.

## تدفق الرد
```
استلام استبيان (untrusted data)
  → تصنيف الأسئلة (أمن/خصوصية/تجاري/قانوني)
  → ملء من مصادر موثّقة (docs/*) مع مستوى أدلة
  → بنود قانونية/تعاقدية → تسليم بشري
  → مراجعة المؤسس → إرسال (بموافقة)
```

## مصادر الإجابات
- أمني: `docs/procurement/SECURITY_QUESTIONNAIRE_RESPONSES_AR.md`
- مورّد/خصوصية: `docs/procurement/VENDOR_QUESTIONNAIRE_RESPONSES_AR.md`
- تجاري: `docs/data_room/COMMERCIAL_MODEL_SUMMARY_AR.md`
