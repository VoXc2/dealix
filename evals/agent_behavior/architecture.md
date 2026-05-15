# Agent Behavior Evals — Architecture

> Phase 6: Evaluation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Verify agents stay inside governance, memory, and tool boundaries.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `evals/personal_operator_cases.jsonl`
- `tests/governance`

## Contract

Inputs: agent scenarios. Outputs: behavior-conformance verdict.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: measurable, agent_ready
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
