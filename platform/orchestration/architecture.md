# Orchestration — Architecture

> Phase 3: Workflow Orchestration Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Event-driven coordination of agents and workflows.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/orchestrator`
- `auto_client_acquisition/agentic_operations_os`

## Contract

Inputs: event. Outputs: routed agent/workflow invocations.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: orchestrated, workflow_native
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
