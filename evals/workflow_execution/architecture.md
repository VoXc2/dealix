# Workflow Execution Evals — Architecture

> Phase 6: Evaluation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Verify workflows complete, retry, compensate, and audit correctly.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `evals/revenue_os_cases.jsonl`
- `tests/governance`

## Contract

Inputs: workflow scenarios. Outputs: execution-correctness verdict.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: measurable, workflow_native
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
