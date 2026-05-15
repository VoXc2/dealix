# العربية

## الجلسات — الطبقة الأولى (الهوية)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف تُنشأ جلسات المستخدمين وتُدار وتُبطَل، بحيث يكون لكل وصول حدود زمنية واضحة وأثر تدقيقي.

### نموذج الجلسة

- الجلسة تمثَّل برمز تحديث محفوظ في جدول `refresh_tokens`.
- رمز الوصول قصير العمر؛ رمز التحديث أطول عمرًا وقابل للإبطال.
- كل جلسة مرتبطة بـ `user_id` و`tenant_id`.

### دورة حياة الجلسة

| المرحلة | الوصف |
|---|---|
| فتح | عند تسجيل الدخول الناجح عبر `api/routers/auth.py` |
| تحديث | رمز التحديث يصدر رمز وصول جديدًا |
| إبطال | المستخدم أو المدير يُسقط الجلسة؛ يُحذف رمز التحديث |
| انتهاء | الجلسة غير المستخدمة تنتهي تلقائيًا بعد المدة المحدّدة |

### قواعد الحوكمة

- إبطال جلسة لا يُلغي قيود التدقيق التاريخية.
- تغيير كلمة المرور يُبطل كل جلسات المستخدم.
- المدير يستطيع إبطال جلسات مستخدمي مستأجره فقط، لا جلسات مستأجر آخر.

### المقاييس

- عدد الجلسات النشطة لكل مستأجر.
- متوسط عمر الجلسة.
- عدد عمليات الإبطال اليدوي.

### المراقبة

- تُسجَّل أحداث الفتح والتحديث والإبطال والانتهاء.
- تنبيه على تحديث رمز من موقع جغرافي غير معتاد (مؤشر سرقة رمز).

### إجراء التراجع

- جلسة أُبطلت خطأً: لا تُستعاد؛ يعيد المستخدم تسجيل الدخول لفتح جلسة جديدة.
- عند تسرّب رموز مشتبه به: إبطال جماعي لكل جلسات المستأجر المتأثر وتسجيله كقيد تدقيق.

### درجة الجاهزية الحالية

تُقاس جاهزية الجلسات ضمن مجمل جاهزية الهوية في `platform/identity/readiness.md`.

### الروابط ذات الصلة

- `platform/identity/auth.md`
- `platform/identity/readiness.md`
- `platform/security/incident_response.md`

# English

## Sessions — Layer 1 (Identity)

Owner: Platform Lead

### Purpose

This document describes how user sessions are created, managed, and revoked, so that every access has clear time bounds and an audit trail.

### Session model

- A session is represented by a refresh token stored in the `refresh_tokens` table.
- The access token is short-lived; the refresh token is longer-lived and revocable.
- Every session is bound to a `user_id` and `tenant_id`.

### Session lifecycle

| Stage | Description |
|---|---|
| Open | On successful login via `api/routers/auth.py` |
| Refresh | The refresh token issues a new access token |
| Revoke | A user or admin drops the session; the refresh token is deleted |
| Expire | An unused session expires automatically after the set period |

### Governance rules

- Revoking a session does not cancel historical audit entries.
- A password change revokes all of the user's sessions.
- An admin can revoke sessions only for their own tenant's users, not another tenant's.

### Metrics

- Active session count per tenant.
- Average session age.
- Count of manual revocations.

### Observability

- Open, refresh, revoke, and expire events are logged.
- Alert on a token refresh from an unusual geographic location (token-theft indicator).

### Rollback procedure

- A wrongly revoked session is not restored; the user logs in again to open a new session.
- On suspected token leakage: bulk-revoke all sessions for the affected tenant and record it as an audit entry.

### Current readiness score

Session readiness is measured within the overall identity readiness in `platform/identity/readiness.md`.

### Related docs

- `platform/identity/auth.md`
- `platform/identity/readiness.md`
- `platform/security/incident_response.md`
