# العربية

## موصّل Slack / Microsoft Teams — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل Slack/Teams يربط Dealix بقنوات الفريق الداخلية في المؤسسة لإرسال إشعارات تشغيلية (مثل: إجراء ينتظر موافقة، فشل تكامل، عمق DLQ متزايد). حالته الحالية **تجريبي داخلي**. القاعدة الثابتة: إشعارات داخلية فقط — لا رسائل تواجه العميل عبر هذا الموصّل.

### النطاق

- **مدعوم:** إرسال إشعارات إلى قناة فريق داخلية محدّدة، نشر تنبيهات صحة التكاملات، إخطار المالك بطلبات الموافقة المعلّقة.
- **غير مدعوم:** مراسلة عملاء أو جهات خارجية، الإرسال إلى قنوات خارج مساحة عمل المؤسسة، أي رسالة تسويقية باردة.

### التنفيذ

- يُستخدَم Slack/Teams عبر محوّل مزوّد يمر بواجهة الموصّلات الموحّدة في `dealix/connectors/connector_facade.py`.
- لا سياسة صريحة للموصّل `slack` في `DEFAULT_POLICIES`؛ يأخذ الافتراضية: 120 نداء/دقيقة، مهلة 10 ثوانٍ، 3 محاولات.
- التكامل يستخدم Incoming Webhook أو Bot Token لقناة محدّدة مسبقاً — لا اكتشاف قنوات ديناميكي.

### دور الموصّل في المراقبة

يُستخدَم هذا الموصّل كقناة إخراج لخطافات المراقبة في الطبقة 6:

- تنبيه عند بقاء قاطع دائرة موصّل مفتوحاً.
- تنبيه عند تزايد عمق DLQ (`outbound`, `webhooks`, `crm_sync`).
- إخطار المالك بطلب موافقة `external_send` معلّق.

### المصادقة والحوكمة

- Bot Token أو Webhook URL يُقرأ كقيمة سرّية ولا يُطبع في أي سجل.
- لأن الوجهة قناة داخلية فقط، لا تنطبق بوّابة `external_send`؛ ومع ذلك يُحظَر أي استخدام لمراسلة عملاء.
- لا تُكتب بيانات شخصية للعملاء في نص الإشعار — تُستخدَم معرّفات مجهّلة فقط.
- العمليات قابلة للإعادة عبر مفتاح عدم التكرار؛ الفشل يُدفَع إلى DLQ ولا يكسر سير العمل.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| طابور الرسائل الفاشلة (مصدر التنبيهات) | `dealix/reliability/dlq.py` (`DLQ.stats`) |
| سجل التدقيق (مصدر التنبيهات) | `dealix/connectors/connector_facade.py` (`audit_tail`) |
| سجل التكاملات | `platform/integrations/integration_registry.md` |

---

# English

## Slack / Microsoft Teams Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The Slack/Teams connector links Dealix to an organization's internal team channels to send operational notifications (e.g. an action awaiting approval, an integration failure, growing DLQ depth). Its current status is **internal beta**. The fixed rule: internal notifications only — no customer-facing messages via this connector.

### Scope

- **Supported:** sending notifications to a specified internal team channel, posting integration health alerts, notifying the owner of pending approval requests.
- **Not supported:** messaging customers or external parties, sending to channels outside the organization's workspace, any cold marketing message.

### Implementation

- Slack/Teams is used via a provider adapter that passes through the unified connector facade in `dealix/connectors/connector_facade.py`.
- There is no explicit policy for the `slack` connector in `DEFAULT_POLICIES`; it takes the default: 120 calls/minute, 10-second timeout, 3 retries.
- The integration uses an Incoming Webhook or Bot Token for a pre-specified channel — no dynamic channel discovery.

### The connector's role in monitoring

This connector is used as an output channel for Layer 6 observability hooks:

- Alert when a connector circuit breaker stays open.
- Alert when DLQ depth grows (`outbound`, `webhooks`, `crm_sync`).
- Notify the owner of a pending `external_send` approval request.

### Authentication and governance

- The Bot Token or Webhook URL is read as a secret value and never printed to any log.
- Because the destination is an internal channel only, the `external_send` gate does not apply; however, any use to message customers is prohibited.
- Customer personal data is not written into the notification body — only anonymized identifiers are used.
- Operations are idempotent via the idempotency key; failure is pushed to the DLQ and does not break the workflow.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| Dead letter queue (alert source) | `dealix/reliability/dlq.py` (`DLQ.stats`) |
| Audit log (alert source) | `dealix/connectors/connector_facade.py` (`audit_tail`) |
| Integration registry | `platform/integrations/integration_registry.md` |
