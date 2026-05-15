# Dealix Scoring System (Gates -> Evidence -> Tests)

## Scoring Equation

Each layer score is calculated from gate scores:

`Layer Score = Sum(Gate Weight x Gate Score) / Sum(Gate Weight)`

Where each gate score is:

`Gate Score = 100 x (Passed Tests / Total Mandatory Tests)`

## Mandatory Hierarchy

1. **Layer**: strategic capability (e.g., Governance).
2. **Gate**: control objective inside the layer.
3. **Evidence**: artifact proving gate implementation.
4. **Test**: executable verification with deterministic result.

No gate can score above 0 if no evidence exists.  
No evidence is valid without an executable test.

## ID Conventions

- Layer IDs: `L-<NAME>` (example: `L-GOV`)
- Gate IDs: `G-<LAYER>-NNN` (example: `G-GOV-003`)
- Evidence IDs: `E-<LAYER>-NNN` (example: `E-GOV-011`)
- Test IDs: `T-<LAYER>-NNN` (example: `T-GOV-021`)

## Gate Status Model

| Status | Condition |
|---|---|
| PASS | All mandatory tests pass |
| FIX | Some tests fail but no critical control broken |
| BLOCKED | Critical control missing or bypass detected |

Critical controls (always BLOCKED on failure):
- Tenant isolation
- RBAC enforcement
- High-risk approval gate
- Traceability/audit continuity
- Rollback readiness

## Weighting Model (v1)

| Layer | Weight |
|---|---:|
| Foundation | 10 |
| Agent Runtime | 8 |
| Workflow Engine | 8 |
| Knowledge / Memory | 8 |
| Governance | 12 |
| Execution / Integrations | 8 |
| Observability | 10 |
| Evals | 8 |
| Delivery Playbooks | 7 |
| Executive Intelligence | 6 |
| Continuous Evolution | 7 |
| Cross-Layer Validation | 16 |

Cross-layer gets the highest weight because isolated layer success is insufficient.

## Test Evidence Requirements

Each test entry must include:
- `test_id`
- `gate_id`
- `release_version`
- `environment`
- `timestamp_utc`
- `result` (`pass`/`fail`)
- `artifact_link` (log, report, dashboard screenshot, or trace export)

## Release Gate Policy

A release may proceed to production only if:

1. No critical control test fails.
2. Weighted global score >= 85.
3. `Cross-Layer Validation` score >= 90.
4. Governance eval threshold is met.
5. Rollback drill freshness <= 30 days.

If any rule fails, release is `BLOCKED`.
