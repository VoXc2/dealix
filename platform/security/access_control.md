# العربية

## التحكم بالوصول — الطبقة الأولى (الأمن)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة كيف يُتحكَّم بالوصول إلى موارد Dealix على كل مستوى: واجهة API، قاعدة البيانات، الأسرار، البنية التحتية.

### مستويات التحكم

| المستوى | الضابط |
|---|---|
| واجهة API | مصادقة JWT + `api/security/auth_deps.py` + RBAC عبر `api/security/rbac.py` |
| تقييد المستأجر | كل استعلام مُقيَّد بـ `tenant_id` |
| معدّل الطلبات | `api/security/rate_limit.py` ضد الإساءة |
| مفاتيح الخدمات | `api/security/api_key.py` منفصلة عن جلسات المستخدمين |
| حماية SSRF | `api/security/ssrf_guard.py` ضد طلبات الخادم الصادرة الخبيثة |
| الأسرار والبنية التحتية | وصول مقصور على أدوار محدّدة، مُسجَّل |

### مبدأ أقل امتياز

- كل دور ومفتاح يحصل على أدنى صلاحية تكفي لمهمته.
- لا صلاحية دائمة لإجراء حساس؛ تمرّ عبر مسار الموافقة `dealix/trust/approval.py`.
- الإجراءات مصنَّفة A0–A3 / R0–R3 / S0–S3 عبر `dealix/classifications/__init__.py`.

### قواعد الحوكمة

- لا وصول بلا مصادقة سارية.
- لا يصل أي دور إلى بيانات مستأجر آخر.
- منح صلاحية إدارية أو ترقية دور إجراء يتطلب موافقة موثَّقة.
- كل رفض ومنح وصول يُكتب كقيد تدقيق.

### المقاييس

- نسبة الموجّهات المحمية بمصادقة وRBAC: هدف 100%.
- عدد محاولات الوصول غير المصرّح بها المرفوضة.
- عدد الأدوار ذات الصلاحيات الزائدة المكتشَفة: هدف صفر.

### المراقبة

- تسجيل كل قرار رفض وصول مع الدور والمسار و`tenant_id`.
- تنبيه على نمط رفض متكرر (مؤشر تصعيد صلاحية أو هجوم).
- تتبّع عبر `dealix/observability/otel.py` والتقاط الأخطاء عبر `dealix/observability/sentry.py`.

### إجراء التراجع

1. عكس منح صلاحية خاطئ إلى الحالة السابقة وتسجيله كقيد تدقيق.
2. عند اشتباه وصول غير مصرّح به: إبطال الجلسات والمفاتيح المتأثرة.
3. تطبيق `docs/SECURITY_RUNBOOK.md` وإبلاغ قائد المنصة.

### الروابط ذات الصلة

- `platform/identity/rbac.md`
- `platform/security/incident_response.md`
- `dealix/classifications/__init__.py`

# English

## Access Control — Layer 1 (Security)

Owner: Platform Lead

### Purpose

This document describes how access to Dealix resources is controlled at every level: API surface, database, secrets, and infrastructure.

### Control levels

| Level | Control |
|---|---|
| API surface | JWT auth + `api/security/auth_deps.py` + RBAC via `api/security/rbac.py` |
| Tenant scoping | Every query scoped to `tenant_id` |
| Request rate | `api/security/rate_limit.py` against abuse |
| Service keys | `api/security/api_key.py` separate from user sessions |
| SSRF protection | `api/security/ssrf_guard.py` against malicious outbound server requests |
| Secrets and infrastructure | Access restricted to specific roles, logged |

### Least-privilege principle

- Every role and key gets the lowest permission sufficient for its task.
- No standing permission for a sensitive action; it passes through the approval path `dealix/trust/approval.py`.
- Actions are classified A0–A3 / R0–R3 / S0–S3 via `dealix/classifications/__init__.py`.

### Governance rules

- No access without valid authentication.
- No role reaches another tenant's data.
- Granting an admin permission or promoting a role requires a documented approval.
- Every access denial and grant is written as an audit entry.

### Metrics

- Ratio of routers protected by auth and RBAC: target 100%.
- Count of rejected unauthorized access attempts.
- Count of over-privileged roles detected: target zero.

### Observability

- Logging of every access-denial decision with role, path, and `tenant_id`.
- Alert on a repeated denial pattern (privilege-escalation or attack indicator).
- Tracing via `dealix/observability/otel.py` and error capture via `dealix/observability/sentry.py`.

### Rollback procedure

1. Reverse a wrong permission grant to the prior state and record it as an audit entry.
2. On suspected unauthorized access: revoke affected sessions and keys.
3. Apply `docs/SECURITY_RUNBOOK.md` and notify the Platform Lead.

### Related docs

- `platform/identity/rbac.md`
- `platform/security/incident_response.md`
- `dealix/classifications/__init__.py`
