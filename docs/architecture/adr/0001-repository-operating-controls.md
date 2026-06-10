# ADR 0001 — Repository Operating Controls

Date: 2026-05-26

## Status

Accepted

## Context

Dealix combines backend APIs, frontend assets, compliance registers, commercial material, and launch runbooks. Without automated operating controls, repository claims can drift from implementation and production launch can become dependent on memory.

## Decision

Adopt explicit repository operating controls:

- Environment template validation through `scripts/check_env_contract.py` and `make env-check`.
- OpenAPI export through `scripts/export_openapi.py` and `make openapi-export`.
- Production verification through `make prod-verify`.
- CI checks for environment contract and OpenAPI export.
- Repository gap tracking through `docs/architecture/REPO_GAP_AUDIT.md`.
- Launch readiness tracking through `docs/ops/PRODUCTION_READINESS_CHECKLIST.md`.

## Consequences

- Production readiness becomes repeatable and auditable.
- New contributors have a smaller path from clone to verification.
- Future work should extend these controls rather than adding ad-hoc scripts.
