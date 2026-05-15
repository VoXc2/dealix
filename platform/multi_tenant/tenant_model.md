# العربية

## نموذج المستأجر — الطبقة الأولى (تعدد المستأجرين)

Owner: قائد المنصة (Platform Lead)

### الغرض

يحدّد نموذج المستأجر الوحدة الأساسية التي تُنظَّم حولها كل بيانات Dealix. كل عميل مؤسسي هو مستأجر له `tenant_id` فريد، وكل صف وملف وذاكرة ومحادثة مرتبط به.

### المكوّنات

- **سجل المستأجر**: كيان قاعدة بيانات يحمل `tenant_id` واسم العميل وحالته وإعداداته.
- **عمود `tenant_id`**: حاضر في كل جدول بيانات للأعمال، مفهرس، إلزامي.
- **مالك المستأجر**: أول مستخدم، يُنشأ مع المستأجر.
- **إعدادات المستأجر**: تفضيلات معزولة لكل مستأجر.
- **أساس الفوترة**: استهلاك المستأجر منسوب عبر `tenant_id` عبر `dealix/observability/cost_tracker.py`.

### إنشاء المستأجر

1. استدعاء مسار التسجيل في `api/routers/auth.py`.
2. تخصيص `tenant_id` فريد.
3. إنشاء مستخدم المالك ضمن نفس `tenant_id`.
4. تهيئة إعدادات المستأجر الافتراضية.
5. كتابة قيد تدقيق بإنشاء المستأجر.

الهدف: إنشاء مستأجر جاهز خلال أقل من 5 دقائق.

### قواعد الحوكمة

- لا صف بيانات أعمال بدون `tenant_id`.
- إنشاء أو حذف مستأجر إجراء بتصنيف A2 على الأقل (`dealix/classifications/__init__.py`).
- لا تنفّذ المنصة إجراءات خارجية موجَّهة للعملاء بدون موافقة المستأجر (سياسة الموافقة المسبقة).
- معالجة بيانات المستأجر تتبع `dealix/registers/compliance_saudi.yaml`.

### المقاييس

- زمن إنشاء المستأجر: أقل من 5 دقائق.
- نسبة الجداول الحاملة لـ `tenant_id`: 100%.
- عدد المستأجرين النشطين.

### المراقبة

- قيد تدقيق لكل إنشاء وتعديل وحذف مستأجر عبر `dealix/trust/audit.py`.
- تتبّع الاستهلاك لكل `tenant_id`.

### إجراء التراجع

- إلغاء إنشاء مستأجر خاطئ: تعطيله ثم حذفه عبر إجراء `platform/multi_tenant/tenant_deletion.md`.
- استرجاع مستأجر محذوف خطأً من آخر لقطة يومية ضمن نافذة RPO.

### الروابط ذات الصلة

- `platform/multi_tenant/tenant_isolation.md`
- `platform/multi_tenant/data_boundaries.md`
- `platform/foundation/architecture.md`

# English

## Tenant Model — Layer 1 (Multi-Tenancy)

Owner: Platform Lead

### Purpose

The tenant model defines the base unit around which all Dealix data is organized. Every enterprise customer is a tenant with a unique `tenant_id`, and every row, file, memory, and conversation is bound to it.

### Components

- **Tenant record**: a database entity holding `tenant_id`, customer name, status, and settings.
- **`tenant_id` column**: present in every business data table, indexed, mandatory.
- **Tenant owner**: the first user, created with the tenant.
- **Tenant settings**: per-tenant isolated preferences.
- **Billing base**: tenant usage attributed via `tenant_id` through `dealix/observability/cost_tracker.py`.

### Tenant creation

1. Call the registration path in `api/routers/auth.py`.
2. Allocate a unique `tenant_id`.
3. Create the owner user under the same `tenant_id`.
4. Initialize default tenant settings.
5. Write an audit entry for tenant creation.

Target: a ready tenant in under 5 minutes.

### Governance rules

- No business data row exists without a `tenant_id`.
- Tenant creation or deletion is an A2-class action at minimum (`dealix/classifications/__init__.py`).
- The platform does not perform external customer-facing actions without tenant approval (approval-first policy).
- Tenant data processing follows `dealix/registers/compliance_saudi.yaml`.

### Metrics

- Tenant creation time: under 5 minutes.
- Tables carrying `tenant_id`: 100%.
- Active tenant count.

### Observability

- An audit entry for every tenant creation, modification, and deletion via `dealix/trust/audit.py`.
- Usage tracking per `tenant_id`.

### Rollback procedure

- Undo a wrongly created tenant: deactivate then delete via the `platform/multi_tenant/tenant_deletion.md` procedure.
- Restore a wrongly deleted tenant from the last daily snapshot within the RPO window.

### Related docs

- `platform/multi_tenant/tenant_isolation.md`
- `platform/multi_tenant/data_boundaries.md`
- `platform/foundation/architecture.md`
