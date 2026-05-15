# Retrieval Evals — Architecture

> Phase 6: Evaluation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Recall, citation accuracy, and permission-leak checks for retrieval.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `evals/lead_intelligence_eval.yaml`
- `tests/governance`

## Contract

Inputs: retrieval cases. Outputs: pass/fail + recall/citation scores.

## Position in the operating model

- Risk tier: **medium**
- Maturity dimensions advanced: measurable, continuously_improving
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
