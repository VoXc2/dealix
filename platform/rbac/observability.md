# RBAC Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Allow/deny ratio, permission drift alerts, authorization p95 latency.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-RBA-001 | error rate exceeds threshold | page on-call owner | G-RBA-030 |
| A-RBA-002 | missing trace correlation over threshold | create incident ticket | G-RBA-031 |
| A-RBA-003 | repeated policy or quality violations | enforce restricted mode | G-RBA-032 |

## Observability Evidence

- E-RBA-030: metric dashboard export for release window.
- E-RBA-031: sample correlated trace and log chain.
- E-RBA-032: alert firing and acknowledgement timeline.

## Control Linkage (RBA)

- Gate ID: G-RBA-900
- Evidence ID: E-RBA-900
- Test ID: T-RBA-900

