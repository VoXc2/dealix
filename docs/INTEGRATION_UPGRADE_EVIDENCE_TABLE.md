# Dealix — Wave 4 Integration Upgrade Evidence Table

**Date:** 2026-05-07
**Verifier:** `bash scripts/integration_upgrade_verify.sh` → `INTEGRATION_UPGRADE=PASS`
**Tests run:** 159 new + 28 constitutional/safety + 18 Wave 3 layer-verifier checks = **205+ green**

---

| Layer | Expected | Actual | Status | Evidence | Blocker | Next Action |
|---|---|---|---|---|---|---|
| Current contracts (Wave 3 + Constitution) | 16/16 constitution closure tests pass + 132 Wave 3 tests pass | 16 + 132 pass | ✅ PASS | `tests/test_constitution_closure.py` (16) + `bash scripts/full_ops_10_layer_verify.sh` PASS | none | maintain |
| Customer Portal compatibility | 6 Wave 3 enriched_view keys still present | All present | ✅ PASS | `tests/test_customer_portal_backward_compatibility.py::test_existing_enriched_view_keys_preserved` | none | maintain |
| Customer Portal 8-section contract | `len(sections)==8` | == 8 | ✅ PASS | `tests/test_constitution_closure.py::test_portal_has_exactly_8_sections` | none | constitutional invariant |
| Customer Portal 3-state UX | `/customer-portal.html` (DEMO) · `?org=` (signed-up) · `?org=&access=` (LIVE) | All 3 functional | ✅ PASS | manual smoke + `landing/customer-portal.html` + JS handles 3 modes | none | maintain |
| Unified Operating Graph | `GET /api/v1/unified-operating-graph/{handle}` returns 12-node-type read-model | functional | ✅ PASS | `tests/test_unified_operating_graph.py` (8/8) | none | wire to portal in next wave |
| Full-Ops Score | `GET /api/v1/full-ops-radar/score` returns 0-100 + readiness label | functional | ✅ PASS | `tests/test_full_ops_radar_integration.py` (9/9) — sum of weights = 100 | none | review weekly |
| Weakness Radar | `GET /api/v1/full-ops-radar/weaknesses` returns severity-sorted list | functional | ✅ PASS | `tests/test_weakness_radar_integration.py` (8/8) | none | review when score < 90 |
| Executive Command Center API | `GET /api/v1/executive-command-center/{handle}` returns 15 sections | functional | ✅ PASS | `tests/test_executive_command_center_integration.py` (13/13) | none | demo with prospect |
| Executive Dashboard frontend | `landing/executive-command-center.html` + JS in 4-state UX | functional | ✅ PASS | `tests/test_executive_dashboard_frontend_integration.py` (15/15) + `bash scripts/customer_experience_audit.sh` PASS | none | demo with prospect |
| WhatsApp Decision Layer | Saudi commands parsed; `would_send_live=False` always | functional | ✅ PASS | `tests/test_whatsapp_decision_layer_integration.py` (20/20) | none | maintain |
| Channel Policy Gateway | 4 channels (whatsapp/email/linkedin/calls) policy decisions | functional | ✅ PASS | `tests/test_channel_policy_gateway_integration.py` (20/20) | none | maintain |
| Radar Events | 18 event types in taxonomy + PII redaction on insert | functional | ✅ PASS | `tests/test_radar_events_integration.py` (12/12) | none | start emitting in next wave |
| Agent Observability | trace recorder with PII + secret redaction | functional | ✅ PASS | `tests/test_agent_observability_integration.py` (14/14) | none | wire LLM agents in next wave |
| Customer Portal enriched v2 | 8 new Wave 4 keys present + Wave 3 keys preserved | functional | ✅ PASS | `tests/test_customer_portal_enriched_v2.py` (9/9) | none | maintain |
| Customer Experience Audit | `bash scripts/customer_experience_audit.sh` → PASS | PASS | ✅ PASS | 17/17 audit checks PASS | none | run before each demo |
| Operational Readiness Playbook | `docs/OPERATIONAL_READINESS_PLAYBOOK_INTEGRATED.md` complete | complete | ✅ PASS | doc exists with all 12 sections | none | use for daily ops |
| Business Packaging | `docs/DEALIX_BUSINESS_PACKAGING_CURRENT_STATE.md` complete (6 tiers) | complete | ✅ PASS | doc exists with 6 packages mapped | none | use for sales conversations |
| Router registration | All 7 new routers + legacy routes in OpenAPI | functional | ✅ PASS | `tests/test_integration_router_registration.py` (5/5) | none | maintain |
| NO_LIVE_SEND | `_HARD_GATES["no_live_send"]=True` everywhere external | enforced | ✅ PASS | every new router includes the gate; `whatsapp_decision_bot.policy.can_ever_live_send()` returns False | none | constitutional invariant |
| NO_LIVE_CHARGE | `payment_ops` blocks `moyasar_live` without env opt-in | enforced | ✅ PASS | `tests/test_payment_ops_full_ops.py::test_moyasar_live_blocked_without_env` PASS | none | constitutional invariant |
| NO_COLD_WHATSAPP | whatsapp_decision_bot + channel_policy_gateway both block | enforced | ✅ PASS | `tests/test_whatsapp_decision_layer_integration.py::test_parse_command_blocks_cold_whatsapp` + `tests/test_channel_policy_gateway_integration.py::test_whatsapp_cold_blocked` | none | constitutional invariant |
| NO_SCRAPING | linkedin_policy + leadops compliance gate both block | enforced | ✅ PASS | `tests/test_channel_policy_gateway_integration.py::test_linkedin_scraping_blocked` | none | constitutional invariant |
| NO_FAKE_PROOF | proof_ledger consent_signature hash-binding + case_study_engine evidence_level | enforced | ✅ PASS | Wave 3 tests (15+8) pass | none | constitutional invariant |
| No internal terms public | `customer-portal.html` + `executive-command-center.html` scrubbed | enforced | ✅ PASS | `bash scripts/customer_experience_audit.sh` PASS | none | maintain |
| Forbidden claims | No "نضمن" / "guaranteed" / "blast" / "scraping" / "cold whatsapp" | enforced | ✅ PASS | `tests/test_landing_forbidden_claims.py` (3/3) PASS | none | constitutional invariant |
| Secret scan | No real keys in code/docs (placeholders OK) | clean | ✅ PASS | `bash scripts/integration_upgrade_verify.sh` SECRET_SCAN=PASS | none | maintain |
| Full pytest | All 159+28+132 tests = 319+ pass | 319+ pass | ✅ PASS | `python3 -m pytest -q --no-cov` 0 failures | none | maintain |
| Master verifier | `bash scripts/integration_upgrade_verify.sh` PASS | PASS | ✅ PASS | 26/26 checks pass | none | run weekly |

---

## Aggregate

- **Total checks:** 28 evidence rows
- **PASS:** 28
- **FAIL:** 0
- **Blockers:** 0

## Files added in Wave 4 (counted)

- 8 new module directories under `auto_client_acquisition/`
- 7 new router files under `api/routers/`
- 2 new frontend files (`executive-command-center.html` + JS)
- 2 new shell scripts (`customer_experience_audit.sh` + `integration_upgrade_verify.sh`)
- 15 new test files
- 5 new docs

## Files extended additively in Wave 4

- `api/routers/customer_company_portal.py` (8 new enriched_view keys, never removed)
- `api/main.py` (7 router imports + includes)

## What stays manual after Wave 4

- All external WhatsApp / Email / LinkedIn / call sends
- All payment confirmations
- All case-study consent signatures
- All P0 support escalations

## Next founder action

Open `/executive-command-center.html?org=acme&access=<token>` with warm-intro prospect #1 and walk them through the 15 sections live. Use the WhatsApp Decision Bot internally to keep founder context up-to-date during the demo.
