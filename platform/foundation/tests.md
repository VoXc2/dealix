# العربية

## مواصفة الاختبار — الطبقة الأولى (الأساس)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات الاختبار ومعايير القبول لطبقة الأساس. هي مواصفة مكتوبة لا تحتوي كودًا.

### حالات الاختبار

#### F-T1 — إنشاء مستأجر

- خطوات: استدعاء `POST /api/v1/auth/register` ببيانات مستأجر صحيحة.
- القبول: يُنشأ سجل مستأجر له `tenant_id` فريد خلال أقل من 5 دقائق، ويُنشأ مستخدم مالك مرتبط به.

#### F-T2 — تقييد كل استعلام بـ tenant_id

- خطوات: تسجيل دخول كمستأجر أ، طلب موارد، ثم محاولة الوصول إلى معرّف مورد يخص مستأجر ب.
- القبول: يُرفض الوصول إلى موارد مستأجر ب؛ لا يظهر أي صف لا يحمل `tenant_id` المستأجر أ.

#### F-T3 — المصادقة وإدارة الجلسة

- خطوات: تسجيل دخول، استخدام رمز الوصول، تدويره عبر رمز التحديث، ثم إبطال الجلسة.
- القبول: رمز الوصول المنتهي يُرفض؛ الرمز المُبطَل لا يُعيد منح وصول.

#### F-T4 — التحكم بالأدوار (RBAC)

- خطوات: محاولة إجراء إداري بدور غير مخوَّل عبر مسار يحميه `api/security/rbac.py`.
- القبول: يُرفض الإجراء برمز 403 ويُكتب قيد تدقيق بالرفض.

#### F-T5 — بوابة الموافقة على الإجراءات الحساسة

- خطوات: تشغيل إجراء بتصنيف R3/S3.
- القبول: لا تنفيذ آلي؛ يُوجَّه الإجراء إلى مسار الموافقة في `dealix/trust/approval.py`.

#### F-T6 — قيد التدقيق لكل إجراء

- خطوات: تنفيذ مجموعة إجراءات حساسة وفحص سجل التدقيق.
- القبول: لكل إجراء حساس قيد تدقيق غير قابل للتعديل يحوي من/ماذا/متى/أي مستأجر.

#### F-T7 — التراجع عن إصدار

- خطوات: نشر إصدار، ثم تشغيل التراجع وفق `platform/foundation/rollback.md`.
- القبول: العودة لآخر إصدار مستقر خلال 15 دقيقة؛ فحص الصحة أخضر؛ لا فقدان بيانات.

#### F-T8 — استرجاع نسخة احتياطية

- خطوات: استرجاع لقطة يومية إلى بيئة معزولة.
- القبول: تكتمل البيانات حتى نقطة الاسترجاع المستهدفة (RPO 24 ساعة)؛ تظل حدود المستأجرين سليمة.

#### F-T9 — منع تسرّب الأسرار

- خطوات: فحص السجلات ومخرجات الأخطاء.
- القبول: لا يظهر أي سرّ أو معرّف شخصي (قاعدة `no_pii_in_logs`).

### معايير القبول الشاملة

- جميع حالات F-T1 إلى F-T9 ناجحة قبل أي نشر للإنتاج.
- التكامل المستمر `.github/workflows/ci.yml` يحجب الدمج عند فشل أي حالة.

### الروابط ذات الصلة

- `platform/foundation/readiness.md`
- `platform/multi_tenant/tests.md`
- `platform/security/tests.md`

# English

## Test Specification — Layer 1 (Foundation)

Owner: Platform Lead

### Purpose

This specification defines test cases and acceptance criteria for the Foundation layer. It is a written spec and contains no code.

### Test cases

#### F-T1 — Tenant creation

- Steps: call `POST /api/v1/auth/register` with valid tenant data.
- Acceptance: a tenant record with a unique `tenant_id` is created in under 5 minutes, and an owner user linked to it is created.

#### F-T2 — Every query scoped to tenant_id

- Steps: log in as tenant A, request resources, then attempt to access a resource ID belonging to tenant B.
- Acceptance: access to tenant B resources is denied; no row without tenant A's `tenant_id` is returned.

#### F-T3 — Authentication and session management

- Steps: log in, use the access token, rotate it via the refresh token, then revoke the session.
- Acceptance: an expired access token is rejected; a revoked token grants no access.

#### F-T4 — RBAC

- Steps: attempt an admin action with an unauthorized role on a path protected by `api/security/rbac.py`.
- Acceptance: the action is denied with 403 and a denial audit entry is written.

#### F-T5 — Sensitive action approval gate

- Steps: trigger an R3/S3-class action.
- Acceptance: no auto-execution; the action is routed to the approval path in `dealix/trust/approval.py`.

#### F-T6 — Audit entry per action

- Steps: execute a set of sensitive actions and inspect the audit log.
- Acceptance: every sensitive action has an immutable audit entry holding who/what/when/which tenant.

#### F-T7 — Release rollback

- Steps: deploy a release, then run the rollback per `platform/foundation/rollback.md`.
- Acceptance: return to the last stable release within 15 minutes; healthcheck green; no data loss.

#### F-T8 — Backup restore

- Steps: restore a daily snapshot into an isolated environment.
- Acceptance: data is complete to the recovery point (RPO 24 hours); tenant boundaries remain intact.

#### F-T9 — Secret leak prevention

- Steps: inspect logs and error outputs.
- Acceptance: no secret or personal identifier appears (`no_pii_in_logs` rule).

### Overall acceptance criteria

- All cases F-T1 through F-T9 pass before any production deploy.
- CI `.github/workflows/ci.yml` blocks merge on any failing case.

### Related docs

- `platform/foundation/readiness.md`
- `platform/multi_tenant/tests.md`
- `platform/security/tests.md`
