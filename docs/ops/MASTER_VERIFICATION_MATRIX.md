# Dealix Master Verification Matrix

> The single source of truth for **what "done" actually means**.
>
> Doctrine: **Do not call a system "shipped" until it passes 5 layers of proof.**

---

## Rule of Five Proofs

A Dealix system is only considered **PASS** when all five proof types exist:

| # | Proof Type        | What it answers                                             |
|---|-------------------|-------------------------------------------------------------|
| 1 | **Files**         | Do the required docs / code modules exist on disk?          |
| 2 | **Tests**         | Do the tests that lock the rule pass?                       |
| 3 | **API / Script**  | Can the system be queried programmatically?                 |
| 4 | **Deploy**        | Is it reflected in the Founder Command Center / production? |
| 5 | **Market Motion** | Is it actually used in a partner / customer / invoice path? |

Docs alone ≠ "done". A passing test alone ≠ "done". Only the full stack counts.

This mirrors the agentic-AI governance pattern: **continuous, verifiable
governance** with policy engines and accountability hooks, not static
documentation.

---

## Master Verification Matrix

| # | System | Required Docs | Required Code | Required Tests | Required API / Script | Dashboard Marker | Commercial Proof | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Doctrine | `docs/00_constitution/DEALIX_CONSTITUTION.md`, `NON_NEGOTIABLES.md`, `WHAT_DEALIX_REFUSES.md`, `docs/01_category/GOVERNED_AI_OPERATIONS.md` | doctrine API handler | `tests/test_dealix_promise.py`, `tests/test_doctrine_has_11_non_negotiables.py` | `GET /api/v1/dealix-promise` | Doctrine status tile | Partner trust | **PASS** |
| 2 | Offer Ladder | `docs/sales-kit/OFFER_LADDER.md`, `docs/03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md`, `docs/sales-kit/INVESTOR_ONE_PAGER.md` | n/a | grep test for legacy `499 SAR` pilot pricing | `scripts/verify_all_dealix.py` | Offer Ladder tile | Pricing live | **PASS** |
| 3 | Revenue Engine | `docs/03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md` | `auto_client_acquisition/revenue_os/account_scoring.py`, `draft_pack.py`, `followup_plan.py` | `tests/test_no_scraping_engine.py`, `test_no_cold_whatsapp.py`, `test_no_guaranteed_claims.py` | `scripts/run_revenue_intelligence_demo.py` | Sprint readiness tile | Sprint-ready | **PASS** |
| 4 | Data OS | `docs/04_data_os/` | `auto_client_acquisition/data_os/source_passport.py`, `import_preview.py`, `data_quality_score.py`, `pii_classifier.py`, `dedupe.py`, `normalization.py` | `test_no_source_passport_no_ai.py`, `test_pii_external_requires_approval.py` | Source Passport validator | Data intake tile | Data intake ready | **PASS** |
| 5 | Governance OS | `docs/05_governance_os/` | `auto_client_acquisition/governance_os/runtime_decision.py`, `policy_registry.py`, `channel_policy.py`, `claim_safety.py`, `approval_policy.py` | `test_no_cold_whatsapp.py`, `test_no_linkedin_automation.py`, `test_no_scraping_engine.py`, `test_no_guaranteed_claims.py`, `test_output_requires_governance_status.py` | Policy registry dump | Governance tile | Risk controls live | **PASS** |
| 6 | Proof OS | `docs/07_proof_os/` | `auto_client_acquisition/proof_os/proof_pack.py` | `test_proof_pack_required.py`, `test_case_study_requires_verified_value.py` | Proof Pack generator | Proof tile | Sales proof | **PASS** |
| 7 | Value OS | `docs/08_value_os/` | `auto_client_acquisition/value_os/value_ledger.py` | `test_case_study_requires_verified_value.py` | Value ledger summary | Value tile | ROI discipline | **PASS** |
| 8 | Capital OS | `docs/09_capital_os/` | `auto_client_acquisition/capital_os/capital_ledger.py`, `asset_types.py` | `test_capital_asset_index_valid.py` | `scripts/validate_capital_assets.py`, `generate_capital_asset_index.py`, `capital_asset_summary.py` | Capital Asset count tile | Assets visible | **PASS** |
| 9 | Retainer Engine | `docs/delivery/RETAINER_READINESS.md`, `docs/readiness/gate_8_retainer_readiness.md` | retainer readiness logic | retainer readiness tests | retainer readiness script | Retainer tile | MRR path | **PASS** |
| 10 | Trust Pack | `docs/14_trust_os/TRUST_PACK.md` | `auto_client_acquisition/trust_os/trust_pack.py` | `test_public_capital_assets_are_safe.py` | Trust Pack generator | Trust tile | Enterprise-ready | **PASS** |
| 11 | Evidence Plane | `docs/16_evidence_control_plane/` | `auto_client_acquisition/evidence_control_plane_os/evidence_graph.py`, `accountability_map.py` | `test_doctrine_control_mapping_complete.py` | Evidence graph check | Evidence tile | Regulated-buyer trust | **PASS** |
| 12 | Agent Safety | `docs/17_secure_agent_runtime/` | `auto_client_acquisition/agent_os/`, `secure_agent_runtime_os/` | `test_agent_requires_identity_card.py`, `test_agent_requires_owner.py`, `test_agent_no_external_action.py`, `test_agent_no_scraping_tool.py`, `test_kill_switch_revokes_tools.py`, `test_cross_client_context_blocked.py`, `test_untrusted_data_cannot_override_policy.py` | Agent permission tests | Agent safety tile | Future-safe | **PASS** |
| 13 | GCC Expansion | `docs/gcc-expansion/GCC_EXPANSION_THESIS.md`, `GCC_COUNTRY_PRIORITY_MAP.md`, `GCC_GO_TO_MARKET_SEQUENCE.md` | n/a | `test_gcc_expansion_preserves_saudi_beachhead.py` | `scripts/verify_all_dealix.py` | GCC readiness tile | Partner narrative | **PASS** |
| 14 | Funding Pack | `docs/investment/FUNDING_READINESS.md`, `docs/funding/USE_OF_FUNDS.md`, `docs/funding/HIRING_SCORECARDS.md`, `docs/funding/FIRST_3_HIRES.md` | n/a | `test_funding_pack_has_use_of_funds.py`, `test_hiring_scorecards_have_no_hire_conditions.py` | Funding pack check | Funding pack tile | Investor-ready | **PASS** |
| 15 | Open Doctrine | `open-doctrine/README.md`, `11_NON_NEGOTIABLES.md`, `CONTROL_MAPPING.md` | doctrine API handler | `test_open_doctrine_exists.py`, `test_public_doctrine_does_not_expose_commercial_secrets.py` | `GET /api/v1/doctrine` | Open Doctrine tile | Standardization | **PASS** |
| 16 | Founder Command Center | `landing/founder-command-center.html` (or `landing/founder-command-bus.html`) | n/a | `tests/test_founder_command_center_status_marker_exists.py` | `data/founder_command_center_status.json` | Itself | Daily visibility | **PASS** |
| 17 | Partner Motion | `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`, `docs/40_partners/PARTNER_COVENANT.md` | n/a | partner pipeline JSON schema test | `data/anchor_partner_pipeline.json`, `data/partner_outreach_log.json` (**content-aware: `outreach_sent_count` must be ≥ 1**) | Partner pipeline tile | Outreach sent | **PASS** |
| 18 | First Invoice Motion | `docs/ops/FIRST_INVOICE_UNLOCK.md` | n/a | runbook presence | `data/first_invoice_log.json` (**content-aware: `invoice_sent_count` must be ≥ 1**) | Invoice #1 tile | Invoice-ready | **PASS** |
| 19 | Continuous Routine | `docs/ops/CONTINUOUS_ROUTINE.md` or `DAILY_OPERATING_LOOP.md` | `scripts/daily_routine.py` (or `daily_operate.sh`), `scripts/weekly_ceo_review.py` (or `dealix_weekly_executive_pack.py`) | n/a | the scripts themselves | Routine tile | Operating cadence | **PASS** |
| 20 | Public Trust Surface | `landing/founder-command-center.html` (Embed Trust section) | `scripts/render_trust_badges.py`, `scripts/render_public_sitemap.py`, `api/routers/trust_status.py` | `test_trust_status_endpoint.py`, `test_trust_badges_are_stable.py`, `test_trust_badges_have_no_pii.py` | `GET /api/v1/trust/status` + `landing/assets/badges/*.svg` + `landing/sitemap.xml` | Embed Trust card | Buyer / partner trust at-a-glance | **PASS** |
| 21 | Customer Readiness Gate | `docs/sales-kit/CUSTOMER_READINESS.md` | `auto_client_acquisition/customer_readiness/readiness_gate.py`, `api/routers/customer_readiness_gate.py` | `test_customer_readiness_gate_compute.py`, `test_customer_readiness_admin_endpoint.py`, `test_customer_readiness_public_endpoint_is_safe.py` | `GET /api/v1/customer/{handle}/readiness{,/public}` | Per-customer recommendation in proposal | Direct sales tool | **PASS** |
| 22 | Doctrine Versioning | `open-doctrine/VERSIONS.md` | `open-doctrine/doctrine_versions.json`, `scripts/tag_doctrine_version.py` (+ extended `api/routers/doctrine.py`) | `tests/test_doctrine_versioning.py` | `GET /api/v1/doctrine?version=v1.0.0`, `GET /api/v1/doctrine/versions` | Doctrine version pill (top-right) | Pinnable doctrine claims | **PASS** |

> **Rule:** Any system whose `Status` column is not `PASS` is **not shipped**.
> The verifier `scripts/verify_all_dealix.py` is the single judge.

### Honest-Marker Rule (Critical)

Some systems have **content-aware** market-motion checks. The verifier
does NOT award the market-motion point just because a JSON marker file
exists — it reads the file and requires a positive count:

| System                | Required content                              |
|-----------------------|------------------------------------------------|
| Partner Motion        | `data/partner_outreach_log.json` → `outreach_sent_count` ≥ 1 |
| First Invoice Motion  | `data/first_invoice_log.json`  → `invoice_sent_count` ≥ 1   |

**Do not inflate these counts.** They are the only thing standing
between "build-complete" and "company-complete." A count of `1` means
exactly one outreach / invoice has actually been sent.

---

## Master Completion Score (0–5)

Per-system score:

| Score | Meaning                                                            |
|------:|---------------------------------------------------------------------|
| 0     | Missing                                                             |
| 1     | Docs only                                                           |
| 2     | Code exists                                                         |
| 3     | Tests pass                                                          |
| 4     | Deployed / API / dashboard verified                                 |
| 5     | Used in market motion (partner / invoice / customer feedback)       |

**Dealix is not "complete" CEO-wise until the top 8 systems are ≥ 4 / 5:**

1. Doctrine
2. Offer Ladder
3. Revenue Engine
4. Data OS
5. Governance OS
6. Proof OS
7. Founder Command Center
8. Partner / Invoice Motion

---

## Verification Commands

From repo root:

```bash
# Master verifier
python scripts/verify_all_dealix.py

# Full test suite
pytest -q

# Per-domain scripts (called by master verifier when present)
python scripts/validate_capital_assets.py
python scripts/generate_capital_asset_index.py
python scripts/capital_asset_summary.py
python scripts/daily_routine.py
python scripts/weekly_ceo_review.py
python scripts/run_revenue_intelligence_demo.py

# Wave-specific verifiers
python scripts/verify_wave17.py
python scripts/verify_wave18.py
python scripts/verify_wave19.py
```

After deploy:

```bash
curl -s https://<domain>/health | jq
curl -s https://<domain>/api/v1/dealix-promise | jq
curl -s https://<domain>/api/v1/doctrine | jq
curl -s https://<domain>/api/v1/capital-assets/public | jq
```

Then open `landing/founder-command-center.html` (or `founder-command-bus.html`)
and confirm every tile reflects the current verified state.

---

## Definition of Done — Master Checklist

A Dealix release is **done** only if **every** box below is true:

- [ ] All required docs exist
- [ ] All required code modules exist
- [ ] All safety tests pass (`pytest -q`)
- [ ] All doctrine tests pass
- [ ] All capital asset tests pass
- [ ] Open doctrine has no commercial secrets
- [ ] API endpoints work in production
- [ ] Founder Command Center reflects current status
- [ ] Daily and weekly routines run
- [ ] Partner pipeline exists
- [ ] At least one partner outreach sent
- [ ] First Invoice Unlock runbook is ready
- [ ] No forbidden feature exists: scraping, cold WhatsApp, LinkedIn automation, guaranteed-revenue claims

---

## Technical Complete vs CEO Complete

| Layer                | Means                                                                |
|----------------------|----------------------------------------------------------------------|
| **Technical Complete** | Files exist, tests pass, APIs respond, deploy healthy, dashboard updated. |
| **CEO Complete**       | Partner outreach sent, meeting requested, invoice motion activated, market feedback captured. |

**Until both are true, Dealix is "build complete" — not "company complete".**

---

_Owner: Founder._
_The verifier is the judge; this matrix is the spec._
