# Strategic Dashboard — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [STRATEGIC_DASHBOARD_AR.md](./STRATEGIC_DASHBOARD_AR.md)

## Context
Most company dashboards measure revenue. The Strategic Dashboard
measures the **five capitals** that the firm is supposed to
accumulate. It is the single board the founder reads to know whether
Dealix is winning the long game. It sits above the operational
metrics in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`, complements the
financial view in `docs/FINANCE_DASHBOARD.md`, and feeds the executive
decision pack in `docs/EXECUTIVE_DECISION_PACK.md`.

## What the dashboard tracks

The dashboard tracks the five capitals defined in
`docs/company/DEALIX_CAPITAL_MODEL.md`, each broken into the
sub-categories that capture its accumulation surface.

### Service Capital
- Ready services — services in the active catalog.
- Beta services — services in pilot validation.
- Scalable services — services with full unit economics and templates.

### Product Capital
- Internal tools — count and adoption.
- Client-visible features — count and usage.
- Repeated workflows — workflows running the same way across ≥ 3
  clients.

### Knowledge Capital
- Playbooks — sector-specific operational guides.
- Templates — reusable artifacts at Stage 2+ in the graduation system.
- Benchmarks — published quantitative references.

### Trust Capital
- Proof packs — total count and recent quarter additions.
- Case studies — published.
- Testimonials — recorded.
- Governance incidents — count, severity, and resolution status.

### Market Capital
- Audience — subscribers, followers, repeat readers.
- Partners — active partner count.
- Referrals — referrals received in last quarter.
- Inbound leads — qualified inbound conversations.

## The principle

> Dealix measures itself as an accumulation of assets, not as a stream
> of revenue.

Revenue without capital accumulation is a leading indicator of
mid-term decline. Capital accumulation with low revenue is a
short-term risk but a long-term win. The Strategic Dashboard exists
to force this trade-off into the founder's weekly review.

## Reading cadence

- **Weekly** — operational tiles (active projects, pipeline, capacity).
- **Monthly** — capital deltas across the five capitals.
- **Quarterly** — strategic review against the targets declared in
  `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Update mechanics

Each tile has a documented source. Service Capital pulls from the
Service Ladder, Product Capital from the engineering backlog,
Knowledge Capital from the IP Registry and Knowledge Graph, Trust
Capital from the Capital Ledger and proof-pack archive, Market Capital
from analytics and the partner roster. No tile is allowed to depend
on manual recollection.

## Decision rules

- If two capitals drop quarter-over-quarter, an investigation is
  opened.
- If Trust Capital drops while revenue is up, the firm pauses new
  sales until proof-pack production resumes.
- If Market Capital is flat for two quarters, the Content Engine is
  audited.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Capital Ledger | Trust + Service tile values | Founder | Weekly |
| IP Registry | Knowledge tile values | Founder | Weekly |
| Engineering backlog | Product tile values | Founder | Weekly |
| Content / partner data | Market tile values | Founder | Weekly |

## Metrics
- Capital growth index — composite quarter-over-quarter change across the five capitals; target ≥ +5%.
- Capitals at risk — capitals flat or down quarter-over-quarter; target ≤ 1.
- Dashboard freshness — share of tiles updated within the cadence; target 100%.
- Decision-to-action latency — days between a dashboard trigger and a logged action; target ≤ 5.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — operational KPI surface beneath this dashboard.
- `docs/FINANCE_DASHBOARD.md` — financial complement to capital view.
- `docs/EXECUTIVE_DECISION_PACK.md` — pack the dashboard feeds.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — model the dashboard measures.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
