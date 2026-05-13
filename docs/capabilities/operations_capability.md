# Operations Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Head of Operations
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [operations_capability_AR.md](./operations_capability_AR.md)

## Context

The Operations capability exists to remove manual steps, time, and
errors from a client's internal workflows. It is the most common
"AI Quick Win" entry point and the foundation for cross-team
automation. It is anchored to `docs/V14_FOUNDER_DAILY_OPS.md` and the
daily operating loop in `docs/ops/DAILY_OPERATING_LOOP.md`. Maturity
is scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Reduce manual steps, time, and errors across recurring workflows.

## Typical Problems

- Manual data entry across tools.
- Repeated workflows with no automation.
- Scattered tools and broken handoffs.

## Required Inputs

- Workflow maps (current state, who does what).
- Source files (forms, exports, sheets).
- Target systems (CRM, accounting, inbox).

## AI Functions

- Extract data from documents and messages.
- Transform between schemas and formats.
- Classify items by rule or model.
- Summarize long content for handoff.
- Route work to the correct system or owner.

## Governance Controls

- Owner named per workflow.
- Approval gate for any external send or write.
- Audit log of every run, input, and output.
- Rollback procedure documented.

## KPIs

- Hours saved — measured per workflow per week.
- Steps reduced — count before vs after.
- Error rate — % of runs that fail QA.

## Services

- AI Quick Win — single-workflow sprint.
- Workflow Automation Sprint — multi-workflow build.
- Monthly AI Ops — recurring operating retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Workflow map | Designed automation | Delivery | Per sprint |
| Source files | Extracted / transformed data | Delivery | Per run |
| Approved output | Write to target system | Client | Per run |
| Run logs | Hours saved report | Delivery | Weekly |

## Metrics

- Hours saved and steps reduced (see KPIs).
- Error rate per workflow.
- Workflow uptime — % of scheduled runs that complete.

## Related

- `docs/V14_FOUNDER_DAILY_OPS.md` — daily ops reference.
- `docs/ops/DAILY_OPERATING_LOOP.md` — operating loop the capability supports.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — runtime that hosts ops workflows.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
