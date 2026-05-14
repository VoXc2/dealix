# حزمة قراءة المستثمر — سياق قصير

**الجمهور:** مستثمر / مستشار — **بعد** طلب diligence أو اجتماع معلوماتي.

## 1. ما يُرسل

1. [../HOLDING_DOCS_HUB_AR.md](../HOLDING_DOCS_HUB_AR.md) — بنية الذاكرة التشغيلية.
2. [../HOLDING_VALUE_REGISTRY_AR.md](../HOLDING_VALUE_REGISTRY_AR.md) — أصول ذات درجات قابضة.
3. [../DEALIX_EXECUTION_WAVES_AR.md](../DEALIX_EXECUTION_WAVES_AR.md) — موجات تنفيذ مقترنة بالكود.
4. [../DOCS_CANONICAL_REGISTRY_AR.md](../DOCS_CANONICAL_REGISTRY_AR.md) — مصدر معتمد لكل مجال (يقلل الالتباس).

**اختياري عند الطلب:** ملخصات من `docs/investment/` بعد تصنيفها **Investor-safe** يدويًا.

## 2. لماذا

إظهار **Operating Memory Infrastructure** قابلة للتحقق (اختبارات، سكربتات، CI) وليس مجلدًا عشوائيًا.

## 3. كيف يُستخدم المستثمر

- يربط الأسئلة بأعمدة **Revenue / Trust / Holding** في السجل.
- يطلب مخرجات **ملخص JSON** إن لزم: [../_generated/holding_value_summary.json](../_generated/holding_value_summary.json).

## 4. ما لا يُرسل

- روابط pipeline داخلية، تسعير خام حساس، بيانات عملاء.
- حزم شريك كاملة دون تصفية — راجع [../DOCS_PUBLICATION_BOUNDARY_AR.md](../DOCS_PUBLICATION_BOUNDARY_AR.md).

**السجل الرسمي:** [../EXTERNAL_PACK_REGISTRY_AR.md](../EXTERNAL_PACK_REGISTRY_AR.md).
