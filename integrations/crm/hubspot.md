# العربية

## موصّل HubSpot CRM — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل HubSpot يربط Dealix بنظام HubSpot CRM للعميل: مزامنة جهات الاتصال والصفقات في الاتجاهين. القاعدة الثابتة: كل كتابة تواجه العميل تتطلب موافقة، وكل عملية قابلة للإعادة دون تكرار.

### النطاق

- **مدعوم:** إنشاء/تحديث جهات اتصال (upsert)، إنشاء صفقات، استقبال تحديثات HubSpot الواردة عبر خطافات الويب.
- **غير مدعوم:** حذف سجلات بالجملة، الكتابة دون موافقة، أي إجراء يتجاوز قواعد الحوكمة.

### العمليات

- **upsert جهة اتصال:** ينفّذ `HubSpotTwoWay.upsert_contact` بحثاً أولاً عبر البريد، ثم `PATCH` إن وُجد السجل أو `POST` إن لم يوجد — هذا يجعل العملية قابلة للإعادة بطبيعتها.
- **مزامنة عميل محتمل:** `HubSpotClient.sync_lead` يغلّف `CRMAgent` لمزامنة عميل محتمل وإنشاء صفقة اختيارياً.
- **خطاف وارد:** `handle_inbound_webhook` يعالج تحديثات جهات الاتصال من HubSpot ويُرجِع عدد الأحداث المعالَجة.

### الموثوقية

- حد المعدّل: 100 نداء/دقيقة، مهلة 8 ثوانٍ، 3 محاولات — من `ConnectorPolicy` للموصّل `hubspot`.
- `require_idempotency = true` للموصّل `hubspot` — كل عملية تحمل مفتاح عدم تكرار.
- الفشل النهائي يُدفَع إلى طابور `crm_sync` في DLQ ولا يكسر سير العمل.
- قاطع الدائرة يحمي من إغراق HubSpot عند تدهوره.

### المصادقة

- رمز وصول HubSpot يُقرأ من `HUBSPOT_ACCESS_TOKEN` كقيمة سرّية؛ لا يُطبع في أي سجل.
- المسار الموصى به للإنتاج: OAuth برمز تحديث (انظر `platform/integrations/auth_flows.md`).

### الحوكمة

- الكتابة التي تواجه العميل (مثل تحديث ينعكس على تواصل) تمر عبر `external_action_requires_approval`.
- لا تُكتب بيانات شخصية في قيد التدقيق — يُسجَّل معرّف العملية ونتيجتها فقط.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| موصّل HubSpot ثنائي الاتجاه | `dealix/connectors/connector_facade.py` (`HubSpotTwoWay`) |
| غلاف HubSpot | `integrations/hubspot.py` (`HubSpotClient`) |
| وكيل CRM | `auto_client_acquisition/agents/crm.py` (`CRMAgent`) |
| سياسة الموصّل | `dealix/connectors/connector_facade.py` (`hubspot` في `DEFAULT_POLICIES`) |
| طابور مزامنة CRM | `dealix/reliability/dlq.py` (`CRM_SYNC_DLQ`) |

---

# English

## HubSpot CRM Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The HubSpot connector links Dealix to a customer's HubSpot CRM: bidirectional sync of contacts and deals. The fixed rule: every customer-facing write requires approval, and every operation is idempotent with no duplicates.

### Scope

- **Supported:** create/update contacts (upsert), create deals, receive inbound HubSpot updates via webhooks.
- **Not supported:** bulk record deletion, writing without approval, any action that bypasses governance rules.

### Operations

- **Upsert contact:** `HubSpotTwoWay.upsert_contact` searches first by email, then `PATCH` if the record exists or `POST` if not — this makes the operation idempotent by nature.
- **Sync lead:** `HubSpotClient.sync_lead` wraps `CRMAgent` to sync a lead and optionally create a deal.
- **Inbound webhook:** `handle_inbound_webhook` processes contact updates from HubSpot and returns the count of processed events.

### Reliability

- Rate limit: 100 calls/minute, 8-second timeout, 3 retries — from the `ConnectorPolicy` for the `hubspot` connector.
- `require_idempotency = true` for the `hubspot` connector — every operation carries an idempotency key.
- Final failure is pushed to the `crm_sync` DLQ queue and does not break the workflow.
- The circuit breaker protects against flooding HubSpot when it degrades.

### Authentication

- The HubSpot access token is read from `HUBSPOT_ACCESS_TOKEN` as a secret value; never printed to any log.
- Recommended production path: OAuth with a refresh token (see `platform/integrations/auth_flows.md`).

### Governance

- A customer-facing write (e.g. an update that reflects in outreach) passes `external_action_requires_approval`.
- No personal data is written to the audit log — only the operation ID and result are recorded.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Two-way HubSpot connector | `dealix/connectors/connector_facade.py` (`HubSpotTwoWay`) |
| HubSpot wrapper | `integrations/hubspot.py` (`HubSpotClient`) |
| CRM agent | `auto_client_acquisition/agents/crm.py` (`CRMAgent`) |
| Connector policy | `dealix/connectors/connector_facade.py` (`hubspot` in `DEFAULT_POLICIES`) |
| CRM sync queue | `dealix/reliability/dlq.py` (`CRM_SYNC_DLQ`) |
