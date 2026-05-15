# Workflow Engine — Architecture

> Phase 3: Workflow Orchestration Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Durable execution with retries, fallback, and compensation.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/workflow_os`
- `auto_client_acquisition/workflow_os_v10`

## Contract

Inputs: workflow definition + event. Outputs: durable run state.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: workflow_native, evolvable, observable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
