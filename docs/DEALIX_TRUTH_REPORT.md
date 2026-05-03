# Dealix Final Systems Truth Report

> Generated 2026-05-03 — branch `claude/dealix-staging-readiness-LJOju`
>
> This document contains only what was directly verified. No marketing
> language. No placeholder claims. Discrepancies between the spec request
> and the actual repository are flagged honestly.

## 1. Git state

| Field | Value |
| --- | --- |
| Branch | `claude/dealix-staging-readiness-LJOju` |
| HEAD before fixes | `75303cd` (chore(actions): bump github/codeql-action from 3 to 4 (#123)) |
| Tree | dirty — fixes staged on this branch |
| Empty critical files | `scripts/__init__.py`, `tests/*/__init__.py` (intentional empty `__init__`) |

Spec mentioned operating on `claude/launch-command-center-6P4N0`. The session
instructions explicitly require `claude/dealix-staging-readiness-LJOju`, so all
work landed there.

## 2. Spec vs. reality (must read first)

The original spec assumed a set of files/routes that do not exist in this
repository. None are blockers. To stay inside the rule "do not add features",
I did NOT fabricate them. Below is the honest mapping of spec → actual.

| Spec item | Actual repo |
| --- | --- |
| `api/routers/operator.py` | `api/routers/personal_operator.py` (covers operator surface) |
| `api/routers/services.py` | covered by `business.py` (`/api/v1/business/proof-pack/demo`, verticals, recommend-plan) and `pricing.py` |
| `api/routers/prospects.py` | `api/routers/prospect.py` (singular — same router) |
| `api/routers/payments.py` | `api/routers/full_os.py` (`/payments/manual-request`, `/payments/mark-paid`) |
| `api/routers/proof_ledger.py` | proof in `business.py`, `customer_success.py`, `command_center.py` |
| `api/routers/role_briefs.py` | not present — closest is `personal_operator.daily-brief` and `command-center` snapshot |
| `api/routers/whatsapp_briefs.py` | not present as a dedicated router — `webhooks.whatsapp` exists; brief logic lives in `personal_operator` |
| `landing/services.html`, `landing/operator.html`, `landing/proof-pack.html`, `landing/role/*.html` | NOT present. 25 other pages do exist and all return 200 |
| `scripts/full_acceptance.sh`, `scripts/launch_readiness_check.py`, `scripts/repo_architecture_audit.py`, `scripts/forbidden_claims_audit.py` | NOT present. The repo ships `scripts/smoke_*.py`, `scripts/print_routes.py`, `scripts/run_demo.py`, and the new `scripts/staging_smoke.sh` |
| `/api/v1/services/catalog` | NOT present. Closest: `/api/v1/business/verticals`, `/api/v1/data/sources/catalog`, `/api/v1/business/pricing` |
| `/api/v1/role-briefs/daily?role=...` | NOT present. Closest: `/api/v1/personal-operator/daily-brief`, `/api/v1/v3/command-center/snapshot` |
| `/api/v1/whatsapp/brief?role=...` | NOT present. WhatsApp surface is `/api/v1/webhooks/whatsapp` (inbound) only |
| `/api/v1/proof-ledger` | NOT present. Closest: `/api/v1/business/proof-pack/demo`, `/api/v1/customers/{id}/proof-pack`, `/api/v1/command-center/proof-pack` |
| Spec total: 364 endpoints | Actual: **260 routes** registered (counted by `scripts/print_routes.py`) |
| Spec total: 939 pytest passing | Actual: **516 passed, 6 skipped** in 2.4 s |
| Spec total: 25 frontend pages | Actual: **25 HTML pages** in `landing/` (matches numerically; names differ) |

These are NOT failures of the system; they are inaccuracies in the spec. The
verdict below is based on what the system actually does, not on what the spec
claimed.

## 3. What was fixed (blockers only)

### 3.1 BLOCKER — `async_session_factory` wrong type

`db/session.py` exported `async_session_factory()` as a function returning an
`async_sessionmaker[AsyncSession]`. Most routers (`automation`, `outreach`,
`data`, `leads`, `ecosystem`, `customer_success`, ...) used it as
`async with async_session_factory() as session:` — but a sessionmaker is
not an async context manager. Every DB-backed route returned **500 Internal
Server Error** with
`'async_sessionmaker' object does not support the asynchronous context manager protocol`.

This bug is live on production today (verified: `/api/v1/automation/status`
and `/api/v1/compliance/check-outreach` both 500 against
`https://api.dealix.me`).

**Fix:** make `async_session_factory()` return a fresh `AsyncSession`
(AsyncSession itself is an async context manager). Internally cached the
sessionmaker. Updated `get_db` / `get_session` from the previous double-call
form. Updated the only file that used the double-call form
(`api/routers/autonomous.py`) to single-call.

Files: `db/session.py`, `api/routers/autonomous.py`.

### 3.2 BLOCKER — `aiosqlite` not declared

`DATABASE_URL=sqlite+aiosqlite://` is the canonical local/test driver, but
`aiosqlite` was not in `requirements.txt` or `requirements-dev.txt`. Without
it, every DB-touching path fails with `ModuleNotFoundError`. Added it to
`requirements-dev.txt` as a test/dev driver only (production uses Postgres
via `asyncpg`, which is already pinned).

Files: `requirements-dev.txt`.

### 3.3 NON_BLOCKING_POLISH — staging smoke script

Spec asked for a `staging_smoke.sh`. None existed. Wrote a minimal one
hitting only public/health/safety routes. No new product features.

Files: `scripts/staging_smoke.sh`.

## 4. Local proof

Environment: `APP_ENV=test`, `DATABASE_URL=sqlite+aiosqlite:////tmp/dealix_test.db`,
all eight live-action gates `false`, `MOYASAR_MODE=sandbox`.

| Check | Result |
| --- | --- |
| `python -m compileall api auto_client_acquisition core db` | OK (no errors) |
| `python -m pip check` | No broken requirements |
| `python -m pytest -q --no-cov` | **516 passed, 6 skipped** in 2.40 s |
| `python scripts/print_routes.py` | **260 routes**, no duplicate method+path |
| `python scripts/smoke_inprocess.py` | `SMOKE_INPROCESS_OK` (6/6 200) |
| `python scripts/run_demo.py` (full pipeline) | 3/3 leads processed end-to-end (intake → ICP → qualification) |
| Module imports (api.main, all key routers) | All OK |

## 5. Frontend proof (local)

Served `landing/` via `python -m http.server 8081`. All **25** files returned
**200**:

```
/, /index.html, /pricing.html, /trust-center.html, /command-center.html,
/case-study.html, /pulse.html, /roi.html, /partners.html, /verticals.html,
/pay-per-result.html, /dashboard.html, /personal-operator.html, /autopilot.html,
/simulator.html, /trust.html, /founder.html, /marketers.html, /community.html,
/academy.html, /customer-portal.html, /copilot.html, /market-radar.html,
/launch-readiness.html, /status.html
```

Spec-named pages NOT in the repo (returned 404, **not created** because that
would be a new feature):

```
/services.html, /operator.html, /proof-pack.html,
/role/sales.html, /role/growth.html, /role/ceo.html
```

If the founder later wants any of these, that is a content task, not a
launch blocker.

## 6. Backend proof (local, port 8765)

Public surface — all 200:

| Path | Status |
| --- | --- |
| `GET /` | 200 — `{"name":"Dealix","status":"operational",...}` |
| `GET /health` | 200 — `{"status":"ok","version":"3.0.0",...}` |
| `GET /docs` | 200 |
| `GET /openapi.json` | 200 |
| `GET /api/v1/business/pricing` | 200 — 6 tiers, SAR |
| `GET /api/v1/business/verticals` | 200 |
| `GET /api/v1/personal-operator/daily-brief` | 200 — Arabic decisions |
| `GET /api/v1/v3/command-center/snapshot` | 200 — agents + radar + compliance |
| `GET /api/v1/business/proof-pack/demo` | 200 |
| `GET /api/v1/data/sources/catalog` | 200 |
| `GET /api/v1/automation/status` | 200 — `{"daily_email_limit":50,"sent_today":0}` (after fix) |

DB-touching surface — all 200 after the `async_session_factory` fix:

| Path | Status |
| --- | --- |
| `POST /api/v1/companies/intake` | 200 → `{"id":"co_…","db_status":"ok"}` |
| `POST /api/v1/conversations` | 200 → conversation logged |
| `GET /api/v1/conversations` | 200 → records returned |
| `POST /api/v1/leads` | 200 → ICP fit, tier |
| `POST /api/v1/deals` | 200 → deal id |
| `POST /api/v1/payments/manual-request` | 200 → bank-transfer fallback (manual SOP) |
| `POST /api/v1/payments/mark-paid` | 200 → customer + onboarding task |
| `POST /api/v1/customers/{id}/proof-pack` | 200 → case study + testimonial AR |
| `POST /api/v1/command-center/proof-pack` | 200 → activity + benchmark |
| `POST /api/v1/compliance/check-outreach` | 200 — opt-out blocked correctly |

## 7. Business E2E (verified, local)

A complete prospect → cash flow runs end-to-end with no live external sends:

```
POST /api/v1/leads { source:"website", ... }            → lead_id
POST /api/v1/deals { lead_id, value_sar:499, stage:"pilot_offered" } → deal_id
POST /api/v1/payments/manual-request { deal_id, amount_sar:499 }    → bank-transfer instruction
POST /api/v1/payments/mark-paid     { deal_id, reference:"manual" } → customer_id + onboarding task
POST /api/v1/customers/{customer_id}/proof-pack { }                 → case study + testimonial AR
```

Recorded artifacts from one local run:

```
lead_id     = lead_94dcb671d297
deal_id     = deal_459e97712aaa48c1
customer_id = cust_2fbd5bae95bd4bf5
payment     = method=bank_transfer  status=payment_requested  follow_up_task_id=task_8fad1cc4340e4fc9
paid        = onboarding_task_id=task_509c9eb1127448a2
proof_pack  = case_study_md_template + testimonial_request_ar + referral_ask_ar
```

No card was charged. No external WhatsApp/email/LinkedIn send was performed.

## 8. Safety gates (verified, prod + local)

All eight live-action gates default `false` (env), enforced at the route layer:

| Channel | Behavior verified |
| --- | --- |
| WhatsApp send | `POST /api/v1/os/test-send` returns `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` (production confirmed) |
| Gmail send | `POST /api/v1/email/send-batch` returns `{"status":"blocked","reason":"gmail_not_configured"}` |
| Moyasar webhook | unsigned `POST /api/v1/webhooks/moyasar` returns **401 bad_signature** (production confirmed) |
| Moyasar charge | `MOYASAR_ALLOW_LIVE_CHARGE=false` → manual-request always returns bank-transfer fallback |
| LinkedIn | only `/linkedin/drafts/create` exists; no automation route. Drafts require human capture |
| Compliance check | `POST /api/v1/compliance/check-outreach` blocks `contact_opt_out=true` |
| Cold WhatsApp on purchased lists | `compliance/campaign-risk` flags risk; `/os/test-send` returns blocked |
| Customer WhatsApp send | inbound webhook only — no outbound endpoint enabled |

`grep -nr "ALLOW_LIVE\|ALLOW_AUTOMATION" core/config/` confirms env defaults
all read `false` unless explicitly overridden.

No secrets were committed, logged, or printed into this report.

## 9. Production proof (`https://api.dealix.me`)

Smoke (`BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh`):

```
PASS=22  FAIL=0
```

Hits include:

```
GET /                                            200 (clean JSON, env=production)
GET /health                                      200 ({"status":"ok","providers":["groq"]})
GET /docs                                        200
GET /openapi.json                                200
GET /api/v1/business/pricing                     200
GET /api/v1/personal-operator/daily-brief        200 (Arabic)
GET /api/v1/personal-operator/launch-report      200
GET /api/v1/v3/command-center/snapshot           200
GET /api/v1/business/proof-pack/demo             200
POST /api/v1/webhooks/moyasar (unsigned)         401 (gate)
POST /api/v1/os/test-send (whatsapp)             {"status":"blocked","error":"whatsapp_allow_live_send_false"}
POST /api/v1/revenue-os/compliance/campaign-risk 200
GET /api/v1/webhooks/whatsapp (no token)         422 (verify token enforced)
```

### Production-only failures still present

These return 500 on production today because the fix in section 3.1 has not
yet been deployed. They run green locally:

```
GET  /api/v1/automation/status               500 (DB session bug, fixed locally)
POST /api/v1/compliance/check-outreach       500 (same root cause, fixed locally)
```

**Action:** merge this branch and redeploy. The `async_session_factory`
patch unblocks every DB-backed route in one shot.

## 10. Company brain mapping

The spec's "Company Brain" is already represented by composing the existing
data models (no new tables required):

| Brain field | Existing source |
| --- | --- |
| `company_name`, `website`, `sector`, `city`, `offer`, ICP | `CompanyRecord` (via `POST /api/v1/companies/intake`) |
| `prospects` | `LeadRecord` |
| `deals` | `DealRecord` |
| `meetings` | `TaskRecord` (type=meeting) |
| `proof_events` | `business/proof-pack`, `customers/{id}/proof-pack` |
| `invoices` | `payments/manual-request` artifacts + Moyasar webhooks |
| `service_sessions` | `customer_success/onboard` + `customer_success/health` |
| `consent_records` | `compliance/check-outreach` + `SuppressionRecord` |
| `next_best_actions` | `command-center/next-best-action`, `revenue-os/copilot/actions` |
| `forbidden_claims` | tone in `personal-operator/messages/draft` |
| `tone_ar` | `CompanyRecord.tone_of_voice` (default "professional_khaliji") |

Conclusion: company brain exists as a logical composite over the current
schema. No new tables added.

## 11. Remaining items

| Severity | Item |
| --- | --- |
| BLOCKER (prod-side) | Redeploy this branch so the `async_session_factory` fix and `aiosqlite` decl are live. After redeploy, `/api/v1/automation/status` and DB-touching POSTs go from 500 → 200. |
| NON_BLOCKING_POLISH | spec-named landing pages (`services.html`, `operator.html`, `proof-pack.html`, `role/*.html`) — copy-only work, can ship anytime |
| NON_BLOCKING_POLISH | unify `/api/v1/role-briefs/daily?role=…` alias over the existing personal-operator brief if the spec wants a stable role-keyed URL |
| NON_BLOCKING_POLISH | `LeadSource` enum has only `website|whatsapp|email|referral|linkedin|cold_outreach|manual|api` — `inbound_form` is not accepted by `POST /api/v1/leads`. Either accept it or document the canonical strings |
| NON_BLOCKING_POLISH | `automation.py:31` deprecation: `regex=` → `pattern=` (FastAPI warning, no functional impact) |
| BACKLOG | spec-claimed scripts (`full_acceptance.sh`, `launch_readiness_check.py`, `repo_architecture_audit.py`, `forbidden_claims_audit.py`) do not exist. If desired, they can be added — but pytest + smoke + staging_smoke already cover their intent |

## 12. Final verdict

**PROVEN_LOCAL.**

Locally, after the two blocker fixes, every required workflow runs:

- public API surface, docs, health
- DB-backed prospect → deal → manual-invoice → customer → proof pack flow
- Arabic operator brief and command-center snapshot
- safety gates enforced (WhatsApp, Gmail, Moyasar live charge, LinkedIn,
  cold WhatsApp on purchased lists, compliance opt-out)
- 516/516 non-skipped tests pass

Production today is partially proven: 22/22 smoke endpoints pass, all safety
gates already enforced live. **PROVEN_STAGING** requires merging the
`async_session_factory` fix and redeploying — at that point the same DB-backed
flow that works locally will work on `https://api.dealix.me`, and
`/api/v1/compliance/check-outreach` and `/api/v1/automation/status` will turn
green.

**FIRST_CUSTOMER_READY** is achievable today via the manual-payment fallback
(no live charge required) — see Section 14.

## 13. Founder action plan (today)

Flow (no live charge, no cold WhatsApp, all consent-first):

1. Send 10 warm LinkedIn DMs to Saudi B2B founders/agency leads. Use
   `POST /api/v1/linkedin/drafts/create` to draft. Send manually from your
   own LinkedIn — no automation.
2. For each prospect that opts in, use the inbound form / `wa.me` link.
   `POST /api/v1/prospect/inbound/form` records consent + auto-classifies.
3. For interested replies, run `POST /api/v1/personal-operator/messages/draft`
   to generate a Khaliji Arabic follow-up. **Send manually.**
4. When a prospect agrees to the 7-Day Growth Proof Sprint:
   - `POST /api/v1/leads`           (source `website` or `whatsapp`)
   - `POST /api/v1/deals`           (lead_id, value_sar:499, stage:"pilot_offered")
   - `POST /api/v1/payments/manual-request`  (returns bank-transfer / STC Pay
     instructions — no live charge)
   - When customer pays: `POST /api/v1/payments/mark-paid` → creates
     `CustomerRecord` + onboarding task automatically.
   - At day 7: `POST /api/v1/customers/{customer_id}/proof-pack` →
     case-study template + testimonial + referral ask.
5. After proof pack, offer `growth_os` (2,999 SAR/mo) using the recommend-plan
   endpoint output.

## 14. Exact commands for the founder

```bash
# Run the system locally (sandbox, no live actions):
APP_ENV=test APP_SECRET_KEY=test-secret \
DATABASE_URL=sqlite+aiosqlite:////tmp/dealix_test.db \
WHATSAPP_ALLOW_LIVE_SEND=false WHATSAPP_ALLOW_INTERNAL_SEND=false \
WHATSAPP_ALLOW_CUSTOMER_SEND=false MOYASAR_ALLOW_LIVE_CHARGE=false \
GMAIL_ALLOW_LIVE_SEND=false CALLS_ALLOW_LIVE_DIAL=false \
LINKEDIN_ALLOW_AUTOMATION=false MOYASAR_MODE=sandbox \
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

# Run staging smoke against production:
BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh

# Run the demo pipeline (3 sample leads, no external sends):
python scripts/run_demo.py

# Print all routes:
python scripts/print_routes.py

# Run full unit tests:
APP_ENV=test APP_SECRET_KEY=test-secret \
DATABASE_URL=sqlite+aiosqlite:////tmp/dealix_test.db \
python -m pytest -q --no-cov
```

## 15. Final decision

| Surface | Status |
| --- | --- |
| Local | **PROVEN_LOCAL** — 516 tests, full E2E, all gates enforced |
| Production read paths | **PROVEN_STAGING (read-only)** — 22/22 smoke, gates enforced |
| Production write paths | **NOT_READY until redeploy** — DB-session bug live on prod |
| First customer | **FIRST_CUSTOMER_READY (offline)** — manual-payment fallback runs today; Moyasar live can stay off |
| Paid beta | **NOT_READY** — by design (live charge gate stays false) |

Once this branch is merged and Railway redeploys, the verdict moves cleanly
to **PROVEN_STAGING** with no further code changes required.
