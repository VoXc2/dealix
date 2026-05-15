# العربية

## عزل المستأجرين — الطبقة الأولى (تعدد المستأجرين)

Owner: قائد المنصة (Platform Lead)

### الغرض

يضمن عزل المستأجرين ألّا يصل أي مستأجر إلى بيانات مستأجر آخر، في قاعدة البيانات والملفات والذاكرة والمحادثات. هذا الوعد الأساسي لطبقة الأساس.

### آلية العزل

- **العزل المنطقي**: كل صف يحمل `tenant_id`؛ كل استعلام مُقيَّد به في الوسيط.
- **استخراج السياق**: `tenant_id` يُستخرج من رمز JWT عبر `api/security/auth_deps.py` في كل طلب.
- **عزل الملفات**: كل ملف مخزَّن تحت مسار/مفتاح يتضمّن `tenant_id`.
- **عزل الذاكرة والمحادثات**: ذاكرة العمل والمحادثات مُفهرسة بـ `tenant_id`.
- **عزل التكلفة**: الاستهلاك منسوب لكل `tenant_id`.

### طبقات الدفاع

1. التطبيق: تقييد كل استعلام في طبقة الوصول للبيانات.
2. الوسيط: رفض أي طلب بلا `tenant_id` صالح.
3. الاختبار: حالات عزل في `platform/multi_tenant/tests.md`.
4. المراقبة: تنبيه على أي استعلام يعيد صفًّا بـ `tenant_id` غير متطابق.

### قواعد الحوكمة

- لا استعلام أعمال بدون شرط `tenant_id`.
- محاولة وصول عبر المستأجرين تُسجَّل وتُنبَّه عليها (الخطر F-R1).
- أي ميزة جديدة تمسّ بيانات يجب أن تُثبت تقييدها بـ `tenant_id` قبل الدمج.

### المقاييس

- عدد الاستعلامات بلا تقييد `tenant_id` المكتشَفة: هدف صفر.
- عدد محاولات الوصول عبر المستأجرين المرفوضة.
- نسبة تغطية اختبارات العزل للموجّهات.

### المراقبة

- تسجيل كل رفض وصول عبر المستأجرين مع المسار والمستأجرين المعنيين.
- تنبيه فوري على أي صف بـ `tenant_id` غير متطابق في نتيجة استعلام.
- تتبّع عبر `dealix/observability/otel.py`.

### إجراء التراجع

1. عند اشتباه تسرّب: تجميد المسار المتأثر فورًا.
2. تحديد نطاق التسرّب من قيود التدقيق وتتبّعات `otel`.
3. تطبيق التراجع وفق `platform/foundation/rollback.md`.
4. إبلاغ المستأجرين المتأثرين وفق `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
5. تسجيل الحادث كقيد تدقيق.

### درجة الجاهزية الحالية

تُقاس ضمن مجمل جاهزية تعدد المستأجرين في `platform/multi_tenant/readiness.md`.

### الروابط ذات الصلة

- `platform/multi_tenant/data_boundaries.md`
- `platform/multi_tenant/readiness.md`
- `docs/PDPL_BREACH_RESPONSE_PLAN.md`

# English

## Tenant Isolation — Layer 1 (Multi-Tenancy)

Owner: Platform Lead

### Purpose

Tenant isolation guarantees that no tenant reaches another tenant's data — in the database, files, memory, and conversations. This is the core promise of the Foundation layer.

### Isolation mechanism

- **Logical isolation**: every row carries `tenant_id`; every query is scoped to it in middleware.
- **Context extraction**: `tenant_id` is extracted from the JWT via `api/security/auth_deps.py` on every request.
- **File isolation**: every stored file lives under a path/key that includes `tenant_id`.
- **Memory and conversation isolation**: working memory and conversations are indexed by `tenant_id`.
- **Cost isolation**: usage is attributed per `tenant_id`.

### Layers of defense

1. Application: query scoping in the data access layer.
2. Middleware: reject any request without a valid `tenant_id`.
3. Testing: isolation cases in `platform/multi_tenant/tests.md`.
4. Observability: alert on any query returning a row with a mismatched `tenant_id`.

### Governance rules

- No business query without a `tenant_id` condition.
- A cross-tenant access attempt is logged and alerted (risk F-R1).
- Any new feature touching data must prove its `tenant_id` scoping before merge.

### Metrics

- Count of queries detected without `tenant_id` scoping: target zero.
- Count of rejected cross-tenant access attempts.
- Isolation test coverage ratio across routers.

### Observability

- Logging of every cross-tenant access denial with the path and tenants involved.
- Immediate alert on any row with a mismatched `tenant_id` in a query result.
- Tracing via `dealix/observability/otel.py`.

### Rollback procedure

1. On suspected leakage: immediately freeze the affected path.
2. Determine the leak scope from audit entries and `otel` traces.
3. Apply rollback per `platform/foundation/rollback.md`.
4. Notify affected tenants per `docs/PDPL_BREACH_RESPONSE_PLAN.md`.
5. Record the incident as an audit entry.

### Current readiness score

Measured within the overall multi-tenancy readiness in `platform/multi_tenant/readiness.md`.

### Related docs

- `platform/multi_tenant/data_boundaries.md`
- `platform/multi_tenant/readiness.md`
- `docs/PDPL_BREACH_RESPONSE_PLAN.md`
