# مخطط Dealix للتحول إلى طبقة تشغيل (Operational Layer)

## الهدف

التحول من "منتج AI" إلى "نسيج تنفيذ مؤسسي" يعتمد عليه التشغيل اليومي.

المعيار:

- القيمة لا تأتي من أذكى نموذج فقط.
- القيمة تأتي من نظام **متكامل تشغيليًا**: workflow + governance + observability + memory + measurable outcomes.

## ما الذي تم تفعيله في هذا التغيير؟

- أول Workflow محكوم وصغير قابل للتوسع:
  - `workflows/sales/lead_qualification.workflow.yaml`
- Runtime حوكمة تنفيذي:
  - `auto_client_acquisition/workflow_engine/governed_runtime.py`
- توثيق طبقة workflow engine:
  - `platform/workflow_engine/README.md`

## سلسلة التنفيذ الحاكمة (Golden Runtime Path)

كل خطوة تمر عبر:

1. `risk_score`
2. `policy_check`
3. `approval_check` (عند الحاجة)
4. `tool_execution`
5. `retry` (حسب الحد الأقصى لكل خطوة)
6. `metrics` + `audit_log`

## ربط الطبقات العشرة بمسارات المشروع

1. Experience Layer: `frontend/` + `dashboard/`
2. API + Orchestration: `api/` + `auto_client_acquisition/orchestrator/`
3. Workflow Engine: `auto_client_acquisition/workflow_engine/` + `workflows/`
4. Agent Runtime: `auto_client_acquisition/orchestrator/` + `api/routers/agent_os.py`
5. Governance Runtime: `auto_client_acquisition/governance_os/` + `auto_client_acquisition/compliance_trust_os/`
6. Memory + Knowledge: `auto_client_acquisition/revenue_memory/` + `auto_client_acquisition/knowledge_os/`
7. Observability: `auto_client_acquisition/observability_v10/` + `api/routers/observability_v10.py`
8. Evals: `evals/` + quality tests in `tests/`
9. Executive Layer: `auto_client_acquisition/executive_os/` + `api/routers/executive_os.py`
10. Delivery Machine: `docs/readiness/` + `docs/sales-kit/` + delivery tests

## مبدأ التوسع

- لا تبنِ المنظومة النهائية دفعة واحدة.
- ثبّت أول Workflow محكوم + measurable impact.
- ثم وسّع:
  - عدد الـ workflows
  - عدد الـ integrations
  - تغطية observability
  - دقة evals

## معيار نجاح أولي (Operational Readiness Seed)

إذا عملت بدون انهيار:

- 1 tenant
- 3 users
- 2 roles
- 1 governed workflow
- 1 agent policy path
- 1 approval rule
- 1 CRM commit
- 1 trace/audit thread
- 1 eval summary
- 1 executive metrics summary
- 1 rollback drill

فأنت بدأت الدخول إلى نطاق البنية المؤسسية.
