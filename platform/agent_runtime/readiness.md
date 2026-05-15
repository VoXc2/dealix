# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead) — قسم هندسة المنصة.

## الغرض

تقيس هذه الوثيقة جاهزية الطبقة 2 — وقت تشغيل الوكلاء. هدف الطبقة: كل وكيل في Dealix كيان منظَّم له هدف، صلاحيات، أدوات، ذاكرة، تقييم، وملف مخاطر.

## قائمة الجاهزية

- [x] لكل وكيل تعريف رسمي `agent.yaml` بـ `owner` و`risk_level`.
- [x] لكل وكيل أدوات معرّفة مصنّفة في سجل الأدوات.
- [x] كل أداة عالية المخاطر تحتاج موافقة قبل التنفيذ.
- [x] يمكن إيقاف أي وكيل فوراً عبر مفتاح الإيقاف.
- [x] لكل وكيل وثائق ثنائية اللغة كاملة (مطالبة، أدوات، صلاحيات، تقييمات، مؤشرات، ملف مخاطر).
- [x] كل قرار مهم له أثر قابل للتدقيق عبر طبقة المراقبة.
- [x] الأدوات الممنوعة (كشط، أتمتة LinkedIn، WhatsApp بارد، تصدير PII بالجملة) مرفوضة عند حدود الأدوات.
- [ ] مقارنة v1 مقابل v2 آلية لكل وكيل.
- [ ] فحص تكامل مستمر يتحقق من تطابق `agent.yaml` مع `AgentSpec`.

## المقاييس

- نسبة الوكلاء ذوي التعريف الرسمي الكامل: 100% (5 من 5).
- عدد محاولات تشغيل وكيل غير مسجّل: 0 (هدف).
- عدد الإجراءات الخارجية المنفَّذة بلا موافقة: 0 (يجب أن يبقى صفراً).
- زمن الاستجابة لمفتاح الإيقاف: أقل من ثانية واحدة.
- تغطية الأثر للقرارات المهمة: 100%.

## خطافات المراقبة

- كل أثر وكيل عبر `auto_client_acquisition/agent_observability/trace.py`.
- تتبّع التكلفة عبر `auto_client_acquisition/agent_observability/cost.py`.
- مؤشرات الجودة عبر `auto_client_acquisition/agent_observability/quality.py`.
- التنقيح قبل التسجيل عبر `auto_client_acquisition/agent_observability/redaction.py`.
- حالات وقت التشغيل عبر `auto_client_acquisition/secure_agent_runtime_os/runtime_states.py`.

## قواعد الحوكمة

- لا يدخل وكيل غير مسجّل وقت التشغيل.
- لا إجراء خارجي بلا موافقة موثَّقة عبر `auto_client_acquisition/governance_os/approval_policy.py`.
- الإجراءات الممنوعة مرفوضة دائماً، لا تُصعَّد.
- تغيير الصلاحيات أو الأدوات يتطلب موافقة مالك المنصة.
- كل إجراء عميل يبدأ كمسودة (draft-only / approval-first).

## إجراء التراجع

1. فعّل مفتاح الإيقاف عبر `auto_client_acquisition/secure_agent_runtime_os/kill_switch.py` (`activate_kill_switch()`).
2. انقل الوكيل المعيب إلى `stopped`.
3. حمّل الإصدار المستقر السابق المرجَّع في `platform/agent_runtime/versioning.md`.
4. تحقق من التقييمات في `platform/agent_runtime/tests.md`.
5. سجّل التراجع كأثر وأبلغ مالك المنصة.

## درجة الجاهزية الحالية

**75 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/agent_runtime/architecture.md`، `platform/agent_runtime/tests.md`، `platform/agent_runtime/scorecard.yaml`.

---

# English

**Owner:** Agent Runtime Platform Lead — Platform Engineering.

## Purpose

This document measures the readiness of Layer 2 — Agent Runtime. The layer goal: every agent in Dealix is a structured entity with a goal, permissions, tools, memory, evaluation, and a risk profile.

## Readiness checklist

- [x] Every agent has a formal `agent.yaml` definition with `owner` and `risk_level`.
- [x] Every agent has defined tools classified in the Tool Registry.
- [x] Every high-risk tool requires approval before execution.
- [x] Any agent can be stopped instantly via the kill switch.
- [x] Every agent has a complete bilingual document set (system prompt, tools, permissions, evals, KPIs, risk profile).
- [x] Every important decision has an auditable trace via the observability layer.
- [x] Forbidden tools (scraping, LinkedIn automation, cold WhatsApp, bulk PII export) are rejected at the tool boundary.
- [ ] Automated v1 vs v2 comparison per agent.
- [ ] CI check verifying `agent.yaml` matches `AgentSpec`.

## Metrics

- Share of agents with a complete formal definition: 100% (5 of 5).
- Count of attempts to run an unregistered agent: 0 (target).
- Count of external actions executed without approval: 0 (must stay zero).
- Kill-switch response time: under one second.
- Trace coverage of important decisions: 100%.

## Observability hooks

- Every agent trace via `auto_client_acquisition/agent_observability/trace.py`.
- Cost tracking via `auto_client_acquisition/agent_observability/cost.py`.
- Quality indicators via `auto_client_acquisition/agent_observability/quality.py`.
- Redaction before recording via `auto_client_acquisition/agent_observability/redaction.py`.
- Runtime states via `auto_client_acquisition/secure_agent_runtime_os/runtime_states.py`.

## Governance rules

- No unregistered agent enters the runtime.
- No external action without a documented approval via `auto_client_acquisition/governance_os/approval_policy.py`.
- Forbidden actions are always rejected, never escalated.
- Changing permissions or tools requires Platform Lead approval.
- Every customer-facing action starts as a draft (draft-only / approval-first).

## Rollback procedure

1. Activate the kill switch via `auto_client_acquisition/secure_agent_runtime_os/kill_switch.py` (`activate_kill_switch()`).
2. Move the faulty agent to `stopped`.
3. Load the previous stable version referenced in `platform/agent_runtime/versioning.md`.
4. Verify evaluations in `platform/agent_runtime/tests.md`.
5. Record the rollback as a trace and notify the Platform Lead.

## Current readiness score

**75 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/agent_runtime/architecture.md`, `platform/agent_runtime/tests.md`, `platform/agent_runtime/scorecard.yaml`.
