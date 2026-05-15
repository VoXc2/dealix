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

## Trace storage bridge (in-process)

Contract-compliant dict events can be appended to the observability v10 in-memory trace buffer via
`auto_client_acquisition.observability_v10.contract_trace_hook.record_contract_trace_event`, which runs
`validate_observability_event` before constructing a `TraceRecordV10` (payload fields live under
`redacted_payload`). This complements external OpenTelemetry exporters by keeping a deterministic,
code-level enforcement path for CI and local verification.

## Consumption policy

- Executive dashboards consume only contract-compliant events.
- Incident retrospectives must include trace extraction from contract-compliant stores.
- Any contract change requires versioning and migration notes.
