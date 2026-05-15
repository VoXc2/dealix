# العربية

## معمارية الأساس — الطبقة الأولى

### الغرض

طبقة الأساس تضمن أن كل مستأجر (tenant) داخل منصة Dealix معزول، آمن، قابل للإدارة، وقابل للاسترجاع. هي القاعدة التي تبني عليها الطبقات الاثنتا عشرة المتبقية. لا توجد قدرة في المنصة تعمل بدون عزل المستأجر ومصادقته وتدقيق إجراءاته.

### المكونات

- **نموذج المستأجر**: كل صف وملف وذاكرة ومحادثة مرتبط بـ `tenant_id`. لا توجد بيانات بدون مستأجر.
- **المصادقة**: رموز JWT للوصول والتحديث، إدارة الجلسات، التحقق متعدد العوامل (TOTP)، تدفق الدعوات.
- **التحكم بالأدوار (RBAC)**: أدوار النظام وأدوار المستأجر، صلاحيات قائمة على القدرات.
- **الأسرار والتشفير**: متغيرات بيئة، تشفير أثناء النقل والتخزين، فصل أسرار البيئات.
- **النشر**: بيئات تطوير/تجهيز/إنتاج، تكامل مستمر، نشر آلي، تراجع.
- **النسخ الاحتياطي والاسترجاع**: لقطات يومية، استرجاع نقطة زمنية، اختبار الاسترجاع.
- **سجل التدقيق**: كل إجراء يولّد قيد تدقيق غير قابل للتعديل.
- **أساس الفوترة**: ربط الاستهلاك بالمستأجر عبر `tenant_id` لأغراض الفوترة المستقبلية.

### تدفق البيانات

1. يصل طلب إلى أحد موجّهات FastAPI الـ117.
2. الوسيط يتحقق من رمز JWT ويستخرج `tenant_id` و`user_id` والدور.
3. كل استعلام قاعدة بيانات يُقيَّد بـ `tenant_id` المستخرج.
4. الإجراءات الحساسة تُصنّف (A0–A3 / R0–R3 / S0–S3) وتُوجّه للموافقة عند اللزوم.
5. كل إجراء يُكتب كقيد تدقيق غير قابل للتعديل.
6. اللقطات اليومية تحفظ الحالة للاسترجاع.

### الربط بالكود الحالي

| المكوّن | المسار في المستودع |
|---|---|
| موجّهات API | `api/routers/` (117 موجّهًا) |
| مصادقة وجلسات | `api/routers/auth.py`، `api/security/jwt.py`، `api/security/auth_deps.py` |
| التحكم بالأدوار | `api/security/rbac.py` |
| مخطط المستأجرين والمستخدمين | `db/migrations/versions/20240101_001_auth_schema.py`، `db/models.py` |
| التصنيفات | `dealix/classifications/__init__.py` |
| الحوكمة والموافقات | `dealix/governance/approvals.py`، `dealix/trust/approval.py` |
| سجل التدقيق | `dealix/trust/audit.py`، `dealix/contracts/audit_log.py` |
| الامتثال السعودي | `dealix/registers/compliance_saudi.yaml`، `auto_client_acquisition/compliance_os/` |
| الهجرات | `alembic/`، `db/migrations/versions/`، `supabase/migrations/` |
| التكامل والنشر | `.github/workflows/ci.yml`، `.github/workflows/railway_deploy.yml`، `.github/workflows/daily_snapshot.yml` |

### الروابط ذات الصلة

- `platform/foundation/readiness.md`
- `platform/multi_tenant/tenant_isolation.md`
- `docs/DEALIX_OPERATING_CONSTITUTION.md`

# English

## Foundation Architecture — Layer 1

### Purpose

The Foundation layer guarantees that every tenant inside the Dealix platform is isolated, secure, manageable, and recoverable. It is the base on which the remaining twelve layers build. No platform capability runs without tenant isolation, authentication, and action auditing.

### Components

- **Tenant model**: every row, file, memory, and conversation is bound to a `tenant_id`. No data exists without a tenant.
- **Authentication**: JWT access and refresh tokens, session management, multi-factor verification (TOTP), invite flow.
- **RBAC**: system roles and tenant roles, capability-based permissions.
- **Secrets and encryption**: environment variables, encryption in transit and at rest, per-environment secret separation.
- **Deployment**: dev/staging/prod environments, continuous integration, automated deploy, rollback.
- **Backup and restore**: daily snapshots, point-in-time restore, restore drills.
- **Audit log**: every action emits an immutable audit entry.
- **Billing base**: usage attribution bound to `tenant_id` for future billing.

### Data flow

1. A request reaches one of the 117 FastAPI routers.
2. Middleware validates the JWT and extracts `tenant_id`, `user_id`, and role.
3. Every database query is scoped to the extracted `tenant_id`.
4. Sensitive actions are classified (A0–A3 / R0–R3 / S0–S3) and routed for approval when required.
5. Every action is written as an immutable audit entry.
6. Daily snapshots persist state for restore.

### Mapping to existing code

| Component | Repo path |
|---|---|
| API routers | `api/routers/` (117 routers) |
| Auth and sessions | `api/routers/auth.py`, `api/security/jwt.py`, `api/security/auth_deps.py` |
| RBAC | `api/security/rbac.py` |
| Tenant and user schema | `db/migrations/versions/20240101_001_auth_schema.py`, `db/models.py` |
| Classifications | `dealix/classifications/__init__.py` |
| Governance and approvals | `dealix/governance/approvals.py`, `dealix/trust/approval.py` |
| Audit log | `dealix/trust/audit.py`, `dealix/contracts/audit_log.py` |
| Saudi compliance | `dealix/registers/compliance_saudi.yaml`, `auto_client_acquisition/compliance_os/` |
| Migrations | `alembic/`, `db/migrations/versions/`, `supabase/migrations/` |
| CI and deploy | `.github/workflows/ci.yml`, `.github/workflows/railway_deploy.yml`, `.github/workflows/daily_snapshot.yml` |

### Related docs

- `platform/foundation/readiness.md`
- `platform/multi_tenant/tenant_isolation.md`
- `docs/DEALIX_OPERATING_CONSTITUTION.md`
