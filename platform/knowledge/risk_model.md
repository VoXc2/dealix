# Knowledge Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-KNW-001 | Low-quality retrieval can produce unsupported claims. | high | enforce policy checks and block on missing context | G-KNW-020 | T-KNW-020 |
| R-KNW-002 | Citation gaps reduce explainability for high-impact outputs. | medium | release gating plus rollback rehearsal | G-KNW-021 | T-KNW-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-KNW-020: risk simulation logs.
- E-KNW-021: mitigation verification artifacts.
