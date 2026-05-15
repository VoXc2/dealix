# العربية

## جاهزية المراقبة — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

تجمع هذه الوثيقة جاهزية الطبقة السابعة كاملة: السجلات، المقاييس، الآثار، التنبيهات، اللوحات، وسجل الحوادث. الهدف العملي: معرفة ما يجري داخل كل وكيل وسير عمل وواجهة برمجية وأداة في الوقت الحقيقي.

### قائمة الجاهزية

- [x] كل طلب يمكن تتبّعه من طرف لطرف عبر `trace_id` واحد.
- [x] كل سير عمل يحمل `trace_id`؛ كل نداء أداة ملفوف بامتداد.
- [x] يُعرف أيُّ وكيل فشل ولماذا عبر `agent_span` ووسم `error_type` الآمن.
- [x] استهلاك الرموز والتكلفة التقديرية واضحان لكل نداء نموذج عبر `cost_tracker.py`.
- [x] الزمن لكل خطوة واضح عبر `latency_ms` والامتدادات.
- [x] التنبيهات تُطلق عند الفشل عبر `sentry_alerts.yaml` و `observability/alerts/`.
- [x] لوحة لكل خدمة: الوكلاء، أسيرة العمل، نظام الإيراد.
- [x] عملية حوادث بمسؤول وحالة موثَّقة في `observability/incident_logs/`.
- [x] تنقية PII والأسرار قبل أي بثّ خارجي عبر `RedactionFilter`.
- [ ] تمرين موثَّق لتتبّع طلب فاشل من الواجهة حتى الأداة.
- [ ] دمج صفحة المناوب (on-call) مُختبَر وموثَّق.
- [ ] أهداف SLO مُعتمَدة بالبيانات الفعلية.

### المقاييس

- نسبة أسيرة العمل الحاملة لـ `trace_id`: 100% (هدف).
- نسبة نداءات النماذج التي تحمل تكلفة تقديرية: 100%.
- زمن من الفشل إلى إطلاق التنبيه: أقل من 5 دقائق.
- نسبة الخدمات الحرجة التي لها لوحة: 100% (هدف).
- نسبة الحوادث الموثَّقة بسجل: 100%.
- زمن الإقرار بحادث SEV-1: أقل من 15 دقيقة.
- نسبة الخطوات الحاملة لـ `latency_ms`: 100% (هدف).

### خطاطيف المراقبة

- إعداد التتبّع وامتدادات OTel عبر `dealix/observability/otel.py`.
- تتبّع التكلفة والرموز عبر `dealix/observability/cost_tracker.py`.
- التقاط الأخطاء وتنقية PII عبر `dealix/observability/sentry.py`.
- محوّلات الوكلاء عبر `auto_client_acquisition/observability_adapters/`.
- واجهات المراقبة عبر `api/routers/agent_observability.py` و `observability_v6.py` و `observability_v10.py`.
- قواعد التنبيه عبر `docs/observability/sentry_alerts.yaml` و `observability/alerts/`.
- سجلات الحوادث تحت `observability/incident_logs/`.

### قواعد الحوكمة

- لا تُكتب PII (هاتف، بريد، هوية وطنية، سجل تجاري، IBAN) في أي سجل أو امتداد أو سجل حادث.
- لا تُرسَل آثار تتبّع خام خارجيًا؛ يُرسَل وسم خطأ آمن فقط.
- لا تُرسَل نصوص محادثات كاملة افتراضيًا (بوابة `no_full_transcripts_by_default`).
- كل رقم تكلفة موسوم "تقديري" لا مؤكَّد.
- تنبيهات انتهاك السياسة دائمًا SEV-1 ولا تُكتم.
- تعديل قواعد التنبيه أو أهداف SLO يتطلب موافقة موثَّقة من المالك.
- التصدير الخارجي يُفعَّل في staging أولاً ثم production.

### إجراء التراجع

1. عند الاشتباه بتسريب PII: ألغِ ضبط `OTEL_EXPORTER_OTLP_ENDPOINT` لإيقاف البثّ الخارجي فورًا.
2. أعد المحوّلات إلى وضع `noop` الآمن عبر `base.py` — الخدمة لا تنقطع.
3. استرجع الإصدار المستقر السابق لأي خدمة مراقبة معطوبة.
4. عند فقدان تغطية تنبيه، استرجع نسخة `sentry_alerts.yaml` السابقة وتحقّق من تنبيهات SEV-1.
5. سجّل الحادث في `observability/incident_logs/` مع المالك والحالة، وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 75 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

الأسس قائمة: تتبّع من طرف لطرف، تتبّع تكلفة، التقاط أخطاء، تنقية PII، تنبيهات، لوحات، عملية حوادث. الفجوات المتبقية تمرينية وتشغيلية: تمارين تحقّق موثَّقة، دمج صفحة المناوب، واعتماد أهداف SLO بالبيانات الفعلية.

# English

## Observability Readiness — Layer 7

Owner: Platform Reliability Lead

### Purpose

This document aggregates the full readiness of Layer 7: logs, metrics, traces, alerts, dashboards, and the incident log. The practical goal: knowing what happens inside every agent, workflow, API, and tool in real time.

### Readiness checklist

- [x] Every request is traceable end to end via a single `trace_id`.
- [x] Every workflow carries a `trace_id`; every tool call is wrapped in a span.
- [x] Which agent failed and why is known via `agent_span` and the safe `error_type` label.
- [x] Token usage and estimated cost are clear per model call via `cost_tracker.py`.
- [x] Latency per step is clear via `latency_ms` and spans.
- [x] Alerts fire on failure via `sentry_alerts.yaml` and `observability/alerts/`.
- [x] A dashboard per service: agents, workflows, revenue OS.
- [x] An incident process with owner and status documented in `observability/incident_logs/`.
- [x] PII and secrets scrubbed before any external emission via `RedactionFilter`.
- [ ] Documented drill for tracing a failed request from API to tool.
- [ ] On-call paging integration tested and documented.
- [ ] SLO targets approved against real data.

### Metrics

- Workflows carrying a `trace_id`: 100% (target).
- Model calls carrying an estimated cost: 100%.
- Time from failure to alert firing: under 5 minutes.
- Critical services with a dashboard: 100% (target).
- Incidents documented with a log: 100%.
- SEV-1 acknowledgement time: under 15 minutes.
- Steps carrying `latency_ms`: 100% (target).

### Observability hooks

- Tracing setup and OTel spans via `dealix/observability/otel.py`.
- Cost and token tracking via `dealix/observability/cost_tracker.py`.
- Error capture and PII scrubbing via `dealix/observability/sentry.py`.
- Agent adapters via `auto_client_acquisition/observability_adapters/`.
- Observability APIs via `api/routers/agent_observability.py`, `observability_v6.py`, and `observability_v10.py`.
- Alert rules via `docs/observability/sentry_alerts.yaml` and `observability/alerts/`.
- Incident logs under `observability/incident_logs/`.

### Governance rules

- No PII (phone, email, national ID, commercial registration, IBAN) is written to any log, span, or incident log.
- No raw stack traces are emitted externally; only a safe error label is sent.
- Full conversation transcripts are not emitted by default (`no_full_transcripts_by_default` gate).
- Every cost figure is labeled "estimated", not verified.
- Policy-violation alerts are always SEV-1 and are never muted.
- Changing alert rules or SLO targets requires a documented approval from the owner.
- External export is enabled in staging first, then production.

### Rollback procedure

1. On suspected PII leak: unset `OTEL_EXPORTER_OTLP_ENDPOINT` to stop external emission immediately.
2. Return adapters to the safe `noop` mode via `base.py` — the service does not go down.
3. Revert to the previous stable release of any broken observability service.
4. On lost alert coverage, revert to the previous `sentry_alerts.yaml` version and verify SEV-1 alerts.
5. File the incident in `observability/incident_logs/` with an owner and status, and notify the Platform Reliability Lead.

### Current readiness score

**Score: 75 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

The foundations are in place: end-to-end tracing, cost tracking, error capture, PII scrubbing, alerts, dashboards, and an incident process. The remaining gaps are drill and operational: documented verification drills, on-call paging integration, and SLO target approval against real data.
