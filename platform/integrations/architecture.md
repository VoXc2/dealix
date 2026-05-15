# العربية

## معمارية التنفيذ والتكاملات — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead) — قسم هندسة المنصة.

### الغرض

الطبقة 6 — التنفيذ والتكاملات — تحوّل Dealix من منصة "تفكّر" إلى منصة "تنفّذ بأمان". تربط أنظمة العميل (CRM، واتساب، البريد، التقويم، Google Drive، Sheets، Slack/Teams، التذاكر) وتشغّل إجراءات حقيقية عبر طبقة موحّدة تفرض المهل الزمنية، إعادة المحاولة، عدم التكرار (idempotency)، قواطع الدائرة، حدود المعدّل، والموافقة البشرية على كل إرسال خارجي. لا تبدأ هذه الطبقة أي محادثة باردة ولا تجمع بيانات بالكشط؛ كل إرسال يواجه العميل يكون مسودة أولاً وبموافقة أولاً.

### المكوّنات

- **واجهة الموصّلات الموحّدة (Connector Facade):** نقطة دخول واحدة لكل نداء خارجي عبر `dealix/connectors/connector_facade.py`، تفرض المهلة وإعادة المحاولة وقاطع الدائرة ومفتاح عدم التكرار وقيد التدقيق.
- **محوّلات المزوّدين (Provider Adapters):** عملاء رفيعون لكل نظام في `integrations/` الجذري (`whatsapp.py`, `email.py`, `calendar.py`, `hubspot.py`).
- **سجل التكاملات (Integration Registry):** مصدر الحقيقة للتكاملات المعرّفة، حالتها، نطاقاتها، وبيئتها (sandbox/live) — موثّق في `platform/integrations/integration_registry.md`.
- **طبقة الموثوقية (Reliability):** عدم التكرار عبر `dealix/reliability/idempotency.py`، إعادة المحاولة عبر `dealix/reliability/retry.py`، طابور الرسائل الفاشلة عبر `dealix/reliability/dlq.py`.
- **بوّابة الموافقة (Approval Gate):** كل إجراء بتصنيف `external_send` يمر عبر قاعدة `external_action_requires_approval` قبل التنفيذ.
- **التحقق من Webhooks:** التحقق من التواقيع لكل حمولة واردة قبل المعالجة.
- **وضع Sandbox:** كل تكامل له بيئة محاكاة معزولة — موثّق في `platform/integrations/sandbox_mode.md`.

### تدفّق البيانات

1. يطلب وكيل في الطبقة 2 إجراءً خارجياً ويرفعه كعقد إلى مستوى التنفيذ.
2. تتحقق بوّابة الموافقة من تصنيف الإجراء؛ إجراءات `external_send` تبقى مسودة حتى موافقة بشرية موثّقة.
3. تستلم واجهة الموصّلات النداء، تحسب مفتاح عدم التكرار، وتفحص حد المعدّل وقاطع الدائرة.
4. ينفّذ محوّل المزوّد النداء مع مهلة زمنية؛ يُعاد المحاولة بتراجع أسّي عند الفشل العابر.
5. الفشل النهائي يُدفع إلى طابور الرسائل الفاشلة لإعادة تشغيل المشغّل — دون كسر سير العمل.
6. تُكتب نتيجة كل نداء كقيد تدقيق (`connector_audit`) وتظهر في لوحة صحة التكاملات.
7. الـ Webhooks الواردة تُتحقَّق توقيعاتها، تُفحص ضد متجر عدم التكرار، ثم تُعالَج.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي في المستودع |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| محوّل واتساب | `integrations/whatsapp.py` |
| محوّل البريد | `integrations/email.py` |
| محوّل التقويم | `integrations/calendar.py` |
| محوّل HubSpot | `integrations/hubspot.py` |
| عدم التكرار | `dealix/reliability/idempotency.py` |
| إعادة المحاولة | `dealix/reliability/retry.py` |
| طابور الرسائل الفاشلة | `dealix/reliability/dlq.py` |
| موافقة الإجراءات الخارجية | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |
| منع واتساب البارد | `auto_client_acquisition/governance_os/rules/no_cold_whatsapp.yaml` |
| مطابقة المدفوعات | `auto_client_acquisition/payment_ops/reconciliation.py` |

انظر أيضاً: `platform/integrations/readiness.md`، `platform/integrations/integration_registry.md`، `platform/integrations/auth_flows.md`، `platform/integrations/webhook_security.md`.

---

# English

## Execution & Integrations Architecture — Layer 6

**Owner:** Integrations Platform Lead — Platform Engineering.

### Purpose

Layer 6 — Execution & Integrations — turns Dealix from a platform that "thinks" into one that "executes safely". It connects customer systems (CRM, WhatsApp, email, calendar, Google Drive, Sheets, Slack/Teams, ticketing) and runs real actions through one shared layer that enforces timeouts, retries, idempotency, circuit breakers, rate limits, and human approval on every external send. This layer never starts a cold conversation and never collects data by scraping; every customer-facing send is draft-first and approval-first.

### Components

- **Connector Facade:** a single entrypoint for every external call via `dealix/connectors/connector_facade.py`, enforcing timeout, retry, circuit breaker, idempotency key, and an audit entry.
- **Provider Adapters:** thin per-system clients in the root `integrations/` package (`whatsapp.py`, `email.py`, `calendar.py`, `hubspot.py`).
- **Integration Registry:** source of truth for defined integrations, their status, scopes, and environment (sandbox/live) — documented in `platform/integrations/integration_registry.md`.
- **Reliability layer:** idempotency via `dealix/reliability/idempotency.py`, retry via `dealix/reliability/retry.py`, dead-letter queue via `dealix/reliability/dlq.py`.
- **Approval Gate:** every `external_send`-class action passes the `external_action_requires_approval` rule before execution.
- **Webhook verification:** signature verification for every inbound payload before processing.
- **Sandbox mode:** every integration has an isolated simulation environment — documented in `platform/integrations/sandbox_mode.md`.

### Data flow

1. A Layer 2 agent requests an external action and raises it as a contract to the Execution Plane.
2. The Approval Gate checks the action class; `external_send` actions stay as drafts until a documented human approval.
3. The Connector Facade receives the call, computes an idempotency key, and checks rate limit and circuit breaker.
4. The provider adapter executes the call with a timeout; transient failures retry with exponential backoff.
5. Final failure is pushed to the dead-letter queue for operator replay — without breaking the workflow.
6. Each call result is written as an audit entry (`connector_audit`) and surfaces on the integration health dashboard.
7. Inbound webhooks are signature-verified, checked against the idempotency store, then processed.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| WhatsApp adapter | `integrations/whatsapp.py` |
| Email adapter | `integrations/email.py` |
| Calendar adapter | `integrations/calendar.py` |
| HubSpot adapter | `integrations/hubspot.py` |
| Idempotency | `dealix/reliability/idempotency.py` |
| Retry | `dealix/reliability/retry.py` |
| Dead-letter queue | `dealix/reliability/dlq.py` |
| External action approval | `auto_client_acquisition/governance_os/rules/external_action_requires_approval.yaml` |
| No cold WhatsApp | `auto_client_acquisition/governance_os/rules/no_cold_whatsapp.yaml` |
| Payment reconciliation | `auto_client_acquisition/payment_ops/reconciliation.py` |

See also: `platform/integrations/readiness.md`, `platform/integrations/integration_registry.md`, `platform/integrations/auth_flows.md`, `platform/integrations/webhook_security.md`.
