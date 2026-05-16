# Multi-Tenant Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-MTN-001 | Cache namespace collisions can expose one tenant data to another. | high | enforce policy checks and block on missing context | G-MTN-020 | T-MTN-020 |
| R-MTN-002 | Missing tenant filters in retrieval paths can leak records. | medium | release gating plus rollback rehearsal | G-MTN-021 | T-MTN-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-MTN-020: risk simulation logs.
- E-MTN-021: mitigation verification artifacts.
