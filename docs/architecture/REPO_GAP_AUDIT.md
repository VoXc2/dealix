# Dealix Repository Gap Audit

_Last reviewed: 2026-05-26_

This audit captures what is missing or under-specified across engineering, product, operations, security, compliance, and go-to-market so the repository can move from an impressive codebase to a repeatable production operating system.

## Executive summary

Dealix already has strong strategic positioning, a broad FastAPI backend, Saudi-native compliance language, a public landing surface, and an unusually rich documentation set. The remaining gap is not “more ideas”; it is operational hardening: canonical run paths, deterministic CI, environment ownership, release discipline, frontend/backend contract testing, and evidence that claims in README, landing pages, and sales collateral are continuously verified.

## Current strengths

| Area | What is already strong |
|---|---|
| Product narrative | Clear Saudi B2B revenue engine positioning with Lead, Service, and Trust layers. |
| Architecture | Explicit Decision, Execution, Trust, Data, and Operating planes. |
| Backend | FastAPI + SQLAlchemy async stack with many routers and integration points. |
| Trust/compliance | PDPL, ZATCA, audit, approval, and no-overclaim concepts are first-class. |
| Commercialization | Pricing, service catalog, onboarding, and day-1 operating material exist. |
| Developer UX | Makefile, Docker, env template, docs tree, and CI exist. |

## Highest-priority gaps

### P0 — Must fix before serious production launch

| Gap | Why it matters | Required action | Owner |
|---|---|---|---|
| CI must be deterministic | Broken or ambiguous CI makes every claim unreliable. | Keep one workflow definition, split Python and web jobs, enforce clear failure modes. | Engineering |
| Environment variable source of truth | `.env.example`, production templates, deploy scripts, and frontend variables can drift. | Generate env docs from one schema or add an env verifier that fails on duplicate/conflicting required variables. | Platform |
| Dependency lock strategy | Python and web builds should be reproducible. | Commit `requirements.txt`/`requirements-dev.txt` from pyproject and add `apps/web/package-lock.json` or switch CI to an intentional package-manager policy. | Platform |
| README accuracy | The repo clone command must match the actual repository. | Replace stale project names and ensure all quick-start commands run from a clean clone. | Developer Experience |
| Security claims need evidence | README says gitleaks/trufflehog/bandit run in CI; CI should prove that. | Add explicit secret scanning/security jobs or adjust public claims to current reality. | Security |
| Production readiness gate | Launch should not depend on memory or ad-hoc scripts. | Add one canonical `make prod-verify` target that runs the official launch checks. | Operations |

### P1 — Needed for credible enterprise pilots

| Gap | Why it matters | Required action | Owner |
|---|---|---|---|
| API contract governance | 100+ routers need stable external contracts. | Export OpenAPI artifact in CI and diff it for breaking changes. | Backend |
| Frontend/backend contract tests | Dashboard demos can silently drift from API behavior. | Add Playwright or API-mock contract tests for critical user flows. | Frontend |
| Release notes and changelog | Enterprise buyers need change traceability. | Add `CHANGELOG.md` and release checklist tied to tags. | Product Ops |
| Observability runbook | Logs exist, but incident triage needs standard queries and dashboards. | Document request-id tracing, Sentry/Langfuse/PostHog usage, and common failure modes. | SRE |
| Data retention and deletion proof | PDPL posture needs executable controls, not only descriptions. | Add tests/scripts for suppression, retention, export, and deletion workflows. | Compliance Engineering |
| Role-based admin boundary | Admin API keys exist, but enterprise access should map to roles. | Add RBAC matrix and tests for admin/customer/public boundaries. | Security |

### P2 — Differentiators to polish

| Gap | Why it matters | Required action | Owner |
|---|---|---|---|
| Bilingual doc parity | Arabic and English docs may drift. | Add doc parity checklist for README, pricing, service catalog, onboarding, and legal text. | Product Marketing |
| Demo data governance | Lead samples and public demos must avoid accidental personal data issues. | Add synthetic-data policy and generator. | Data |
| Architecture decision records | Many decisions are implicit. | Add ADRs for LLM routing, trust plane, provider fallback, persistence, and auth. | Architecture |
| Benchmarks and evals | AI quality claims need repeatable measurement. | Publish eval set structure, scoring rubric, and regression dashboard. | AI Engineering |
| Partner/agency enablement | White-label model needs operational package. | Add agency onboarding kit, SLA template, brand rules, and support escalation. | GTM |

## Specific repository fixes completed in this pass

- Consolidated the duplicated `.github/workflows/ci.yml` definitions into one workflow.
- Preserved Python quality, readiness, regression, coverage, smoke, and deterministic eval checks.
- Added a dedicated Next.js web build job for `apps/web`.
- Made the web dependency install tolerant of the current repository state where `apps/web/package-lock.json` may not exist yet.
- Added this audit as a canonical gap register so future work can be tracked against explicit priorities.

## Recommended next commits

1. Fix README quick-start repository name and command paths.
2. Add `docs/ops/PRODUCTION_READINESS_CHECKLIST.md` with one launch gate.
3. Add `scripts/check_env_contract.py` and fail CI on duplicate or conflicting env definitions.
4. Add `CHANGELOG.md` and `.github/pull_request_template.md`.
5. Add `make prod-verify` that wraps the actual launch verification scripts.
6. Add `apps/web/package-lock.json` once dependencies are installed locally.
7. Add OpenAPI export and breaking-change diff in CI.
8. Align security claims with actual CI jobs or add gitleaks/trufflehog/detect-secrets jobs.

## Acceptance criteria for “complete from all angles”

Dealix should be considered repository-complete when:

- A new developer can clone, configure, run, test, and deploy from README without tribal knowledge.
- CI covers backend, frontend, security, contracts, readiness data freshness, and production smoke paths.
- Every public product claim has a linked source, test, register entry, or documented status.
- Every production env var is owned, documented, validated, and free of duplicate contradictory definitions.
- Release notes, rollback, incident response, and customer onboarding are connected to one release process.
- Admin, public, webhook, and customer routes have explicit auth and regression tests.
- Saudi compliance controls include executable verification for consent, suppression, retention, and audit trails.

## Arabic summary

الريبو قوي جدًا من ناحية الفكرة، العمارة، والمواد التجارية. الناقص الحقيقي هو تحويله إلى نظام إنتاجي قابل للتشغيل والتدقيق بدون معرفة داخلية: CI ثابت، أوامر تشغيل دقيقة، متغيرات بيئة موحدة، اختبارات عقد بين الواجهة والـ API، توثيق إطلاق واحد، وإثبات آلي لكل ادعاء أمني أو امتثالي أو تجاري.
