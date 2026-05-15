# Execution Engine Layer Metrics

## KPI Set

| Metric ID | Metric Name | Purpose | Threshold |
|---|---|---|---|
| M-EXE-001 | reliability_score | layer execution reliability | >= 0.99 |
| M-EXE-002 | control_compliance_score | gate and policy conformance | >= 0.98 |
| M-EXE-003 | latency_p95_seconds | tail latency under load | layer-defined |
| M-EXE-004 | change_failure_rate | release regression indicator | <= 0.05 |

## Measurement Cadence

- Operational metrics: continuous collection.
- Readiness metrics: reviewed per release gate.
- Executive metrics: summarized weekly.

## Metric Evidence

- E-EXE-050: release-period metric snapshot.
- E-EXE-051: threshold breach analysis where applicable.

## Control Linkage (EXE)

- Gate ID: G-EXE-900
- Evidence ID: E-EXE-900
- Test ID: T-EXE-900

