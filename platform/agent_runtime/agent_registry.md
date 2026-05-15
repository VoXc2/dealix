# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead) — قسم هندسة المنصة.

## الغرض

سجل الوكلاء هو مصدر الحقيقة الوحيد لكل وكيل معرَّف رسمياً في Dealix. لا يُسمح بتشغيل أي وكيل غير مُسجَّل. يضمن السجل أن لكل وكيل هدفاً معلناً، صلاحيات، أدوات، نطاق ذاكرة، ومستوى مخاطر — قبل أن يدخل وقت التشغيل.

## المكوّنات

- **بطاقة الوكيل (`AgentCard`):** هوية الوكيل من `auto_client_acquisition/agent_os/agent_card.py` — المعرّف، الاسم، المالك، الغرض، مستوى الاستقلالية، الحالة. تتحقق `agent_card_valid(...)` من اكتمالها.
- **عقد الحوكمة (`AgentSpec`):** عقد الحوكمة لكل وكيل من `auto_client_acquisition/agent_governance/schemas.py` — `allowed_tools`، `forbidden_tools`، `max_autonomy`، `requires_human_review`.
- **السجل التشغيلي:** `auto_client_acquisition/agent_os/agent_registry.py` و`auto_client_acquisition/agent_governance/agent_registry.py` و`auto_client_acquisition/ai_workforce/agent_registry.py`.
- **تعريفات الملفات:** كل وكيل له مجلد `agents/<name>/` يحوي `agent.yaml` المصدر القابل للقراءة بشرياً.

## مصدر الحقيقة

الوكلاء الخمسة المعرّفون: `sales_agent`, `support_agent`, `ops_agent`, `executive_agent`, `governance_agent`. كل منهم له `agents/<name>/agent.yaml` ومجموعة وثائق ثنائية اللغة. السجل يرفض أي وكيل بلا `owner` معلن أو بلا `risk_level`.

## قائمة الجاهزية

- [x] لكل وكيل تعريف `agent.yaml` رسمي.
- [x] كل وكيل يحمل `owner` بدور مُسمّى و`risk_level`.
- [x] الأدوات المُرسِلة خارجياً مُدرجة تحت `requires_approval_for` فقط.
- [ ] التحقق الآلي من تطابق `agent.yaml` مع `AgentSpec` في التكامل المستمر.

## المقاييس

- عدد الوكلاء المسجّلين مقابل الوكلاء قيد التشغيل (يجب أن يتطابقا).
- نسبة الوكلاء الذين لديهم وثائق ثنائية اللغة كاملة: 100%.
- عدد محاولات تشغيل وكيل غير مسجّل (هدف: صفر).

## خطافات المراقبة

- حدث `agent.registered` و`agent.deregistered` عبر `auto_client_acquisition/agent_observability/trace.py`.
- تنبيه عند محاولة تحميل وكيل غير موجود في السجل.

## قواعد الحوكمة

- لا يدخل وكيل وقت التشغيل قبل اجتياز `agent_card_valid(...)`.
- تعديل `allowed_tools` أو `requires_approval_for` يتطلب موافقة مالك المنصة.
- لا يُسجَّل وكيل بأداة إرسال خارجي ضمن `allowed_tools`.

## إجراء التراجع

أزل الوكيل من السجل (يمنع تحميله)، ثم أعد تسجيل الإصدار المستقر السابق المرجَّع في `platform/agent_runtime/versioning.md`.

## درجة الجاهزية الحالية

**76 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/agent_runtime/architecture.md` و`platform/agent_runtime/tool_registry.md`.

---

# English

**Owner:** Agent Runtime Platform Lead — Platform Engineering.

## Purpose

The Agent Registry is the single source of truth for every formally defined agent in Dealix. No unregistered agent may run. The registry guarantees every agent has a declared goal, permissions, tools, memory scope, and risk level — before it enters the runtime.

## Components

- **Agent card (`AgentCard`):** agent identity from `auto_client_acquisition/agent_os/agent_card.py` — id, name, owner, purpose, autonomy level, status. `agent_card_valid(...)` checks completeness.
- **Governance contract (`AgentSpec`):** per-agent governance contract from `auto_client_acquisition/agent_governance/schemas.py` — `allowed_tools`, `forbidden_tools`, `max_autonomy`, `requires_human_review`.
- **Operational registries:** `auto_client_acquisition/agent_os/agent_registry.py`, `auto_client_acquisition/agent_governance/agent_registry.py`, and `auto_client_acquisition/ai_workforce/agent_registry.py`.
- **File definitions:** each agent has an `agents/<name>/` directory holding the human-readable source `agent.yaml`.

## Source of truth

The five defined agents: `sales_agent`, `support_agent`, `ops_agent`, `executive_agent`, `governance_agent`. Each has an `agents/<name>/agent.yaml` and a bilingual document set. The registry rejects any agent with no declared `owner` or no `risk_level`.

## Readiness checklist

- [x] Every agent has a formal `agent.yaml` definition.
- [x] Every agent carries an `owner` with a named role and a `risk_level`.
- [x] Tools that send external messages appear only under `requires_approval_for`.
- [ ] Automated CI check that `agent.yaml` matches `AgentSpec`.

## Metrics

- Registered agent count vs running agent count (must match).
- Share of agents with complete bilingual docs: 100%.
- Count of attempts to run an unregistered agent (target: zero).

## Observability hooks

- `agent.registered` and `agent.deregistered` events via `auto_client_acquisition/agent_observability/trace.py`.
- Alert on any attempt to load an agent absent from the registry.

## Governance rules

- An agent does not enter the runtime before passing `agent_card_valid(...)`.
- Changing `allowed_tools` or `requires_approval_for` requires Platform Lead approval.
- No agent is registered with an external-send tool inside `allowed_tools`.

## Rollback procedure

Deregister the agent (blocks loading), then re-register the previous stable version referenced in `platform/agent_runtime/versioning.md`.

## Current readiness score

**76 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/agent_runtime/architecture.md` and `platform/agent_runtime/tool_registry.md`.
