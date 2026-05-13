---
title: Product Roadmap — Phase 1 / 2 / 3 / 4 (90-Day Plan)
doc_id: W6.T34.product-roadmap
owner: HoP
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T11, W6.T34, W6.T36]
kpi:
  metric: phase_on_time_completion
  target: 90
  window: per_phase
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 1
  score: roadmap
---

# Product Roadmap

## 1. Context

Dealix's product roadmap is sequenced by *revenue weight* not feature
ambition. Four phases mirror the 90-day execution plan: Foundation, Build,
Productize, Integrate. Each phase has a single dominant question to answer
before the next phase opens.

The canonical RICE methodology and quarterly capacity allocation live in
[`revenue_weighted_roadmap.md`](revenue_weighted_roadmap.md). This file is
the human-readable phase plan.

## 2. Audience

HoP (owner), CTO, CEO, engineering managers, AEs (consume phase scope when
forecasting deal-eligible features), CSMs (consume phase deliveries when
forecasting renewal-eligible features).

## 3. The Four Phases

### 3.1 Phase 1 — Foundation (Weeks 1–6)

**Question to answer**: can we deliver the 3 starting offers consistently?

- Service Catalog: 3 starting offers fully scoped, priced, demo-runnable.
- Delivery OS: intake, scope, checklist, QA, handoff, renewal — all 8
  stages wired end-to-end.
- Trust OS gap-fills: PII detector, forbidden claims, approval matrix.
- Reporting OS: executive artifact generator with KPI block + audit links.
- Three runnable demos in `demos/`.

**Exit criterion**: 3 paying customers across the 3 offers, QA pass.

### 3.2 Phase 2 — Build (Weeks 7–12)

**Question to answer**: which OS modules carry the most revenue weight?

- Saudi Lead Engine — flagship Grow Revenue offering.
- Data Quality OS hardening: validation rules, dedupe, quality score.
- Scoring OS: feature-based scoring, explainability.
- Workflow OS productization: durable workflows + approvals + audit.
- Knowledge OS (RAG) spike → production.
- A/B framework + AI eval framework operational.

**Exit criterion**: ≥ 5 paying customers, ≥ 1 retainer, repeatable delivery.

### 3.3 Phase 3 — Productize (Weeks 13–24)

**Question to answer**: can Dealix itself help deliver the service?

- Customer portal: intake → scope → checklist → QA evidence → handoff.
- Internal CS console: stage machine UI, QA evaluator UI, approval queue.
- Proof Ledger automation: outcome capture, before/after deltas, exports.
- Maturity Level 3 (Platform-Assisted Delivery) achieved per
  [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md).

**Exit criterion**: Sprint → Retainer conversion ≥ 40%; NRR ≥ 120%.

### 3.4 Phase 4 — Integrate (Weeks 25–52)

**Question to answer**: which integrations unlock enterprise revenue?

- CRM adapters: HubSpot, Salesforce.
- Inbox adapters: Google Workspace, Microsoft 365.
- Billing adapters: Moyasar (KSA), Stripe (GCC partner geographies).
- Multi-tenant RBAC, SLA, governance dashboard, audit exports.
- Enterprise onboarding playbook.

**Exit criterion**: Maturity Level 5 (Enterprise AI OS) achieved; first
enterprise contract signed.

## 4. Phase Ordering Rules

- A phase opens only when the prior phase's exit criterion is met.
- Engineering capacity allocated per the RICE rubric in
  [`revenue_weighted_roadmap.md`](revenue_weighted_roadmap.md).
- New features require RW-RICE > 50 to enter a phase mid-flight.

## 5. Cross-links

- RICE methodology: [`revenue_weighted_roadmap.md`](revenue_weighted_roadmap.md)
- Master plan: [`../strategy/SAUDI_30_TASKS_MASTER_PLAN.md`](../strategy/SAUDI_30_TASKS_MASTER_PLAN.md)
- Maturity model: [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
- Module map: [`MODULE_MAP.md`](MODULE_MAP.md)
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Integration strategy: [`INTEGRATION_STRATEGY.md`](INTEGRATION_STRATEGY.md)
- Existing roadmap pointer: `docs/PRODUCT_ROADMAP.md` (legacy)

## 6. Owner & Review Cadence

- **Owner**: HoP.
- **Review**: quarterly planning + monthly mid-cycle check.

## 7. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoP | Initial 4-phase plan (Foundation / Build / Productize / Integrate) |
