# Governance Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-GOV-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-GOV-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-GOV-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-GOV-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-GOV-050: release-period metric snapshot.
- E-GOV-051: threshold breach analysis where applicable.
