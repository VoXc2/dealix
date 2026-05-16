# Dealix Repositioning Rollout — Governed Revenue & AI Operations Company

**Status:** APPROVED by founder (Sami) — full repositioning + comprehensive implementation.
**Branch:** `claude/dealix-governed-revenue-ops-KCCy4`
**Date opened:** 2026-05-16

This document is the canonical execution record for the strategic repositioning
of Dealix from a 5-rung AI-ops offer ladder to a **Governed Revenue & AI
Operations Company** with a 7-service catalog. It is the single source of truth
for what was decided, sequenced, and shipped.

---

## 1. Target positioning (canonical)

**Dealix = Governed Revenue & AI Operations Company.**

- **EN:** "Dealix helps companies turn AI experiments and revenue operations into
  governed, measurable, evidence-backed workflows."
- **AR:** "Dealix تساعد الشركات على تحويل تجارب الذكاء الاصطناعي وعمليات الإيراد
  إلى تشغيل محكوم، قابل للقياس، ومربوط بالأدلة."

**Differentiator vs ordinary RevOps firms:** every recommendation, follow-up, and
sales decision is tied to `source_ref` + approval + evidence + decision passport.
Lead commercial entry point = **Governed Revenue Operations**, NOT CRM tidy-up.

## 2. Company evolution sequence (do NOT skip ahead)

Service → Repeatable Sprint → Retainer → Internal Platform → Client Workspace →
SaaS Module. Current form = **service-led company with software-assisted
delivery + governance/evidence layer.** Platform comes later.

## 3. The 7 moats

Proof moat · Trust moat · Revenue moat · Workflow moat · Saudi/GCC localization
moat · Approval-first safety moat · Service-to-platform learning moat.

---

## 4. Phased rollout

### Phase 1 — Doctrine + positioning + 7-service catalog (docs)
- New canonical positioning doc (this repositioning).
- New canonical 7-service catalog doc.
- First offer to market spec: **Governed Revenue Ops Diagnostic**.
- Reconcile `SERVICE_REGISTRY.md`, `SERVICE_ID_MAP.yaml`,
  `service_readiness_defaults.yaml`, `DEALIX_READINESS.md`, stage gates.
- Archive old 5-rung ladder (`OFFER_LADDER.md`) — mark SUPERSEDED, move copy to
  `docs/archive/`.
- Owner: dealix-content (bilingual AR+EN).

### Phase 2 — Backend domains + APIs + state machine
- Domain manifest: clients, contacts, market_proof, revenue_ops, diagnostics,
  evidence, approvals, billing, board_decision, reports.
- Extend existing `/api/v1/revenue-os/*` surface (do NOT duplicate):
  - `POST /api/v1/revenue-ops/diagnostics`
  - `POST /api/v1/revenue-ops/upload`
  - `POST /api/v1/revenue-ops/score`
  - `GET  /api/v1/revenue-ops/{id}/decision-passport`
  - `POST /api/v1/revenue-ops/{id}/follow-up-drafts`
  - `POST /api/v1/evidence/events`
  - `POST /api/v1/approvals`
  - `POST /api/v1/invoices`
- Engagement state machine: draft → approved → sent → used_in_meeting (L5) →
  scope_requested (L6) → invoice_sent (L7 candidate) → invoice_paid (L7).
- Owner: dealix-engineer.

### Phase 3 — Frontend 6 screens
1. Founder Command Center, 2. Service Catalog, 3. Market Proof Console,
4. Revenue Ops Console (most important), 5. Evidence Ledger, 6. Billing/Invoices.
- No "Send automatically" button anywhere.
- Owner: dealix-engineer (or scope note if frontend out of band).

### Phase 4 — Outreach drafts + metrics
- First 5 warm-list outreach drafts (queue as drafts only — never send).
- Metrics: sent_count, reply_count, meeting_count, diagnostic_scope_requested,
  invoice_sent, invoice_paid, proof_pack_created, retainer_opportunity.
- Owner: dealix-sales + dealix-content.

---

## 5. Non-negotiables enforced throughout

No scraping · no cold WhatsApp · no LinkedIn automation · no autonomous external
send · every claim evidence-backed (`source_ref`) · draft→approval→send state
machine · no guarantee language · no PII in logs · no source-less answers · no
project without Proof Pack · no project without Capital Asset.

---

## 6. Execution log

(Updated incrementally as each phase commits.)

- [x] **Phase 1 — docs** (2026-05-16)
  - `docs/strategic/DEALIX_GOVERNED_REVENUE_OPS_POSITIONING.md` (new — canonical positioning)
  - `docs/company/SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md` (new — canonical 7-service catalog)
  - `docs/services/governed_revenue_ops_diagnostic/offer.md` (new — first offer to market)
  - `docs/archive/OFFER_LADDER_5_RUNG_SUPERSEDED.md` (new — archived 5-rung ladder)
  - `docs/company/SERVICE_REGISTRY.md` (updated — 7-service catalog at top, old 3 marked SUPERSEDED)
  - `docs/company/OFFER_LADDER.md` (updated — SUPERSEDED banner)
  - `docs/company/POSITIONING.md` (updated — new canonical section at top)
  - `DEALIX_READINESS.md` (updated — official services = 7-service catalog)
- [x] **Phase 2 — backend** (2026-05-16)
  - `auto_client_acquisition/revenue_ops/__init__.py` (new — domain package)
  - `auto_client_acquisition/revenue_ops/state_machine.py` (new — governed engagement state machine)
  - `auto_client_acquisition/revenue_ops/diagnostics.py` (new — Governed Revenue Ops Diagnostic engine)
  - `api/routers/revenue_ops_engagements.py` (new — `/api/v1/revenue-ops` surface, 10 endpoints)
  - `api/routers/domains/sales/__init__.py` (updated — registers the new router)
  - `tests/test_revenue_ops_engagement_state_machine.py` (new — 11 doctrine tests, all passing)
  - `docs/strategic/GOVERNED_REVENUE_OPS_BACKEND_DOMAINS.md` (new — domain manifest + API + state machine)
- [x] **Phase 3 — frontend** (2026-05-16)
  - 6 screens under `frontend/src/app/[locale]/`: `founder-command-center`,
    `service-catalog`, `market-proof`, `revenue-ops-console`,
    `evidence-ledger`, `billing-invoices` (each a `page.tsx`)
  - `frontend/src/components/revenue-ops/RevenueOpsConsole.tsx` (new — primary console)
  - `frontend/src/components/revenue-ops/RevenueOpsScreens.tsx` (new — other 5 screens)
  - `frontend/src/lib/api.ts` (updated — `/api/v1/revenue-ops` client functions)
  - `frontend/src/components/layout/Sidebar.tsx` (updated — 6 new nav entries)
  - `frontend/messages/{en,ar}.json` (updated — `revenueOps` namespace + nav, bilingual)
  - Doctrine: NO "Send automatically" button on any screen; invoices are
    draft-only; every screen ends with the bilingual disclaimer.
- [x] **Phase 4 — outreach + metrics** (2026-05-16)
  - `data/outreach/governed_revenue_ops_warm_list_drafts.md` (new — 5 segment
    drafts: B2B services, consulting, SaaS, fintech, agency; all `draft` state,
    `approval_required=true`; email / warm intro only; signed "Sami")
  - `data/outreach/governed_revenue_ops_metrics.md` (new — 8-metric sheet, all 0)
- [x] **Phase 5 — readiness matrix wiring (all 7 services)** (2026-05-16)
  - All 7 catalog services now appear in the automated readiness matrix
    (`scripts/print_service_readiness_matrix.py`), each with an HONEST score.
  - `scripts/verify_service_files.py` (updated — added `REQUIRED_BY_FOLDER`
    keys for all 7 new folders + their required file lists).
  - `docs/company/SERVICE_ID_MAP.yaml` (updated — 7 new `{folder, service_id}`
    mappings).
  - `auto_client_acquisition/governance_os/policies/service_readiness_defaults.yaml`
    (updated — 7 new `service_id` entries with honest evidence flags).
  - 7 new service folders under `docs/services/` with real delivery blueprints:
    - `governed_revenue_ops_diagnostic/` — 10 new files + fixed `offer.md`
      (added `## Best for`, `## Duration`, `## Not included`, `## Success metric`
      to satisfy the verifier's 7 offer markers).
    - `revenue_intelligence_sprint/` — 11 files.
    - `governed_ops_retainer/` — 11 files.
    - `ai_governance_for_revenue_teams/` — 10 files.
    - `crm_data_readiness_for_ai/` — 10 files.
    - `board_decision_memo/` — 8 files (lighter document-led set).
    - `trust_pack_lite/` — 8 files (lighter request-only set).
  - Honest flag notes:
    - `has_demo: false` for ALL 7 — no demo pack was built under `demos/`.
    - `has_module_support: true` only for the 3 revenue-ops services backed by
      `auto_client_acquisition/revenue_ops/` + the `/api/v1/revenue-ops` router;
      `false` for the 4 document-led services (no dedicated code module).
    - `has_upsell_path: false` for `board_decision_memo` and `trust_pack_lite`
      (compact / request-only — no `upsell.md`).
  - Resulting honest scores: 3 revenue-ops services = 90 (Sellable/Excellent);
    `ai_governance_for_revenue_teams` and `crm_data_readiness_for_ai` = 75
    (Beta); `board_decision_memo` and `trust_pack_lite` = 65 (Not Ready).
  - Owner: dealix-engineer + dealix-content.

### Phase 5 readiness matrix (actual scores, 2026-05-16)

| Service folder | service_id | Score | Tier |
|----------------|------------|------:|------|
| lead_intelligence_sprint | lead_intelligence_sprint | 100 | Sellable/Excellent |
| ai_quick_win_sprint | quick_win_ops | 100 | Sellable/Excellent |
| company_brain_sprint | company_brain_sprint | 100 | Sellable/Excellent |
| ai_support_desk_sprint | support_desk_sprint | 90 | Sellable/Excellent |
| ai_governance_program | ai_governance_program | 100 | Sellable/Excellent |
| client_ai_policy_pack | client_ai_policy_pack | 100 | Sellable/Excellent |
| governed_revenue_ops_diagnostic | governed_revenue_ops_diagnostic | 90 | Sellable/Excellent |
| revenue_intelligence_sprint | revenue_intelligence_sprint | 90 | Sellable/Excellent |
| governed_ops_retainer | governed_ops_retainer | 90 | Sellable/Excellent |
| ai_governance_for_revenue_teams | ai_governance_for_revenue_teams | 75 | Beta |
| crm_data_readiness_for_ai | crm_data_readiness_for_ai | 75 | Beta |
| board_decision_memo | board_decision_memo | 65 | Not Ready |
| trust_pack_lite | trust_pack_lite | 65 | Not Ready |

The four sub-90 scores are correct and acceptable: they honestly reflect that
no demo pack and (for the document-led services) no backing code module exist
yet. Raising them is a deliberate future step (build demo packs; build code
modules where it makes sense) — not a flag flip.

---

## 7. Verification status (2026-05-16)

- `scripts/verify_dealix_ready.py --skip-tests` → **SELL_READY_STACK**.
- `scripts/verify_service_catalog.py` → **SERVICE_CATALOG_PASS=true**.
- `tests/test_revenue_ops_engagement_state_machine.py` → 11/11 passing.
- Doctrine guards (`test_no_guaranteed_claims`, `test_doctrine_guardrails`,
  `test_no_cold_whatsapp`, `test_no_scraping_engine`, `test_no_linkedin_automation`,
  `test_v7_no_fake_proof`, `test_decision_passport`, `test_revenue_os_catalog`,
  `test_commercial_engagements_lead_intelligence`) → all passing.
- Known pre-existing failure (NOT a regression from this work):
  `test_v7_no_guaranteed_claims::test_landing_pages_have_no_unallowlisted_forbidden_claims`
  fails on the merge-base commit `fe25274` as well — a landing-HTML allowlist
  gap. No landing HTML file was touched by this repositioning.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
