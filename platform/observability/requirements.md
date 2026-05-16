# Observability Requirements — Agentic Revenue OS

## الهدف

توفير رؤية تشغيلية كاملة لكل تشغيل workflow بحيث يمكن:

- المتابعة اللحظية
- التحقيق بعد الحوادث
- إعادة التشغيل (replay)
- إثبات الامتثال والنتائج

## الحد الأدنى الإلزامي

### 1) Traces

- trace لكل workflow run.
- span لكل خطوة رئيسية: qualification, retrieval, scoring, approval, crm update.
- `trace_id` يجب أن يظهر في logs وaudit وeval report.

### 2) Metrics

- workflow success/failure rate
- step latency (p50/p95)
- approval turnaround time
- retry count
- policy denial rate
- business KPI deltas (conversion / response time)

### 3) Logs

- structured JSON logs.
- حقول إلزامية: `tenant_id`, `workflow_id`, `run_id`, `trace_id`, `actor_id`.
- يمنع تسجيل بيانات حساسة كاملة (PII redaction).

### 4) Alerts

- فشل متكرر في خطوة واحدة.
- ارتفاع policy denials بشكل غير طبيعي.
- missing audit record بعد تنفيذ action.
- retry exhaustion.

## متطلبات إعادة التشغيل (Replayability)

- حفظ input payload المرجعي لكل run (مع redaction مناسب).
- حفظ workflow version + agent version.
- قدرة إعادة التشغيل في وضع dry-run للتحقيق.

## لوحات المتابعة التنفيذية

- Lead throughput
- Qualification accuracy
- Approval bottlenecks
- CRM sync reliability
- ROI trend (weekly/monthly)
