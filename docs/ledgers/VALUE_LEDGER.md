# Value Ledger — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [VALUE_LEDGER_AR.md](./VALUE_LEDGER_AR.md)

## Context
The Value Ledger is the canonical record of every value claim Dealix has
produced. It is the receipt layer that converts engagement work into
provable business outcomes and feeds the dashboards described in
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md` and the finance view in
`docs/FINANCE_DASHBOARD.md`. Without ledger entries, proof packs are
isolated artifacts. With ledger entries, Dealix can speak about value at
the company level — by capability, sector, service, and cohort. The ledger
implements the rule defined in `docs/company/VALUE_REALIZATION_SYSTEM.md`
and the constitutional commitment in `docs/DEALIX_OPERATING_CONSTITUTION.md`
that proof packs must exist for billable work.

## Ledger schema

| Field | Type | Description |
|---|---|---|
| ID | string | `V-NNN` unique sequential identifier |
| Client | string | client alias or anonymized handle |
| Service | string | service name from the service ladder |
| Value Type | enum | Revenue / Time / Quality / Risk / Knowledge |
| Metric | string | exact name of the measured KPI |
| Baseline | string | pre-state value (or "unknown" with reason) |
| Result | string | post-state value |
| Evidence | string | proof pack path or asset id |
| Next Value | string | the next-value opportunity proposed |
| Owner | string | Dealix delivery owner |
| Date | date | date the claim was signed off |

## Starting entries

| ID | Client | Service | Value Type | Metric | Baseline | Result | Evidence | Next Value |
|---|---|---|---|---|---|---|---|---|
| V-001 | Client A | Lead Intelligence | Revenue | ranked accounts | unknown | top 50 | proof pack | Pilot Conversion |
| V-002 | Client B | Quick Win | Time | manual hours | 6/week | 2/week | workflow report | Monthly AI Ops |

> The ledger above is the seed format. New rows are appended per
> engagement and must reference an evidence artifact.

## Rule

> Any proof pack without a Value Ledger entry = **incomplete**.

A proof pack is the technical artifact (data, screenshots, reports). The
ledger is the business artifact. Both must exist before an engagement is
marked done.

## Aggregations published

- **By Value Type** — pipeline of Revenue/Time/Quality/Risk/Knowledge claims.
- **By Capability** — value rolled up to capabilities from
  `docs/company/CAPABILITY_VALUE_MAP.md`.
- **By Service** — value by service line from
  `docs/COMPANY_SERVICE_LADDER.md`.
- **By Sector** — concentration risk and sector-fit signal.
- **By Cohort** — quarterly cohort retention/expansion view.

## Process

1. Delivery owner opens a candidate row at engagement kickoff (baseline).
2. Owner updates the row at delivery (result + evidence).
3. CSM logs the next-value opportunity and target close date.
4. CSM presents the next-value offer within 14 days.
5. Head of Delivery validates the row weekly and signs the monthly digest.

## Anti-patterns

- Backfilling rows months later from memory.
- Marking a row complete without an evidence link.
- "Baseline = unknown" without a written justification.
- Multiple rows per engagement when one composite metric is appropriate.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement kickoff metadata | Candidate ledger row | Delivery owner | Per engagement |
| Proof pack | Result + evidence link | Delivery owner | Per engagement |
| Ledger snapshot | Monthly aggregation report | Head of Delivery | Monthly |
| Cohort snapshot | Quarterly retention/expansion view | CEO | Quarterly |

## Metrics
- Ledger Coverage — % of engagements with a signed-off entry.
- Median Time-to-Entry — days between kickoff and first row update.
- Evidence Completeness — % of rows with a valid evidence link.
- Next-Value Pull-Through — % of next-value rows converted to revenue.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard consuming the ledger
- `docs/FINANCE_DASHBOARD.md` — finance view linking value to revenue
- `docs/EXECUTIVE_DECISION_PACK.md` — exec pack referencing ledger summaries
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — proof-pack requirement
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
