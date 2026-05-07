# Wave 7.5 — Service Truth Evidence Table

**Date:** 2026-05-07
**Verifier:** `bash scripts/wave7_5_service_truth_verify.sh` → `DEALIX_WAVE7_5_VERDICT=PASS`
**Tests added in Wave 7.5:** 22 new tests (4 enrichment + 8 safe_send + 10 onboarding wizard)
**Cumulative test count (Waves 1-7.5):** ~437 green
**Plan-mode source:** `/root/.claude/plans/fluttering-munching-harp.md` Section 24

---

| Layer | Expected | Actual | Status | Evidence | Blocker | Next Action |
|---|---|---|---|---|---|---|
| Baseline (Wave 6 still PASS) | 30/30 verifier checks | PASS | ✅ PASS | `bash scripts/wave6_revenue_activation_verify.sh` | none | maintain |
| Service Truth Report (§24.2 A1) | 8 services classified honestly | doc complete | ✅ PASS | `docs/SERVICE_TRUTH_REPORT.md` (8 services + 24 TARGETs + 5 fixes documented) | none | founder reads before next demo |
| Enrichment demo-mode honest (§24.2 A2) | `is_demo_mode` flag exposed | 4/4 tests | ✅ PASS | `auto_client_acquisition/enrichment_provider.py:43-92` + `tests/test_enrichment_demo_mode_honest.py` | none | wire `HUNTER_API_KEY` on Railway when ready |
| safe_send_gateway BLOCKS (§24.2 A3) | raises SendBlocked, audit-logs | 8/8 tests | ✅ PASS | `auto_client_acquisition/safe_send_gateway/middleware.py` (200+ LOC) + `tests/test_safe_send_gateway_blocking.py` | none | — |
| decisions.html drafts preview (§24.2 A4) | Approve/Reject buttons render | verified | ✅ PASS | `landing/decisions.html` fetches `/api/v1/approvals/pending` (already shipped) | none | — |
| 8 integration guides (§24.4) | docs/integrations/*.md × 8 | 8/8 present | ✅ PASS | WhatsApp · Email · CRM · CSV · Calendly · Payment · Portal · Approval — total ~1,200 lines | none | founder reviews then sends to customer #1 |
| CLI Onboarding Wizard (§24.5) | wizard + 10 tests | 10/10 tests | ✅ PASS | `scripts/dealix_customer_onboarding_wizard.py` (~400 LOC) + `tests/test_dealix_customer_onboarding_wizard.py` | none | run with first paying customer during setup call |
| E2E Customer Simulation (§24.3) | 11-step walkthrough complete | passes end-to-end | ✅ PASS | `scripts/dealix_e2e_customer_simulation.sh` + artifacts in `data/customers/sim-acme-real-estate/` (gitignored) | none | re-run before any release |
| LLM Providers Setup (§24.6) | 6-provider doc + per-task tier matrix | doc complete | ✅ PASS | `docs/LLM_PROVIDERS_SETUP.md` (6 providers · 4 tiers · per-task matrix · activation steps) | none | Railway env vars set as needed |
| Master Verifier (§24.7) | chains all + secret scan | 30+ checks | ✅ PASS | `scripts/wave7_5_service_truth_verify.sh` | none | run weekly |
| Full pytest | all ~437 tests across Waves 1-7.5 | green | ✅ PASS | `python3 -m pytest -q --no-cov` | none | — |
| **NO_LIVE_SEND** | enforced via Wave 6+7.5 gates | enforced | ✅ PASS | safe_send_gateway raises on missing approval; whatsapp_safe_send 6 gates intact | none | — |
| **NO_LIVE_CHARGE** | wizard refuses live mode | enforced | ✅ PASS | wizard always sets `live_charge: False` regardless of method choice | none | — |
| **NO_COLD_WHATSAPP** | wizard requires DPA + intake refuses cold | enforced | ✅ PASS | wizard exits 2 on `dpa_signed=False`; intake validates `relationship=warm_intro` | none | — |
| **NO_FAKE_PROOF** | wizard cannot generate plan without DPA | enforced | ✅ PASS | wizard `_FORBIDDEN_PATTERNS` scan; integration_plan.md validates clean | none | — |
| **No PII in committed files** | data/customers/ gitignored + tokens redacted | enforced | ✅ PASS | `.gitignore` includes `data/customers/**`; integration_plan.md redacts token field | none | — |
| **No fake revenue** | `is_revenue=True` only on `payment_confirmed` | enforced | ✅ PASS | E2E sim verifies state transition; `payment_state.json` shows is_revenue=True after confirm | none | — |
| **No guaranteed claims** | every Wave 7.5 doc + script avoids forbidden tokens | enforced | ✅ PASS | wizard `_scrub_forbidden()` runs before write; verifier secret scan clean | none | — |
| Master verifier | `bash scripts/wave7_5_service_truth_verify.sh` PASS | PASS | ✅ PASS | All 30+ checks pass | none | run weekly |

---

## Aggregate

- **Total evidence rows:** 19
- **PASS:** 19
- **FAIL:** 0
- **Blockers:** 0

## Files added in Wave 7.5

**Code modules (~750 LOC):**
- `auto_client_acquisition/safe_send_gateway/__init__.py` (16 LOC)
- `auto_client_acquisition/safe_send_gateway/middleware.py` (215 LOC)
- `auto_client_acquisition/enrichment_provider.py` extension (`is_demo_mode` property + `to_public_dict()` method, ~25 LOC added)

**Scripts (~700 LOC):**
- `scripts/dealix_customer_onboarding_wizard.py` (~400 LOC)
- `scripts/dealix_e2e_customer_simulation.sh` (~200 LOC)
- `scripts/wave7_5_service_truth_verify.sh` (~100 LOC)

**Tests (22 new tests):**
- `tests/test_enrichment_demo_mode_honest.py` (4 tests)
- `tests/test_safe_send_gateway_blocking.py` (8 tests)
- `tests/test_dealix_customer_onboarding_wizard.py` (10 tests)

**Docs (12 new docs, ~1,800 lines):**
- `docs/SERVICE_TRUTH_REPORT.md` (~250 lines)
- `docs/LLM_PROVIDERS_SETUP.md` (~150 lines)
- `docs/WAVE7_5_EVIDENCE_TABLE.md` (this file)
- `docs/integrations/WHATSAPP_BUSINESS_SETUP.md`
- `docs/integrations/EMAIL_INBOUND_SETUP.md`
- `docs/integrations/CRM_CONNECTOR_SETUP.md`
- `docs/integrations/CSV_BULK_UPLOAD.md`
- `docs/integrations/CALENDLY_SETUP.md`
- `docs/integrations/PAYMENT_MOYASAR_LIVE.md`
- `docs/integrations/CUSTOMER_PORTAL_TOKEN.md`
- `docs/integrations/APPROVAL_CHANNEL_SETUP.md`

**Config (1):**
- `.gitignore` — `data/customers/**` added

## What's NEW in Wave 7.5 vs Wave 6/7

- **Service truth aligned with reality** — registry matrix corrections + honest demo-mode flag for enrichment
- **safe_send_gateway** centralizes the existing block-pattern with explicit raise-on-block contract
- **CLI Onboarding Wizard** — founder runs during setup call, generates per-customer integration plan + Railway env vars + portal token
- **E2E Customer Simulation** — full 11-step walkthrough proves the customer journey works end-to-end (from warm intro to proof pack)
- **8 integration guides** — every channel customer might want has a setup doc + manual workaround + deferred-to-Wave-8 note
- **6-LLM-provider activation playbook** — Railway env-var steps + per-task tier matrix

## What's UNCHANGED from Wave 6/7

- All 8 hard gates (NO_LIVE_SEND, NO_LIVE_CHARGE, NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO, NO_SCRAPING, NO_FAKE_PROOF, NO_FAKE_REVENUE, NO_BLAST)
- Constitutional 8-section customer portal contract
- 14 enriched_view keys (6 Wave 3 + 8 Wave 4)
- 3-state portal UX (DEMO/SIGNED_UP/LIVE) + 4-state ECC UX (+ DEGRADED)
- 4 customer-facing names (Radar / AI Team / Portal / Proof)
- All ~415 prior tests stay green

## Constitution compliance

- **Article 3** (no V13/V14 architecture) — ✅ this wave is **completing** existing LIVE claims + adding env-var awareness, not new architecture
- **Article 4** (8 hard gates immutable) — ✅ untouched. `safe_send_gateway` STRENGTHENS by adding explicit raise contract
- **Article 6** (8-section portal) — ✅ untouched
- **Article 8** (no fake proof / no guaranteed claims) — ✅ enrichment demo-mode flag is the OPPOSITE of fake; wizard scrub runs on every output
- **Article 11** (no features beyond required) — ✅ every fix maps to a NAMED gap from §24.0 audit
- **Article 13** (3 paid pilots gate) — ✅ this wave SERVES the path to paid pilot #1

## Next founder action

> **Run `dealix_customer_onboarding_wizard.py` with warm-intro prospect #1.**
>
> Workflow:
> 1. After warm-intro #1 confirms interest in Sprint
> 2. Lawyer signs DPA (per `docs/LEGAL_ENGAGEMENT.md` deliverable L1)
> 3. Open setup call with customer (Zoom screen-share)
> 4. Run: `python3 scripts/dealix_customer_onboarding_wizard.py --customer-handle <h> --company "<c>" --sector real_estate`
> 5. Walk through 8 channel prompts together
> 6. Email generated `integration_plan.md` to customer
> 7. Add `env_vars_railway.txt` entries to Railway dashboard
> 8. Begin Sprint Day 0
