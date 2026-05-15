# Observability Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-OBS-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-OBS-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-OBS-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-OBS-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-OBS-050: release-period metric snapshot.
- E-OBS-051: threshold breach analysis where applicable.

## Control Linkage (OBS)

- Gate ID: G-OBS-900
- Evidence ID: E-OBS-900
- Test ID: T-OBS-900

