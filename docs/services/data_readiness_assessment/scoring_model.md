# Data Readiness Assessment — Scoring Model — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scoring_model_AR.md](./scoring_model_AR.md)

## Context
Without a written scoring model, a "readiness score" is a feeling
dressed up as a number. This file is the exact, defensible scoring
model used in every Data Readiness Assessment. It produces a 100-point
composite that drives the recommendation in `report_template.md` and
the upsell in `upsell.md`. It operates inside the Capability Operating
Model in `docs/company/CAPABILITY_OPERATING_MODEL.md` and honours the
data handling rules in `docs/DPA_DEALIX_FULL.md` and
`docs/DATA_RETENTION_POLICY.md`.

## Composite Weighting
Total = 100 points. The composite is the sum of seven weighted
dimensions:

| Dimension | Weight | What we check |
|---|---:|---|
| Source coverage | 20 | Are all relevant sources mapped and accessible? |
| Completeness | 20 | Are required fields populated for in-scope records? |
| Consistency | 15 | Are field values consistent across sources and time? |
| Freshness | 10 | How recently was the data updated? |
| PII handling | 15 | Is personal data classified, redacted, and routed safely? |
| Access clarity | 10 | Are owners, permissions, and access paths documented? |
| Business mapping | 10 | Do fields map to the business meanings AI will use? |

## Scoring Rubric (per Dimension)
Each dimension is scored 0–100 then weighted. The rubric is the same
for each:

- **0–20** Absent or unusable.
- **21–40** Present but with major issues.
- **41–60** Usable with caveats and remediation.
- **61–80** Mostly ready; minor gaps remain.
- **81–100** Ready as-is.

## Aggregation and Decision Bands
- **Composite ≥ 80** — Ready. Start the recommended AI Sprint.
- **Composite 60 – 79** — Almost ready. Light Data Cleanup first.
- **Composite < 60** — Not ready. Data Cleanup or process work before
  any AI Sprint.

Any dimension scoring below 40 forces the recommendation down one band
regardless of the composite — a single critical dimension can block a
service.

## Worked Example
| Dimension | Raw | Weighted |
|---|---:|---:|
| Source coverage | 70 | 14 |
| Completeness | 60 | 12 |
| Consistency | 50 | 7.5 |
| Freshness | 80 | 8 |
| PII handling | 90 | 13.5 |
| Access clarity | 70 | 7 |
| Business mapping | 60 | 6 |
| **Composite** | — | **68** |

This client lands in the **Almost ready** band; recommended next step
is a light Data Cleanup before the AI Sprint.

## Evidence Requirements
Each dimension score must cite at least one artefact:

- A sampled file or report.
- A screenshot of the source.
- An interview note from a named owner.
- A linked record in `docs/product/ADVANCED_DATA_MODEL.md` (e.g. a
  `data_source` entry).

Scores without evidence are not allowed.

## Drift and Recalibration
- The model is reviewed quarterly against actual Sprint outcomes.
- If "Ready" Sprints fail more than 15% of the time, dimension weights
  are recalibrated.
- All changes are versioned and noted in the change log.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sampled data, owner interviews | Per-dimension scores, composite | Data Lead | Per engagement |
| Composite | Recommendation band, Sprint recommendation | Founder | Per engagement |
| Outcomes of recommended Sprints | Weight recalibration | Data Lead | Quarterly |

## Metrics
- **Score Reliability** — share of composite scores that hold after
  delivery (target ≥ 90%).
- **Critical Dimension Detection** — share of failing Sprints where the
  cause was a sub-40 dimension flagged in advance (target ≥ 85%).
- **Recalibration Cadence** — quarterly recalibrations completed on
  schedule (target = 4 per year).
- **Evidence Coverage** — share of dimension scores with at least one
  artefact (target = 100%).

## Related
- `docs/DPA_DEALIX_FULL.md` — data processing rules followed.
- `docs/DATA_RETENTION_POLICY.md` — retention on sampled data.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture consuming readiness
  evidence.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
