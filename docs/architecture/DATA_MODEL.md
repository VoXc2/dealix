# Data Model — اتجاه البيانات (عالي المستوى)

## المبادئ

1. **المصدر أولًا** — كل artifact يرتبط بـ `source_id` حيث ينطبق.  
2. **الحد الأدنى من الاشتقاق** — لا حقول PII زائدة في مسارات AI.  
3. **امتثال PDPL-aware** — غرض، أساس قانوني، احتفاظ، عبر الحدود — انظر [`../governance/PDPL_DATA_RULES.md`](../governance/PDPL_DATA_RULES.md).  
4. **أحداث للتدقيق** — تغييرات حساسة تُسجّل كـ events — [`EVENT_MODEL.md`](EVENT_MODEL.md).

## كيانات مرجعية (أسماء منطقية)

- Client / Project / ServiceRun  
- Dataset · Document · SourcePassport  
- ProofPack · ProofEvent · ValueMetric  
- CapitalAsset · PlaybookVersion  
- AuditEvent · Approval · AI_run  

**تفاصيل مخطط المنتج:** [`../product/MVP_DATA_MODEL.md`](../product/MVP_DATA_MODEL.md)

## Source Registry

[`../ledgers/SOURCE_REGISTRY.md`](../ledgers/SOURCE_REGISTRY.md)
