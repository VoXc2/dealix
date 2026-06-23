# Dealix — NEXT ECO PLAN

**Date:** 2026-06-23  
**Planner:** Dealix Startup Release Planner  
**Branch:** `main`  
**Remote:** `origin/main`  
**Working Tree:** Clean (excluding requested local deliverables `DEALIX_FULL_SESSION_EXPORT.zip` and `SESSION_COMMIT_HISTORY.txt`)  
**Current HEAD:** `cfd82a5`

---

## Executive Verdict

Dealix has a **solid foundation** — a working Vite/React frontend, Hono/tRPC backend, MySQL/Drizzle schema, Docker images, Python operational scripts, investor-grade business materials, and active safety gates. However, it still lacks a clean `.env.example`, validated Docker healthchecks, endpoint tests, and a production runbook. The repo is **not yet startup-grade** in its deployment and env-contract discipline, but it is **close**.

**Immediate goal:** Create one stabilization PR that hardens the production surface (env, Docker, boot, docs) without changing the product surface.

**Then:** Execute sequential feature PRs to build a real Startup OS across Revenue Command Room, Company Brain, Client Delivery, Trust/Compliance, and GTM.

---

## Current Repository Reality

| Surface | Actual State |
|---|---|
| **Frontend** | `src/` — Vite + React + React Router (canonical) |
| **Backend** | `api/boot.ts` — Hono app with `/health`, `/ready`, tRPC, WhatsApp webhook |
| **Database** | MySQL via Drizzle ORM; `db/schema.ts` complete |
| **Docker** | `Dockerfile`, `Dockerfile.prod`, `docker-compose.yml`; **no `docker-compose.prod.yml`** |
| **Env contract** | `api/lib/env.ts` requires `APP_ID`, `APP_SECRET`, `DATABASE_URL`, `KIMI_AUTH_URL`, `KIMI_OPEN_URL` in production; **no `.env.example` exists** |
| **Health endpoints** | `/health` and `/ready` exist |
| **Safety scripts** | `scripts/verify_company_launch_ready.py`, `scripts/verify_no_auto_external_send.py` |
| **Tests** | **None found** |
| **Business docs** | Complete presentations, brand guidelines, pricing, product specs |
| **Client templates** | Complete 6-phase delivery lifecycle |
| **Compliance** | PDPL + SDAIA docs present |

### What the Pasted Plan Got Wrong

The pasted plan assumes:
- `apps/web` or `frontend/` — **actual canonical frontend is `src/`**
- `api/main.py` — **actual backend is `api/boot.ts` (Node/TypeScript)**
- Postgres + Alembic — **actual database is MySQL + Drizzle Kit**
- `docker-compose.prod.yml` — **does not exist**

This plan is **adapted to the real repo**.

---

## Known Blockers and Risks

### High Priority
1. **No `.env.example`** — new contributors and Railway deployments have no env contract.
2. **Docker healthcheck points to `/`** — the root path may 404 in production because static files are served only when `env.isProduction` is true; healthcheck should point to `/health`.
3. **No endpoint tests** — `/health`, `/ready`, `/api/trpc` are not covered by automated tests.
4. **No Railway runbook** — deployment steps are not documented.
5. **No production `.env` contract validation** — `verify_company_launch_ready.py` does not check `.env.example`.

### Medium Priority
6. **`api/lib/env.ts` requires `KIMI_AUTH_URL`/`KIMI_OPEN_URL` even in production** — if Kimi auth is not used, this blocks boot.
7. **No smoke tests for frontend pages** — cannot catch TypeScript/runtime regressions automatically.
8. **Operational scripts depend on DB defaults** (`DB_USER`, `DB_PASSWORD`) that may not match `DATABASE_URL`.

### Low Priority
9. `vite.config.ts` includes `kimi-plugin-inspect-react` in production build path — dev-only plugin, but it is in devDependencies so it is fine.
10. `company_os/reports/LAUNCH_READINESS_REPORT.md` is generated and changes timestamp frequently — should remain generated, not hand-edited.

---

## Safety / Outbound Status

| Flag | Required Value | Current Status |
|---|---|---|
| `EXTERNAL_SEND_ENABLED` | `false` | ✅ Safe |
| `EMAIL_SEND_ENABLED` | `false` | ✅ Safe |
| `WHATSAPP_SEND_ENABLED` | `false` | ✅ Safe |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | ✅ Safe |
| `SMS_SEND_ENABLED` | `false` | ✅ Safe |
| `OUTBOUND_MODE` | `draft_only` | ✅ Safe |
| `WHATSAPP_AGENT_MODE` | `dry_run` | ✅ Safe |

**Verdict:** No live outbound is enabled. Safety gates are active.

---

## Exact Next PR Scope

**Branch:** `fix/startup-prod-surface-stabilization`  
**Base:** `main`  
**Goal:** Make the repo startup-grade enough to boot, build, validate, and deploy safely.

### In Scope
1. Create `.env.example` with safe defaults and placeholder secrets.
2. Update `docker-compose.yml` healthcheck to use `/health`.
3. Validate `docker compose config`.
4. Ensure `npm run check` and `npm run build` pass.
5. Ensure backend boots with safe local env.
6. Update `scripts/verify_company_launch_ready.py` to check `.env.example`.
7. Create/update:
   - `docs/ops/ENVIRONMENT_VARIABLES.md`
   - `docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md`
   - `reports/go_live/PROD_SURFACE_STABILIZATION_REPORT.md`
8. Create PR; do **not** merge directly.

### Out of Scope
- No new product features.
- No UI redesign.
- No new database tables.
- No enabling of live outbound.
- No direct push to `main`.

---

## Files to Edit (Phase 1)

| File | Change |
|---|---|
| `.env.example` | Create new env contract file |
| `docker-compose.yml` | Fix healthcheck path to `/health` |
| `scripts/verify_company_launch_ready.py` | Add `.env.example` existence/parse check |
| `docs/ops/ENVIRONMENT_VARIABLES.md` | Sync with `.env.example` |
| `docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md` | Create production deployment guide |
| `reports/go_live/PROD_SURFACE_STABILIZATION_REPORT.md` | Create execution report |
| `PR_DESCRIPTION_STARTUP_PROD_SURFACE.md` | PR description (temporary, not committed) |

---

## Commands to Run (Phase 1)

```bash
# 1. Create branch
git switch main
git pull --ff-only origin main
git switch -c fix/startup-prod-surface-stabilization

# 2. Validate TypeScript
npm run check

# 3. Validate build
npm run build

# 4. Validate Docker Compose
docker compose -f docker-compose.yml config

# 5. Validate backend boot (safe local env)
NODE_ENV=development \
DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix \
APP_ID=local APP_SECRET=local \
KIMI_AUTH_URL=http://localhost KIMI_OPEN_URL=http://localhost \
node -e "import('./api/boot.ts').then(() => console.log('BOOT_OK'))"

# 6. Run safety gates
python scripts/verify_no_auto_external_send.py
python scripts/verify_company_launch_ready.py

# 7. Lint/format checks
npm run lint
npx prettier --check .

# 8. Create PR
git push -u origin HEAD
gh pr create --title "Stabilize startup production surfaces" --body-file PR_DESCRIPTION_STARTUP_PROD_SURFACE.md
```

---

## Tests to Add (Phase 1)

Create a minimal test file:
- `api/__tests__/health.test.ts`
  - `GET /health` returns `status: healthy`
  - `GET /ready` returns `status: ready` when DB is reachable, or `not_ready` when not

Use Vitest + `@hono/node-server` test helpers or simple fetch against a test server.

---

## Rollback Plan

If the PR introduces regressions:

```bash
gh pr close <PR_NUMBER>
git branch -D fix/startup-prod-surface-stabilization
```

If accidentally merged:

```bash
git revert <MERGE_COMMIT_SHA>
git push origin main
```

---

## Do-Not-Touch List

- `src/pages/*` product code (no UI refactors in Phase 1).
- `api/whatsapp-router.ts` send logic (only confirm safety defaults, do not refactor).
- `db/schema.ts` (no migrations in Phase 1).
- `business/presentations/*` (already complete).
- `clients/_template/*` (already complete).
- Any `.env` or `.env.local` files that contain real credentials.
- `.dealix_allow_external_send` override file.

---

## Phase Roadmap (After Phase 1)

| Phase | Branch | Goal |
|---|---|---|
| 1 | `fix/startup-prod-surface-stabilization` | Env + Docker + boot + docs |
| 2 | `phase/backend-api-production-readiness` | Status/outbound endpoints + tests |
| 3 | `phase/frontend-launch-app` | Page smoke tests + safety indicator |
| 4 | `phase/database-foundation` | Drizzle baseline + seed script |
| 5 | `phase/revenue-command-room` | Daily revenue reports + UI |
| 6 | `phase/company-brain-os` | Decision/risk workflows |
| 7 | `phase/client-delivery-os` | Delivery tracking + proof packs |
| 8 | `phase/trust-compliance-os` | PDPL/SDAIA + no-fake-claims policy |
| 9 | `phase/gtm-machine` | ICP + sector playbooks |
| 10 | `phase/railway-go-live` | Deploy runbook + smoke tests |

---

## Definition of Done (Every Phase)

- [ ] `npm run check` passes with 0 TypeScript errors.
- [ ] `npm run build` passes.
- [ ] `npm run production-check` returns **GO**.
- [ ] `npm run outbound-dry` returns **PASS**.
- [ ] No live outbound flags enabled.
- [ ] No secrets committed.
- [ ] No direct push to `main`.
- [ ] PR created and reviewed.

---

*Plan generated: 2026-06-23*  
*Next action: Create branch `fix/startup-prod-surface-stabilization` and implement Phase 1.*
