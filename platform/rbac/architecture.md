# RBAC — Architecture

> Phase 1: Foundation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

No unrestricted access; no shared permissions.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/agent_identity_access_os`
- `api/security`

## Contract

Inputs: principal + resource + action. Outputs: allow / deny + reason.

## Position in the operating model

- Risk tier: **critical**
- Maturity dimensions advanced: governable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
