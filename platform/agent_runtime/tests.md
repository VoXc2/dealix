# Agent Runtime Layer Tests

## Test Suite

| Test ID | Test Type | Purpose | Evidence ID |
|---|---|---|---|
| T-ART-001 | contract | validate entry and output contract | E-ART-001 |
| T-ART-002 | determinism | verify stable behavior for identical input | E-ART-002 |
| T-ART-003 | telemetry | confirm trace and log fields | E-ART-003 |
| T-ART-010 | readiness smoke | validate release gate prerequisites | E-ART-010 |
| T-ART-040 | rollback drill | verify safe restoration path | E-ART-040 |

## Execution Policy

- Run contract and determinism tests on each pull request touching this layer.
- Run rollback drills at least once per release cycle.
- Block promotion when any gate-linked test fails.
