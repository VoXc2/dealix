# العربية

## سجل التكاملات — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

سجل التكاملات هو مصدر الحقيقة الوحيد لكل تكامل خارجي تعرفه Dealix: حالته، نطاقاته، بيئته (sandbox أو live)، مالكه، وقاعدة الحوكمة المرتبطة به. أي تكامل غير مسجَّل لا يُسمح له بتنفيذ نداء خارجي عبر `dealix/connectors/connector_facade.py`.

### حقول السجل لكل تكامل

- **المعرّف:** اسم الموصّل كما في `DEFAULT_POLICIES` داخل `connector_facade.py` (مثل `hubspot`, `whatsapp`, `email`).
- **الفئة:** CRM / مراسلة / تقويم / تخزين / جداول / دردشة فريق / تذاكر / مدفوعات.
- **الحالة:** `defined` / `sandbox_only` / `pilot` / `live` / `disabled`.
- **النطاقات:** الصلاحيات الممنوحة (قراءة فقط أو قراءة/كتابة)؛ الكتابة التي تواجه العميل تتطلب موافقة.
- **المالك:** الدور المسؤول عن صحة التكامل وتدويره.
- **قاعدة الحوكمة:** القاعدة المرتبطة في `auto_client_acquisition/governance_os/rules/`.
- **حد المعدّل:** من `ConnectorPolicy` في `connector_facade.py`.

### التكاملات المسجّلة الحالية

| المعرّف | الفئة | الحالة | كتابة تواجه العميل؟ | قاعدة الحوكمة |
|---|---|---|---|---|
| `hubspot` | CRM | pilot | نعم — بموافقة | `external_action_requires_approval` |
| `whatsapp` | مراسلة | sandbox_only | نعم — مسودة + موافقة | `no_cold_whatsapp`, `external_action_requires_approval` |
| `email` | مراسلة | pilot | نعم — مسودة + موافقة | `external_action_requires_approval` |
| `calendly` | تقويم | pilot | لا (روابط فقط) | — |
| `enrich_so` | إثراء | sandbox_only | لا | `no_scraping` |
| `n8n` | أتمتة | defined | لا | — |
| `linkedin` | — | disabled | لا | `no_linkedin_automation` |

### قواعد التسجيل

- لا يُضاف تكامل بحالة `live` قبل اجتياز قائمة جاهزية الطبقة 6.
- `linkedin` يبقى `disabled` دائماً — لا أتمتة LinkedIn ولا كشط (`no_linkedin_automation`, `no_scraping`).
- كل تكامل مراسلة يبدأ `sandbox_only` ويتطلب موافقة موثّقة للترقية إلى `pilot`.
- تغيير حالة أي تكامل إجراء بتصنيف A2 ويُسجَّل كقيد تدقيق.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| سياسات الموصّلات | `dealix/connectors/connector_facade.py` (`DEFAULT_POLICIES`) |
| قواعد الحوكمة | `auto_client_acquisition/governance_os/rules/` |
| محوّلات المزوّدين | `integrations/` (الجذر) |

---

# English

## Integration Registry — Layer 6

**Owner:** Integrations Platform Lead.

### Purpose

The integration registry is the single source of truth for every external integration Dealix knows: its status, scopes, environment (sandbox or live), owner, and bound governance rule. Any unregistered integration is not allowed to execute an external call through `dealix/connectors/connector_facade.py`.

### Registry fields per integration

- **Identifier:** the connector name as in `DEFAULT_POLICIES` inside `connector_facade.py` (e.g. `hubspot`, `whatsapp`, `email`).
- **Category:** CRM / messaging / calendar / storage / sheets / team chat / ticketing / payments.
- **Status:** `defined` / `sandbox_only` / `pilot` / `live` / `disabled`.
- **Scopes:** granted permissions (read-only or read/write); customer-facing writes require approval.
- **Owner:** the role accountable for integration health and rotation.
- **Governance rule:** the bound rule in `auto_client_acquisition/governance_os/rules/`.
- **Rate limit:** from `ConnectorPolicy` in `connector_facade.py`.

### Currently registered integrations

| Identifier | Category | Status | Customer-facing write? | Governance rule |
|---|---|---|---|---|
| `hubspot` | CRM | pilot | Yes — with approval | `external_action_requires_approval` |
| `whatsapp` | Messaging | sandbox_only | Yes — draft + approval | `no_cold_whatsapp`, `external_action_requires_approval` |
| `email` | Messaging | pilot | Yes — draft + approval | `external_action_requires_approval` |
| `calendly` | Calendar | pilot | No (links only) | — |
| `enrich_so` | Enrichment | sandbox_only | No | `no_scraping` |
| `n8n` | Automation | defined | No | — |
| `linkedin` | — | disabled | No | `no_linkedin_automation` |

### Registration rules

- No integration is added with `live` status before passing the Layer 6 readiness checklist.
- `linkedin` stays `disabled` permanently — no LinkedIn automation and no scraping (`no_linkedin_automation`, `no_scraping`).
- Every messaging integration starts `sandbox_only` and requires a documented approval to promote to `pilot`.
- Changing any integration status is an A2-class action and is recorded as an audit entry.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector policies | `dealix/connectors/connector_facade.py` (`DEFAULT_POLICIES`) |
| Governance rules | `auto_client_acquisition/governance_os/rules/` |
| Provider adapters | `integrations/` (root) |
