# Identity Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Session validation latency, denied session count, claim mismatch count.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-IDN-001 | error rate exceeds threshold | page on-call owner | G-IDN-030 |
| A-IDN-002 | missing trace correlation over threshold | create incident ticket | G-IDN-031 |
| A-IDN-003 | repeated policy or quality violations | enforce restricted mode | G-IDN-032 |

## Observability Evidence

- E-IDN-030: metric dashboard export for release window.
- E-IDN-031: sample correlated trace and log chain.
- E-IDN-032: alert firing and acknowledgement timeline.

## Control Linkage (IDN)

- Gate ID: G-IDN-900
- Evidence ID: E-IDN-900
- Test ID: T-IDN-900

