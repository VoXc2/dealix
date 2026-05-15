# Observability Layer Observability

## Required Signals

- Traces: all critical operations include trace and span identifiers.
- Logs: structured logs include tenant, actor, layer, and decision code.
- Metrics: Trace coverage, alert precision, mean time to detect, mean time to recover.

## Alert Rules

| Alert ID | Trigger | Action | Related Gate |
|---|---|---|---|
| A-OBS-001 | error rate exceeds threshold | page on-call owner | G-OBS-030 |
| A-OBS-002 | missing trace correlation over threshold | create incident ticket | G-OBS-031 |
| A-OBS-003 | repeated policy or quality violations | enforce restricted mode | G-OBS-032 |

## Observability Evidence

- E-OBS-030: metric dashboard export for release window.
- E-OBS-031: sample correlated trace and log chain.
- E-OBS-032: alert firing and acknowledgement timeline.

## Control Linkage (OBS)

- Gate ID: G-OBS-900
- Evidence ID: E-OBS-900
- Test ID: T-OBS-900

