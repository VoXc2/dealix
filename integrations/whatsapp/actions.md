# العربية

## إجراءات واتساب — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

هذا المستند يصف الإجراءات الصادرة التي يدعمها موصّل واتساب وكيف تمر كلها عبر بوّابة الموافقة. القاعدة الثابتة: لا إجراء واتساب يواجه العميل يُنفَّذ دون موافقة بشرية موثّقة.

### الإجراءات المدعومة

- **إرسال قالب معتمد (`send_template`):** يرسل قالباً وافق عليه Meta مسبقاً، بلغة محدّدة ومكوّنات. يُستخدَم لبدء محادثة ضمن علاقة قائمة فقط.
- **إرسال نص (`send_text`):** يرسل نصاً عادياً ضمن نافذة محادثة قائمة (خلال 24 ساعة من آخر رسالة من العميل).

كلا الإجراءين منفّذان في `integrations/whatsapp.py` ويُرجِعان `WhatsAppMessageResult` بـ `success` و`message_id` أو `error`.

### دورة حياة الإجراء — موافقة أولاً

1. ينشئ وكيل Dealix مسودة رسالة كاقتراح.
2. يُصنَّف الإجراء `external_send`؛ تفرض قاعدة `external_action_requires_approval` حالة `require_approval`.
3. تبقى المسودة معلّقة في انتظار موافقة بشرية موثّقة.
4. يُتحقَّق من علاقة المستلم؛ مستلم دون علاقة قائمة يُحظَر عبر `no_cold_whatsapp`.
5. بعد الموافقة فقط، يُستدعى `send_template` أو `send_text`.
6. إذا كانت `whatsapp_allow_live_send=false`، يُرجَع `whatsapp_allow_live_send_false` ولا يخرج إرسال فعلي.
7. تُسجَّل النتيجة كقيد تدقيق؛ الفشل النهائي يُدفَع إلى DLQ.

### قابلية الإعادة

- يُحسب مفتاح عدم التكرار من حمولة الرسالة عبر واجهة الموصّلات.
- إعادة نفس الإرسال بنفس المفتاح لا تُنتج رسالة مزدوجة.

### ما لا تفعله إجراءات واتساب

- لا تبدأ محادثة باردة.
- لا ترسل دفعات غير مطلوبة.
- لا ترسل دون موافقة بشرية موثّقة.
- لا تَعِد بأرقام مبيعات أو نتائج مضمونة في نص الرسالة.

### الربط بالشيفرة الموجودة

| الإجراء | المسار الحقيقي |
|---|---|
| إرسال قالب | `integrations/whatsapp.py` (`send_template`) |
| إرسال نص | `integrations/whatsapp.py` (`send_text`) |
| راية الإرسال الحي | `integrations/whatsapp.py` (`whatsapp_allow_live_send`) |
| قاعدة الموافقة | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |

---

# English

## WhatsApp Actions — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

This document describes the outbound actions the WhatsApp connector supports and how all of them pass the approval gate. The fixed rule: no customer-facing WhatsApp action runs without documented human approval.

### Supported actions

- **Send approved template (`send_template`):** sends a template Meta has pre-approved, with a specified language and components. Used to start a conversation within an existing relationship only.
- **Send text (`send_text`):** sends plain text within an existing conversation window (within 24 hours of the customer's last message).

Both actions are implemented in `integrations/whatsapp.py` and return a `WhatsAppMessageResult` with `success` and `message_id` or `error`.

### Action lifecycle — approval first

1. A Dealix agent creates a draft message as a proposal.
2. The action is classed `external_send`; the `external_action_requires_approval` rule forces `require_approval`.
3. The draft stays pending awaiting documented human approval.
4. The recipient relationship is checked; a recipient with no existing relationship is blocked via `no_cold_whatsapp`.
5. Only after approval is `send_template` or `send_text` invoked.
6. If `whatsapp_allow_live_send=false`, `whatsapp_allow_live_send_false` is returned and no actual send goes out.
7. The result is recorded as an audit entry; final failure is pushed to the DLQ.

### Idempotency

- An idempotency key is computed from the message payload via the connector facade.
- Replaying the same send with the same key produces no duplicate message.

### What WhatsApp actions do not do

- Do not start a cold conversation.
- Do not send unsolicited batches.
- Do not send without documented human approval.
- Do not promise sales numbers or guaranteed results in the message body.

### Mapping to existing code

| Action | Real repo path |
|---|---|
| Send template | `integrations/whatsapp.py` (`send_template`) |
| Send text | `integrations/whatsapp.py` (`send_text`) |
| Live-send flag | `integrations/whatsapp.py` (`whatsapp_allow_live_send`) |
| Approval rule | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |
