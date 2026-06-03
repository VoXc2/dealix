# نظام الخدمات المُنتَجة (Productized Services OS)

كل خدمة مُعرّفة كبيانات في `data/productized_services/services.yaml` وتُتحقَّق ضد
`schemas/productized_service.schema.json` (اختبار `tests/test_schemas_and_data.py`).

## الحقول الإلزامية لكل خدمة
`name, buyer, pain, promise, deliverables, timeline, price_range, scope,
out_of_scope, acceptance_criteria, evidence_level, risks, upsell_path, renewal_path`.

## قواعد
- **الوعد آمن:** بلا ضمانات/مبالغة (يُفحص بكاشف الادعاءات).
- **السعر نطاق فقط:** السعر النهائي بموافقة بشرية.
- **النطاق محكوم:** `out_of_scope` صريح لمنع الانزلاق.
- **العرض ↔ الكتالوج:** أي عرض يرتبط بخدمة هنا (`evaluate_proposal`).
- **التجديد بقيمة:** مسار التجديد يتطلب قيمة مُسلّمة.

## الخدمات الحالية
P1 Revenue Intelligence Sprint · P2 AI Sales Ops Retainer
(انظر `SERVICE_CATALOG_AR.md`).
