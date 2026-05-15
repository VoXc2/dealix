# العربية

## مواصفة اختبارات موصّل واتساب — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

مواصفة اختبار مكتوبة — حالات ومعايير قبول دون شيفرة. كل حالة تُنفَّذ في وضع sandbox مع `whatsapp_allow_live_send=false`.

### مجموعة 1 — الإعداد والإرسال

- **W1.1 غير مُعَدّ:** رمز الوصول أو معرّف الرقم غائب. **القبول:** `configured` تُرجِع `false`؛ الإرسال يُرجِع `WhatsApp not configured` دون نداء API.
- **W1.2 sandbox يمنع الإرسال:** `whatsapp_allow_live_send=false`. **القبول:** `send_text` و`send_template` تُرجِعان `whatsapp_allow_live_send_false` دون أي نداء HTTP.
- **W1.3 إرسال نص ناجح:** علاقة قائمة + موافقة + راية حية في sandbox محاكي. **القبول:** `WhatsAppMessageResult.success = true` مع `message_id`.
- **W1.4 إعادة المحاولة:** خطأ HTTP عابر. **القبول:** يُعاد المحاولة حتى 3 مرات بتراجع أسّي قبل الفشل النهائي.

### مجموعة 2 — الموافقة والحوكمة

- **W2.1 الإرسال يتطلب موافقة:** إجراء `external_send` غير معتمد. **القبول:** القرار `require_approval`؛ المسودة معلّقة، لا إرسال.
- **W2.2 منع واتساب البارد:** مستلم دون علاقة قائمة. **القبول:** القرار `block` عبر `no_cold_whatsapp`.
- **W2.3 لا أرقام مهاتف في السجلات:** فحص السطور المسجّلة. **القبول:** بادئة فقط (`to_prefix`)، لا رقم كامل ولا رمز خام.

### مجموعة 3 — خطافات الويب

- **W3.1 تحقق GET صحيح:** رمز تحقّق مطابق و`mode=subscribe`. **القبول:** `verify_webhook` تعيد التحدّي.
- **W3.2 تحقق GET خاطئ:** رمز غير مطابق. **القبول:** `verify_webhook` تُرجِع `None`.
- **W3.3 توقيع صالح:** ترويسة `X-Hub-Signature-256` صحيحة. **القبول:** `verify_signature` تُرجِع `true`.
- **W3.4 توقيع مزوّر:** ترويسة غير صحيحة. **القبول:** `verify_signature` تُرجِع `false`؛ لا معالجة.
- **W3.5 تحليل الحمولة:** خطاف برسالة واحدة. **القبول:** `parse_incoming` تُرجِع المرسِل والمعرّف والنص بدقة.

### مجموعة 4 — عدم التكرار والفشل

- **W4.1 حدث مكرر:** نفس الخطاف مرتين. **القبول:** المعالجة الثانية تُتجاهَل عبر `claim` دون أثر جانبي.
- **W4.2 فشل بعد التحقق:** خطأ معالجة بعد توقيع صالح. **القبول:** يُدفَع إلى `WEBHOOKS_DLQ` دون فقدان الحدث.

### معايير القبول العامة

- لا حالة تمر بإرسال فعلي خارج sandbox.
- كل إرسال يبقى مسودة حتى موافقة موثّقة.
- لا يكسر فشل واتساب سير العمل المستدعي.

---

# English

## WhatsApp Connector Test Specification — Dealix

**Owner:** Integrations Platform Lead.

A written test specification — cases and acceptance criteria, no code. Every case runs in sandbox mode with `whatsapp_allow_live_send=false`.

### Group 1 — Configuration and sending

- **W1.1 Not configured:** access token or phone ID missing. **Acceptance:** `configured` returns `false`; sending returns `WhatsApp not configured` with no API call.
- **W1.2 Sandbox blocks send:** `whatsapp_allow_live_send=false`. **Acceptance:** `send_text` and `send_template` return `whatsapp_allow_live_send_false` with no HTTP call.
- **W1.3 Successful text send:** existing relationship + approval + live flag in a simulated sandbox. **Acceptance:** `WhatsAppMessageResult.success = true` with a `message_id`.
- **W1.4 Retry:** a transient HTTP error. **Acceptance:** retried up to 3 times with exponential backoff before final failure.

### Group 2 — Approval and governance

- **W2.1 Send requires approval:** an unapproved `external_send` action. **Acceptance:** decision is `require_approval`; the draft is pending, no send.
- **W2.2 Cold WhatsApp blocked:** a recipient with no existing relationship. **Acceptance:** decision is `block` via `no_cold_whatsapp`.
- **W2.3 No phone numbers in logs:** inspect logged lines. **Acceptance:** only a prefix (`to_prefix`), no full number and no raw token.

### Group 3 — Webhooks

- **W3.1 Correct GET verification:** matching verify token and `mode=subscribe`. **Acceptance:** `verify_webhook` returns the challenge.
- **W3.2 Wrong GET verification:** a non-matching token. **Acceptance:** `verify_webhook` returns `None`.
- **W3.3 Valid signature:** a correct `X-Hub-Signature-256` header. **Acceptance:** `verify_signature` returns `true`.
- **W3.4 Forged signature:** an incorrect header. **Acceptance:** `verify_signature` returns `false`; no processing.
- **W3.5 Payload parsing:** a webhook with one message. **Acceptance:** `parse_incoming` returns the sender, ID, and text accurately.

### Group 4 — Idempotency and failure

- **W4.1 Duplicate event:** the same webhook twice. **Acceptance:** the second processing is skipped via `claim` with no side effect.
- **W4.2 Failure after verification:** a processing error after a valid signature. **Acceptance:** pushed to `WEBHOOKS_DLQ` without losing the event.

### General acceptance criteria

- No case passes with an actual send outside sandbox.
- Every send stays a draft until documented approval.
- A WhatsApp failure does not break the calling workflow.
