# Escalation — Architecture

> Phase 2: Agentic Runtime Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Every high-risk action escalates to a human above the loop.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/approval_center`
- `auto_client_acquisition/governance_os/approval_matrix.py`

## Contract

Inputs: risky action. Outputs: human decision (approve / reject / modify).

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: governable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
