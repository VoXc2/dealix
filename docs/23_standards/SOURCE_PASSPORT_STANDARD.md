# Source Passport Standard

## معيار جواز سفر المصدر

> Open Standard, version 1.0. Implementations may use any storage backend, any schema validator, and any language. The fields, decision rules, and failure modes defined here are the normative part.

A Source Passport is the identity document of a piece of data. Before any byte enters an AI-assisted workflow, that byte must trace back to a Source Passport that declares who owns it, what it may be used for, whether it contains personal information, and how long it may be retained.

This standard formalizes the Source Passport so that any organization can adopt it. The Dealix reference implementation lives in `auto_client_acquisition/data_os/source_passport.py`, but the spec is independent of that implementation.

---

## 1. Required fields — الحقول المطلوبة

Every Source Passport must declare the following fields. Missing or null values for any required field invalidate the passport.

| Field | Type | Allowed values | Meaning |
|-------|------|----------------|---------|
| `source_id` | string | non-empty, unique within tenant | Stable identifier for the source. |
| `source_type` | enum | `client_upload`, `crm_export`, `manual_entry`, `partner_data`, `licensed_dataset` | How the data entered the system. |
| `owner` | enum | `client`, `dealix`, `partner` | Who holds the legal/business ownership of the data. |
| `allowed_use` | tuple of strings | from a closed vocabulary (e.g. `analysis`, `enrichment`, `drafting`, `targeting`, `reporting`) | The set of purposes the source may serve. Anything outside this tuple is denied. |
| `contains_pii` | boolean | `true` / `false` | Whether the source contains personally identifiable information about a natural person. |
| `sensitivity` | enum | `low`, `medium`, `high` | Business sensitivity, independent of PII flag. |
| `ai_access_allowed` | boolean | `true` / `false` | Whether AI components may read this source at all. |
| `external_use_allowed` | boolean | `true` / `false` | Whether derivatives of this source may leave the organization. |
| `retention_policy` | enum | `project_duration`, `retainer_duration`, `anonymize_after_close`, `delete_after_close` | The lifecycle rule that applies when the project closes. |

Optional but recommended: `created_at`, `created_by`, `legal_basis`, `dpa_reference`, `tags`.

---

## 2. JSON schema — مخطط JSON

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SourcePassport",
  "type": "object",
  "required": [
    "source_id",
    "source_type",
    "owner",
    "allowed_use",
    "contains_pii",
    "sensitivity",
    "ai_access_allowed",
    "external_use_allowed",
    "retention_policy"
  ],
  "properties": {
    "source_id": { "type": "string", "minLength": 1 },
    "source_type": {
      "type": "string",
      "enum": ["client_upload", "crm_export", "manual_entry", "partner_data", "licensed_dataset"]
    },
    "owner": { "type": "string", "enum": ["client", "dealix", "partner"] },
    "allowed_use": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "uniqueItems": true
    },
    "contains_pii": { "type": "boolean" },
    "sensitivity": { "type": "string", "enum": ["low", "medium", "high"] },
    "ai_access_allowed": { "type": "boolean" },
    "external_use_allowed": { "type": "boolean" },
    "retention_policy": {
      "type": "string",
      "enum": ["project_duration", "retainer_duration", "anonymize_after_close", "delete_after_close"]
    }
  }
}
```

---

## 3. Decision matrix — مصفوفة القرار

When a workflow tries to use a source, the runtime asks a small set of questions. The answers compose using the rule "hardest restriction wins": if any rule yields `BLOCK`, the outcome is `BLOCK`; otherwise the strictest non-allow decision applies.

| Condition | Decision |
|-----------|----------|
| No passport found for the data | `BLOCK` |
| Passport exists but fails schema validation | `BLOCK` |
| `ai_access_allowed == false` and the action is an AI read | `BLOCK` |
| Action's purpose is not in `allowed_use` | `BLOCK` |
| `contains_pii == true` and the action targets an external surface | `REQUIRE_APPROVAL` |
| `sensitivity == "high"` and the action targets an external surface | `REQUIRE_APPROVAL` |
| `external_use_allowed == false` and the action exports a derivative | `BLOCK` |
| All passes | `ALLOW` |

In plain language: a source with no passport is treated as if it does not exist. A source with PII that is heading outside the organization always requires explicit approval, even if every other rule says allow. A source marked high-sensitivity is treated like PII for external use, regardless of whether names are present.

بلغة بسيطة: لا جواز يعني الرفض. أي مصدر يحوي بيانات شخصية ويتجه إلى الخارج يستلزم موافقة صريحة. أي مصدر عالي الحساسية يُعامَل خارجياً معاملة بيانات شخصية.

---

## 4. Retention behavior — سلوك الاحتفاظ

Retention is enforced at project close, not at file upload. The four policies translate into concrete actions:

- `project_duration` — the source is retained while the project is open; deleted within fourteen days of close.
- `retainer_duration` — the source is retained while a paid retainer is active; deleted within thirty days of retainer end.
- `anonymize_after_close` — at project close, identifying fields are stripped and a non-reversible hash replaces them; the anonymized form may be retained for analytics.
- `delete_after_close` — at project close, the source and all derivatives are deleted within seven days.

A workflow may not extend retention by copying the data into a different store. Retention policy travels with the `source_id`, not with the storage location.

---

## 5. Reference implementation — التنفيذ المرجعي

The Dealix reference implementation is `auto_client_acquisition/data_os/source_passport.py`. It exposes:

- A `SourcePassport` dataclass that mirrors the schema above.
- A validator that returns the same decision matrix outcomes.
- Helper constructors for the five `source_type` values.

The reference implementation is one possible realization. Any equivalent implementation that produces the same decisions on the same inputs is conformant.

---

## 6. Failure modes — أنماط الفشل

A conformant runtime must refuse to proceed in the following cases:

1. The data has no `source_id`.
2. The `source_id` resolves to no passport.
3. The passport fails validation.
4. The action's purpose is outside `allowed_use`.
5. The action would export a source with `external_use_allowed = false`.

Each refusal must emit a recorded event for audit. Silent refusal is not conformant.

---

## 7. Cross-references — مراجع متقاطعة

- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) — the umbrella standard.
- [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md) — how passport decisions compose with output-side governance.
- [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md) — every passport used in a project is listed in Proof Pack section four.

---

## 8. Disclaimer — إخلاء مسؤولية

This standard is descriptive. It does not by itself create lawful basis for processing personal data under the Saudi Personal Data Protection Law or any other regulation. Adopting organizations remain responsible for obtaining consent, signing DPAs, and complying with all applicable laws.

هذا المعيار توصيفي ولا يُنشئ بذاته أساساً نظامياً لمعالجة البيانات الشخصية وفق نظام حماية البيانات الشخصية. الجهات المتبنّية مسؤولة عن الحصول على الموافقات وتوقيع الاتفاقيات المطلوبة.
