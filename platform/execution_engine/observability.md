# Execution Engine Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Connector success rate, duplicate action prevention count, external error rate.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-EXE-001 | error rate exceeds threshold | page on-call owner | G-EXE-030 |
| A-EXE-002 | missing trace correlation over threshold | create incident ticket | G-EXE-031 |
| A-EXE-003 | repeated policy or quality violations | enforce restricted mode | G-EXE-032 |

## Observability Evidence

- E-EXE-030: metric dashboard export for release window.
- E-EXE-031: sample correlated trace and log chain.
- E-EXE-032: alert firing and acknowledgement timeline.

## Control Linkage (EXE)

- Gate ID: G-EXE-900
- Evidence ID: E-EXE-900
- Test ID: T-EXE-900

