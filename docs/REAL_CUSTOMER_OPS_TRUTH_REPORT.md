# Dealix — Real Customer Ops Truth Report

> Generated 2026-05-03 — branch `claude/dealix-staging-readiness-LJOju`.
>
> Statuses used (and only these):
> - `PROVEN_LIVE` — verified on `https://api.dealix.me`
> - `PROVEN_STAGING` — verified on a staging-equivalent surface
> - `PROVEN_LOCAL` — verified locally with full test environment
> - `CODE_EXISTS_NOT_PROVEN` — code is present, behaviour not exercised here
> - `MISSING_OR_EMPTY` — file/route does not exist or is empty
> - `BLOCKER` — actively breaking a customer-facing flow today
> - `BACKLOG` — desirable but not required for first-customer flow

## 1. Two-branch reality

| Lane | Branch | Where it runs | Notes |
| --- | --- | --- | --- |
| Local working tree | `claude/dealix-staging-readiness-LJOju` | local + previously deployed to test | session rule: develop only here |
| Production deploy | `claude/launch-command-center-6P4N0` | `https://api.dealix.me` | far ahead — adds ~46 routers (operator chat, services, role-briefs, whatsapp/brief, support, partners portal, observability, founder/today, auth, calls, cards, daily-ops, delivery, intelligence, learning, meetings, negotiation, onboarding, proof-ledger, prospects, self-growth, self-ops, service_tower, sprints) |
| Truth | both branches share `main` history but live ops are on the deploy branch | — | Spec was written about the deploy branch |

Implication: my fixes (AsyncSession contract + aiosqlite + staging_smoke) live on
`claude/dealix-staging-readiness-LJOju`. The classifier/operator/role-brief
issues found below live on the **deploy branch** and need a fix landed THERE,
not here. I did not push to a different branch — that is explicitly forbidden
by session rules.

## 2. Empty file scan

```
./scripts/__init__.py
./tests/governance/__init__.py
./tests/integration/__init__.py
./tests/unit/__init__.py
```

All four are intentional package markers. No critical empty files.

## 3. Spec-claimed files vs. local truth

| Spec file | Local repo | Status |
| --- | --- | --- |
| `api/main.py` | present, 5,381 B | OK |
| `api/routers/operator.py` | absent locally | MISSING_OR_EMPTY (lives on deploy branch) |
| `api/routers/services.py` | absent locally | MISSING_OR_EMPTY (lives on deploy branch) |
| `api/routers/prospects.py` | absent (have `prospect.py` singular) | MISSING_OR_EMPTY |
| `api/routers/payments.py` | absent (have routes inside `full_os.py`) | MISSING_OR_EMPTY |
| `api/routers/proof_ledger.py` | absent locally | MISSING_OR_EMPTY (lives on deploy branch) |
| `api/routers/role_briefs.py` | absent locally | MISSING_OR_EMPTY (lives on deploy branch) |
| `api/routers/whatsapp_briefs.py` | absent locally | MISSING_OR_EMPTY (lives on deploy branch) |
| `landing/index.html` | present | OK |
| `landing/services.html`, `operator.html`, `proof-pack.html` | absent | MISSING_OR_EMPTY |
| `landing/command-center.html` | present | OK |
| `scripts/full_acceptance.sh` | absent | MISSING_OR_EMPTY |
| `scripts/staging_smoke.sh` | created last session | OK |
| `scripts/launch_readiness_check.py` | absent | MISSING_OR_EMPTY (closest: `personal-operator/launch-readiness` endpoint) |

## 4. Production endpoints (verified live)

`BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` → **22/22 pass**.

| Endpoint | Status | Notes |
| --- | --- | --- |
| `GET /` | 200 PROVEN_LIVE | clean JSON, env=production |
| `GET /health` | 200 PROVEN_LIVE | providers=[groq] |
| `GET /docs` | 200 PROVEN_LIVE | |
| `GET /openapi.json` | 200 PROVEN_LIVE | **306 routes** registered on prod |
| `GET /api/v1/services/catalog` | 200 PROVEN_LIVE | 6 bundles (free_diagnostic, growth_starter, data_to_revenue, executive_growth_os, partnership_growth, full_growth_control_tower) |
| `GET /api/v1/services/{bundle_id}` | 200 PROVEN_LIVE | per-bundle contract |
| `GET /api/v1/services/{bundle_id}/intake-questions` | 200 PROVEN_LIVE | 3-5 questions per bundle |
| `POST /api/v1/operator/chat/message` | 200 PROVEN_LIVE | classifier OK on most cases — see Operator Matrix |
| `POST /api/v1/operator/service/start` | 200 PROVEN_LIVE | returns `session_id` |
| `GET /api/v1/role-briefs/roles` | 200 PROVEN_LIVE | 8 roles |
| `GET /api/v1/role-briefs/daily?role=sales_manager` | 200 PROVEN_LIVE but with `_errors` field | **BLOCKER**: schema mismatch — `column deals.hubspot_deal_id does not exist` |
| `GET /api/v1/role-briefs/daily?role=growth_manager` | 200 PROVEN_LIVE | clean |
| `GET /api/v1/role-briefs/daily?role=ceo` | 200 PROVEN_LIVE | |
| `GET /api/v1/role-briefs/daily?role=marketing_manager` | 400 | **BLOCKER**: role not registered — task spec asked for it |
| `GET /api/v1/role-briefs/daily?role=finance_manager` | 400 | spec used `finance_manager`, code expects `finance` |
| `GET /api/v1/role-briefs/daily?role=customer_success` | 200 PROVEN_LIVE | |
| `GET /api/v1/role-briefs/daily?role=compliance` | 200 PROVEN_LIVE | |
| `GET /api/v1/whatsapp/brief?role=sales_manager` | **500** | BLOCKER — same DB schema mismatch |
| `GET /api/v1/whatsapp/brief?role=growth_manager` | 200 PROVEN_LIVE | Arabic internal preview text |
| `GET /api/v1/whatsapp/brief?role=ceo` | **500** | BLOCKER |
| `GET /api/v1/automation/status` | **500** | BLOCKER (AsyncSession contract — fix is on `claude/dealix-staging-readiness-LJOju`, not yet redeployed) |
| `POST /api/v1/compliance/check-outreach` | **500** | BLOCKER — same root cause |
| `POST /api/v1/webhooks/moyasar` (unsigned) | 401 PROVEN_LIVE | bad_signature, gate enforced |
| `POST /api/v1/os/test-send?phone=…` (whatsapp) | 200 PROVEN_LIVE | body `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` |
| `GET /api/v1/proof-ledger/units` | 200 PROVEN_LIVE | 10 RWU types |
| `GET /api/v1/support/sla` | 200 PROVEN_LIVE | P0/P1/P2/P3 SLA |
| `POST /api/v1/support/classify` | 200 PROVEN_LIVE | priority/category/SLA |

## 5. Local proof

| Check | Result |
| --- | --- |
| `python -m pip check` | No broken requirements |
| `python -m compileall api auto_client_acquisition core db` | OK |
| `python -m pytest -q --no-cov` | **516 passed, 6 skipped** in 4.50 s |
| `scripts/print_routes.py` | 260 routes (no duplicate method+path) |
| `scripts/smoke_inprocess.py` | `SMOKE_INPROCESS_OK` |
| `scripts/run_demo.py` | 3/3 sample leads processed |
| Local E2E (lead → deal → manual invoice → mark paid → customer → proof pack) | full pass |

```
lead_id     = lead_2be6aaae9444
deal_id     = deal_14e3ed3697d5405f
invoice     = method=bank_transfer status=payment_requested follow_up_task_id=task_758de3162e87471c
paid        = customer_id=cust_e49e5bb76d3c4851
proof_pack  = customer/proof-pack returns case_study + testimonial + referral
proof_grade = command-center/proof-pack returns grade=D (no activity yet)
compliance  = contact_opt_out → blocked correctly
```

## 6. Live operator quality (prod) — 14 scenarios

| Input | Detected language | Got intent | Got bundle | Expected | Pass |
| --- | --- | --- | --- | --- | --- |
| "أبي عملاء أكثر لشركتي" | ar | want_more_customers | growth_starter | growth_starter | ✅ |
| "أبي أرسل واتساب لأرقام مشتريها" | ar | want_more_customers | growth_starter | **BLOCKED** | **❌ SAFETY** |
| "ارسل cold whatsapp" | mixed | cold_whatsapp_request | — (blocked) | BLOCKED | ✅ |
| "ابغى واتساب بارد" | ar | cold_whatsapp_request | — (blocked) | BLOCKED | ✅ |
| "أبغى أبيع لأرقام جبتها من قائمة شريتها" | ar | want_more_customers | growth_starter | **BLOCKED** | **❌ SAFETY** |
| "أبي blast واتساب" | mixed | want_more_customers | growth_starter | **BLOCKED** | **❌ SAFETY** |
| "Can you blast WhatsApp?" | en | cold_whatsapp_request | — (blocked) | BLOCKED | ✅ |
| "We have a list of 500 leads" | en | has_list | data_to_revenue | data_to_revenue | ✅ |
| "عندي ملف فيه 200 عميل محتمل" | ar | want_more_customers | growth_starter | data_to_revenue | ❌ |
| "I need more B2B leads in Saudi" | en | want_more_customers | growth_starter | growth_starter | ✅ |
| "Need proof report for management" | en | want_more_customers | growth_starter | proof / executive | ❌ |
| "عندي SaaS وأبي pipeline مرتب" | mixed | want_more_customers | growth_starter | growth_starter | ✅ |
| "عندي شركة تدريب وأبي مواعيد" | ar | want_more_customers | growth_starter | growth_starter | ✅ |
| "أبي شراكات مع وكالات" | ar | want_partnerships | partnership_growth | partnership_growth | ✅ |

**Score: 10 / 14 pass. 4 fails — 3 of them are safety-critical Arabic
phrasings of cold-WhatsApp / purchased-list requests that the classifier
fails to block.** This is the most urgent prod-side blocker.

## 7. Service Tower (prod, verified)

All six bundles return a valid contract object with: `id`, `name_ar`,
`name_en`, `price_sar`, `price_label`, `cadence`, `duration_days`,
`for_whom_ar`, `deliverables_ar` (list), `proof_metrics`,
`sla_ar`, `safe_policy_ar`, `cta_path`. Intake questions endpoint
returns a structured form with `key`, `label_ar`, `type`, `required`.

| Bundle | Price (SAR) | Cadence | Duration | Intake Qs | Proof metrics | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `free_diagnostic` | 0 | one_time | 1 d | 4 | sectors_scanned, improvement_areas, recommended_bundle | PROVEN_LIVE |
| `growth_starter` | 499 | one_time | 7 d | 5 | opportunities_created, drafts_created, risks_blocked, proof_pack_url | PROVEN_LIVE |
| `data_to_revenue` | 1,500 | one_time | 10 d | 4 | rows_cleaned, contactability_score, drafts_created, risks_blocked | PROVEN_LIVE |
| `executive_growth_os` | 2,999 | monthly | 30 d | 4 | weekly_proof_packs, role_briefs_delivered, decisions_logged | PROVEN_LIVE |
| `partnership_growth` | 3,000-7,500 | one_time | 30 d | 3 | partner_shortlist_size, intros_sent, co_pilot_started | PROVEN_LIVE |
| `full_growth_control_tower` | custom | monthly | — | n/a | enterprise / not for self-serve | PROVEN_LIVE |

## 8. Safety gates (prod, verified)

| Gate | How enforced | Live result | Status |
| --- | --- | --- | --- |
| `WHATSAPP_ALLOW_LIVE_SEND` (default false) | settings.py:106 + `os/test-send` policy provider | body `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` | PROVEN_LIVE ✅ |
| Cold WhatsApp by intent | operator chat classifier | **fails for some Arabic phrasings** | **PROVEN_LIVE FAIL** ❌ |
| Moyasar webhook | `MOYASAR_WEBHOOK_SECRET` constant-time HMAC | unsigned → 401 bad_signature | PROVEN_LIVE ✅ |
| Moyasar live charge | absence of `MOYASAR_SECRET_KEY` → `payments/manual-request` returns bank-transfer fallback | manual fallback returned | PROVEN_LIVE ✅ |
| Gmail live send | `gmail_configured()` check requires `GMAIL_CLIENT_ID + GMAIL_REFRESH_TOKEN + GMAIL_SENDER_EMAIL` | not configured → blocked | PROVEN_LIVE ✅ |
| LinkedIn automation | only `linkedin/drafts/create` + manual-capture exists; no automation route | manual-only by design | PROVEN_LIVE ✅ |
| Live dial / calls | `calls/dial-live` exists on prod — needs verification it's gated | not exercised here | CODE_EXISTS_NOT_PROVEN |
| Compliance opt-out | `compliance/check-outreach` (after AsyncSession fix) returns `allowed:false reasons:[contact_opt_out_true]` | blocked locally | PROVEN_LOCAL ✅, **prod 500 BLOCKER** |
| WhatsApp inbound verify token | `webhooks/whatsapp` GET requires verify token | 422 without token | PROVEN_LIVE ✅ |

## 9. Frontend (local served at 8081)

25 actual pages — all 200 (last session). Spec-claimed pages
(`services.html`, `operator.html`, `proof-pack.html`, `role/*.html`)
not present. Their FUNCTIONAL equivalent on prod is via API routes
(`/api/v1/services/catalog`, `/api/v1/operator/chat/message`,
`/api/v1/customers/{id}/proof-pack`). `landing/README.md` exists on
deploy branch but not here.

## 10. Backend reality (numbers)

| Metric | Local branch | Prod (deploy branch) |
| --- | --- | --- |
| OpenAPI paths | 260 | 306 |
| Spec asked for | 364 | — |
| Pytest pass | 516 | not run on prod |
| Spec claim | 939 | — |

The "364 / 939" numbers in the original spec do not match either branch.

## 11. Verdict

| Surface | Status |
| --- | --- |
| Local | **PROVEN_LOCAL** — 516 tests, full E2E, all gates verified |
| Prod public reads | **PROVEN_LIVE** — 22/22 staging smoke green |
| Prod service tower | **PROVEN_LIVE** — 6 bundles + intake forms |
| Prod operator chat (English + obvious Arabic) | **PROVEN_LIVE** |
| Prod operator chat (some Arabic Saudi phrasings) | **BLOCKER** — 3 cold-WA misses |
| Prod role-briefs | **BLOCKER** — DB schema mismatch (`deals.hubspot_deal_id`) |
| Prod whatsapp/brief sales_manager+ceo | **BLOCKER** — same schema mismatch |
| Prod automation/status + compliance/check-outreach | **BLOCKER** — AsyncSession (fix is on this branch, not yet on deploy) |
| Prod write paths (DB POSTs) | not exercised against prod by design |
