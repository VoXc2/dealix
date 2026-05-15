# Agent Catalog — Architecture

> Phase 2: Agentic Runtime Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Every agent has identity, role, permissions, memory scope, risk level, KPIs.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/agents`
- `auto_client_acquisition/ai_workforce_v10`
- `core/agents`

## Contract

Inputs: agent goal. Outputs: agent card + governed execution result.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: agent_ready, governable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
