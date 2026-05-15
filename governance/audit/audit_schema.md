# العربية

**Owner:** قائد الخصوصية والثقة (Privacy & Trust Plane Lead).

## مخطط قيد التدقيق

تصف هذه الوثيقة بنية قيد التدقيق `AuditEntry` المعرّفة في `dealix/contracts/audit_log.py` والمكتوبة عبر `dealix/trust/audit.py`. القيد إلحاقي فقط؛ لا تعديل ولا حذف.

### الحقول

| الحقل | الوصف | إلزامي |
|---|---|---|
| `id` | مُعرّف القيد الفريد | نعم |
| `tenant_id` | المستأجر المالك للقيد | نعم |
| `decision_id` | مُعرّف القرار للربط بين القيود | نعم |
| `actor` | الفاعل: وكيل أو إنسان (هوية مستعارة للأفراد) | نعم |
| `action` | نوع الإجراء (قيمة من `action.value`) | نعم |
| `classification` | تصنيف A/R/S للإجراء | نعم |
| `policy_decision` | `allow` / `require_approval` / `block` | نعم |
| `approval_ref` | مرجع طلب الموافقة إن وُجد | لا |
| `reason` | سبب القرار أو القاعدة المُفعَّلة | نعم |
| `timestamp` | الطابع الزمني UTC | نعم |
| `prev_entry_id` | مُعرّف القيد السابق ضمن المستأجر (سلسلة) | نعم |

### المخطط (JSON)

```json
{
  "id": "string",
  "tenant_id": "string",
  "decision_id": "string",
  "actor": {"type": "agent | human", "ref": "string (pseudonymous)"},
  "action": "string",
  "classification": {"approval": "A0-A3", "reversibility": "R0-R3", "sensitivity": "S0-S3"},
  "policy_decision": "allow | require_approval | block",
  "approval_ref": "string | null",
  "reason": "string",
  "timestamp": "ISO-8601 UTC",
  "prev_entry_id": "string | null"
}
```

### قواعد المخطط

- لا حقل يحوي بيانات شخصية خام؛ `actor.ref` معرّف مستعار (قاعدة `no_pii_in_logs`).
- `prev_entry_id` يربط القيود في سلسلة قابلة للتحقق ضمن كل مستأجر.
- القيد غير قابل للتعديل؛ التصحيح بقيد جديد معاكس يشير لـ `decision_id` نفسه.

### قائمة الجاهزية

- [x] كل الحقول الإلزامية مُنفَّذة في `AuditEntry`.
- [x] لا حقل يحوي بيانات شخصية خام.
- [x] `prev_entry_id` يشكّل سلسلة قابلة للتحقق.
- [ ] التحقق الآلي من اكتمال السلسلة (مُخطَّط).

### المقاييس

- نسبة القيود المكتملة الحقول الإلزامية: 100%.
- عدد فجوات السلسلة المكتشفة: صفر (هدف).

### الحوكمة والتراجع

- تعديل المخطط يتطلب موافقة قائد الخصوصية والثقة وقيد تدقيق.
- لا يُتراجَع عن قيد بحذف؛ التراجع تصحيح بقيد جديد.

انظر أيضاً: `governance/audit/audit_retention.md`، `platform/governance/audit_engine.md`.

---

# English

**Owner:** Privacy & Trust Plane Lead.

## Audit Entry Schema

This document describes the `AuditEntry` structure defined in `dealix/contracts/audit_log.py` and written via `dealix/trust/audit.py`. The entry is append-only; no edit, no delete.

### Fields

| Field | Description | Required |
|---|---|---|
| `id` | Unique entry id | Yes |
| `tenant_id` | The tenant owning the entry | Yes |
| `decision_id` | Decision id correlating entries | Yes |
| `actor` | Actor: agent or human (pseudonymous identity for individuals) | Yes |
| `action` | Action type (a value from `action.value`) | Yes |
| `classification` | A/R/S classification of the action | Yes |
| `policy_decision` | `allow` / `require_approval` / `block` | Yes |
| `approval_ref` | Approval request reference if any | No |
| `reason` | Reason for the decision or the rule that fired | Yes |
| `timestamp` | UTC timestamp | Yes |
| `prev_entry_id` | Prior entry id within the tenant (chain) | Yes |

### Schema (JSON)

```json
{
  "id": "string",
  "tenant_id": "string",
  "decision_id": "string",
  "actor": {"type": "agent | human", "ref": "string (pseudonymous)"},
  "action": "string",
  "classification": {"approval": "A0-A3", "reversibility": "R0-R3", "sensitivity": "S0-S3"},
  "policy_decision": "allow | require_approval | block",
  "approval_ref": "string | null",
  "reason": "string",
  "timestamp": "ISO-8601 UTC",
  "prev_entry_id": "string | null"
}
```

### Schema rules

- No field holds raw personal data; `actor.ref` is a pseudonymous identifier (`no_pii_in_logs` rule).
- `prev_entry_id` links entries into a verifiable chain within each tenant.
- The entry is immutable; correction is by a new compensating entry referencing the same `decision_id`.

### Readiness checklist

- [x] All required fields are implemented in `AuditEntry`.
- [x] No field holds raw personal data.
- [x] `prev_entry_id` forms a verifiable chain.
- [ ] Automatic chain-completeness verification (planned).

### Metrics

- Share of entries with all required fields complete: 100%.
- Detected chain gaps: zero (target).

### Governance and rollback

- Changing the schema requires the Privacy & Trust lead's approval and an audit entry.
- An entry is not rolled back by deletion; rollback is correction by a new entry.

See also: `governance/audit/audit_retention.md`, `platform/governance/audit_engine.md`.
