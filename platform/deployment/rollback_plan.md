# العربية

## خطة التراجع — الطبقة الأولى (النشر)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه الخطة كيف تتراجع Dealix عن إصدار إنتاج فاشل أو ضار إلى آخر حالة مستقرة معروفة خلال نافذة زمنية محدّدة.

### نطاق الخطة

- تراجع كود التطبيق (`api/`).
- تراجع هجرة المخطط (`alembic/`، `db/migrations/versions/`، `supabase/migrations/`).
- تراجع إعدادات البيئة والأسرار.

### المؤشرات التي تستدعي التراجع

- فشل فحص الصحة بعد النشر (`.github/workflows/scheduled_healthcheck.yml`).
- ارتفاع معدل الأخطاء في `dealix/observability/sentry.py`.
- اكتشاف تسرّب بيانات بين المستأجرين.
- فشل كتابة قيود التدقيق.

### خطوات التراجع

1. تجميد النشر وإعلان "تراجع قيد التنفيذ".
2. تحديد آخر إصدار مستقر من سجل `.github/workflows/release.yml`.
3. تشغيل `.github/workflows/railway_deploy.yml` مثبَّتًا على الإصدار السابق.
4. عند تغيّر المخطط: `alembic downgrade <revision>` أو هجرة Supabase العكسية.
5. التحقق: فحص الصحة، تقييد `tenant_id`، استمرار قيود التدقيق.
6. تأكيد عزل المستأجرين لمستأجرَين على الأقل.
7. تسجيل التراجع كقيد تدقيق عبر `dealix/trust/audit.py` وإبلاغ قائد المنصة.

### معايير ما بعد التراجع

- فحص الصحة أخضر خلال 15 دقيقة.
- لا فقدان بيانات لأي مستأجر (RPO أقصاه 24 ساعة).
- قيد تدقيق يوثّق التراجع وسببه.

### قواعد الحوكمة

- لا تراجع يحذف بيانات مستأجر دون موافقة A3.
- التراجع نفسه إجراء مُسجَّل؛ لا تراجع صامت.
- لا يُستخدم التراجع لتجاوز بوابة الموافقة `dealix/trust/approval.py`.

### المقاييس

- زمن التراجع: أقل من 15 دقيقة.
- نسبة عمليات التراجع المنجزة ضمن النافذة الزمنية.
- عدد عمليات التراجع وكلها مُسجَّلة.

### المراقبة

- تنبيه على بدء أي تراجع.
- قيد تدقيق لكل خطوة تراجع.

### الروابط ذات الصلة

- `platform/foundation/rollback.md`
- `platform/deployment/ci_cd.md`
- `platform/deployment/backup_restore.md`

# English

## Rollback Plan — Layer 1 (Deployment)

Owner: Platform Lead

### Purpose

This plan defines how Dealix rolls back a failed or harmful production release to the last known-good stable state within a defined time window.

### Plan scope

- Application code rollback (`api/`).
- Schema migration rollback (`alembic/`, `db/migrations/versions/`, `supabase/migrations/`).
- Environment configuration and secrets rollback.

### Triggers that warrant a rollback

- Post-deploy healthcheck failure (`.github/workflows/scheduled_healthcheck.yml`).
- Error rate spike in `dealix/observability/sentry.py`.
- Detection of cross-tenant data leakage.
- Failure to write audit entries.

### Rollback steps

1. Freeze deploys and declare "rollback in progress".
2. Identify the last stable release from the `.github/workflows/release.yml` log.
3. Run `.github/workflows/railway_deploy.yml` pinned to the prior release.
4. On a schema change: `alembic downgrade <revision>` or the inverse Supabase migration.
5. Verify: healthcheck, `tenant_id` scoping, continued audit entries.
6. Confirm tenant isolation for at least two tenants.
7. Record the rollback as an audit entry via `dealix/trust/audit.py` and notify the Platform Lead.

### Post-rollback criteria

- Healthcheck green within 15 minutes.
- No data loss for any tenant (RPO at most 24 hours).
- An audit entry documents the rollback and its cause.

### Governance rules

- No rollback deletes tenant data without an A3 approval.
- The rollback itself is a recorded action; no silent rollbacks.
- Rollback is never used to bypass the `dealix/trust/approval.py` approval gate.

### Metrics

- Rollback time: under 15 minutes.
- Ratio of rollbacks completed within the time window.
- Count of rollbacks, all recorded.

### Observability

- Alert on the start of any rollback.
- An audit entry for every rollback step.

### Related docs

- `platform/foundation/rollback.md`
- `platform/deployment/ci_cd.md`
- `platform/deployment/backup_restore.md`
