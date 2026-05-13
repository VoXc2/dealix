# Data Request — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
This is the standard request used to receive client data into a
Dealix engagement. It is filled during the Discover stage of the
Delivery Standard (`docs/delivery/DELIVERY_STANDARD.md`) and is the
input to the Diagnose stage. It pairs with the Data Readiness Standard
(`docs/data/DATA_READINESS_STANDARD.md`), the Data Schema Library
(`docs/data/DATA_SCHEMA_LIBRARY.md`), and the PDPL rules
(`docs/governance/PDPL_DATA_RULES.md`).

## How To Use
List every data asset the client will provide. Each row must be filled
completely. Mark unknown values as `unknown`; do not leave blank. The
Data Lead reviews this document before any data is accepted into the
Dealix workspace.

## Asset Inventory
| # | Asset name | Owner | Format | Access method | Sensitivity | Allowed use | Expected delivery date |
|---|---|---|---|---|---|---|---|
| 1 | `<text>` | `<text>` | `<csv/xlsx/api/db>` | `<text>` | `<low/medium/high>` | `<research/outreach/service_delivery/none>` | `<date>` |
| 2 | `<text>` | `<text>` | `<csv/xlsx/api/db>` | `<text>` | `<low/medium/high>` | `<research/outreach/service_delivery/none>` | `<date>` |
| 3 | `<text>` | `<text>` | `<csv/xlsx/api/db>` | `<text>` | `<low/medium/high>` | `<research/outreach/service_delivery/none>` | `<date>` |

## PII Declaration
For each asset, declare PII presence and lawful basis.

| Asset | PII fields | Lawful basis (LB-01..LB-05) | Consent record ID | Retention |
|---|---|---|---|---|
| `<text>` | `<text>` | `<text>` | `<text>` | `<text>` |

A `none` value in `Allowed use` blocks ingestion until reviewed.

## Access And Security
- Preferred transfer mode: `<secure share | encrypted email | API>`.
- Encryption at rest: required.
- Encryption in transit: required.
- Workspace destination: `<Dealix workspace ID>`.
- Access reviewers: `<text>`.
- Access expiry: 90 days unless extended.

## Schema Conformance
- Target schema from `docs/data/DATA_SCHEMA_LIBRARY.md`: `<text>`.
- Known field mapping notes: `<text>`.
- Schema version: `<text>`.

## Risk And Issue Log
- Known data quality issues: `<text>`.
- Known consent gaps: `<text>`.
- Known cross-border concerns: `<text>`.
- Mitigation owner: `<text>`.

## Sign-Off
- Client data owner: `<name, date>`.
- Dealix data lead: `<name, date>`.
- Dealix governance lead (for PII): `<name, date>`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Intake form | Data request draft | Delivery lead | Per engagement |
| Asset inventory | DRS computation input | Data lead | Per engagement |
| PII declaration | Lawful basis record | Governance lead | Per engagement |
| Signed request | Ingestion clearance | Data lead | Per engagement |

## Metrics
- **Asset inventory completeness** — share of rows with all required
  cells filled. Target: 100%.
- **PII declaration coverage** — share of PII-bearing assets with
  lawful basis recorded. Target: 100%.
- **Time to first ingestion** — business days from signed data
  request to first ingestion. Target: ≤ 3.

## Related
- `docs/data/DATA_READINESS_STANDARD.md` — readiness standard.
- `docs/data/DATA_SCHEMA_LIBRARY.md` — schema library.
- `docs/governance/PDPL_DATA_RULES.md` — PDPL rules.
- `docs/templates/intake_form.md` — intake form sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
