# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead) — قسم هندسة المنصة.

## الغرض

الطبقة 2 — وقت تشغيل الوكلاء — تجعل كل وكيل في Dealix كياناً منظَّماً له هدف معلن، صلاحيات صريحة، أدوات معرّفة، نطاق ذاكرة، تقييم، وملف مخاطر. هذه الطبقة هي مستوى التنفيذ للـ "Decision Plane" المذكور في `README.md`؛ لا تنفّذ التزامات خارجية بنفسها بل ترفعها إلى Execution Plane عبر عقود، وتمرّ كل خطوة عالية المخاطر عبر Trust Plane.

## المكوّنات

- **سجل الوكلاء (Agent Registry):** مصدر الحقيقة للوكلاء المعرّفين رسمياً. يستند إلى `auto_client_acquisition/agent_governance/agent_registry.py` و`auto_client_acquisition/ai_workforce/agent_registry.py`. أي وكيل غير مسجَّل يفشل في التقييم.
- **سجل الأدوات (Tool Registry):** فئات الأدوات وتصنيف صلاحياتها (`allowed` / `requires_approval` / `forbidden`) من `ToolCategory` و`ToolPermission` في `auto_client_acquisition/agent_governance/schemas.py`.
- **مدير دورة الحياة (Lifecycle Manager):** يحكم انتقالات الوكيل: `defined → loaded → running → paused → stopped → retired`، مع إيقاف فوري.
- **نطاق الذاكرة (Memory Scope):** عزل الذاكرة لكل وكيل عبر `auto_client_acquisition/ai_workforce_v10/memory_store.py`.
- **بوّابة التصعيد (Escalation Gateway):** ترفع الإجراءات عالية المخاطر إلى `auto_client_acquisition/approval_center/approval_policy.py`.
- **طبقة المراقبة (Observability):** التتبّع والتكلفة والجودة عبر `auto_client_acquisition/agent_observability/`.
- **التحكّم بالإصدارات (Versioning):** مقارنة v1 مقابل v2 لكل وكيل.

## تدفّق البيانات

1. يصل طلب إلى الوكيل عبر المنسّق (`auto_client_acquisition/ai_workforce/orchestrator.py`).
2. يحمّل وقت التشغيل تعريف الوكيل من السجل ويثبّت نطاق ذاكرته.
3. يخطّط الوكيل ويستدعي أدوات؛ كل استدعاء يُفحص مقابل سجل الأدوات.
4. الأدوات `requires_approval` تُرفع إلى بوّابة التصعيد ولا تُنفَّذ قبل الموافقة.
5. تُسجَّل كل خطوة في طبقة المراقبة مع أثر قابل للتدقيق.
6. تُرفع المخرجات النهائية إلى Execution Plane عبر عقد.

## الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي في المستودع |
|---|---|
| سجل حوكمة الوكلاء | `auto_client_acquisition/agent_governance/agent_registry.py` |
| مخططات الحوكمة | `auto_client_acquisition/agent_governance/schemas.py` |
| سياسة الحوكمة | `auto_client_acquisition/agent_governance/policy.py` |
| سجل القوى العاملة | `auto_client_acquisition/ai_workforce/agent_registry.py` |
| عقود الوكلاء | `auto_client_acquisition/ai_workforce/agent_contracts.py` |
| المنسّق | `auto_client_acquisition/ai_workforce/orchestrator.py` |
| مخزن الذاكرة | `auto_client_acquisition/ai_workforce_v10/memory_store.py` |
| التصعيد/الموافقات | `auto_client_acquisition/approval_center/approval_policy.py` |
| التتبّع والمراقبة | `auto_client_acquisition/agent_observability/trace.py` |
| الوكلاء الأساسيون | `core/agents/base.py`, `core/agents/multi_agent.py` |
| تعريفات الوكلاء التشغيلية | `.claude/agents/dealix-sales.md` وغيرها |

انظر أيضاً: `platform/agent_runtime/readiness.md` و`platform/agent_runtime/agent_lifecycle.md`.

---

# English

**Owner:** Agent Runtime Platform Lead — Platform Engineering.

## Purpose

Layer 2 — Agent Runtime — makes every Dealix agent a structured entity with a declared goal, explicit permissions, defined tools, memory scope, evaluation, and risk profile. This layer is the implementation surface of the Decision Plane named in `README.md`; it never makes external commitments itself but raises them to the Execution Plane through contracts, and every high-risk step passes the Trust Plane.

## Components

- **Agent Registry:** source of truth for formally defined agents, built on `auto_client_acquisition/agent_governance/agent_registry.py` and `auto_client_acquisition/ai_workforce/agent_registry.py`. Any unregistered agent fails evaluation.
- **Tool Registry:** tool categories and permission classification (`allowed` / `requires_approval` / `forbidden`) from `ToolCategory` and `ToolPermission` in `auto_client_acquisition/agent_governance/schemas.py`.
- **Lifecycle Manager:** governs agent transitions `defined → loaded → running → paused → stopped → retired`, with instant stop.
- **Memory Scope:** per-agent memory isolation via `auto_client_acquisition/ai_workforce_v10/memory_store.py`.
- **Escalation Gateway:** raises high-risk actions to `auto_client_acquisition/approval_center/approval_policy.py`.
- **Observability layer:** tracing, cost, and quality via `auto_client_acquisition/agent_observability/`.
- **Versioning control:** v1 vs v2 comparison per agent.

## Data flow

1. A request reaches the agent through the orchestrator (`auto_client_acquisition/ai_workforce/orchestrator.py`).
2. The runtime loads the agent definition from the registry and binds its memory scope.
3. The agent plans and calls tools; each call is checked against the Tool Registry.
4. `requires_approval` tools are raised to the Escalation Gateway and are not executed before approval.
5. Every step is recorded in the observability layer with an auditable trace.
6. Final outputs are lifted to the Execution Plane through a contract.

## Mapping to existing code

| Component | Real repo path |
|---|---|
| Agent governance registry | `auto_client_acquisition/agent_governance/agent_registry.py` |
| Governance schemas | `auto_client_acquisition/agent_governance/schemas.py` |
| Governance policy | `auto_client_acquisition/agent_governance/policy.py` |
| Workforce registry | `auto_client_acquisition/ai_workforce/agent_registry.py` |
| Agent contracts | `auto_client_acquisition/ai_workforce/agent_contracts.py` |
| Orchestrator | `auto_client_acquisition/ai_workforce/orchestrator.py` |
| Memory store | `auto_client_acquisition/ai_workforce_v10/memory_store.py` |
| Escalation/approvals | `auto_client_acquisition/approval_center/approval_policy.py` |
| Tracing/observability | `auto_client_acquisition/agent_observability/trace.py` |
| Core agents | `core/agents/base.py`, `core/agents/multi_agent.py` |
| Operational agent definitions | `.claude/agents/dealix-sales.md` and peers |

See also: `platform/agent_runtime/readiness.md` and `platform/agent_runtime/agent_lifecycle.md`.
