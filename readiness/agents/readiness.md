# العربية

Owner: قائد زمن تشغيل الوكيل (Agent Runtime Lead)

## درجة الطبقة

طبقة زمن تشغيل الوكيل (Layer 2): **75 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/agent_runtime/architecture.md`، `auto_client_acquisition/agent_os/`، `auto_client_acquisition/secure_agent_runtime_os/`، `core/agents/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/agent_runtime/readiness.md` |
| اختبارات | متوفر | `readiness/agents/tests.md` |
| مراقبة | متوفر | `auto_client_acquisition/agent_observability/trace.py` |
| حوكمة | متوفر | `auto_client_acquisition/agent_os/tool_permissions.py`، `auto_client_acquisition/secure_agent_runtime_os/policy_engine.py` |
| تراجع | متوفر | `auto_client_acquisition/secure_agent_runtime_os/kill_switch.py`، `auto_client_acquisition/agent_os/agent_lifecycle.py` |
| مقاييس | متوفر | `readiness/agents/scorecard.yaml` |
| مالك | متوفر | قائد زمن تشغيل الوكيل |

## الفجوات المحددة

- **تمرين تراجع للوكلاء:** مفتاح الإيقاف وحالات التشغيل قائمة في `secure_agent_runtime_os/`، لكن تمريناً متحقَّقاً يعيد إصدار وكيل سابق غير مُسجَّل على وتيرة دورية.
- **حدود الأدوات تحت اختبار عابر:** ربط حدود الأدوات بالموافقة على الأفعال الخارجية يحتاج اختباراً عابراً مُنفَّذاً (انظر `readiness/cross_layer/agent_tool_approval_test.md`).

## روابط ذات صلة

- `readiness/agents/tests.md`
- `readiness/agents/scorecard.yaml`
- `readiness/cross_layer/agent_tool_approval_test.md`
- `readiness/cross_layer/tenant_agent_memory_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Agent Runtime Lead

## Layer score

Agent Runtime layer (Layer 2): **75 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/agent_runtime/architecture.md`, `auto_client_acquisition/agent_os/`, `auto_client_acquisition/secure_agent_runtime_os/`, `core/agents/` |
| readiness | present | this document and `platform/agent_runtime/readiness.md` |
| tests | present | `readiness/agents/tests.md` |
| observability | present | `auto_client_acquisition/agent_observability/trace.py` |
| governance | present | `auto_client_acquisition/agent_os/tool_permissions.py`, `auto_client_acquisition/secure_agent_runtime_os/policy_engine.py` |
| rollback | present | `auto_client_acquisition/secure_agent_runtime_os/kill_switch.py`, `auto_client_acquisition/agent_os/agent_lifecycle.py` |
| metrics | present | `readiness/agents/scorecard.yaml` |
| owner | present | Agent Runtime Lead |

## Specific gaps

- **Agent rollback drill:** the kill switch and runtime states exist in `secure_agent_runtime_os/`, but a verified drill that restores a prior agent version is not recorded on a periodic cadence.
- **Tool boundaries under cross-layer test:** linking tool boundaries to external-action approval needs an executed cross-layer test (see `readiness/cross_layer/agent_tool_approval_test.md`).

## Related links

- `readiness/agents/tests.md`
- `readiness/agents/scorecard.yaml`
- `readiness/cross_layer/agent_tool_approval_test.md`
- `readiness/cross_layer/tenant_agent_memory_test.md`

Estimated value is not Verified value.
