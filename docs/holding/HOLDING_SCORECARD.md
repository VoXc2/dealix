# Holding Scorecard — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO + CFO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [HOLDING_SCORECARD_AR.md](./HOLDING_SCORECARD_AR.md)

## Context
This is the **single board-level scorecard** for the Dealix Group. It is reviewed by the CEO weekly and by the board monthly. Every other dashboard in the system (`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`, `docs/FINANCE_DASHBOARD.md`, `docs/EXECUTIVE_DECISION_PACK.md`) is either a feeder into this scorecard or a drill-down from it. The scorecard makes the cascade in [`SUCCESS_ASSURANCE_SYSTEM.md`](./SUCCESS_ASSURANCE_SYSTEM.md) measurable.

## The scorecard

| Dimension | Metric | Target | Red signal | Green signal |
|---|---|---|---|---|
| Revenue | MRR | Rising month-over-month | MRR flat or down 2 months in a row | MRR ↑ for 3+ months |
| Profitability | Gross margin | 65–75% | < 60% blended | > 70% blended |
| Delivery | QA score | 85+ | < 80 average over 4 sprints | 90+ average |
| Governance | Critical incidents | 0 | Any unresolved critical incident > 7 days | 0 incidents 90 days |
| Proof | Proof packs per project | 1+ | Any closed project without a pack | 100% projects with pack |
| Retention | Sprint-to-retainer | 25–40% early stage | < 20% conversion | > 40% conversion |
| Product | Repeated steps productized | Increasing | 0 new productized steps in 30 days | 3+ per quarter |
| Capital | Assets per project | 2+ | < 1 average | > 3 average |
| Market | Inbound / referrals | Increasing | Inbound share flat or down | Inbound > 30% of pipeline |
| Strategic | Enterprise readiness | Improving | Enterprise audit gap unresolved 60+ days | All audit gaps closed |

## Red / Green decision rules

- **Red on any single dimension → discussion item** at the next weekly Strategic Control Tower review.
- **Red on two dimensions in the same week → CEO decision item** (sell / build / stop / raise / hire).
- **Red on Governance** is always treated as **highest priority** — it can invalidate every other green.
- **All green for 4 weeks → opportunity item**: the Control Tower drafts an "accelerate" proposal (price increase, BU expansion, capital raise, etc.).

## Source of truth per row

| Row | Source system / doc |
|---|---|
| Revenue | Stripe + Moyasar consolidated; mirrored in `docs/FINANCE_DASHBOARD.md` |
| Profitability | Group P&L; reconciled via `docs/UNIT_ECONOMICS_AND_MARGIN.md` |
| Delivery | QA gate logs per sprint; aggregated in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` |
| Governance | Incident log + audit log emitted by Governance Runtime |
| Proof | Proof Ledger entries; one per closed project |
| Retention | CRM cohort report (sprint → retainer transitions) |
| Product | Productization Ledger (`docs/product/PRODUCTIZATION_LEDGER.md`) |
| Capital | Capital Ledger entries (`capital_asset_created` events) |
| Market | Pipeline source attribution in CRM |
| Strategic | Enterprise readiness checklist in `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` |

## Cadence

| Audience | Frequency | Format |
|---|---|---|
| CEO | Weekly | Live dashboard + 10-row table |
| Board | Monthly | PDF export + commentary |
| BU GMs | Weekly | Per-row drill-down |
| All-hands | Quarterly | Narrative summary of green/red trends |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| MRR, P&L, QA scores, incidents, proof packs, retainer conversions, productized steps, capital assets, pipeline source, enterprise gaps | One scorecard row per dimension | Group CFO + each BU GM | Weekly |
| Red signals | CEO decisions | CEO | Weekly |
| Board narrative | Monthly board pack | CEO + CFO | Monthly |

## Metrics
- **Dimensions green** — count of the 10 rows in green (target 10).
- **Mean red duration** — average days a row stays red before returning to green.
- **Red recurrence** — number of times a row enters red within a quarter.
- **Decision velocity** — average days from red trigger to CEO decision.
- **Scorecard data freshness** — max age in hours of any row's underlying source.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard spec.
- `docs/FINANCE_DASHBOARD.md` — financial source rows.
- `docs/EXECUTIVE_DECISION_PACK.md` — weekly decision packet.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — margin reconciliation.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
