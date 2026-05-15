# Continuous Improvement — Architecture

> Phase 7: Continuous Evolution Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Feedback loops and regression detection feeding safe change.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/learning_flywheel`
- `auto_client_acquisition/self_growth_os`

## Contract

Inputs: feedback + telemetry. Outputs: prioritized, gated improvements.

## Position in the operating model

- Risk tier: **medium**
- Maturity dimensions advanced: continuously_improving, evolvable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
