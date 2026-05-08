# Dealix Master Execution — Evidence Table

> Per-row audit ledger for the 30-row Master Execution Matrix.
> Date: 2026-05-08 · Branch `claude/wave10-5-master-execution-audit` · Base SHA `811fddd`.
> Honesty contract: every "Actual" reflects what `git ls-files` + verifier output show today.

---

### Row 1: Business model (positioning · ICP · pricing · offer ladder)

- **Expected:** business doc + module + pricing page + verifier green
- **Actual:** docs + module + pricing.html exist; `business_readiness_verify.sh` exits FAIL (4 forbidden-token violations)
- **Evidence path:** `docs/BUSINESS_MODEL.md`, `auto_client_acquisition/business/`, `landing/pricing.html`
- **Test path:** `tests/test_business_strategy.py`
- **Verifier output:** `BUSINESS_READINESS=FAIL (fix 4 failures above)` — 35 PASS / 4 FAIL
- **Status:** PARTIAL
- **Blocker:** 4 forbidden-token violations (cold WA, fake proof, guaranteed, scraping)
- **Next action:** Scrub the 4 violations and re-run `business_readiness_verify.sh`.

### Row 2: ICP refinement loop

- **Expected:** ICP stored, refined per outcome, dashboard
- **Actual:** ICP matcher + leadops spine exist; no dedicated UI for refinement
- **Evidence path:** `auto_client_acquisition/leadops_spine/`, `tests/unit/test_icp_matcher.py`
- **Test path:** `tests/unit/test_icp_matcher.py`, `tests/test_leadops_spine_golden_path.py`
- **Verifier output:** `LEADOPS_SPINE=FAIL` (in `integration_upgrade_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** No frontend; refinement loop relies on JSON files in `data/icp/`
- **Next action:** Wire ICP refinement to first-customer feedback loop.

### Row 3: Offer ladder + unit economics

- **Expected:** ladder doc + unit economics module + pricing page + tests
- **Actual:** all artifacts present and aligned
- **Evidence path:** `docs/UNIT_ECONOMICS_AND_MARGIN.md`, `docs/COMPANY_SERVICE_LADDER.md`, `auto_client_acquisition/business/unit_economics.py`, `landing/pricing.html`
- **Test path:** `tests/test_business_strategy.py`
- **Verifier output:** `ECONOMICS: Figures labeled as estimates (not guarantees)=PASS` (`business_readiness_verify.sh`)
- **Status:** PASS
- **Blocker:** —
- **Next action:** Adjust ladder after first customer outcome.

### Row 4: Sales playbook

- **Expected:** playbook doc + CRM module + sales API + tests
- **Actual:** all 7 artifacts present; live endpoints under `/api/v1/sales-os/*`
- **Evidence path:** `docs/SALES_PLAYBOOK.md`, `auto_client_acquisition/crm_v10/`, `api/routers/sales_os.py`
- **Test path:** `tests/unit/test_lead_scorer.py`, `tests/test_full_ops_score_final.py`
- **Verifier output:** `SALES_OS=pass` (`v12_full_ops_verify.sh`)
- **Status:** PASS
- **Blocker:** —
- **Next action:** Use playbook on first warm call.

### Row 5: Lead Machine

- **Expected:** spine module + router + UI + tests + green verifier
- **Actual:** all artifacts present, but `LEADOPS_SPINE=FAIL`
- **Evidence path:** `auto_client_acquisition/leadops_spine/`, `api/routers/leadops_spine.py`, `landing/founder-leads.html`
- **Test path:** `tests/test_leadops_spine_golden_path.py`, `tests/test_leadops_reliability.py`
- **Verifier output:** `LEADOPS_SPINE=FAIL` (`integration_upgrade_verify.sh`); also flagged for NO_COLD_WHATSAPP violation in `business_readiness_verify.sh`
- **Status:** PARTIAL
- **Blocker:** Forbidden-token in `leadops_spine.py` + failing layer test
- **Next action:** Scrub cold-WhatsApp text; rerun `pytest tests/test_leadops_spine_golden_path.py -v`.

### Row 6: Revenue Intelligence (signal radar)

- **Expected:** detectors + opportunity feed + sector pulse + UI + tests
- **Actual:** market_intelligence (690 LOC) + revenue_graph + market-radar.html present
- **Evidence path:** `auto_client_acquisition/market_intelligence/{signal_detectors,opportunity_feed,sector_pulse,city_heatmap}.py`, `landing/market-radar.html`
- **Test path:** `tests/unit/test_market_radar.py`, `tests/unit/test_revenue_graph.py`
- **Verifier output:** No standalone signal-radar verifier; rolled into `integration_upgrade_verify.sh` (FAIL on neighbouring layers)
- **Status:** PARTIAL
- **Blocker:** No isolated verifier for the signal radar layer
- **Next action:** Add `signal_radar_verify.sh` to isolate this layer's health.

### Row 7: Customer Brain

- **Expected:** module + router + UI + tests + verifier green
- **Actual:** module (256 LOC) + router exist; `CUSTOMER_BRAIN=FAIL` in verifier
- **Evidence path:** `auto_client_acquisition/customer_brain/`, `api/routers/customer_brain.py`
- **Test path:** `tests/test_customer_brain_full_ops.py`
- **Verifier output:** `CUSTOMER_BRAIN=FAIL` (`integration_upgrade_verify.sh`)
- **Status:** FAIL
- **Blocker:** Test failure — needs investigation
- **Next action:** Run `pytest tests/test_customer_brain_full_ops.py -v` and fix the failing assertion.

### Row 8: Decision Passport

- **Expected:** builder + schema + router + UI + tests
- **Actual:** all artifacts present; new test `test_decision_passport.py` added in #182
- **Evidence path:** `auto_client_acquisition/decision_passport/{builder.py,schema.py}`, `api/routers/decision_passport.py`, `landing/decisions.html`
- **Test path:** `tests/test_decision_passport.py`
- **Verifier output:** No dedicated verifier
- **Status:** PARTIAL
- **Blocker:** Docs scattered across `V14_*.md`; no consolidated PRD or verifier
- **Next action:** Add `decision_passport_verify.sh` and consolidated PRD doc.

### Row 9: Action Center

- **Expected:** action queue module + router + UI + tests
- **Actual:** Daily Command Center routes work items, no standalone Action Center page
- **Evidence path:** `auto_client_acquisition/full_ops/`, `api/routers/full_ops.py`
- **Test path:** `tests/test_full_ops_daily_command_center_v12.py`, `tests/test_full_ops_work_item_v12.py`
- **Verifier output:** `WORKITEM_LAYER=pass`, `DAILY_COMMAND_CENTER=pass` (`v12_full_ops_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** No `landing/action-center.html` — Action Center is rolled into founder-dashboard
- **Next action:** Decide whether to create dedicated UI or formally rename Daily Command Center → Action Center.

### Row 10: Approval Center (+ Wave 7.7 founder rules)

- **Expected:** module + extensions + router + UI + tests + verifier
- **Actual:** module (514 LOC) + router + tests exist; `APPROVAL_CENTER=FAIL` in verifier
- **Evidence path:** `auto_client_acquisition/approval_center/`, `api/routers/approval_center.py`
- **Test path:** `tests/test_approval_center.py`, `tests/test_approval_center_extensions.py`
- **Verifier output:** `APPROVAL_CENTER=FAIL` (`integration_upgrade_verify.sh`)
- **Status:** FAIL
- **Blocker:** Test failure; Wave 7.7 founder rules in flight
- **Next action:** Run `pytest tests/test_approval_center.py -v` and close Wave 7.7 founder-rules patch.

### Row 11: Operating Execution

- **Expected:** 10-layer regression green
- **Actual:** `FULL_OPS_10_LAYER_REGRESSION=FAIL` — multiple layer FAILs cascade up
- **Evidence path:** `auto_client_acquisition/full_ops/`, `auto_client_acquisition/full_ops_radar/`
- **Test path:** `tests/test_full_ops_contracts.py`, `tests/test_full_ops_radar_integration.py`
- **Verifier output:** `FULL_OPS_10_LAYER_REGRESSION=FAIL` (`full_ops_10_layer_verify.sh`); 9/10 sub-layers FAIL
- **Status:** FAIL
- **Blocker:** Cascade failure from rows 5, 7, 10, 12, 14, 15, 17
- **Next action:** Fix layer-by-layer starting with `LEADOPS_SPINE`, then re-run.

### Row 12: Service Sessions

- **Expected:** module + router + UI + tests
- **Actual:** module (209 LOC) + router exist; `SERVICE_SESSIONS=FAIL`
- **Evidence path:** `auto_client_acquisition/service_sessions/`, `api/routers/service_sessions.py`
- **Test path:** `tests/test_service_sessions_full_ops.py`
- **Verifier output:** `SERVICE_SESSIONS=FAIL` (`integration_upgrade_verify.sh`)
- **Status:** FAIL
- **Blocker:** Failing test in `test_service_sessions_full_ops.py`
- **Next action:** Run `pytest tests/test_service_sessions_full_ops.py -v` and fix.

### Row 13: Support OS

- **Expected:** OS module + inbox + KB + router + tests
- **Actual:** Support OS v12 passes; Support Inbox layer FAILs
- **Evidence path:** `auto_client_acquisition/support_os/`, `auto_client_acquisition/support_inbox/` (231 LOC), `api/routers/support_os.py`, `api/routers/support_journey.py`
- **Test path:** `tests/test_support_os_v12.py`, `tests/test_support_inbox_full_ops.py`, `tests/test_support_journey_final.py`, `tests/test_support_knowledge_base_v12.py`
- **Verifier output:** `SUPPORT_OS=pass` (`v12_full_ops_verify.sh`); `SUPPORT_INBOX=FAIL` (`integration_upgrade_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** Inbox-layer regression
- **Next action:** Reconcile Support OS vs Support Inbox; fix the inbox test.

### Row 14: Payment State (8-state machine)

- **Expected:** 8-state machine + Moyasar guard + tests + safe gate
- **Actual:** 8 states confirmed in `orchestrator.py` (invoice_intent · invoice_sent_manual · payment_pending · payment_evidence_uploaded · payment_confirmed · delivery_kickoff · refunded · voided); live charge BLOCKED
- **Evidence path:** `auto_client_acquisition/payment_ops/orchestrator.py` (175 LOC)
- **Test path:** `tests/test_payment_ops_full_ops.py`, `tests/test_billing_moyasar_safety.py`, `tests/test_wave6_payment_confirmation.py`
- **Verifier output:** `PAYMENT_OPS=FAIL` (`integration_upgrade_verify.sh`); `NO_LIVE_CHARGE=PASS` everywhere
- **Status:** PARTIAL
- **Blocker:** Failing payment_ops layer test; Moyasar live charge BLOCKED until KYC
- **Next action:** Fix payment_ops_full_ops test; submit Moyasar KYC docs.

### Row 15: Customer Portal (9 sections)

- **Expected:** 9 sections + backend module + router + UI + tests
- **Actual:** 9 `<section>` confirmed via grep; router yes, but module `auto_client_acquisition/customer_company_portal/` MISSING
- **Evidence path:** `landing/customer-portal.html`, `api/routers/customer_company_portal.py`
- **Test path:** `tests/test_customer_portal_contract_final.py`, `tests/test_customer_portal_empty_states_final.py`, `tests/test_customer_portal_live_full_ops.py`, `tests/test_customer_portal_enriched_v2.py`, `tests/test_customer_portal_backward_compatibility.py`
- **Verifier output:** `CUSTOMER_PORTAL=FAIL` (`integration_upgrade_verify.sh`)
- **Status:** FAIL
- **Blocker:** Backend module missing — router likely imports from elsewhere
- **Next action:** Create `auto_client_acquisition/customer_company_portal/` package or redirect router imports.

### Row 16: Founder Command Center

- **Expected:** module + multiple routers + UI pages + tests
- **Actual:** founder_v10 (9 modules) + 3 founder routers + 3 founder landing pages
- **Evidence path:** `auto_client_acquisition/founder_v10/{daily_brief,blockers,next_actions,evidence_summary,cost_summary,dashboard_builder,cache,schemas}.py`, `api/routers/{founder,founder_beast_command_center,founder_v10}.py`, `landing/{founder,founder-dashboard,command-center}.html`
- **Test path:** `tests/test_constitution_closure.py` (touches founder routes)
- **Verifier output:** No dedicated founder-command verifier
- **Status:** PARTIAL
- **Blocker:** No isolated verifier; tests scattered across constitution/full_ops
- **Next action:** Add `founder_command_verify.sh`.

### Row 17: Proof Engine (event + L0-L5)

- **Expected:** event store + ledger + L0-L5 levels + redaction + HMAC
- **Actual:** ledger (1110 LOC) + new event store (`test_pg_event_store.py` from #182); L0-L5 only in docs, no enum constants
- **Evidence path:** `auto_client_acquisition/proof_ledger/{factory,evidence_export,hmac_signing,pack_assembly,postgres_backend,file_backend,consent_signature,schemas}.py`
- **Test path:** `tests/test_proof_event_sample_validates.py`, `tests/test_proof_ledger_extensions.py`, `tests/test_proof_ledger_redacts_on_export.py`, `tests/test_proof_ledger_postgres_backend.py`, `tests/test_pg_event_store.py`
- **Verifier output:** `PROOF_LEDGER=FAIL` (`integration_upgrade_verify.sh`); `PROOF_REDACTS_ON_EXPORT=PASS`
- **Status:** PARTIAL
- **Blocker:** L0-L5 levels exist only in markdown, no code-level enum; layer test failing
- **Next action:** Add `ProofMaturity` enum to `schemas.py`; fix the failing ledger test.

### Row 18: Proof Pack

- **Expected:** standard doc + assembler + UI + CLI + multiple test files
- **Actual:** v6 standard + 4 assembler tests + Wave 6 CLI all green
- **Evidence path:** `docs/PROOF_PACK_V6_STANDARD.md`, `auto_client_acquisition/proof_ledger/pack_assembly.py`, `landing/proof.html`, `scripts/dealix_wave6_proof_pack.py`
- **Test path:** `tests/test_proof_pack.py`, `tests/test_proof_pack_v6.py`, `tests/test_proof_pack_v11.py`, `tests/test_proof_pack_assembler.py`, `tests/test_wave6_proof_pack.py`
- **Verifier output:** `SCRIPT_dealix_wave6_proof_pack.py=PASS` (`wave6_revenue_activation_verify.sh`)
- **Status:** PASS
- **Blocker:** —
- **Next action:** Apply on first customer outcome.

### Row 19: Expansion Engine

- **Expected:** module + gates + router + tests + UI
- **Actual:** Revenue OS spine commit `811fddd` adds expansion gates; proof_to_market module exists; no dedicated UI
- **Evidence path:** `auto_client_acquisition/proof_to_market/`, `api/routers/proof_to_market.py`, `api/routers/revenue_os.py` (`/expansion`)
- **Test path:** Implicit in `tests/test_revenue_os_catalog.py` (new in #182)
- **Verifier output:** No dedicated verifier
- **Status:** PARTIAL
- **Blocker:** No e2e expansion gate test, no UI
- **Next action:** Add `tests/test_expansion_gates.py` and `landing/expansion.html`.

### Row 20: Learning Loop

- **Expected:** loop module + router + closing logic + tests + UI
- **Actual:** self_growth_os + customer_loop (407 LOC, 2 modules) + router exist; small surface area
- **Evidence path:** `auto_client_acquisition/self_growth_os/`, `auto_client_acquisition/customer_loop/{customer_journey,schemas}.py`, `api/routers/{self_improvement_os,self_growth}.py`
- **Test path:** `tests/test_constitution_closure.py`
- **Verifier output:** `SELF_IMPROVEMENT_OS=pass` (`v12_full_ops_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** customer_loop only contains `customer_journey.py` + `schemas.py`; no UI; loop closing logic thin
- **Next action:** Wire learning loop to approval-center decisions for closure.

### Row 21: Integrations (8 named providers)

- **Expected:** registry + adapters + tests + per-integration setup docs
- **Actual:** 20 integrations tracked; 16/20 status=`not_configured` or `configured_manual`
- **Evidence path:** `docs/WAVE8_INTEGRATION_REGISTRY.md`, `docs/wave8/integration_registry.yaml`, `auto_client_acquisition/integration_upgrade/`, `auto_client_acquisition/observability_adapters/{otel_adapter,langfuse_adapter,redaction}.py`
- **Test path:** `tests/test_wave8_integration_registry.py`, `tests/test_wave8_observability_adapter_readiness.py`
- **Verifier output:** `OBSERVABILITY_ADAPTERS=PRESENT` · `INTEGRATION_REGISTRY=PRESENT` (`wave8_customer_ready_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** Most integrations need credentials from real customer
- **Next action:** Request credentials per integration when first customer needs it.

### Row 22: Security (JWT · RBAC · API key · rate limit · audit · OWASP)

- **Expected:** middleware files + tests + OWASP review
- **Actual:** 5 security modules + 3 unit tests; OWASP review not formalised
- **Evidence path:** `api/security/{jwt,rbac,api_key,rate_limit,webhook_signatures,auth_deps}.py`
- **Test path:** `tests/unit/test_auth_flow.py`, `tests/unit/test_api_key_middleware.py`, `tests/unit/test_webhook_signatures.py`
- **Verifier output:** `SECRET_SCAN=PASS` everywhere
- **Status:** PARTIAL
- **Blocker:** No OWASP Top-10 documented review; no rate-limit integration test
- **Next action:** Run OWASP self-assessment + add rate-limit integration test.

### Row 23: RBAC (roles · permissions · enforcement)

- **Expected:** Role enum + per-route enforcement + role × endpoint test matrix
- **Actual:** Role enum (5 roles) + system_role flag exist; no enforcement matrix test
- **Evidence path:** `api/security/rbac.py` (Role: viewer · sales_rep · sales_manager · tenant_admin · super_admin), `api/security/auth_deps.py`
- **Test path:** Limited coverage in `tests/test_constitution_closure.py` (role count assertion only)
- **Verifier output:** None
- **Status:** PARTIAL
- **Blocker:** No matrix test of role × endpoint
- **Next action:** Add `tests/test_rbac_matrix.py` covering each role × each protected route.

### Row 24: Tenant isolation (RLS)

- **Expected:** Postgres `ENABLE ROW LEVEL SECURITY` + `CREATE POLICY` per table
- **Actual:** tenant_id columns in migrations + per-tenant rate-limit bucketing; **no `CREATE POLICY` statements found** — application-layer isolation only
- **Evidence path:** `db/migrations/versions/{0001_uuid_softdelete_indexes,20240101_001_auth_schema,20260507_002_saudi_compliance}.py`, `api/security/rate_limit.py`
- **Test path:** None for RLS at DB layer
- **Verifier output:** None
- **Status:** PARTIAL
- **Blocker:** No Postgres RLS — risk if any direct DB access bypasses application
- **Next action:** Enable Postgres RLS with `CREATE POLICY tenant_isolation` on all tenanted tables before multi-tenant prod.

### Row 25: PDPL readiness (DPA + Privacy + Terms + Breach + DSAR + Cross-Border)

- **Expected:** 6 legal docs + router + consent module + tests
- **Actual:** all 6 docs present + landing pages + pdpl router + 2 tests
- **Evidence path:** `docs/{DPA_DEALIX_FULL,PRIVACY_POLICY_v2,TERMS_OF_SERVICE_v2,PDPL_BREACH_RESPONSE_PLAN,PDPL_DATA_SUBJECT_REQUEST_SOP,CROSS_BORDER_TRANSFER_ADDENDUM}.md`, `landing/{privacy,terms,subprocessors}.html`, `api/routers/pdpl.py`, `auto_client_acquisition/customer_data_plane/consent_registry.py`
- **Test path:** `tests/test_pdpl_consent_default_deny.py`, `tests/unit/test_pdpl_suppression.py`
- **Verifier output:** `DPA_CONSENT=PRESENT` (`wave8_customer_ready_verify.sh`)
- **Status:** PARTIAL
- **Blocker:** All docs founder-drafted — needs licensed Saudi lawyer review
- **Next action:** Engage PDPL-experienced Saudi lawyer for review before first signed contract.

### Row 26: ZATCA readiness

- **Expected:** schema + integration + cert + Fatoora onboarding
- **Actual:** `zatca_invoices` table + router exist; no certified provider integration
- **Evidence path:** `docs/INVOICING_ZATCA_READINESS.md`, `db/migrations/versions/20260507_002_saudi_compliance.py`, `api/routers/zatca.py`
- **Test path:** None — no `test_zatca*` files exist
- **Verifier output:** None
- **Status:** BLOCKED
- **Blocker:** External — needs certified ZATCA provider contract + cert + Fatoora onboarding (Phase 2)
- **Next action:** Contact ZATCA-approved provider when first B2B invoice is needed.

### Row 27: Frontend (Arabic RTL · mobile · empty states · trust badges)

- **Expected:** Arabic-primary pages + design system + empty-state tests + verifier
- **Actual:** 46 HTML pages + design system + 2 dedicated empty-state tests + designops verifier
- **Evidence path:** 46 files in `landing/*.html`, `landing/styles.css`, `auto_client_acquisition/designops/`
- **Test path:** `tests/test_customer_portal_empty_states_final.py`, `tests/test_dealix_design_system.py`
- **Verifier output:** `designops_verify.sh` exists
- **Status:** PASS
- **Blocker:** —
- **Next action:** Verify mobile breakpoints on iPhone SE before first demo.

### Row 28: Production smoke (api.dealix.me/health + 8 critical endpoints)

- **Expected:** live health endpoint + smoke verifier + post-redeploy verifier
- **Actual:** `https://api.dealix.me/health` returns 200; full smoke 44/44 PASS
- **Evidence path:** Live HTTP 200 verified, `scripts/{wave8_production_readiness_smoke,post_redeploy_verify,smoke_test}.sh`
- **Test path:** `tests/test_wave8_production_readiness_smoke.py`
- **Verifier output:** `WAVE8_PRODUCTION_SMOKE: ALL_PASS` — 44 PASS / 0 FAIL
- **Status:** PASS
- **Blocker:** —
- **Next action:** Run post-redeploy after every deploy.

### Row 29: Business readiness

- **Expected:** business audit doc + verifier green + zero forbidden tokens
- **Actual:** docs present, verifier exits FAIL with 4 violations
- **Evidence path:** `docs/BUSINESS_REALITY_AUDIT.md`, `docs/BUSINESS_READINESS_EVIDENCE_TABLE.md`
- **Test path:** Same files referenced in `business_readiness_verify.sh`
- **Verifier output:** `BUSINESS_READINESS=FAIL (fix 4 failures above)` — 35 PASS / 4 FAIL
- **Status:** FAIL
- **Blocker:** 4 forbidden-token violations: NO_COLD_WHATSAPP in `leadops_spine.py`, NO_FAKE_PROOF in `customer_data_plane.py`, GUARANTEED_CLAIMS in `landing/ai-team.html`, SCRAPING in `revenue_graph/agent_registry.py`
- **Next action:** Scrub the 4 violations before approaching first customer.

### Row 30: First customer readiness

- **Expected:** playbook + diagnostic script + warm messages + launch verifier + production smoke
- **Actual:** all docs present; wave8 verifier=PASS; but business+full_ops verifiers FAIL
- **Evidence path:** `docs/{14_DAY_FIRST_REVENUE_PLAYBOOK,FIRST_3_CUSTOMER_LOOP_BOARD,FIRST_3_DIAGNOSTIC_SCRIPT,FIRST_10_WARM_MESSAGES_AR_EN}.md`, `landing/launchpad.html`
- **Test path:** `tests/test_dealix_customer_onboarding_wizard.py`, `tests/test_wave8_customer_onboarding_wizard_hardening.py`
- **Verifier output:** `wave8_customer_ready_verify.sh`=PASS (39/0); but `business_readiness_verify.sh`=FAIL and `full_ops_10_layer_verify.sh`=FAIL
- **Status:** PARTIAL
- **Blocker:** Cannot declare "ready" while two upstream verifiers FAIL
- **Next action:** Close row 29 (4 violations) + key full_ops layer fixes before saying "ready."

---

## Summary tally

| Status | Count | Rows |
|---|---|---|
| PASS | 5 | 3 (Offer ladder), 4 (Sales playbook), 18 (Proof Pack), 27 (Frontend), 28 (Production smoke) |
| PARTIAL | 18 | 1, 2, 5, 6, 8, 9, 13, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 30 |
| FAIL | 6 | 7, 10, 11, 12, 15, 29 |
| DEFERRED | 0 | (Article 11 not invoked) |
| BLOCKED | 1 | 26 (ZATCA — external certified provider needed) |

> Row 24 (RLS) is rated PARTIAL — application-layer tenant isolation works; Postgres-level RLS policies missing. Not a hard blocker for first customer (single-tenant prod), but mandatory before multi-tenant launch.

---

*Generated 2026-05-08 against base SHA `811fddd`.*
