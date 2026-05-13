---
title: Revenue-Weighted Roadmap
doc_id: W1.T11.roadmap
owner: HoP
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W1.T31, W4.T13, W4.T24, W4.T26]
kpi:
  metric: revenue_weighted_items_shipped_top_quartile
  target: 80%
  window: quarterly
rice:
  reach: 0
  impact: 3
  confidence: 0.8
  effort: 2
  score: roadmap-governance
---

# Revenue-Weighted Roadmap

## 1. Context

Engineering-driven roadmaps optimize for technical elegance and accumulate features that nobody pays for. A revenue-weighted roadmap forces every backlog item to declare its dollar (SAR) impact, deal-stage influence, and customer-account reach before it competes for engineering capacity. This doc is the governance contract for how Dealix prioritizes the product backlog — quarterly.

## 2. Audience

HoP, CTO, CEO. Engineering managers consume scoring; sales/CS contributes weights.

## 3. Decisions / Content

### 3.1 Revenue-weighted RICE (RW-RICE)

Standard RICE + two Saudi-revenue multipliers:

- **Reach** = number of paying Saudi accounts that touch the feature in 90d.
- **Impact** ∈ {0.25, 0.5, 1, 2, 3} — same as master plan.
- **Confidence** ∈ [0.5, 0.7, 0.9, 1.0].
- **Effort** = engineering person-weeks.
- **Revenue multiplier** ∈ [0.5, 1.0, 1.5, 2.0]:
  - 0.5 = enables existing revenue (retention-only).
  - 1.0 = enables new revenue from existing segment.
  - 1.5 = unlocks new ICP tier.
  - 2.0 = unlocks new vertical (BFSI/Retail/Healthcare).
- **Vision-2030 alignment multiplier** ∈ [1.0, 1.2]:
  - 1.2 = directly supports a Vision 2030 program target (Saudization, data sovereignty, SME enablement).
- **RW-RICE** = (Reach × Impact × Confidence × Rev-mult × V2030-mult) / Effort.

### 3.2 Quarterly capacity allocation

Engineering capacity (target distribution):

| Bucket | % capacity | Examples |
|--------|-----------|----------|
| Top-quartile RW-RICE features | 50% | Lead Engine sources, Decision Passport hardening |
| Engineering health (ADRs, debt, SLO work) | 20% | Event store migration, observability |
| Trust/compliance | 15% | PDPL features, audit log, retention |
| Quick wins / customer-requested | 10% | Logged in CS-driven feature requests |
| Speculative / R&D | 5% | New model integrations, experimental UX |

### 3.3 Backlog item template (frontmatter)

Every backlog item (issue, RFC, ticket) carries:

```yaml
rw_rice:
  reach: 0
  impact: 0
  confidence: 0
  effort: 0
  revenue_multiplier: 1.0
  v2030_multiplier: 1.0
  score: 0
links_to:
  customer_evidence: [list of CRM opp IDs or CS tickets]
  saudi_vertical: [bfsi | retail | healthcare | other]
  kpi_owned: <metric from T13 KPI spec>
```

### 3.4 Quarterly planning ritual

- **Week -2**: HoP collects backlog scores, normalizes, ranks.
- **Week -1**: cross-functional review (CRO, CTO, CS) re-weights based on evidence.
- **Week 0**: CEO approves top-quartile commit; remainder is stretch.
- **Week +6 (mid-quarter)**: review shipped vs planned; reallocate.
- **Week +12 (close)**: outcomes vs predicted impact captured into Win/Loss-style retrospective.

### 3.5 Linkage to T13 executive dashboard

Every top-quartile item must declare which KPI (from T13 executive KPI spec) it moves. Items that cannot point to a tracked KPI are demoted automatically.

### 3.6 Tie-breakers when scores are equal

1. Unblocks a Tier-1 enterprise deal in commit.
2. Enables a new Saudi vertical.
3. Reduces engineering toil (frees capacity).
4. Brings AR/EN parity (bilingual debt).
5. Reduces a tracked enterprise legal risk (T27).

## 4. KPIs

- Top-quartile shipped: ≥ 80% per quarter.
- % of shipped items with predicted-vs-actual impact retro: 100%.
- Engineering-health bucket utilization: 20% ± 5%.

## 5. Dependencies

- KPI spec (T13) — defines metrics every item must move.
- A/B framework (T26) — validates predicted impact post-ship.
- FinOps (T24) — gates expensive features.
- Lead Engine (T31) — top customer of high-RW-RICE items in Q1–Q2.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Lead Engine: `docs/product/saudi_lead_engine.md`
- KPI spec: `docs/analytics/executive_kpi_spec.md`
- Existing: `docs/STRATEGIC_MASTER_PLAN_2026.md` (cross-link, not replaced)

## 7. Owner & Review Cadence

- **Owner**: HoP.
- **Review**: quarterly planning ritual (above) + monthly mid-cycle check.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoP | Initial RW-RICE governance, capacity allocation, quarterly ritual |
