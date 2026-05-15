# Versions — Observability

## Traces

- `versions.tag`
- `versions.rollback`

## Metrics

See `metrics.md` — every KPI there must be exported as a metric.

## Logs

Structured logs MUST include `tenant_id`, `principal_id`, `trace_id`, and
`action`. No log line crosses a tenant boundary.

## Alerts

| Condition | Severity | Routes to |
|-----------|----------|-----------|
| KPI breaches its target threshold | warning | owning team |
| Risk-tier-medium failure | page | on-call (`docs/ON_CALL.md`) |

Backed by: `auto_client_acquisition/observability_v10`, `auto_client_acquisition/auditability_os`.
