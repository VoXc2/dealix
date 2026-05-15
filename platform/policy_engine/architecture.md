# Policy Engine — Architecture

> Phase 5: Governance Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Declarative policies validated at runtime on every action.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/governance_os/policy_registry.py`
- `auto_client_acquisition/governance_os/policy_check.py`

## Contract

Inputs: action + context. Outputs: policy verdict + violated rules.

## Position in the operating model

- Risk tier: **critical**
- Maturity dimensions advanced: governable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
