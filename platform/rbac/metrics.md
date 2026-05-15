# RBAC Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-RBA-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-RBA-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-RBA-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-RBA-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-RBA-050: release-period metric snapshot.
- E-RBA-051: threshold breach analysis where applicable.

## Control Linkage (RBA)

- Gate ID: G-RBA-900
- Evidence ID: E-RBA-900
- Test ID: T-RBA-900

