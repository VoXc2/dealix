# فهرس تنفيذ خطة الرئيس التنفيذي (ما وُجد في الريبو)

هذا المستند يربط **خطة التنفيذ التنفيذية** بملفات قابلة للتشغيل في المستودع.

## المرحلة 0 — دمج وتحقق

- [docs/ops/PHASE0_CEO_RELEASE_GATE_AR.md](../ops/PHASE0_CEO_RELEASE_GATE_AR.md)
- [docs/ops/ALEMBIC_MIGRATION_POLICY.md](../ops/ALEMBIC_MIGRATION_POLICY.md)
- أوامر التحقق: `bash scripts/revenue_os_master_verify.sh`، `python scripts/smoke_inprocess.py` (مع مفاتيح اختبار كما في البوابة).

## المرحلة 1 — P0 تقني

| عنصر | مسار |
|------|------|
| Workflow OS v10 | `auto_client_acquisition/workflow_os_v10/` + `tests/test_workflow_os_v10.py` |
| AI Workforce v10 | `auto_client_acquisition/ai_workforce_v10/` + `tests/test_ai_workforce_v10.py` |
| Platform v10 (عقود) | `auto_client_acquisition/platform_v10/` + `tests/test_platform_v10.py` |
| CRM v10 | `auto_client_acquisition/crm_v10/` + `tests/test_crm_v10.py` |

## المرحلة 2 — طبقات v10 إضافية

- Inbox: `customer_inbox_v10/` + `tests/test_customer_inbox_v10.py`
- Growth: `growth_v10/` + `tests/test_growth_v10.py`
- LLM Gateway: `llm_gateway_v10/` + `tests/test_llm_gateway_v10.py`
- Observability: `observability_v10/` + `tests/test_observability_v10.py`
- Knowledge: `knowledge_v10/` + `tests/test_knowledge_v10.py`
- Safety: `safety_v10/` + `tests/test_safety_v10.py`
- Founder: `founder_v10/` + `tests/test_founder_v10.py`

تشغيل مجمّع: `pytest tests/test_*_v10.py -q --no-cov`

## المرحلة 3 — GTM

- [GTM_PLAYBOOK_SERVICE_LADDER_AR.md](GTM_PLAYBOOK_SERVICE_LADDER_AR.md) + [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md)

## المرحلة 4 — امتثال

- [docs/ops/PDPL_CLOSURE_CHECKLIST_AR.md](../ops/PDPL_CLOSURE_CHECKLIST_AR.md) + `dealix/registers/no_overclaim.yaml`

## المرحلة 5 — قياس

- [CEO_OPERATING_METRICS_AR.md](CEO_OPERATING_METRICS_AR.md)

## وسيط HTTP (تعارض الحزمة)

- التطبيق الصحيح: `api/middleware/http_stack.py` مع تصدير من `api/middleware/__init__.py` — لا ملف `api/middleware.py` منفصل يظلّل الحزمة.
