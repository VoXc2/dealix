# العربية

## التكامل والنشر المستمران — الطبقة الأولى (النشر)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة خط التكامل والنشر المستمرين في Dealix: كيف يُفحص كل تغيير ويُنشر بأمان عبر البيئات الثلاث.

### خط التكامل المستمر

- يعمل عبر `.github/workflows/ci.yml` على كل طلب دمج.
- يشمل: فحص الكود، الاختبارات، فحص الأمن `.github/workflows/codeql.yml`.
- يحجب الدمج عند فشل أي فحص.

### خط النشر

| المرحلة | سير العمل |
|---|---|
| بناء الحاوية | `.github/workflows/docker-build.yml` |
| النشر للتجهيز | `.github/workflows/deploy.yml` ثم اختبار دخان `.github/workflows/staging-smoke.yml` |
| النشر للإنتاج | `.github/workflows/railway_deploy.yml` |
| الإصدار | `.github/workflows/release.yml` و`.github/workflows/release-please.yml` |
| اختبارات الواجهة | `.github/workflows/playwright_smoke.yml` |

### هجرات قاعدة البيانات

- تُطبَّق الهجرات عبر `alembic/` و`db/migrations/versions/` و`supabase/migrations/`.
- كل هجرة لها مسار تراجع (`alembic downgrade`).
- لا تُطبَّق هجرة على الإنتاج دون اختبارها على التجهيز.

### قواعد الحوكمة

- لا دمج بدون نجاح التكامل المستمر.
- لا نشر للإنتاج بدون مرور بالتجهيز ونجاح اختبار الدخان.
- نشر الإنتاج وتطبيق هجرة إنتاج إجراء بتصنيف A2 على الأقل ويُسجَّل.
- كل إصدار له وسم واضح في سجل الإصدارات.

### المقاييس

- نسبة الدمج الذي مرّ بالتكامل المستمر: 100%.
- زمن خط النشر من الدمج إلى الإنتاج.
- معدل فشل النشر.
- زمن التراجع عن إصدار: أقل من 15 دقيقة.

### المراقبة

- فحص صحة بعد كل نشر عبر `.github/workflows/scheduled_healthcheck.yml`.
- قيد تدقيق لكل نشر وكل هجرة.
- تنبيه على فشل خط نشر أو فحص دخان.

### إجراء التراجع

1. تحديد آخر إصدار مستقر من سجل الإصدارات.
2. تشغيل `.github/workflows/railway_deploy.yml` مثبَّتًا على الإصدار السابق.
3. عند تغيّر المخطط: `alembic downgrade` للمراجعة المستهدفة.
4. التحقق من فحص الصحة وتسجيل التراجع كقيد تدقيق.

### درجة الجاهزية الحالية

تُقاس ضمن مجمل جاهزية النشر في `platform/deployment/readiness.md`.

### الروابط ذات الصلة

- `platform/deployment/environments.md`
- `platform/deployment/rollback_plan.md`
- `platform/foundation/rollback.md`

# English

## CI/CD — Layer 1 (Deployment)

Owner: Platform Lead

### Purpose

This document describes the Dealix continuous integration and deployment pipeline: how every change is checked and deployed safely across the three environments.

### Continuous integration pipeline

- Runs via `.github/workflows/ci.yml` on every merge request.
- Includes: code linting, tests, security scan `.github/workflows/codeql.yml`.
- Blocks merge on any failing check.

### Deployment pipeline

| Stage | Workflow |
|---|---|
| Container build | `.github/workflows/docker-build.yml` |
| Staging deploy | `.github/workflows/deploy.yml` then smoke test `.github/workflows/staging-smoke.yml` |
| Production deploy | `.github/workflows/railway_deploy.yml` |
| Release | `.github/workflows/release.yml` and `.github/workflows/release-please.yml` |
| UI tests | `.github/workflows/playwright_smoke.yml` |

### Database migrations

- Migrations are applied via `alembic/`, `db/migrations/versions/`, and `supabase/migrations/`.
- Every migration has a rollback path (`alembic downgrade`).
- No migration is applied to production without testing it on staging.

### Governance rules

- No merge without passing CI.
- No production deploy without passing through staging and a passing smoke test.
- A production deploy and a production migration are A2-class actions at minimum and are recorded.
- Every release has a clear tag in the release log.

### Metrics

- Ratio of merges that passed through CI: 100%.
- Pipeline time from merge to production.
- Deploy failure rate.
- Release rollback time: under 15 minutes.

### Observability

- A healthcheck after every deploy via `.github/workflows/scheduled_healthcheck.yml`.
- An audit entry for every deploy and every migration.
- Alert on a failed deploy pipeline or smoke test.

### Rollback procedure

1. Identify the last stable release from the release log.
2. Run `.github/workflows/railway_deploy.yml` pinned to the prior release.
3. On a schema change: `alembic downgrade` to the target revision.
4. Verify the healthcheck and record the rollback as an audit entry.

### Current readiness score

Measured within the overall deployment readiness in `platform/deployment/readiness.md`.

### Related docs

- `platform/deployment/environments.md`
- `platform/deployment/rollback_plan.md`
- `platform/foundation/rollback.md`
