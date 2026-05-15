# العربية

**Owner:** مهندس وقت تشغيل سير العمل (Workflow Runtime Engineer).

## الغرض

يحدّد هذا المستند كيف يصبح كل تشغيل سير عمل مرئياً بالكامل: السجلات، الأثر، المقاييس، والتنبيهات. القاعدة: لا خطوة تنفَّذ دون أثر قابل للتدقيق.

## سجلات سير العمل

كل تشغيل ينتج سجلاً منظَّماً يحتوي:

- معرّف التشغيل، اسم سير العمل، الإصدار المثبَّت، معرّف المستأجر.
- لكل خطوة: الاسم، الحالة (`completed` / `retrying` / `failed` / `skipped`)، الطابع الزمني للبدء والانتهاء، المالك.
- نتيجة كل محاولة إعادة وكل خطوة تعويض.
- قرار كل خطوة موافقة: مَن وافق ومتى.

## خطاطيف المراقبة

- تتبّع التشغيل عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تتبّع التكلفة لكل تشغيل عبر `dealix/observability/cost_tracker.py`.
- قيود التدقيق عبر `dealix/trust/audit.py`.
- أثر الوكلاء داخل الخطوات عبر `auto_client_acquisition/agent_observability/trace.py`.

## المقاييس

تُجمَّع مقاييس سير العمل عبر `auto_client_acquisition/workflow_os/workflow_metrics.py`:

- `completion_rate` — نسبة التشغيلات التي تصل المخرج النهائي.
- `cycle_time_hours` — زمن التشغيل من المحفّز إلى الإنهاء.
- `rework_count` — عدد الخطوات المعادة.
- `governance_block_rate` — نسبة التشغيلات المحجوبة عند الحوكمة.
- معدّل عمق DLQ لكل طابور.

## التنبيهات

- تنبيه عند انخفاض `completion_rate` تحت 95% في سيناريو عادي.
- تنبيه عند تجاوز عمق DLQ حدّاً معلناً.
- تنبيه عند تجاوز تشغيل لـ SLA المعلن في تعريفه.
- تنبيه عند فشل خطوة تعويض (`compensation_failed`).

## الحوكمة على المراقبة

- لا تُكتب بيانات تعريف شخصية (PII) في السجلات؛ تُنقَّح عبر `auto_client_acquisition/agent_observability/redaction.py`.
- كل قرار موافقة قيد تدقيق غير قابل للتعديل.
- سجلات سير العمل معزولة بـ `tenant_id`.

انظر أيضاً: `platform/workflow_engine/readiness.md`، `platform/workflow_engine/retries.md`.

---

# English

**Owner:** Workflow Runtime Engineer.

## Purpose

This document defines how every workflow run becomes fully visible: logs, traces, metrics, and alerts. The rule: no step executes without an auditable trace.

## Workflow logs

Every run produces a structured log containing:

- Run id, workflow name, pinned version, tenant id.
- Per step: name, state (`completed` / `retrying` / `failed` / `skipped`), start and end timestamp, owner.
- The outcome of each retry attempt and each compensation step.
- The decision of each approval step: who approved and when.

## Observability hooks

- Run tracing via `dealix/observability/otel.py`.
- Error capture via `dealix/observability/sentry.py`.
- Per-run cost tracking via `dealix/observability/cost_tracker.py`.
- Audit entries via `dealix/trust/audit.py`.
- In-step agent traces via `auto_client_acquisition/agent_observability/trace.py`.

## Metrics

Workflow metrics are aggregated via `auto_client_acquisition/workflow_os/workflow_metrics.py`:

- `completion_rate` — share of runs that reach the final output.
- `cycle_time_hours` — run time from trigger to finalization.
- `rework_count` — number of re-run steps.
- `governance_block_rate` — share of runs blocked at governance.
- DLQ depth rate per queue.

## Alerts

- Alert when `completion_rate` drops below 95% in a normal scenario.
- Alert when DLQ depth crosses a declared threshold.
- Alert when a run exceeds the SLA declared in its definition.
- Alert when a compensation step fails (`compensation_failed`).

## Governance on observability

- No personally identifiable information (PII) is written to logs; it is redacted via `auto_client_acquisition/agent_observability/redaction.py`.
- Every approval decision is an immutable audit entry.
- Workflow logs are partitioned by `tenant_id`.

See also: `platform/workflow_engine/readiness.md`, `platform/workflow_engine/retries.md`.
