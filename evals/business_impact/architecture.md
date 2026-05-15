# Business Impact Evals — Architecture

> Phase 6: Evaluation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Tie platform behavior to ROI and operational outcomes.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `evals/outreach_quality_eval.yaml`
- `evals/company_brain_eval.yaml`

## Contract

Inputs: outcome scenarios. Outputs: business-impact score.

## Position in the operating model

- Risk tier: **medium**
- Maturity dimensions advanced: measurable, continuously_improving
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
