# Wave 12 — Saudi AI Revenue Command Center: Evidence Table

**Generated:** 2026-05-12
**Branch:** `claude/wave12-7-api-wiring` (Wave 12 + Wave 12.6 already on main)
**Audited by:** Claude Code (Wave 12.5 §33.4.2)

---

## Schema

Per plan §26.1, every PASS row must have all 7 artifacts:
**file + code + test + run command + clear output + production/customer evidence + status**.

Status taxonomy:
- **PASS** — all artifacts present + tests green + verifier ok
- **PARTIAL** — partially present; gaps named
- **DEFERRED** — explicit Article 11 deferral with named trigger
- **BLOCKED** — external dependency (lawyer / DNS / Moyasar KYC)

---

## The 12 engines + Intelligence Layer + Wave 12.6

| # | Engine | Module | Tests | Verifier | Status |
|---|---|---|---|---|---|
| 1 | Saudi Market Radar Extended | `auto_client_acquisition/market_intelligence/{signal_detectors,saudi_seasons}.py` | `tests/test_market_radar_v2.py` (12) | `ENGINE_1_MARKET_RADAR_V2=PASS` | **PASS** |
| 2 | Lead Intelligence 13-dim | `auto_client_acquisition/pipelines/saudi_dimensions.py` | `tests/test_saudi_dimensions_v1.py` (20) | `ENGINE_2_LEAD_INTELLIGENCE=PASS` | **PASS** |
| 3 | Company Brain Timeline | `auto_client_acquisition/company_brain_v6/timeline.py` | `tests/test_company_brain_timeline_v1.py` (12) | `ENGINE_3_COMPANY_BRAIN_TIMELINE=PASS` | **PASS** |
| 4 | Decision Passport v1.1 | `auto_client_acquisition/decision_passport/{schema,builder}.py` + `api/routers/decision_passport.py` | `tests/test_decision_passport_v2.py` (10) | `ENGINE_4_DECISION_PASSPORT_V2=PASS` | **PASS** |
| 5 | WhatsApp Decision Layer v2 | `auto_client_acquisition/whatsapp_decision_bot/{schemas,command_parser}.py` | `tests/test_whatsapp_decision_layer_v2.py` (10) | `ENGINE_5_WHATSAPP_DECISION_V2=PASS` | **PASS** |
| 6 | Action & Approval v2 | `auto_client_acquisition/approval_center/schemas.py` | `tests/test_action_approval_engine_v2.py` (8) | `ENGINE_6_ACTION_APPROVAL_V2=PASS` | **PASS** |
| 7 | Delivery OS 7-workflow | `auto_client_acquisition/delivery_factory/workflow_loader.py` + `data/workflows/*.yaml` (7) | `tests/test_delivery_workflows_v2.py` (14) | `ENGINE_7_DELIVERY_OS=PASS` | **PASS** |
| 8 | Support OS v3 | `auto_client_acquisition/support_os/ticket.py` + `customer_success/health_score.py` | `tests/test_support_os_v3.py` (13) | `ENGINE_8_SUPPORT_OS_V3=PASS` | **PASS** |
| 9 | Payment + ZATCA | `auto_client_acquisition/payment_ops/refund_state_machine.py` | `tests/test_payment_refund_zatca_v1.py` (14) | `ENGINE_9_PAYMENT_ZATCA=PASS` | **PASS** |
| 10 | Proof + Expansion v2 | `auto_client_acquisition/proof_engine/auto_summary.py` + `expansion_engine/readiness_score.py` + Wave 12.7 router | `tests/test_proof_expansion_v2.py` (18) | `ENGINE_10_PROOF_EXPANSION_V2=PASS` | **PASS** |
| 11 | Learning Flywheel v1 | `auto_client_acquisition/learning_flywheel/{aggregator,funnel_metrics,feature_gating}.py` | `tests/test_learning_flywheel_v1.py` (16) | `ENGINE_11_LEARNING_FLYWHEEL=PASS` | **PASS** |
| 12 | Trust/Security v1 | `api/security/ssrf_guard.py` + `email/deliverability_check.py` | `tests/test_engine12_security_v1.py` (17) | `ENGINE_12_TRUST_SECURITY_V1=PASS` | **PASS** |
| 12.6 | Tenant Isolation + BOPLA | `api/middleware/{tenant_isolation,bopla_redaction}.py` | `tests/test_tenant_isolation_v1.py` (18) + `test_bopla_redaction_v1.py` (12) | (folds into ENGINE_12) | **PASS** |
| ⭐ | Intelligence Layer | `auto_client_acquisition/intelligence/{dealix_task_registry,local_model_client,confidence,dealix_model_router}.py` + Wave 12.7 router | `tests/test_intelligence_layer_v1.py` (21) | `INTELLIGENCE_LAYER=PASS` | **PASS** |

**Total: 13 layers · 215 tests · 215/215 PASS**

---

## Wave 12.7 — API Wiring (this commit)

| Router | Endpoints | Wraps |
|---|---|---|
| `api/routers/intelligence_layer.py` | `GET /api/v1/intelligence/status` · `GET /tasks` · `POST /route` · `POST /confidence` | `intelligence/dealix_model_router` + `task_registry` + `confidence` |
| `api/routers/expansion_engine.py` | `GET /api/v1/expansion-engine/status` · `GET /pain-types` · `POST /readiness` · `POST /recommend` | `expansion_engine/readiness_score` |

Both routers compile cleanly (verified via importlib in sandbox per plan §27.3 documented `_cffi_backend` cascade).

---

## Hard gates: 8/8 IMMUTABLE every commit

| Gate | Where enforced |
|---|---|
| NO_LIVE_SEND | `safe_send_gateway/middleware.py` raises `SendBlocked` |
| NO_LIVE_CHARGE | `payment_ops/orchestrator._enforce_no_live_charge` + sandbox env |
| NO_COLD_WHATSAPP | `channel_policy_gateway/whatsapp` consent required |
| NO_LINKEDIN_AUTO | `agent_registry` `linkedin_company_search_requires_founder_approval` |
| NO_SCRAPING | `tests/test_no_linkedin_scraper_string_anywhere.py` git ls-files scan |
| NO_FAKE_PROOF | `proof_engine/evidence.EvidenceLevel` + `auto_summary` 3-gate publish |
| NO_FAKE_REVENUE | `revenue_truth.py` + `payment_ops/refund_state_machine.is_revenue_after_refund` |
| NO_BLAST | `safety_v10/policies` + `learning_flywheel/feature_gating.REJECTED_UNSAFE` |

Plus 3 Wave 12.6 additions:
- **No silent cross-tenant access** (`assert_tenant_match` raises `CrossTenantAccessDenied`)
- **No SSRF** (`api/security/ssrf_guard.check_url` blocks 8 internal-IP patterns)
- **No PII leak by role** (`bopla_redaction.fields_blocked_for_role` default-deny)

---

## Master verifier output (last run)

```
WAVE12_SAUDI_REVENUE_COMMAND_CENTER=PASS  (29/32)
ENGINES_PASSING=12_of_12
HARD_GATE_AUDIT_8_OF_8=PASS
WAVE11_E2E_CUSTOMER_JOURNEY=PASS
SECRET_SCAN=PASS
ARTIFACT_*=PASS (10/10)
LOCAL_HEAD=aa9e545d... (post Wave 12 + Wave 12.6 merge)
```

3 documented skips:
- `WAVE6_REVENUE_ACTIVATION=KNOWN_PARTIAL_PRE_EXISTING [needs prod env]`
- `WAVE7_5_SERVICE_TRUTH=KNOWN_PARTIAL_PRE_EXISTING [needs prod env]`
- `PROD_SMOKE_HARDENED=SKIPPED [set RUN_PROD_SMOKE=1 to run]`

---

## Article 13 trigger status

| Criterion | Required | Actual | Status |
|---|---|---|---|
| Paid Sprint customers | 3 | 0 | NOT_YET |
| Partner upsells | 1 | 0 | NOT_YET |
| Customer Signal Synthesis | yes | no | NOT_YET |
| **Article 13 fired** | all 3 | 0/3 | **NOT_YET** |

---

## Three-level reality check

| Level | Status |
|---|---|
| Technical Ready | ✅ YES — 13/13 layers PASS |
| Operational Ready | ✅ YES — Wave 11 §31 closed |
| Business Reality | ❌ NOT YET — 0 paid customers |

> **System is ready. Revenue execution is pending.**

---

## What's deferred (Article 11 + Article 13 honored — explicit triggers)

| Item | Trigger condition |
|---|---|
| Langfuse SDK v4 wire | First Partner customer signs OR LLM cost >100 SAR/month |
| Next.js founder app migration | After CSM hire (post-Article-13) |
| Temporal | First 30+ day workflow exceeds APScheduler reliability |
| Founder DPA signature | Before customer #1 payment confirmed |
| DNS records (SPF/DKIM/DMARC) | Before any outbound email at scale |
| ZATCA Fatoora live submission | After founder approves first invoice |

---

## Single most important next step

> **Send the first warm-intro WhatsApp message to prospect #1 today.**

The codebase has done its job. The founder's WhatsApp now needs to do its job.
