# Reranking — Architecture

> Phase 4: Organizational Memory Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Confidence-scored reranking on top of first-stage retrieval.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/intelligence_os`
- `auto_client_acquisition/intelligence`

## Contract

Inputs: candidate passages. Outputs: reranked passages + confidence.

## Position in the operating model

- Risk tier: **low**
- Maturity dimensions advanced: measurable, transformation_ready
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
