# Data Readiness Assessment — Scope — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scope_AR.md](./scope_AR.md)

## Context
A Readiness Assessment that drifts into actual cleanup or integration
work bleeds margin and confuses the buyer about what comes next. This
scope file sets the inclusions, exclusions, and boundaries for the
Data Readiness Assessment service. It complements the offer in
`offer.md`, sits inside the Capability Operating Model
(`docs/company/CAPABILITY_OPERATING_MODEL.md`), and operates under
the data handling rules of `docs/DPA_DEALIX_FULL.md` and
`docs/DATA_RETENTION_POLICY.md`.

## Inclusions
- **Source mapping.** Identify each data source, owner, format, access
  path, and refresh cadence.
- **Sampling.** Take controlled samples (no full extracts) sufficient
  to score quality and risk.
- **Quality scoring.** Apply the scoring model in `scoring_model.md`
  to produce a composite readiness score.
- **Gap report.** List the top gaps blocking AI use, with severity and
  effort estimates.
- **Recommendation.** Recommend the next Sprint or readiness service,
  using `upsell.md`.

## Exclusions
- **Data cleanup.** Fixing duplicates, missing fields, or schema drift
  is a separate Data Cleanup service.
- **ETL build.** Building extract/transform/load pipelines is out of
  scope.
- **Integration work.** Connecting CRM, ERP, or other systems is out
  of scope.
- **AI model build.** No prompts, models, or workflows are built in
  this engagement.
- **Long-term monitoring.** Ongoing data quality monitoring is sold
  separately.

## Boundaries
- **Time.** 7 to 10 working days.
- **Sample size.** Up to 3 sources at headline level; deeper coverage
  by upgrade.
- **Access.** Read-only sampling under the DPA; no production writes.
- **Confidentiality.** Findings shared only with named client
  stakeholders.
- **Output.** One report, one recommendation, one optional governance
  memo.

## Change Requests
- A change request that asks Dealix to start fixing data turns the
  engagement into a Data Cleanup; this is sold separately and adds
  scope, time, and price.
- A change request that asks for deeper coverage adds days at the
  agreed daily rate from `docs/OFFER_LADDER_AND_PRICING.md`.
- Any change must be confirmed in writing before work continues.

## Dependencies on Client
- Access to the data request items in `data_request.md`.
- A named client owner for each in-scope source.
- A 60-minute kickoff and a 90-minute readout with decision makers.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client data samples and contacts | Source map, quality score, gap report | Data Lead | Per engagement |
| Scope confirmation | Signed scope statement | Founder, Client | Per engagement |
| Change requests | Revised scope, revised price | Founder | As raised |

## Metrics
- **Scope Conformance** — share of engagements delivered within signed
  scope (target ≥ 90%).
- **Out-of-Scope Conversions** — count of in-flight change requests
  converted to a new paid service (track, not bound).
- **Readiness Score Reliability** — share of scores not revised after
  delivery (target ≥ 90%).
- **Client Satisfaction (Scope)** — share of clients rating scope
  clarity ≥ 4/5 (target ≥ 90%).

## Related
- `docs/DPA_DEALIX_FULL.md` — data processing rules followed.
- `docs/DATA_RETENTION_POLICY.md` — retention applied to samples.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture consuming the
  readiness output.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
