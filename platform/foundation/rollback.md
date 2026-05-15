# العربية

## إجراء التراجع — الطبقة الأولى (الأساس)

Owner: قائد المنصة (Platform Lead)

### الغرض

يضمن هذا الإجراء أن أي إصدار أو هجرة مخطط أو تغيير بنية تحتية يمكن التراجع عنه إلى آخر حالة مستقرة معروفة خلال نافذة زمنية محدّدة، دون أثر على عزل المستأجرين أو سلامة بياناتهم.

### نطاق التراجع

- تراجع إصدار التطبيق (كود FastAPI ضمن `api/`).
- تراجع هجرة مخطط قاعدة البيانات (`alembic/`، `db/migrations/versions/`، `supabase/migrations/`).
- تراجع تغيير إعدادات بيئة (متغيرات البيئة، الأسرار).

### المؤشرات التي تستدعي التراجع

- فشل فحص الصحة بعد النشر عبر `.github/workflows/scheduled_healthcheck.yml`.
- ارتفاع معدل الأخطاء المُلتقَطة في `dealix/observability/sentry.py` فوق العتبة.
- اكتشاف تسرّب بيانات بين المستأجرين (الخطر F-R1).
- فشل كتابة قيود التدقيق عبر `dealix/trust/audit.py`.

### إجراء التراجع — خطوة بخطوة

1. تجميد النشر: إيقاف أي خط نشر جارٍ وإعلان حالة "تراجع قيد التنفيذ".
2. تحديد آخر إصدار مستقر معروف من سجل الإصدارات (`.github/workflows/release.yml`).
3. تراجع الكود: تشغيل `.github/workflows/railway_deploy.yml` مثبَّتًا على الإصدار السابق.
4. تراجع المخطط عند اللزوم: `alembic downgrade <revision>` إلى المراجعة المستهدفة؛ على Supabase تطبيق هجرة التراجع المقابلة.
5. التحقق: تشغيل فحص الصحة، التأكد من تقييد كل استعلام بـ `tenant_id`، التأكد من استمرار كتابة قيود التدقيق.
6. تأكيد عزل المستأجرين: عيّنة تحقّق من مستأجرَين على الأقل دون تداخل بيانات.
7. التسجيل: كتابة التراجع كقيد تدقيق غير قابل للتعديل عبر `dealix/trust/audit.py` وإبلاغ قائد المنصة.

### معايير ما بعد التراجع

- فحص الصحة أخضر خلال 15 دقيقة من اكتمال التراجع.
- لا فقدان بيانات لأي مستأجر (RPO أقصاه 24 ساعة).
- قيد تدقيق واحد على الأقل يوثّق التراجع وسببه.

### القيود غير القابلة للتفاوض

- لا تراجع يحذف بيانات مستأجر دون موافقة بتصنيف A3.
- التراجع نفسه إجراء يُسجَّل؛ لا تراجع صامت.
- لا يُستخدم التراجع لتجاوز بوابة الموافقة `dealix/trust/approval.py`.

### الروابط ذات الصلة

- `platform/deployment/rollback_plan.md`
- `platform/deployment/ci_cd.md`
- `platform/foundation/risk_model.md`

# English

## Rollback Procedure — Layer 1 (Foundation)

Owner: Platform Lead

### Purpose

This procedure guarantees that any release, schema migration, or infrastructure change can be reverted to the last known-good stable state within a defined time window, with no impact on tenant isolation or data integrity.

### Rollback scope

- Application release rollback (FastAPI code under `api/`).
- Database schema migration rollback (`alembic/`, `db/migrations/versions/`, `supabase/migrations/`).
- Environment configuration rollback (environment variables, secrets).

### Triggers that warrant a rollback

- Post-deploy healthcheck failure via `.github/workflows/scheduled_healthcheck.yml`.
- Captured error rate in `dealix/observability/sentry.py` above threshold.
- Detection of cross-tenant data leakage (risk F-R1).
- Failure to write audit entries via `dealix/trust/audit.py`.

### Rollback procedure — step by step

1. Freeze deploys: halt any in-flight deploy pipeline and declare a "rollback in progress" state.
2. Identify the last known-good release from the release log (`.github/workflows/release.yml`).
3. Code rollback: run `.github/workflows/railway_deploy.yml` pinned to the prior release.
4. Schema rollback when needed: `alembic downgrade <revision>` to the target revision; on Supabase apply the matching down migration.
5. Verify: run the healthcheck, confirm every query is scoped to `tenant_id`, confirm audit entries continue to write.
6. Confirm tenant isolation: sample-check at least two tenants for no data overlap.
7. Record: write the rollback as an immutable audit entry via `dealix/trust/audit.py` and notify the Platform Lead.

### Post-rollback criteria

- Healthcheck green within 15 minutes of rollback completion.
- No data loss for any tenant (RPO at most 24 hours).
- At least one audit entry documents the rollback and its cause.

### Non-negotiables

- No rollback may delete tenant data without an A3-class approval.
- The rollback itself is a recorded action; no silent rollbacks.
- Rollback is never used to bypass the `dealix/trust/approval.py` approval gate.

### Related docs

- `platform/deployment/rollback_plan.md`
- `platform/deployment/ci_cd.md`
- `platform/foundation/risk_model.md`
