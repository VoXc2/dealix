# Governance Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-GOV-001 | Policy bypass can allow unauthorized high-impact actions. | high | enforce policy checks and block on missing context | G-GOV-020 | T-GOV-020 |
| R-GOV-002 | Inconsistent risk scoring can create unreliable approvals. | medium | release gating plus rollback rehearsal | G-GOV-021 | T-GOV-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-GOV-020: risk simulation logs.
- E-GOV-021: mitigation verification artifacts.
