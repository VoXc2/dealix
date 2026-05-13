# Data Readiness Assessment — Report Template — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [report_template_AR.md](./report_template_AR.md)

## Context
The deliverable here is the only artefact the client takes home from a
Data Readiness Assessment. A vague or inconsistent deliverable destroys
the upsell path. This template fixes the structure, headings, and
required content so that every deliverable looks the same and earns
trust. It honours the data handling rules in
`docs/DPA_DEALIX_FULL.md`, `docs/DATA_RETENTION_POLICY.md`, and the
PDPL retention schedule in `docs/ops/PDPL_RETENTION_POLICY.md`, and
slots into the architecture in `docs/BEAST_LEVEL_ARCHITECTURE.md`.

## Deliverable Structure
The deliverable has six fixed sections, in this order.

### 1. Executive Summary
- Half-page Arabic-and-English summary.
- Composite readiness score and recommendation band.
- Recommended next service in one sentence.

### 2. Scoring Breakdown
- Table of the seven dimensions with raw and weighted scores from
  `scoring_model.md`.
- One paragraph per dimension citing evidence.
- A clearly marked composite total.

### 3. Top Gaps
- The three to five highest-impact gaps blocking AI use.
- Each gap has: description, affected sources, severity (Low / Medium
  / High), and effort estimate.
- Each gap references one or more `data_source` records from
  `docs/product/ADVANCED_DATA_MODEL.md`.

### 4. Recommendations
- Recommended next Sprint or readiness service, drawn from `upsell.md`.
- Reasoning in three to five sentences.
- Alternatives if the client prefers a different path, with trade-offs.

### 5. Next Sprint
- A one-page scope sketch of the recommended Sprint.
- Capability uplift target (current and target level per
  `docs/company/CAPABILITY_MATURITY_MODEL.md`).
- Expected timeline, indicative price from
  `docs/OFFER_LADDER_AND_PRICING.md`, and required client inputs.

### 6. Risks
- Top three risks if the recommendation is not followed.
- Governance risks (PII, claims, external action) flagged per
  `docs/governance/RUNTIME_GOVERNANCE.md`.
- Operational risks (owner availability, integration cost).

## Style and Format
- Arabic and English versions delivered together; identical structure.
- Tables, not paragraphs, for any list of more than three items.
- No fictional case studies; only redacted references to the client's
  own data.
- Every claim in the deliverable must be traceable to an evidence
  artefact in the assessment workspace.

## QA Gate Before Delivery
- The deliverable is reviewed against this template by a second Dealix
  reviewer.
- Required: composite score present, evidence cited for each
  dimension, at least one named recommendation, governance risks
  reviewed.
- Deliverables missing any of the above must not be sent to the
  client.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Scoring outputs, gap analysis, recommendations | Final readiness deliverable | Data Lead | Per engagement |
| QA review | Approval to deliver | Founder, QA Lead | Per engagement |
| Delivered deliverable | Client signature on next-step decision | Founder, Client | Per engagement |

## Metrics
- **Template Conformance** — share of deliverables matching the
  six-section structure (target = 100%).
- **Evidence Citation Rate** — share of dimension paragraphs citing at
  least one artefact (target = 100%).
- **Decision Rate at Readout** — share of clients making a decision in
  the readout meeting (target ≥ 70%).
- **Bilingual Delivery** — share of deliverables produced in Arabic
  and English (target = 100%).

## Related
- `docs/DPA_DEALIX_FULL.md` — data rules during this work.
- `docs/DATA_RETENTION_POLICY.md` — retention on deliverables.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture for storing
  artefacts.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
