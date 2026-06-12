# Dealix Environment Contract

> **Status:** Active (P0)
> **Owner:** Founder Office
> **Enforcer:** `scripts/check_env_contract.py` + `make env-check`
> **Last verified:** see `reports/prod/PROD_VERIFY_LATEST.md`

This is the single source of truth for Dealix environment variables. The contract is enforced by a dependency-free Python script that runs early in CI, in pre-commit, and on every PR.

## 1. What the contract is

A binding list of:

- **Required keys** (backend + frontend) — the app will not start without them.
- **Forbidden patterns** — what counts as a public-admin key, malformed assignment, or duplicate key.
- **Templates** — `.env.example` (backend) and `apps/web/.env.example` (frontend) are the canonical templates the contract validates against.

If the templates change, the contract changes. If the contract changes, this doc changes. All three are versioned together.

## 2. What is enforced

`scripts/check_env_contract.py` checks four things and exits non-zero on any failure:

1. **Duplicate keys** — same `KEY=...` defined twice in one template.
2. **Malformed assignments** — anything that does not match `^[A-Z][A-Z0-9_]*=.*$`.
3. **Public-admin exposure** — a `NEXT_PUBLIC_*` variable whose name suggests admin authority (currently: `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`) is flagged so the operator confirms it is intentional.
4. **Required keys** — both templates must declare every key in `REQUIRED_KEYS` / `REQUIRED_WEB_KEYS`.

The script is dependency-free so it can run before `pip install`. That is why it lives in `scripts/` and not in `api/`.

## 3. Required keys

| Key | Template | Role |
| --- | --- | --- |
| `ENVIRONMENT` | backend | `development` / `test` / `production`. Never `production` in local dev. |
| `LOG_LEVEL` | backend | `DEBUG` / `INFO` / `WARNING` / `ERROR`. |
| `APP_SECRET_KEY` | backend | Session / JWT signing. Must be ≥ 32 chars random. |
| `DATABASE_URL` | backend | Postgres connection string (asyncpg). |
| `APP_URL` | backend | Public app URL. Used for CORS + email links. |
| `ADMIN_API_KEYS` | backend | Comma-separated. Required for any `/api/v1/ops-autopilot/*` route. |
| `CORS_ORIGINS` | backend | Comma-separated allowed origins. No `*` in production. |
| `NEXT_PUBLIC_SITE_URL` | frontend | Public site origin. |
| `NEXT_PUBLIC_API_URL` | frontend | Backend origin for the Next.js client. |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | frontend | Toggle for the ops proxy route. |

The frontend admin key (`NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`) is **publicly visible** by definition (`NEXT_PUBLIC_` prefix ships to the browser bundle). Use it only for read-only, non-privileged operations. Anything that mutates production must go through the server-side `ADMIN_API_KEYS` and `X-Admin-API-Key` header.

## 4. What counts as a public-admin key

`NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` is in `PUBLIC_ADMIN_KEYS` and the script flags it. The check is intentional: a `NEXT_PUBLIC_` admin key is convenient in dev and dangerous in prod. The flag is a forcing function for the operator to confirm the value is rotated and scoped to local dev.

## 5. How to run locally

```bash
make env-check
# or, directly:
python scripts/check_env_contract.py
```

The script prints a one-line status per template. Exit 0 = contract valid. Exit 1 = one or more failures, listed above the summary line.

## 6. How to fix common failures

### `Duplicate key: X`

Open the template the script points to, remove the duplicate line, and keep the canonical one. The first occurrence wins.

### `Missing required key: X`

Add `X=` to the template with a comment explaining the expected value. Do not commit a real secret — only the key name.

### `Public admin key in NEXT_PUBLIC_`

If intentional (local dev only), add a comment above the line: `# dev-only: rotate before staging`. The check is non-blocking in dev. In prod, remove the key entirely and call the admin API through the server-side `ADMIN_API_KEYS` path.

### `Malformed assignment: X`

The script expects `^[A-Z][A-Z0-9_]*=.*$`. Lowercase keys, hyphens, or empty values are rejected. Fix the line.

### `CI blocks the PR`

The `make env-check` target is wired into `make prod-verify`, which is the canonical pre-deploy gate. A failing contract blocks the PR.

## 7. CI behavior

- **PR:** blocking. The contract must pass for the PR to be mergeable.
- **Main:** non-blocking. The contract is logged but does not fail the deploy (the env is already locked to Railway).
- **Local pre-commit:** `make doctor` runs the contract plus alembic-heads plus security-smoke.

## 8. Versioning

The contract changes when:

- A new required key is added (rare — usually means a new non-optional service).
- A new public-admin key is introduced (very rare — usually means a refactor of admin auth).
- A required key is renamed or removed (breaking — coordinate with the founder office).

The contract owner is the founder office. Open a PR against `docs/ops/ENV_CONTRACT.md` first, then update the script.

## 9. Related

- `scripts/check_env_contract.py` — enforcer
- `Makefile` → `env-check`, `doctor`, `prod-verify` targets
- `docs/ops/PRODUCTION_VERIFICATION_GUIDE.md` — what `make prod-verify` does
- `docs/contributing/DEPLOYMENT.md` — production env minimums
