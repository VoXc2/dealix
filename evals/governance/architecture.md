# Governance Evals — Architecture

> Phase 6: Evaluation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Verify policy, approval, and audit enforcement holds under test.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `evals/governance_eval.yaml`
- `tests/governance`

## Contract

Inputs: governance scenarios. Outputs: enforcement verdict.

## Position in the operating model

- Risk tier: **critical**
- Maturity dimensions advanced: measurable, governable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
