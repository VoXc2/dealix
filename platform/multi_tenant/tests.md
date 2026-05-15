# العربية

## مواصفة الاختبار — الطبقة الأولى (تعدد المستأجرين)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات اختبار عزل المستأجرين ومعايير قبولها. مواصفة مكتوبة بلا كود.

### حالات الاختبار

#### MT-T1 — إنشاء مستأجر

- خطوات: إنشاء مستأجر جديد عبر مسار التسجيل.
- القبول: يُخصَّص `tenant_id` فريد ويُنشأ مالك خلال أقل من 5 دقائق.

#### MT-T2 — تقييد الاستعلام بـ tenant_id

- خطوات: تسجيل دخول كمستأجر أ وطلب قائمة موارد.
- القبول: كل صف معاد يحمل `tenant_id` المستأجر أ فقط.

#### MT-T3 — رفض الوصول عبر المستأجرين

- خطوات: مستخدم مستأجر أ يطلب معرّف مورد يخص مستأجر ب.
- القبول: يُرفض الوصول؛ لا تُكشف بيانات مستأجر ب.

#### MT-T4 — عزل الملفات

- خطوات: رفع ملف كمستأجر أ ثم محاولة الوصول إليه كمستأجر ب.
- القبول: يُرفض الوصول؛ مفتاح الملف يتضمّن `tenant_id` المستأجر أ.

#### MT-T5 — عزل الذاكرة والمحادثات

- خطوات: إنشاء محادثة كمستأجر أ ثم استعلامها كمستأجر ب.
- القبول: لا تظهر محادثة مستأجر أ لمستأجر ب.

#### MT-T6 — حذف مستأجر بلا أثر جانبي

- خطوات: حذف مستأجر ب والتحقق من مستأجر أ ومستأجر ج.
- القبول: تُحذف بيانات مستأجر ب فقط؛ مستأجر أ وج سليمان تمامًا.

#### MT-T7 — حفظ قيود التدقيق بعد الحذف

- خطوات: حذف مستأجر ثم فحص سجل التدقيق.
- القبول: قيود التدقيق التاريخية للمستأجر المحذوف لا تزال موجودة.

#### MT-T8 — موافقة حذف المستأجر

- خطوات: بدء حذف مستأجر بدون موافقة.
- القبول: لا يُنفَّذ الحذف؛ يُوجَّه إلى مسار الموافقة `dealix/trust/approval.py`.

#### MT-T9 — استرجاع مستأجر محذوف

- خطوات: استرجاع مستأجر من آخر لقطة يومية إلى بيئة معزولة.
- القبول: تُستعاد بيانات المستأجر حتى نقطة RPO؛ المستأجرون الآخرون غير متأثرين.

### معايير القبول الشاملة

- جميع حالات MT-T1 إلى MT-T9 ناجحة قبل النشر للإنتاج.
- التكامل المستمر يحجب الدمج عند فشل أي حالة عزل.

### الروابط ذات الصلة

- `platform/multi_tenant/readiness.md`
- `platform/multi_tenant/tenant_isolation.md`
- `platform/foundation/tests.md`

# English

## Test Specification — Layer 1 (Multi-Tenancy)

Owner: Platform Lead

### Purpose

This specification defines tenant-isolation test cases and their acceptance criteria. It is a written spec with no code.

### Test cases

#### MT-T1 — Tenant creation

- Steps: create a new tenant via the registration path.
- Acceptance: a unique `tenant_id` is allocated and an owner is created in under 5 minutes.

#### MT-T2 — Query scoped to tenant_id

- Steps: log in as tenant A and request a resource list.
- Acceptance: every returned row carries only tenant A's `tenant_id`.

#### MT-T3 — Cross-tenant access denial

- Steps: a tenant A user requests a resource ID belonging to tenant B.
- Acceptance: access is denied; no tenant B data is exposed.

#### MT-T4 — File isolation

- Steps: upload a file as tenant A, then attempt to access it as tenant B.
- Acceptance: access is denied; the file key includes tenant A's `tenant_id`.

#### MT-T5 — Memory and conversation isolation

- Steps: create a conversation as tenant A, then query it as tenant B.
- Acceptance: tenant A's conversation does not appear for tenant B.

#### MT-T6 — Tenant deletion with no side effects

- Steps: delete tenant B and verify tenant A and tenant C.
- Acceptance: only tenant B data is deleted; tenants A and C are fully intact.

#### MT-T7 — Audit entries retained after deletion

- Steps: delete a tenant, then inspect the audit log.
- Acceptance: the deleted tenant's historical audit entries still exist.

#### MT-T8 — Tenant-deletion approval

- Steps: start a tenant deletion without an approval.
- Acceptance: the deletion does not execute; it is routed to the approval path `dealix/trust/approval.py`.

#### MT-T9 — Deleted tenant restore

- Steps: restore a tenant from the last daily snapshot into an isolated environment.
- Acceptance: tenant data is restored to the RPO point; other tenants are unaffected.

### Overall acceptance criteria

- All cases MT-T1 through MT-T9 pass before a production deploy.
- CI blocks merge on any failing isolation case.

### Related docs

- `platform/multi_tenant/readiness.md`
- `platform/multi_tenant/tenant_isolation.md`
- `platform/foundation/tests.md`
