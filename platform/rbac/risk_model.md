# RBAC Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-RBA-001 | Permission drift can grant unintended tool access. | high | enforce policy checks and block on missing context | G-RBA-020 | T-RBA-020 |
| R-RBA-002 | Silent deny reasons create operator ambiguity. | medium | release gating plus rollback rehearsal | G-RBA-021 | T-RBA-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-RBA-020: risk simulation logs.
- E-RBA-021: mitigation verification artifacts.
