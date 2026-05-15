# العربية

## مواصفة الاختبار — الطبقة الأولى (الهوية)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات اختبار الهوية ومعايير قبولها. مواصفة مكتوبة بلا كود.

### حالات الاختبار

#### ID-T1 — تسجيل دخول ناجح

- خطوات: استدعاء مسار الدخول في `api/routers/auth.py` ببيانات صحيحة.
- القبول: يُصدر رمز وصول ورمز تحديث؛ كلاهما يحمل `tenant_id` و`user_id` والدور الصحيح.

#### ID-T2 — رفض بيانات خاطئة

- خطوات: تسجيل دخول بكلمة مرور خاطئة.
- القبول: يُرفض الدخول؛ لا يُصدر رمز؛ يُسجَّل حدث فشل.

#### ID-T3 — انتهاء رمز الوصول

- خطوات: استخدام رمز وصول بعد انتهاء عمره.
- القبول: يُرفض الطلب برمز 401.

#### ID-T4 — تدوير الرمز

- خطوات: استخدام رمز التحديث لإصدار رمز وصول جديد.
- القبول: يُصدر رمز وصول صالح دون إعادة إدخال كلمة المرور.

#### ID-T5 — إبطال الجلسة

- خطوات: إبطال جلسة ثم محاولة استخدام رمز التحديث المرتبط بها.
- القبول: يُرفض التدوير؛ الجلسة لم تعد صالحة.

#### ID-T6 — إنفاذ RBAC

- خطوات: تنفيذ إجراء إداري بدور Viewer.
- القبول: يُرفض الإجراء برمز 403 ويُكتب قيد تدقيق رفض.

#### ID-T7 — عزل الدور بين المستأجرين

- خطوات: محاولة مستخدم مستأجر أ الوصول إلى مورد مستأجر ب.
- القبول: يُرفض الوصول مهما كان دور المستخدم.

#### ID-T8 — حماية آخر مالك

- خطوات: محاولة حذف آخر مالك في مستأجر.
- القبول: يُرفض الحذف؛ يُطلب نقل الملكية أولًا.

#### ID-T9 — محدّد معدّل الدخول

- خطوات: تكرار محاولات دخول فاشلة فوق العتبة.
- القبول: تُحجب المحاولات الإضافية عبر `api/security/rate_limit.py`.

### معايير القبول الشاملة

- جميع حالات ID-T1 إلى ID-T9 ناجحة قبل النشر للإنتاج.
- التكامل المستمر يحجب الدمج عند فشل أي حالة.

### الروابط ذات الصلة

- `platform/identity/readiness.md`
- `platform/foundation/tests.md`
- `platform/security/tests.md`

# English

## Test Specification — Layer 1 (Identity)

Owner: Platform Lead

### Purpose

This specification defines identity test cases and their acceptance criteria. It is a written spec with no code.

### Test cases

#### ID-T1 — Successful login

- Steps: call the login path in `api/routers/auth.py` with valid credentials.
- Acceptance: an access token and refresh token are issued; both carry the correct `tenant_id`, `user_id`, and role.

#### ID-T2 — Reject wrong credentials

- Steps: log in with a wrong password.
- Acceptance: login is rejected; no token is issued; a failure event is logged.

#### ID-T3 — Access token expiry

- Steps: use an access token after its lifetime ends.
- Acceptance: the request is rejected with 401.

#### ID-T4 — Token rotation

- Steps: use the refresh token to issue a new access token.
- Acceptance: a valid access token is issued without re-entering the password.

#### ID-T5 — Session revocation

- Steps: revoke a session, then attempt to use its associated refresh token.
- Acceptance: rotation is rejected; the session is no longer valid.

#### ID-T6 — RBAC enforcement

- Steps: perform an admin action with a Viewer role.
- Acceptance: the action is rejected with 403 and a denial audit entry is written.

#### ID-T7 — Cross-tenant role isolation

- Steps: a tenant A user attempts to access a tenant B resource.
- Acceptance: access is rejected regardless of the user's role.

#### ID-T8 — Last-owner protection

- Steps: attempt to delete the last Owner of a tenant.
- Acceptance: deletion is rejected; ownership transfer is required first.

#### ID-T9 — Login rate limit

- Steps: repeat failed login attempts above the threshold.
- Acceptance: additional attempts are blocked via `api/security/rate_limit.py`.

### Overall acceptance criteria

- All cases ID-T1 through ID-T9 pass before a production deploy.
- CI blocks merge on any failing case.

### Related docs

- `platform/identity/readiness.md`
- `platform/foundation/tests.md`
- `platform/security/tests.md`
