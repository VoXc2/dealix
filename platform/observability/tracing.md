# العربية

## التتبّع الموزَّع — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

التتبّع يجيب على سؤال واحد: ما الذي حدث لهذا الطلب من بدايته إلى نهايته؟ كل طلب يحمل `trace_id` واحدًا، وتحته سلسلة امتدادات (spans) متداخلة: امتداد الواجهة البرمجية، ثم امتداد سير العمل، ثم امتداد كل وكيل، ثم امتداد كل أداة، ثم امتداد كل نداء نموذج لغوي. عند الفشل يظهر الامتداد الذي توقّف ونوع الخطأ.

### نموذج الامتدادات

`dealix/observability/otel.py` يوفّر ثلاثة مديري سياق:

- `agent_span(agent_name, **attrs)` — يحيط بتنفيذ وكيل، السمة `agent.name`.
- `tool_span(tool_name, **attrs)` — يحيط باستدعاء أداة، السمة `tool.name`.
- `llm_span(model, task, **attrs)` — يحيط بنداء نموذج لغوي، السمات `llm.model` و `llm.task`.

كما يُجهّز `setup_tracing` مزوّد OpenTelemetry، و`instrument_fastapi` يُجهّز FastAPI و HTTPX، و`instrument_sqlalchemy` يُجهّز قاعدة البيانات. عند غياب مكتبات OTel أو متغير `OTEL_EXPORTER_OTLP_ENDPOINT` تعمل الدوال بأمان دون أثر.

في سير عمل اكتساب العملاء يوفّر `auto_client_acquisition/observability_adapters/otel_adapter.py` المحوّل `OtelAdapter` مع `start_trace` و `end_trace` و `emit`، ويرجع إلى محوّل عدم العمل الآمن عند غياب الإعداد.

### تدفّق الأثر

1. يصل طلب؛ يُولَّد `request_id` أو يُؤخذ من `X-Request-ID`.
2. تُنشئ أدوات FastAPI امتداد الجذر.
3. سير العمل يفتح امتداده، وتحته `agent_span` لكل وكيل.
4. كل أداة داخل `tool_span`، وكل نداء نموذج داخل `llm_span`.
5. تُصدَّر الامتدادات عبر OTLP عبر `BatchSpanProcessor`.

### قائمة الجاهزية

- [x] كل سير عمل يحمل `trace_id` واحدًا.
- [x] كل نداء وكيل وأداة ونموذج لغوي ملفوف بامتداد.
- [x] رجوع آمن دون أثر عند غياب إعداد OTel.
- [x] محوّل OpenTelemetry للوكلاء فاشل-آمن (`OtelAdapter`).
- [ ] معدّل أخذ العيّنات (sampling) موثَّق ومضبوط لكل بيئة.
- [ ] تمرين موثَّق لتتبّع طلب فاشل من الواجهة حتى الأداة.

### المقاييس

- نسبة أسيرة العمل الحاملة لـ `trace_id`: 100% (هدف).
- نسبة نداءات الأدوات الملفوفة بامتداد: 100%.
- معدّل أخذ العيّنات للآثار في الإنتاج: قابل للضبط عبر `SENTRY_TRACES_SAMPLE_RATE` (افتراضي 0.1).
- زمن تتبّع طلب من الواجهة حتى الأداة: أقل من دقيقتين بحثًا.

### خطاطيف المراقبة

- إعداد التتبّع عبر `dealix/observability/otel.py`.
- امتدادات الوكلاء عبر `OtelAdapter` في `auto_client_acquisition/observability_adapters/otel_adapter.py`.
- ربط الأثر مع التكلفة عبر `request_id` المشترك مع `cost_tracker.py`.
- تتبّع أداء Sentry عبر `traces_sample_rate` في `sentry.py`.

### قواعد الحوكمة

- لا تُوضع PII في سمات الامتداد؛ تُستخدم `customer_handle` لا اسم العميل.
- لا تُوضع نصوص نداءات كاملة في الامتدادات.
- معدّل أخذ العيّنات يُغيَّر فقط بموافقة قائد موثوقية المنصة.
- التصدير الخارجي يُفعَّل في staging أولاً ثم production كما في `docs/OBSERVABILITY_ENV.md`.

### إجراء التراجع

1. إن سبّب التتبّع حملًا زائدًا، اخفض `SENTRY_TRACES_SAMPLE_RATE` أو ألغِ ضبط `OTEL_EXPORTER_OTLP_ENDPOINT`.
2. الدوال ترجع آمنة دون أثر عند غياب الإعداد — لا انقطاع خدمة.
3. استرجع الإصدار السابق من خدمة التتبّع إن تعطّل التصدير.
4. سجّل التراجع كقيد تدقيق وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 74 / 100 — بيتا داخلي (Internal Beta).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Distributed Tracing — Layer 7

Owner: Platform Reliability Lead

### Purpose

Tracing answers one question: what happened to this request from start to finish? Every request carries a single `trace_id`, and under it a chain of nested spans: the API span, then the workflow span, then a span per agent, then a span per tool, then a span per LLM call. On failure, the span that stopped and the error type are visible.

### Span model

`dealix/observability/otel.py` provides three context managers:

- `agent_span(agent_name, **attrs)` — wraps an agent execution, attribute `agent.name`.
- `tool_span(tool_name, **attrs)` — wraps a tool call, attribute `tool.name`.
- `llm_span(model, task, **attrs)` — wraps an LLM call, attributes `llm.model` and `llm.task`.

`setup_tracing` initializes the OpenTelemetry provider, `instrument_fastapi` instruments FastAPI and HTTPX, and `instrument_sqlalchemy` instruments the database. When OTel libraries or `OTEL_EXPORTER_OTLP_ENDPOINT` are absent, the functions run safely with no effect.

In the acquisition workflow, `auto_client_acquisition/observability_adapters/otel_adapter.py` provides `OtelAdapter` with `start_trace`, `end_trace`, and `emit`, falling back to the fail-safe noop adapter when unconfigured.

### Trace flow

1. A request arrives; `request_id` is generated or taken from `X-Request-ID`.
2. FastAPI instrumentation creates the root span.
3. The workflow opens its span, with an `agent_span` per agent under it.
4. Each tool runs inside a `tool_span`, each model call inside an `llm_span`.
5. Spans are exported over OTLP via `BatchSpanProcessor`.

### Readiness checklist

- [x] Every workflow carries a single `trace_id`.
- [x] Every agent, tool, and LLM call is wrapped in a span.
- [x] Safe no-effect fallback when OTel is unconfigured.
- [x] Agent OpenTelemetry adapter is fail-safe (`OtelAdapter`).
- [ ] Sampling rate documented and tuned per environment.
- [ ] Documented drill for tracing a failed request from API to tool.

### Metrics

- Workflows carrying a `trace_id`: 100% (target).
- Tool calls wrapped in a span: 100%.
- Trace sampling rate in production: tunable via `SENTRY_TRACES_SAMPLE_RATE` (default 0.1).
- Time to trace a request from API to tool: under 2 minutes of investigation.

### Observability hooks

- Tracing setup via `dealix/observability/otel.py`.
- Agent spans via `OtelAdapter` in `auto_client_acquisition/observability_adapters/otel_adapter.py`.
- Trace-to-cost correlation via the shared `request_id` with `cost_tracker.py`.
- Sentry performance tracing via `traces_sample_rate` in `sentry.py`.

### Governance rules

- No PII in span attributes; `customer_handle` is used, not a customer name.
- No full call transcripts in spans.
- The sampling rate is changed only with the Platform Reliability Lead's approval.
- External export is enabled in staging first, then production, per `docs/OBSERVABILITY_ENV.md`.

### Rollback procedure

1. If tracing causes excess load, lower `SENTRY_TRACES_SAMPLE_RATE` or unset `OTEL_EXPORTER_OTLP_ENDPOINT`.
2. The functions fall back safely with no effect when unconfigured — no service interruption.
3. Revert to the previous tracing service version if export breaks.
4. Record the rollback as an audit entry and notify the Platform Reliability Lead.

### Current readiness score

**Score: 74 / 100 — Internal Beta.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
