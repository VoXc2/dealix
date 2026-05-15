# العربية

## المصادقة — الطبقة الأولى (الهوية)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف يثبت المستخدمون هويتهم داخل Dealix وكيف تُدار رموزهم، بحيث لا يصل أي مستخدم إلى بيانات إلا ضمن مستأجره.

### آلية المصادقة

- تسجيل الدخول عبر `POST` على مسارات `api/routers/auth.py`.
- إصدار رمز وصول JWT قصير العمر ورمز تحديث أطول عمرًا، عبر `api/security/jwt.py`.
- كل رمز يحمل `tenant_id` و`user_id` والدور؛ يُستخرج في كل طلب عبر `api/security/auth_deps.py`.
- التحقق متعدد العوامل (TOTP) متاح للحسابات الإدارية.
- تدفق الدعوة: ينشئ المالك دعوة مرتبطة بمستأجره؛ المدعوّ يكمل التسجيل ضمن نفس `tenant_id`.

### دورة حياة الرمز

| المرحلة | الوصف |
|---|---|
| إصدار | عند تسجيل الدخول الناجح؛ رمز وصول قصير + رمز تحديث |
| استخدام | رمز الوصول في ترويسة كل طلب؛ يُتحقَّق منه في الوسيط |
| تدوير | رمز التحديث يصدر رمز وصول جديدًا دون إعادة إدخال كلمة المرور |
| إبطال | إبطال الجلسة يُسقط رمز التحديث في جدول `refresh_tokens` |

### قواعد المصادقة

- لا وصول بدون رمز صالح غير منتهٍ.
- كلمات المرور مُجزَّأة (hashed)، لا تُخزَّن نصًّا.
- محاولات الدخول الفاشلة محدودة المعدّل عبر `api/security/rate_limit.py`.
- مفاتيح API للخدمات تُدار عبر `api/security/api_key.py` ومنفصلة عن جلسات المستخدمين.

### المراقبة

- تُسجَّل أحداث الدخول والفشل والتدوير والإبطال.
- تنبيه على ارتفاع غير طبيعي في فشل الدخول (مؤشر هجوم).

### القيود غير القابلة للتفاوض

- لا يُكتب أي رمز أو كلمة مرور في السجلات.
- لا تنفّذ المنصة إجراءات مصادقة خارجية نيابة عن المستخدم دون موافقته.

### الروابط ذات الصلة

- `platform/identity/sessions.md`
- `platform/identity/rbac.md`
- `platform/security/access_control.md`

# English

## Authentication — Layer 1 (Identity)

Owner: Platform Lead

### Purpose

This document describes how users prove their identity inside Dealix and how their tokens are managed, so that no user reaches data outside their tenant.

### Authentication mechanism

- Login via `POST` on `api/routers/auth.py` paths.
- Issue of a short-lived JWT access token and a longer-lived refresh token, via `api/security/jwt.py`.
- Each token carries `tenant_id`, `user_id`, and role; extracted on every request via `api/security/auth_deps.py`.
- Multi-factor verification (TOTP) is available for admin accounts.
- Invite flow: an owner creates an invite bound to their tenant; the invitee completes registration under the same `tenant_id`.

### Token lifecycle

| Stage | Description |
|---|---|
| Issue | On successful login; short access token + refresh token |
| Use | Access token in each request header; validated in middleware |
| Rotate | Refresh token issues a new access token without re-entering the password |
| Revoke | Session revocation drops the refresh token in the `refresh_tokens` table |

### Authentication rules

- No access without a valid, non-expired token.
- Passwords are hashed, never stored as plaintext.
- Failed login attempts are rate-limited via `api/security/rate_limit.py`.
- Service API keys are managed via `api/security/api_key.py` and kept separate from user sessions.

### Observability

- Login, failure, rotation, and revocation events are logged.
- Alert on an abnormal spike in login failures (attack indicator).

### Non-negotiables

- No token or password is written to logs.
- The platform does not perform external authentication actions on a user's behalf without their consent.

### Related docs

- `platform/identity/sessions.md`
- `platform/identity/rbac.md`
- `platform/security/access_control.md`
