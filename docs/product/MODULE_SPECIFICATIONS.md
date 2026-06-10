# Product Modules — Exact Responsibilities

Bindings: Data OS, Governance OS, Revenue OS, Reporting OS, Delivery OS, plus Customer/Operations/Knowledge and `llm_gateway` / `ai_workforce` as expanded spine.

---

## `data_os`

**Purpose:** Make data usable and safe.

**Responsibilities:**

- parse CSV/XLSX
- validate schema
- detect missing fields
- detect duplicates
- detect PII
- calculate data readiness
- produce import preview

**Functions (logical API):**

```text
parse_dataset(file)
validate_schema(records, schema)
detect_duplicates(records)
detect_pii(records)
score_data_quality(records)
generate_import_preview(records)
```

---

## `governance_os`

**Purpose:** Make every action safe, approved, and auditable.

**Responsibilities:**

- check allowed use
- classify action risk
- detect forbidden behavior
- redact PII
- require approval
- write audit event

**Functions:**

```text
check_policy(context)
classify_action(action)
detect_forbidden_claims(text)
redact_pii(text)
requires_approval(action)
write_audit_event(event)
```

---

## `revenue_os`

**Purpose:** Turn data into revenue action.

**Responsibilities:**

- define ICP
- score accounts
- explain scores
- generate draft pack
- create mini pipeline
- recommend next action

**Scoring formula (reference):**

```text
final_priority_score =
  fit_score * 0.30
+ urgency_score * 0.20
+ value_score * 0.20
+ data_quality_score * 0.15
+ compliance_score * 0.15
```

**Account score schema:**

```json
{
  "account_id": "ACC-001",
  "company_name": "Example Co",
  "final_priority_score": 84,
  "fit_score": 90,
  "urgency_score": 75,
  "value_score": 80,
  "data_quality_score": 85,
  "compliance_score": 90,
  "reasons_ar": [],
  "reasons_en": [],
  "risks": [],
  "recommended_next_action": "manual_research_then_email_draft"
}
```

---

## `reporting_os`

**Purpose:** Turn work into executive proof.

**Responsibilities:**

- generate reports
- generate proof pack
- summarize value
- list risks
- recommend next step

**Functions:**

```text
generate_executive_report(project)
generate_proof_pack(project)
summarize_value(metrics)
recommend_next_offer(project)
```

---

## `delivery_os`

**Purpose:** Make service delivery repeatable.

**Responsibilities:**

- intake
- scope
- checklist
- QA
- handoff
- renewal recommendation

**QA result schema:**

```json
{
  "business_score": 88,
  "data_score": 82,
  "ai_output_score": 86,
  "arabic_quality_score": 90,
  "compliance_score": 100,
  "reusability_score": 80,
  "upsell_score": 85,
  "overall_score": 87,
  "pass": true,
  "required_fixes": []
}
```

See [`../quality/QUALITY_STANDARD_V1.md`](../quality/QUALITY_STANDARD_V1.md).
