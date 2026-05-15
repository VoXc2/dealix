# العربية

## تدفّقات المصادقة وإدارة المفاتيح — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

كل تكامل خارجي يحتاج إلى بيانات اعتماد. هذا المستند يحدّد كيف تحصل Dealix على المفاتيح والرموز، وكيف تخزّنها مشفّرة، وكيف تدوّرها، ومن يملك صلاحية الوصول. القاعدة الثابتة: لا رمز مكشوف في السجلات أو الشيفرة أو الردود.

### أنماط المصادقة المدعومة

- **OAuth 2.0 برمز تحديث (Authorization Code):** المسار المفضّل لـ HubSpot وZoho وSalesforce وGoogle (Calendar/Drive/Sheets). يخزّن Dealix رمز التحديث المشفّر ويجدّد رمز الوصول قصير العمر عند الحاجة.
- **رموز وصول دائمة (Long-lived tokens):** واتساب للأعمال (Meta) — يُقرأ من `whatsapp_access_token` كقيمة سرّية عبر `core.config.settings`.
- **مفاتيح API:** البريد (Resend/SendGrid)، Calendly — تُقرأ كقيم سرّية ولا تُطبع أبداً.
- **حساب خدمة (Service Account):** Google Calendar عبر ملف مفتاح JSON كما في `integrations/calendar.py`.

### تدفّق OAuth (مثال CRM)

1. يبدأ مالك الحساب في العميل تفويض OAuth من لوحة Dealix.
2. يعيد المزوّد رمز تفويض إلى عنوان إعادة التوجيه المسجَّل.
3. تستبدل Dealix الرمز برمز وصول ورمز تحديث.
4. يُشفَّر رمز التحديث ويُخزَّن مربوطاً بـ `tenant_id` للعميل.
5. عند كل نداء، يُجدَّد رمز الوصول إذا انتهى — دون تدخّل بشري.
6. سحب التفويض من جانب العميل يُبطل التكامل فوراً ويوقف كل الأفعال.

### تخزين المفاتيح وتشفيرها

- تُقرأ كل الأسرار عبر `core.config.settings` كأنواع سرّية (`SecretStr`)؛ لا يُطبع `get_secret_value()` في أي سجل.
- الأسرار المخزّنة في قاعدة البيانات تُشفَّر بمفتاح يديره مزوّد إدارة الأسرار (KMS أو ما يعادله).
- لا تُكتب الأسرار في `connector_audit` — يُسجَّل فقط معرّف الموصّل ونتيجة النداء.
- خطافات الويب تُسجَّل ببصمة مجزّأة للمفتاح وليس بالمفتاح نفسه (انظر `idem_mark_failed` في `idempotency.py`).

### التدوير والإبطال

- تُدوَّر مفاتيح API كل 90 يوماً أو فوراً عند أي اشتباه تسريب.
- يُحتفظ بالمفتاح القديم نافذاً لمدة سماح قصيرة لتجنّب انقطاع الخدمة.
- إبطال أي مفتاح إجراء بتصنيف A2 ويُسجَّل كقيد تدقيق.
- اختبار التدوير الربعي جزء من قائمة جاهزية الطبقة 6.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| قراءة الأسرار | `core.config.settings` (مستهلك في `integrations/whatsapp.py`، `integrations/email.py`) |
| حساب خدمة Google | `integrations/calendar.py` |
| سياسات الموصّلات | `dealix/connectors/connector_facade.py` |
| سجل التكاملات | `platform/integrations/integration_registry.md` |

---

# English

## Authentication Flows and Key Management — Layer 6

**Owner:** Integrations Platform Lead.

### Purpose

Every external integration needs credentials. This document defines how Dealix obtains keys and tokens, stores them encrypted, rotates them, and who may access them. The fixed rule: no token exposed in logs, code, or responses.

### Supported authentication patterns

- **OAuth 2.0 with refresh token (Authorization Code):** the preferred path for HubSpot, Zoho, Salesforce, and Google (Calendar/Drive/Sheets). Dealix stores the encrypted refresh token and renews the short-lived access token on demand.
- **Long-lived access tokens:** WhatsApp Business (Meta) — read from `whatsapp_access_token` as a secret value via `core.config.settings`.
- **API keys:** email (Resend/SendGrid), Calendly — read as secret values and never printed.
- **Service account:** Google Calendar via a JSON key file as in `integrations/calendar.py`.

### OAuth flow (CRM example)

1. The customer account owner starts OAuth authorization from the Dealix console.
2. The provider returns an authorization code to the registered redirect URI.
3. Dealix exchanges the code for an access token and a refresh token.
4. The refresh token is encrypted and stored bound to the customer's `tenant_id`.
5. On each call, the access token is renewed if expired — without human intervention.
6. Authorization revocation on the customer side disables the integration immediately and halts all actions.

### Key storage and encryption

- All secrets are read via `core.config.settings` as secret types (`SecretStr`); `get_secret_value()` is never printed to any log.
- Secrets stored in the database are encrypted with a key managed by the secrets manager (KMS or equivalent).
- Secrets are never written to `connector_audit` — only the connector identifier and call result are logged.
- Webhooks are logged with a hashed fingerprint of the key, not the key itself (see `idem_mark_failed` in `idempotency.py`).

### Rotation and revocation

- API keys are rotated every 90 days or immediately on any suspected leak.
- The old key stays valid for a short grace period to avoid service interruption.
- Revoking any key is an A2-class action and is recorded as an audit entry.
- A quarterly rotation drill is part of the Layer 6 readiness checklist.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Secret reads | `core.config.settings` (consumed in `integrations/whatsapp.py`, `integrations/email.py`) |
| Google service account | `integrations/calendar.py` |
| Connector policies | `dealix/connectors/connector_facade.py` |
| Integration registry | `platform/integrations/integration_registry.md` |
