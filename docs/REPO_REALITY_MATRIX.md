# Repo Reality Matrix

> Verified vs. spec-claimed. Statuses use the canonical set only.

## Critical paths

| Path | Purpose | Exists | Non-empty | Tested | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `api/main.py` | FastAPI factory + root + lifespan | ✅ | ✅ | ✅ | PROVEN_LIVE | clean JSON root, /healthz + /health both 200 |
| `api/routers/health.py` | health probe | ✅ | ✅ | ✅ | PROVEN_LIVE | |
| `api/routers/operator.py` | operator chat | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch | safety classifier shipped here imports cleanly |
| `api/routers/services.py` | services catalog | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch | |
| `api/routers/prospect.py` (singular) | prospect routes | ✅ | ✅ | ✅ | PROVEN_LIVE | spec asked plural but file is singular |
| `api/routers/full_os.py` | payments routes (`/payments/manual-request`, `/payments/mark-paid`) | ✅ | ✅ | ✅ | PROVEN_LOCAL | |
| `api/routers/payments.py` | dedicated payments | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch | |
| `api/routers/proof_ledger.py` | proof ledger | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch | |
| `api/routers/role_briefs.py` | role briefs | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch (BLOCKER for sales_manager pending migration) |
| `api/routers/whatsapp_briefs.py` | whatsapp role briefs | ❌ on this branch | n/a | n/a | MISSING_OR_EMPTY locally; PROVEN_LIVE on deploy branch (BLOCKER for sales_manager + ceo pending migration) |
| `api/routers/automation.py` | compliance gate | ✅ | ✅ | ✅ | PROVEN_LOCAL; BLOCKER on prod (500 — fix in PR #131) | |
| `api/routers/autonomous.py` | core write routes | ✅ | ✅ | ✅ | PROVEN_LOCAL (after AsyncSession fix) | |
| `auto_client_acquisition/safety/intent_classifier.py` | bilingual safety classifier | ✅ | ✅ | ✅ | PROVEN_LOCAL | this PR |
| `auto_client_acquisition/customer_ops/company_brain.py` | company brain aggregator | ✅ | ✅ | ✅ | PROVEN_LOCAL | this PR |
| `auto_client_acquisition/operator/` | dedicated operator package | ❌ | n/a | n/a | MISSING_OR_EMPTY | spec wanted; functional equivalent via deploy-branch operator router |
| `auto_client_acquisition/service_tower/` | service tower package | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via `/api/v1/services/*` |
| `auto_client_acquisition/revenue_company_os/` | role-brief builder | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent on deploy branch's `role_briefs.py` |
| `auto_client_acquisition/proof/` | proof package | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via deploy-branch `proof_ledger.py` |
| `auto_client_acquisition/compliance/` | compliance package | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via `auto_client_acquisition/email/compliance.py` |
| `auto_client_acquisition/whatsapp/` | whatsapp package | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via `auto_client_acquisition/personal_operator/whatsapp_cards.py` |
| `auto_client_acquisition/partner_os/` | partner package | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via deploy-branch `partners.py` |
| `auto_client_acquisition/learning/` | learning loop | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via deploy-branch `self-growth/*` endpoints |
| `landing/index.html` | marketing landing | ✅ | ✅ | ✅ | PROVEN_LOCAL | |
| `landing/services.html` | services page | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via API |
| `landing/operator.html` | operator UI | ❌ | n/a | n/a | MISSING_OR_EMPTY | API-only on deploy branch |
| `landing/command-center.html` | command center | ✅ | ✅ | ✅ | PROVEN_LOCAL | |
| `landing/proof-pack.html` | proof pack page | ❌ | n/a | n/a | MISSING_OR_EMPTY | functional equivalent via API |
| `landing/trust-center.html` | safety + PDPL | ✅ | ✅ | ✅ | PROVEN_LOCAL | |
| `landing/pricing.html` | pricing | ✅ | ✅ | ✅ | PROVEN_LOCAL | |
| `scripts/full_acceptance.sh` | full acceptance | ❌ | n/a | n/a | MISSING_OR_EMPTY | substituted by `pytest` + `staging_smoke.sh` + `verify_service_tower.py` + `verify_delivery_workflows.py` |
| `scripts/staging_smoke.sh` | smoke against staging | ✅ | ✅ | ✅ | PROVEN_LIVE | upgraded this PR |
| `scripts/launch_readiness_check.py` | launch readiness | ❌ | n/a | n/a | MISSING_OR_EMPTY | substituted by `/api/v1/personal-operator/launch-readiness` endpoint |
| `scripts/verify_service_tower.py` | new | ✅ | ✅ | ✅ | PROVEN_LIVE | this PR |
| `scripts/verify_delivery_workflows.py` | new | ✅ | ✅ | ✅ | PROVEN_LIVE | this PR |
| `scripts/migrate_add_hubspot_deal_id.py` | new | ✅ | ✅ | ✅ | PROVEN_LOCAL idempotent | this PR |
| `db/migrations/` | migrations | dir exists, mostly empty | — | — | MISSING_OR_EMPTY | not Alembic-driven yet |
| `db/session.py` | DB session | ✅ | ✅ | ✅ | PROVEN_LOCAL (after fix) | |
| `tests/test_*.py` | test suite | ✅ | ✅ | ✅ | PROVEN_LOCAL | 595 passing |
| `docs/*.md` | governance docs | ✅ | ✅ | n/a | PROVEN_LOCAL | 24+ matrices/specs |

## Counts

| Metric | Value |
| --- | --- |
| Local pytest passing | 595 |
| Local routes | 260 |
| Prod routes | 306 |
| Local landing pages | 25 / 25 actual; 6 spec-claimed missing |
| Spec-claimed routers missing locally (live on deploy branch) | 7 |
| Empty critical files | 0 (only intentional `__init__.py` markers) |
