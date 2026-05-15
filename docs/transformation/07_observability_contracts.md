# 07 — Observability Contracts and Trace Discipline

## Objective

Enforce standardized telemetry contracts for run/action/tool events so operational and commercial decisions rely on complete and consistent signals.

## Contract domains

- Workflow run lifecycle
- Approval lifecycle
- Runtime safety lifecycle
- Value event lifecycle
- Self-evolving lifecycle

## Required contract fields

- `tenant_id`
- `correlation_id`
- `run_id`
- `event_type`
- `source_module`
- `actor`
- `occurred_at`
- `payload_schema_version`

## Validation rules

- Events missing required fields are invalid.
- Unknown event types fail contract checks.
- Timestamp ordering checks required for lifecycle chains.
- Value lifecycle events must include source evidence references for measured metrics.

## Consumption policy

- Executive dashboards consume only contract-compliant events.
- Incident retrospectives must include trace extraction from contract-compliant stores.
- Any contract change requires versioning and migration notes.
