# Data Readiness Standard

## Purpose

No AI implementation starts until **data readiness** is known and recorded. Organizational failure modes (leadership, data discipline, governance, operating model) dominate “model-only” fixes; readiness is therefore a **gate**, not an afterthought.

Poor-quality or ungoverned data produces unsafe or misleading AI outputs—readiness and quality scoring are prerequisite, not optional polish.

## Score Components

| Component | Weight |
|---|---:|
| Source coverage | 20 |
| Completeness | 15 |
| Consistency | 15 |
| Freshness | 10 |
| Deduplication | 10 |
| PII handling | 15 |
| Business mapping | 15 |

## Readiness Levels

| Score | Status | Decision |
|---:|---|---|
| 85–100 | Ready | AI workflow can proceed |
| 70–84 | Usable with review | proceed with risk notes |
| 50–69 | Needs cleanup | do Data Cleanup first |
| <50 | Not ready | no AI implementation |

## Required Fields for Business Account Data

- `company_name`
- `sector`
- `city`
- `source_type`
- `allowed_use`
- `relationship_status`
- `notes`

## Optional Fields

- `website`
- `contact_role`
- `email`
- `phone`
- `estimated_size`
- `last_interaction_date`

## PII Handling

If email, phone, person name, or private identifiers exist:

- source must be known
- `allowed_use` must be defined
- `relationship_status` must be defined
- no external action without approval

---

## Data quality output schema (reference)

```json
{
  "dataset_id": "DS-001",
  "records_total": 500,
  "records_valid": 420,
  "records_invalid": 80,
  "duplicates_found": 46,
  "pii_fields_detected": ["email", "phone"],
  "source_coverage_score": 90,
  "completeness_score": 78,
  "consistency_score": 82,
  "freshness_score": 65,
  "pii_risk_score": 40,
  "overall_data_readiness": 76,
  "decision": "usable_with_review",
  "required_actions": [
    "review phone number lawful basis",
    "fill missing sector for 55 records"
  ]
}
```

Implementation touchpoints: Data OS · [`../services/data_readiness_assessment/`](../services/data_readiness_assessment/) · [`../governance/PDPL_DATA_RULES.md`](../governance/PDPL_DATA_RULES.md).
