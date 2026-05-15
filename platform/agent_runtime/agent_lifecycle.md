# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead).

## الغرض

تعريف دورة حياة كل وكيل في Dealix بحيث يمكن تحميله وتشغيله وإيقافه فوراً وتقاعده بطريقة محكومة.

## حالات دورة الحياة

| الحالة | الوصف |
|---|---|
| `defined` | للوكيل تعريف رسمي في `agent.yaml` ومسجَّل في `auto_client_acquisition/agent_governance/agent_registry.py`. |
| `loaded` | حُمِّل التعريف، ثُبِّت نطاق الذاكرة، وحُلَّت الأدوات مقابل سجل الأدوات. |
| `running` | الوكيل ينفّذ مهمة عبر المنسّق `auto_client_acquisition/ai_workforce/orchestrator.py`. |
| `paused` | توقّفت المهام الجديدة؛ تكتمل المهمة الجارية أو تُلغى. |
| `stopped` | إيقاف فوري — لا استدعاء أدوات جديد؛ تُلغى الاستدعاءات المعلّقة. |
| `retired` | أُزيل الإصدار من الإنتاج بعد ترحيل حركته إلى إصدار أحدث. |

## الانتقالات المسموح بها

`defined → loaded → running → paused → running` و`paused → stopped` و`running → stopped` و`stopped → retired`. أي انتقال آخر مرفوض.

## الإيقاف الفوري

زر إيقاف لكل وكيل ولكل المنصة. عند الإيقاف: تُرفض الاستدعاءات الجديدة فوراً، تُلغى الأدوات `requires_approval` المعلّقة، ويُكتب حدث `agent.stopped` في `auto_client_acquisition/agent_observability/trace.py`.

## قائمة جاهزية دورة الحياة

- [ ] لكل وكيل تعريف رسمي في `agents/<name>/agent.yaml`.
- [ ] كل انتقال حالة مسجَّل في طبقة المراقبة.
- [ ] الإيقاف الفوري مُختبَر لكل وكيل.
- [ ] التقاعد لا يحدث قبل ترحيل الحركة.

## المقاييس

- زمن التحميل (`loaded` ← `defined`).
- زمن الاستجابة للإيقاف الفوري (هدف: أقل من ثانية واحدة).
- عدد الوكلاء في كل حالة.

## خطافات المراقبة

أحداث `agent.loaded` و`agent.running` و`agent.paused` و`agent.stopped` و`agent.retired` في `auto_client_acquisition/agent_observability/trace.py`.

## قواعد الحوكمة

لا يدخل وكيل حالة `running` قبل المرور بـ `defined` و`loaded`. التقاعد يتطلب موافقة مالك المنصة.

## إجراء التراجع

أعد الوكيل إلى `stopped`، ثم حمّل الإصدار المستقر السابق المسجَّل في `platform/agent_runtime/versioning.md`، ثم انتقل إلى `running`.

## درجة الجاهزية الحالية

**74 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

**Owner:** Agent Runtime Platform Lead.

## Purpose

Define the lifecycle of every Dealix agent so it can be loaded, run, stopped instantly, and retired in a governed way.

## Lifecycle states

| State | Description |
|---|---|
| `defined` | The agent has a formal definition in `agent.yaml` and is registered in `auto_client_acquisition/agent_governance/agent_registry.py`. |
| `loaded` | Definition loaded, memory scope bound, tools resolved against the Tool Registry. |
| `running` | The agent executes a task through the orchestrator `auto_client_acquisition/ai_workforce/orchestrator.py`. |
| `paused` | New tasks halted; the in-flight task completes or is cancelled. |
| `stopped` | Instant stop — no new tool calls; pending calls cancelled. |
| `retired` | The version is removed from production after its traffic is migrated to a newer version. |

## Allowed transitions

`defined → loaded → running → paused → running`, `paused → stopped`, `running → stopped`, and `stopped → retired`. Any other transition is rejected.

## Instant stop

A per-agent and platform-wide stop control. On stop: new calls are rejected immediately, pending `requires_approval` tools are cancelled, and an `agent.stopped` event is written to `auto_client_acquisition/agent_observability/trace.py`.

## Lifecycle readiness checklist

- [ ] Every agent has a formal definition in `agents/<name>/agent.yaml`.
- [ ] Every state transition is recorded in the observability layer.
- [ ] Instant stop is tested for each agent.
- [ ] Retirement does not happen before traffic migration.

## Metrics

- Load time (`defined` → `loaded`).
- Instant-stop response time (target: under one second).
- Count of agents per state.

## Observability hooks

`agent.loaded`, `agent.running`, `agent.paused`, `agent.stopped`, `agent.retired` events in `auto_client_acquisition/agent_observability/trace.py`.

## Governance rules

An agent does not enter `running` before passing `defined` and `loaded`. Retirement requires Platform Lead approval.

## Rollback procedure

Return the agent to `stopped`, load the previous stable version recorded in `platform/agent_runtime/versioning.md`, then transition to `running`.

## Current readiness score

**74 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
