# العربية

## موصّل البريد الإلكتروني — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل البريد يربط Dealix بمزوّدي البريد لإرسال رسائل معتمدة فقط. القاعدة الثابتة: كل رسالة تواجه العميل مسودة + موافقة بشرية أولاً؛ لا إرسال جماعي بارد.

### النطاق

- **مدعوم:** إرسال رسائل فردية معتمدة (نص و/أو HTML)، تحديد عنوان رد.
- **غير مدعوم:** الإرسال الجماعي غير المطلوب، الإرسال لقوائم لم توافق، أي رسالة دون موافقة موثّقة.

### المزوّدون المدعومون

ينفّذ `EmailClient` في `integrations/email.py` ثلاثة مسارات، يُختار المزوّد من `settings.email_provider`:

- **Resend** (المفضّل) — `_send_resend`، يُقرأ `resend_api_key` كقيمة سرّية.
- **SendGrid** — `_send_sendgrid`، يُقرأ `sendgrid_api_key` كقيمة سرّية.
- **SMTP** (احتياطي) — `_send_smtp`، يستخدم `smtp_host` و`smtp_user` و`smtp_password`.

كل مسار يُرجِع `EmailResult` بـ `success` و`provider` و`message_id` أو `error`.

### الموثوقية

- إعادة المحاولة بتراجع أسّي عبر `tenacity` لـ Resend وSendGrid على المهلات وأخطاء HTTP (3 محاولات).
- المهلة 30 ثانية لكل نداء HTTP.
- حد المعدّل: 120 نداء/دقيقة عبر `ConnectorPolicy` للموصّل `email`.
- الفشل النهائي يُدفَع إلى طابور `outbound` في DLQ ولا يكسر سير العمل.

### الحوكمة

- كل إرسال إجراء `external_send` يمر عبر `external_action_requires_approval` — يبقى مسودة حتى موافقة موثّقة.
- في sandbox، الإرسال يُوجَّه إلى نطاق اختبار أو يُكتب كمسودة عبر مزوّد الاختبار.
- لا تُكتب عناوين البريد الكاملة في قيد التدقيق — يُسجَّل المعرّف والنتيجة فقط.
- لا وعود بأرقام مبيعات أو نتائج مضمونة في نص الرسالة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| عميل البريد | `integrations/email.py` (`EmailClient`) |
| إرسال Resend | `integrations/email.py` (`_send_resend`) |
| إرسال SendGrid | `integrations/email.py` (`_send_sendgrid`) |
| إرسال SMTP | `integrations/email.py` (`_send_smtp`) |
| سياسة الموصّل | `dealix/connectors/connector_facade.py` (`email` في `DEFAULT_POLICIES`) |
| موافقة الإرسال الخارجي | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |

---

# English

## Email Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The email connector links Dealix to email providers to send approved messages only. The fixed rule: every customer-facing message is draft + human approval first; no cold bulk sending.

### Scope

- **Supported:** sending individual approved messages (text and/or HTML), setting a reply-to address.
- **Not supported:** unsolicited bulk sending, sending to lists that did not consent, any message without documented approval.

### Supported providers

`EmailClient` in `integrations/email.py` implements three paths, with the provider chosen from `settings.email_provider`:

- **Resend** (preferred) — `_send_resend`, reads `resend_api_key` as a secret value.
- **SendGrid** — `_send_sendgrid`, reads `sendgrid_api_key` as a secret value.
- **SMTP** (fallback) — `_send_smtp`, uses `smtp_host`, `smtp_user`, and `smtp_password`.

Each path returns an `EmailResult` with `success`, `provider`, and `message_id` or `error`.

### Reliability

- Exponential backoff retry via `tenacity` for Resend and SendGrid on timeouts and HTTP errors (3 attempts).
- A 30-second timeout per HTTP call.
- Rate limit: 120 calls/minute via the `ConnectorPolicy` for the `email` connector.
- Final failure is pushed to the `outbound` DLQ queue and does not break the workflow.

### Governance

- Every send is an `external_send` action and passes `external_action_requires_approval` — it stays a draft until documented approval.
- In sandbox, sending is routed to a test domain or written as a draft via the test provider.
- Full email addresses are not written to the audit log — only the ID and result are recorded.
- No promises of sales numbers or guaranteed results in the message body.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Email client | `integrations/email.py` (`EmailClient`) |
| Resend send | `integrations/email.py` (`_send_resend`) |
| SendGrid send | `integrations/email.py` (`_send_sendgrid`) |
| SMTP send | `integrations/email.py` (`_send_smtp`) |
| Connector policy | `dealix/connectors/connector_facade.py` (`email` in `DEFAULT_POLICIES`) |
| External send approval | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |
