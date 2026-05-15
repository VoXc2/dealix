# العربية

## أمان خطافات الويب — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

تستقبل Dealix أحداثاً واردة من أنظمة العميل (HubSpot، Calendly، واتساب، مزوّدو الدفع). هذا المستند يحدّد كيف يُتحقَّق من كل حمولة واردة قبل معالجتها. القاعدة الثابتة: لا تُعالَج حمولة لم يُتحقَّق من توقيعها.

### مبادئ التحقق

- **توقيع لكل حمولة:** يحمل كل خطاف توقيع HMAC من المزوّد. تتحقق Dealix منه بمقارنة ثابتة الزمن قبل المعالجة.
- **عدم التكرار:** يُمرَّر كل حدث عبر `dealix/reliability/idempotency.py` — الحدث المكرر يُتجاهَل بأمان.
- **التحقق من المستوطن:** يُربط الخطاف بـ `tenant_id` الصحيح؛ الحدث الذي لا يطابق مستوطناً معروفاً يُرفَض.
- **نافذة زمنية:** الخطافات الأقدم من نافذة مقبولة تُرفَض لمنع إعادة التشغيل الضارة.

### التحقق من واتساب (Meta)

يُتحقَّق من واتساب على مرحلتين، كما هو منفّذ في `integrations/whatsapp.py`:

1. **خطوة GET للتحقق:** `verify_webhook(mode, token, challenge)` تعيد التحدّي فقط عند تطابق رمز التحقق بمقارنة `hmac.compare_digest`.
2. **توقيع POST:** `verify_signature(payload, signature_header)` تتحقق من ترويسة `X-Hub-Signature-256` باستخدام سرّ التطبيق وHMAC-SHA256.

أي حمولة تفشل أي مرحلة تُرفَض ولا تُعالَج.

### تدفّق المعالجة

1. يصل الخطاف؛ يُقرأ التوقيع الخام من الترويسة.
2. يُحسب التوقيع المتوقّع ويُقارَن بمقارنة ثابتة الزمن.
3. عند الفشل: تُرجَع 401، يُسجَّل قيد تدقيق، ولا تحدث معالجة.
4. عند النجاح: يُحسب مفتاح عدم التكرار، ويُفحَص عبر `IdempotencyStore.claim`.
5. الحدث الجديد يُعالَج؛ المكرر يُرجِع حالة "مكرر" دون أثر جانبي.
6. فشل المعالجة بعد التحقق يُدفَع إلى طابور `webhooks` في DLQ لإعادة التشغيل.

### التعامل مع الفشل

- خطافات فشلت معالجتها بعد التحقق تذهب إلى `WEBHOOKS_DLQ` في `dealix/reliability/dlq.py`.
- يُعيد المشغّل تشغيلها يدوياً من DLQ — عدم التكرار يضمن أمان الإعادة.
- عمق DLQ يظهر في لوحة صحة التكاملات؛ عمق متزايد ينبّه المالك.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| التحقق من توقيع واتساب | `integrations/whatsapp.py` (`verify_signature`, `verify_webhook`) |
| تحليل حمولة واتساب | `integrations/whatsapp.py` (`parse_incoming`) |
| عدم تكرار الأحداث | `dealix/reliability/idempotency.py` (`claim`) |
| طابور الخطافات الفاشلة | `dealix/reliability/dlq.py` (`WEBHOOKS_DLQ`) |
| خطاف HubSpot الوارد | `dealix/connectors/connector_facade.py` (`handle_inbound_webhook`) |

---

# English

## Webhook Security — Layer 6

**Owner:** Integrations Platform Lead.

### Purpose

Dealix receives inbound events from customer systems (HubSpot, Calendly, WhatsApp, payment providers). This document defines how every inbound payload is verified before processing. The fixed rule: no payload is processed without a verified signature.

### Verification principles

- **Signature per payload:** every webhook carries an HMAC signature from the provider. Dealix verifies it with a constant-time comparison before processing.
- **Idempotency:** every event passes through `dealix/reliability/idempotency.py` — a duplicate event is safely ignored.
- **Tenant check:** the webhook is bound to the correct `tenant_id`; an event not matching a known tenant is rejected.
- **Time window:** webhooks older than an accepted window are rejected to prevent malicious replay.

### WhatsApp (Meta) verification

WhatsApp is verified in two stages, as implemented in `integrations/whatsapp.py`:

1. **GET verification step:** `verify_webhook(mode, token, challenge)` returns the challenge only when the verify token matches via `hmac.compare_digest`.
2. **POST signature:** `verify_signature(payload, signature_header)` verifies the `X-Hub-Signature-256` header using the app secret and HMAC-SHA256.

Any payload that fails either stage is rejected and not processed.

### Processing flow

1. The webhook arrives; the raw signature is read from the header.
2. The expected signature is computed and compared with a constant-time comparison.
3. On failure: 401 is returned, an audit entry is logged, and no processing happens.
4. On success: an idempotency key is computed and checked via `IdempotencyStore.claim`.
5. A new event is processed; a duplicate returns a "duplicate" status with no side effect.
6. A processing failure after verification is pushed to the `webhooks` DLQ for replay.

### Failure handling

- Webhooks that fail processing after verification go to `WEBHOOKS_DLQ` in `dealix/reliability/dlq.py`.
- An operator replays them manually from the DLQ — idempotency keeps replay safe.
- DLQ depth surfaces on the integration health dashboard; growing depth alerts the owner.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| WhatsApp signature verification | `integrations/whatsapp.py` (`verify_signature`, `verify_webhook`) |
| WhatsApp payload parsing | `integrations/whatsapp.py` (`parse_incoming`) |
| Event idempotency | `dealix/reliability/idempotency.py` (`claim`) |
| Failed webhook queue | `dealix/reliability/dlq.py` (`WEBHOOKS_DLQ`) |
| HubSpot inbound webhook | `dealix/connectors/connector_facade.py` (`handle_inbound_webhook`) |
