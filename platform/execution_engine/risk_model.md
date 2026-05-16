# Execution Engine Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-EXE-001 | Connector retries without idempotency can duplicate customer actions. | high | enforce policy checks and block on missing context | G-EXE-020 | T-EXE-020 |
| R-EXE-002 | Approval token misuse can execute blocked actions. | medium | release gating plus rollback rehearsal | G-EXE-021 | T-EXE-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-EXE-020: risk simulation logs.
- E-EXE-021: mitigation verification artifacts.
