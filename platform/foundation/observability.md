# العربية

## المراقبة — الطبقة الأولى (الأساس)

Owner: قائد المنصة (Platform Lead)

### الغرض

يصف هذا المستند ما يُسجَّل ويُتتبَّع ويُنبَّه عليه في طبقة الأساس، حتى يكون لكل مستأجر وكل إجراء أثر يمكن استرجاعه وتدقيقه.

### ما يُسجَّل (Logs)

- كل طلب API: المسار، الدور، `tenant_id`، `user_id`، رمز الحالة، زمن الاستجابة.
- كل إجراء حساس: التصنيف (A/R/S)، حالة الموافقة، النتيجة.
- أحداث المصادقة: تسجيل دخول، فشل دخول، تدوير رمز، إبطال جلسة.
- لا تُسجَّل الأسرار ولا المعرّفات الشخصية (قاعدة `no_pii_in_logs`).

### ما يُتتبَّع (Traces)

- تتبّع موزَّع لكل طلب عبر `dealix/observability/otel.py`.
- مدّة كل خطوة في تدفق الطلب، بما فيها استعلامات قاعدة البيانات.
- تتبّع التكلفة لكل مستأجر عبر `dealix/observability/cost_tracker.py` (أساس الفوترة).

### ما يُلتقَط من أخطاء

- استثناءات وقت التشغيل عبر `dealix/observability/sentry.py`.
- ربط كل خطأ بـ `tenant_id` ومعرّف الطلب دون كشف بيانات شخصية.

### قيود التدقيق

- كل إجراء حساس يولّد قيد تدقيق غير قابل للتعديل عبر `dealix/trust/audit.py`.
- القيد يحوي: من، ماذا، متى، أي مستأجر، حالة الموافقة، النتيجة.

### التنبيهات

| التنبيه | المصدر | الإجراء |
|---|---|---|
| فشل لقطة يومية | `.github/workflows/daily_snapshot.yml` | إخطار قائد المنصة، تشغيل لقطة يدوية |
| فشل فحص الصحة | `.github/workflows/scheduled_healthcheck.yml` | تقييم التراجع |
| ارتفاع معدل الأخطاء | `dealix/observability/sentry.py` | فرز فوري |
| فجوة في تغطية قيود التدقيق | فحص `dealix/trust/audit.py` | تحقيق، حجب الإصدار |
| انحراف عن الأساس | `.github/workflows/watchdog_drift.yml` | مراجعة |

### المقاييس المرصودة

- زمن الاستجابة (p50/p95) لكل موجّه.
- معدل الأخطاء لكل مستأجر.
- نسبة تغطية قيود التدقيق للإجراءات الحساسة.
- نجاح/فشل اللقطة اليومية.

### الروابط ذات الصلة

- `platform/foundation/readiness.md`
- `platform/security/incident_response.md`
- `docs/SECURITY_RUNBOOK.md`

# English

## Observability — Layer 1 (Foundation)

Owner: Platform Lead

### Purpose

This document describes what is logged, traced, and alerted in the Foundation layer, so that every tenant and every action has a retrievable, auditable trail.

### What is logged

- Every API request: path, role, `tenant_id`, `user_id`, status code, response time.
- Every sensitive action: classification (A/R/S), approval state, outcome.
- Authentication events: login, failed login, token rotation, session revocation.
- Secrets and personal identifiers are never logged (`no_pii_in_logs` rule).

### What is traced

- Distributed tracing per request via `dealix/observability/otel.py`.
- Duration of each step in the request flow, including database queries.
- Per-tenant cost tracing via `dealix/observability/cost_tracker.py` (billing base).

### Error capture

- Runtime exceptions via `dealix/observability/sentry.py`.
- Each error is linked to a `tenant_id` and request ID without exposing personal data.

### Audit entries

- Every sensitive action emits an immutable audit entry via `dealix/trust/audit.py`.
- The entry holds: who, what, when, which tenant, approval state, outcome.

### Alerts

| Alert | Source | Action |
|---|---|---|
| Daily snapshot failure | `.github/workflows/daily_snapshot.yml` | Notify Platform Lead, run manual snapshot |
| Healthcheck failure | `.github/workflows/scheduled_healthcheck.yml` | Evaluate rollback |
| Error rate spike | `dealix/observability/sentry.py` | Immediate triage |
| Audit coverage gap | `dealix/trust/audit.py` check | Investigate, block release |
| Drift from baseline | `.github/workflows/watchdog_drift.yml` | Review |

### Monitored metrics

- Response time (p50/p95) per router.
- Error rate per tenant.
- Audit coverage ratio for sensitive actions.
- Daily snapshot success/failure.

### Related docs

- `platform/foundation/readiness.md`
- `platform/security/incident_response.md`
- `docs/SECURITY_RUNBOOK.md`
