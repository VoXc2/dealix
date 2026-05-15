# Agent Memory — Architecture

> Phase 2: Agentic Runtime Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Per-agent memory scope with isolation between agents and tenants.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `core/memory`
- `auto_client_acquisition/revenue_memory`

## Contract

Inputs: scoped read/write. Outputs: isolated agent memory.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: agent_ready, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
