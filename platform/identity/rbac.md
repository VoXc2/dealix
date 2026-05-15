# العربية

## التحكم بالأدوار — الطبقة الأولى (الهوية)

Owner: قائد المنصة (Platform Lead)

### الغرض

يحدّد التحكم بالأدوار (RBAC) ما يستطيع كل مستخدم فعله داخل مستأجره. الصلاحية قائمة على القدرات لا على الهوية الفردية.

### نموذج الأدوار

- **أدوار النظام**: تخص تشغيل المنصة (مثل قائد المنصة)، خارج نطاق أي مستأجر.
- **أدوار المستأجر**: تُطبَّق ضمن `tenant_id` واحد.

| دور المستأجر | القدرات |
|---|---|
| المالك (Owner) | إدارة المستخدمين، الفوترة، الإعدادات، كل قدرات الأدوار الأدنى |
| المدير (Admin) | إدارة المستخدمين والإعدادات ضمن المستأجر |
| العضو (Member) | تنفيذ العمل اليومي ضمن صلاحياته |
| المُشاهد (Viewer) | قراءة فقط |

### الإنفاذ

- الإنفاذ عبر `api/security/rbac.py` على مستوى كل موجّه.
- كل قرار صلاحية مُقيَّد بـ `tenant_id` المستخرج من الرمز.
- الإجراءات الحساسة تُصنّف عبر `dealix/classifications/__init__.py` (A0–A3 / R0–R3 / S0–S3) وقد تتطلب موافقة فوق صلاحية الدور.

### قواعد الحوكمة

- لا يستطيع دور أدنى منح نفسه قدرة دور أعلى.
- ترقية دور إلى مالك إجراء يتطلب موافقة موثَّقة.
- لا يصل أي دور إلى بيانات مستأجر آخر مهما كانت قدرته.
- كل تغيير دور يُكتب كقيد تدقيق عبر `dealix/trust/audit.py`.

### المقاييس

- نسبة الموجّهات المحمية بفحص RBAC.
- عدد محاولات الوصول المرفوضة (403) لكل مستأجر.

### المراقبة

- تُسجَّل قرارات الرفض مع الدور والمسار و`tenant_id`.
- تنبيه على نمط رفض متكرر (مؤشر تصعيد صلاحية).

### الروابط ذات الصلة

- `platform/identity/auth.md`
- `platform/identity/users.md`
- `platform/security/access_control.md`

# English

## RBAC — Layer 1 (Identity)

Owner: Platform Lead

### Purpose

RBAC defines what each user can do inside their tenant. Permission is capability-based, not based on individual identity.

### Role model

- **System roles**: cover platform operation (e.g. Platform Lead), outside any tenant scope.
- **Tenant roles**: applied within a single `tenant_id`.

| Tenant role | Capabilities |
|---|---|
| Owner | Manage users, billing, settings, all lower-role capabilities |
| Admin | Manage users and settings within the tenant |
| Member | Perform daily work within their permissions |
| Viewer | Read only |

### Enforcement

- Enforcement via `api/security/rbac.py` at the per-router level.
- Every permission decision is scoped to the `tenant_id` extracted from the token.
- Sensitive actions are classified via `dealix/classifications/__init__.py` (A0–A3 / R0–R3 / S0–S3) and may require approval above the role's capability.

### Governance rules

- A lower role cannot grant itself a higher role's capability.
- Promoting a role to Owner is an action requiring a documented approval.
- No role reaches another tenant's data regardless of its capability.
- Every role change is written as an audit entry via `dealix/trust/audit.py`.

### Metrics

- Ratio of routers protected by an RBAC check.
- Count of denied (403) access attempts per tenant.

### Observability

- Denial decisions are logged with role, path, and `tenant_id`.
- Alert on a repeated denial pattern (privilege-escalation indicator).

### Related docs

- `platform/identity/auth.md`
- `platform/identity/users.md`
- `platform/security/access_control.md`
