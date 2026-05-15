# Security — Architecture

> Phase 1: Foundation Maturity
> Layer of *The operating infrastructure layer for the agentic enterprise.*

## Goal

Secrets, encryption, and runtime hardening as a baseline, not an add-on.

## Implemented by (existing modules)

This system is a **governing operating-model layer**. It does not re-implement
logic — it indexes, documents, and scores the modules below. Change behavior in
the modules, not here.

- `auto_client_acquisition/security_privacy`
- `auto_client_acquisition/secure_agent_runtime_os`
- `.gitleaks.toml`

## Contract

Inputs: any request crossing a trust boundary. Outputs: hardened, audited request.

## Position in the operating model

- Risk tier: **critical**
- Maturity dimensions advanced: enterprise_safe, governable
- Required companion artifacts: architecture.md, readiness.md, observability.md, rollback.md, metrics.md, risk_model.md, `tests/`, `evals/`

## Required artifacts

Every system in this layer ships: `architecture.md`, `readiness.md`,
`observability.md`, `rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
