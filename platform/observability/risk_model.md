# Observability Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-OBS-001 | Missing trace propagation hides where policy or quality failed. | high | enforce policy checks and block on missing context | G-OBS-020 | T-OBS-020 |
| R-OBS-002 | Noisy alerts can mask critical incidents. | medium | release gating plus rollback rehearsal | G-OBS-021 | T-OBS-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-OBS-020: risk simulation logs.
- E-OBS-021: mitigation verification artifacts.
