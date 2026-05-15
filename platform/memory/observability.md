# Memory Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Memory append success rate, recall accuracy score, stale-memory conflict rate.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-MEM-001 | error rate exceeds threshold | page on-call owner | G-MEM-030 |
| A-MEM-002 | missing trace correlation over threshold | create incident ticket | G-MEM-031 |
| A-MEM-003 | repeated policy or quality violations | enforce restricted mode | G-MEM-032 |

## Observability Evidence

- E-MEM-030: metric dashboard export for release window.
- E-MEM-031: sample correlated trace and log chain.
- E-MEM-032: alert firing and acknowledgement timeline.

## Control Linkage (MEM)

- Gate ID: G-MEM-900
- Evidence ID: E-MEM-900
- Test ID: T-MEM-900

