# Identity Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-IDN-001 | Stale sessions can allow actions after privilege removal. | high | enforce policy checks and block on missing context | G-IDN-020 | T-IDN-020 |
| R-IDN-002 | Incomplete identity attributes break downstream policy checks. | medium | release gating plus rollback rehearsal | G-IDN-021 | T-IDN-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-IDN-020: risk simulation logs.
- E-IDN-021: mitigation verification artifacts.
