# Platform Foundation — Architecture

> Phase 1: Foundation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Single bootstrap and capability registry for the whole platform.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/enterprise_os`
- `auto_client_acquisition/platform_v10`

## Contract

Inputs: tenant bootstrap request. Outputs: provisioned tenant + capability registry entry.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: enterprise_safe, transformation_ready
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
