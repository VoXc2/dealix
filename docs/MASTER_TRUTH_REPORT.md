# Dealix Master Truth Report

> Living document. Updated 2026-05-03. Branch
> `claude/dealix-staging-readiness-LJOju`. Statuses are exclusively from
> the canonical set:
>
> `PROVEN_LIVE | PROVEN_STAGING_WRITE_SAFE | PROVEN_STAGING_READ_ONLY |`
> `PROVEN_LOCAL | CODE_EXISTS_NOT_PROVEN | MISSING_OR_EMPTY | BLOCKER | BACKLOG`

```
CURRENT_BRANCH = claude/dealix-staging-readiness-LJOju
CURRENT_COMMIT = 319ff66 (last published) → about to advance with this report
DIRTY_STATUS   = dirty (this commit's docs + classifier patches + migration script)
DEPLOY_BRANCH  = claude/launch-command-center-6P4N0  (Railway)
FIX_BRANCH     = claude/dealix-staging-readiness-LJOju
TARGET_VERDICT = FIRST_CUSTOMER_READY_REALISTIC (achieved when PR #131 is merged + wiring patch applied + DB migration run + Railway redeploys)
```

## Truth table — system surfaces

| Surface | Status | Evidence |
| --- | --- | --- |
| `/`, `/health`, `/docs`, `/openapi.json` | PROVEN_LIVE | `BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` 22/22 |
| Service Tower 6/6 bundles | PROVEN_LIVE | `BASE_URL=https://api.dealix.me python scripts/verify_service_tower.py` → SERVICE_TOWER_OK |
| Role briefs (5/8 roles green) | PROVEN_LIVE for ceo/growth/cs/compliance/revops/finance | live probe |
| Role brief sales_manager + whatsapp/brief sales_manager | BLOCKER | 500 due to missing `deals.hubspot_deal_id` |
| Operator chat — English + obvious Arabic cold-WA blocks | PROVEN_LIVE | live probe |
| Operator chat — Saudi Arabic cold-WA blocks (12 phrasings) | PROVEN_LOCAL → BLOCKER on prod | classifier shipped here, deploy branch needs the 4-line wiring |
| WhatsApp outbound gate | PROVEN_LIVE | `os/test-send` returns blocked |
| Moyasar webhook signed | PROVEN_LIVE | 401 on unsigned |
| Moyasar live charge | PROVEN_LIVE blocked (no live key configured) | manual fallback path active |
| Gmail live send | PROVEN_LIVE blocked (`gmail_configured()` false) | live probe |
| LinkedIn automation | PROVEN_LIVE blocked (no route exists) | route inventory |
| Compliance/check-outreach + automation/status | BLOCKER on prod (500) | AsyncSession bug — fix in PR #131 |
| Local first-customer flow | PROVEN_LOCAL | curl chain documented in `docs/FIRST_CUSTOMER_REALITY_REPORT.md` |
| 595 unit/integration tests | PROVEN_LOCAL | `pytest -q --no-cov` |
| 79 new safety/brain/policy tests | PROVEN_LOCAL | this branch |
| Bilingual safety classifier | PROVEN_LOCAL | `tests/test_operator_saudi_safety.py` 31/31 |
| Company Brain aggregator | PROVEN_LOCAL | `tests/test_company_brain.py` 7/7 |
| Proof Ledger units (10 RWUs) | PROVEN_LIVE | `/api/v1/proof-ledger/units` |
| Proof Pack HMAC signature | BACKLOG | not implemented |
| Proof Pack hosted PDF | BACKLOG | Markdown only today |
| Postgres migration `deals.hubspot_deal_id` | PROVEN_LOCAL (idempotent) | `scripts/migrate_add_hubspot_deal_id.py` |
| Frontend pages 25/25 | PROVEN_LOCAL | `python -m http.server` 200s |
| Frontend services.html / operator.html / proof-pack.html | MISSING_OR_EMPTY | not built; functional equivalent via API |

## What this PR adds (status: PROVEN_LOCAL → ready for PR #131)

| File | Status |
| --- | --- |
| `auto_client_acquisition/safety/intent_classifier.py` | PROVEN_LOCAL |
| `auto_client_acquisition/customer_ops/company_brain.py` | PROVEN_LOCAL |
| `tests/test_operator_saudi_safety.py` (31 cases) | PROVEN_LOCAL |
| `tests/test_operator_bilingual_intent.py` | PROVEN_LOCAL |
| `tests/test_safe_action_gateway.py` | PROVEN_LOCAL |
| `tests/test_no_guaranteed_claims.py` | PROVEN_LOCAL |
| `tests/test_live_gates_default_false.py` | PROVEN_LOCAL |
| `tests/test_whatsapp_policy.py` (18 cases) | PROVEN_LOCAL |
| `tests/test_company_brain.py` | PROVEN_LOCAL |
| `tests/test_support_bot_bilingual.py` (with documented xfails) | PROVEN_LOCAL |
| `scripts/verify_service_tower.py` | PROVEN_LIVE (runs against prod) |
| `scripts/verify_delivery_workflows.py` | PROVEN_LIVE |
| `scripts/staging_smoke.sh` (upgraded) | PROVEN_LIVE |
| `scripts/migrate_add_hubspot_deal_id.py` | PROVEN_LOCAL (idempotent) |
| 21+ docs (this report, runbooks, matrices, playbooks) | PROVEN_LOCAL |

## Verdict

Today: **PROVEN_STAGING_READ_ONLY**.

After PR #131 merge + 4-line operator wiring patch + DB migration + Railway redeploy: **FIRST_CUSTOMER_READY_REALISTIC**.

Path to **PAID_BETA_READY** still requires: real customer payment +
real Proof Pack delivered + paid-beta policy doc — none of which can
be produced by this branch alone.
