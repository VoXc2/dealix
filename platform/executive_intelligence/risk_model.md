# Executive Intelligence Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-EXI-001 | Unverified summaries can mislead commercial decisions. | high | enforce policy checks and block on missing context | G-EXI-020 | T-EXI-020 |
| R-EXI-002 | Metric lag can hide negative trend changes. | medium | release gating plus rollback rehearsal | G-EXI-021 | T-EXI-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-EXI-020: risk simulation logs.
- E-EXI-021: mitigation verification artifacts.
