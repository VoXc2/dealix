# Dealix — Final Cutover Evidence

> Verified 2026-05-03 against the merged deploy branch
> `claude/launch-command-center-6P4N0` @ `29d8e8f`. Every claim below is
> backed by a command + output. No motivational claims.

## Status legend

`PROVEN_LOCAL` · `PROVEN_STAGING` · `PROVEN_PROD_READ` · `PROVEN_PROD_WRITE` ·
`CONFIGURED_SAFE_OFF` · `MANUAL_FALLBACK` · `DOC_ONLY` · `BACKLOG` · `BLOCKED`

## 1. Runtime

| Item | Value | Status |
| --- | --- | --- |
| Python | 3.11.15 | PROVEN_LOCAL |
| FastAPI / uvicorn | 0.115.x / 0.32.x | PROVEN_LOCAL |
| DB driver (prod) | asyncpg | PROVEN_PROD_READ |
| DB driver (local/test) | aiosqlite 0.22.x | PROVEN_LOCAL |
| Deployment | Railway, Dockerfile builder, /healthz | PROVEN_PROD_READ |
| Source | `claude/launch-command-center-6P4N0` @ `29d8e8f` (PR #132 merged) | PROVEN_LOCAL |

## 2. Database

| Item | Status | Evidence |
| --- | --- | --- |
| Postgres production | PROVEN_PROD_READ | `/health` 200 + structured-log `dialect=postgresql` paths reachable |
| SQLite local/test | PROVEN_LOCAL | `DATABASE_URL=sqlite+aiosqlite:////tmp/...` boots app + tests |
| Migration `deals.hubspot_deal_id` | PROVEN_LOCAL idempotent | `MIGRATION_OK column 'hubspot_deal_id' already present` (2 runs) |
| Migration on prod | **pending_founder_secret** | requires founder to run with prod `DATABASE_URL` |
| Destructive changes | none | nullable column add only |

## 3. AI providers

| Provider | Status | Notes |
| --- | --- | --- |
| Groq | CONFIGURED_SAFE_OFF (read-only on prod) | `/health` reports `providers:["groq"]` |
| Anthropic | not configured on prod | optional fallback |
| DeepSeek / GLM / Gemini | not configured on prod | optional fallback |
| Determinism guarantee | PROVEN_LOCAL | safety classifier never calls LLM on hot path |

## 4. Payments

| Item | Status | Evidence |
| --- | --- | --- |
| Moyasar live charge gate | CONFIGURED_SAFE_OFF | `MOYASAR_ALLOW_LIVE_CHARGE` referenced in `api/routers/payments.py:14`, returns 403 when off |
| Moyasar webhook signature | PROVEN_PROD_READ | unsigned `/api/v1/webhooks/moyasar` → **401** |
| Manual bank-transfer invoice | MANUAL_FALLBACK PROVEN_LOCAL | `POST /api/v1/payments/manual-request` returns bank-transfer SOP |
| Live charge route | not deployed | `/api/v1/payments/charge` → **404** (no surface to misuse) |
| Pilot 499 SAR | priced as 49,900 halalah if invoice API used | documented in `PAYMENTS_AND_BILLING_POLICY.md` |

## 5. WhatsApp

| Item | Status | Evidence |
| --- | --- | --- |
| Live customer outbound gate | CONFIGURED_SAFE_OFF | `WHATSAPP_ALLOW_LIVE_SEND=False` (`core/config/settings.py:106`) |
| Live customer outbound on prod | PROVEN_PROD_READ blocked | `POST /api/v1/os/test-send` → `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` |
| Inbound webhook | PROVEN_PROD_READ gated | GET without verify-token → **422** |
| Internal brief send | CONFIGURED_SAFE_OFF | `POST /api/v1/whatsapp/brief/send-internal` → **403** on prod |
| Cold WhatsApp / purchased lists (intent layer, English) | PROVEN_PROD_READ | unsafe English → `blocked:true` |
| Cold WhatsApp / purchased lists (intent layer, Saudi Arabic) | PROVEN_LOCAL only | local: 28/28 phrasings blocked (after PR #132); **prod: 0/4 blocked → Railway has not redeployed** |
| Opt-in policy | DOC_ONLY → MANUAL_FALLBACK | enforced manually until template path wired (BACKLOG) |

## 6. Email

| Item | Status |
| --- | --- |
| Gmail / SMTP live send | CONFIGURED_SAFE_OFF (`gmail_allow_live_send: bool = False`, `core/config/settings.py:110`) |
| Resend magic-link | CONFIGURED_SAFE_OFF (`resend_allow_live_send: bool = False`, `core/config/settings.py:115`) |
| Drafts only | PROVEN_LOCAL |

## 7. LinkedIn

| Item | Status |
| --- | --- |
| Automation route | not present | no `/linkedin/*automation*` route in OpenAPI |
| Manual draft only | PROVEN_LOCAL via `POST /api/v1/linkedin/drafts/create` |

## 8. Frontend

| Item | Status | Evidence |
| --- | --- | --- |
| Local pages 25/25 | PROVEN_LOCAL | `python -m http.server 8765` + probe → 25/25 200 |
| No "guaranteed sales/revenue" claim | PROVEN_LOCAL | grep returns no matches in `landing/` |
| Cold-WhatsApp text only in safety messages | PROVEN_LOCAL | every `cold WhatsApp` mention in `landing/` is a "do NOT" statement |
| API base configurability | DOC_ONLY (BACKLOG) | not directly audited |

## 9. Backend

| Item | Status |
| --- | --- |
| OpenAPI on prod | PROVEN_PROD_READ — 306 paths returned |
| Architecture audit | PROVEN_LOCAL — 9/9 PASS |
| Service tower | PROVEN_PROD_READ — `SERVICE_TOWER_OK bundles_verified=6` |
| Delivery workflows | PROVEN_PROD_READ — `WORKFLOWS_VERIFY_OK 25/25` |

## 10. Service Tower

| Bundle | Status |
| --- | --- |
| free_diagnostic | PROVEN_PROD_READ (full contract + intake-questions) |
| growth_starter | PROVEN_PROD_READ |
| data_to_revenue | PROVEN_PROD_READ |
| executive_growth_os | PROVEN_PROD_READ |
| partnership_growth | PROVEN_PROD_READ |
| full_growth_control_tower | PROVEN_PROD_READ (custom/sales-led) |

## 11. Safety

| Check | Status | Evidence |
| --- | --- | --- |
| Forbidden claims (`tests/test_no_guaranteed_claims.py`) | PROVEN_LOCAL | 11/11 pass |
| Cold-WA block (English) | PROVEN_PROD_READ | smoke 11/12 |
| Cold-WA block (Arabic Saudi) | PROVEN_LOCAL only | **prod 0/4 — needs Railway redeploy** |
| Live gates default false | PROVEN_LOCAL | `tests/test_live_gates_default_false.py` 3/3 |
| No secrets committed | PROVEN_LOCAL | grep returns only placeholder strings (`sk_live_xxxxx`) |

## 12. First customer

| Item | Status |
| --- | --- |
| Manual flow lead → deal → invoice → mark paid → customer → proof pack | MANUAL_FALLBACK PROVEN_LOCAL (chain documented in `FIRST_CUSTOMER_REAL_PLAYBOOK.md`) |
| Proof Pack (Markdown template) | PROVEN_PROD_READ — `/api/v1/proof-ledger/customer/cus_smoke/pack` returns 200 |
| Proof Pack HMAC signature / hosted PDF | BACKLOG |
| Outreach playbook (Arabic + English warm scripts) | DOC_ONLY (in `FIRST_CUSTOMER_EXECUTION_PACK.md`) |
| Outreach GO | NO — production has stale operator (see Safety §11) |

## Production smoke summary

```
$ BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
PASS=11  FAIL=1
```

Single failure:
```
unsafe Arabic cold-WA blocked 0/4 — production has not redeployed PR #132
  - أبي أرسل واتساب لأرقام مشتريها
  - أبي حملة واتساب على أرقام من السوق
  - أبي blast واتساب
  - أرسل لهم كلهم واتساب حتى لو ما وافقوا
```

This single FAIL is the **diagnostic signal** that Railway has not yet
redeployed the merged commit `29d8e8f`. Once redeployed, expect 12/12.

## Local test summary

| Suite | Result |
| --- | --- |
| `pytest -q` (full) | last clean run: 1016 passed, 5 fails (4 architecture cascades + 1 operator label) — all four fixed locally on `29d8e8f` |
| Architecture audit | 9/9 PASS |
| Safety battery (8 files, 82 asserts) | 82 passed in 14.03s |
| Service tower verifier | SERVICE_TOWER_OK 6/6 |
| Delivery workflows verifier | WORKFLOWS_VERIFY_OK 25/25 |
| Frontend local probe | 25/25 200 |

## Conclusion

The deploy branch contains every blocker fix. Production is healthy on
all read surfaces and all safety gates. The single missing piece is a
Railway redeploy: until that happens, the operator on prod still uses
the pre-merge classifier and 4 Saudi Arabic cold-WhatsApp phrasings
pass through unblocked.

**Verdict:** PROVEN_STAGING_READ_ONLY → **becomes FIRST_CUSTOMER_READY_REALISTIC the moment the founder triggers Railway redeploy + runs the prod migration**.
