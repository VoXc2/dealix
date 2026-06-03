# Module Map

Canonical mapping from Dealix OS names to repository packages — **always edit with CODE_MAP**.

| OS | Package paths |
|----|----------------|
| Strategy OS | `auto_client_acquisition/strategy_os/` |
| Data OS | `auto_client_acquisition/data_os/`, `revenue_data_intake/` |
| Revenue OS | `auto_client_acquisition/revenue_os/` |
| Customer OS | `auto_client_acquisition/support_os/`, `support_inbox/`, related API routers |
| Operations OS | `workflow_os_v10/`, `delivery_factory/`, `bottleneck_radar/` |
| Knowledge OS | `knowledge_os/` (thin), `company_brain_mvp/`, `support_os/knowledge_answer.py` |
| Governance OS | `governance_os/`, `compliance_os/`, `agent_governance/` |
| Reporting OS | `reporting_os/`, `executive_reporting/` |
| Delivery OS | `delivery_os/`, `service_sessions/`, `commercial_engagements/` |
| AI Gateway | `llm_gateway_v10/`, tool guardrails — **نية البوابة:** [`LLM_GATEWAY_INTENT_AR.md`](LLM_GATEWAY_INTENT_AR.md) |
| Capability matrix (خدمات ↔ كود) | [`CAPABILITY_MATRIX.md`](CAPABILITY_MATRIX.md) |
| Productization | [`PRODUCTIZATION_MAP.md`](PRODUCTIZATION_MAP.md) |
| Delivery engines (method + QA/gov/proof/playbook/learning + Growth) | **نية المنتج:** [`DELIVERY_ENGINES_INTENT_AR.md`](DELIVERY_ENGINES_INTENT_AR.md) — يربط المراحل الثماني بـ `delivery_os`، `reporting_os`، `governance_os` |
| AI Workforce | `ai_workforce_v10/` |
| Observability | `agent_observability/`, Sentry integration as configured |

Full table: [`../commercial/CODE_MAP_OS_TO_MODULES_AR.md`](../commercial/CODE_MAP_OS_TO_MODULES_AR.md).

**رؤية طويلة المدى (BUs، منصة، معمارية نية):** [`../company/DEALIX_AI_OS_LONG_TERM_AR.md`](../company/DEALIX_AI_OS_LONG_TERM_AR.md).
