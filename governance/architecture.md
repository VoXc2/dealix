# Governance — Architecture

> Phase 5: Governance Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Every action passes risk scoring -> policy -> approval -> execution -> audit.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/governance_os`
- `dealix/governance`

## Contract

Inputs: proposed action. Outputs: governed decision + audit record.

## Position in the operating model

- Risk tier: **critical**
- Maturity dimensions advanced: governable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
