# Data Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Head of Data
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_capability_AR.md](./data_capability_AR.md)

## Context

The Data capability gets a client's data ready for AI and for
decisions. It is the gate every other capability depends on: messy
data = unsafe AI. It is anchored to `docs/BEAST_LEVEL_ARCHITECTURE.md`,
`docs/DPA_DEALIX_FULL.md`, and `docs/DATA_RETENTION_POLICY.md`.
Maturity is scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Get data ready for AI and for decisions — known fields, known sources,
known owners.

## Typical Problems

- Duplicates and inconsistent records.
- Missing fields.
- Scattered sources with no canonical owner.
- No retention or PII policy applied.

## Required Inputs

- Raw datasets (CSV, exports, sheets).
- Schemas (or absence thereof, flagged).
- Sensitivity tags.

## AI Functions

- Quality scoring per record and per field.
- Deduplication.
- Classification by record type.
- Enrichment proposal with cited source.

## Governance Controls

- PII handling per `docs/DPA_DEALIX_FULL.md`.
- Source registry entry per dataset.
- Retention rule per dataset per `docs/DATA_RETENTION_POLICY.md`.

## KPIs

- Quality score before/after — composite 0–100.
- Gap closure rate — % of flagged gaps closed per sprint.

## Services

- Data Readiness Assessment — paid assessment.
- Data Cleanup — sprint to fix issues.
- Data OS — recurring data operating retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Raw datasets | Quality score + gap list | Delivery | Per sprint |
| Approved fixes | Cleaned dataset | Delivery | Per sprint |
| Source list | Source registry entries | Delivery | Per dataset |
| Retention rule | Applied retention | Delivery | Monthly |

## Metrics

- Quality score lift (see KPIs).
- Gap closure rate.
- PII-flagged records resolved.

## Related

- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture that hosts the data.
- `docs/DPA_DEALIX_FULL.md` — data processing agreement and PII rules.
- `docs/DATA_RETENTION_POLICY.md` — retention policy applied per dataset.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
