# Agent Runtime Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-ART-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-ART-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-ART-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-ART-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-ART-050: release-period metric snapshot.
- E-ART-051: threshold breach analysis where applicable.

## Control Linkage (ART)

- Gate ID: G-ART-900
- Evidence ID: E-ART-900
- Test ID: T-ART-900

