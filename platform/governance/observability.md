# Governance Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Policy deny rate, approval SLA, governance bypass attempt count.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-GOV-001 | error rate exceeds threshold | page on-call owner | G-GOV-030 |
| A-GOV-002 | missing trace correlation over threshold | create incident ticket | G-GOV-031 |
| A-GOV-003 | repeated policy or quality violations | enforce restricted mode | G-GOV-032 |

## Observability Evidence

- E-GOV-030: metric dashboard export for release window.
- E-GOV-031: sample correlated trace and log chain.
- E-GOV-032: alert firing and acknowledgement timeline.

## Control Linkage (GOV)

- Gate ID: G-GOV-900
- Evidence ID: E-GOV-900
- Test ID: T-GOV-900

