# سجل المصادر المعتمدة لوثائق Dealix (Canonical Registry)

**الغرض:** تحديد **المصدر المعتمد** لكل مجال ومنع الالتباس بين المجلدات المكررة أو التاريخية. لا يعني هذا حذف المجلدات الأخرى؛ يعني أن القرار والعروض والتسليم يَصدر من الصف المُعرَّف `canonical` هنا.

**المبدأ:** التصنيف فوق إعادة الهيكلة — راجع [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md).

| المجال | المصدر المعتمد | ملفات داعمة / مرآة | الحالة | ملاحظات |
|--------|----------------|---------------------|--------|---------|
| بوابة الوثائق | [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md) | [_generated/docs_top_level_snapshot.json](_generated/docs_top_level_snapshot.json) | CANONICAL | مدخل القراءة الرئيسي |
| خارطة التنفيذ | [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md) | [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md) | CANONICAL | يربط الموجات بالقيمة |
| مصفوفة العروض (26–44) | [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md) | [../26_service_catalog/](../26_service_catalog/) | CANONICAL | سعر / مدة / مستبعد |
| كتالوج الخدمات التفصيلي | [../26_service_catalog/](../26_service_catalog/) | [../26_human_amplified/](../26_human_amplified/) | CANONICAL | التجاري أولًا؛ المرآة للسياق |
| Change Requests ونطاق التوسع | [../28_change_requests/](../28_change_requests/) | [../28_operating_finance/](../28_operating_finance/) | CANONICAL | CR و Retainer backlog |
| التسعير التجاري | [../30_pricing/](../30_pricing/) | [../30_standards/](../30_standards/) | CANONICAL | السعر والحزم |
| جاهزية مؤسسية / Trust للبيع | [../32_enterprise_readiness/](../32_enterprise_readiness/) | [../32_ecosystem/](../32_ecosystem/) | CANONICAL | بعد بوابة BU4 |
| AI Estate | [../34_ai_estate/](../34_ai_estate/) | [../34_market_power/](../34_market_power/) | CANONICAL | جرد وحوكمة استخدامات |
| الشركاء وترخيص IP | [../40_partners/IP_LICENSE_OUTLINE_AR.md](../40_partners/IP_LICENSE_OUTLINE_AR.md) | [../40_partners/PARTNER_COVENANT.md](../40_partners/PARTNER_COVENANT.md) | CANONICAL | عقد منفصل عن SaaS |
| بوابة بيع BU4 Trust | [../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md) | [../14_trust_os/](../14_trust_os/) | CANONICAL | N عملاء قبل البيع |
| حزمة إثبات السوق | [../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md) | Revenue Intelligence API | ACTIVE | مسار حي 5 عملاء |
| Retainer مصغّر | [../commercial/RETAINER_PILOT_MINI_AR.md](../commercial/RETAINER_PILOT_MINI_AR.md) | [../13_workflow_os/MONTHLY_VALUE_REPORT.md](../13_workflow_os/MONTHLY_VALUE_REPORT.md) | ACTIVE | بوابات Proof/Adoption |
| لقطة فهرس المجلدات | [_generated/docs_top_level_snapshot.json](_generated/docs_top_level_snapshot.json) | `scripts/generate_docs_hub_snapshot.py` | GENERATED | يُحدّث شهريًا أو عند تغيير كبير |
| حوكمة الذاكرة (هذا الملف + الإخوة) | [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md) | [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md)، [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md) | CANONICAL | طبقة الحكم على الوثائق |

## ربط سريع

- [سجل القيمة القابضة](HOLDING_VALUE_REGISTRY_AR.md)
- [سياسة الأرشفة](DOCS_ARCHIVE_POLICY_AR.md)
- [قائمة مراجعة الأرشفة](ARCHIVE_REVIEW_QUEUE_AR.md)
- [الحزم الخارجية المعتمدة](EXTERNAL_PACK_REGISTRY_AR.md)
- [قواعد القرار](DOCS_DECISION_RULES_AR.md)
