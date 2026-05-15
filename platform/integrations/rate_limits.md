# العربية

## حدود المعدّل وقواطع الدائرة — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

كل مزوّد خارجي يفرض حدوداً على عدد النداءات. هذا المستند يحدّد كيف تحترم Dealix هذه الحدود، وكيف تحمي نفسها وأنظمة العميل من الإغراق، وكيف تتعامل مع تدهور المزوّد. القاعدة الثابتة: لكل تكامل حد معدّل صريح.

### حدود المعدّل لكل موصّل

تُعرَّف الحدود في `DEFAULT_POLICIES` داخل `dealix/connectors/connector_facade.py` عبر `ConnectorPolicy`:

| الموصّل | نداءات/دقيقة | المهلة (ث) | إعادة المحاولة | عدم تكرار مطلوب |
|---|---|---|---|---|
| `hubspot` | 100 | 8 | 3 | نعم |
| `whatsapp` | 90 | 10 | 3 | لا |
| `email` | 120 | 15 | 3 | لا |
| `calendly` | 60 | 8 | 3 | لا |
| `enrich_so` | 30 | 15 | 3 | لا |
| `n8n` | 200 | 10 | 3 | لا |
| `linkedin` | 20 | 15 | 3 | لا |

أي موصّل غير مُدرَج يأخذ `ConnectorPolicy` الافتراضية: 120 نداء/دقيقة، مهلة 10 ثوانٍ، 3 محاولات.

### قاطع الدائرة

ينفّذ `BreakerState` في `connector_facade.py` قاطع دائرة لكل موصّل:

- **مغلق (طبيعي):** النداءات تمر؛ يُعاد عدّاد الأخطاء عند كل نجاح.
- **مفتوح:** بعد 5 أخطاء متتالية يُفتح القاطع لمدة 30 ثانية؛ النداءات تُرفَض فوراً برسالة `circuit_open`.
- **نصف مفتوح:** بعد فترة التهدئة يُسمح بنداء تجريبي واحد؛ النجاح يغلق القاطع، الفشل يعيد فتحه.

هذا يمنع إغراق مزوّد متدهور ويحمي سير عمل Dealix من الانتظار الطويل.

### إعادة المحاولة والتراجع

- يُعاد المحاولة بتراجع أسّي: `backoff_base * 2^(attempt-1)` كما في `connector_facade.py` و`dealix/reliability/retry.py`.
- يُضاف ارتجاف (jitter) لتفادي تزامن إعادة المحاولات.
- بعد استنفاد المحاولات يُدفَع الإجراء إلى DLQ ولا يُعاد إلى ما لا نهاية.

### المراقبة

- تجاوز حد المعدّل أو فتح القاطع يُسجَّل في `connector_audit` ويظهر في لوحة الصحة.
- عمق DLQ المتزايد لموصّل معيّن مؤشر على تدهور مستمر.
- تنبيه للمالك عند بقاء قاطع أي موصّل مفتوحاً أكثر من نافذة محدّدة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| سياسات حدود المعدّل | `dealix/connectors/connector_facade.py` (`DEFAULT_POLICIES`, `ConnectorPolicy`) |
| قاطع الدائرة | `dealix/connectors/connector_facade.py` (`BreakerState`) |
| إعادة المحاولة بالتراجع | `dealix/reliability/retry.py` (`retry_with_backoff`) |
| طابور الرسائل الفاشلة | `dealix/reliability/dlq.py` |

---

# English

## Rate Limits and Circuit Breakers — Layer 6

**Owner:** Integrations Platform Lead.

### Purpose

Every external provider enforces limits on call volume. This document defines how Dealix respects those limits, protects itself and customer systems from flooding, and handles provider degradation. The fixed rule: every integration has an explicit rate limit.

### Rate limits per connector

Limits are defined in `DEFAULT_POLICIES` inside `dealix/connectors/connector_facade.py` via `ConnectorPolicy`:

| Connector | Calls/minute | Timeout (s) | Retries | Idempotency required |
|---|---|---|---|---|
| `hubspot` | 100 | 8 | 3 | Yes |
| `whatsapp` | 90 | 10 | 3 | No |
| `email` | 120 | 15 | 3 | No |
| `calendly` | 60 | 8 | 3 | No |
| `enrich_so` | 30 | 15 | 3 | No |
| `n8n` | 200 | 10 | 3 | No |
| `linkedin` | 20 | 15 | 3 | No |

Any connector not listed takes the default `ConnectorPolicy`: 120 calls/minute, 10-second timeout, 3 retries.

### Circuit breaker

`BreakerState` in `connector_facade.py` implements a per-connector circuit breaker:

- **Closed (normal):** calls pass; the error counter resets on each success.
- **Open:** after 5 consecutive errors the breaker opens for 30 seconds; calls are rejected immediately with a `circuit_open` message.
- **Half-open:** after the cooldown one trial call is allowed; success closes the breaker, failure reopens it.

This prevents flooding a degraded provider and protects the Dealix workflow from long waits.

### Retry and backoff

- Retries use exponential backoff: `backoff_base * 2^(attempt-1)` as in `connector_facade.py` and `dealix/reliability/retry.py`.
- Jitter is added to avoid retry synchronization.
- After retries are exhausted the action is pushed to the DLQ and is not retried indefinitely.

### Monitoring

- A rate-limit breach or breaker open is logged in `connector_audit` and surfaces on the health dashboard.
- Growing DLQ depth for a specific connector indicates sustained degradation.
- The owner is alerted when any connector breaker stays open beyond a defined window.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Rate limit policies | `dealix/connectors/connector_facade.py` (`DEFAULT_POLICIES`, `ConnectorPolicy`) |
| Circuit breaker | `dealix/connectors/connector_facade.py` (`BreakerState`) |
| Backoff retry | `dealix/reliability/retry.py` (`retry_with_backoff`) |
| Dead letter queue | `dealix/reliability/dlq.py` |
