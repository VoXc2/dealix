# سجل الحزم الخارجية لـ Dealix

**الغرض:** منع الإرسال العشوائي للوثائق وتحويل الذاكرة إلى **حزم آمنة** قابلة للاستخدام في البيع والشراكة والتمويل والتشغيل.

## القاعدة

لا تُرسل أي وثيقة خارج Dealix إلا إذا كانت:

- ضمن **حزمة خارجية معتمدة** في الجدول أدناه، أو  
- مصنّفة صراحةً في [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md) **وبموافقة المؤسس**.

## الحزم المعتمدة

| الحزمة | الجمهور | الملفات | التصنيف | آخر مراجعة | ملاحظات |
|--------|---------|---------|---------|-------------|---------|
| Partner Intro Pack | شريك | [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md)، [../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md)، [../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md)، [../40_partners/IP_LICENSE_OUTLINE_AR.md](../40_partners/IP_LICENSE_OUTLINE_AR.md) | Partner-safe | TBD | لا يحتوي بيانات عميل أو pipeline خاص |
| Investor Diligence Lite | مستثمر | [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md)، [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md)، [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md)، [../investment/FUNDING_READINESS.md](../investment/FUNDING_READINESS.md) (حتى إنشاء `USE_OF_FUNDS.md` إن لزم) | Investor-safe | TBD | نسخة خفيفة قبل data room |
| Client Proof Demo Pack | عميل | [../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md)، [../commercial/RETAINER_PILOT_MINI_AR.md](../commercial/RETAINER_PILOT_MINI_AR.md) | Client-facing | TBD | للاجتماع الأول أو demo |
| Operator Onboarding Pack | مشغّل داخلي | [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md)، [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md)، [DOCS_READING_PACKS_AR.md](DOCS_READING_PACKS_AR.md)، [../27_delivery_playbooks/](../27_delivery_playbooks/) | Internal-only | TBD | **لا يُرسل خارجيًا** |
| Enterprise Trust Pack Lite | عميل enterprise / شريك assurance | [../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md)، مجلد [../enterprise_trust/](../enterprise_trust/)، [../32_enterprise_readiness/](../32_enterprise_readiness/) | Partner-safe / Client-facing | TBD | قبل أي مشاركة: فحص أسرار ومطابقة [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md) |

## قرار الإرسال

قبل الإرسال:

1. تحقق من **التصنيف** (Publication boundary).
2. تحقق أن الحزمة **لا تحتوي أسرارًا** (مفاتيح، بيانات عملاء، pipeline خاص).
3. تحقق أنها **لا تدعي اعتمادًا تنظيميًا** مبالغًا فيه.
4. **سجّل** الاستخدام في [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json) (`entries`).

**قاعدة القيمة:** *No usage, no commercial evidence* — الأصل لا يُحدَّث بـ «Evidence» في السجل قبل إدخال حقيقي في سجل الاستخدام.

## مراجع

- حزم قراءة مختصرة: [packs/PARTNER_READING_PACK_AR.md](packs/PARTNER_READING_PACK_AR.md) · [packs/INVESTOR_READING_PACK_AR.md](packs/INVESTOR_READING_PACK_AR.md) · [packs/OPERATOR_READING_PACK_AR.md](packs/OPERATOR_READING_PACK_AR.md)
- [DOCS_DECISION_RULES_AR.md](DOCS_DECISION_RULES_AR.md)
