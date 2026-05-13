---
title: Saudi Competitive Landscape and Win/Loss Framework
doc_id: W1.T17.competitive
owner: CEO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T05, W1.T01, W2.T08, W2.T04]
kpi:
  metric: win_rate_vs_named_competitors
  target: tracked_baseline
  window: 90d
rice:
  reach: 100
  impact: 2
  confidence: 0.7
  effort: 1
  score: 140
---

# Saudi Competitive Landscape and Win/Loss Framework

## 1. Context

Saudi enterprise buyers compare Dealix against three competitor classes: (a) US-translated SaaS tools (Salesforce + Outreach + Apollo stack), (b) local incumbents (homegrown CRMs and consulting-driven sales-ops shops), (c) status quo (manual + spreadsheets + agency outreach). Without a maintained landscape and Win/Loss discipline, sales loses the framing battle. This doc defines the four named competitors to track, our counter-positioning, and the Win/Loss capture protocol.

## 2. Audience

CEO, CRO, Product. Sales reps consume the counter-positioning section in T8 (persona matrix).

## 3. Decisions / Content

### 3.1 Four named competitors

**Comp 1 — US-translated stack (Salesforce + Outreach + Apollo + ZoomInfo).**
- **Strengths**: brand, ecosystem, ZoomInfo data depth.
- **Weaknesses**: zero Saudi-native data sources, no Arabic entity resolution, no PDPL Art. 13/14 enforcement, no decision passport, ZoomInfo has weak KSA coverage.
- **Counter**: "Dealix replaces 3 tools with 1, uses Saudi-native sources US tools can't reach, and gives you audit-grade outreach defensible to your DPO and procurement."

**Comp 2 — Local incumbent CRMs (e.g., Zid CRM, regional Salesforce SIs).**
- **Strengths**: relationships, local presence, Arabic UI.
- **Weaknesses**: CRM-only — no lead generation engine, no AI scoring, no policy gating, services-heavy delivery model.
- **Counter**: "We are not a CRM — we are the engine that fills your CRM with PDPL-compliant, vertical-tagged, ranked Saudi leads."

**Comp 3 — Lead-list/agency model (boutique outreach agencies).**
- **Strengths**: low entry friction, white-glove service.
- **Weaknesses**: per-list cost, no compounding asset, no audit trail, breaks under PDPL scrutiny, lacks consent infrastructure.
- **Counter**: "Pay once for the engine, not monthly for lists. Every lead is auditable. Your team learns to operate it."

**Comp 4 — Status quo (manual + spreadsheets).**
- **Strengths**: free, full control.
- **Weaknesses**: doesn't scale, no governance, no enrichment depth, BDR burnout, opportunity cost.
- **Counter**: "You will spend 60% of your BDR hours on manual research that Dealix automates with a Decision Passport for every account."

### 3.2 Counter-positioning matrix (consumed by T8)

| Dimension | US stack | Local CRM | Agency | Status quo | **Dealix** |
|-----------|----------|-----------|--------|-------------|-----------|
| Saudi data sources | ❌ | partial | manual | ❌ | ✅ ≥25 |
| Arabic entity resolution | ❌ | partial | ❌ | ❌ | ✅ |
| Decision Passport (audit) | ❌ | ❌ | ❌ | ❌ | ✅ |
| PDPL Art. 13/14 enforcement | ❌ | partial | ❌ | ❌ | ✅ |
| Lead Engine (seed→ranked) | ❌ | ❌ | manual | ❌ | ✅ |
| Bilingual sales motion | partial | ✅ | ✅ | partial | ✅ |
| Procurement-ready trust pack | partial | ❌ | ❌ | ❌ | ✅ |

### 3.3 Win/Loss capture protocol

Mandatory for every closed-won AND closed-lost opportunity over SAR 100K:

- **Trigger**: opp moves to Won or Lost stage in CRM.
- **Action**: AE schedules 30-min Win/Loss call with primary buyer within 14 days.
- **Capture**: standardized questions (see 3.4) into `docs/sales/win_loss_log.md` (created in W2 enablement).
- **Review**: monthly Win/Loss review by CRO + CEO + Product; insights feed roadmap (T11) and persona matrix (T8).

### 3.4 Win/Loss question bank (10 questions)

1. What problem were you trying to solve when you opened the procurement process?
2. Who else did you evaluate? (capture exact tool names)
3. What did you like and dislike about each option?
4. What was the deciding factor?
5. What surprised you (positively or negatively) about Dealix during the cycle?
6. Was PDPL/Trust a gating factor? How?
7. How long did internal alignment take? Where did it stall?
8. What would have made you decide faster?
9. What is your 12-month plan for revenue tooling?
10. (Loss only) What would Dealix need to change for you to reconsider?

### 3.5 Competitive intelligence operating rhythm

- **Weekly**: sales records every observed competitor mention in CRM custom field.
- **Monthly**: this doc reviewed; matrix updated; new entrant added if observed ≥3 times in a quarter.
- **Quarterly**: deep-dive on top competitor; counter-positioning A/B tested via T26.

## 4. KPIs

- Win/Loss capture rate: 100% of opps ≥ SAR 100K within 14 days of close.
- Win rate vs Comp 1 (US stack): baseline by Q1; target +10pp by Q2.
- Counter-positioning A/B beats control: ≥1 winning variant per quarter.

## 5. Dependencies

- ICP (T5), persona matrix (T8) for buyer framing.
- A/B framework (T26) for counter-positioning tests.
- Sales enablement (T28) for rep training on counter-positioning.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Persona: `docs/sales/persona_value_matrix.md`
- A/B: `docs/experiments/ab_framework.md`
- Existing: `docs/COMPETITIVE_POSITIONING.md` (cross-link, do not rewrite)

## 7. Owner & Review Cadence

- **Owner**: CEO (CRO co-owner for sales surface).
- **Review**: monthly Win/Loss meeting; quarterly competitor deep-dive.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CEO | Initial 4-competitor landscape, counter-positioning matrix, Win/Loss protocol |
