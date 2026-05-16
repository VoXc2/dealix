# Integrations Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Connector latency, payload validation failures, credential expiry incidents.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-INT-001 | error rate exceeds threshold | page on-call owner | G-INT-030 |
| A-INT-002 | missing trace correlation over threshold | create incident ticket | G-INT-031 |
| A-INT-003 | repeated policy or quality violations | enforce restricted mode | G-INT-032 |

## Observability Evidence

- E-INT-030: metric dashboard export for release window.
- E-INT-031: sample correlated trace and log chain.
- E-INT-032: alert firing and acknowledgement timeline.
