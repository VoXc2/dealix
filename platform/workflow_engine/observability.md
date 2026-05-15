# Workflow Engine Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Workflow success rate, retry saturation, compensation invocation rate.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-WFE-001 | error rate exceeds threshold | page on-call owner | G-WFE-030 |
| A-WFE-002 | missing trace correlation over threshold | create incident ticket | G-WFE-031 |
| A-WFE-003 | repeated policy or quality violations | enforce restricted mode | G-WFE-032 |

## Observability Evidence

- E-WFE-030: metric dashboard export for release window.
- E-WFE-031: sample correlated trace and log chain.
- E-WFE-032: alert firing and acknowledgement timeline.
