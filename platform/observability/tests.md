# العربية

## مواصفة اختبارات المراقبة — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

هذه مواصفة اختبار، لا كود. تصف حالات الاختبار ومعايير القبول التي تثبت أن الطبقة السابعة تعمل كما تدّعي وثائقها. كل حالة لها معرّف، وصف، خطوات، ومعيار قبول قابل للقياس.

### حالات الاختبار

#### OBS-T1 — تتبّع طلب من طرف لطرف

- **الخطوات:** أرسل طلبًا يستدعي سير عمل به وكيل وأداة ونداء نموذج لغوي.
- **معيار القبول:** يحمل الطلب `trace_id` واحدًا؛ تظهر امتدادات الواجهة وسير العمل والوكيل والأداة والنموذج متداخلة تحته؛ يمكن استرجاع الأثر كاملًا بمعرّفه.

#### OBS-T2 — تحديد الوكيل الفاشل وسبب فشله

- **الخطوات:** أجبر وكيلًا واحدًا على الفشل ضمن سير عمل.
- **معيار القبول:** يُحدِّد الأثر امتداد الوكيل الفاشل؛ يحمل الامتداد وسم `error_type` آمنًا؛ لا يحتوي الوسم على أثر تتبّع خام.

#### OBS-T3 — السجل المنظَّم يحمل معرّفات الارتباط

- **الخطوات:** افحص سجلات طلب نموذجي.
- **معيار القبول:** كل سطر سجل بصيغة JSON ويحمل `request_id` و `trace_id`؛ لا سطر بنصّ حر.

#### OBS-T4 — تنقية PII قبل البثّ

- **الخطوات:** مرّر نصًّا يحتوي هاتفًا وبريدًا ومفتاحًا و IBAN عبر `RedactionFilter`.
- **معيار القبول:** تُستبدل كل الأنماط الحساسة بوسوم `REDACTED_*`؛ ترجع `is_safe_for_external_log` القيمة false قبل التنقية و true بعدها.

#### OBS-T5 — تنقية أحداث Sentry

- **الخطوات:** التقط خطأ على مسار حسّاس (`/api/v1/checkout`، `/api/v1/webhooks/`).
- **معيار القبول:** تُستبدل رؤوس المصادقة وسلسلة الاستعلام وجسم الطلب بـ `<redacted>`؛ تُسقط أحداث مسارات `tests/` كاملةً.

#### OBS-T6 — تسجيل التكلفة والرموز لكل نداء نموذج

- **الخطوات:** سجّل نداء نموذج عبر `CostTracker.record`.
- **معيار القبول:** يحمل القيد المزوّد والنموذج ورموز الإدخال والإخراج والمخزَّنة والتكلفة التقديرية والزمن؛ يُحسب `cost_usd` عبر `estimate_cost_usd`.

#### OBS-T7 — تقدير تكلفة نموذج مجهول تحفّظي

- **الخطوات:** قدّر تكلفة نموذج غير موجود في `MODEL_PRICES`.
- **معيار القبول:** يُستخدم سعر نموذج تحفّظي مرتفع؛ لا يُقلَّل تقدير الإنفاق.

#### OBS-T8 — ملخّص التكلفة لكل وكيل وسير عمل

- **الخطوات:** استدعِ `/api/v1/agent-observability/cost-summary`.
- **معيار القبول:** يُرجِع تفصيلًا لكل وكيل ولكل سير عمل؛ يحمل الحقل `is_estimate` القيمة true.

#### OBS-T9 — التنبيه يُطلق عند الفشل

- **الخطوات:** حاكِ فشل webhook 5xx وعدم تطابق توقيع.
- **معيار القبول:** تتطابق قاعدة تنبيه في `sentry_alerts.yaml`؛ تنبيه عدم تطابق التوقيع لا يُكرَّر (`frequency_min: 0`).

#### OBS-T10 — رجوع آمن عند غياب إعداد المراقبة

- **الخطوات:** شغّل النظام دون `OTEL_EXPORTER_OTLP_ENDPOINT` ودون مفاتيح Langfuse.
- **معيار القبول:** ترجع الدوال إلى وضع عدم العمل الآمن؛ لا استثناء يُرفع؛ لا انقطاع خدمة.

#### OBS-T11 — لوحة لكل خدمة

- **الخطوات:** افحص تعريفات `observability/dashboards/`.
- **معيار القبول:** توجد لوحة للوكلاء وأخرى لأسيرة العمل وأخرى لنظام الإيراد؛ كل لوحة JSON صالحة بلوحات تحمل عنوانًا ومقياسًا واستعلامًا ونوعًا.

#### OBS-T12 — الحادث له مالك وحالة

- **الخطوات:** أنشئ سجل حادث وفق قالب `observability/incident_logs/README.md`.
- **معيار القبول:** يحمل السجل معرّفًا ودرجة خطورة ومالكًا واحدًا وحالة و `trace_id` مرتبطًا؛ لا يحتوي على PII.

### معايير القبول الإجمالية

- اجتياز كل حالات OBS-T1 إلى OBS-T12.
- صفر تسريبات PII في أي سجل أو امتداد أو سجل حادث.
- كل رقم تكلفة موسوم "تقديري".
- كل ملفات اللوحات JSON صالحة وكل ملفات التنبيهات YAML صالحة.

# English

## Observability Test Specification — Layer 7

Owner: Platform Reliability Lead

### Purpose

This is a test specification, not code. It describes the test cases and acceptance criteria proving Layer 7 works as its documentation claims. Each case has an ID, description, steps, and a measurable acceptance criterion.

### Test cases

#### OBS-T1 — End-to-end request tracing

- **Steps:** send a request that invokes a workflow with an agent, a tool, and an LLM call.
- **Acceptance:** the request carries a single `trace_id`; the API, workflow, agent, tool, and model spans appear nested under it; the full trace is retrievable by its identifier.

#### OBS-T2 — Identify the failed agent and its failure reason

- **Steps:** force a single agent to fail within a workflow.
- **Acceptance:** the trace identifies the failed agent's span; the span carries a safe `error_type` label; the label contains no raw stack trace.

#### OBS-T3 — Structured log carries correlation identifiers

- **Steps:** inspect the logs of a sample request.
- **Acceptance:** every log line is JSON and carries `request_id` and `trace_id`; no line is free text.

#### OBS-T4 — PII redaction before emission

- **Steps:** pass a string containing a phone, an email, a key, and an IBAN through `RedactionFilter`.
- **Acceptance:** all sensitive patterns are replaced with `REDACTED_*` tags; `is_safe_for_external_log` returns false before redaction and true after.

#### OBS-T5 — Sentry event scrubbing

- **Steps:** capture an error on a sensitive path (`/api/v1/checkout`, `/api/v1/webhooks/`).
- **Acceptance:** auth headers, query string, and request body are replaced with `<redacted>`; events from `tests/` paths are dropped entirely.

#### OBS-T6 — Cost and token recording per model call

- **Steps:** record a model call via `CostTracker.record`.
- **Acceptance:** the entry carries provider, model, input/output/cached tokens, estimated cost, and latency; `cost_usd` is computed via `estimate_cost_usd`.

#### OBS-T7 — Conservative cost estimate for an unknown model

- **Steps:** estimate the cost of a model not present in `MODEL_PRICES`.
- **Acceptance:** a conservative high model rate is used; spend is never under-estimated.

#### OBS-T8 — Cost summary per agent and workflow

- **Steps:** call `/api/v1/agent-observability/cost-summary`.
- **Acceptance:** it returns a breakdown per agent and per workflow; the `is_estimate` field is true.

#### OBS-T9 — Alert fires on failure

- **Steps:** simulate a webhook 5xx failure and a signature mismatch.
- **Acceptance:** an alert rule in `sentry_alerts.yaml` matches; the signature-mismatch alert is not deduplicated (`frequency_min: 0`).

#### OBS-T10 — Safe fallback when observability is unconfigured

- **Steps:** run the system without `OTEL_EXPORTER_OTLP_ENDPOINT` and without Langfuse keys.
- **Acceptance:** functions fall back to a safe no-op mode; no exception is raised; no service interruption.

#### OBS-T11 — A dashboard per service

- **Steps:** inspect the definitions under `observability/dashboards/`.
- **Acceptance:** dashboards exist for agents, workflows, and revenue OS; each is valid JSON with panels carrying title, metric, query, and type.

#### OBS-T12 — Incident has an owner and a status

- **Steps:** create an incident log following the template in `observability/incident_logs/README.md`.
- **Acceptance:** the log carries an ID, severity, a single owner, a status, and a linked `trace_id`; it contains no PII.

### Overall acceptance criteria

- All cases OBS-T1 through OBS-T12 pass.
- Zero PII leaks in any log, span, or incident log.
- Every cost figure is labeled "estimated".
- All dashboard JSON files are valid and all alert YAML files are valid.
