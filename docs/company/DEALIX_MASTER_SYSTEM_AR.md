# Dealix Master System — الأنظمة الثمانية

**قاعدة الاحتراف:** [`COMPANY_PROFESSIONALISM_AR.md`](COMPANY_PROFESSIONALISM_AR.md) — **نواة التشغيل اليومي:** [`DEALIX_OPERATING_KERNEL.md`](DEALIX_OPERATING_KERNEL.md) — [`DECISION_RULES.md`](DECISION_RULES.md) — [`SERVICE_REGISTRY.md`](SERVICE_REGISTRY.md) — **نموذج الطبقات السبع:** [`DEALIX_OPERATING_MODEL_7_LAYERS_AR.md`](DEALIX_OPERATING_MODEL_7_LAYERS_AR.md) — **منهجية التشغيل:** [`DEALIX_METHOD_AR.md`](DEALIX_METHOD_AR.md) — **رؤية AI OS طويلة المدى:** [`DEALIX_AI_OS_LONG_TERM_AR.md`](DEALIX_AI_OS_LONG_TERM_AR.md) — **نية محركات التسليم:** [`../product/DELIVERY_ENGINES_INTENT_AR.md`](../product/DELIVERY_ENGINES_INTENT_AR.md).

كل **خدمة** تمر عبر هذه الأنظمة قبل البيع الرسمي والتسليم. الربط بالوثائق والكود في الريبو:

| النظام | الوثائق | الكود / التحقق |
|--------|---------|----------------|
| **1. Market** | [`docs/strategy/MARKET_MAP_SAUDI.md`](../strategy/MARKET_MAP_SAUDI.md)، [`VERTICAL_PLAYBOOKS.md`](../strategy/VERTICAL_PLAYBOOKS.md)، [`ICP.md`](ICP.md) | تحليل قطاعات (لاحقاً) |
| **2. Offer** | [`SERVICE_CATALOG.md`](SERVICE_CATALOG.md)، [`PRICING.md`](PRICING.md)، [`docs/services/*/offer.md`](../services/) | [`service_readiness`](../../auto_client_acquisition/delivery_os/service_readiness.py) + YAML |
| **3. Delivery** | [`docs/delivery/`](../delivery/)، قوائم التحقق لكل خدمة | [`delivery_os`](../../auto_client_acquisition/delivery_os/)، [`readiness_gates`](../../auto_client_acquisition/delivery_os/readiness_gates.py) |
| **4. Product** | [`docs/product/MODULE_MAP.md`](../product/MODULE_MAP.md) | `data_os`, `revenue_os`, `governance_os`, `reporting_os`, `knowledge_os`, واجهات API |
| **5. Quality** | [`docs/quality/`](../quality/) | بوابات QA، اختبارات pytest، حد أدنى تسليم |
| **6. Governance** | [`docs/governance/`](../governance/) | [`governance_os`](../../auto_client_acquisition/governance_os/)، [`compliance_os`](../../auto_client_acquisition/compliance_os/) |
| **7. Proof** | `proof_pack_template.md` لكل خدمة | [`reporting_os`](../../auto_client_acquisition/reporting_os/)، [`executive_reporting`](../../auto_client_acquisition/executive_reporting/) |
| **8. Growth** | [`docs/sales/`](../sales/)، `upsell.md` لكل خدمة | سكربت [`verify_full_mvp_ready.py`](../../scripts/verify_full_mvp_ready.py) — أصول مبيعات دنيا |

مرجع التحقق من القدرة على التشغيل: [`CAPABILITY_VERIFICATION_AR.md`](CAPABILITY_VERIFICATION_AR.md). **بوابات الجاهزية (Pass/Fix):** [`DEALIX_STAGE_GATES_AR.md`](DEALIX_STAGE_GATES_AR.md) و[`../../DEALIX_READINESS.md`](../../DEALIX_READINESS.md) وسكربت [`verify_dealix_ready.py`](../../scripts/verify_dealix_ready.py). **نظام الأدلة:** [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md).
