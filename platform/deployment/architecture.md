# Deployment / Infrastructure-as-Code — Architecture

> Phase 1: Foundation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Reproducible, rollbackable deployments via IaC and CI.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/enterprise_rollout_os`
- `scripts/infra`
- `Dockerfile`
- `docker-compose.yml`
- `.github`

## Contract

Inputs: release candidate. Outputs: staged deployment + rollback handle.

## Position in the operating model

- Risk tier: **high**
- Maturity dimensions advanced: evolvable, enterprise_safe
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
