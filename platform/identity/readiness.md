# العربية

## جاهزية الهوية — الطبقة الأولى

Owner: قائد المنصة (Platform Lead)

### قائمة الجاهزية

- [x] مصادقة برموز JWT للوصول والتحديث عبر `api/security/jwt.py`.
- [x] استخراج `tenant_id` و`user_id` والدور في كل طلب عبر `api/security/auth_deps.py`.
- [x] إدارة جلسات عبر جدول `refresh_tokens` مع قدرة إبطال.
- [x] تحكم بالأدوار مُنفَّذ عبر `api/security/rbac.py`.
- [x] تدفق دعوة يربط كل مستخدم بمستأجر واحد.
- [x] محدّدات معدّل على محاولات الدخول عبر `api/security/rate_limit.py`.
- [x] كل تغيير دور وكل إبطال جلسة يولّد قيد تدقيق.
- [ ] تفعيل التحقق متعدد العوامل إلزاميًا لكل الحسابات الإدارية (متاح، غير إلزامي بعد).
- [ ] تمرين موثَّق لاكتشاف سرقة رمز والاستجابة لها.

### المقاييس

- نسبة الموجّهات المحمية بفحص RBAC: هدف 100%.
- زمن إصدار الرمز: أقل من ثانية واحدة.
- معدل فشل الدخول الطبيعي: تحت العتبة المحدّدة.
- نسبة الحسابات الإدارية المفعّلة للتحقق متعدد العوامل.
- عدد الجلسات النشطة لكل مستأجر.

### خطاطيف المراقبة

- تسجيل أحداث الدخول والفشل والتدوير والإبطال عبر `dealix/observability/otel.py`.
- التقاط أخطاء المصادقة عبر `dealix/observability/sentry.py`.
- قيود تدقيق تغييرات الأدوار والجلسات عبر `dealix/trust/audit.py`.
- تنبيه على ارتفاع فشل الدخول وعلى تدوير رمز من موقع غير معتاد.

### قواعد الحوكمة

- لا وصول بدون رمز صالح غير منتهٍ.
- ترقية دور إلى مالك تتطلب موافقة موثَّقة (تصنيف A2 على الأقل).
- لا يصل أي دور إلى بيانات مستأجر آخر.
- الأسرار والرموز لا تُكتب في السجلات (قاعدة `no_pii_in_logs`).

### إجراء التراجع

1. عند اشتباه تسرّب رموز: إبطال جماعي لجلسات المستأجر المتأثر.
2. عكس تغيير دور خاطئ إلى الدور السابق وتسجيله كقيد تدقيق.
3. استرجاع مستخدم محذوف خطأً من آخر لقطة يومية ضمن نافذة RPO.
4. التحقق من فحص الصحة وقيود التدقيق بعد التراجع وإبلاغ قائد المنصة.

### درجة الجاهزية الحالية

**الدرجة: 80 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Identity Readiness — Layer 1

Owner: Platform Lead

### Readiness checklist

- [x] JWT access and refresh token authentication via `api/security/jwt.py`.
- [x] Extraction of `tenant_id`, `user_id`, and role on every request via `api/security/auth_deps.py`.
- [x] Session management via the `refresh_tokens` table with revocation capability.
- [x] RBAC enforced via `api/security/rbac.py`.
- [x] An invite flow binds every user to a single tenant.
- [x] Rate limits on login attempts via `api/security/rate_limit.py`.
- [x] Every role change and session revocation emits an audit entry.
- [ ] Mandatory multi-factor verification enabled for all admin accounts (available, not yet mandatory).
- [ ] Documented drill for token-theft detection and response.

### Metrics

- Ratio of routers protected by an RBAC check: target 100%.
- Token issue time: under one second.
- Normal login failure rate: below the set threshold.
- Ratio of admin accounts with multi-factor verification enabled.
- Active session count per tenant.

### Observability hooks

- Login, failure, rotation, and revocation events logged via `dealix/observability/otel.py`.
- Authentication error capture via `dealix/observability/sentry.py`.
- Audit entries for role and session changes via `dealix/trust/audit.py`.
- Alert on login-failure spikes and on token refresh from an unusual location.

### Governance rules

- No access without a valid, non-expired token.
- Promoting a role to Owner requires a documented approval (A2 class at minimum).
- No role reaches another tenant's data.
- Secrets and tokens are never written to logs (`no_pii_in_logs` rule).

### Rollback procedure

1. On suspected token leakage: bulk-revoke sessions for the affected tenant.
2. Reverse a wrong role change to the prior role and record it as an audit entry.
3. Restore a wrongly deleted user from the last daily snapshot within the RPO window.
4. Verify healthcheck and audit entries after rollback and notify the Platform Lead.

### Current readiness score

**Score: 80 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
