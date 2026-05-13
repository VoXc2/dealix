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
> customers, and stand up 5 OS modules. Master plan in
> `/root/.claude/plans/mighty-plotting-moore.md`. Vertical playbooks in
> `docs/strategy/VERTICAL_PLAYBOOKS.md`.

## Day-90 success criteria (binary)

- ≥ **5 paying customers** (avg deal ≥ SAR 12K) — total cash ≥ SAR 60K.
- ≥ **2 retainers** (SAR 15K+ / mo each) — MRR ≥ SAR 30K.
- ≥ **3 case studies** with quantitative Proof Packs.
- **5 OS modules** in production: Data / Revenue / Governance /
  Reporting / Delivery.
- **Quality Score ≥ 80** on 100% of shipped projects.
- **Zero PDPL violations**.

## Month 1 — Sellable Core (W1–W4)

**Goal:** ship 3 starting offers operationally; first paying customers
by end of W4.

**Engineering (CTO + 1 engineer):**
- **Data OS**: `validation_rules.py`, `data_quality_score.py`,
  `pii_detection.py`.
- **Revenue OS**: wire `POST /api/v1/revenue-os/seed` + `GET /leads`;
  add `lead_scoring.py`, `icp_builder.py`.
- **Governance OS**: `pii_detector.py`, `forbidden_claims.py`,
  `approval_matrix.py`; hook into every action.
- **Reporting OS** (new dir `dealix/reporting/`): `executive_report.py`,
  `proof_pack.py`, `weekly_summary.py`.
- **Delivery OS**: `client_intake.py`, `scope_builder.py`,
  `delivery_checklist.py`, `qa_review.py` (5-gate, 100-point scoring).

**Commercial:**
- 5-pillar service pages + 3 offer pages on landing site.
- Intake form → `delivery_os/client_intake.py` schema.
- Demo report, demo CSV, Company Brain demo, sales deck (AR+EN).

**Sales (W3–4):** 200 outbound accounts → 30 demos → 10 qualified →
**3 paying pilots signed** (one per starting offer).

**Hiring:** Enterprise AE (BFSI), SDR (Riyadh, bilingual), CS Lead.

**Gate:** 3 pilots signed; 5-gate QA live; ≥ 2 of 3 reach Stage 5 ≥ 80.

## Month 2 — Expand to AI Ops (W5–W8)

**Goal:** activate Serve Customers and Build Company Brain pillars;
first 5 cumulative customers; first retainer signed.

**Engineering:**
- **Customer OS consolidation**: merge `support_os/` + `customer_inbox_v10/`
  → `customer_os/` with `inbox_model`, `message_classifier`,
  `suggested_replies`, `faq_builder`, `escalation_rules`. Suggested-
  reply only (no auto-send).
- **Knowledge OS depth**: `chunking.py`, `freshness_policy.py`,
  `knowledge_eval.py`. Enforce "no source = no answer."
- **Operations OS**: `sop_builder.py`, `exception_handler.py`,
  `ops_dashboard.py`.
- **Frontend**: Strategy / Marketing / Delivery onboarding UIs.

**Commercial:**
- Activate Monthly RevOps, Monthly AI Ops, Customer Support AI
  retainers.
- 1 AI Support Desk Sprint (Customer OS validation).
- 1 Company Brain Sprint (Knowledge OS validation).
- Customer #4 and #5 signed.

**Hiring:** Marketing manager (Saudi-native, bilingual).

**Gate:** 5 cumulative paying customers; 1 retainer signed; ≥ 80
Quality across all 5; first vertical playbook published.

## Month 3 — Retainer Machine (W9–W12)

**Goal:** ≥ 40% of sprint customers to retainers; predictable MRR.

**Engineering:**
- **Strategy OS (new)**: `ai_readiness.py`, `use_case_scoring.py`,
  `roi_estimator.py`, `risk_map.py`, `roadmap_builder.py`,
  `executive_report.py`. Sells as AI Readiness (7.5K–25K SAR).
- **Marketing OS (new)**: `brand_voice.py`, `content_calendar.py`,
  `campaign_angles.py`, `landing_copy.py`, `email_sequence.py`,
  `offer_builder.py`.
- **Monthly dashboards**: per-customer health + outcome.
- **CRM hygiene loop**: weekly auto cleanup for retainers.

**Commercial:**
- 2 retainers signed (SAR 15K–60K / mo).
- 2 AI Readiness Assessments (Phase-4 funnel).
- First Vertical Playbook published (BFSI).

**Hiring:** AE #2 (Retail focus, W5+ if M1 closed).

**Gate:** ≥ 2 retainers; MRR ≥ SAR 30K; 3 case studies; SAR 1.5M Q1
pipeline.

## Cross-cutting

- **Cadence**: weekly CRO + HoCS; bi-weekly CEO ops; monthly board.
- **PDPL**: 100% outbound passes Approval Matrix; Art. 13 footer on
  every message.
- **Quality**: 8-stage Delivery Standard (Discover → Diagnose → Design
  → Build → Validate → Deliver → Prove → Expand) with 5-gate QA at
  Validate.
- **Proof**: every project ends with a Proof Pack within 14 days.
- **Catalog**: ≥ 80% productized revenue share by M12.

## Forbidden in 90 days

- Bespoke quoting in conversation 1.
- Cold WhatsApp; LinkedIn automation; scraping.
- "We will build it" custom-development promises.
- Discount > 12% without CRO; > 25% without CEO.
- Shipping at Quality Score < 80.

## Cross-links

- Master plan: `/root/.claude/plans/mighty-plotting-moore.md`
- 12-month roadmap: `docs/strategy/12_MONTH_ROADMAP.md`
- 12-month GTM: `docs/go-to-market/saudi_gtm_12m.md`
- Three starting offers: `docs/strategy/three_starting_offers.md`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
- Operating principles: `docs/company/OPERATING_PRINCIPLES.md`
- Vertical playbooks: `docs/strategy/VERTICAL_PLAYBOOKS.md`
- Go-to-market: `docs/strategy/GO_TO_MARKET.md`
- Existing: `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`
