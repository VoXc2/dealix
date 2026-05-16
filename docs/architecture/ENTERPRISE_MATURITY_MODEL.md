# Dealix Enterprise Maturity Model (DEMM)

## الهدف

هذا النموذج يحوّل القياس من:

- عدد الـ features
- عدد الـ APIs
- عدد الـ agents
- كمية الكود

إلى قياس واحد حقيقي:

**Organizational Capability Maturity**.

المرجع التنفيذي في الكود: `auto_client_acquisition/enterprise_maturity_os/enterprise_maturity_model.py`.
ولطبقة "الجهاز العصبي المؤسسي": `docs/architecture/ENTERPRISE_NERVOUS_SYSTEM.md`.

---

## المراحل السبعة

| Stage | الاسم | معيار النجاح |
|---|---|---|
| 1 | AI Tool | prompts + APIs + workflows بسيطة |
| 2 | AI SaaS Platform | auth + dashboard + billing + multi-user |
| 3 | Enterprise AI Platform | tenant isolation + RBAC + governance + retrieval + evals |
| 4 | Agentic Operating Platform | orchestrated workflows + human approvals + organizational memory |
| 5 | Agentic Enterprise Infrastructure | distributed execution + multi-agent coordination + governed autonomy |
| 6 | Enterprise-Ready Infrastructure | Stage 5 + جميع أنظمة التحقق >= 85 + جميع readiness gates >= 85 |
| 7 | Mission-Critical Operating Layer | Stage 6 + جميع الأنظمة >= 95 + simulation + executive reasoning |

> المراحل 6 و7 تضيفان طبقة "التحقق التشغيلي الصارم" حتى لا يكون النظام مجرد demo.

---

## أنظمة التحقق الخمسة (mandatory)

`enterprise_maturity_model.py` يحسب خمس درجات:

1. **Real Workflow Testing**
2. **Governance Validation**
3. **Operational Evaluations**
4. **Enterprise Readiness Gates**
5. **Executive Proof System**

كل نظام يحصل على score (0-100) ثم band:

- `0-59` = `prototype`
- `60-74` = `internal_beta`
- `75-84` = `client_pilot`
- `85-94` = `enterprise_ready`
- `95+` = `mission_critical`

---

## Readiness Gates (10)

1. `architecture_readiness`
2. `security_readiness`
3. `governance_readiness`
4. `workflow_readiness`
5. `evaluation_readiness`
6. `operational_readiness`
7. `delivery_readiness`
8. `transformation_readiness`
9. `executive_readiness`
10. `scale_readiness`

كل gate يجب أن يكون واضحًا ومقاسًا قبل أي claim مؤسسي.

---

## كيف تستخدمه في الكود

```python
from auto_client_acquisition.enterprise_maturity_os import (
    CapabilitySnapshot,
    WorkflowTestingMetrics,
    GovernanceValidationMetrics,
    OperationalEvaluationMetrics,
    ReadinessGateMetrics,
    ExecutiveProofMetrics,
    VerificationInput,
    assess_enterprise_maturity,
)

assessment = assess_enterprise_maturity(
    capabilities=CapabilitySnapshot(...),
    verification=VerificationInput(
        workflow_testing=WorkflowTestingMetrics(...),
        governance_validation=GovernanceValidationMetrics(...),
        operational_evaluations=OperationalEvaluationMetrics(...),
        enterprise_readiness_gates=ReadinessGateMetrics(...),
        executive_proof=ExecutiveProofMetrics(...),
    ),
)
```

الناتج يعطيك:

- المرحلة الحالية (`stage`)
- اسم المرحلة EN/AR
- `overall_score`
- نتائج كل verification system
- score + band لكل readiness gate
- `missing_for_next_stage` (الفجوات قبل الترقية)

---

## قاعدة اتخاذ القرار

لا نسأل: "كم feature أضفنا؟"

نسأل: "هل Dealix قادر يشغل workflows مؤسسية كاملة، بحوكمة، وأثر قابل للإثبات؟"
