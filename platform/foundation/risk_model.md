# Foundation Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-FND-001 | Missing tenant context can leak records across customers. | high | enforce policy checks and block on missing context | G-FND-020 | T-FND-020 |
| R-FND-002 | Unverified rollback assets can extend incidents. | medium | release gating plus rollback rehearsal | G-FND-021 | T-FND-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-FND-020: risk simulation logs.
- E-FND-021: mitigation verification artifacts.
