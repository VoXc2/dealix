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
- [ ] Phase 2 — backend
- [ ] Phase 3 — frontend
- [ ] Phase 4 — outreach + metrics

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
