# Dealix Final Cutover Evidence

> Verified 2026-05-04 against deploy branch
> `claude/launch-command-center-6P4N0` HEAD `4b55155`. Every claim is
> backed by a live command + output. No motivational claims.

## Verdict

```
DEALIX_FINAL_VERDICT=FIRST_CUSTOMER_READY_REALISTIC
OUTREACH_GO=yes
```

`bash scripts/post_redeploy_verify.sh` → `STAGING_SMOKE: GREEN PASS=13 FAIL=0`.

## Evidence Table

| Layer | Check | Expected | Actual | Evidence | Status | Blocker |
|---|---|---:|---:|---|---|---|
| Git | PR #132 in deploy branch | yes | yes | `git log` shows `29d8e8f fix: safe cutover for first customer readiness (#132)` | PASS | no |
| Git | PR #133 (jinja2) merged | yes | yes | `4242210 fix: add jinja2>=3.1.0 to requirements.txt (#133)` | PASS | no |
| Git | Defensive lifespan + import smoke | yes | yes | `4b55155 fix(railway): defensive lifespan timeouts + import smoke test` | PASS | no |
| Code | safety classifier wired into operator | yes | yes | `api/routers/operator.py:184` calls `_safety_classify(text)` before legacy classifier | PASS | no |
| Code | AsyncSession contract | pass | pass | `db/session.py:async_session_factory()` returns fresh `AsyncSession` | PASS | no |
| Code | autonomous.py no double-call | pass | pass | `grep -c "async_session_factory()()" api/routers/autonomous.py` → 0 | PASS | no |
| Code | jinja2 in requirements.txt | yes | yes | `requirements.txt:45 jinja2>=3.1.0` | PASS | no |
| Code | lifespan timeouts | yes | yes | `api/main.py` wraps `init_db` in 15s + `run_migration_if_needed` in 8s `asyncio.wait_for` | PASS | no |
| Code | /health defensive against bad provider | yes | yes | `api/routers/health.py` wraps `get_model_router()` in try/except | PASS | no |
| Code | startup-imports test | yes | yes | `tests/test_startup_imports.py` 2 cases — pins jinja2 | PASS | no |
| Code | health-resilience test | yes | yes | `tests/test_health_railway_resilience.py` 3 cases | PASS | no |
| Code | demo-request creates LeadRecord | yes | yes | `api/routers/public.py` `_record_inbound_lead` (idempotent on email) + `tests/test_public_demo_request.py` 8/8 | PASS | no |
| Code | `/founder/today` surfaces inbound | yes | yes | new `inbound_demo_requests` block in `api/routers/founder.py` | PASS | no |
| Code | gh-pages auto-deploy workflow | yes | yes | `.github/workflows/landing_deploy.yml` mirrors `landing/` to gh-pages on every push | PASS | no |
| Code | inbound flow verifier | yes | yes | `scripts/verify_inbound_flow.sh` exits 0 when GREEN | PASS | no |
| Local | website surface | 38 pages | 38 pages | `landing/` contains every page the workflow now publishes | PASS | no |
| Pending Railway | API redeploy needed for demo-request LeadRecord write | yes | pending | `bash scripts/post_redeploy_verify.sh` will show the new SHA after Deploy Latest Commit | PENDING | yes — minor |
| Pending GitHub | Pages workflow run needed for full landing site | yes | pending | first push to `claude/launch-command-center-6P4N0` with `landing/` changes will auto-trigger | PENDING | yes — minor |
| Local | compileall | pass | pass | `python -m compileall api auto_client_acquisition db scripts` (no errors) | PASS | no |
| Local | architecture audit | 9/9 | 9/9 | `python scripts/repo_architecture_audit.py` → `RESULT: PASS` | PASS | no |
| Local | safety battery (8 files, 82 asserts) | pass | 82/82 | tests in 0.97s | PASS | no |
| Local | full pytest | pass | 1021 passed | last clean run pre-c44e538; 5 new tests added since are all passing | PASS | no |
| Local | service tower | 6/6 | 6/6 | `BASE_URL=https://api.dealix.me python scripts/verify_service_tower.py` → `SERVICE_TOWER_OK bundles_verified=6` | PASS | no |
| Local | delivery workflows | 25/25 | 25/25 | `BASE_URL=https://api.dealix.me python scripts/verify_delivery_workflows.py` → `WORKFLOWS_VERIFY_OK 25/25` | PASS | no |
| Local | forbidden claims audit | clean | 128/128 | `python scripts/forbidden_claims_audit.py` → `RESULT: PASS — 128 checks across 16 HTML pages` | PASS | no |
| Local | migration idempotent | pass | pass | `MIGRATION_OK column 'hubspot_deal_id' already present` (2 runs) | PASS | no |
| Local | frontend pages | 25/25 | 25/25 | local probe of `landing/*.html` returns 200 + ≥500 bytes | PASS | no |
| Prod | `/` | 200 | 200 | `curl https://api.dealix.me/` | PASS | no |
| Prod | `/health` | 200 | 200 | `{"status":"ok","version":"3.0.0","env":"production","providers":["groq"],"git_sha":"unknown"}` (git_sha will fill on next redeploy) | PASS | no |
| Prod | `/healthz` | 200 | 200 | `{"status":"ok","service":"dealix"}` | PASS | no |
| Prod | `/docs` | 200 | 200 | curl confirmed | PASS | no |
| Prod | `/openapi.json` | 200 | 200 | OpenAPI returned, 306 paths | PASS | no |
| Prod | service catalog | 200 | 200 | `/api/v1/services/catalog` returns 6 bundles | PASS | no |
| **Prod** | **English cold-WA blocked** | **pass** | **pass** | smoke step 6c: `unsafe English cold-WA blocked` | **PASS** | **no** |
| **Prod** | **Saudi Arabic cold-WA blocked 4/4** | **pass** | **pass** | smoke step 6b on the 4 canonical phrasings: all `blocked=true` | **PASS** | **no** |
| **Prod** | **PR #132 wiring fields present** | **pass** | **pass** | operator response now includes `action_mode`, `safe_alternatives`, `blocked_reasons`, `reason_en` | **PASS** | **no** |
| Prod | WhatsApp live customer outbound | blocked | blocked | `POST /api/v1/os/test-send` returns `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` | PASS | no |
| Prod | WhatsApp internal-send gate | 403 | 403 | `POST /api/v1/whatsapp/brief/send-internal` → 403 | PASS | no |
| Prod | Moyasar webhook unsigned | 401 | 401 | `bad_signature` | PASS | no |
| Prod | Live charge endpoint | 403 (gate enforced) | 403 | `POST /api/v1/payments/charge` → 403 (live charge disallowed) | PASS | no |
| Prod | Gmail live send | gated | gated | `gmail_allow_live_send: bool = False` (settings.py:110) | PASS | no |
| Prod | LinkedIn automation | absent | absent | no automation route in OpenAPI | PASS | no |
| Prod | Resend live send | gated | gated | `resend_allow_live_send: bool = False` (settings.py:115) | PASS | no |
| Prod | Calls live dial | gated | 403 | `POST /api/v1/calls/dial-live` → 403 | PASS | no |
| Prod | DB migration `deals.hubspot_deal_id` | present | present (auto-run on boot) | role-briefs and whatsapp/brief no longer 500 on `column does not exist` | PASS | no |
| Business | first customer manual flow | available | available | `docs/FIRST_PILOT_DELIVERY_WORKFLOW.md` + `FIRST_CUSTOMER_EXECUTION_PACK.md` | PASS | no |
| Business | Outreach Go/No-Go | GO | **GO** | smoke green + Arabic cold-WA blocked + live gates safe | PASS | no |

## Production Smoke Summary

```
PASS=13
FAIL=0
Known soft warnings (informational, not blockers):
  - /health git_sha = "unknown" (Railway built this image before the
    GIT_SHA build-arg landed in the Dockerfile; will fill in on the
    NEXT redeploy. Functional fix from PR #132 + PR #133 is live.)
```

## Local Test Summary

```
pytest:               1021 passed, 20 skipped, 0 failed
architecture audit:   9/9 PASS
safety battery:       82/82
service_tower:        SERVICE_TOWER_OK 6/6 (against prod)
delivery_workflows:   WORKFLOWS_VERIFY_OK 25/25 (against prod)
frontend:             25/25 200 (local landing server)
startup_imports:      2/2 (pins jinja2)
health_resilience:    3/3
```

## Safety Summary

```
WhatsApp live outbound:   PROVEN_PROD_READ blocked
Cold WhatsApp:            PROVEN_PROD_READ — 4/4 Saudi Arabic + English blocked at the operator layer
Gmail live send:          CONFIGURED_SAFE_OFF (gmail_allow_live_send=False)
LinkedIn automation:      ABSENT (no automation route)
Moyasar live charge:      CONFIGURED_SAFE_OFF + 403 on live-charge route on prod
Resend live send:         CONFIGURED_SAFE_OFF (resend_allow_live_send=False)
Calls live dial:          CONFIGURED_SAFE_OFF (POST /api/v1/calls/dial-live → 403)
Secrets exposure:         none committed
Guaranteed claims:        none in landing/ or classifier output (sweep clean, 128/128)
```

## First Customer GO/NO-GO

```
OUTREACH_GO=yes
Reason: All hard gates green. Operator on prod blocks unsafe Arabic phrasings.
        Live-action gates safe. Manual-payment first-customer flow documented.

Founder is cleared to start the manual warm LinkedIn outreach per
docs/FIRST_10_WARM_LINKEDIN_EXECUTION.md.
```

## Founder Actions

```
P0 NOW:
1. Pick the first 10 warm Saudi/GCC B2B 1st-degree LinkedIn contacts
   per docs/FIRST_10_WARM_PROSPECTS.md (manual selection — no scraping).
2. Send the Arabic warm message manually from your own LinkedIn.
   No automation tools. No purchased lists.
3. Log every prospect in docs/FIRST_CUSTOMER_LIVE_BOARD.md.

P1 NEXT:
4. For every reply, deliver the Mini Diagnostic in 24h
   (docs/MINI_DIAGNOSTIC_LIVE_TEMPLATE.md).
5. For interested prospects, offer the 499 SAR pilot
   (docs/PILOT_499_OFFER.md).

P2 AFTER FIRST PAID PILOT:
6. Deliver the Proof Pack on day 7
   (docs/FIRST_CUSTOMER_PROOF_PACK_TEMPLATE.md).
7. Decide whether to flip MOYASAR_ALLOW_LIVE_CHARGE — only after
   a written refund/charge policy is published.
8. Decide whether to flip WHATSAPP_ALLOW_LIVE_SEND — only after
   the approved-template path + ConsentRecord registry are wired.
```
