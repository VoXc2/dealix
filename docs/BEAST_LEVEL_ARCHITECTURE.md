# Dealix V12.5 Beast Level Architecture

> **Founder decision (explicit):** "Build the beast first, launch second."
> This iteration converts Dealix from "Full-Ops + RX" into a true
> Self-Growing Saudi AI Revenue & Company Operating System.

## What V12.5 Beast adds (5 new layers on top of V12+RX)

| Layer | Path | New modules | Purpose |
|---|---|---|---|
| **B1 RevOps** | `auto_client_acquisition/revops/` | invoice_state, payment_confirmation, margin, finance_brief | Complete the financial truth layer started in RX (revenue_pipeline) |
| **B2 Growth Beast** | `auto_client_acquisition/growth_beast/` | market_radar, signal_engine, icp_score, account_ranker, offer_intelligence, content_engine, warm_route, experiment_engine, proof_to_content, weekly_learning | Self-targeting engine for Dealix's own growth |
| **B3 Company Growth Beast** | `auto_client_acquisition/company_growth_beast/` | company_profile, growth_diagnostic, target_segment_engine, offer_matcher, content_pack_builder, support_to_growth, proof_loop, weekly_report, command_center | Same engine, packaged as a service for client companies |
| **B4 Role Command** | `auto_client_acquisition/role_command/` (extends `role_command_os/`) | ceo, growth, sales, support, cs, delivery, finance, compliance, ops | 9 role-specific daily decision endpoints |
| **B5 Proof-to-Market** | `auto_client_acquisition/proof_to_market/` | proof_selector, approval_gate, content_snippet, case_study_candidate, sector_learning | Convert real proof events into approval-required marketing content |

## What stays UNCHANGED (no regression)

- All V11/V12/V13/RX modules (do not modify)
- All hard gates (no live send/charge/cold WhatsApp/scraping/fake proof)
- All 9 V12 OSes
- Daily Command Center (extended with Beast feeds)
- Knowledge Base (V12)
- Phase E execution kit (V11)
- Test perimeter (1644+ tests preserved)

## Hard rules (Beast version — even stricter than V12)

| Rule | Beast enforcement |
|---|---|
| no live send | Compliance OS action_check is the ONLY gate; Growth Beast outputs `draft_only` always |
| no live charge | RevOps `payment_confirmation` requires explicit evidence string; CLI rejects `sk_live_*` without `--allow-live` |
| no scraping | Market Radar uses ONLY public-source signal types (job_post / press / tender / directory); no HTTP fetch in V12.5 (signal sources are caller-supplied for now) |
| no cold WhatsApp | Warm Route Engine HARD-blocks `cold_whatsapp` channel; only `warm_intro / partner_intro / inbound_reply / public_content_cta` allowed |
| no LinkedIn automation | Channel enum excludes `linkedin_dm_automation`; messaging is `manual_send_only` always |
| no fake proof | Proof-to-Market `approval_gate` requires `customer_signed_permission=true` before any external content |
| no fake metric | RevOps `finance_brief` distinguishes `cash_collected` (real) vs `commitments_open` (signed) vs `pipeline_value` (qualified) |
| no fake forecast | Executive OS `weekly_pack` returns `data_status="insufficient_data"` if N<3 paid pilots |
| no auto PR | Self-Improvement OS suggestions are `suggest_only`; no GitHub MCP write actions from inside the loop |

## The 5 Beast Loops

```
Loop 1 — Signal Loop:
  market signal → ICP score → account rank → offer match → action recommendation

Loop 2 — Content Loop:
  pain insight → content draft → approval-required publish → inbound → diagnostic

Loop 3 — Sales Loop:
  lead → qualification → objection → follow-up → pilot → proof

Loop 4 — Support Loop:
  ticket → category → KB gap → better answer → fewer repeats

Loop 5 — Proof Loop:
  delivery → proof event → proof pack → case snippet → stronger targeting
```

## API surface added (~25 new endpoints)

```
# B1 RevOps
GET  /api/v1/revops/status
POST /api/v1/revops/invoice-state
POST /api/v1/revops/payment-confirm
POST /api/v1/revops/margin-snapshot
GET  /api/v1/revops/finance-brief

# B2 Growth Beast (Dealix self-growth)
GET  /api/v1/growth-beast/status
POST /api/v1/growth-beast/signals/evaluate
POST /api/v1/growth-beast/targets/rank
POST /api/v1/growth-beast/offer/match
POST /api/v1/growth-beast/content/draft
POST /api/v1/growth-beast/warm-route/draft
POST /api/v1/growth-beast/experiment/next
GET  /api/v1/growth-beast/today

# B3 Company Growth Beast (service for clients)
GET  /api/v1/company-growth-beast/status
POST /api/v1/company-growth-beast/profile
POST /api/v1/company-growth-beast/diagnostic
POST /api/v1/company-growth-beast/targets
POST /api/v1/company-growth-beast/offer
POST /api/v1/company-growth-beast/content-pack
GET  /api/v1/company-growth-beast/weekly-report

# B4 Role Command (9 roles)
GET  /api/v1/role-command/today/{role}    # role ∈ ceo/growth/sales/support/cs/delivery/finance/compliance/ops

# B5 Proof-to-Market
GET  /api/v1/proof-to-market/status
POST /api/v1/proof-to-market/select
POST /api/v1/proof-to-market/snippet
POST /api/v1/proof-to-market/case-study-candidate
GET  /api/v1/proof-to-market/sector-learning
```

## Tests added (target: ~120)

- `tests/test_revops_*.py` (4 files, ~25 tests)
- `tests/test_growth_beast_*.py` (5 files, ~30 tests)
- `tests/test_company_growth_beast_*.py` (5 files, ~30 tests)
- `tests/test_role_command_*.py` (1 file, ~20 tests)
- `tests/test_proof_to_market_*.py` (3 files, ~15 tests)
- `tests/test_beast_level_verify.py` (1 file, ~6 tests)

## Beast verifier output

```
DEALIX_BEAST_LEVEL=PASS
PRODUCTION_TRUTH=
V11_VERIFIER=PASS
V12_FULL_OPS_VERIFY=PASS
REVENUE_EXECUTION_VERIFY=PASS
REVOPS=pass
GROWTH_BEAST=pass
COMPANY_GROWTH_BEAST=pass
ROLE_COMMAND=pass (9/9 roles)
PROOF_TO_MARKET=pass
NO_FAKE_PROOF=pass
NO_FAKE_REVENUE=pass
NO_LIVE_SEND=pass
NO_LIVE_CHARGE=pass
NO_COLD_WHATSAPP=pass
NO_SCRAPING=pass
ARABIC_PRIMARY=pass
NEXT_FOUNDER_ACTION=Open V12.5 Beast PR → merge → Railway redeploy → start Day 1 Launch Kit
```
