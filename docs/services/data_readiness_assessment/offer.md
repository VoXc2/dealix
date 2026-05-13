# Data Readiness Assessment — Offer — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
Most failed AI projects fail because the data was not ready. This
short, paid engagement lets Dealix find that out before the client pays
for an AI Sprint. The assessment plugs into the Capability Operating
Model from `docs/company/CAPABILITY_OPERATING_MODEL.md`, respects the
data handling commitments in `docs/DPA_DEALIX_FULL.md` and
`docs/DATA_RETENTION_POLICY.md`, and is referenced as a prerequisite by
high-data services in `docs/BEAST_LEVEL_ARCHITECTURE.md`.

## Promise
Assess whether your data is ready for AI workflows and identify gaps
before any implementation work begins. Walk out with a readiness
score, the top gaps, and a recommended next Sprint.

## Who It Is For
- Companies that have heard the words "we have lots of data" but have
  never seen it audited.
- Companies that tried an AI project and the model ended up hallucinating
  or producing bad outputs because of bad inputs.
- Companies that need to satisfy a board, regulator, or partner that
  the data foundation is ready.

## Deliverables
- **Data Source Inventory** — every source mapped with owner, format,
  and access path.
- **Data Quality Score** — composite score per the scoring model in
  `scoring_model.md`.
- **PII / Sensitivity Flags** — fields flagged for risk and required
  handling.
- **Integration Gaps** — what is missing to connect sources for an AI
  workflow.
- **Readiness Report** — see `report_template.md`.
- **Recommended Next Sprint** — from the upsell mapping in
  `upsell.md`.

## Engagement Shape
- **Duration:** 7 to 10 working days.
- **Team:** 1 Data Lead + 1 analyst.
- **Format:** kickoff, data request, 2 working sessions, readout.
- **Inputs requested:** see `data_request.md`.

## Decision the Client Walks Away With
- **Ready (≥ 80):** start the recommended AI Sprint.
- **Almost ready (60 – 79):** light Data Cleanup engagement first.
- **Not ready (< 60):** Data Cleanup or process work before any AI
  Sprint.

## Pricing
Pricing follows `docs/OFFER_LADDER_AND_PRICING.md`. The assessment is
sold as a fixed-fee service. If the client commits to the recommended
next Sprint within 30 days, the fee may be credited as per the offer
ladder rules.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client data samples, interviews | Source inventory, quality score, gap report, recommendation | Data Lead | Per engagement |
| Readiness output | Sprint scope, governance memo if needed | Founder, Delivery Lead | Per engagement |
| Outcome of recommended Sprint | Validation of readiness score accuracy | Delivery Lead | Per delivery |

## Metrics
- **Readiness-to-Sprint Conversion** — share of assessments that lead
  to a paid Sprint within 30 days (target ≥ 50%).
- **Readiness Score Accuracy** — share of "Ready" assessments where the
  follow-on Sprint succeeds (target ≥ 85%).
- **Time-to-Report** — calendar days from kickoff to readiness report
  (target ≤ 10 days).
- **Gap Closure Rate** — share of identified gaps closed within 60 days
  by the client or by Dealix (target ≥ 60%).

## Related
- `docs/DPA_DEALIX_FULL.md` — data processing commitments governing
  this work.
- `docs/DATA_RETENTION_POLICY.md` — retention rules respected during
  sampling.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention schedule.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture that consumes
  ready data.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
