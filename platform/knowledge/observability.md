# Knowledge Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Citation coverage rate, retrieval precision at k, stale-source detection count.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-KNW-001 | error rate exceeds threshold | page on-call owner | G-KNW-030 |
| A-KNW-002 | missing trace correlation over threshold | create incident ticket | G-KNW-031 |
| A-KNW-003 | repeated policy or quality violations | enforce restricted mode | G-KNW-032 |

## Observability Evidence

- E-KNW-030: metric dashboard export for release window.
- E-KNW-031: sample correlated trace and log chain.
- E-KNW-032: alert firing and acknowledgement timeline.
