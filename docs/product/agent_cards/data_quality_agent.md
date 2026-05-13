# Data Quality Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_quality_agent_AR.md](./data_quality_agent_AR.md)

## Context
Most Dealix engagements start with messy data. The Data Quality Agent is
the first inspector in the workflow: it classifies issues, scores
datasets, and recommends fixes — without ever touching the source.
This agent enforces the data-readiness layer described in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and the AI-workforce contract in
`docs/product/AI_WORKFORCE_OPERATING_MODEL.md`.

## Agent Card

- **Role:** Classifies and scores data quality issues across uploaded
  datasets so the engagement can begin from a measurable baseline.
- **Allowed Inputs:** raw CSV/JSON datasets (client-approved), schema
  definitions, sensitivity labels.
- **Allowed Outputs:** quality score, issue list, recommended fixes,
  baseline snapshot.
- **Forbidden:** modifying client data; exporting raw PII; writing to
  client systems; sending notifications.
- **Required Checks:**
  - input dataset has provenance and sensitivity label;
  - PII fields detected and flagged;
  - score follows the published rubric;
  - recommended fixes are reversible.
- **Output Schema:** `DataQualityReport { dataset_id, score, issues[],
  recommended_fixes[], pii_flags[], baseline_snapshot_ref }`.
- **Approval:** human review before client delivery.

## Issue taxonomy

- Missing fields / empty rows.
- Duplicates and near-duplicates.
- Type mismatches and format drift.
- Stale records (age beyond threshold).
- Sensitive fields lacking masking.
- Inconsistent identifiers across sources.

## Scoring rubric (summary)

| Dimension | Weight | Notes |
|---|---|---|
| Completeness | 25% | required fields populated |
| Uniqueness | 20% | dedupe ratio |
| Validity | 20% | type and format conformance |
| Freshness | 15% | within engagement window |
| Sensitivity | 10% | PII masked/labeled |
| Consistency | 10% | cross-source agreement |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Raw dataset + schema | DataQualityReport | Delivery owner | Per engagement |
| Issue list | Fix plan | Delivery owner | Per engagement |
| Score snapshot | Value Ledger baseline | Delivery owner | Per engagement |

## Metrics
- Time-to-Baseline — minutes from dataset upload to first score.
- Score Lift — average score uplift from baseline to delivery.
- False-Flag Rate — % of flagged issues dismissed by reviewer.
- PII Detection Recall — % of known PII fields correctly flagged.

## Related
- `docs/AI_STACK_DECISIONS.md` — model selection for this agent
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval suite reference
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governing rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
