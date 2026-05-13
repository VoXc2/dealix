---
title: Saudi ICP — Multi-tier Ideal Customer Profile
doc_id: W1.T05.icp-saudi
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: docs/go-to-market/icp_saudi.ar.md
related: [W0.T00, W1.T01, W1.T17, W1.T31, W2.T04, W2.T08]
kpi:
  metric: icp_qualified_accounts_in_crm
  target: 200
  window: 60d
rice:
  reach: 300
  impact: 3
  confidence: 0.9
  effort: 1
  score: 810
---

# Saudi ICP — Multi-tier Ideal Customer Profile

## 1. Context

The existing `docs/POSITIONING_AND_ICP.md` is generic. The Saudi enterprise market has a sharper buyer profile (state-adjacent budgets, PDPL/Vision 2030 alignment, bilingual procurement, royal-decree-level decision velocity in some segments) that requires a dedicated ICP. This document is the canonical Saudi ICP and the vocabulary source for verticals (T1), persona matrix (T8), GTM 12m (T4), and the Lead Engine targeting layer (T31).

## 2. Audience

CRO, Head of Sales, BDRs, partners. Used to score MQL→SQL→Opportunity and to seed the Lead Engine.

## 3. Decisions / Content

### 3.1 Three ICP tiers

**Tier 1 — Enterprise core (top-priority).**
- **Firmographic**: SAR 200M+ revenue, 200+ employees, HQ Riyadh / Jeddah / Khobar, CR active ≥ 5 years.
- **Sectoral**: BFSI (SAMA-regulated banks, finance companies, fintechs), Telco (CITC-licensed Tier-1), Energy (Aramco affiliates, downstream), Govt-adjacent (PIF portfolio, sovereign vehicles), Large Retail (chains with ≥50 outlets), Healthcare groups (SFDA-licensed hospital networks).
- **Technographic**: existing CRM (Salesforce / MS Dynamics / HubSpot Enterprise), Arabic + English internal ops, dedicated CISO or DPO.
- **Buying committee**: CEO/Managing Director sponsor, CRO/CCO economic buyer, CIO/CTO technical buyer, DPO/Legal compliance buyer, Procurement gatekeeper.
- **Deal size**: SAR 500K–3M ARR.
- **Cycle**: 90–180 days.

**Tier 2 — Mid-market expansion.**
- **Firmographic**: SAR 30M–200M revenue, 50–200 employees.
- **Sectoral**: Tech-forward verticals (SaaS, edtech, healthtech, fintech challengers), regional retail brands, professional services groups, mid-sized contractors.
- **Buying committee**: founder/CEO, Head of Sales/Growth, Head of Tech.
- **Deal size**: SAR 100K–500K ARR.
- **Cycle**: 30–90 days.

**Tier 3 — SME (PLG/long-tail).**
- **Firmographic**: SAR 5M–30M revenue, 10–50 employees, Monsha'at-tagged.
- **Sectoral**: e-commerce on Salla/Zid, B2B SaaS, agencies, F&B chains.
- **Buying committee**: founder.
- **Deal size**: SAR 24K–100K ARR.
- **Cycle**: 7–30 days; self-serve onboarding.

### 3.2 Deal-breakers (immediate disqualify)

- No CR or expired CR.
- Active legal/regulatory enforcement action.
- < SAR 5M revenue and no growth signal.
- Not VAT-registered (for Enterprise tier) — implies non-compliant operations.
- Requests data residency outside KSA (cannot fulfill on Sovereign tier).

### 3.3 MQL → SQL → Opportunity scoring

| Stage | Required signals | Owner | SLA |
|-------|------------------|-------|-----|
| MQL | ICP-firmographic match + 1 engagement signal (web, content, event) | Marketing | n/a |
| SQL | MQL + buying-committee contact identified + budget signal (tender, hiring, funding) | BDR | qualified in 7 days |
| Opportunity | SQL + discovery call completed + initial pain validated + Decision Passport draft | AE | created in 14 days from SQL |

### 3.4 Buying triggers (highest-intent signals)

1. **Tender on Etimad** matching ICP keywords (e.g., "Revenue", "Sales", "AI", "Data").
2. **Senior hire** posted on LinkedIn ("Head of Sales", "Head of AI", "CRO", "CDO", "Head of Growth").
3. **Funding round** (Wamda/MAGNiTT) ≥ SAR 20M.
4. **M&A or expansion news** (Argaam/SPA).
5. **CR amendment** indicating activity expansion (sectoral move).
6. **Vision 2030 program enrollment** (PIF portfolio, NTP linkage).
7. **PDPL DPO appointment** (signals compliance readiness for vendor onboarding).

### 3.5 Lead Engine targeting taxonomy (consumed by T31)

The Saudi Lead Engine accepts seeds in this taxonomy:

```
seed:
  vertical: [bfsi | telco | energy | govt_adjacent | retail | healthcare | manufacturing | logistics | hospitality | edtech | fintech | other]
  region: [riyadh | jeddah | khobar | medina | makkah | dammam | other]
  tier: [enterprise | mid_market | sme]
  trigger: [tender | hire | funding | expansion | cr_amendment | vision2030 | dpo_appointment | none]
  exclude: [list of CR numbers, domains, or competitor-customer flags]
```

This taxonomy is the contract between the ICP (this doc) and the Lead Engine (T31). Any new vertical added here must be added to `auto_client_acquisition/revenue_os/source_registry.py` ICP filters within 7 days.

## 4. KPIs

- 200 ICP-qualified accounts in CRM within 60 days.
- ≥70% of new opportunities tagged Tier 1 within 90 days.
- < 20% disqualification rate at Opportunity stage (signal: ICP is right-tuned).

## 5. Dependencies

- Upstream: master plan (W0.T00).
- Downstream: verticals (T1), persona matrix (T8), GTM 12m (T4), Lead Engine (T31).
- Existing doc: `docs/POSITIONING_AND_ICP.md` (kept for non-Saudi context; add cross-link note).

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Verticals: `docs/go-to-market/saudi_vertical_positioning.md`
- Lead Engine: `docs/product/saudi_lead_engine.md`
- Existing: `docs/POSITIONING_AND_ICP.md`

## 7. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: monthly with sales leadership; quarterly with CEO.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial 3-tier Saudi ICP with deal-breakers, triggers, and Lead Engine taxonomy |
