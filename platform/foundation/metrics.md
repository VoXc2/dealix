# Foundation Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-FND-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-FND-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-FND-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-FND-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-FND-050: release-period metric snapshot.
- E-FND-051: threshold breach analysis where applicable.

## Control Linkage (FND)

- Gate ID: G-FND-900
- Evidence ID: E-FND-900
- Test ID: T-FND-900

