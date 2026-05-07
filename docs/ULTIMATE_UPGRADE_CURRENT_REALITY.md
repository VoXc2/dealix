# Dealix — Wave 5 Ultimate Upgrade · Current Reality (Phase 0)

**Date:** 2026-05-07
**Branch:** `claude/service-activation-console-IA2JK`
**Pre-Wave-5 HEAD:** `585978e feat(integration): non-breaking executive Full-Ops Radar layer (Wave 4)`

---

## Pre-flight verifier baseline (run before Wave 5)

```
INTEGRATION_UPGRADE=PASS  (Wave 4 master verifier — 26/26)
DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS  (Wave 3 verifier — 18/18)
CUSTOMER_EXPERIENCE_AUDIT=PASS  (Wave 4 — 17/17)
test_constitution_closure.py  16/16
test_landing_forbidden_claims.py  3/3
SEO audit  pages=45, required_gap=0
Service registry  LIVE=8, TARGET=24
Internal linking planner  CLEAN
Working tree  clean
```

---

## What exists post-Wave-4 (the platform we're hardening)

### Modules (auto_client_acquisition/)

| Layer | Module | Wave |
|---|---|---|
| LeadOps Spine | `leadops_spine/` | Wave 3 |
| Customer Brain | `customer_brain/` | Wave 3 |
| Service Sessions | `service_sessions/` | Wave 3 |
| Approval Center (extended) | `approval_center/` | Wave 1 + Wave 3 ext. |
| Payment Ops | `payment_ops/` | Wave 3 |
| Proof Ledger (extended) | `proof_ledger/` | Wave 1 + Wave 3 ext. |
| Support Inbox | `support_inbox/` | Wave 3 |
| Support OS (legacy) | `support_os/` | V12 |
| Executive Pack v2 | `executive_pack_v2/` | Wave 3 |
| Case Study Engine | `case_study_engine/` | Wave 3 |
| Full-Ops Contracts | `full_ops_contracts/` | Wave 3 |
| Integration Upgrade adapter | `integration_upgrade/` | Wave 4 |
| Unified Operating Graph | `unified_operating_graph/` | Wave 4 |
| Full-Ops Radar | `full_ops_radar/` | Wave 4 |
| Executive Command Center | `executive_command_center/` | Wave 4 |
| WhatsApp Decision Bot | `whatsapp_decision_bot/` | Wave 4 |
| Channel Policy Gateway | `channel_policy_gateway/` | Wave 4 |
| Radar Events | `radar_events/` | Wave 4 |
| Agent Observability | `agent_observability/` | Wave 4 |
| Older internal modules (V10/V11/V12/V12.5) | various | pre-Wave 3 |

### Routers (api/routers/) — count

- 76 routers registered in `api/main.py` (verified via OpenAPI)
- All Wave 1-4 routers respond with `_HARD_GATES` dict

### Customer-facing surface

| Page | Wave | Notes |
|---|---|---|
| `/` (homepage) | various | Wave 2.5 hero CTAs |
| `/launchpad.html` | Wave 2.5 | Closed-package surface |
| `/customer-portal.html` | Wave 2.6 | 3-state UX (DEMO/SIGNED_UP/LIVE) |
| `/executive-command-center.html` | Wave 4 | 4-state UX |
| `/diagnostic.html` + sector variants | Wave 1 | |
| `/start.html`, `/pricing.html`, `/compare.html` | Wave 1 | |
| `/proof.html`, `/workflow.html` | Wave 1 | |

### Verifiers + scripts

- `scripts/v10_master_verify.sh` — V10 base
- `scripts/v11_customer_closure_verify.sh` — V11 customer closure
- `scripts/v12_full_ops_verify.sh` — V12 Full-Ops
- `scripts/beast_level_verify.sh` — Beast layer
- `scripts/revenue_execution_verify.sh` — revenue
- `scripts/full_ops_10_layer_verify.sh` — Wave 3 (18 checks)
- `scripts/integration_upgrade_verify.sh` — Wave 4 (26 checks)
- `scripts/customer_experience_audit.sh` — Wave 4 (17 checks)
- `scripts/launch_readiness_check.py`
- `scripts/seo_audit.py`
- `scripts/verify_service_readiness_matrix.py`

---

## Top 20 improvement opportunities (Wave 5 targets)

| # | Opportunity | Phase |
|---|---|---|
| 1 | 32 internal module names → 4 customer-facing names (Radar/AI Team/Portal/Proof) | Phase 1 |
| 2 | ECC cards lack 8-field business schema (signal/why_now/risk/impact/owner/action_mode/proof_link/recommended_action) | Phase 2 |
| 3 | Customer portal empty states are generic (no Arabic helper copy) | Phase 3 |
| 4 | LeadOps has no health/debug surface (`/reliability` missing) | Phase 4 |
| 5 | Full-Ops Score response shape inconsistent in some downstream readers | Phase 5 |
| 6 | No gross-margin per-service visibility (founder can't see which package bleeds) | Phase 6 |
| 7 | Support is ticket-only, no buyer-journey stages | Phase 7 |
| 8 | No unified tool guardrail gateway (channel_policy_gateway is per-channel only) | Phase 8 |
| 9 | Agent observability has no cost-summary aggregation | Phase 9 |
| 10 | Frontend has 3+ CTAs per page (should be 1 primary + 1 secondary) | Phase 10 |
| 11 | Some endpoints return 500 on subsystem missing instead of degraded section | Phase 11 |
| 12 | No mobile-first audit on customer-facing HTML | Phase 12 |
| 13 | Sales/founder lacks one-page revenue playbook for warm-intro outreach | Phase 13 |
| 14 | No master verifier that chains Wave 3 + Wave 4 + Wave 5 | Phase 14 |
| 15 | Risk register isn't surfaced as separate ECC section yet | Phase 2 (in card schema) |
| 16 | Demo labels not always shown when state=DEMO | Phase 3 |
| 17 | Performance budgets unenforced (no fast-fail on slow endpoints) | Phase 11 |
| 18 | Cost budget not enforced per-LLM-call (potential runaway cost) | Phase 8 (cost_budget.py) |
| 19 | Trust badges not visible on customer-portal/executive-command-center | Phase 10 |
| 20 | No bilingual font-loading verification | Phase 12 |

---

## What can be reused (most of the work)

Per the plan Section 22 reuse map, ~85% of Wave 5 functionality maps to existing modules:
- `payment_ops` → revenue ground truth for Phase 6
- `support_inbox` + `support_os` → 7-stage classifier for Phase 7
- `channel_policy_gateway` + `designops/safety_gate` → input/output guardrails for Phase 8
- `agent_observability` → cost-summary endpoint for Phase 9
- `full_ops_radar` (already complete) → Phase 5 polish only
- `executive_command_center` (already complete) → Phase 2 schema additions only
- `customer_company_portal` enriched_view (Wave 3+4) → empty states only

## What MUST NOT be touched

- 8-section `sections` invariant (constitutional)
- 14 enriched_view keys (6 Wave 3 + 8 Wave 4) — additive only
- 3-state portal UX
- `_HARD_GATES` pattern in every router
- 18-check Wave 3 verifier (must stay PASS)
- 26-check Wave 4 verifier (must stay PASS)
- All ~200 existing tests
- Existing pricing on `/pricing.html` (Phase 13 doc-only)

## Customer-ready vs internal-only inventory

**Customer-ready surfaces:**
- `/`, `/launchpad.html`, `/customer-portal.html`, `/executive-command-center.html`, `/diagnostic*.html`, `/start.html`, `/pricing.html`, `/compare.html`, `/proof.html`, `/workflow.html`, `/ai-team.html`

**Internal-only surfaces:**
- `/founder.html`, `/founder-leads.html`, `/founder-dashboard.html`, `/pilot-tracker.html`, `/decisions.html`, `/investor.html`, `/dealix-beast-power.html`, `/command-center.html`
- All `/api/v1/*` endpoints (server-only — never exposed in HTML)

**Demo-only:**
- `/customer-portal.html` (no params) — DEMO state
- `/executive-command-center.html` (no params) — DEMO state

## What blocks revenue (per-tier diagnosis)

| Tier | Blocker if any |
|---|---|
| Free Diagnostic | None — fully working |
| 7-Day Sprint (499) | Founder must manually confirm Moyasar payment (acceptable for MVP) |
| Data-to-Revenue Pack (1,500) | Customer Brain snapshot must be built per customer (Wave 3 P3 already complete) |
| Managed Revenue Ops (2,999-4,999/mo) | Need first 3 paid pilots before scaling |
| Executive Command Center (7,500-15,000/mo) | **Wave 5 makes this tier real** — ECC frontend + 15 sections + Full-Ops Score (Phase 2-5) |
| Agency Partner OS | Multi-tenant RLS (deferred until customer #2) |

## What blocks trust

- No public Trust Center page detailing the 8 hard gates in customer language → Phase 10 polish
- No SDAIA registration (founder action, not code)

## What blocks support

- Support journey is ticket-classification-only, no stage-based routing → Phase 7
- No SLA breach visibility on customer side → Phase 3 (already in enriched_view from Wave 4)

## What blocks proof

- No published Case Study yet (need first paid customer first — Article 13)
- Case Study Engine ready (Wave 3 P11) but no input data

## Acceptance for Phase 0

- [x] HEAD recorded: `585978e`
- [x] Wave 4 master verifier PASS confirmed
- [x] 20 named improvement opportunities captured
- [x] Reuse map summarized
- [x] Customer-ready / internal-only inventory captured
- [x] No code behaviour changed
