# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة.

## الغرض

محرّك التدقيق يكتب سجلاً غير قابل للتعديل لكل قرار وموافقة وتنفيذ في طبقة الحوكمة. هدفه واحد: أن نُثبت للعميل لاحقاً ما الذي فعله الذكاء الاصطناعي، ولماذا، ومن وافق عليه. السجل إلحاقي فقط (append-only)؛ لا تعديل ولا حذف.

## المكوّنات

- مصبّ التدقيق `dealix/trust/audit.py` — واجهة `AuditSink` المجرّدة مع `append()` و`recent()`؛ المرحلة 0–1 تستخدم `InMemoryAuditSink` مع نسخة في السجلات المهيكلة، والمرحلة 2 تستخدم `PostgresSink` بجدول إلحاقي وتقسيم شهري.
- عقد قيد التدقيق `dealix/contracts/audit_log.py` — بنية `AuditEntry`.
- حزم الأدلة في `dealix/trust/` — تربط كل قرار بمخرجاته وأدلته.

## ما يُسجَّل

كل قيد `AuditEntry` يحوي على الأقل: المُعرّف، المستأجر، الفاعل (وكيل أو إنسان)، الإجراء، التصنيف A/R/S، قرار السياسة، مرجع الموافقة إن وُجد، الطابع الزمني، ومُعرّف القرار `decision_id` للربط.

## آلية تعذّر التلاعب

1. السجل إلحاقي فقط؛ لا تتيح الواجهة أي تعديل أو حذف.
2. في المرحلة 2 يكون جدول التدقيق إلحاقياً على مستوى قاعدة البيانات ومقسّماً شهرياً.
3. كل قيد يحمل مُعرّف القيد السابق ضمن نفس المستأجر لتشكيل سلسلة قابلة للتحقق.
4. أي فجوة في السلسلة تُرفع كحادث حوكمة فوري.

## قائمة الجاهزية

- [x] كل قرار سياسة وكل تغيير موافقة يُكتب كقيد تدقيق.
- [x] السجل إلحاقي فقط؛ لا واجهة تعديل أو حذف.
- [x] كل قيد مرتبط بمستأجر و`decision_id`.
- [ ] جدول `PostgresSink` الإلحاقي المقسّم (مُخطَّط للمرحلة 2).
- [ ] التحقق الدوري من سلامة سلسلة القيود (مُخطَّط).

## المقاييس

- تغطية قيود التدقيق: 100% من الإجراءات S2/S3 والموافقات.
- زمن كتابة القيد: أقل من 20 مللي ثانية.
- عدد فجوات السلسلة المكتشفة: صفر (هدف).

## خطاطيف المراقبة

- مرآة كل قيد في السجلات المهيكلة عبر `core/logging.py`.
- تتبّع الكتابة عبر `dealix/observability/otel.py`.
- تنبيه عند فشل كتابة قيد أو اكتشاف فجوة سلسلة.

## قواعد الحوكمة

- لا يُكتب أي معرّف شخصي خام في القيد (قاعدة `no_pii_in_logs`)؛ تُستخدم معرّفات مستعارة.
- مدة الاحتفاظ بالقيود سبع سنوات وفق `dealix/registers/compliance_saudi.yaml`.
- حذف قيد تدقيق ممنوع منعاً مطلقاً؛ التصحيح يتم بقيد جديد معاكس.

## إجراء التراجع

1. محرّك التدقيق لا يُتراجَع عنه بحذف؛ التراجع يعني تصحيحاً بقيد جديد.
2. عند خلل في المصبّ: التحويل إلى مصبّ احتياطي مع الحفاظ على الترتيب.
3. التحقق من اكتمال السلسلة بعد الاستعادة.
4. تسجيل الحادث نفسه كقيد تدقيق.

## درجة الجاهزية الحالية

**الدرجة: 76 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `governance/audit/audit_schema.md`، `governance/audit/audit_retention.md`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## Purpose

The Audit Engine writes an immutable record of every decision, approval, and execution in the Governance layer. Its single goal: to later prove to a customer what the AI did, why, and who approved it. The log is append-only; no edit, no delete.

## Components

- Audit sink `dealix/trust/audit.py` — the abstract `AuditSink` interface with `append()` and `recent()`; Phase 0–1 uses `InMemoryAuditSink` with a structured-log mirror, and Phase 2 uses `PostgresSink` with an append-only table and monthly partitioning.
- Audit entry contract `dealix/contracts/audit_log.py` — the `AuditEntry` structure.
- Evidence packs in `dealix/trust/` — link each decision to its outputs and evidence.

## What is recorded

Every `AuditEntry` holds at least: id, tenant, actor (agent or human), action, A/R/S classification, policy decision, approval reference if any, timestamp, and the `decision_id` for correlation.

## Tamper-evidence mechanism

1. The log is append-only; the interface exposes no edit or delete.
2. In Phase 2 the audit table is append-only at the database level and monthly-partitioned.
3. Each entry carries the prior entry's id within the same tenant to form a verifiable chain.
4. Any chain gap is raised as an immediate governance incident.

## Readiness checklist

- [x] Every policy decision and every approval state change is written as an audit entry.
- [x] The log is append-only; no edit or delete interface.
- [x] Every entry is bound to a tenant and a `decision_id`.
- [ ] Append-only, partitioned `PostgresSink` table (planned for Phase 2).
- [ ] Periodic verification of chain integrity (planned).

## Metrics

- Audit entry coverage: 100% of S2/S3 actions and approvals.
- Entry write time: under 20 ms.
- Detected chain gaps: zero (target).

## Observability hooks

- Every entry mirrored to structured logs via `core/logging.py`.
- Write tracing via `dealix/observability/otel.py`.
- Alert on a failed entry write or a detected chain gap.

## Governance rules

- No raw personal identifier is written into an entry (`no_pii_in_logs` rule); pseudonymous identifiers are used.
- Entry retention is seven years per `dealix/registers/compliance_saudi.yaml`.
- Deleting an audit entry is strictly forbidden; correction is done by a new compensating entry.

## Rollback procedure

1. The Audit Engine is not rolled back by deletion; rollback means correction by a new entry.
2. On a sink fault: fail over to a backup sink while preserving ordering.
3. Verify chain completeness after recovery.
4. Record the incident itself as an audit entry.

## Current readiness score

**Score: 76 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `governance/audit/audit_schema.md`, `governance/audit/audit_retention.md`.
