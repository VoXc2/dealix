# Workflow Engine Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-WFE-001 | Invalid transition paths can skip required governance steps. | high | enforce policy checks and block on missing context | G-WFE-020 | T-WFE-020 |
| R-WFE-002 | Non-idempotent retries can duplicate external side effects. | medium | release gating plus rollback rehearsal | G-WFE-021 | T-WFE-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-WFE-020: risk simulation logs.
- E-WFE-021: mitigation verification artifacts.
