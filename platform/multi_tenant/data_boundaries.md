# العربية

## حدود البيانات — الطبقة الأولى (تعدد المستأجرين)

Owner: قائد المنصة (Platform Lead)

### الغرض

تحدّد هذه الوثيقة الحدود التي لا تعبرها بيانات المستأجر: أين تُخزَّن، كيف تُصنَّف، ومن يصل إليها.

### أنواع البيانات وحدودها

| نوع البيانات | الموقع | الحد |
|---|---|---|
| صفوف قاعدة البيانات | الجداول المُهاجَرة عبر `db/migrations/versions/` و`supabase/migrations/` | عمود `tenant_id` إلزامي |
| الملفات والمرفقات | تخزين كائنات بمفتاح يتضمّن `tenant_id` | بادئة المستأجر إلزامية |
| الذاكرة والمحادثات | مُفهرسة بـ `tenant_id` | لا قراءة عبر المستأجرين |
| القياسات والتكلفة | منسوبة عبر `dealix/observability/cost_tracker.py` | تجميع لكل مستأجر فقط |
| قيود التدقيق | عبر `dealix/trust/audit.py` | مرتبطة بـ `tenant_id` ومحفوظة بعد حذف المستأجر للمساءلة |

### تصنيف الحساسية

- تُصنَّف البيانات الحساسة عبر فئات `dealix/classifications/__init__.py` (S0–S3).
- بيانات S3 (الأكثر حساسية): تصديرها يتطلب موافقة A3.
- معالجة البيانات الشخصية تتبع `auto_client_acquisition/compliance_os/` (المواد 5/13/14/18/21 من نظام حماية البيانات الشخصية) و`dealix/registers/compliance_saudi.yaml`.

### قواعد الحوكمة

- لا تعبر بيانات أعمال حدود `tenant_id` إطلاقًا.
- تصدير البيانات إجراء مصنَّف ويُسجَّل.
- لا مشاركة بيانات مع طرف ثالث دون أساس نظامي مسجَّل في سجل المعالجة (`auto_client_acquisition/compliance_os/ropa.py`).
- لا تُكتب بيانات شخصية في السجلات (قاعدة `no_pii_in_logs`).

### المقاييس

- عدد عبور الحدود المكتشَف: هدف صفر.
- نسبة البيانات الحساسة المصنَّفة.
- عدد عمليات التصدير وكلها موثَّقة بموافقة.

### المراقبة

- قيد تدقيق لكل تصدير بيانات.
- تنبيه على أي وصول لبيانات S3 خارج مسار موافقة.

### إجراء التراجع

- تصدير بيانات خاطئ: إبطال الوصول للملف المُصدَّر وتسجيل الحادث.
- استرجاع بيانات حُذفت خطأً من آخر لقطة يومية ضمن نافذة RPO.

### الروابط ذات الصلة

- `platform/multi_tenant/tenant_isolation.md`
- `platform/security/encryption.md`
- `dealix/registers/compliance_saudi.yaml`

# English

## Data Boundaries — Layer 1 (Multi-Tenancy)

Owner: Platform Lead

### Purpose

This document defines the boundaries that tenant data does not cross: where it is stored, how it is classified, and who reaches it.

### Data types and their boundaries

| Data type | Location | Boundary |
|---|---|---|
| Database rows | Tables migrated via `db/migrations/versions/` and `supabase/migrations/` | `tenant_id` column mandatory |
| Files and attachments | Object storage with a key including `tenant_id` | Tenant prefix mandatory |
| Memory and conversations | Indexed by `tenant_id` | No cross-tenant reads |
| Metrics and cost | Attributed via `dealix/observability/cost_tracker.py` | Per-tenant aggregation only |
| Audit entries | Via `dealix/trust/audit.py` | Bound to `tenant_id`, retained after tenant deletion for accountability |

### Sensitivity classification

- Sensitive data is classified via the `dealix/classifications/__init__.py` classes (S0–S3).
- S3 data (most sensitive): export requires an A3 approval.
- Personal-data processing follows `auto_client_acquisition/compliance_os/` (PDPL Articles 5/13/14/18/21) and `dealix/registers/compliance_saudi.yaml`.

### Governance rules

- Business data never crosses a `tenant_id` boundary.
- Data export is a classified, recorded action.
- No third-party data sharing without a lawful basis recorded in the processing register (`auto_client_acquisition/compliance_os/ropa.py`).
- Personal data is never written to logs (`no_pii_in_logs` rule).

### Metrics

- Count of detected boundary crossings: target zero.
- Ratio of sensitive data that is classified.
- Count of export operations, all documented with an approval.

### Observability

- An audit entry for every data export.
- Alert on any access to S3 data outside an approval path.

### Rollback procedure

- A wrong data export: revoke access to the exported file and record the incident.
- Restore wrongly deleted data from the last daily snapshot within the RPO window.

### Related docs

- `platform/multi_tenant/tenant_isolation.md`
- `platform/security/encryption.md`
- `dealix/registers/compliance_saudi.yaml`
