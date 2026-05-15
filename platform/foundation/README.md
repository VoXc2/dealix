# Foundation Core

هذا المسار يعرّف أقل بنية تشغيلية لازمة لتحويل Dealix من مشروع إلى نظام مؤسسي قابل للنشر.

## الهدف
- حلقة واحدة مكتملة End-to-End.
- حوكمة إلزامية قبل أي تنفيذ خارجي.
- قابلية قياس واضحة (traces + metrics + audit).

## المكوّنات المرتبطة
- `platform/multi_tenant`
- `platform/identity`
- `platform/rbac`
- `platform/workflow_engine`
- `platform/agent_runtime`
- `platform/governance`
- `platform/observability`

## التنفيذ البرمجي
- `auto_client_acquisition/foundation_core/enterprise_loop.py`
- `api/routers/foundation_loop.py`
