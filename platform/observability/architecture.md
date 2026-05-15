# العربية

## معمارية المراقبة — الطبقة السابعة

### الغرض

الطبقة السابعة تجيب عن سؤال واحد: ماذا يحدث الآن داخل كل وكيل وكل سير عمل وكل واجهة برمجية وكل أداة؟ هدفها أن يصبح أي طلب قابلاً للتتبع من بدايته حتى نهايته، وأن يُعرف أي وكيل فشل ولماذا، وأن تُطلق التنبيهات عند الفشل قبل أن يبلّغ العميل عنه.

### المكوّنات

- **التتبع الموزّع (Tracing):** يستند إلى OpenTelemetry عبر `dealix/observability/otel.py`. يوفّر spans للوكلاء والأدوات واستدعاءات النماذج، ويعمل بوضع لا-عملية آمن عند غياب المُصدِّر.
- **محوّلات المراقبة (Adapters):** `auto_client_acquisition/observability_adapters/` تضم المحوّل الأساسي ومحوّل OpenTelemetry ومحوّل Langfuse، جميعها فاشلة-بأمان ولا ترفع استثناءات.
- **التقاط الأخطاء:** `dealix/observability/sentry.py` يلتقط الاستثناءات غير المُعالَجة مع تنقية البيانات الشخصية قبل الإرسال.
- **تتبع التكلفة والرموز:** `dealix/observability/cost_tracker.py` يسجّل كل استدعاء نموذج مع الرموز والتكلفة التقديرية.
- **سجلّ التتبع للوكلاء:** `api/routers/agent_observability.py` يكشف تتبعات الوكلاء وملخّص التكلفة.
- **سجلّ التدقيق والحوادث (v6):** `api/routers/observability_v6.py` للقراءة فقط مع سجلّ حوادث ملحَق فقط.
- **مخطط التتبع المتوافق مع OTel (v10):** `api/routers/observability_v10.py` يطبّق تنقية البيانات الشخصية عند الإدراج.
- **مرشّح التنقية:** `auto_client_acquisition/observability_adapters/redaction.py` يزيل الهواتف والبريد والمفاتيح وأرقام السجل التجاري قبل أي بثّ.

### تدفّق البيانات

1. يدخل الطلب عبر `api/middleware.py` فيُولَّد `request_id` أو يُؤخذ من رأس `X-Request-ID`.
2. تُنشأ span جذرية لكل طلب عبر `instrument_fastapi`؛ وتُولَّد spans فرعية للوكيل والأداة والنموذج.
3. كل استدعاء نموذج يُسجَّل في `cost_tracker` مع الرموز والتكلفة وزمن الاستجابة.
4. تُكتب الأحداث المنظَّمة عبر `ObservabilityEvent` وتمرّ على `RedactionFilter` قبل البثّ.
5. تُصدَّر التتبعات عبر OTLP/HTTP إلى المُصدِّر المُكوَّن؛ وتلتقط Sentry الأخطاء.
6. لوحات المعلومات تقرأ من نقاط `recent` و`cost-summary` و`audit`؛ وتُقيَّم قواعد التنبيه على المقاييس المجمَّعة.

### الربط بالكود القائم

| المكوّن | المسار في المستودع |
|---|---|
| إعداد التتبع وspans | `dealix/observability/otel.py` |
| تتبع التكلفة والرموز | `dealix/observability/cost_tracker.py` |
| التقاط الأخطاء | `dealix/observability/sentry.py` |
| المحوّل الأساسي والحدث | `auto_client_acquisition/observability_adapters/base.py` |
| محوّل OpenTelemetry | `auto_client_acquisition/observability_adapters/otel_adapter.py` |
| محوّل Langfuse | `auto_client_acquisition/observability_adapters/langfuse_adapter.py` |
| مرشّح تنقية البيانات | `auto_client_acquisition/observability_adapters/redaction.py` |
| واجهة تتبع الوكلاء | `api/routers/agent_observability.py` |
| التدقيق والحوادث | `api/routers/observability_v6.py` |
| مخطط التتبع v10 | `api/routers/observability_v10.py` |
| توليد `request_id` | `api/middleware.py` |
| قواعد تنبيه Sentry | `docs/observability/sentry_alerts.yaml` |
| متغيرات البيئة | `docs/OBSERVABILITY_ENV.md` |

# English

## Observability Architecture — Layer 7

### Purpose

Layer 7 answers one question: what is happening right now inside every agent, workflow, API, and tool? Its goal is to make any request traceable end to end, to make it clear which agent failed and why, and to fire alerts on failure before a customer reports it.

### Components

- **Distributed tracing:** built on OpenTelemetry via `dealix/observability/otel.py`. It provides spans for agents, tools, and LLM calls, and runs in a safe no-op mode when no exporter is configured.
- **Observability adapters:** `auto_client_acquisition/observability_adapters/` holds the base adapter, the OpenTelemetry adapter, and the Langfuse adapter — all fail-safe and never raising.
- **Error capture:** `dealix/observability/sentry.py` captures unhandled exceptions with PII scrubbing before transmission.
- **Cost and token tracking:** `dealix/observability/cost_tracker.py` records every LLM call with tokens and estimated cost.
- **Agent trace surface:** `api/routers/agent_observability.py` exposes agent traces and a cost summary.
- **Audit and incident log (v6):** `api/routers/observability_v6.py`, read-only with an append-only incident log.
- **OTel-aligned trace schema (v10):** `api/routers/observability_v10.py` applies PII redaction on insert.
- **Redaction filter:** `auto_client_acquisition/observability_adapters/redaction.py` removes phones, emails, keys, and CR numbers before any emission.

### Data flow

1. A request enters via `api/middleware.py`, which generates a `request_id` or takes it from the `X-Request-ID` header.
2. A root span is created per request via `instrument_fastapi`; child spans are created for agent, tool, and model.
3. Every LLM call is recorded in `cost_tracker` with tokens, cost, and latency.
4. Structured events are written via `ObservabilityEvent` and pass through `RedactionFilter` before emission.
5. Traces are exported via OTLP/HTTP to the configured exporter; Sentry captures errors.
6. Dashboards read from the `recent`, `cost-summary`, and `audit` endpoints; alert rules are evaluated on aggregated metrics.

### Mapping to existing code

| Component | Repo path |
|---|---|
| Tracing setup and spans | `dealix/observability/otel.py` |
| Cost and token tracking | `dealix/observability/cost_tracker.py` |
| Error capture | `dealix/observability/sentry.py` |
| Base adapter and event | `auto_client_acquisition/observability_adapters/base.py` |
| OpenTelemetry adapter | `auto_client_acquisition/observability_adapters/otel_adapter.py` |
| Langfuse adapter | `auto_client_acquisition/observability_adapters/langfuse_adapter.py` |
| PII redaction filter | `auto_client_acquisition/observability_adapters/redaction.py` |
| Agent trace surface | `api/routers/agent_observability.py` |
| Audit and incidents | `api/routers/observability_v6.py` |
| Trace schema v10 | `api/routers/observability_v10.py` |
| `request_id` generation | `api/middleware.py` |
| Sentry alert rules | `docs/observability/sentry_alerts.yaml` |
| Environment variables | `docs/OBSERVABILITY_ENV.md` |
