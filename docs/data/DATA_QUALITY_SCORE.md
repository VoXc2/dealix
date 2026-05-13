# Data Quality Score — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DATA_QUALITY_SCORE_AR.md](./DATA_QUALITY_SCORE_AR.md)

## Context
This file is the operational guide for computing the Data Readiness
Score introduced in `docs/data/DATA_READINESS_STANDARD.md`. It defines
formulas, sample boundary cases, how to log results in the AI Run
Ledger, and how the score is consumed by `governance_check`. It pairs
with `docs/AI_OBSERVABILITY_AND_EVALS.md` and `docs/EVALS_RUNBOOK.md`
for the observability story, and with
`docs/services/data_readiness_assessment/scoring_model.md` for the
productized scoring service.

## Formula
The aggregate Data Readiness Score (DRS) is a weighted sum of seven
component scores. Weights are normative; do not deviate without an
amendment.

```
DRS = (
  source_coverage_score   * 0.20 +
  completeness_score      * 0.15 +
  consistency_score       * 0.15 +
  freshness_score         * 0.10 +
  dedup_score             * 0.10 +
  pii_handling_score      * 0.15 +
  business_mapping_score  * 0.15
)
```

Each component is on a 0-100 scale. The DRS is clamped to `[0, 100]`.

## Component Formulas
- `source_coverage_score = 100 * records_with_known_source / records_total`
- `completeness_score = 100 * required_fields_filled / required_fields_total`
- `consistency_score = 100 * records_passing_type_and_enum_checks / records_total`
- `freshness_score = 100 * records_updated_within_180_days / records_total`
- `dedup_score = 100 * (records_total - duplicate_records) / records_total`
- `pii_handling_score = base score 100, subtract per missing control`:
  - `−40` if any PII field has no `allowed_use`
  - `−30` if any PII field has no `source_type`
  - `−20` if any record has no `relationship_status`
  - `−10` if PII appears in any logged event
- `business_mapping_score = 100 * records_mapped_to_capability / records_total`

## Boundary Cases
| Case | Behavior |
|---|---|
| `records_total = 0` | DRS undefined; decision = `not_ready` |
| PII present but no `allowed_use` | Auto-downgrade to `not_ready` |
| Single component score below 30 | Flag as `bottleneck` and surface in proof pack |
| Freshness score below 40 | Trigger a refresh ticket before AI use |
| Schema not in library | Reject; route to schema fork remediation |

## Logging — AI Run Ledger
Every score computation writes a record to the AI Run Ledger. The
ledger record carries the score, the inputs, and the decision. The
schema:

```json
{
  "ai_run_id": "AIR-DRS-001",
  "agent": "DataReadinessAgent",
  "task": "score_dataset",
  "dataset_id": "DS-001",
  "drs_components": {
    "source_coverage_score": 90,
    "completeness_score": 78,
    "consistency_score": 82,
    "freshness_score": 65,
    "dedup_score": 70,
    "pii_handling_score": 40,
    "business_mapping_score": 80
  },
  "overall_data_readiness": 76,
  "decision": "usable_with_review",
  "bottlenecks": ["pii_handling_score"],
  "audit_event_id": "AUD-1042"
}
```

## Plumbing Into Governance Check
The `governance_check` runtime takes the DRS as an input and applies
the following routing:

- DRS ≥ 85 and no critical bottleneck → `ALLOW`
- DRS 70-84 → `ALLOW_WITH_REVIEW`
- DRS 50-69 → `BLOCK` with reason `cleanup_required`
- DRS < 50 → `BLOCK` with reason `not_ready`
- PII bottleneck → `REQUIRE_APPROVAL` regardless of numeric DRS

See `docs/governance/RUNTIME_GOVERNANCE.md` for the verb definitions.

## Re-scoring
Every dataset must be re-scored when:
- The dataset is updated.
- 30 days have passed since the last score.
- The schema version changes.
- A governance amendment changes weights or thresholds.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Dataset + schema | DRS record | Data lead | Per dataset |
| DRS record | Governance routing decision | Governance lead | Per run |
| Bottleneck list | Cleanup or remediation plan | Delivery lead | Per finding |

## Metrics
- **Score freshness** — share of in-use datasets with a DRS younger
  than 30 days. Target: 100%.
- **Bottleneck closure latency** — days from bottleneck detection to
  remediation. Target: ≤ 14 days.
- **Score drift** — quarter-over-quarter DRS change per dataset.
  Target: ≥ 0 (no regressions).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability for AI runs and
  scores.
- `docs/EVALS_RUNBOOK.md` — evaluation runbook for AI workflows.
- `docs/services/data_readiness_assessment/scoring_model.md` —
  productized scoring model.
- `docs/data/DATA_READINESS_STANDARD.md` — standard this guide
  operationalizes.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
