# العربية

## خطافات واتساب — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

يستقبل موصّل واتساب أحداثاً واردة من Meta: رسائل العملاء وتحديثات حالة التسليم. هذا المستند يصف كيف يُتحقَّق من كل خطاف ويُعالَج بأمان. القاعدة الثابتة: لا تُعالَج حمولة لم يُتحقَّق من توقيعها.

### التحقق على مرحلتين

كما هو منفّذ في `integrations/whatsapp.py`:

1. **خطوة التحقق GET:** يطلب Meta رابط الخطاف برمز تحقّق. `verify_webhook(mode, token, challenge)` تعيد التحدّي فقط عند تطابق `whatsapp_verify_token` بمقارنة `hmac.compare_digest` و`mode == "subscribe"`.
2. **توقيع POST:** كل حمولة حدث تحمل ترويسة `X-Hub-Signature-256`. `verify_signature(payload, signature_header)` تحسب HMAC-SHA256 بسرّ التطبيق وتقارنه بمقارنة ثابتة الزمن.

أي حمولة تفشل أي مرحلة تُرفَض ولا تُعالَج.

### تدفّق معالجة الحدث الوارد

1. يصل الخطاف؛ يُقرأ التوقيع الخام من الترويسة.
2. `verify_signature` تتحقق؛ الفشل يُرجِع 401 ويُسجَّل قيد تدقيق.
3. عند النجاح، `parse_incoming(payload)` تستخرج الرسائل: المرسِل، المعرّف، الطابع الزمني، النوع، النص، اسم جهة الاتصال.
4. يُحسب مفتاح عدم التكرار لكل رسالة ويُفحَص عبر `IdempotencyStore.claim`.
5. الرسالة الجديدة تُمرَّر إلى سير العمل المناسب؛ المكررة تُتجاهَل بأمان.
6. فشل المعالجة بعد التحقق يُدفَع إلى `WEBHOOKS_DLQ` لإعادة التشغيل.

### أنواع الأحداث المتعامَل معها

- **رسائل واردة:** رسائل العملاء — تُمرَّر إلى منطق الرد (الذي يبقى موافقة أولاً للإرسال).
- **تحديثات الحالة:** تسليم/قراءة الرسائل الصادرة — تُحدِّث سجل التدقيق فقط.

### الخصوصية

- لا تُكتب أرقام الهواتف الكاملة في السجلات؛ يُسجَّل بادئة فقط (مثل `to_prefix=to[:6]`).
- محتوى الرسائل لا يُسجَّل في قيد التدقيق — يُسجَّل المعرّف والنتيجة فقط.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| تحقق GET | `integrations/whatsapp.py` (`verify_webhook`) |
| تحقق التوقيع | `integrations/whatsapp.py` (`verify_signature`) |
| تحليل الحمولة | `integrations/whatsapp.py` (`parse_incoming`) |
| عدم تكرار الأحداث | `dealix/reliability/idempotency.py` (`claim`) |
| طابور الخطافات الفاشلة | `dealix/reliability/dlq.py` (`WEBHOOKS_DLQ`) |

---

# English

## WhatsApp Webhooks — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The WhatsApp connector receives inbound events from Meta: customer messages and delivery status updates. This document describes how every webhook is verified and processed safely. The fixed rule: no payload is processed without a verified signature.

### Two-stage verification

As implemented in `integrations/whatsapp.py`:

1. **GET verification step:** Meta requests the webhook URL with a verify token. `verify_webhook(mode, token, challenge)` returns the challenge only when `whatsapp_verify_token` matches via `hmac.compare_digest` and `mode == "subscribe"`.
2. **POST signature:** every event payload carries an `X-Hub-Signature-256` header. `verify_signature(payload, signature_header)` computes HMAC-SHA256 with the app secret and compares it with a constant-time comparison.

Any payload that fails either stage is rejected and not processed.

### Inbound event processing flow

1. The webhook arrives; the raw signature is read from the header.
2. `verify_signature` checks it; failure returns 401 and logs an audit entry.
3. On success, `parse_incoming(payload)` extracts messages: sender, ID, timestamp, type, text, contact name.
4. An idempotency key is computed per message and checked via `IdempotencyStore.claim`.
5. A new message is passed to the appropriate workflow; a duplicate is safely ignored.
6. A processing failure after verification is pushed to `WEBHOOKS_DLQ` for replay.

### Handled event types

- **Inbound messages:** customer messages — passed to reply logic (which stays approval-first for sending).
- **Status updates:** delivery/read of outbound messages — update the audit log only.

### Privacy

- Full phone numbers are not written to logs; only a prefix is logged (e.g. `to_prefix=to[:6]`).
- Message content is not written to the audit log — only the ID and result are recorded.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| GET verification | `integrations/whatsapp.py` (`verify_webhook`) |
| Signature verification | `integrations/whatsapp.py` (`verify_signature`) |
| Payload parsing | `integrations/whatsapp.py` (`parse_incoming`) |
| Event idempotency | `dealix/reliability/idempotency.py` (`claim`) |
| Failed webhook queue | `dealix/reliability/dlq.py` (`WEBHOOKS_DLQ`) |
