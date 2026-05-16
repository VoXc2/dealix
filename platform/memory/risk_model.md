# Memory Layer Risk Model

## Risk Register

| Risk ID | Description | Severity | Mitigation | Gate ID | Test ID |
|---|---|---|---|---|---|
| R-MEM-001 | Unbounded memory writes can store noisy or conflicting facts. | high | enforce policy checks and block on missing context | G-MEM-020 | T-MEM-020 |
| R-MEM-002 | Cross-tenant memory indexing can cause data exposure. | medium | release gating plus rollback rehearsal | G-MEM-021 | T-MEM-021 |

## Risk Scoring Rule

- high risk: immediate gate failure and release block.
- medium risk: release allowed only with mitigation evidence.
- low risk: tracked in weekly review.

## Evidence Requirements

- E-MEM-020: risk simulation logs.
- E-MEM-021: mitigation verification artifacts.
