# Dealix CI Economics V1 — 2026-09-08

Purpose: reduce GitHub Actions runner-minute waste without removing or weakening any trust gate.

## Proven waste on the current CI workflow

The current full CI is triggered on both push and pull_request across feature/fix/chore/copilot/claude/release branch patterns. A normal PR branch can therefore consume a full push run and a full PR run for the same code revision. Existing concurrency is ref-scoped, so push refs and PR refs do not cancel each other.

The current Web checks also provision two separate runners and execute two separate `npm ci` installs against the same `apps/web` lockfile:

- Next.js web verify: `npm ci` -> `npm run verify`
- Frontend verify: `npm ci` -> `npm run typecheck` -> `npm run build`

## Bounded optimization contract

1. Full push CI runs on `main` only.
2. Full pull-request CI runs for PRs targeting `main`.
3. `workflow_dispatch` remains available for explicit live Railway smoke inputs.
4. Concurrency uses PR number when present, otherwise the ref, and cancels superseded runs.
5. Web verify/typecheck/build share one checkout, Node setup and `npm ci`.
6. Python quality/readiness, coverage, doctrine guards, commercial/company-intelligence checks, Docker image builds, OpenAPI/Alembic, Codecov diagnostics and optional Railway smoke are preserved.
7. Do not add third-party path-filter actions merely to save minutes.
8. Do not treat a cheaper CI run as stronger evidence; source/runtime/release truth rules remain unchanged.

## Current blocking context

GitHub-hosted Actions execution has been proven historically to fail before repository steps after the included Actions-minute pool was exhausted. This patch does not restore billing/quota by itself. Its purpose is to prevent avoidable duplicate consumption once runner execution is available again.

`L5_EXECUTED=NONE`
