# العربية

## جاهزية الأساس — الطبقة الأولى

Owner: قائد المنصة (Platform Lead)

### قائمة الجاهزية

- [x] كل جدول وملف وذاكرة ومحادثة مرتبط بعمود `tenant_id`.
- [x] إنشاء مستأجر جديد عبر `POST /api/v1/auth/register` خلال دقائق.
- [x] المصادقة برموز JWT وإدارة جلسات عبر جدول `refresh_tokens`.
- [x] التحكم بالأدوار عبر `api/security/rbac.py`.
- [x] الأسرار خارج الكود في متغيرات البيئة لكل بيئة.
- [x] التكامل المستمر يحجب الدمج عند فشل الفحوص (`.github/workflows/ci.yml`).
- [x] لقطات يومية عبر `.github/workflows/daily_snapshot.yml`.
- [x] كل إجراء يولّد قيد تدقيق غير قابل للتعديل.
- [ ] حذف مستأجر كامل مؤكَّد بدون أثر على المستأجرين الآخرين (إجراء قائم، يحتاج تمرين دوري موثَّق).
- [ ] تمرين استرجاع نسخة احتياطية كامل موثَّق ربع سنويًا.

### المقاييس

- زمن إنشاء المستأجر: أقل من 5 دقائق (هدف).
- نسبة الجداول الحاملة لـ `tenant_id`: 100%.
- زمن استرجاع النسخة الاحتياطية: أقل من 60 دقيقة.
- تغطية قيود التدقيق: 100% من الإجراءات الحساسة (S2/S3).
- زمن التراجع عن إصدار: أقل من 15 دقيقة.
- نقطة الاسترجاع المستهدفة (RPO): 24 ساعة. هدف زمن الاسترجاع (RTO): 60 دقيقة.

### خطاطيف المراقبة

- تتبّع كل طلب عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تتبّع التكلفة عبر `dealix/observability/cost_tracker.py`.
- قيود التدقيق المكتوبة عبر `dealix/trust/audit.py`.
- تنبيه عند فشل لقطة يومية أو فحص صحة (`scheduled_healthcheck.yml`).

### قواعد الحوكمة

- إنشاء أو حذف مستأجر إجراء بتصنيف A2 على الأقل ويتطلب موافقة موثَّقة.
- تصدير بيانات حساسة (S3) يتطلب موافقة A3 وفق `dealix/classifications/__init__.py`.
- لا تنفيذ آلي لإجراءات R3؛ تمر عبر مسار الموافقة في `dealix/trust/approval.py`.
- الأسرار لا تُكتب في السجلات (قاعدة `no_pii_in_logs`).
- النشر للإنتاج يتطلب نجاح التكامل المستمر.

### إجراء التراجع

1. تحديد الإصدار المستقر السابق من سجل الإصدارات.
2. تشغيل التراجع عبر `.github/workflows/railway_deploy.yml` على الإصدار السابق.
3. عند تغيّر المخطط: تطبيق `alembic downgrade` للمراجعة المستهدفة.
4. التحقق من فحص الصحة وقيود التدقيق بعد التراجع.
5. تسجيل التراجع كقيد تدقيق وإبلاغ قائد المنصة.

### درجة الجاهزية الحالية

**الدرجة: 78 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Foundation Readiness — Layer 1

Owner: Platform Lead

### Readiness checklist

- [x] Every table, file, memory, and conversation is bound to a `tenant_id` column.
- [x] A new tenant is created via `POST /api/v1/auth/register` within minutes.
- [x] Authentication uses JWT and session management via the `refresh_tokens` table.
- [x] RBAC enforced via `api/security/rbac.py`.
- [x] Secrets kept out of code in per-environment variables.
- [x] Continuous integration blocks merge on failed checks (`.github/workflows/ci.yml`).
- [x] Daily snapshots via `.github/workflows/daily_snapshot.yml`.
- [x] Every action emits an immutable audit entry.
- [ ] Full tenant deletion verified with no impact on other tenants (procedure exists, needs a documented periodic drill).
- [ ] Full backup restore drill documented quarterly.

### Metrics

- Tenant creation time: under 5 minutes (target).
- Tables carrying `tenant_id`: 100%.
- Backup restore time: under 60 minutes.
- Audit entry coverage: 100% of sensitive (S2/S3) actions.
- Release rollback time: under 15 minutes.
- Recovery Point Objective (RPO): 24 hours. Recovery Time Objective (RTO): 60 minutes.

### Observability hooks

- Every request traced via `dealix/observability/otel.py`.
- Error capture via `dealix/observability/sentry.py`.
- Cost tracking via `dealix/observability/cost_tracker.py`.
- Audit entries written via `dealix/trust/audit.py`.
- Alert on failed daily snapshot or healthcheck (`scheduled_healthcheck.yml`).

### Governance rules

- Tenant creation or deletion is an A2-class action at minimum and requires a documented approval.
- Sensitive data export (S3) requires A3 approval per `dealix/classifications/__init__.py`.
- No auto-execution of R3 actions; they pass through the approval path in `dealix/trust/approval.py`.
- Secrets are never written to logs (`no_pii_in_logs` rule).
- Production deploy requires passing CI.

### Rollback procedure

1. Identify the previous stable release from the release log.
2. Trigger rollback via `.github/workflows/railway_deploy.yml` on the prior release.
3. On schema change: apply `alembic downgrade` to the target revision.
4. Verify healthcheck and audit entries after rollback.
5. Record the rollback as an audit entry and notify the Platform Lead.

### Current readiness score

**Score: 78 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
