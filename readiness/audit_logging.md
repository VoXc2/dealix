# Audit Logging (As-Built) — سجلّ التدقيق

**EN.** The audit trail **as it exists in the repo today**. Audit logging is
implemented and tied to PDPL Article 18. This file records what is there and the
residual gaps. Audit logging is a control that backs Layer 7 (Governance) and is
a Release 1 acceptance criterion.

**AR.** سجلّ التدقيق **كما هو موجود في المستودع اليوم**. التدقيق مُنفَّذ ومرتبط
بالمادة 18 من نظام حماية البيانات (PDPL). تسجّل هذه الوثيقة ما هو قائم والفجوات
المتبقية. التدقيق ضابط يدعم الطبقة 7 (الحوكمة) وهو معيار قبول للإصدار 1.

Owner: Governance Lead.

---

## 1. As-built — ما هو منفّذ فعلاً

### Record
`db/models.py` → `AuditLogRecord` (`audit_logs` table). Every sensitive read
(contact PII, deal financials) and every write (create / update / delete)
produces one row.

| Field | Purpose |
|-------|---------|
| `tenant_id` | Scopes the entry to a tenant (indexed). |
| `user_id` | Who acted (nullable, indexed). |
| `action` | e.g. `contact.read`, `lead.create`, `contact.delete`. |
| `entity_type` / `entity_id` | What was touched. |
| `ip_address`, `user_agent`, `request_id` | Request context. |
| `diff` | Before/after JSON for writes. |
| `status` | `ok` / `denied` / `error`. |
| `created_at` | Timestamp (indexed). |

Indexes: `ix_audit_tenant_created` (`tenant_id`, `created_at`),
`ix_audit_entity` (`entity_type`, `entity_id`).

### Middleware
`api/middleware/http_stack.py` → `AuditLogMiddleware`, registered in
`api/main.py` (`app.add_middleware(AuditLogMiddleware)`).

### Export
`api/routers/audit_export.py` exposes audit retrieval. Related middleware
`api/middleware/bopla_redaction.py` redacts object properties (OWASP API3:2023
BOPLA).

### Tests
`tests/test_audit_export.py`, `tests/test_audit_correlation_id_v14.py`,
`tests/test_customer_experience_audit_integration.py`.

### Non-negotiable tie-in
`docs/00_foundation/NON_NEGOTIABLES.md` forbids **PII in logs**. The `diff`
field stores before/after state and **must** be redacted for PII-bearing
entities — see residual gaps.

---

## 2. Readiness checklist — قائمة التحقق

Release 1 acceptance: **every sensitive action produces an audit log.**

| # | Check | Evidence | State |
|---|-------|----------|-------|
| 1 | Audit record model exists with full context | `AuditLogRecord` | ✅ Met |
| 2 | Audit middleware on every request | `AuditLogMiddleware` in `main.py` | ✅ Met |
| 3 | Writes capture before/after diff | `AuditLogRecord.diff` | ✅ Met |
| 4 | Denied actions are logged (`status=denied`) | `status` field | ⚠️ Partial — field exists; deny-path coverage unproven |
| 5 | Audit entries are tenant-scoped | `tenant_id` indexed | ✅ Met |
| 6 | Audit log is exportable | `audit_export.py` | ✅ Met |
| 7 | No PII written to logs / `diff` | `bopla_redaction.py` | ⚠️ Partial — redaction on responses; **`diff` redaction unproven** |
| 8 | `pytest` covers audit emission | `test_audit_export.py` et al. | ✅ Met |
| 9 | Super-admin cross-tenant reads are audited | — | ⚠️ Partial — required by convention, not enforced |

---

## 3. Residual gaps — الفجوات المتبقية

1. **`diff` PII redaction.** The `diff` field stores before/after JSON, which can
   contain `contact_email`, `contact_phone`, names. Confirm a redaction pass runs
   before the `diff` is persisted; if not, this is a **hard fail** against the
   "no PII in logs" non-negotiable.
2. **Deny-path coverage.** `status` supports `denied`/`error`, but there is no
   evidence every rejected/failed sensitive action writes a row. Add explicit
   tests for the denied path.
3. **Super-admin enforcement.** Cross-tenant super-admin reads must be audited
   (see [`multi_tenancy.md`](multi_tenancy.md) gap 2) — currently convention only.
4. **Retention + tamper-evidence.** Define a retention window for `audit_logs`
   and decide whether append-only / hash-chained tamper-evidence is required for
   enterprise contracts.

Gap 1 is the priority — it can flip the layer to `BLOCKED` on a hard fail.

---

## ملخص بالعربية

سجلّ التدقيق منفّذ عبر `AuditLogRecord` ووسيط `AuditLogMiddleware` ومنفذ تصدير،
ويغطّي القراءات الحسّاسة والكتابات مع فروقات قبل/بعد. الفجوة الأهم: التأكد من
تنقيح حقل `diff` من بيانات PII قبل التخزين — وإلا فهو إخفاق قاطع ضد قاعدة «لا
PII في السجلّات». فجوات أخرى: تغطية مسار الرفض، وفرض تدقيق وصول المشرف الأعلى،
وتحديد مدة الاحتفاظ ومقاومة العبث.
