# العربية

## المستخدمون — الطبقة الأولى (الهوية)

Owner: قائد المنصة (Platform Lead)

### الغرض

تصف هذه الوثيقة دورة حياة المستخدم داخل مستأجر Dealix: الإنشاء، الدعوة، التعديل، التعطيل، الحذف.

### نموذج المستخدم

- كل مستخدم مرتبط بـ `tenant_id` واحد ودور واحد على الأقل.
- المستخدم الأول في المستأجر هو المالك، يُنشأ مع المستأجر.
- بيانات المستخدم محفوظة في مخطط المصادقة (`db/migrations/versions/20240101_001_auth_schema.py`).

### دورة حياة المستخدم

| المرحلة | الوصف |
|---|---|
| إنشاء المالك | يُنشأ تلقائيًا عند تسجيل المستأجر عبر `api/routers/auth.py` |
| الدعوة | المالك أو المدير يدعو مستخدمًا ضمن نفس `tenant_id` |
| التعديل | تغيير الدور أو البيانات؛ تغيير الدور يُسجَّل كقيد تدقيق |
| التعطيل | إيقاف الوصول دون حذف البيانات؛ تُبطَل الجلسات |
| الحذف | إزالة بيانات المستخدم مع الحفاظ على قيود التدقيق التاريخية |

### قواعد الحوكمة

- لا يُنشأ مستخدم بدون `tenant_id`.
- لا يمكن حذف آخر مالك في مستأجر؛ يجب نقل الملكية أولًا.
- حذف مستخدم إجراء يُسجَّل ولا يحذف قيود تدقيقه التاريخية.
- معالجة بيانات المستخدم تتبع الأساس النظامي في `auto_client_acquisition/compliance_os/` (نظام حماية البيانات الشخصية، المواد 5/13/14/18/21).

### حقوق صاحب البيانات

- طلبات الوصول والتصحيح والحذف تُدار عبر `auto_client_acquisition/compliance_os/data_subject_requests.py`.

### المقاييس

- زمن إنشاء مستخدم/إكمال دعوة.
- عدد المستخدمين النشطين لكل مستأجر.

### المراقبة

- تُسجَّل أحداث الإنشاء والدعوة والتعطيل والحذف مع `tenant_id`.

### إجراء التراجع

- إعادة تفعيل مستخدم مُعطَّل: عكس حالة التعطيل، يُسجَّل كقيد تدقيق.
- استرجاع مستخدم محذوف خطأً: من آخر لقطة يومية ضمن نافذة RPO.

### الروابط ذات الصلة

- `platform/identity/rbac.md`
- `platform/identity/sessions.md`
- `platform/multi_tenant/tenant_deletion.md`

# English

## Users — Layer 1 (Identity)

Owner: Platform Lead

### Purpose

This document describes the user lifecycle inside a Dealix tenant: creation, invitation, modification, deactivation, deletion.

### User model

- Every user is bound to a single `tenant_id` and at least one role.
- The first user in a tenant is the Owner, created with the tenant.
- User data is stored in the auth schema (`db/migrations/versions/20240101_001_auth_schema.py`).

### User lifecycle

| Stage | Description |
|---|---|
| Owner creation | Created automatically on tenant registration via `api/routers/auth.py` |
| Invitation | An Owner or Admin invites a user under the same `tenant_id` |
| Modification | Role or data change; role change is recorded as an audit entry |
| Deactivation | Access stopped without deleting data; sessions are revoked |
| Deletion | Removal of user data while preserving historical audit entries |

### Governance rules

- No user is created without a `tenant_id`.
- The last Owner of a tenant cannot be deleted; ownership must be transferred first.
- User deletion is a recorded action and does not delete their historical audit entries.
- User-data processing follows the lawful basis in `auto_client_acquisition/compliance_os/` (PDPL Articles 5/13/14/18/21).

### Data subject rights

- Access, correction, and deletion requests are handled via `auto_client_acquisition/compliance_os/data_subject_requests.py`.

### Metrics

- Time to create a user / complete an invite.
- Active user count per tenant.

### Observability

- Creation, invite, deactivation, and deletion events are logged with `tenant_id`.

### Rollback procedure

- Reactivate a deactivated user: reverse the deactivation state, recorded as an audit entry.
- Restore a wrongly deleted user: from the last daily snapshot within the RPO window.

### Related docs

- `platform/identity/rbac.md`
- `platform/identity/sessions.md`
- `platform/multi_tenant/tenant_deletion.md`
