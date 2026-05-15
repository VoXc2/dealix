# Executive Intelligence Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Brief generation timeliness, KPI freshness, decision confidence coverage.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-EXI-001 | error rate exceeds threshold | page on-call owner | G-EXI-030 |
| A-EXI-002 | missing trace correlation over threshold | create incident ticket | G-EXI-031 |
| A-EXI-003 | repeated policy or quality violations | enforce restricted mode | G-EXI-032 |

## Observability Evidence

- E-EXI-030: metric dashboard export for release window.
- E-EXI-031: sample correlated trace and log chain.
- E-EXI-032: alert firing and acknowledgement timeline.
