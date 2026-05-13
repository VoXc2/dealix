# Data Productization — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Data
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DATA_PRODUCTIZATION_AR.md](./DATA_PRODUCTIZATION_AR.md)

## Context
Every recurring engagement creates a dataset. Without explicit schemas,
those datasets remain ad-hoc and AI quality collapses. This file defines
the canonical "data products" Dealix maintains, their schemas, and the
discipline that keeps them clean. It feeds the technical architecture in
`docs/BEAST_LEVEL_ARCHITECTURE.md` and the reliability work in
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`.

## Principle

> Any service without a clear schema becomes chaos.

A data product is owned, versioned, documented, accessible by approved
users, and reused across engagements.

## Core data products

### Lead Dataset
- `company_name` (string)
- `city` (string)
- `sector` (enum)
- `source` (string)
- `relationship_status` (enum: none / consented / existing)
- `notes` (text)

### Support Dataset
- `message` (text)
- `channel` (enum: email / whatsapp / web / phone)
- `customer_type` (enum)
- `timestamp` (datetime)
- `category` (enum)
- `resolution_status` (enum: open / resolved / escalated)

### Document Dataset
- `title` (string)
- `owner` (string)
- `last_updated` (datetime)
- `sensitivity` (enum: public / internal / restricted)
- `source_type` (enum: file / wiki / drive / crm)
- `allowed_users` (list)

## Discipline

- Each dataset has a published schema and a versioned definition.
- Each schema change ships via PR with migration notes.
- Each dataset has a steward.
- Datasets carry sensitivity labels that the agents honor.
- Stale data is flagged automatically.

## Anti-patterns

- Per-client schemas that drift forever.
- Free-text fields where enums should exist.
- Sensitivity unset by default.
- Recurring engagements without a productized dataset.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Raw client inputs | Productized dataset | Data steward | Per engagement |
| Schema change request | New version + migration | Head of Data | Per change |
| Sensitivity labels | Agent access filter | Knowledge Agent | Per query |
| Data quality telemetry | Quality dashboard | Head of Data | Continuous |

## Metrics
- Productization Coverage — % of recurring engagements on canonical schema.
- Schema Drift — schema changes per dataset per quarter.
- Stewardship Coverage — % of datasets with named steward.
- Sensitivity Compliance — % of records labeled correctly.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture context
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability work
- `docs/AI_STACK_DECISIONS.md` — stack decisions
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — data posture
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
