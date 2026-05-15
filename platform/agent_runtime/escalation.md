# العربية

**Owner:** قائد حوكمة الوكلاء (Agent Governance Lead) — قسم Trust & Governance.

## الغرض

بوّابة التصعيد ترفع كل إجراء عالي المخاطر إلى موافقة بشرية قبل التنفيذ. أي إجراء يرسل رسالة خارجية أو يلتزم مالياً أو يلمس PII حساسة لا يُنفَّذ آلياً — يُرفع، يُوثَّق، وينتظر موافقة.

## متى يُصعَّد

- استدعاء أداة مصنّفة `requires_approval` في سجل الأدوات.
- أي إرسال خارجي: `send_email_live`, `send_whatsapp_live`.
- أي التزام مالي أو تعاقدي: `charge_payment_live`, خصم، التزام عقد.
- أي إجراء يلمس PII أو يفتقر إلى أساس قانوني وفق `auto_client_acquisition/governance_os/lawful_basis.py`.
- أي طلب يلامس إجراءً ممنوعاً وفق `auto_client_acquisition/governance_os/forbidden_actions.py` (يُرفض لا يُصعَّد).

## المكوّنات

- **مصفوفة الموافقات:** `auto_client_acquisition/governance_os/approval_matrix.py` تحدد مستوى المخاطر والمُوافِق المطلوب.
- **سياسة الموافقة:** `auto_client_acquisition/governance_os/approval_policy.py` تُنشئ طلب موافقة بمهلة زمنية.
- **بوّابة المسودات:** `auto_client_acquisition/governance_os/draft_gate.py` تضمن أن كل إجراء خارجي يبدأ كمسودة.
- **محرّك السياسات:** `auto_client_acquisition/secure_agent_runtime_os/policy_engine.py`.

## قائمة الجاهزية

- [x] كل أداة `requires_approval` تمر عبر بوّابة التصعيد.
- [x] لكل طلب موافقة مهلة زمنية ومُوافِق مُسمّى.
- [x] الإجراءات الممنوعة تُرفض عند البوّابة لا تُصعَّد.
- [ ] إشعار آلي للمُوافِق عبر قناة موثَّقة.

## المقاييس

- عدد التصعيدات لكل وكيل ولكل نوع إجراء.
- متوسط زمن الموافقة.
- عدد طلبات الموافقة المنتهية بدون رد.
- عدد الإجراءات الخارجية المنفَّذة بلا موافقة (يجب أن يكون صفراً).

## خطافات المراقبة

- حدث `escalation.raised` و`escalation.approved` و`escalation.denied` و`escalation.expired` عبر `auto_client_acquisition/agent_observability/trace.py`.
- حقل `approval_status` في كل أثر.

## قواعد الحوكمة

- لا إجراء خارجي بلا موافقة موثَّقة — قاعدة `external_action_requires_approval` في `auto_client_acquisition/governance_os/rules/external_action_requires_approval.py`.
- لا يصعّد الوكيل لنفسه؛ المُوافِق دائماً دور بشري مختلف.
- انتهاء مهلة الموافقة = رفض ضمني، لا تنفيذ.

## إجراء التراجع

عند موافقة خاطئة: ألغِ الإجراء إن كان قابلاً للإلغاء، أوقف الوكيل، راجع سجل التصعيد، وأعد المعايرة عبر `approval_matrix.py`.

## درجة الجاهزية الحالية

**77 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

**Owner:** Agent Governance Lead — Trust & Governance.

## Purpose

The Escalation Gateway raises every high-risk action to human approval before execution. Any action that sends an external message, makes a financial commitment, or touches sensitive PII is not auto-executed — it is raised, recorded, and waits for approval.

## When escalation happens

- A tool call classified `requires_approval` in the Tool Registry.
- Any external send: `send_email_live`, `send_whatsapp_live`.
- Any financial or contractual commitment: `charge_payment_live`, discount, contract commitment.
- Any action touching PII or lacking a lawful basis per `auto_client_acquisition/governance_os/lawful_basis.py`.
- Any request matching a forbidden action per `auto_client_acquisition/governance_os/forbidden_actions.py` (rejected, not escalated).

## Components

- **Approval matrix:** `auto_client_acquisition/governance_os/approval_matrix.py` decides risk level and required approver.
- **Approval policy:** `auto_client_acquisition/governance_os/approval_policy.py` creates an approval request with a TTL.
- **Draft gate:** `auto_client_acquisition/governance_os/draft_gate.py` ensures every external action starts as a draft.
- **Policy engine:** `auto_client_acquisition/secure_agent_runtime_os/policy_engine.py`.

## Readiness checklist

- [x] Every `requires_approval` tool passes the Escalation Gateway.
- [x] Every approval request has a TTL and a named approver.
- [x] Forbidden actions are rejected at the gateway, not escalated.
- [ ] Automated approver notification over a documented channel.

## Metrics

- Escalation count per agent and per action type.
- Median approval time.
- Count of approval requests that expired without a response.
- Count of external actions executed without approval (must be zero).

## Observability hooks

- `escalation.raised`, `escalation.approved`, `escalation.denied`, `escalation.expired` events via `auto_client_acquisition/agent_observability/trace.py`.
- `approval_status` field on every trace.

## Governance rules

- No external action without a documented approval — the `external_action_requires_approval` rule in `auto_client_acquisition/governance_os/rules/external_action_requires_approval.py`.
- An agent never escalates to itself; the approver is always a different human role.
- An expired approval TTL means an implicit denial, not execution.

## Rollback procedure

On a wrong approval: reverse the action if reversible, stop the agent, review the escalation log, and recalibrate via `approval_matrix.py`.

## Current readiness score

**77 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
