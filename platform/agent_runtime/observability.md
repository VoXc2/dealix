# Agent Runtime Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Unauthorized tool attempt count, approval pause rate, runtime error budget.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-ART-001 | error rate exceeds threshold | page on-call owner | G-ART-030 |
| A-ART-002 | missing trace correlation over threshold | create incident ticket | G-ART-031 |
| A-ART-003 | repeated policy or quality violations | enforce restricted mode | G-ART-032 |

## Observability Evidence

- E-ART-030: metric dashboard export for release window.
- E-ART-031: sample correlated trace and log chain.
- E-ART-032: alert firing and acknowledgement timeline.
