# العربية

## جاهزية الأمن — الطبقة الأولى

Owner: قائد المنصة (Platform Lead)

### قائمة الجاهزية

- [x] كل الأسرار في متغيرات بيئة منفصلة لكل بيئة، لا في الكود.
- [x] التشفير أثناء النقل (TLS) لكل اتصالات API الـ117.
- [x] التشفير أثناء التخزين لقاعدة البيانات والنسخ الاحتياطية والملفات.
- [x] كلمات المرور مُجزَّأة، لا تُخزَّن نصًّا.
- [x] التحكم بالوصول عبر المصادقة وRBAC وتقييد المستأجر.
- [x] حماية SSRF عبر `api/security/ssrf_guard.py` ومحدّد المعدّل عبر `api/security/rate_limit.py`.
- [x] فحص الكود الثابت عبر `.github/workflows/codeql.yml`.
- [x] خطة استجابة للحوادث موثَّقة مرتبطة بـ `docs/SECURITY_RUNBOOK.md`.
- [ ] تمرين استجابة للحوادث موثَّق دوريًا (محاكاة تسرّب).
- [ ] جدول تدوير أسرار آلي موثَّق ومُتحقَّق منه.

### المقاييس

- نسبة الاتصالات المشفّرة: 100%.
- عدد الأسرار المُسرَّبة في الكود المكتشَفة: هدف صفر.
- نسبة الموجّهات المحمية بمصادقة وRBAC: هدف 100%.
- زمن الاحتواء عند حادث حرج: أقل من ساعة.
- عدد الحوادث المُبلَّغ عنها ضمن المهلة النظامية.

### خطاطيف المراقبة

- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تتبّع الطلبات عبر `dealix/observability/otel.py`.
- قيود تدقيق الأمن عبر `dealix/trust/audit.py`.
- انحراف الأساس عبر `.github/workflows/watchdog_drift.yml`.
- تنبيه على اكتشاف سرّ، اتصال غير مشفّر، نمط رفض متكرر.

### قواعد الحوكمة

- لا يُكتب أي سرّ في السجلات (قاعدة `no_pii_in_logs`).
- منح صلاحية إدارية أو تغيير سرّ إنتاجي إجراء بتصنيف A2 على الأقل.
- الإبلاغ عن خرق البيانات الشخصية يتبع نظام حماية البيانات الشخصية عبر `auto_client_acquisition/compliance_os/`.
- لا إخفاء حادث؛ كل حادث مُسجَّل كقيد تدقيق.

### إجراء التراجع

1. عند تسرّب سرّ: تدوير فوري وإبطال السرّ القديم.
2. عند خلل في إعداد أمني: التراجع لآخر إعداد آمن معروف وفق `platform/foundation/rollback.md`.
3. عند مساس ببيانات شخصية: تطبيق `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
4. التحقق من فحص الصحة والعزل وتسجيل إغلاق الحادث.

### درجة الجاهزية الحالية

**الدرجة: 77 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Security Readiness — Layer 1

Owner: Platform Lead

### Readiness checklist

- [x] All secrets in per-environment separated environment variables, not in code.
- [x] Encryption in transit (TLS) for all 117 API connections.
- [x] Encryption at rest for the database, backups, and files.
- [x] Passwords hashed, never stored as plaintext.
- [x] Access control via authentication, RBAC, and tenant scoping.
- [x] SSRF protection via `api/security/ssrf_guard.py` and rate limiting via `api/security/rate_limit.py`.
- [x] Static code scanning via `.github/workflows/codeql.yml`.
- [x] A documented incident-response plan linked to `docs/SECURITY_RUNBOOK.md`.
- [ ] A periodically documented incident-response drill (leak simulation).
- [ ] A documented, verified automated secret-rotation schedule.

### Metrics

- Ratio of encrypted connections: 100%.
- Count of secrets detected leaked in code: target zero.
- Ratio of routers protected by auth and RBAC: target 100%.
- Containment time for a critical incident: under one hour.
- Count of incidents reported within the statutory window.

### Observability hooks

- Error capture via `dealix/observability/sentry.py`.
- Request tracing via `dealix/observability/otel.py`.
- Security audit entries via `dealix/trust/audit.py`.
- Baseline drift via `.github/workflows/watchdog_drift.yml`.
- Alert on secret detection, unencrypted connection, repeated denial pattern.

### Governance rules

- No secret is written to logs (`no_pii_in_logs` rule).
- Granting an admin permission or changing a production secret is an A2-class action at minimum.
- Personal-data breach reporting follows PDPL via `auto_client_acquisition/compliance_os/`.
- No incident concealment; every incident is recorded as an audit entry.

### Rollback procedure

1. On a leaked secret: immediate rotation and revocation of the old secret.
2. On a security-configuration fault: revert to the last known-good setting per `platform/foundation/rollback.md`.
3. On impact to personal data: apply `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
4. Verify the healthcheck and isolation, and record the incident closure.

### Current readiness score

**Score: 77 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
