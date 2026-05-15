# العربية

## مواصفة الاختبار — الطبقة الأولى (النشر)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات اختبار النشر ومعايير قبولها. مواصفة مكتوبة بلا كود.

### حالات الاختبار

#### DEP-T1 — فصل البيئات

- خطوات: فحص أسرار ومتغيرات بيئات التطوير والتجهيز والإنتاج.
- القبول: لا سرّ مشترك بين البيئات؛ لا بيانات إنتاج في التطوير أو التجهيز.

#### DEP-T2 — حجب الدمج عند فشل التكامل المستمر

- خطوات: تقديم تغيير يُفشِل أحد فحوص `.github/workflows/ci.yml`.
- القبول: يُحجب الدمج حتى نجاح كل الفحوص.

#### DEP-T3 — اختبار الدخان على التجهيز

- خطوات: نشر للتجهيز ثم تشغيل `.github/workflows/staging-smoke.yml`.
- القبول: عند فشل الدخان تُحجب الترقية للإنتاج.

#### DEP-T4 — نشر الإنتاج عبر التجهيز

- خطوات: محاولة نشر للإنتاج لم يمرّ بالتجهيز.
- القبول: يُرفض النشر المباشر؛ يلزم المرور بالتجهيز.

#### DEP-T5 — نجاح اللقطة اليومية

- خطوات: التحقق من تشغيل `.github/workflows/daily_snapshot.yml`.
- القبول: تُنشأ لقطة يومية صالحة؛ تنبيه عند الفشل.

#### DEP-T6 — استرجاع نسخة احتياطية

- خطوات: استرجاع لقطة إلى بيئة معزولة.
- القبول: تكتمل البيانات حتى نقطة RPO؛ حدود `tenant_id` سليمة؛ ضمن RTO.

#### DEP-T7 — تراجع إصدار

- خطوات: نشر إصدار ثم تشغيل التراجع وفق `rollback_plan.md`.
- القبول: العودة لآخر إصدار مستقر خلال 15 دقيقة؛ فحص الصحة أخضر.

#### DEP-T8 — تراجع هجرة المخطط

- خطوات: تطبيق هجرة ثم `alembic downgrade` للمراجعة السابقة.
- القبول: يعود المخطط للحالة السابقة دون فقدان بيانات مستأجر.

#### DEP-T9 — قيد تدقيق النشر

- خطوات: تنفيذ نشر وفحص سجل التدقيق.
- القبول: قيد تدقيق يوثّق النشر بالبيئة والإصدار والوقت.

### معايير القبول الشاملة

- جميع حالات DEP-T1 إلى DEP-T9 ناجحة قبل أي نشر للإنتاج.
- التكامل المستمر يحجب الدمج عند فشل أي حالة.

### الروابط ذات الصلة

- `platform/deployment/readiness.md`
- `platform/deployment/rollback_plan.md`
- `platform/foundation/tests.md`

# English

## Test Specification — Layer 1 (Deployment)

Owner: Platform Lead

### Purpose

This specification defines deployment test cases and their acceptance criteria. It is a written spec with no code.

### Test cases

#### DEP-T1 — Environment separation

- Steps: inspect secrets and variables of the dev, staging, and prod environments.
- Acceptance: no secret shared across environments; no production data in dev or staging.

#### DEP-T2 — Merge blocked on CI failure

- Steps: submit a change that fails a `.github/workflows/ci.yml` check.
- Acceptance: the merge is blocked until all checks pass.

#### DEP-T3 — Staging smoke test

- Steps: deploy to staging then run `.github/workflows/staging-smoke.yml`.
- Acceptance: on a smoke failure, promotion to production is blocked.

#### DEP-T4 — Production deploy via staging

- Steps: attempt a production deploy that did not pass through staging.
- Acceptance: the direct deploy is rejected; passing through staging is required.

#### DEP-T5 — Daily snapshot success

- Steps: verify that `.github/workflows/daily_snapshot.yml` runs.
- Acceptance: a valid daily snapshot is created; an alert fires on failure.

#### DEP-T6 — Backup restore

- Steps: restore a snapshot into an isolated environment.
- Acceptance: data is complete to the RPO point; `tenant_id` boundaries intact; within RTO.

#### DEP-T7 — Release rollback

- Steps: deploy a release then run the rollback per `rollback_plan.md`.
- Acceptance: return to the last stable release within 15 minutes; healthcheck green.

#### DEP-T8 — Schema migration rollback

- Steps: apply a migration then `alembic downgrade` to the prior revision.
- Acceptance: the schema returns to the prior state with no tenant data loss.

#### DEP-T9 — Deploy audit entry

- Steps: run a deploy and inspect the audit log.
- Acceptance: an audit entry documents the deploy with environment, release, and time.

### Overall acceptance criteria

- All cases DEP-T1 through DEP-T9 pass before any production deploy.
- CI blocks merge on any failing case.

### Related docs

- `platform/deployment/readiness.md`
- `platform/deployment/rollback_plan.md`
- `platform/foundation/tests.md`
