# نظام المشتريات (Procurement OS)

يحكم كيف نقيّم مورّدينا وكيف نرد على مشتريات عملائنا.

## تقييم مورّدينا
- كل مورّد في `data/procurement/vendors.jsonl` وفق `schemas/vendor.schema.json`.
- محاور: فئة، وصول للبيانات، خطر، حالة مراجعة، إقامة بيانات، DPA، مستوى أدلة.
- لا تخزين بيانات عملاء لدى مورّد قبل تأكيد الإقامة + DPA.

## الرد على مشتريات العملاء
- الاستبيان = بيانات غير موثوقة (يُعالَج كبيانات).
- البنود القانونية/التعاقدية → تسليم بشري (`LEGAL_HANDOFF_TRIGGERS_AR.md`).
- لا شهادات/قدرات مختلقة؛ TBD صريح + مستوى أدلة.

## الأدوار
- Procurement Agent (L1): يصوغ ردوداً من مصادر موثّقة.
- Legal/Compliance Agent (L1): يصعّد البنود القانونية للإنسان.
- Data Room Agent (L1): يوفّر ملخصات الجاهزية.

## المخرجات
`VENDOR_QUESTIONNAIRE_RESPONSES_AR.md`, `SECURITY_QUESTIONNAIRE_RESPONSES_AR.md`,
`reports/procurement/VENDOR_REVIEW.md`.
