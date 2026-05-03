# Dealix Final Cutover Evidence

> Re-verified 2026-05-03 against deploy branch
> `claude/launch-command-center-6P4N0` @ `bf8f6a0`
> (PR #132 merge `29d8e8f` + smoke-script + evidence updates).
> Every claim is backed by a command + output. No motivational claims.

## Verdict

```
DEALIX_FINAL_VERDICT=PROVEN_STAGING_READ_ONLY
```

To upgrade to `FIRST_CUSTOMER_READY_REALISTIC` requires:
- Railway redeploy of `claude/launch-command-center-6P4N0` HEAD `bf8f6a0`
- Prod migration `python scripts/migrate_add_hubspot_deal_id.py`
- Re-run staging smoke → expect `PASS=12 FAIL=0`

## Evidence Table

| Layer | Check | Expected | Actual | Evidence | Status | Blocker |
|---|---|---:|---:|---|---|---|
| Git | PR #132 in deploy branch | yes | yes | `git log` shows `29d8e8f fix: safe cutover for first customer readiness (#132)` | PASS | no |
| Git | HEAD bf8f6a0 or later | yes | yes | `git log -1 --oneline` → `bf8f6a0 fix(cutover): smoke script accepts safer 404 + tests Arabic cold-WA block` | PASS | no |
| Local | compileall | pass | pass | `python -m compileall -q api auto_client_acquisition db scripts` (no errors) | PASS | no |
| Local | architecture audit | 9/9 | 9/9 | `python scripts/repo_architecture_audit.py` → `RESULT: PASS` | PASS | no |
| Local | safety battery | pass | 82/82 | `pytest tests/test_operator_saudi_safety.py + bilingual + whatsapp_policy + safe_action_gateway + live_gates_default_false + no_guaranteed_claims + company_brain` → `82 passed in 9.22s` | PASS | no |
| Local | service tower | 6/6 | 6/6 | `BASE_URL=https://api.dealix.me python scripts/verify_service_tower.py` → `SERVICE_TOWER_OK bundles_verified=6` | PASS | no |
| Local | delivery workflows | 25/25 | 25/25 | `BASE_URL=https://api.dealix.me python scripts/verify_delivery_workflows.py` → `WORKFLOWS_VERIFY_OK 25/25` | PASS | no |
| Local | forbidden claims audit | clean | clean | `python scripts/forbidden_claims_audit.py` → `RESULT: PASS — 128 checks across 16 HTML pages` | PASS | no |
| Local | migration idempotent | pass | pass | `MIGRATION_OK column 'hubspot_deal_id' already present` (2 runs against fresh sqlite) | PASS | no |
| Local | frontend pages | 25/25 | 25/25 | local probe of `landing/*.html` returns 200 + ≥500 bytes for all 25 | PASS | no |
| Prod | `/` | 200 | 200 | `curl -i https://api.dealix.me/` | PASS | no |
| Prod | `/health` | 200 | 200 | `{"status":"ok","version":"3.0.0","env":"production","providers":["groq"]}` | PASS | no |
| Prod | `/docs` | 200 | 200 | `curl -i https://api.dealix.me/docs` | PASS | no |
| Prod | `/openapi.json` | 200 | 200 | OpenAPI returned, 306 paths | PASS | no |
| Prod | service catalog | 200 | 200 | `/api/v1/services/catalog` returns 6 bundles | PASS | no |
| Prod | English cold-WA blocked | pass | pass | smoke 6c: `unsafe English cold-WA blocked` | PASS | no |
| **Prod** | **Saudi Arabic cold-WA blocked** | **pass** | **fail 0/4** | direct operator probe: every Arabic phrasing returns `blocked=False intent=want_more_customers bundle=growth_starter` | **FAIL** | **YES** |
| Prod | WhatsApp live outbound | blocked | blocked | `POST /api/v1/os/test-send` → `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` | PASS | no |
| Prod | Gmail live send | blocked | blocked | `gmail_allow_live_send: bool = False` (settings.py:110) + no live route exposed | PASS | no |
| Prod | Moyasar live charge | blocked | blocked | no `/payments/charge` route on prod (404), only `/payments/manual-request` | PASS | no |
| Prod | LinkedIn automation | absent | absent | no automation route in OpenAPI | PASS | no |
| Prod | Resend live send | gated | gated | `resend_allow_live_send: bool = False` (settings.py:115) | PASS | no |
| Prod | Calls live dial | gated | 403 | `POST /api/v1/calls/dial-live → 403` (always until `CALLS_ALLOW_LIVE_DIAL=true`) | PASS | no |
| Prod | DB migration `deals.hubspot_deal_id` | present | pending | requires founder secret `DATABASE_URL` to verify | PENDING | YES |
| Business | first customer flow | manual fallback | manual_fallback | `docs/FIRST_CUSTOMER_REAL_PLAYBOOK.md` + `FIRST_CUSTOMER_EXECUTION_PACK.md` document the full curl chain; `payments/manual-request` returns bank-transfer SOP | PASS | no |
| Business | Outreach Go/No-Go | per docs | NO-GO | `docs/OUTREACH_GO_NO_GO.md` requires staging smoke green + Arabic cold-WA blocked on prod | NO-GO | derived |

## Production Smoke Summary

```
PASS=11
FAIL=1
Known failures:
  - unsafe Arabic cold-WA blocked 0/4 — production has not redeployed PR #132
    - أبي أرسل واتساب لأرقام مشتريها
    - أبي حملة واتساب على أرقام من السوق
    - أبي blast واتساب
    - أرسل لهم كلهم واتساب حتى لو ما وافقوا
```

## Local Test Summary

```
pytest:               full suite green at HEAD bf8f6a0 (last clean run 1016 passed)
architecture:         9/9 PASS
safety:               82 passed in 9.22s (8 files, ≥82 asserts)
service_tower:        SERVICE_TOWER_OK 6/6 (against prod openapi)
delivery_workflows:   WORKFLOWS_VERIFY_OK 25/25 (against prod openapi)
frontend:             25/25 200 (local landing server)
```

## Safety Summary

```
WhatsApp live outbound:   PROVEN_PROD_READ blocked (whatsapp_allow_live_send_false)
Cold WhatsApp:            English PROVEN_PROD_READ; Saudi Arabic STALE on prod (Railway not redeployed)
Gmail live send:          CONFIGURED_SAFE_OFF (gmail_allow_live_send=False)
LinkedIn automation:      ABSENT (no automation route)
Moyasar live charge:      CONFIGURED_SAFE_OFF + 404 on prod (no live-charge surface)
Resend live send:         CONFIGURED_SAFE_OFF (resend_allow_live_send=False)
Calls live dial:          CONFIGURED_SAFE_OFF (POST /api/v1/calls/dial-live → 403)
Secrets exposure:         none committed (only placeholder strings sk_live_xxxxx in deployment docs)
Guaranteed claims:        none in landing/ or classifier output (sweep clean, 128/128)
```

## First Customer GO/NO-GO

```
OUTREACH_GO=no
Reason: Production /api/v1/operator/chat/message does not yet block Saudi Arabic
        cold-WhatsApp phrasings. The fix is merged (29d8e8f) and additional
        evidence is on bf8f6a0, but Railway has not redeployed yet.

Required before outreach:
  1. Railway redeploy on claude/launch-command-center-6P4N0 @ bf8f6a0 (or later).
  2. Prod migration: DATABASE_URL='<railway pg>' python scripts/migrate_add_hubspot_deal_id.py
  3. Re-run staging smoke → expect PASS=12 FAIL=0.
  4. Re-probe operator with the 4 Arabic phrasings → expect blocked=true on all.
```

## Founder Actions

```
P0 TODAY:
1. Railway → service "dealix" → Deployments → Redeploy on
   claude/launch-command-center-6P4N0 HEAD bf8f6a0
   (includes PR #132 + smoke + evidence updates).
2. Run prod migration ONCE:
     DATABASE_URL='<paste Railway Postgres URL — never share in chat>' \
       python scripts/migrate_add_hubspot_deal_id.py
   Expected: MIGRATION_OK
3. Re-run smoke:
     BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
   Expected: PASS=12 FAIL=0

P1 BEFORE OUTREACH:
1. Re-read docs/OUTREACH_GO_NO_GO.md — confirm all 9 GO conditions are green.
2. Confirm by direct probe:
     curl -X POST https://api.dealix.me/api/v1/operator/chat/message \
       -H "Content-Type: application/json" \
       --data-binary '{"text":"أبي أرسل واتساب لأرقام مشتريها"}'
   Expected: "blocked": true.

P2 AFTER FIRST PAID PILOT:
1. Decide whether to flip MOYASAR_ALLOW_LIVE_CHARGE — only after a written
   refund/charge policy is published in docs/PAYMENTS_AND_BILLING_POLICY.md
   (still BACKLOG today).
2. Decide whether to flip WHATSAPP_ALLOW_LIVE_SEND — only after the
   approved-template path + ConsentRecord registry are wired and tested
   (BACKLOG).
```
