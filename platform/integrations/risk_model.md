# Integrations Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-INT-001 | API contract drift can silently corrupt external records. | high | enforce policy checks and block on missing context | G-INT-020 | T-INT-020 |
| R-INT-002 | Credential misuse can trigger actions outside intended tenant scope. | medium | release gating plus rollback rehearsal | G-INT-021 | T-INT-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-INT-020: risk simulation logs.
- E-INT-021: mitigation verification artifacts.
