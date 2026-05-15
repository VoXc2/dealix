# العربية

## جاهزية النشر — الطبقة الأولى

Owner: قائد المنصة (Platform Lead)

### قائمة الجاهزية

- [x] ثلاث بيئات منفصلة: تطوير، تجهيز، إنتاج، بأسرار منفصلة.
- [x] تكامل مستمر يحجب الدمج عند فشل الفحوص (`.github/workflows/ci.yml`).
- [x] فحص أمن للكود عبر `.github/workflows/codeql.yml`.
- [x] نشر آلي عبر `.github/workflows/railway_deploy.yml`.
- [x] اختبار دخان على التجهيز قبل الإنتاج (`.github/workflows/staging-smoke.yml`).
- [x] لقطات يومية آلية عبر `.github/workflows/daily_snapshot.yml`.
- [x] هجرات لها مسار تراجع عبر `alembic/` و`supabase/migrations/`.
- [x] فحص صحة مجدول عبر `.github/workflows/scheduled_healthcheck.yml`.
- [ ] تمرين استرجاع نسخة احتياطية موثَّق ربع سنويًا.
- [ ] تمرين تراجع إصدار موثَّق دوريًا يثبت زمن أقل من 15 دقيقة.

### المقاييس

- نسبة الدمج الذي مرّ بالتكامل المستمر: 100%.
- نسبة عمليات النشر للإنتاج التي مرّت بالتجهيز: 100%.
- زمن التراجع عن إصدار: أقل من 15 دقيقة (هدف).
- نقطة الاسترجاع المستهدفة RPO: 24 ساعة. زمن الاسترجاع المستهدف RTO: 60 دقيقة.
- نسبة نجاح اللقطة اليومية: هدف 100%.

### خطاطيف المراقبة

- فحص صحة بعد كل نشر عبر `.github/workflows/scheduled_healthcheck.yml`.
- التقاط أخطاء النشر عبر `dealix/observability/sentry.py`.
- قيد تدقيق لكل نشر وهجرة واسترجاع عبر `dealix/trust/audit.py`.
- تنبيه على فشل لقطة يومية أو خط نشر أو اختبار دخان.

### قواعد الحوكمة

- لا نشر للإنتاج دون مرور بالتجهيز ونجاح التكامل المستمر.
- نشر الإنتاج وتطبيق هجرة إنتاج واسترجاع بيانات إنتاج إجراء بتصنيف A2 على الأقل ويُسجَّل.
- لا تراجع يحذف بيانات مستأجر دون موافقة A3.
- لا تُستخدم بيانات مستأجر حقيقية خارج بيئة الإنتاج.

### إجراء التراجع

1. تحديد آخر إصدار مستقر من سجل الإصدارات.
2. تشغيل `.github/workflows/railway_deploy.yml` مثبَّتًا على الإصدار السابق.
3. عند تغيّر المخطط: `alembic downgrade` للمراجعة المستهدفة.
4. التحقق من فحص الصحة وعزل المستأجرين وقيود التدقيق.
5. تسجيل التراجع كقيد تدقيق وإبلاغ قائد المنصة.

### درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Deployment Readiness — Layer 1

Owner: Platform Lead

### Readiness checklist

- [x] Three separated environments: dev, staging, prod, with separated secrets.
- [x] Continuous integration blocks merge on failed checks (`.github/workflows/ci.yml`).
- [x] Code security scan via `.github/workflows/codeql.yml`.
- [x] Automated deploy via `.github/workflows/railway_deploy.yml`.
- [x] Staging smoke test before production (`.github/workflows/staging-smoke.yml`).
- [x] Automated daily snapshots via `.github/workflows/daily_snapshot.yml`.
- [x] Migrations have a rollback path via `alembic/` and `supabase/migrations/`.
- [x] Scheduled healthcheck via `.github/workflows/scheduled_healthcheck.yml`.
- [ ] A documented quarterly backup-restore drill.
- [ ] A periodically documented release-rollback drill proving under-15-minute time.

### Metrics

- Ratio of merges that passed through CI: 100%.
- Ratio of production deploys that passed through staging: 100%.
- Release rollback time: under 15 minutes (target).
- Recovery Point Objective RPO: 24 hours. Recovery Time Objective RTO: 60 minutes.
- Daily snapshot success rate: target 100%.

### Observability hooks

- A healthcheck after every deploy via `.github/workflows/scheduled_healthcheck.yml`.
- Deploy error capture via `dealix/observability/sentry.py`.
- An audit entry for every deploy, migration, and restore via `dealix/trust/audit.py`.
- Alert on a failed daily snapshot, deploy pipeline, or smoke test.

### Governance rules

- No production deploy without passing through staging and passing CI.
- A production deploy, a production migration, and a production data restore are A2-class actions at minimum and are recorded.
- No rollback deletes tenant data without an A3 approval.
- Real tenant data is never used outside the production environment.

### Rollback procedure

1. Identify the last stable release from the release log.
2. Run `.github/workflows/railway_deploy.yml` pinned to the prior release.
3. On a schema change: `alembic downgrade` to the target revision.
4. Verify the healthcheck, tenant isolation, and audit entries.
5. Record the rollback as an audit entry and notify the Platform Lead.

### Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
