# العربية

## السجلّات المنظَّمة — الطبقة السابعة

Owner: مهندس الموثوقية (Reliability Engineer)

### الغرض

كل سطر سجلّ يجب أن يكون منظَّماً وقابلاً للربط بطلب واحد، ونظيفاً من البيانات الشخصية. هذا المستند يحدّد كيف تُكتب السجلّات في Dealix وما الذي يُسمح ويُمنع داخلها.

### مبادئ التسجيل

- **سجلّ منظَّم:** كل حدث يحمل `request_id` و`trace_id` و`span_id` ووسم البيئة، ليُربط بطلب واحد عبر الطبقات.
- **حدث منظَّم موحَّد:** `ObservabilityEvent` في `auto_client_acquisition/observability_adapters/base.py` هو الشكل القياسي للأحداث: نوع الحدث، معرّف العميل (ليس بيانات شخصية)، النموذج، الرموز، زمن الاستجابة، النجاح، وسم الخطأ الآمن.
- **التنقية أولاً:** كل سلسلة وقاموس يمر على `RedactionFilter` في `auto_client_acquisition/observability_adapters/redaction.py` قبل أي بثّ خارجي.
- **مستويات السجلّ:** debug للتفاصيل المحلية، info للأحداث العادية، warning للتدهور، error للفشل الذي يحتاج تدخّلاً.

### ما يُمنع في السجلّات

- أرقام الهواتف والبريد الإلكتروني وأرقام الهوية والسجل التجاري والآيبان — تُستبدل بوسوم `REDACTED_*`.
- المفاتيح والرموز والأسرار ورؤوس المصادقة — تُستبدل بـ `REDACTED`.
- النصوص الكاملة للمحادثات لا تُسجَّل افتراضياً (بوابة `no_full_transcripts_by_default`).
- آثار المكدّس الخام لا تُرسَل خارجياً؛ يُرسَل وسم خطأ آمن فقط.

### نقاط التكامل في الكود

- توليد `request_id` عند الحافة: `api/middleware.py` (رأس `X-Request-ID`).
- كتابة الأحداث المنظَّمة عبر المحوّلات: `auto_client_acquisition/observability_adapters/`.
- تنقية أحداث Sentry قبل الإرسال: دالة `_scrub_event` في `dealix/observability/sentry.py`.
- تسجيل استدعاءات النماذج: `dealix/observability/cost_tracker.py` يسجّل المزوّد والنموذج والرموز والحالة.

### المقاييس

- نسبة أسطر السجلّ الحاملة لـ `trace_id`: هدف 100% لمسارات الوكلاء والأدوات.
- نسبة الأحداث التي مرّت على التنقية قبل البثّ: 100%.
- معدّل أخطاء التنقية (سلسلة غير آمنة عبرت): هدف صفر.
- زمن البحث عن طلب واحد بمعرّفه: أقل من دقيقة واحدة.

### خطاطيف المراقبة

- كل محوّل يكشف `is_configured` لمعرفة ما إذا كان البثّ مفعّلاً.
- `RedactionFilter.is_safe_for_external_log` يُستخدم كفحص بوابة قبل البثّ.
- فشل الاستمرارية في `cost_tracker` يُسجَّل كـ warning ولا يُسقط الطلب.

### قواعد الحوكمة

- لا يُكتب أي حقل بيانات شخصية في السجلّات (قاعدة `no_pii_in_logs`).
- النصوص الكاملة للمحادثات تتطلب موافقة موثَّقة وعلَماً صريحاً.
- تغيير أنماط التنقية في `redaction.py` يتطلب مراجعة من مهندس الموثوقية.
- لا يعتمد التسجيل على مزوّد خارجي إلزامي؛ الوضع الافتراضي لا-عملية آمن.

### إجراء التراجع

1. إذا سرّب إصدار بيانات شخصية في السجلّات، أوقف البثّ الخارجي بإلغاء ضبط مُصدِّر OTLP فوراً.
2. ارجع المحوّلات إلى وضع لا-عملية عبر إعداد المحوّل `noop` في `base.py`.
3. أعد نشر الإصدار المستقر السابق وتحقّق من توقّف التسريب.
4. سجّل الحادث في `observability_v6` مع المالك والحالة.

### درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل.**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Structured Logging — Layer 7

Owner: Reliability Engineer

### Purpose

Every log line must be structured, correlatable to a single request, and free of PII. This document defines how logs are written in Dealix and what is allowed and forbidden inside them.

### Logging principles

- **Structured logs:** every event carries `request_id`, `trace_id`, `span_id`, and an environment tag so it can be tied to a single request across layers.
- **One unified structured event:** `ObservabilityEvent` in `auto_client_acquisition/observability_adapters/base.py` is the standard event shape: event type, customer handle (not PII), model, tokens, latency, success, and a safe error label.
- **Redaction first:** every string and dict passes through `RedactionFilter` in `auto_client_acquisition/observability_adapters/redaction.py` before any external emission.
- **Log levels:** debug for local detail, info for normal events, warning for degradation, error for failure needing intervention.

### Forbidden in logs

- Phone numbers, emails, national IDs, CR numbers, and IBANs — replaced with `REDACTED_*` tags.
- Keys, tokens, secrets, and auth headers — replaced with `REDACTED`.
- Full conversation transcripts are not logged by default (`no_full_transcripts_by_default` gate).
- Raw stacktraces are not sent externally; only a safe error label is sent.

### Code integration points

- `request_id` generation at the edge: `api/middleware.py` (`X-Request-ID` header).
- Structured event writing via adapters: `auto_client_acquisition/observability_adapters/`.
- Sentry event scrubbing before send: `_scrub_event` in `dealix/observability/sentry.py`.
- LLM call logging: `dealix/observability/cost_tracker.py` records provider, model, tokens, and status.

### Metrics

- Share of log lines carrying `trace_id`: target 100% for agent and tool paths.
- Share of events passed through redaction before emission: 100%.
- Redaction miss rate (unsafe string passed through): target zero.
- Time to find a single request by its identifier: under one minute.

### Observability hooks

- Each adapter exposes `is_configured` to tell whether emission is enabled.
- `RedactionFilter.is_safe_for_external_log` is used as a gate check before emission.
- Persistence failure in `cost_tracker` is logged as a warning and never drops the request.

### Governance rules

- No PII field is ever written to logs (`no_pii_in_logs` rule).
- Full conversation transcripts require a documented approval and an explicit flag.
- Changing redaction patterns in `redaction.py` requires Reliability Engineer review.
- Logging does not depend on a mandatory external provider; the default is a safe no-op mode.

### Rollback procedure

1. If a release leaks PII into logs, stop external emission by unsetting the OTLP exporter immediately.
2. Return adapters to no-op mode via the `noop` adapter selection in `base.py`.
3. Redeploy the previous stable release and verify the leak has stopped.
4. File the incident in `observability_v6` with an owner and status.

### Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
