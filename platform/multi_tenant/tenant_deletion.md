# العربية

## حذف المستأجر — الطبقة الأولى (تعدد المستأجرين)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه الوثيقة كيف يُحذف مستأجر كامل من Dealix دون أي أثر على المستأجرين الآخرين، مع احترام الالتزامات النظامية للاحتفاظ.

### مبدأ الحذف

- الحذف مُقيَّد بـ `tenant_id` المستهدف فقط.
- لا يلمس الحذف أي صف أو ملف لا يحمل `tenant_id` المستهدف.
- قيود التدقيق التاريخية تُحفظ بعد الحذف للمساءلة النظامية.

### إجراء الحذف — خطوة بخطوة

1. طلب الحذف: يبدأ كإجراء بتصنيف A2 على الأقل ويتطلب موافقة موثَّقة عبر `dealix/trust/approval.py`.
2. التعطيل: إيقاف وصول كل مستخدمي المستأجر وإبطال جلساتهم.
3. فترة سماح: نافذة محدّدة قبل الحذف النهائي لإتاحة التراجع.
4. الحذف: إزالة صفوف قاعدة البيانات والملفات والذاكرة والمحادثات المُقيَّدة بـ `tenant_id`.
5. تأكيد العزل: عيّنة تحقّق أن مستأجرين آخرين سليمَين تمامًا.
6. الاحتفاظ النظامي: الإبقاء على قيود التدقيق والبيانات التي يلزم الاحتفاظ بها وفق `dealix/registers/compliance_saudi.yaml`.
7. التسجيل: كتابة قيد تدقيق نهائي بحذف المستأجر.

### قواعد الحوكمة

- لا حذف بدون موافقة موثَّقة.
- حذف بيانات حساسة S3 يتطلب موافقة A3.
- معالجة طلبات حذف صاحب البيانات تتبع `auto_client_acquisition/compliance_os/data_subject_requests.py` والمادة 18 من نظام حماية البيانات الشخصية.
- لا حذف صامت؛ كل حذف مُسجَّل.

### المقاييس

- زمن إكمال الحذف.
- عدد المستأجرين الآخرين المتأثرين: يجب أن يكون صفرًا.
- نسبة عمليات الحذف الموثَّقة بموافقة: 100%.

### المراقبة

- قيد تدقيق لكل مرحلة من مراحل الحذف عبر `dealix/trust/audit.py`.
- تنبيه إذا مسّ الحذف صفوفًا خارج `tenant_id` المستهدف.

### إجراء التراجع

1. خلال فترة السماح: إعادة تفعيل المستأجر تلغي الحذف بالكامل.
2. بعد الحذف النهائي: استرجاع من آخر لقطة يومية ضمن نافذة RPO إلى بيئة معزولة ثم إعادة الربط.
3. تسجيل التراجع كقيد تدقيق وإبلاغ قائد المنصة.

### درجة الجاهزية الحالية

تُقاس ضمن مجمل جاهزية تعدد المستأجرين في `platform/multi_tenant/readiness.md`. تمرين الحذف الموثَّق دوريًا فجوة جاهزية معروفة.

### الروابط ذات الصلة

- `platform/multi_tenant/tenant_isolation.md`
- `platform/deployment/backup_restore.md`
- `auto_client_acquisition/compliance_os/data_subject_requests.py`

# English

## Tenant Deletion — Layer 1 (Multi-Tenancy)

Owner: Platform Lead

### Purpose

This document defines how a full tenant is deleted from Dealix with no impact on other tenants, while respecting statutory retention obligations.

### Deletion principle

- Deletion is scoped to the target `tenant_id` only.
- Deletion never touches any row or file not carrying the target `tenant_id`.
- Historical audit entries are retained after deletion for statutory accountability.

### Deletion procedure — step by step

1. Deletion request: starts as an A2-class action at minimum and requires a documented approval via `dealix/trust/approval.py`.
2. Deactivation: stop access for all tenant users and revoke their sessions.
3. Grace period: a defined window before final deletion to allow rollback.
4. Deletion: remove database rows, files, memory, and conversations scoped to `tenant_id`.
5. Isolation confirmation: sample-verify that other tenants are fully intact.
6. Statutory retention: keep audit entries and data that must be retained per `dealix/registers/compliance_saudi.yaml`.
7. Record: write a final audit entry for the tenant deletion.

### Governance rules

- No deletion without a documented approval.
- Deleting S3 sensitive data requires an A3 approval.
- Handling of data-subject deletion requests follows `auto_client_acquisition/compliance_os/data_subject_requests.py` and PDPL Article 18.
- No silent deletion; every deletion is recorded.

### Metrics

- Deletion completion time.
- Count of other tenants affected: must be zero.
- Ratio of deletions documented with an approval: 100%.

### Observability

- An audit entry for every deletion stage via `dealix/trust/audit.py`.
- Alert if deletion touches rows outside the target `tenant_id`.

### Rollback procedure

1. During the grace period: reactivating the tenant fully cancels the deletion.
2. After final deletion: restore from the last daily snapshot within the RPO window into an isolated environment, then re-link.
3. Record the rollback as an audit entry and notify the Platform Lead.

### Current readiness score

Measured within the overall multi-tenancy readiness in `platform/multi_tenant/readiness.md`. A periodically documented deletion drill is a known readiness gap.

### Related docs

- `platform/multi_tenant/tenant_isolation.md`
- `platform/deployment/backup_restore.md`
- `auto_client_acquisition/compliance_os/data_subject_requests.py`
