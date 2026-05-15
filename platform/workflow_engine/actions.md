# العربية

**Owner:** مهندس وقت تشغيل سير العمل (Workflow Runtime Engineer).

## الغرض

الإجراء (action) هو وحدة عمل واحدة داخل خطوة سير عمل. يصنّف هذا المستند الإجراءات حسب المخاطر ويحدّد أيها يحتاج موافقة بشرية.

## فئات الإجراءات

- **إجراء داخلي (Internal action):** يعمل ضمن أنظمة Dealix فقط — تصنيف، إثراء، تسجيل نقاط، تحديث CRM داخلي. ينفّذه `system_auto` دون موافقة.
- **إجراء مسودة (Draft action):** ينشئ نصاً موجهاً لطرف خارجي لكنه لا يرسله — صياغة رد، صياغة رسالة متابعة. المخرج مسودة محتجزة.
- **إجراء تواصل خارجي (External communication action):** يرسل فعلياً إلى طرف خارجي. لا ينفَّذ مطلقاً قبل خطوة موافقة بشرية صريحة.
- **إجراء إشعار داخلي (Internal notification action):** يبلّغ دوراً داخلياً — مثل إشعار مالك المبيعات. منخفض المخاطر.

## قاعدة الموافقة الإلزامية

أي خطوة تحتوي إجراء تواصل خارجي يجب أن تسبقها خطوة `request_human_approval` في تعريف YAML. المحرّك يرفض تحميل سير عمل يضع إجراء إرسال خارجي دون موافقة سابقة. هذا غير قابل للتفاوض.

## ربط الإجراءات بالشيفرة

- المسودات والصياغة: وكلاء `auto_client_acquisition/agents/` (مثل `outreach.py`, `followup.py`).
- بوابة القنوات: `auto_client_acquisition/channel_policy_gateway/` تفحص أن القناة مسموحة.
- التصعيد إلى موافقة: `auto_client_acquisition/approval_center/approval_policy.py`.
- تحديث CRM الداخلي: وحدات `auto_client_acquisition/crm_v10/`.

## ما لا تفعله الإجراءات أبداً

- لا إرسال واتساب بارد أو رسائل مجمّعة.
- لا أتمتة LinkedIn.
- لا كشط بيانات من مصادر خارجية.
- لا تنفيذ تواصل خارجي نيابة عن العميل دون موافقته الصريحة.

انظر أيضاً: `platform/workflow_engine/triggers.md`، `platform/workflow_engine/retries.md`، `platform/workflow_engine/compensation.md`.

---

# English

**Owner:** Workflow Runtime Engineer.

## Purpose

An action is a single unit of work inside a workflow step. This document classifies actions by risk and defines which ones require human approval.

## Action categories

- **Internal action:** runs only within Dealix systems — classification, enrichment, scoring, internal CRM update. Executed by `system_auto` without approval.
- **Draft action:** produces text addressed to an external party but does not send it — drafting a reply, drafting a follow-up. The output is a parked draft.
- **External communication action:** actually sends to an external party. It is never executed before an explicit human-approval step.
- **Internal notification action:** notifies an internal role — for example notifying the sales owner. Low risk.

## Mandatory approval rule

Any step containing an external communication action must be preceded by a `request_human_approval` step in the YAML definition. The engine refuses to load a workflow that places an external send action without a prior approval. This is non-negotiable.

## Mapping actions to code

- Drafts and composition: agents in `auto_client_acquisition/agents/` (for example `outreach.py`, `followup.py`).
- Channel gateway: `auto_client_acquisition/channel_policy_gateway/` checks that the channel is allowed.
- Escalation to approval: `auto_client_acquisition/approval_center/approval_policy.py`.
- Internal CRM update: modules under `auto_client_acquisition/crm_v10/`.

## What actions never do

- No cold WhatsApp or bulk messages.
- No LinkedIn automation.
- No data scraping from external sources.
- No external communication on a customer's behalf without their explicit consent.

See also: `platform/workflow_engine/triggers.md`, `platform/workflow_engine/retries.md`, `platform/workflow_engine/compensation.md`.
