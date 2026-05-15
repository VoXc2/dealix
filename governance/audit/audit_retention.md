# العربية

**Owner:** قائد الخصوصية والثقة (Privacy & Trust Plane Lead).

## احتفاظ سجلات التدقيق

تحدّد هذه الوثيقة كم تُحفظ قيود التدقيق وكيف، وكيف تظل قابلة للتحقق طوال مدة الاحتفاظ.

### مدة الاحتفاظ

قيود التدقيق وحزم الأدلة تُحفظ **سبع سنوات** وفق جدول الاحتفاظ في `dealix/registers/compliance_saudi.yaml`. هذه المدة تغطي متطلبات السجل التجاري ومتطلبات الإثبات للعميل.

| العنصر | مدة الاحتفاظ |
|---|---|
| قيود التدقيق | 7 سنوات |
| حزم الأدلة المرتبطة بالقرارات | 7 سنوات |
| سجلات الموافقات | 7 سنوات |

### آلية التخزين

- المرحلة 0–1: `InMemoryAuditSink` مع مرآة في السجلات المهيكلة عبر `core/logging.py`.
- المرحلة 2: `PostgresSink` بجدول إلحاقي ومقسّم شهرياً، وفق ما تصفه `dealix/trust/audit.py`.
- النسخ الاحتياطية اليومية تشمل جدول التدقيق؛ الاسترجاع يحافظ على الترتيب والسلسلة.

### تعذّر التلاعب طوال الاحتفاظ

- الجدول إلحاقي على مستوى قاعدة البيانات؛ لا تحديث ولا حذف.
- كل قيد يحمل `prev_entry_id` لتشكيل سلسلة؛ التحقق الدوري يكشف أي فجوة.
- لا يُحذَف قيد قبل انتهاء مدته؛ بعد المدة يُحذَف وفق إجراء موثَّق فقط.

### الحذف بعد انتهاء المدة

- الحذف بعد سبع سنوات إجراء بتصنيف A3 يتطلب موافقة مزدوجة.
- الحذف نفسه يُسجَّل كقيد تدقيق ميتا (في سجل منفصل) لإثبات أن الحذف تمّ نظامياً.
- لا حذف انتقائي لقيود ضمن المدة؛ الحذف بالدفعات حسب القسم الشهري.

### قائمة الجاهزية

- [x] مدة الاحتفاظ محددة في سجل الامتثال (7 سنوات).
- [x] القيود مشمولة في النسخ الاحتياطية اليومية.
- [ ] جدول `PostgresSink` الإلحاقي المقسّم (مُخطَّط للمرحلة 2).
- [ ] إجراء الحذف الآلي بعد انتهاء المدة (مُخطَّط).
- [ ] التحقق الدوري من سلامة السلسلة (مُخطَّط).

### المقاييس

- نسبة القيود المحفوظة ضمن المدة: 100%.
- زمن استرجاع قيود من نسخة احتياطية.
- عدد عمليات الحذف بعد المدة الموثَّقة بقيد ميتا.

### خطاطيف المراقبة

- تنبيه عند فشل نسخ احتياطي يشمل جدول التدقيق.
- تنبيه عند اكتشاف فجوة سلسلة.

### الحوكمة والتراجع

- تقصير مدة الاحتفاظ ممنوع دون مراجعة قانونية.
- التراجع: استرجاع القيود من النسخة الاحتياطية مع التحقق من اكتمال السلسلة.

انظر أيضاً: `governance/audit/audit_schema.md`، `governance/compliance/data_deletion.md`.

---

# English

**Owner:** Privacy & Trust Plane Lead.

## Audit Log Retention

This document defines how long audit entries are kept and how, and how they remain verifiable throughout the retention period.

### Retention period

Audit entries and evidence packs are kept for **seven years** per the retention schedule in `dealix/registers/compliance_saudi.yaml`. This period covers commercial-record requirements and the need to prove actions to a customer.

| Item | Retention |
|---|---|
| Audit entries | 7 years |
| Evidence packs linked to decisions | 7 years |
| Approval records | 7 years |

### Storage mechanism

- Phase 0–1: `InMemoryAuditSink` with a mirror in structured logs via `core/logging.py`.
- Phase 2: `PostgresSink` with an append-only, monthly-partitioned table, as described by `dealix/trust/audit.py`.
- Daily backups include the audit table; restore preserves ordering and the chain.

### Tamper-evidence through retention

- The table is append-only at the database level; no update, no delete.
- Every entry carries `prev_entry_id` to form a chain; periodic verification detects any gap.
- No entry is deleted before its period ends; after the period it is deleted only via a documented procedure.

### Deletion after the period ends

- Deletion after seven years is an A3-class action requiring dual approval.
- The deletion itself is recorded as a meta audit entry (in a separate log) to prove the deletion was lawful.
- No selective deletion of entries within the period; deletion is by monthly-partition batches.

### Readiness checklist

- [x] Retention period defined in the compliance register (7 years).
- [x] Entries included in daily backups.
- [ ] Append-only, partitioned `PostgresSink` table (planned for Phase 2).
- [ ] Automated post-period deletion procedure (planned).
- [ ] Periodic chain-integrity verification (planned).

### Metrics

- Share of entries retained within the period: 100%.
- Time to restore entries from a backup.
- Count of post-period deletions documented by a meta entry.

### Observability hooks

- Alert when a backup that includes the audit table fails.
- Alert when a chain gap is detected.

### Governance and rollback

- Shortening the retention period is forbidden without a legal review.
- Rollback: restore entries from a backup with chain-completeness verification.

See also: `governance/audit/audit_schema.md`, `governance/compliance/data_deletion.md`.
