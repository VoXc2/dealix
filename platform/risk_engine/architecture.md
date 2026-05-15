# Risk Engine — Architecture

> Phase 5: Governance Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Score every action's risk before it runs.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/risk_resilience_os`
- `auto_client_acquisition/governance_os/runtime_decision.py`

## Contract

Inputs: action + context. Outputs: risk score + tier + required controls.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: governable, measurable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
