# فهرس القابضة — بوابة موحّدة لوثائق Dealix

**الغرض:** تحويل «كثافة الملفات» إلى **مسار قراءة وتسليم وبيع**. هذا الملف محور تنقل؛ التفاصيل العددية المحدّثة لكل مجلد في الجذر تُستخرج آليًا في اللقطة: [`_generated/docs_top_level_snapshot.json`](_generated/docs_top_level_snapshot.json) (شغّل `py -3 scripts/generate_docs_hub_snapshot.py` بعد إضافة مجلدات كبيرة).

**قاعدة:** وثيقة بدون عرض وسعر في سياق العميل = تكلفة داخلية؛ راجع [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md).

## حوكمة الذاكرة والأصول القابضة (Holding Memory & Capital Asset OS)

من **فهرس قابل للتصفح** إلى **سجل قابل للحكم والقيمة**:

| الوثيقة | الدور |
|---------|--------|
| [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md) | المصدر المعتمد لكل مجال (canonical vs مرآة). |
| [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) | درجات قيمة: Revenue / Trust / Delivery / Partner / Investor / Holding. |
| [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md) | حالات CANONICAL، LEGACY، DEPRECATED، … بدون نقل جماعي. |
| [DOCS_ASSET_LIFECYCLE_AR.md](DOCS_ASSET_LIFECYCLE_AR.md) | دورة حياة من Draft إلى Archived. |
| [DOCS_REVIEW_CADENCE_AR.md](DOCS_REVIEW_CADENCE_AR.md) | إيقاع أسبوعي/شهري/ربع سنوي + أوامر التحقق. |
| [DOCS_READING_PACKS_AR.md](DOCS_READING_PACKS_AR.md) | حزم قراءة: مؤسس، شريك، مستثمر، مشغّل، مهندس. |
| [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md) | ما يُنشر وما يبقى داخليًا. |
| [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) | حزم خارجية معتمدة (شريك / مستثمر / عميل) + سجل إرسال. |
| [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md) | طابور مراجعة أرشفة بدون نقل أو حذف. |
| [DOCS_DECISION_RULES_AR.md](DOCS_DECISION_RULES_AR.md) | قواعد: إنشاء / تحديث / أرشفة / نشر خارجي. |
| [OS_ASSET_OPERATING_MODEL_AR.md](OS_ASSET_OPERATING_MODEL_AR.md) | الإطار الخمسي فوق الذاكرة: Evidence، Motion، Conversion، Trust، Capital allocation. |
| [MARKET_SIGNAL_OPERATING_LOOP_AR.md](MARKET_SIGNAL_OPERATING_LOOP_AR.md) | حلقة إشارات السوق: من L4 إلى قرار (متابعة، تصنيف، archetype، تحويل) — *evidence register*. |
| [FOUNDER_SIGNAL_ROADMAP_AR.md](FOUNDER_SIGNAL_ROADMAP_AR.md) | رودماب **Founder Signal → Product Spine**: مراحل P0–P7، بوابات، ممنوعات، DoD؛ يكمل [FULL_MARKET_PROOF_RUN_AR.md](FULL_MARKET_PROOF_RUN_AR.md). |
| [FULL_MARKET_PROOF_RUN_AR.md](FULL_MARKET_PROOF_RUN_AR.md) | Command Center: Full Market Proof Run + Signal + **Founder Signal Command** + Founder Command Execution + **War Room يومي**؛ PARTNER‑001→003. |

**تحقق آلي:** `py -3 scripts/validate_docs_governance.py` — المخرجات: `PASS` / `FAIL`. **ملخص الأصول:** `py -3 scripts/generate_holding_value_summary.py` → [_generated/holding_value_summary.json](_generated/holding_value_summary.json) و[_generated/asset_activation_priorities.json](_generated/asset_activation_priorities.json) و[_generated/asset_evidence_summary.json](_generated/asset_evidence_summary.json) و[_generated/asset_capital_allocation.json](_generated/asset_capital_allocation.json). **CI:** يمرّ البوابة في `ci.yml`.

---

## تشغيل الأصول بعد الفهرسة (Holding Memory Activation)

بعد تحديد المصادر المعتمدة والقيمة القابضة، تُفعَّل الذاكرة بهذه الملفات — **قرارات يومية** لا مجرد قراءة:

| الملف | الغرض |
|-------|--------|
| [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) | يحدد الحزم المسموح إرسالها خارجيًا فقط. |
| [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md) | يمنع النقل/الحذف العشوائي؛ طابور تصنيف أولًا. |
| [DOCS_DECISION_RULES_AR.md](DOCS_DECISION_RULES_AR.md) | يمنع تضخم الوثائق؛ سؤال sell/deliver/govern/… |
| [../../data/docs_asset_usage_log.json](../../data/docs_asset_usage_log.json) | يسجل الاستخدام التجاري والتشغيلي؛ *No usage, no commercial evidence*. |

**مرحلة التشغيل:** أرسل **Partner Intro Pack** من السجل ثم أضف عنصرًا في `entries` بالسجل؛ حدّث عمود **LastUsed** في [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) عند أول استخدام حقيقي.

---

## تشغيل الأصول القابضة

بعد حوكمة الذاكرة، تُستخدم هذه الملفات لتحويل الوثائق إلى **حركة** (شريك / مستثمر / عميل / تسليم):

| الملف | الغرض |
|-------|--------|
| [ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md) | يحدد متى يُحسب استخدام الأصل ومتى تُرفع درجات القيمة. |
| [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md) | درجات إثبات L0–L7؛ holding-grade مقابل commercial-grade. |
| [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) | الحزم الخارجية المعتمدة وسجل الإرسال. |
| [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md) | أرشفة مُحكومة بدون كسر الروابط. |
| [packs/PARTNER_MOTION_PACK_AR.md](packs/PARTNER_MOTION_PACK_AR.md) | حزمة شريك تنفيذية معتمدة. |
| [packs/INVESTOR_MOTION_PACK_AR.md](packs/INVESTOR_MOTION_PACK_AR.md) | حزمة مستثمر خفيفة. |
| [packs/CLIENT_DEMO_PACK_AR.md](packs/CLIENT_DEMO_PACK_AR.md) | حزمة عرض للعميل وأولى الإثباتات. |
| [MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md) | مجلس أصول شهري (runbook). |
| [QUARTERLY_PRUNING_POLICY_AR.md](QUARTERLY_PRUNING_POLICY_AR.md) | تشذيب ربع سنوي بلا حذف عشوائي. |
| [OS_ASSET_OPERATING_MODEL_AR.md](OS_ASSET_OPERATING_MODEL_AR.md) | الخمس أنظمة التشغيلية فوق الذاكرة + مسارات Motion. |
| [MARKET_SIGNAL_OPERATING_LOOP_AR.md](MARKET_SIGNAL_OPERATING_LOOP_AR.md) | تحويل L4 إلى إشارات وقرار؛ لا بناء قبل إشارة سوق. |

---

## ترتيب قراءة مقترح

1. **الموجات والكود:** [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md) — ربط Milestones بـ `auto_client_acquisition/` وواجهات FastAPI.
2. **التجاري والعروض:** [../commercial/README.md](../commercial/README.md) ثم المصفوفة [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md).
3. **مسار إثبات 5 عملاء:** [../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md).
4. **Retainer:** [../commercial/RETAINER_PILOT_MINI_AR.md](../commercial/RETAINER_PILOT_MINI_AR.md).
5. **بوابة BU4:** [../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md).
6. **ترخيص IP للشريك:** [../40_partners/IP_LICENSE_OUTLINE_AR.md](../40_partners/IP_LICENSE_OUTLINE_AR.md).
7. **الدستور والامتثال:** `docs/00_constitution/`، `docs/25_compliance_trust/`، و`docs/enterprise_trust/`.

---

## طبقة 00–25 — مجلدات مرقمة (تنفيذ OS + دستور)

> **تنبيه:** يوجد **تكرار في الرقم نفسه** بين مجلدين (مثلاً `04_data_os` و`04_product_strategy`). عند التعارض يُفضَّل مرجع **الموجة** في [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md) وكتالوج الخدمات في `docs/26_service_catalog/` كمصدر «تجاري»، مع بقية المجلدات كسياق أو أرشيف طبقي.

### 00–12

| المجلد | دور مختصر | موجة رئيسية | وسم |
|--------|-------------|----------------|-----|
| [`../00_constitution/`](../00_constitution/) | دستور القابضة وغير القابلة للتفاوض | أساس | داخلي / شريك (Trust) |
| [`../00_foundation/`](../00_foundation/) | معادلة التشغيل ورفض المنتجات الخاطئة | أساس | داخلي |
| [`../01_category/`](../01_category/) | صناعة الفئة والسرد | أساس | إيراد (لغة) |
| [`../01_category_creation/`](../01_category_creation/) | مسار إنشاء فئة | أساس | إيراد |
| [`../02_saudi_positioning/`](../02_saudi_positioning/) | تموضع سعودي (نسخة طبقة) | أساس | إيراد |
| [`../02_strategy/`](../02_strategy/) | استراتيجية وهوية مبكرة | أساس | داخلي |
| [`../03_commercial_mvp/`](../03_commercial_mvp/) | MVP تجاري، Sprint، Proof metrics | مو1 | إيراد |
| [`../03_saudi_positioning/`](../03_saudi_positioning/) | تموضع (نسخة موازية) | أساس | إيراد |
| [`../04_data_os/`](../04_data_os/) | جواز المصدر، جودة، تطبيع | مو1 | إيراد |
| [`../04_product_strategy/`](../04_product_strategy/) | استراتيجية منتج | أساس | داخلي |
| [`../05_client_os/`](../05_client_os/) | لوحات عميل وتجربة | مو1–مو2 | إيراد |
| [`../05_governance_os/`](../05_governance_os/) | حوكمة وقت التشغيل وقرارات | مو1 | داخلي / إيراد |
| [`../06_data_os/`](../06_data_os/) | تكرار ترقيمي — ركّز على `04_data_os` للمرجعية الحديثة إن تعارض | مو1 | داخلي |
| [`../06_llm_gateway/`](../06_llm_gateway/) | بوابة نماذج وسياسات | مو1 | داخلي |
| [`../07_governance/`](../07_governance/) | حوكمة عامة | مو1 | داخلي |
| [`../07_proof_os/`](../07_proof_os/) | Proof Pack وهيكل الأدلة | مو1 | إيراد |
| [`../08_responsible_ai/`](../08_responsible_ai/) | مسؤولية الاستخدام | مو1 | داخلي |
| [`../08_value_os/`](../08_value_os/) | دفتر قيمة | مو1 | داخلي |
| [`../09_capital_os/`](../09_capital_os/) | رأس مال معرفي/تشغيل | مو1 | داخلي |
| [`../09_llm_gateway/`](../09_llm_gateway/) | تكرار ترقيمي — راجع `06_llm_gateway` | مو1 | داخلي |
| [`../10_agents/`](../10_agents/) | وكلاء مبكر | مو4 | داخلي |
| [`../10_tests/`](../10_tests/) | وثائق اختبار موازية لـ `tests/` | مو1 | داخلي |
| [`../11_client_os/`](../11_client_os/) | تكرار ترقيمي — راجع `05_client_os` | مو2 | إيراد |
| [`../11_secure_runtime/`](../11_secure_runtime/) | تشغيل آمن مبكر | مو4 | داخلي |
| [`../12_adoption_os/`](../12_adoption_os/) | اعتماد وجاهزية retainer | مو2 | إيراد |
| [`../12_auditability/`](../12_auditability/) | تدقيق وأحداث | مو3 | داخلي / شريك |

### 13–25

| المجلد | دور مختصر | موجة رئيسية | وسم |
|--------|-------------|----------------|-----|
| [`../13_evidence_control_plane/`](../13_evidence_control_plane/) | سلسلة أدلة | مو3 | داخلي |
| [`../13_workflow_os/`](../13_workflow_os/) | سير عمل وتقارير شهرية | مو2 | إيراد |
| [`../14_proof/`](../14_proof/) | Proof (مرآة موضوعية) | مو1 | إيراد |
| [`../14_trust_os/`](../14_trust_os/) | حزم ثقة | مو3 | شريك |
| [`../15_auditability/`](../15_auditability/) | تكرار ترقيمي — راجع `12_auditability` | مو3 | داخلي |
| [`../15_evidence_control_plane/`](../15_evidence_control_plane/) | تكرار ترقيمي — راجع `13_evidence_control_plane` | مو3 | داخلي |
| [`../15_value/`](../15_value/) | قيمة وقياس | مو2 | داخلي |
| [`../16_agents/`](../16_agents/) | وكلاء | مو4 | داخلي |
| [`../16_capital/`](../16_capital/) | رأس مال | مو1 | داخلي |
| [`../16_evidence_control_plane/`](../16_evidence_control_plane/) | تكرار ترقيمي — طبقة أدلة | مو3 | داخلي |
| [`../17_revenue_os/`](../17_revenue_os/) | Revenue OS وكتالوج الإشارات | مو1 | إيراد |
| [`../17_secure_agent_runtime/`](../17_secure_agent_runtime/) | أمان وقت تشغيل الوكيل | مو4 | داخلي |
| [`../18_brain_os/`](../18_brain_os/) | ذاكرة تشغيل/دماغ | مو2+ | داخلي |
| [`../18_intelligence_os/`](../18_intelligence_os/) | ذكاء تشغيلي | مو2+ | داخلي |
| [`../19_command_os/`](../19_command_os/) | قيادة وتوجيه | مو2 | داخلي |
| [`../19_workflow_os/`](../19_workflow_os/) | تكرار ترقيمي — راجع `13_workflow_os` | مو2 | داخلي |
| [`../20_adoption/`](../20_adoption/) | اعتماد (مرآة) | مو2 | إيراد |
| [`../20_sales_os/`](../20_sales_os/) | مبيعات (مرآة طبقة) | مو1 | إيراد |
| [`../21_operating_finance/`](../21_operating_finance/) | إيقاع مالي تشغيلي | مو2 | داخلي |
| [`../21_operating_rhythm/`](../21_operating_rhythm/) | إيقاع تشغيل أسبوعي/شهري | مو2 | داخلي |
| [`../22_board_decision/`](../22_board_decision/) | قرارات مجلس | أساس+ | داخلي |
| [`../22_enterprise_rollout/`](../22_enterprise_rollout/) | طرح مؤسسي (مرقّم) | مو3 | شريك |
| [`../23_intelligence/`](../23_intelligence/) | ذكاء (مرآة) | مو2+ | داخلي |
| [`../23_standards/`](../23_standards/) | معايير تشغيل قابلة للرقابة | مو5 | داخلي / ترخيص IP |
| [`../24_ecosystem/`](../24_ecosystem/) | نظام بيئي | مو5 | شريك |
| [`../24_risk_resilience/`](../24_risk_resilience/) | مخاطر ومرونة | مو3 | داخلي |
| [`../25_compliance_trust/`](../25_compliance_trust/) | امتثال وثقة | مو3 | شريك |
| [`../25_ventures/`](../25_ventures/) | بوابة مشاريع/مخاطر | مو5 | داخلي |

---

## طبقة 26–44 — توسع وكتالوج وBU

- **مصفوفة العروض (سعر / مدة / مستبعد):** [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md).
- **توليد هيكل المجلدات:** [`../../scripts/generate_scale_phase_docs.py`](../../scripts/generate_scale_phase_docs.py).

### أرقام مكررة — أي مجلد «canonical» للعرض؟

| الرقم | المصدر المعتمد للعرض (canonical) | مجلد موازٍ (سياق / مرآة / أرشيف) |
|-------|-----------------------------------|-------------------------------------|
| 26 | [`../26_service_catalog/`](../26_service_catalog/) | [`../26_human_amplified/`](../26_human_amplified/) |
| 27 | [`../27_delivery_playbooks/`](../27_delivery_playbooks/) | [`../27_value_capture/`](../27_value_capture/) |
| 28 | [`../28_change_requests/`](../28_change_requests/) | [`../28_operating_finance/`](../28_operating_finance/) |
| 29 | [`../29_sales_os/`](../29_sales_os/) | [`../29_enterprise_rollout/`](../29_enterprise_rollout/) |
| 30 | [`../30_pricing/`](../30_pricing/) | [`../30_standards/`](../30_standards/) |
| 31 | [`../31_operating_finance/`](../31_operating_finance/) | [`../31_certification/`](../31_certification/) |
| 32 | [`../32_enterprise_readiness/`](../32_enterprise_readiness/) | [`../32_ecosystem/`](../32_ecosystem/) |
| 33 | [`../33_enterprise_rollout/`](../33_enterprise_rollout/) | [`../33_ventures/`](../33_ventures/) |
| 34 | [`../34_ai_estate/`](../34_ai_estate/) | [`../34_market_power/`](../34_market_power/) |
| 35 | [`../35_agent_iam/`](../35_agent_iam/) | [`../35_tests/`](../35_tests/) |
| 36–44 | مجلد واحد لكل رقم في المصفوفة | — |

---

## مجلدات موضوعية (بلا بادئة رقمية) — خرائط سريعة

القائمة الكاملة مع عدّ الملفات وعناوين README في: [`_generated/docs_top_level_snapshot.json`](_generated/docs_top_level_snapshot.json).

| كتلة | أمثلة مجلدات | غرض |
|------|----------------|-----|
| تشغيل ومهام | `operations/`, `ops/`, `readiness/`, `compliance_trust_ops/`, `observability/`, `testing/` | تشغيل يومي، SLO، جاهزية |
| تجاري وعرض | `commercial/`, `sales/`, `sales-kit/`, `go-to-market/`, `revenue/`, `pricing` (ملفات جذر) | عروض، مبيعات، حزم |
| قانوني وعقود | `contracts/`, `legal/` | DPA، شروط، إطار التعاقد |
| مؤسسي وثقة | `enterprise_trust/`, `enterprise/`, `enterprise_rollout/`, `trust/`, `board_ready/`, `institutional/` | BU4، مجلس، امتثال |
| منتج وتسليم | `product/`, `delivery/`, `engineering/`, `services/` | مواصفات، تسليم، تشخيص خدمات |
| استراتيجية وصفر→قابضة | `from_zero/`, `strategy/`, `blueprint/`, `holding/`, `ventures/`, `scale/` | رؤية، موجات، نمو |
| معرفة وفهرسة | `knowledge/`, `knowledge_base/`, `knowledge-base/`, `meta/`, `registry/`, `memory/` | فهارس، خرائط، ذاكرة |
| سوق وفئة | `market/`, `market_power/`, `category/`, `sector-reports/`, `global_grade/` | مرجعية، فئة، درجات |
| أمن وجودة | `security/`, `quality/`, `risk/`, `risk_resilience/` | حوادث، جودة، مخاطر |
| محتوى وتدريب | `content/`, `training/`, `templates/`, `prompts/`, `playbooks/`, `academy/` | قوالب، تمارين |
| تكامل وواجهات | `integrations/`, `localization/`, `ar/`, `public/` | تكامل، عربي، مواد عامة |
| أرشيف وموجات قديمة | `archive/`, `wave6/`, `wave8/`, `v10/`, `phase-e/`, `ultimate_manual/` | مرجع تاريخي — لا تعتمد كمصدر وحيد |
| أخرى مفيدة | `control_tower/`, `ledgers/`, `proof_architecture/`, `snapshots/`, `group/`, `team/`, `meetings/` | قيادة، دفاتر، لقطات |

---

## ربط وحدات الأعمال بالكود (BU1–BU4)

| وحدة | واجهة API رئيسية | حزم `auto_client_acquisition` | وثائق داعمة |
|------|------------------|--------------------------------|-------------|
| BU1 Sprint ذكاء إيرادات | [`api/routers/revenue_intelligence.py`](../../api/routers/revenue_intelligence.py) | `revenue_os/`, `governance_os/`, `proof_os/`, `data_os/` | `docs/03_commercial_mvp/`, `docs/26_service_catalog/` |
| BU2 Data Readiness / جواز | [`api/routers/data_os.py`](../../api/routers/data_os.py) | `data_os/` | `docs/04_data_os/`, `docs/26_service_catalog/` |
| BU3 Retainer / قيمة شهرية | [`api/routers/wave2_client_ops.py`](../../api/routers/wave2_client_ops.py) | `adoption_os/`, `client_os/` | `docs/13_workflow_os/`, [RETAINER_PILOT_MINI_AR.md](../commercial/RETAINER_PILOT_MINI_AR.md) |
| BU4 Trust Enterprise | — (حزم + وثائق) | `trust_os/`, `auditability_os/`, `secure_agent_runtime_os/`, `agent_os/` | `docs/32_enterprise_readiness/`–`docs/36_agent_runtime_security/`، [BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md) |

**كتالوج خدمات JSON:** [`../../scripts/dealix_export_service_catalog_json.py`](../../scripts/dealix_export_service_catalog_json.py) → `landing/assets/data/services-catalog.json`.

---

## شهادة تشغيل (حوكمة مدمجة — للعروض)

- اختبارات: [`../../tests/`](../../tests/)
- تحقق Revenue OS: [`../../scripts/revenue_os_master_verify.sh`](../../scripts/revenue_os_master_verify.sh)
- تحقق القدرات: [`../../scripts/dealix_capability_verify.sh`](../../scripts/dealix_capability_verify.sh)
- CI: [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml)

---

## أدوات فهرسة إضافية

- فهرس مشروع محلي (بحث كلمات): [`../../scripts/index_project_memory.py`](../../scripts/index_project_memory.py)
- رؤية دستورية مولَّدة: [`../../scripts/generate_holding_vision_docs.py`](../../scripts/generate_holding_vision_docs.py)

---

## ملخص

| احتياجك | ابدأ من |
|---------|---------|
| فهم الموجات والكود | [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md) |
| عرض وسعر لكل مجلد 26–44 | [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md) |
| قائمة كل مجلدات `docs/` مع إحصاءات | [`_generated/docs_top_level_snapshot.json`](_generated/docs_top_level_snapshot.json) |
| تجربة عميل حية | [PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md) |
