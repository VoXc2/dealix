---
doc_id: strategy.90_day_plan
title: Dealix 90-Day Execution Plan
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
---

# 90-Day Execution Plan

> Three-month operating plan to ship 3 starting offers, sign 5+ paying
> customers, and stand up 5 OS modules in production. Master plan in
> `/root/.claude/plans/mighty-plotting-moore.md`. Vertical playbooks in
> `docs/strategy/VERTICAL_PLAYBOOKS.md`.

## Day-90 success criteria (binary)

- ≥ **5 paying customers** (avg deal ≥ SAR 12K). Total cash ≥ SAR 60K.
- ≥ **2 retainers signed** (SAR 15K+ / mo each). MRR ≥ SAR 30K.
- ≥ **3 case studies** published with quantitative Proof Packs.
- **5 OS modules** in production: Data / Revenue / Governance / Reporting
  / Delivery (Phase 1 set).
- **Quality Score ≥ 80** on 100% of shipped projects.
- **Zero PDPL violations** (forbidden claims, cold WA/LinkedIn auto, etc.).

## Month 1 — Sellable Core (Weeks 1–4)

**Goal:** ship the 3 starting offers operationally. First paying
customers by end of Week 4.

**Engineering (CTO + 1 engineer):**
- **Data OS**: extend `auto_client_acquisition/customer_data_plane/`
  with `validation_rules.py`, `data_quality_score.py`, `pii_detection.py`.
- **Revenue OS**: wire `POST /api/v1/revenue-os/seed` + `GET /leads`;
  add `lead_scoring.py`, `icp_builder.py`.
- **Governance OS**: add `dealix/trust/pii_detector.py`,
  `forbidden_claims.py`, `approval_matrix.py`; hook into every action
  before `event_store.append_event`.
- **Reporting OS** (new dir `dealix/reporting/`):
  `executive_report.py`, `proof_pack.py`, `weekly_summary.py`.
- **Delivery OS**: `client_intake.py`, `scope_builder.py`,
  `delivery_checklist.py`, `qa_review.py` (5-gate, 100-point scoring).

**Commercial (CRO + designer):**
- 5-pillar service pages + 3 offer pages on landing site.
- Intake form (Typeform/Tally) → `delivery_os/client_intake.py` schema.
- Demo report (sample Revenue Intelligence Sprint deliverable).
- Demo CSV (anonymized Saudi-shaped data).
- Sample Company Brain demo (1 cached customer with citations).
- Sales deck (10 slides, AR+EN).

**Sales (Week 3–4):**
- Outbound: 200 targeted Saudi B2B accounts (B2B services / clinics /
  logistics) via Lead Engine seed → ranked-A.
- 30 demos booked → 10 qualified → **3 paying pilots signed** (one per
  starting offer).

**Hiring (Month 1):** Enterprise AE (BFSI focus), SDR (Riyadh,
bilingual), CS Lead.

**Month-1 gate:** 3 pilots signed; 5-gate QA system live; ≥ 2 of 3
pilots reach Stage 5 (Validate) with score ≥ 80.

## Month 2 — Expand to AI Ops (Weeks 5–8)

**Goal:** activate 2 more pillars (Serve Customers, Build Company
Brain) at scale; first 5 cumulative customers; first retainer signed.

**Engineering:**
- **Customer OS consolidation**: merge `support_os/` + `customer_inbox_v10/`
  → `customer_os/` with `inbox_model.py`, `message_classifier.py`,
  `suggested_replies.py`, `faq_builder.py`, `escalation_rules.py`.
  Suggested-reply only (no auto-send).
- **Knowledge OS depth**: extend `knowledge_v10/` with `chunking.py`,
  `freshness_policy.py`, `knowledge_eval.py`. Enforce "no source = no answer."
- **Operations OS**: `orchestrator/sop_builder.py`, `exception_handler.py`,
  `ops_dashboard.py`.
- **Frontend**: Strategy / Marketing / Delivery onboarding UIs.

**Commercial:**
- Activate 3 retainer offers (Monthly RevOps, Monthly AI Ops, Customer
  Support AI Retainer).
- Run AI Support Desk Sprint for 1 customer (Customer OS validation).
- Run Company Brain Sprint for 1 customer (Knowledge OS validation).
- Customer #4 and #5 signed.

**Hiring (Month 2):** Marketing manager (Saudi-native, bilingual).

**Month-2 gate:** 5 cumulative paying customers; 1 retainer signed;
≥ 80 Quality Score across all 5; first vertical playbook published.

## Month 3 — Retainer Machine (Weeks 9–12)

**Goal:** convert ≥ 40% of Month-1 and Month-2 sprint customers to
monthly retainers. Predictable MRR.

**Engineering:**
- **Strategy OS (new)**: `auto_client_acquisition/strategy_os/` with
  `ai_readiness.py`, `use_case_scoring.py`, `roi_estimator.py`,
  `risk_map.py`, `roadmap_builder.py`, `executive_report.py`. Sells
  as AI Readiness Assessment (7.5K–25K SAR).
- **Marketing OS (new)**: `auto_client_acquisition/marketing_os/` with
  `brand_voice.py`, `content_calendar.py`, `campaign_angles.py`,
  `landing_copy.py`, `email_sequence.py`, `offer_builder.py`.
- **Monthly dashboards**: per-customer health + outcome dashboards via
  Reporting OS.
- **CRM hygiene loop**: weekly automated cleanup for retainer customers.

**Commercial:**
- 2 retainers signed (SAR 15K–60K / mo each).
- 2 AI Readiness Assessments (top-of-funnel for Phase-4 enterprise).
- First Vertical Playbook published (BFSI).

**Hiring (Month 3):** AE #2 (Retail focus, Week 5 if Month-1 closed).

**Month-3 gate:** ≥ 2 retainers signed; MRR ≥ SAR 30K; 3 case studies
published; SAR 1.5M Q1 pipeline.

## Cross-cutting throughout 90 days

- **Operating cadence**: weekly CRO + HoCS review; bi-weekly CEO ops
  review; monthly board update.
- **PDPL discipline**: 100% outbound passes Approval Matrix; every
  outbound message has the Art. 13 footer.
- **Quality discipline**: every project follows the 8-stage Delivery
  Standard (Discover → Diagnose → Design → Build → Validate → Deliver →
  Prove → Expand) with the 5-gate QA at Validate.
- **Proof discipline**: every project ends with a Proof Pack within 14
  days; written to Proof Ledger.
- **Catalog discipline**: ≥ 80% productized revenue share by Month 12
  (gate begins to bind in Month 3).

## Anti-patterns (forbidden in 90 days)

- Bespoke quoting in conversation 1.
- Any cold WhatsApp; any LinkedIn automation; any scraping.
- "We will build it" custom-development promises in sales conversations.
- Discount > 12% without CRO sign-off; > 25% without CEO sign-off.
- Shipping a project at Quality Score < 80.

## Cross-links

- Master 90-day plan: `/root/.claude/plans/mighty-plotting-moore.md`
- 12-month roadmap: `docs/strategy/12_MONTH_ROADMAP.md`
- 12-month GTM: `docs/go-to-market/saudi_gtm_12m.md`
- Three starting offers: `docs/strategy/three_starting_offers.md`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
- Operating principles: `docs/company/OPERATING_PRINCIPLES.md`
- Vertical playbooks: `docs/strategy/VERTICAL_PLAYBOOKS.md`
- Go-to-market: `docs/strategy/GO_TO_MARKET.md`
- Existing 90-day execution: `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`
