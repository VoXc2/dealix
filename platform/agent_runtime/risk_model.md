# Agent Runtime Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-ART-001 | Prompt or tool injection can bypass expected controls. | high | enforce policy checks and block on missing context | G-ART-020 | T-ART-020 |
| R-ART-002 | Unpinned agent versions can cause unstable behavior. | medium | release gating plus rollback rehearsal | G-ART-021 | T-ART-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-ART-020: risk simulation logs.
- E-ART-021: mitigation verification artifacts.
