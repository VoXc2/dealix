---
title: Saudi Lead Engine — Capabilities, Data Sources, Pipeline
doc_id: W1.T31.lead-engine
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal, customer, partner]
language: en
ar_companion: docs/product/saudi_lead_engine.ar.md
related: [W0.T00, W1.T05, W1.T01, W4.T14, W4.T25, W4.T12, W3.T07]
kpi:
  metric: enriched_leads_per_90d
  target: 5000
  window: 90d
rice:
  reach: 500
  impact: 3
  confidence: 0.9
  effort: 3
  score: 450
---

# Saudi Lead Engine — Capabilities, Data Sources, Pipeline

## 1. Context

Dealix's promise to Saudi enterprises is: "give us a seed (a vertical, a geography, a buying trigger, or a known account) and we return enriched, deduplicated, scored, decision-passport-gated leads ready for sales action — with full audit trail and PDPL compliance." This document is the canonical product/engineering spec for that engine. It is the **operational heart** of Dealix's Saudi GTM and the doc every customer trust review, every demo, every RFP response, and every engineering ADR refers back to.

The engine is not vapor: its plumbing already exists at `auto_client_acquisition/revenue_os/` (Source Registry, Enrichment Waterfall, Signal Normalizer, Dedupe, Proof Canonical, Action Catalog) and `auto_client_acquisition/revenue_memory/event_store.py`. This doc closes the gap between the existing plumbing and a productized **Saudi Lead Engine** — by enumerating Saudi-specific data sources, the seed-to-ranked-lead contract, the policy gates, and the KPIs.

## 2. Audience

- **Customer**: understands what data sources Dealix uses, what's lawful under PDPL, what arrives in their CRM, on what cadence, with what confidence.
- **Partner / SI / reseller**: knows the engine's input surfaces and output guarantees to scope integrations.
- **Engineering**: maps each pipeline stage to a code module and an SLO.
- **Legal / Trust**: maps every data source to legal basis (PDPL Art. 5/13/14/18/21) and retention rules.

## 3. Decisions / Content

### 3.1 Capabilities (what the engine does)

1. **Seed-based targeting** — accept seed inputs of 5 types: (a) vertical+region, (b) buying-trigger event, (c) known-account expansion, (d) lookalike-of-customer, (e) RFP/tender keywords.
2. **Multi-source enrichment** — waterfall across ≥10 Saudi-specific data sources with deterministic fallback.
3. **Entity resolution** — collapse duplicates across CR number, VAT number, domain, English/Arabic name variants.
4. **Signal normalization** — convert raw events into `MarketSignal → Why Now → Offer → Proof Target`.
5. **Scoring & ranking** — A/B/C/D bands with explainable feature weights.
6. **Decision Passport gating** — no outbound action without an L1+ evidence passport stamped to `api/routers/decision_passport.py`.
7. **Audit & replay** — every step appended to event store at `auto_client_acquisition/revenue_memory/event_store.py` for full re-derivation.
8. **PDPL compliance** — retention windows, consent capture surfaces, right-to-erasure handling baked in.
9. **Bilingual output** — Arabic + English names, addresses, role titles normalized.
10. **Continuous learning** — outcome events feed back into source weighting (no manual rule tuning required).

### 3.2 Data sources — Saudi-specific registry

The engine must register each source in `auto_client_acquisition/revenue_os/source_registry.py` with: name, kind, freshness, legal basis, cost model, rate limits, parser.

#### A. Public / official (legal basis: PDPL Art. 5 — lawful & publicly available)

| Source | Kind | Freshness | What it provides |
|--------|------|-----------|------------------|
| Ministry of Commerce — CR (Commercial Registry) lookup | Web API / scrape | Daily | CR number, legal name (AR/EN), capital, activity codes, status |
| ZATCA — VAT registry | Web | Weekly | VAT registration, tax status (for B2B eligibility) |
| Maroof — Saudi business directory | Web | Weekly | Verified merchant profiles, ratings, service tags |
| Monsha'at — SME registry | Web | Monthly | SME tier (micro/small/medium), accelerator/incubator membership |
| Etimad — government procurement / tenders | API/web | Daily | RFP triggers (≥SAR 100k contracts surface as buying triggers) |
| MCI sectoral CR statistics | Web | Quarterly | Sector growth signals at macro level |
| Saudi Patent and Trademark Office | Web | Monthly | Innovation signals; trademark filings (expansion signal) |

#### B. Sectoral chambers & associations

| Source | Kind | What it provides |
|--------|------|------------------|
| Riyadh Chamber of Commerce member directory | Web | Member roster, sub-sector tags |
| Jeddah Chamber of Commerce member directory | Web | Member roster |
| Eastern Province Chamber | Web | Member roster |
| SAMA member banks list | Web | BFSI ICP universe |
| CMA-licensed entities | Web | Capital markets ICP universe |
| CITC-licensed entities | Web | ICT ICP universe |
| SFDA-licensed entities | Web | Healthcare/pharma ICP universe |

#### C. Professional networks (legal basis: legitimate interest + public profile data, with PDPL Art. 13/14 notice and opt-out)

| Source | Kind | What it provides |
|--------|------|------------------|
| LinkedIn Sales Navigator | API (via authorized seat) | Decision-maker discovery: titles, tenure, recent role changes |
| LinkedIn public job postings | Scrape | Hiring-velocity buying triggers (e.g., "Head of AI" posted = adoption signal) |

#### D. Real estate & operations (B2B context for retail, logistics, hospitality)

| Source | Kind | What it provides |
|--------|------|------------------|
| Aqar / Bayut (B2B listings only) | Scrape | New retail/warehouse openings as expansion signals |
| Google Maps Places API | API | Outlet counts (retail chain footprint) |

#### E. News & social triggers

| Source | Kind | What it provides |
|--------|------|------------------|
| Argaam, Mubasher (financial news AR) | RSS/API | Earnings, expansion, M&A signals |
| Wamda, MAGNiTT | API/scrape | Funding rounds, startup ecosystem |
| Twitter/X Saudi business accounts | API | Real-time executive announcements |
| Saudi Press Agency (SPA) | RSS | Govt contract awards, policy shifts |

#### F. Tendering & contract signals (highest buying-intent)

| Source | Kind | What it provides |
|--------|------|------------------|
| Etimad tender portal | API/scrape | Live tenders matching ICP keywords |
| Sectoral procurement portals (Aramco, STC, etc., where public) | Web | Vendor pre-qualifications |

#### G. Customer-provided seed (legal basis: PDPL Art. 5 contract)

- CRM exports, customer's own first-party data.
- Account lookalike seed list.

**Total registered sources (target):** ≥25 by end of Wave 1; ≥40 by end of Q1 post-launch.

### 3.3 Pipeline contract (seed → ranked lead)

```
                    +-----------------------+
SEED (5 types) ───► |  1. SEED NORMALIZER   |  validate, classify seed type
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  2. SOURCE FANOUT     |  pick subset of source registry
                    +-----------+-----------+    based on seed type
                                │
                    +-----------▼-----------+
                    |  3. ENRICHMENT        |  waterfall: primary→fallback per field
                    |     WATERFALL         |  parallel where allowed by rate limits
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  4. DEDUPE / ENTITY   |  CR# > VAT# > domain > fuzzy name
                    |     RESOLUTION        |  Arabic transliteration normalization
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  5. SIGNAL            |  MarketSignal → Why Now → Offer
                    |     NORMALIZER        |  evidence level L0–L5 stamped
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  6. SCORING           |  feature-weighted A/B/C/D bands
                    |                       |  explainability per feature
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  7. POLICY GATE       |  dealix/trust/policy.py
                    |                       |  Decision Passport stamped or rejected
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  8. ACTION CATALOG    |  routes ranked-A leads to email/call/
                    |                       |  CRM push/Slack alert per playbook
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    |  9. EVENT STORE       |  append every step for audit/replay
                    +-----------+-----------+
                                │
                    +-----------▼-----------+
                    | 10. OUTCOME FEEDBACK  |  win/loss → source-weight learner
                    +-----------------------+
```

**Throughput target:** 5,000 enriched leads / 90d / tenant on Growth tier; 50,000 / 90d / tenant on Enterprise.
**Latency target:** seed → first ranked lead < 60 seconds (cached sources) / < 10 minutes (cold).

### 3.4 API & CLI surface

- **REST**: `POST /api/v1/revenue-os/seed` (accept seed, return job-id) · `GET /api/v1/revenue-os/leads?job_id=...&min_score=A` · `POST /api/v1/revenue-os/leads/{id}/feedback`.
- **Webhook**: outbound `lead.ranked` event with full decision passport.
- **CLI**: `dealix lead generate --vertical bfsi --region riyadh --trigger funding --limit 500`.
- **UI**: dashboard "Lead Engine" workspace with seed builder, live progress, score bands, drill-down to evidence.

### 3.5 Quality, policy, and PDPL gates

- **Data quality gates (T25)**: source freshness, completeness ≥95%, duplicate rate <2%, contact field accuracy ≥90% (sampled).
- **Policy gates (T14)**: PDPL Art. 13 (notice) and Art. 14 (consent for direct marketing) enforced before any outbound action — leads can be generated without consent for internal scoring but **not actioned** outbound until consent or legitimate-interest justification is recorded.
- **Right to erasure**: any lead can be deleted across all caches and the event store via `DELETE /api/v1/revenue-os/leads/{id}` (cryptographic erasure for immutable events: per-lead key destroyed).

### 3.6 Why this beats CRM + manual lists

- **Saudi-native sources**: no US tool wires up MoC CR, ZATCA, Maroof, Etimad out of the box.
- **Arabic entity resolution**: deduplicates "شركة الاتصالات السعودية" with "Saudi Telecom Company" with "STC".
- **Audit-grade**: every lead carries a Decision Passport — defensible to procurement and regulators.
- **No manual scraping by the customer**: they provide seed; engine handles the rest.

## 4. KPIs

| Metric | Target | Window |
|--------|--------|--------|
| Enriched leads delivered | 5,000 / tenant | 90d |
| Ranked-A leads delivered | 1,000 / tenant | 90d |
| Seed → first ranked-A lead latency | < 60s warm / < 10m cold | continuous |
| Source registry size | ≥ 25 sources | end of Wave 1 |
| Decision Passport coverage | 100% of outbound actions | continuous |
| PDPL right-to-erasure SLA | < 72 hours | continuous |
| Pilot → paid conversion (driven by engine) | 60% | 180d |

## 5. Dependencies

- Code: `auto_client_acquisition/revenue_os/source_registry.py`, `enrichment_waterfall.py`, `signal_normalizer.py`, `dedupe.py`, `proof_canonical.py`, `action_catalog.py`; `auto_client_acquisition/revenue_memory/event_store.py`; `api/routers/decision_passport.py`; `dealix/trust/policy.py`.
- Docs: W1.T05 (ICP) defines targeting taxonomy; W1.T01 (verticals) defines vertical-specific seed types; W4.T14 (policy rules) gates outbound; W4.T25 (data quality) gates ingest; W4.T12 (event taxonomy) governs telemetry; W3.T07 (trust pack) explains to customers.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Verticals: `docs/go-to-market/saudi_vertical_positioning.md`
- Policy: `docs/policy/revenue_os_policy_rules.md`
- Data quality: `docs/data/data_quality_gates.md`
- Trust — data governance: `docs/trust/data_governance.md`

## 7. Owner & Review Cadence

- **Owner**: CTO (with HoP for product surfacing, HoData for sources, HoLegal for PDPL).
- **Review**: weekly during build (60 days); monthly thereafter.
- **Escalation**: any source legal basis change → HoLegal within 24h; any pipeline SLO breach → CTO within 1h.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial spec; 25-source registry; pipeline contract; PDPL gates |
