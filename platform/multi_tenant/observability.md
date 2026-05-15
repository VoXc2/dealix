# Multi-Tenant Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Cross-tenant deny events, tenant filter coverage, cache key collision count.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-MTN-001 | error rate exceeds threshold | page on-call owner | G-MTN-030 |
| A-MTN-002 | missing trace correlation over threshold | create incident ticket | G-MTN-031 |
| A-MTN-003 | repeated policy or quality violations | enforce restricted mode | G-MTN-032 |

## Observability Evidence

- E-MTN-030: metric dashboard export for release window.
- E-MTN-031: sample correlated trace and log chain.
- E-MTN-032: alert firing and acknowledgement timeline.
