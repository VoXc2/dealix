# Data Readiness Standard — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DATA_READINESS_STANDARD_AR.md](./DATA_READINESS_STANDARD_AR.md)

## Context
No AI implementation at Dealix starts until data readiness is known.
This standard is the gate that protects clients from building AI
workflows on top of unfit data. It is referenced by
`docs/DEALIX_OPERATING_CONSTITUTION.md`, by
`docs/BEAST_LEVEL_ARCHITECTURE.md` for the architecture impact, by
`docs/AI_STACK_DECISIONS.md` for the model and pipeline implications,
and by `docs/services/data_readiness_assessment/offer.md` for the
productized service. The standard is enforced through the runtime
governance layer; a low readiness score must produce either a cleanup
service or a no-go decision.

## Purpose
Make every dataset entering a Dealix workflow scored, labeled, and
auditable before any AI runs against it.

## Score Components
The Data Readiness Score (DRS) is a weighted aggregate of seven
components. Weights sum to 100.

| Component | Weight |
|---|---:|
| Source coverage | 20 |
| Completeness | 15 |
| Consistency | 15 |
| Freshness | 10 |
| Deduplication | 10 |
| PII handling | 15 |
| Business mapping | 15 |

Each component is scored 0-100. The DRS is the weighted sum divided by
100. Detailed formulas live in
`docs/data/DATA_QUALITY_SCORE.md`.

## Readiness Levels
| Range | Label | Decision |
|---|---|---|
| 85-100 | Ready | AI workflow may proceed |
| 70-84 | Usable with review | Proceed with documented risk notes |
| 50-69 | Needs cleanup | Run a Data Cleanup service first |
| < 50 | Not ready | No AI implementation; remediation only |

A dataset cannot be promoted to a higher level without re-scoring.

## Required Fields For Business Account Data
The following fields are mandatory for any business account dataset
used in revenue, customer, or operations workflows.

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
If any of `email`, `phone`, person name, or other private identifiers
exist in a dataset, all four conditions below must hold before the
dataset can be scored above 70.

1. `source_type` is known and documented.
2. `allowed_use` is defined and recorded.
3. `relationship_status` is defined per record.
4. No external action may be taken without an explicit approval per
   the Approval Matrix (`docs/governance/APPROVAL_MATRIX.md`).

PDPL obligations are defined in
`docs/governance/PDPL_DATA_RULES.md` and the binding agreement is
`docs/DPA_DEALIX_FULL.md`.

## Sample Output Schema
The Data Readiness service produces the following JSON record per
dataset. It is logged in the AI Run Ledger and surfaced in the proof
pack.

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

## Decision Rules
- If `overall_data_readiness >= 85` → `proceed`.
- If `70 <= overall_data_readiness < 85` → `proceed_with_review` with
  named risks.
- If `50 <= overall_data_readiness < 70` → `cleanup_required` and
  trigger the Data Cleanup service.
- If `overall_data_readiness < 50` → `not_ready`; no AI work.

A dataset with PII and an undefined `allowed_use` is automatically
downgraded to `not_ready` regardless of the numeric score.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Raw client dataset | Scored readiness record | Data lead | Per dataset |
| Schema definitions | Validation report | Data lead | Per dataset |
| PII inventory | PII risk score and redaction map | Governance lead | Per dataset |
| Decision record | Cleanup scope or proceed signal | Delivery lead | Per dataset |

## Metrics
- **Pre-AI readiness compliance** — share of AI runs that have a DRS
  record older than 30 days. Target: 100%.
- **Cleanup conversion rate** — share of `cleanup_required` datasets
  that produce a paid Cleanup engagement. Target: ≥ 50%.
- **PII override count** — datasets that proceeded with PII despite
  missing lawful basis. Target: 0.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture context for the
  data pipeline.
- `docs/AI_STACK_DECISIONS.md` — model and pipeline decisions.
- `docs/DPA_DEALIX_FULL.md` — binding data processing agreement.
- `docs/services/data_readiness_assessment/offer.md` — productized
  service.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
