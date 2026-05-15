# Identity Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-IDN-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-IDN-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-IDN-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-IDN-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-IDN-050: release-period metric snapshot.
- E-IDN-051: threshold breach analysis where applicable.

## Control Linkage (IDN)

- Gate ID: G-IDN-900
- Evidence ID: E-IDN-900
- Test ID: T-IDN-900

