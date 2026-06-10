# Dealix Production Finalization Status

_Last updated: 2026-05-26_

This file separates repository-complete work from items that require external execution in GitHub, the hosting provider, DNS, payment dashboards, or a local package manager.

## Completed in repository

| Area | Status | Evidence |
|---|---|---|
| CI consolidation | Done | `.github/workflows/ci.yml` has one CI workflow with Python and web verification jobs. |
| Security automation | Done | `.github/workflows/security.yml` adds CodeQL and Dependency Review. |
| Dependency automation | Done | `.github/dependabot.yml` covers pip, npm, GitHub Actions, and Docker. |
| Production smoke automation | Done | `.github/workflows/production-smoke.yml` runs scheduled/manual smoke tests. |
| Env contract validation | Done | `scripts/check_env_contract.py`, `make env-check`. |
| OpenAPI export | Done | `scripts/export_openapi.py`, `make openapi-export`. |
| OpenAPI contract check | Done | `scripts/check_openapi_contract.py`, `make api-contract-check`. |
| Security smoke | Done | `scripts/security_smoke.py`, `make security-smoke`. |
| Production command bundle | Done | `make prod-verify`, `make production-smoke`. |
| Frontend security headers | Done | `apps/web/next.config.mjs` sets HSTS, CSP, frame, referrer, MIME, and permissions headers. |
| Frontend SEO metadata | Done | `apps/web/app/layout.tsx`, `robots.ts`, `sitemap.ts`, `manifest.ts`, and homepage JSON-LD. |
| Frontend homepage upgrade | Done | `apps/web/app/page.tsx` now positions Dealix as Revenue OS, Agent Governance, Trust & Safety, and Value Engine. |
| Frontend status page | Done | `apps/web/app/status/page.tsx` provides public operational links. |
| Frontend verification | Done | `apps/web/package.json` has `typecheck` and `verify`; CI runs `npm run verify`. |
| Frontend env template | Done | `apps/web/.env.example` documents public site/API variables. |
| Live domain runbook | Done | `docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`. |
| Frontend production runbook | Done | `docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md`. |
| Server hardening checklist | Done | `docs/ops/SERVER_HARDENING_CHECKLIST.md`. |
| Production secrets checklist | Done | `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`. |
| Monitoring matrix | Done | `docs/ops/MONITORING_MATRIX.md`. |
| Incident drill | Done | `docs/ops/LIVE_DOMAIN_INCIDENT_DRILL.md`. |
| Release process | Done | `docs/ops/RELEASE_PROCESS.md`. |
| API policy | Done | `docs/architecture/API_CONTRACT_POLICY.md`. |
| Ownership | Done | `.github/CODEOWNERS`, `docs/ops/OWNERSHIP_MATRIX.md`. |
| Execution backlog | Done | `docs/ops/EXECUTION_BACKLOG.md` and CSV importer. |
| README refresh | Done | `README.md` now points to the real repo and operating commands. |

## Tracked external execution

| Issue | Item | Why it needs external execution |
|---|---|---|
| #467 | Generate and commit `apps/web/package-lock.json` | Requires npm registry dependency resolution. |
| #468 | Configure live production secrets | Secrets cannot be inferred or safely committed. |
| #469 | Verify live DNS and TLS | DNS/certificate state lives in provider dashboards. |
| #470 | Verify payment and webhook dashboards | Provider dashboards and real credentials are outside the repo. |
| #471 | Run CI, Security, and Production Smoke workflows | Requires GitHub Actions runner execution and review of results. |

## Recommended final execution order

1. Set repository and hosting secrets from `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`.
2. Generate and commit `apps/web/package-lock.json`.
3. Run GitHub Actions: CI, Security, Production Smoke.
4. Run local verification if you have the repo cloned:

```bash
make env-check
make api-contract-check
make security-smoke
make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me
```

5. Verify DNS/TLS in hosting/DNS provider dashboards.
6. Verify payment and webhook provider dashboards.
7. Close issues #467–#471 only after evidence is attached.

## Arabic summary

تم إنجاز كل ما يمكن إنجازه داخل الريبو: CI، security، smoke، env، OpenAPI، runbooks، ownership، release، monitoring، hardening للواجهة، SEO، status page، وأوامر الإنتاج. المتبقي محصور في مهام خارجية موثقة كـ Issues لأنها تحتاج GitHub Secrets، تشغيل Actions، DNS/hosting dashboard، payment dashboards، أو توليد npm lockfile من registry.
