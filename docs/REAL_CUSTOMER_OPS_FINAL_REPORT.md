# Dealix Real Customer Ops Final Report

> Generated 2026-05-03 — branch `claude/dealix-staging-readiness-LJOju`,
> HEAD `624fe13`. Verified against `https://api.dealix.me`.

## Verdict

**PROVEN_STAGING_READ_ONLY** with a documented path to **FIRST_CUSTOMER_READY**.

- Public API and service-tower **reads** are PROVEN_LIVE on prod (22/22).
- Operator chat is PROVEN_LIVE for English + obvious Arabic, with **3
  Arabic Saudi safety misses** that need a small classifier patch on the
  deploy branch before declaring FIRST_CUSTOMER_READY for self-serve users.
- DB-write paths on prod are blocked by an `async_session_factory` bug
  (fix exists on this branch — needs merge + Railway redeploy).
- Local: 516 tests pass, full first-customer flow runs end-to-end with
  manual-payment fallback. **PROVEN_LOCAL**.

## Git State

```
branch  : claude/dealix-staging-readiness-LJOju  (per session rule)
HEAD    : 624fe13  fix(db): resolve async_session_factory contract mismatch
status  : clean (after this report's writes — see git status before commit)
remote  : pushed
```

The PRODUCTION runtime is on a different branch, `claude/launch-command-center-6P4N0`,
which is far ahead with ~46 additional routers (operator, services,
role-briefs, whatsapp/brief, support, partners-portal, observability,
calls, cards, daily-ops, delivery, intelligence, learning, meetings,
negotiation, onboarding, proof-ledger, prospects, self-growth/-ops,
sprints, founder, auth, inbound, actions). Per session rules I did NOT
push there.

## What was fixed (this session)

- Confirmed the prior session's two fixes still hold locally:
  1. `db/session.py` — `async_session_factory()` returns AsyncSession (not sessionmaker)
  2. `requirements-dev.txt` — `aiosqlite` added
  3. `api/routers/autonomous.py` — single-call form
- Added new evidence + matrices (this session):
  - `docs/REAL_CUSTOMER_OPS_TRUTH_REPORT.md`
  - `docs/SERVICE_TOWER_REALITY_MATRIX.md`
  - `docs/OPERATOR_LANGUAGE_AND_INTENT_TESTS.md`
  - `docs/SUPPORT_BOT_REALITY_MATRIX.md`
  - `docs/WHATSAPP_POLICY_AND_FLOW.md`
  - `docs/COMPANY_BRAIN_SPEC_AND_STATUS.md`
  - `docs/FRONTEND_REALITY_MATRIX.md`
  - `docs/API_REALITY_MATRIX.md`
  - `docs/FIRST_CUSTOMER_REALITY_REPORT.md`
  - `docs/TOOLS_AND_SKILLS_INVENTORY.md`
- No new product features added. No live-action gates flipped.

## What was proven locally

```
$ APP_ENV=test ... python -m pytest -q --no-cov
516 passed, 6 skipped in 4.50s

$ python scripts/print_routes.py
TOTAL_ROUTE_ROWS 260
ROUTE_CHECK_OK no duplicate method+path

$ python scripts/smoke_inprocess.py
SMOKE_INPROCESS_OK

$ python scripts/run_demo.py
3/3 leads through pipeline (intake → ICP → qualification → done)

# E2E demo flow (lead → deal → manual invoice → mark paid → customer → proof pack):
lead_id     = lead_2be6aaae9444     ← POST /api/v1/leads
deal_id     = deal_14e3ed3697d5405f ← POST /api/v1/deals
invoice_req = bank_transfer fallback ← POST /api/v1/payments/manual-request
customer_id = cust_e49e5bb76d3c4851  ← POST /api/v1/payments/mark-paid
proof_pack  = case_study + testimonial + referral AR
compliance  = blocks contact_opt_out=true
```

## What was proven on api.dealix.me

```
$ BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
PASS=22  FAIL=0
```

22/22 endpoints OK including:
- `/`, `/health`, `/docs`, `/openapi.json`
- `/api/v1/services/catalog` (6 bundles)
- `/api/v1/services/{bundle_id}` per bundle
- `/api/v1/services/{bundle_id}/intake-questions`
- `/api/v1/role-briefs/roles` and `/api/v1/role-briefs/daily?role=growth_manager|ceo|customer_success|compliance|revops`
- `/api/v1/whatsapp/brief?role=growth_manager`
- `/api/v1/business/pricing`, `/api/v1/business/proof-pack/demo`
- `/api/v1/v3/command-center/snapshot`
- `/api/v1/proof-ledger/units`
- `/api/v1/support/sla`, `/api/v1/support/classify`
- `/api/v1/operator/chat/message` (with caveats below)
- safety: `webhooks/moyasar` unsigned 401, `os/test-send` blocked, `webhooks/whatsapp` GET 422

## What is still NOT proven

| Concern | Status | Evidence |
| --- | --- | --- |
| `/api/v1/automation/status` | BLOCKER on prod | 500 — AsyncSession bug fixed locally, not yet deployed |
| `/api/v1/compliance/check-outreach` | BLOCKER on prod | same root cause |
| `/api/v1/role-briefs/daily?role=sales_manager` | BLOCKER on prod | DB schema — `column deals.hubspot_deal_id does not exist` |
| `/api/v1/whatsapp/brief?role=sales_manager`, `?role=ceo` | BLOCKER on prod | same schema mismatch |
| `/api/v1/role-briefs/daily?role=marketing_manager`, `?role=finance_manager` | 400 — role names mismatch | spec used `marketing_manager`, code expects `growth_manager`; spec used `finance_manager`, code expects `finance` |
| Operator Saudi-Arabic cold-WA blocking | BLOCKER on prod | 3 of 14 scenarios miss the block — see OPERATOR_LANGUAGE_AND_INTENT_TESTS.md |
| HMAC-signed proof pack | BACKLOG | response lacks signature field |
| Hosted PDF proof pack | BACKLOG | currently Markdown only |
| Frontend pages `services.html`, `operator.html`, `proof-pack.html`, `support.html`, `onboarding.html`, `role/*.html` | MISSING_OR_EMPTY | not required for sales-led first customer; required for self-serve UX |
| Prod write paths (POST DB) | not exercised against prod | by design — would write fake data into a customer DB |

## Service Tower Status

6/6 bundles registered live with full contract objects. Intake questions
present. Pricing visible. Safety policy ("approval-first, no cold WhatsApp")
in `safe_policy_ar`. **PROVEN_LIVE.** See SERVICE_TOWER_REALITY_MATRIX.md.

## Operator Language Status

| Language | Pass rate | Notes |
| --- | --- | --- |
| Arabic Saudi | 6 / 9 | 3 cold-WA misses |
| English | 4 / 4 | clean |
| Mixed AR/EN | 2 / 3 | "blast واتساب" missed |
| **Overall** | **10 / 14** | **3 SAFETY MISSES on prod** |

Detail: OPERATOR_LANGUAGE_AND_INTENT_TESTS.md.

## Support Bot Status

`/support/sla` + `/support/classify` PROVEN_LIVE; tickets endpoint
CODE_EXISTS_NOT_PROVEN. SLA matrix P0–P3 with Arabic labels live.
Classifier escalates billing/legal/outage. See SUPPORT_BOT_REALITY_MATRIX.md.

## WhatsApp Policy Status

`WHATSAPP_ALLOW_LIVE_SEND=false` enforced live. Customer outbound
blocked. Inbound webhook signature gate enforced. No template send
wired. `whatsapp/brief` works for some roles, BLOCKER for sales_manager
and ceo (same DB schema bug). See WHATSAPP_POLICY_AND_FLOW.md.

## Company Brain Status

Logical composite over existing models — no new tables needed. Field
map verified in COMPANY_BRAIN_SPEC_AND_STATUS.md. PROVEN_LIVE for the
component reads; no unified `companies/{id}/brain` aggregator exists
(BACKLOG).

## Frontend Status

25 actual landing pages all 200 locally. 6 spec-claimed pages missing
(BACKLOG, not blocker for sales-led first customer). API base
configurability not audited this session (CODE_EXISTS_NOT_PROVEN).
Some `cta_path` values from the live services catalog point at pages
not in this branch's `landing/`. See FRONTEND_REALITY_MATRIX.md.

## Backend / API Status

- prod openapi: 306 paths
- local openapi: 260 paths
- 22/22 prod smoke green
- 5 BLOCKERs on prod (above)
- See API_REALITY_MATRIX.md.

## Business E2E Status

PROVEN_LOCAL (full chain). PROVEN_STAGING_READ_ONLY on prod. Will be
PROVEN_STAGING_WRITE_SAFE after the AsyncSession fix lands on the
deploy branch + Railway redeploy.

## Safety Gates

| Gate | Status |
| --- | --- |
| Cold WhatsApp blocked (channel level) | ✅ PROVEN_LIVE |
| Cold WhatsApp blocked (intent level, English) | ✅ PROVEN_LIVE |
| Cold WhatsApp blocked (intent level, Saudi Arabic) | ❌ **PARTIAL — 3/9 miss** |
| Live WhatsApp customer outbound | ✅ blocked by `WHATSAPP_ALLOW_LIVE_SEND=false` |
| Gmail live send | ✅ blocked (`gmail_configured()=false`) |
| Moyasar live charge | ✅ falls back to manual bank transfer when no `MOYASAR_SECRET_KEY` |
| Moyasar webhook signature | ✅ 401 on unsigned (verified live) |
| LinkedIn automation | ✅ no automation route exists; only drafts |
| Live phone dial | ⚠️ `calls/dial-live` exists on deploy — gate not verified |
| Opt-out respected | ✅ PROVEN_LOCAL |
| No "guaranteed" claims | ✅ catalog uses approval-first language |

## First Customer Playbook

Today, sales-led, no live external action needed:

1. Founder confirms `https://api.dealix.me/health` returns 200.
2. Founder opens `https://api.dealix.me/docs` and verifies key bundles.
3. Founder sends 10 warm LinkedIn DMs to Saudi B2B founders / agency leads.
   No automation. No purchased lists.
4. Each prospect that opts in fills the inbound form / `wa.me` link →
   `POST /api/v1/prospect/inbound/form` records consent and classifies.
5. For interested prospects, Founder runs the **Free Diagnostic**:
   `POST /api/v1/operator/service/start {bundle_id:"free_diagnostic", company_name, sector, …}`
6. Founder delivers the diagnostic in a Khaliji Arabic doc within 24h.
7. If prospect agrees to **7-Day Growth Proof Sprint** at 499 SAR:
   - `POST /api/v1/leads` (the prospect)
   - `POST /api/v1/deals { lead_id, value_sar:499, stage:"pilot_offered" }`
   - `POST /api/v1/payments/manual-request { deal_id, amount_sar:499 }`
     → returns bank transfer / STC Pay instruction (no live charge)
   - When customer pays: `POST /api/v1/payments/mark-paid { deal_id, reference }`
     → creates CustomerRecord + onboarding task
8. Day 7: `POST /api/v1/customers/{customer_id}/proof-pack` → case-study
   template + testimonial + referral asks. Founder fills in metrics.
9. Founder asks customer for testimonial + 1 referral.
10. Only AFTER proof: offer `executive_growth_os` (2,999 SAR/mo).

This is the path to **FIRST_CUSTOMER_READY** without flipping any live
gate.

## Founder Actions Required

Ranked by what unblocks the most:

| # | Action | Effect |
| - | --- | --- |
| 1 | **Railway Redeploy** the deploy branch after merging the AsyncSession fix from `claude/dealix-staging-readiness-LJOju` (or cherry-pick `db/session.py` + `api/routers/autonomous.py`) | turns 5 BLOCKER endpoints green |
| 2 | Patch the operator-chat classifier (deploy branch) with the Saudi Arabic phrase signals listed in OPERATOR_LANGUAGE_AND_INTENT_TESTS.md §"Recommended fix" | closes 3 SAFETY MISSES |
| 3 | Add an Alembic migration (or run `POST /api/v1/admin/recreate-tables` if safe in your environment) so prod Postgres has `deals.hubspot_deal_id` | turns the role-brief / whatsapp-brief sales_manager + ceo from 500 → 200 |
| 4 | (env-only, no live actions) confirm Railway has `WHATSAPP_ALLOW_LIVE_SEND=false` and `MOYASAR_SECRET_KEY` either unset or set to **sandbox** key. Do NOT set live keys yet. | preserves safety |
| 5 | Send the first 10 warm LinkedIn DMs manually | starts the funnel |
| 6 | When a real prospect responds, run the playbook above | first-customer flow |

## Founder Action Plan (today)

```
1. curl -fsSI https://api.dealix.me/health  # confirm 200
2. open https://api.dealix.me/docs          # confirm Swagger
3. open https://github.com/VoXc2/dealix/pulls  # merge AsyncSession fix into deploy branch
4. Railway → Deployments → Redeploy
5. Re-run: BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
   Expected after redeploy: PASS=22 FAIL=0 AND /automation/status, /compliance/check-outreach turn green
6. Send 10 warm LinkedIn DMs from your own account (no automation, no purchased lists)
7. For each opt-in: run the Free Diagnostic → 499 Pilot → Proof Pack flow above
```

## Final Decision

| Surface | Verdict |
| --- | --- |
| Local | PROVEN_LOCAL |
| Prod (read) | PROVEN_STAGING_READ_ONLY |
| Prod (write, after redeploy + classifier patch) | path to PROVEN_STAGING_WRITE_SAFE then FIRST_CUSTOMER_READY |
| Paid Beta | NOT_READY (by design — live gates remain false) |
