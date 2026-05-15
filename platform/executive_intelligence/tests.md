# Executive Intelligence Layer Tests

## Test Suite

| Test ID | Test Type | Purpose | Evidence ID |
|---|---|---|---|
| T-EXI-001 | contract | validate entry and output contract | E-EXI-001 |
| T-EXI-002 | determinism | verify stable behavior for identical input | E-EXI-002 |
| T-EXI-003 | telemetry | confirm trace and log fields | E-EXI-003 |
| T-EXI-010 | readiness smoke | validate release gate prerequisites | E-EXI-010 |
| T-EXI-040 | rollback drill | verify safe restoration path | E-EXI-040 |

## Execution Policy

- Run contract and determinism tests on each pull request touching this layer.
- Run rollback drills at least once per release cycle.
- Block promotion when any gate-linked test fails.

## Control Linkage (EXI)

- Gate ID: G-EXI-900
- Evidence ID: E-EXI-900
- Test ID: T-EXI-900

