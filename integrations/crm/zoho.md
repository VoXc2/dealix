# العربية

## موصّل Zoho CRM — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل Zoho يربط Dealix بنظام Zoho CRM للعميل لمزامنة جهات الاتصال. حالته الحالية **تجريبي داخلي** — يعمل في بيئات Dealix الداخلية فقط ولم يُرقَّ بعد للاستخدام مع العملاء. القاعدة الثابتة: كل كتابة تواجه العميل تتطلب موافقة.

### النطاق

- **مدعوم (sandbox/تجريبي داخلي):** قراءة وكتابة جهات الاتصال (upsert)، استقبال تحديثات Zoho الواردة عبر خطافات موقّعة.
- **غير مدعوم:** الكتابة في الإنتاج قبل الترقية، الحذف بالجملة، أي إجراء يتجاوز الحوكمة.

### التنفيذ

- يُستخدَم Zoho عبر محوّل مزوّد يمر بواجهة الموصّلات الموحّدة في `dealix/connectors/connector_facade.py`.
- لا توجد سياسة صريحة للموصّل `zoho` في `DEFAULT_POLICIES`، لذا يأخذ `ConnectorPolicy` الافتراضية: 120 نداء/دقيقة، مهلة 10 ثوانٍ، 3 محاولات.
- إضافة سياسة صريحة لـ `zoho` شرط للترقية إلى `pilot`.

### المصادقة

- Zoho يستخدم OAuth 2.0 برمز تحديث (انظر `platform/integrations/auth_flows.md`).
- رمز التحديث يُخزَّن مشفّراً مربوطاً بـ `tenant_id` للعميل؛ رمز الوصول قصير العمر يُجدَّد عند الحاجة.
- مراكز بيانات Zoho متعددة المناطق — يُسجَّل المركز الصحيح لكل عميل.

### الموثوقية والحوكمة

- العمليات قابلة للإعادة عبر مفتاح عدم التكرار من واجهة الموصّلات.
- الفشل النهائي يُدفَع إلى طابور `crm_sync` في DLQ ولا يكسر سير العمل.
- الكتابة التي تواجه العميل تمر عبر `external_action_requires_approval`.
- الخطافات الواردة تُتحقَّق توقيعاتها قبل المعالجة (انظر `platform/integrations/webhook_security.md`).

### معايير الترقية إلى Pilot

1. سياسة صريحة لـ `zoho` في `DEFAULT_POLICIES`.
2. وضع sandbox مُثبَت بحساب اختبار Zoho.
3. اجتياز حالات الاختبار ذات الصلة في `platform/integrations/tests.md`.
4. موافقة موثّقة من مالك المنصة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| سجل التكاملات | `platform/integrations/integration_registry.md` |
| تدفّقات المصادقة | `platform/integrations/auth_flows.md` |
| طابور مزامنة CRM | `dealix/reliability/dlq.py` (`CRM_SYNC_DLQ`) |

---

# English

## Zoho CRM Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The Zoho connector links Dealix to a customer's Zoho CRM for contact sync. Its current status is **internal beta** — it runs only in Dealix internal environments and is not yet promoted for customer use. The fixed rule: every customer-facing write requires approval.

### Scope

- **Supported (sandbox/internal beta):** read and write contacts (upsert), receive inbound Zoho updates via signed webhooks.
- **Not supported:** production writes before promotion, bulk deletion, any action that bypasses governance.

### Implementation

- Zoho is used via a provider adapter that passes through the unified connector facade in `dealix/connectors/connector_facade.py`.
- There is no explicit policy for the `zoho` connector in `DEFAULT_POLICIES`, so it takes the default `ConnectorPolicy`: 120 calls/minute, 10-second timeout, 3 retries.
- Adding an explicit `zoho` policy is a condition for promotion to `pilot`.

### Authentication

- Zoho uses OAuth 2.0 with a refresh token (see `platform/integrations/auth_flows.md`).
- The refresh token is stored encrypted bound to the customer's `tenant_id`; the short-lived access token is renewed on demand.
- Zoho data centers are multi-region — the correct center is recorded per customer.

### Reliability and governance

- Operations are idempotent via the idempotency key from the connector facade.
- Final failure is pushed to the `crm_sync` DLQ queue and does not break the workflow.
- Customer-facing writes pass `external_action_requires_approval`.
- Inbound webhooks are signature-verified before processing (see `platform/integrations/webhook_security.md`).

### Promotion criteria to Pilot

1. An explicit `zoho` policy in `DEFAULT_POLICIES`.
2. A sandbox mode proven with a Zoho test account.
3. Passing the relevant test cases in `platform/integrations/tests.md`.
4. Documented approval from the platform owner.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| Integration registry | `platform/integrations/integration_registry.md` |
| Authentication flows | `platform/integrations/auth_flows.md` |
| CRM sync queue | `dealix/reliability/dlq.py` (`CRM_SYNC_DLQ`) |
