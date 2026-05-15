# العربية

## موصّل Salesforce CRM — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل Salesforce يربط Dealix بنظام Salesforce CRM للعميل. حالته الحالية **نموذج أولي** — قيد التطوير، لا يُستخدَم مع بيانات عميل حقيقية، ومقصور على بيئة Salesforce sandbox الرسمية. القاعدة الثابتة: لا كتابة على بيانات إنتاج عميل في طور النموذج الأولي.

### النطاق

- **مدعوم (نموذج أولي، sandbox فقط):** قراءة جهات الاتصال (Contacts/Leads) من Salesforce sandbox.
- **مخطّط له (بعد الترقية):** كتابة جهات اتصال وفرص (Opportunities) — بموافقة لكل كتابة تواجه العميل.
- **غير مدعوم:** أي نداء على Salesforce إنتاجي، الحذف بالجملة، تجاوز الحوكمة.

### التنفيذ

- يُستخدَم Salesforce عبر محوّل مزوّد يمر بواجهة الموصّلات الموحّدة في `dealix/connectors/connector_facade.py`.
- لا سياسة صريحة للموصّل `salesforce` في `DEFAULT_POLICIES`؛ يأخذ الافتراضية حتى تُضاف سياسة مخصّصة.
- Salesforce يفرض حدود API يومية صارمة — تُضاف سياسة محافظة عند الترقية.

### المصادقة

- Salesforce يستخدم OAuth 2.0؛ تدفّق JWT bearer موصى به للخوادم (انظر `platform/integrations/auth_flows.md`).
- بيئة sandbox الرسمية من Salesforce تستخدم نطاق `test.salesforce.com` المنفصل.
- الرموز تُخزَّن مشفّرة مربوطة بـ `tenant_id`.

### الموثوقية والحوكمة

- العمليات قابلة للإعادة عبر مفتاح عدم التكرار من واجهة الموصّلات.
- الفشل النهائي يُدفَع إلى طابور `crm_sync` في DLQ ولا يكسر سير العمل.
- قاطع الدائرة يحمي من تجاوز حدود API اليومية.
- أي كتابة مستقبلية تواجه العميل تمر عبر `external_action_requires_approval`.

### معايير الترقية من نموذج أولي إلى Pilot

1. سياسة صريحة محافظة لـ `salesforce` في `DEFAULT_POLICIES`.
2. وضع sandbox مُثبَت ببيئة Salesforce sandbox رسمية.
3. اجتياز حالات الاختبار ذات الصلة في `platform/integrations/tests.md`.
4. إثبات احترام حدود API اليومية تحت الحمل.
5. موافقة موثّقة من مالك المنصة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| سجل التكاملات | `platform/integrations/integration_registry.md` |
| تدفّقات المصادقة | `platform/integrations/auth_flows.md` |
| حدود المعدّل وقواطع الدائرة | `platform/integrations/rate_limits.md` |

---

# English

## Salesforce CRM Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The Salesforce connector links Dealix to a customer's Salesforce CRM. Its current status is **prototype** — under development, not used with real customer data, and limited to the official Salesforce sandbox environment. The fixed rule: no writes to customer production data while in the prototype stage.

### Scope

- **Supported (prototype, sandbox only):** reading contacts (Contacts/Leads) from a Salesforce sandbox.
- **Planned (after promotion):** writing contacts and Opportunities — with approval for every customer-facing write.
- **Not supported:** any call against a production Salesforce, bulk deletion, bypassing governance.

### Implementation

- Salesforce is used via a provider adapter that passes through the unified connector facade in `dealix/connectors/connector_facade.py`.
- There is no explicit policy for the `salesforce` connector in `DEFAULT_POLICIES`; it takes the default until a custom policy is added.
- Salesforce enforces strict daily API limits — a conservative policy is added on promotion.

### Authentication

- Salesforce uses OAuth 2.0; the JWT bearer flow is recommended for servers (see `platform/integrations/auth_flows.md`).
- The official Salesforce sandbox uses the separate `test.salesforce.com` domain.
- Tokens are stored encrypted bound to `tenant_id`.

### Reliability and governance

- Operations are idempotent via the idempotency key from the connector facade.
- Final failure is pushed to the `crm_sync` DLQ queue and does not break the workflow.
- The circuit breaker protects against exceeding daily API limits.
- Any future customer-facing write passes `external_action_requires_approval`.

### Promotion criteria from prototype to Pilot

1. An explicit conservative `salesforce` policy in `DEFAULT_POLICIES`.
2. A sandbox mode proven with an official Salesforce sandbox environment.
3. Passing the relevant test cases in `platform/integrations/tests.md`.
4. Proof of respecting daily API limits under load.
5. Documented approval from the platform owner.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| Integration registry | `platform/integrations/integration_registry.md` |
| Authentication flows | `platform/integrations/auth_flows.md` |
| Rate limits and circuit breakers | `platform/integrations/rate_limits.md` |
