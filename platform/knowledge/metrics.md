# Knowledge Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-KNW-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-KNW-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-KNW-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-KNW-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-KNW-050: release-period metric snapshot.
- E-KNW-051: threshold breach analysis where applicable.
