# Dealix Production Readiness Checklist

_Last reviewed: 2026-05-26_

Use this checklist before any public launch, enterprise pilot, production redeploy, or live-domain change.

## 1. Source and release integrity

- [ ] Default branch is protected or governed by a ruleset.
- [ ] CI is green on the target commit.
- [ ] Security workflow is green or reviewed.
- [ ] The release commit is tagged.
- [ ] `CHANGELOG.md` explains customer-visible changes.
- [ ] Rollback commit/tag/container image is known.
- [ ] Docker image digest is recorded when images are deployed.

## 2. Configuration and secrets

- [ ] `.env.example` matches runtime settings used by API, workers, and frontend.
- [ ] `make env-check` passes.
- [ ] No required production variable has duplicate or contradictory definitions.
- [ ] Secrets are set through the hosting platform, not committed files.
- [ ] `DEALIX_PUBLIC_URL` points to the public website domain.
- [ ] `DEALIX_PRODUCTION_BASE_URL` points to the production API domain.
- [ ] `CORS_ORIGINS` includes only expected production/staging origins.
- [ ] Browser `NEXT_PUBLIC_*` variables do not expose privileged credentials.

## 3. Live domain and TLS

- [ ] Public domain resolves to the intended frontend service.
- [ ] API domain resolves to the intended backend service.
- [ ] `https://dealix.me` or the configured public host responds successfully.
- [ ] `https://api.dealix.me/health` or the configured API health URL responds successfully.
- [ ] TLS certificates are valid and auto-renewed.
- [ ] Old DNS records are removed or documented.
- [ ] `docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md` is current.

## 4. Database and persistence

- [ ] Database URL points to the intended production database.
- [ ] Migrations apply cleanly from the previous production state.
- [ ] Alembic has a single head.
- [ ] Backup and restore process has been tested.
- [ ] Retention, suppression, and deletion workflows have evidence.
- [ ] Event/proof ledgers use the intended production backend mode.

## 5. API and backend

- [ ] `/health` returns healthy.
- [ ] Public endpoints are unauthenticated only where intended.
- [ ] Admin endpoints reject missing or invalid credentials.
- [ ] Webhook signature verification is active where applicable.
- [ ] `make openapi-export` passes.
- [ ] `python scripts/check_openapi_contract.py` passes.
- [ ] Production smoke test passes against the API domain.
- [ ] Scheduled `Production Smoke` workflow is enabled.

## 6. Frontend and public surface

- [ ] `apps/web/package-lock.json` is committed for reproducible builds.
- [ ] Landing pages build successfully.
- [ ] Pricing, service catalog, and demo flows point to the correct API URL.
- [ ] Arabic and English copy match approved commercial claims.
- [ ] SEO audit has no required gaps.
- [ ] Analytics capture respects the privacy posture.
- [ ] Browser console is free of production-blocking errors.

## 7. Trust, compliance, and claims

- [ ] No-overclaim register is updated for all public claims.
- [ ] PDPL consent, lawful basis, opt-out, retention, and suppression paths are represented in tests or scripts.
- [ ] ZATCA/payment claims reflect the deployed flow.
- [ ] High-stakes AI actions require the correct approval class.
- [ ] Evidence packs include source references, tool/model traceability, and bilingual summaries where required.
- [ ] External commitments cannot be sent automatically without policy approval.

## 8. Observability and incident response

- [ ] Structured logs are enabled in production.
- [ ] Request IDs are propagated through API and integrations.
- [ ] Error capture is configured if used.
- [ ] Metrics/analytics destinations are configured where enabled.
- [ ] Incident owner, escalation path, and rollback steps are known.
- [ ] Domain/TLS failure path is covered by `docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`.

## 9. Commercial readiness

- [ ] Pricing page and checkout amounts match approved offer packaging.
- [ ] Demo request workflow routes to the right inbox/CRM/calendar.
- [ ] Onboarding checklist is current.
- [ ] Customer-facing security/compliance answers match implemented controls.
- [ ] Support and refund/payment escalation processes are documented.

## Minimum launch gate

A commit is launch-ready only when:

1. CI is green.
2. Security workflow is green or explicitly risk-accepted.
3. Image/platform build succeeds.
4. The production env contract is verified.
5. `/health` and public smoke checks pass on the production API domain.
6. Security scanning has no unresolved high/critical findings.
7. No-overclaim register has no stale customer-facing claims.
8. Rollback instructions are available to the operator running the launch.

## Arabic summary

قبل أي إطلاق لازم يكون عندك: CI ناجح، أسرار سليمة، DNS/TLS صحيح، API health ناجح، قاعدة بيانات قابلة للترقية والرجوع، اختبارات دخان للإنتاج، إثبات للامتثال، وخطة rollback واضحة.
