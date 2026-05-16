# Dealix Enterprise Maturity Operating System

هذا المستند يترجم Dealix من "AI SaaS" إلى "AI Operating Infrastructure Company" عبر نظام نضج تشغيلي قابل للقياس.

## الهدف

قياس القدرة التنظيمية (Organizational Capability) بدل عدّ الـfeatures:

1. Workflow redesign
2. Agent orchestration
3. Action governance
4. Memory management
5. Execution supervision
6. Business impact measurement
7. Safe evolution
8. Digital workforce management
9. Executive intelligence generation
10. Organizational intelligence scaling

## نموذج التشغيل (7 مراحل)

1. Foundation maturity
2. Agentic runtime maturity
3. Workflow orchestration maturity
4. Organizational memory maturity
5. Governance maturity
6. Evaluation maturity
7. Continuous evolution maturity

## إنفاذ قياس النضج

السكربت الرسمي:

```bash
python scripts/verify_enterprise_maturity_os.py
```

مصدر درجات القدرات:

`docs/enterprise/ENTERPRISE_READINESS_MODEL.yaml`

### قاعدة الحسم

- كل مجال (Domain) يحسب درجة blended:
  - 70% درجة القدرات
  - 30% تغطية artifacts الفعلية في الريبو
- جاهزية التحول (`ENTERPRISE_TRANSFORMATION_READY=true`) لا تتحقق إلا إذا **كل** domain ≥ 75.

## مسارات الملفات المطلوبة (Mapped safely)

المتطلب النظري كان تحت `/platform/*`.
تنفيذيًا في Python monorepo استخدمنا `/dealix_platform/*` لتفادي تضارب اسم `platform` مع Python stdlib.

### Foundation

- `dealix_platform/foundation`
- `dealix_platform/identity`
- `dealix_platform/rbac`
- `dealix_platform/multi_tenant`
- `dealix_platform/security`
- `dealix_platform/deployment`
- `dealix_platform/observability`

### Agentic runtime

- `agents`
- `dealix_platform/agent_runtime`
- `dealix_platform/tool_registry`
- `dealix_platform/agent_memory`
- `dealix_platform/escalation`

### Workflow orchestration

- `workflows`
- `dealix_platform/workflow_engine`
- `dealix_platform/orchestration`
- `dealix_platform/execution_engine`

### Organizational memory

- `memory`
- `dealix_platform/knowledge`
- `dealix_platform/retrieval`
- `dealix_platform/reranking`

### Governance

- `governance`
- `dealix_platform/policy_engine`
- `dealix_platform/approval_engine`
- `dealix_platform/risk_engine`

### Evaluation

- `evals/retrieval`
- `evals/hallucination`
- `evals/workflow_execution`
- `evals/agent_behavior`
- `evals/governance`
- `evals/business_impact`

### Continuous evolution

- `continuous_improvement`
- `releases`
- `changelogs`
- `versions`

## متطلبات كل system

داخل كل root system يجب وجود:

- `architecture.md`
- `readiness.md`
- `observability.md`
- `rollback.md`
- `metrics.md`
- `risk_model.md`
- `tests/`
- `evals/`

## Master Prompt

نسخة prompt الرسمية موجودة في:

`docs/prompts/CLAUDE_DEALIX_ENTERPRISE_MASTER_PROMPT.md`
