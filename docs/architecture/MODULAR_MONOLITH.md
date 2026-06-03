# Modular Monolith — قرار المعمارية

**القرار الافتراضي لـ Dealix:** **Modular Monolith** — سرعة، تكلفة أقل، اختبار أسهل، حدود وحدات واضحة **داخل** نفس deployable.

## لماذا ليس microservices مبكرًا؟

- تعقيد تشغيلي قبل تحقيق الـscale  
- حوكمة ومراقبة أصعب على فرق صغيرة  
- تكلفة دمج أعلى في مرحلة إثبات الفئة  

## متى «تفصل» حدودًا؟

عندما تتكرر الأسباب: **فريق مستقل** ، **SLO مختلف** ، **حمل معزول** ، أو **متطلبات امتثال** تفرض حدًا صلبًا.

## طبقات عرض

انظر [`../company/DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md`](../company/DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md) §6 — Presentation → Application → AI Control → Governance → Data → Learning.

**خريطة كود:** [`../product/MASTER_CODE_MAP.md`](../product/MASTER_CODE_MAP.md)
