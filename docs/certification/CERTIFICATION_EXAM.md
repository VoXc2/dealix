# Certification Exam

## المكوّنات الأربعة

1. Knowledge test  
2. Case simulation  
3. Governance test  
4. QA review  

## مثال Governance Test

**سؤال:** العميل يرفع جدولًا فيه أسماء وأرقام ويطلب إرسال واتساب آليًا للبارد. ماذا تفعل Dealix؟

**إجابة صحيحة (ملخص):**

- تصنيف PII · مراجعة Source Passport وallowed use · منع cold WhatsApp automation · مسودات فقط إن وُجد أساس علاقة/موافقة · موافقة بشرية قبل أي إجراء خارجي · تسجيل قرار حوكمة.

**الكود:** `CERTIFICATION_EXAM_COMPONENTS` · `certification_exam_components_complete` — `standards_os/certification.py`

**صعود:** [`CERTIFICATION_SYSTEM.md`](CERTIFICATION_SYSTEM.md)
