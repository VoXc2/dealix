# العربية

**Owner:** قائد الخصوصية والثقة (Privacy & Trust Plane Lead).

## حذف البيانات

تحدّد هذه الوثيقة كيف تُحذَف بيانات Dealix: بناءً على طلب صاحب البيانات، أو عند انتهاء مدة الاحتفاظ. الحذف إجراء عالي المخاطر يمر عبر الموافقة دائماً.

### مسارات الحذف

1. **حذف بناءً على طلب صاحب البيانات (PDPL المادة 18):** يُعالَج عبر `auto_client_acquisition/compliance_os/data_subject_requests.py` ووفق `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.
2. **حذف بانتهاء مدة الاحتفاظ:** يُطبَّق على البيانات التي تجاوزت جدول الاحتفاظ في `dealix/registers/compliance_saudi.yaml`.
3. **حذف مستأجر كامل:** يشمل كل بيانات المستأجر دون أثر على غيره.

### تصنيف المخاطر

حذف بيانات شخصية إجراء بتصنيف A3/R3/S3: غير عكوس، يمسّ بيانات شخصية، ويتطلب موافقة مزدوجة من المالك القانوني ومالك الحوكمة. لا حذف آلي لبيانات S3.

### الآلية

1. يصل طلب الحذف (من صاحب بيانات أو من مهمة احتفاظ مجدوَلة).
2. يُتحقَّق من نطاق البيانات والأساس النظامي المرتبط.
3. يُرفع للموافقة المزدوجة وفق `governance/approval_rules/legal_approval_rules.md`.
4. عند الموافقة يُنفَّذ الحذف على كل المخازن: قاعدة البيانات، الملفات، الذاكرة، النسخ المتفرّعة.
5. **قيود التدقيق لا تُحذَف:** الحذف نفسه يُسجَّل كقيد تدقيق يثبت أن الحذف تمّ نظامياً، ومتى، وبموافقة من.

### استثناء قيود التدقيق

قيود التدقيق وحزم الأدلة محفوظة سبع سنوات (راجع `governance/audit/audit_retention.md`) ولا تُحذَف بطلب صاحب بيانات؛ لأنها سجل امتثال نظامي. تُستخدم فيها معرّفات مستعارة لا بيانات شخصية خام (قاعدة `no_pii_in_logs`)، فلا يتعارض حفظها مع حق المحو.

### قائمة الجاهزية

- [x] مسار حذف طلب صاحب البيانات مُنفَّذ في `data_subject_requests.py`.
- [x] الحذف يمر عبر موافقة مزدوجة A3.
- [x] الحذف يُسجَّل كقيد تدقيق دون مساس بقيود التدقيق.
- [ ] الحذف الآلي بانتهاء مدة الاحتفاظ (مُخطَّط — يحتاج هجرة ومهمة مجدوَلة).
- [ ] تمرين موثَّق لحذف مستأجر كامل (إجراء قائم، يحتاج تمريناً دورياً).

### المقاييس

- زمن تنفيذ طلب حذف من الموافقة حتى الاكتمال.
- نسبة طلبات الحذف المكتملة عبر كل المخازن.
- عدد عمليات الحذف الموثَّقة بقيد تدقيق: 100% من عمليات الحذف.

### خطاطيف المراقبة

- قيد تدقيق عند استلام طلب الحذف وعند اكتماله عبر `dealix/trust/audit.py`.
- تنبيه عند فشل حذف في أحد المخازن.

### قواعد الحوكمة

- لا حذف بيانات شخصية دون موافقة مزدوجة موثَّقة.
- قيود التدقيق لا تُحذَف بطلب محو؛ مبرَّر بحفظها كسجل امتثال.
- الحذف يُطبَّق على كل المخازن؛ لا حذف جزئي صامت.

### إجراء التراجع

- الحذف غير عكوس بطبيعته؛ لا تراجع بعد التنفيذ.
- الضمان قبل التنفيذ: التحقق من النطاق والموافقة المزدوجة وقيد التدقيق المسبق.
- عند خطأ في النطاق المقترح: يُرفض الطلب قبل الموافقة ويُعاد تحديد النطاق.

انظر أيضاً: `governance/compliance/pdpl_readiness.md`، `governance/audit/audit_retention.md`، `governance/policies/data_handling_policy.md`.

---

# English

**Owner:** Privacy & Trust Plane Lead.

## Data Deletion

This document defines how Dealix data is deleted: on a data subject's request, or when the retention period ends. Deletion is a high-risk action that always passes through approval.

### Deletion paths

1. **Deletion on a data subject request (PDPL Article 18):** handled via `auto_client_acquisition/compliance_os/data_subject_requests.py` and per `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`.
2. **Deletion on retention-period expiry:** applied to data past the retention schedule in `dealix/registers/compliance_saudi.yaml`.
3. **Full tenant deletion:** covers all of a tenant's data with no impact on others.

### Risk classification

Deleting personal data is an A3/R3/S3-class action: irreversible, touches personal data, and requires dual approval from the legal owner and the governance owner. There is no auto-deletion of S3 data.

### Mechanism

1. A deletion request arrives (from a data subject or a scheduled retention job).
2. The data scope and the linked lawful basis are verified.
3. It is raised for dual approval per `governance/approval_rules/legal_approval_rules.md`.
4. On approval, deletion is executed across all stores: database, files, memory, derived copies.
5. **Audit entries are not deleted:** the deletion itself is recorded as an audit entry proving the deletion was lawful, when, and approved by whom.

### Audit-entry exception

Audit entries and evidence packs are kept seven years (see `governance/audit/audit_retention.md`) and are not deleted on a data subject request, because they are a statutory compliance record. They use pseudonymous identifiers, not raw personal data (`no_pii_in_logs` rule), so retaining them does not conflict with the right to erasure.

### Readiness checklist

- [x] The data subject request deletion path is implemented in `data_subject_requests.py`.
- [x] Deletion passes through dual A3 approval.
- [x] Deletion is recorded as an audit entry without touching audit entries.
- [ ] Automatic deletion on retention-period expiry (planned — needs a migration and a scheduled job).
- [ ] Documented full-tenant-deletion drill (procedure exists, needs a periodic drill).

### Metrics

- Time from approval to completion for a deletion request.
- Share of deletion requests completed across all stores.
- Count of deletions documented by an audit entry: 100% of deletions.

### Observability hooks

- Audit entry on deletion request receipt and on completion via `dealix/trust/audit.py`.
- Alert on a failed deletion in any store.

### Governance rules

- No personal data deletion without a documented dual approval.
- Audit entries are not deleted on an erasure request; their retention as a compliance record is the justification.
- Deletion is applied across all stores; no silent partial deletion.

### Rollback procedure

- Deletion is irreversible by nature; there is no rollback after execution.
- The guarantee is pre-execution: scope verification, dual approval, and the prior audit entry.
- On an error in the proposed scope: the request is rejected before approval and the scope is redefined.

See also: `governance/compliance/pdpl_readiness.md`, `governance/audit/audit_retention.md`, `governance/policies/data_handling_policy.md`.
