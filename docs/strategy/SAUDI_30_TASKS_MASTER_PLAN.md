---
title: Saudi GTM 30-Task Master Plan
doc_id: W0.T00.master-plan
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W1.T01, W1.T05, W1.T11, W1.T17, W1.T31, W2.T02, W2.T03, W2.T04, W2.T08, W2.T09, W2.T16, W2.T28, W3.T06, W3.T07, W3.T15, W3.T20, W3.T27, W4.T12, W4.T13, W4.T14, W4.T21, W4.T22, W4.T23, W4.T24, W4.T25, W4.T26, W5.T10, W5.T18, W5.T19, W5.T29, W5.T30]
kpi:
  metric: documented_saudi_capabilities_index
  target: 31
  window: 90d
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 6
  score: meta
---

# Saudi GTM 30-Task Master Plan

## 1. Context

Dealix has the core platform of a sovereign Saudi B2B Revenue OS — Revenue OS, Decision Passport, Event Store, Orchestrator, Policy Engine — but lacks the Saudi-specific GTM, trust, and engineering rigor documentation needed to win and serve Saudi enterprise customers credibly. This master plan governs a single-batch documentation initiative on branch `claude/saudi-gtm-strategy-9yrRX` that delivers **31 documents** (30 original tasks + 1 elevated Saudi Lead Engine spec) across six commit-coherent waves. The plan also explicitly elevates **T31 — Saudi Lead Engine** because the core user requirement is a system that can generate real, targeted Saudi leads automatically from seed inputs — not merely strategy docs.

## 2. Audience

- **CEO**: prioritization, owner assignment, board narrative.
- **CRO / Head of Sales**: GTM, pricing, ICP, sales/enablement consumption.
- **CTO / Head of Engineering**: ADRs, SRE, FinOps, data quality, policy engine.
- **Head of Product**: roadmap, launch, lead engine spec.
- **Head of CS / Delivery**: pilot, CS framework, expansion.
- **Head of Legal / Trust**: trust pack, procurement, legal risk register.

## 3. Decisions / Content

### 3.1 RICE rubric (binding)

- **Reach** = expected Saudi accounts directly touched in 90 days (integer).
- **Impact** ∈ {0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive}.
- **Confidence** ∈ [0.5, 0.7, 0.9, 1.0] — evidence tier (L0–L5 mapped).
- **Effort** = person-weeks to complete and operationalize (not just write the doc).
- **Score** = (Reach × Impact × Confidence) / Effort. Higher = earlier priority.

### 3.2 RICE table for all 31 tasks

| ID | Task | Owner | Reach | Impact | Conf | Effort | Score |
|----|------|-------|-------|--------|------|--------|-------|
| T31 | **Saudi Lead Engine spec** | CTO | 500 | 3 | 0.9 | 3 | **450** |
| T5 | Saudi ICP | CRO | 300 | 3 | 0.9 | 1 | **810** |
| T1 | Vertical positioning (3 verticals) | CRO | 300 | 2 | 0.9 | 2 | **270** |
| T7 | Trust pack (4 docs) | HoLegal | 200 | 3 | 0.9 | 3 | **180** |
| T3 | Saudi pricing packages | CRO | 250 | 2 | 0.9 | 1 | **450** |
| T9 | AR sales playbook | CRO | 150 | 2 | 0.9 | 1 | **270** |
| T15 | Procurement pack | HoLegal | 80 | 3 | 0.9 | 2 | **108** |
| T6 | Partner program SA | CRO | 50 | 3 | 0.8 | 2 | **60** |
| T2 | ROI model + deck | CRO | 200 | 2 | 0.8 | 1 | **320** |
| T8 | Persona-value matrix | CRO | 200 | 1 | 0.9 | 1 | **180** |
| T17 | Competitive landscape SA | CEO | 100 | 2 | 0.7 | 1 | **140** |
| T16 | Value metrics pricing | CRO | 150 | 2 | 0.7 | 1 | **210** |
| T4 | GTM 12m | CEO | 200 | 2 | 0.7 | 2 | **140** |
| T11 | Revenue-weighted roadmap | HoP | 0 (internal) | 3 | 0.8 | 2 | **120** |
| T28 | Sales enablement | CRO | 20 (reps) | 2 | 0.9 | 1 | **36** |
| T20 | Bilingual assets index | HoP | 0 | 1 | 1.0 | 0.5 | **operational** |
| T14 | Revenue OS policy rules | CTO | 0 | 3 | 0.9 | 2 | **engineering** |
| T21 | ADR set (6 ADRs) | CTO | 0 | 3 | 0.9 | 3 | **engineering** |
| T22 | Event store async migration | CTO | 0 | 2 | 0.8 | 2 | **engineering** |
| T23 | SLO framework | CTO | 0 | 3 | 0.9 | 2 | **engineering** |
| T24 | FinOps / model cost | CTO | 0 | 3 | 0.9 | 1 | **engineering** |
| T25 | Data quality gates | HoData | 0 | 3 | 0.9 | 1 | **engineering** |
| T26 | A/B framework | HoP | 0 | 2 | 0.8 | 1 | **engineering** |
| T12 | Event taxonomy | HoData | 0 | 2 | 0.9 | 1 | **engineering** |
| T13 | Executive KPI spec | CEO | 0 | 3 | 0.9 | 1 | **engineering** |
| T27 | Legal risk register | HoLegal | 0 | 3 | 0.9 | 1 | **legal** |
| T10 | CS framework | HoCS | 50 | 2 | 0.8 | 1 | **80** |
| T18 | Pilot framework | HoCS | 30 | 3 | 0.8 | 1 | **72** |
| T19 | Expansion playbook | HoCS | 30 | 2 | 0.8 | 1 | **48** |
| T29 | Launch checklist | HoP | 50 | 2 | 0.9 | 1 | **90** |
| T30 | Executive operating cadence | CEO | 0 | 3 | 0.9 | 1 | **operating** |

**Top 5 by RICE (customer-facing impact):** T5 (810), T3 (450), T31 (450), T2 (320), T1 (270).

### 3.3 90-day schedule (W1–W13)

| Week | Wave | Deliverables |
|------|------|--------------|
| W1 | W0 | Master plan + template (this commit) |
| W2 | W1 | T5 ICP, T1 verticals, T17 competitive landscape, T11 roadmap, **T31 Saudi Lead Engine** |
| W3–W4 | W2 | T4 GTM 12m, T2 ROI, T3 pricing packages, T16 value metrics, T8 persona matrix, T9 AR sales playbook, T28 enablement |
| W5–W6 | W3 | T6 partner program, T7 trust pack (×4), T15 procurement, T20 bilingual index, T27 legal risk register |
| W7–W9 | W4 | T21 ADRs (×6), T22 event store migration, T23 SLO, T24 FinOps, T25 data quality, T26 A/B, T14 policy rules, T12 event taxonomy, T13 KPI spec |
| W10–W11 | W5 | T10 CS framework, T18 pilot framework, T19 expansion, T29 launch checklist, T30 ops cadence |
| W12 | Verify | Cross-link audit, AR translation review, lint, push |
| W13 | Buffer | Reviewer feedback cycle |

### 3.4 KPI per task (90-day targets)

| ID | KPI metric | Target | Window |
|----|-----------|--------|--------|
| T31 | Saudi leads generated from seed→enriched→ranked | 5,000 enriched, 1,000 ranked-A | 90d |
| T5 | ICP-qualified accounts in CRM | 200 | 60d |
| T1 | Vertical-tagged opportunities | 30 (10 per vertical) | 90d |
| T7 | Trust pack downloads by enterprise prospects | 50 | 90d |
| T3 | Pricing-page-to-pricing-call conversion | 8% | 60d |
| T9 | AR playbook adoption by reps | 100% (6/6 reps) | 30d |
| T15 | RFP response cycle time | < 5 business days | 90d |
| T6 | Active partner signups | 8 | 90d |
| T2 | ROI calc completions per deal | 1.0 attach rate | 60d |
| T8 | Persona-tagged emails sent | 1,000 | 60d |
| T17 | Win-rate vs identified competitors | tracked baseline | 90d |
| T16 | Expansion revenue from value metrics | +15% NRR | 180d |
| T4 | Pipeline coverage ratio | 3.0× quota | quarterly |
| T11 | Revenue-tagged roadmap items shipped | 80% of top-quartile | quarterly |
| T28 | Rep ramp time to first SQL | < 30 days | 90d |
| T14 | Policy-violation actions blocked | 100% (zero leakage) | continuous |
| T21 | ADRs reviewed in engineering forum | 6/6 | 60d |
| T22 | Async event publish p95 latency | < 50 ms | continuous |
| T23 | Availability SLO attainment | 99.5% Starter / 99.9% Enterprise | monthly |
| T24 | LLM cost per workflow | < 30% of revenue per workflow | monthly |
| T25 | Data quality gate pass rate | 98% | continuous |
| T26 | Experiments shipped per quarter | 4 | quarterly |
| T12 | Event taxonomy coverage | 100% of core flows | 60d |
| T13 | Exec dashboard freshness | < 24h | continuous |
| T27 | Open enterprise legal risks (high) | 0 | continuous |
| T10 | Customer health score coverage | 100% of paying accounts | 60d |
| T18 | Pilot → paid conversion | 60% | 180d |
| T19 | Net Revenue Retention | ≥ 115% | annual |
| T29 | Launch readiness gates passed | 100% before GA | per launch |
| T30 | Exec cadence attendance | 90% | monthly |
| T20 | Bilingual freshness (AR within 14 days of EN) | 100% | continuous |

### 3.5 Owner role definitions

- **CEO**: strategic narrative, board, exec cadence.
- **CRO**: revenue org, sales, partner program, pricing, ICP, enablement.
- **CTO**: engineering, ADRs, SRE, FinOps, policy engine, lead engine architecture.
- **HoP** (Head of Product): roadmap, launch, lead engine product spec, A/B.
- **HoCS** (Head of Customer Success): pilot, CS framework, expansion.
- **HoLegal**: trust, procurement, legal risk, compliance.
- **HoData** (Head of Data): event taxonomy, data quality, lead engine data sources.

### 3.6 Dependency graph

```
T0 (master plan) ──► everything

T5 (ICP) ──┬─► T1 (verticals)
           ├─► T8 (persona matrix)
           ├─► T4 (GTM 12m)
           └─► T31 (lead engine — targeting layer)

T31 (lead engine) ──┬─► T25 (data quality gates)
                    ├─► T12 (event taxonomy)
                    ├─► T14 (policy rules — gates outbound actions)
                    └─► T7 (trust — explains data sourcing to customers)

T7 (trust pack) ──┬─► T15 (procurement)
                  ├─► T27 (legal risk)
                  └─► T29 (launch checklist)

T3 (pricing) ──┬─► T16 (value metrics)
               ├─► T2 (ROI)
               └─► T6 (partner program)

T21 (ADRs) ──┬─► T22 (event store)
             ├─► T23 (SLO)
             └─► T14 (policy)

T29 (launch) consumes: T7, T4, T28, T23, T27, T30
```

### 3.7 Saudi Lead Engine (T31) — why elevated

User mandate: the system must generate **real, targeted Saudi lead data** from seed inputs without manual work. Existing implementation hooks:

- `auto_client_acquisition/revenue_os/source_registry.py` — registry of data sources (must add Saudi sources: MoC CR, ZATCA, Maroof, Monsha'at, sectoral chambers, Bayut/Aqar B2B, LinkedIn Sales Navigator, news/tender portals).
- `auto_client_acquisition/revenue_os/enrichment_waterfall.py` — multi-source enrichment with fallback.
- `auto_client_acquisition/revenue_os/signal_normalizer.py` — converts raw signals to `MarketSignal → Why Now → Offer`.
- `auto_client_acquisition/revenue_os/dedupe.py` — entity resolution across sources.
- `auto_client_acquisition/revenue_memory/event_store.py` — append-only audit of every enrichment/scoring decision.
- `api/routers/decision_passport.py` — gates outbound action on every lead with evidence L0–L5.

T31 spec must enumerate: (a) every Saudi data source with legal basis (PDPL Art. 5), (b) the seed→ranked pipeline contract, (c) the public/CLI/API surface, (d) success metrics (5K enriched + 1K ranked-A in 90d).

## 4. KPIs

Master KPI: **31/31 documents drafted and cross-linked, AR companions for 9 logical sets, 6 commits landed on branch, zero broken cross-links, branch pushed** within session.

## 5. Dependencies

- Existing repo docs (referenced, not rewritten): `GTM_PLAYBOOK.md`, `PRICING_*`, `SALES_PLAYBOOK.md`, `CUSTOMER_SUCCESS_PLAYBOOK.md`, `TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`, `POSITIONING_AND_ICP.md`, `STRATEGIC_MASTER_PLAN_2026.md`, `BUSINESS_MODEL.md`, etc.
- Code anchors: `auto_client_acquisition/revenue_os/`, `auto_client_acquisition/revenue_memory/`, `auto_client_acquisition/orchestrator/runtime.py`, `dealix/trust/policy.py`, `api/routers/decision_passport.py`, `api/v1/revenue-os/*`.
- Template: `docs/_templates/SAUDI_DOC_TEMPLATE.md`.

## 6. Cross-links

- Template: `docs/_templates/SAUDI_DOC_TEMPLATE.md`
- All 31 task docs by `doc_id` (see frontmatter `related`).

## 7. Owner & Review Cadence

- **Owner**: CEO. Each task owner accountable for their deliverable.
- **Review**: weekly during 90-day window; monthly thereafter as part of T30 executive operating cadence.
- **Escalation**: any task >1 week off-schedule escalates to CEO in weekly review.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CEO | Initial master plan, RICE, schedule, KPIs |
| 2026-05-13 | CEO | Elevated T31 Saudi Lead Engine to top priority alongside T5 ICP |
| 2026-05-13 | CEO | Added Wave 6 (AI Operating Partner repositioning): T32 positioning, T33 portfolio catalog, T34 9-module OS architecture (added Delivery OS), T35 three starting offers, T36 Delivery Standard & Quality System. T31 demoted from "company" to "flagship inside Grow Revenue." |

## 9. Wave 6 — AI Operating Partner Strategy (Added 2026-05-13)

Dealix repositioned from "Revenue OS / Lead Engine company" to **AI Operating Partner for Saudi companies** with:

- **5 customer-facing pillars**: Grow Revenue / Serve Customers / Automate Operations / Build Company Brain / Govern AI.
- **9 internal OS modules** (Intake / Data Quality / Scoring / Workflow / Knowledge / Outreach / Reporting / Governance / Delivery).
- **30+ productized service offerings** across 8 service domains.
- **7 productized packages** spanning Quick Win (7.5K SAR) → Enterprise (85K+ SAR setup).
- **3 starting offers** for first-90-day market entry: Revenue Intelligence Sprint (9.5K), AI Quick Win Sprint (12K), Company Brain Sprint (20K).
- **8-stage Delivery Standard** (Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand).
- **5-gate Quality System** (Business / Data / AI / Compliance / Delivery QA).
- **Project Quality Score 0–100** with 80 floor for handoff.
- **5 operationalized competitive advantages**: Outcome-first, Saudi-localized, Proof-backed, Governed AI, Productized delivery.

| Wave 6 doc | Path |
|-----------|------|
| Positioning (T32) | `docs/strategy/dealix_operating_partner_positioning.md` (+ AR) |
| Portfolio catalog (T33) | `docs/strategy/service_portfolio_catalog.md` (+ AR) |
| OS modules (T34) | `docs/product/internal_os_modules.md` |
| Three starting offers (T35) | `docs/strategy/three_starting_offers.md` (+ AR) |
| Delivery Standard & QA (T36) | `docs/strategy/dealix_delivery_standard_and_quality_system.md` (+ AR) |
