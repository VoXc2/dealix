# العربية

## موصّل واتساب للأعمال — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل واتساب يربط Dealix بـ WhatsApp Business Cloud API من Meta. وظيفته استقبال رسائل العملاء وإرسال ردود معتمدة فقط. القاعدة الثابتة: لا واتساب بارد، وكل إرسال يواجه العميل مسودة + موافقة بشرية أولاً.

### النطاق

- **مدعوم:** استقبال رسائل العملاء الواردة، إرسال قوالب معتمدة مسبقاً، إرسال نص ضمن نافذة محادثة قائمة — كلها بعد موافقة.
- **غير مدعوم:** بدء محادثة باردة، الإرسال الجماعي غير المطلوب، أي رسالة دون علاقة قائمة أو موافقة.

### الإعداد

تُقرأ كل بيانات الاعتماد كقيم سرّية عبر `core.config.settings`، كما في `integrations/whatsapp.py`:

- `whatsapp_access_token` — رمز وصول Meta.
- `whatsapp_phone_number_id` — معرّف رقم الإرسال.
- `whatsapp_app_secret` — للتحقق من توقيع الخطافات.
- `whatsapp_verify_token` — لخطوة التحقق GET.
- `whatsapp_allow_live_send` — راية الإرسال الحي؛ عندما تكون `false`، الموصّل في وضع sandbox ولا يرسل فعلياً.

الخاصية `configured` تؤكد توفّر الرمز ومعرّف الرقم قبل أي محاولة.

### الموثوقية

- إعادة المحاولة بتراجع أسّي عبر `tenacity` على المهلات وأخطاء HTTP (3 محاولات).
- المهلة 30 ثانية لكل نداء HTTP.
- حد المعدّل: 90 نداء/دقيقة عبر `ConnectorPolicy` للموصّل `whatsapp`.
- الفشل النهائي يُدفَع إلى طابور `outbound` في DLQ ولا يكسر سير العمل.

### الحوكمة

- `no_cold_whatsapp` يمنع أي رسالة لمستلم دون علاقة قائمة أو موافقة.
- `external_action_requires_approval` يُبقي كل إرسال مسودة حتى موافقة بشرية موثّقة.
- في sandbox، `whatsapp_allow_live_send=false` يضمن عدم خروج أي رسالة فعلية.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| عميل واتساب | `integrations/whatsapp.py` (`WhatsAppClient`) |
| سياسة الموصّل | `dealix/connectors/connector_facade.py` (`whatsapp` في `DEFAULT_POLICIES`) |
| منع واتساب البارد | `auto_client_acquisition/governance_os/rules/no_cold_whatsapp.yaml` |
| موافقة الإرسال الخارجي | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |

انظر أيضاً: `integrations/whatsapp/actions.md`، `integrations/whatsapp/webhooks.md`، `integrations/whatsapp/tests.md`.

---

# English

## WhatsApp Business Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The WhatsApp connector links Dealix to Meta's WhatsApp Business Cloud API. Its job is to receive customer messages and send approved replies only. The fixed rule: no cold WhatsApp, and every customer-facing send is draft + human approval first.

### Scope

- **Supported:** receiving inbound customer messages, sending pre-approved templates, sending text within an existing conversation window — all after approval.
- **Not supported:** starting a cold conversation, unsolicited bulk sending, any message without an existing relationship or consent.

### Configuration

All credentials are read as secret values via `core.config.settings`, as in `integrations/whatsapp.py`:

- `whatsapp_access_token` — Meta access token.
- `whatsapp_phone_number_id` — the sending phone number ID.
- `whatsapp_app_secret` — for webhook signature verification.
- `whatsapp_verify_token` — for the GET verification step.
- `whatsapp_allow_live_send` — the live-send flag; when `false`, the connector is in sandbox mode and does not actually send.

The `configured` property confirms the token and phone ID are available before any attempt.

### Reliability

- Exponential backoff retry via `tenacity` on timeouts and HTTP errors (3 attempts).
- A 30-second timeout per HTTP call.
- Rate limit: 90 calls/minute via the `ConnectorPolicy` for the `whatsapp` connector.
- Final failure is pushed to the `outbound` DLQ queue and does not break the workflow.

### Governance

- `no_cold_whatsapp` blocks any message to a recipient without an existing relationship or consent.
- `external_action_requires_approval` keeps every send a draft until documented human approval.
- In sandbox, `whatsapp_allow_live_send=false` ensures no actual message goes out.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| WhatsApp client | `integrations/whatsapp.py` (`WhatsAppClient`) |
| Connector policy | `dealix/connectors/connector_facade.py` (`whatsapp` in `DEFAULT_POLICIES`) |
| Cold WhatsApp block | `auto_client_acquisition/governance_os/rules/no_cold_whatsapp.yaml` |
| External send approval | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |

See also: `integrations/whatsapp/actions.md`, `integrations/whatsapp/webhooks.md`, `integrations/whatsapp/tests.md`.
