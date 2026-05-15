# Dealix System Map — المخطط ↔ التنفيذ في الريبو

**دستور الطبقات المرقّم:** [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md) — فهرس `docs/00_constitution` … `docs/36_architecture` مع `auto_client_acquisition/dealix_master_layers/registry.py`.

المخطط أدناه يصف **طبقات تشغيلية** (Operating OS layers). أسماء المجلدات في المخطط قد تختلف عن أسماء الحزم الفعلية؛ الجدول يربط الصادق بالريبو.

## الطبقات العليا (Blueprint)

```
auto_client_acquisition/
  core_os/              ← مفهوم: عمود فقري للهوية والأحداث (انظر CORE_OS.md)
  data_os/
  governance_os/
  llm_gateway/          ← تنفيذ: llm_gateway_v10
  agent_os/             ← تنفيذ: ai_workforce + agent_governance
  workflow_os/          ← تنفيذ: delivery_os + سير عمل المنتج/المشغل
  revenue_os/
  brain_os/             ← تنفيذ: knowledge_os
  proof_os/             ← تنفيذ: proof_architecture_os
  value_os/             ← تنفيذ: proof_architecture_os (value_ledger) + value_capture_os
  capital_os/           ← تنفيذ: operating_finance_os + board_decision_os
  client_os/
  intelligence_os/      ← + intelligence_compounding_os
  command_os/           ← تنفيذ: board_decision_os
  trust_os/             ← تنفيذ: compliance_trust_os
  risk_os/              ← تنفيذ: risk_resilience_os
  standards_os/
  ecosystem_os/
```

## جدول التعيين (Blueprint → مسار في الريبو)

| الطبقة في المخطط | الدور | مسار التنفيذ الأساسي |
|------------------|-------|----------------------|
| **core_os** | هوية، أحداث، سجلات، كيانات مشتركة | `auto_client_acquisition/revenue_memory/`، `auto_client_acquisition/institutional_control_os/`، طبقة API في `api/` |
| **data_os** | جواز المصدر، جودة، تصنيف، احتفاظ | `auto_client_acquisition/data_os/` |
| **governance_os** | سياسات، قرار تشغيلي، مسودات | `auto_client_acquisition/governance_os/` |
| **llm_gateway** | لا استدعاء نموذج خارج البوابة | `auto_client_acquisition/llm_gateway_v10/` |
| **agent_os** | سجل الوكلاء، صلاحيات، تكلفة | `auto_client_acquisition/ai_workforce/`، `auto_client_acquisition/agent_governance/` |
| **workflow_os** | تسليم، جاهزية، تسليم يد | `auto_client_acquisition/delivery_os/`، `docs/product/WORKFLOW_REGISTRY.md` |
| **revenue_os** | الـ wedge التجاري الأول | `auto_client_acquisition/revenue_os/` |
| **brain_os** | إجابات موثّقة، نقص أدلة | `auto_client_acquisition/knowledge_os/` |
| **proof_os** | Proof Pack، درجة إثبات | `auto_client_acquisition/proof_architecture_os/` |
| **value_os** | أحداث قيمة، تمييز estimated/observed/verified | `auto_client_acquisition/proof_architecture_os/value_ledger.py`، `auto_client_acquisition/value_capture_os/` |
| **capital_os** | مراجعة رأس المال، تخصيص | `auto_client_acquisition/operating_finance_os/` |
| **client_os** | مساحة عمل العميل، لوحات | `auto_client_acquisition/client_os/`، واجهة `frontend/` |
| **intelligence_os** | إشارات → أنماط | `auto_client_acquisition/intelligence_os/`، `auto_client_acquisition/intelligence_compounding_os/` |
| **command_os** | قرارات المؤسس/المجلس | `auto_client_acquisition/board_decision_os/` |
| **trust_os** | جواز، تقارير، تصدير تدقيق | `auto_client_acquisition/compliance_trust_os/` |
| **risk_os** | سجل مخاطر، مرونة | `auto_client_acquisition/risk_resilience_os/` |
| **standards_os** | معيار Dealix | `auto_client_acquisition/standards_os/` |
| **ecosystem_os** | شركاء، أكاديمية، معايير خارجية | `auto_client_acquisition/ecosystem_os/`، `docs/enterprise/` |
| **saudi_layer** | عربي، قطاعات، حدود واتساب، PDPL | موزّع: `revenue_os/saudi_targeting_profile.py`، `market_intelligence/saudi_seasons.py`، `pipelines/saudi_dimensions.py`، ووثائق `docs/intelligence_compounding/ARABIC_SAUDI_INTELLIGENCE_LAYER.md` |
| **operating_rhythm** | إيقاع CEO، قرارات، مجلس إيراد سيئ، تمنتج | `docs/operating_rhythm/`، `auto_client_acquisition/operating_rhythm_os/` |
| **responsible_ai (D-RAIOS)** | معيار AI مسؤول، Trust Pack، مخاطر use case، درجة جاهزية | `docs/responsible_ai/`، `auto_client_acquisition/responsible_ai_os/` |
| **client_maturity** | سلم التحول، محرك النضج، عروض ومسارات تقدم | `docs/client_maturity/`، `auto_client_acquisition/client_maturity_os/` |
| **evidence_control_plane** | أدلة، تغطية، فجوات، Proof v3، مساءلة | `docs/evidence_control_plane/`، `auto_client_acquisition/evidence_control_plane_os/` |
| **agentic_operations** | وكلاء محكومون، هوية، صلاحيات، handoff، MVP levels | `docs/agentic_operations/`، `auto_client_acquisition/agentic_operations_os/` |

## قاعدة القراءة

عند إضافة ميزة جديدة: **حدّد الطبقة**، **التدفق المسموح** ([API_BOUNDARIES.md](API_BOUNDARIES.md))، **الحدث في السجل**، **الاختبار العقدي** ([TESTS_REQUIRED.md](TESTS_REQUIRED.md)).
