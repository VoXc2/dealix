# Foundation Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Context validation pass rate, rollback drill freshness, audit write latency.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-FND-001 | error rate exceeds threshold | page on-call owner | G-FND-030 |
| A-FND-002 | missing trace correlation over threshold | create incident ticket | G-FND-031 |
| A-FND-003 | repeated policy or quality violations | enforce restricted mode | G-FND-032 |

## Observability Evidence

- E-FND-030: metric dashboard export for release window.
- E-FND-031: sample correlated trace and log chain.
- E-FND-032: alert firing and acknowledgement timeline.

## Control Linkage (FND)

- Gate ID: G-FND-900
- Evidence ID: E-FND-900
- Test ID: T-FND-900

