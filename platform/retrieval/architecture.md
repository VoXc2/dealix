# Retrieval — Architecture

> Phase 4: Organizational Memory Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Hybrid, permission-aware retrieval with citations and lineage.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/intelligence_os`
- `auto_client_acquisition/revenue_memory`

## Contract

Inputs: query + principal. Outputs: ranked passages + citations + lineage.

## Position in the operating model

- Risk tier: **medium**
- Maturity dimensions advanced: transformation_ready, governable, measurable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
