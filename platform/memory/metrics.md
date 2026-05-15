# Memory Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-MEM-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-MEM-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-MEM-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-MEM-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-MEM-050: release-period metric snapshot.
- E-MEM-051: threshold breach analysis where applicable.
