# Execution Engine — Architecture

> Phase 3: Workflow Orchestration Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Deterministic execution of approved actions with full audit.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/execution_os`
- `auto_client_acquisition/delivery_factory`

## Contract

Inputs: approved action. Outputs: executed + audit-logged result.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: orchestrated, governable, observable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
