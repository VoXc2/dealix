# Success Assurance System — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO + Group COO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SUCCESS_ASSURANCE_SYSTEM_AR.md](./SUCCESS_ASSURANCE_SYSTEM_AR.md)

## Context
A typical startup judges itself on revenue alone. Dealix judges itself on **seven dimensions of success at the same time**, because each dimension protects the others from collapsing. Revenue alone is fragile: a quarter of big checks with no proof and no retainer is a flash that disappears. This file defines the seven dimensions, the cascade rule between them, and how the Strategic Control Tower surfaces a failing dimension before it kills the others. The dashboards that operationalize this file live in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` and `docs/EXECUTIVE_DECISION_PACK.md`. Underlying evidence is captured in `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md`.

## The seven success dimensions

| # | Dimension | Question it answers | Failure mode if neglected |
|---|---|---|---|
| 1 | Commercial | Are we selling? | Cash dries up |
| 2 | Delivery | Are projects shipped on time, at quality? | Refunds, churn, brand damage |
| 3 | Proof | Are outcomes documented and defensible? | No referrals, no retainers |
| 4 | Product | Are repeated steps productized into Core OS? | Margins capped at agency level |
| 5 | Governance | Are AI uses safe, auditable, PDPL-aligned? | Enterprise trust collapse, fines |
| 6 | Capital | Are reusable assets captured per project? | No compounding, no moat |
| 7 | Strategic | Are we still ahead on category position? | Commoditization, price war |

## The cascade rule

The seven dimensions are not independent — they cascade. Failure in an earlier dimension makes the later ones meaningless:

```
Commercial → Delivery → Proof → Retainer → Product → Capital → Strategic
```

Reading the cascade:

1. **Commercial without Delivery** = burnt customer base.
2. **Delivery without Proof** = invisible outcomes, no compounding.
3. **Proof without Retainer Conversion** = one-shot revenue.
4. **Retainer without Productization** = stuck at agency margin.
5. **Product without Sales** = unused inventory.
6. **Capital without Strategic alignment** = a library of unused assets.
7. **Governance failure** at any step = kills trust across all of the above.

This is the structural reason Dealix runs as a holding: the cascade is enforced by **separate functions with shared metrics**, not by a single team trying to optimize everything at once.

## Per-dimension assurance loops

### 1. Commercial assurance
- Owner: Head of Sales (Shared Service).
- Signal: pipeline coverage, win rate, ARR, retention.
- Loop: weekly pipeline review; monthly cohort retention review.

### 2. Delivery assurance
- Owner: Head of Dealix Services + QA lead.
- Signal: QA score, on-time delivery, NPS, refund rate.
- Loop: every sprint closure must pass QA gate before invoice.

### 3. Proof assurance
- Owner: BU GMs + Proof Ledger owner.
- Signal: proof packs / project, ROI captured, case study count.
- Loop: no project is "Closed" until a Proof Pack is in the Proof Ledger.

### 4. Product assurance
- Owner: Head of Dealix Core.
- Signal: # repeated steps productized, Core OS adoption ratio.
- Loop: bi-weekly Product Council reviews `feature_candidate_created` events.

### 5. Governance assurance
- Owner: Group GC / DPO.
- Signal: critical incidents (target 0), policy coverage, audit log completeness.
- Loop: weekly governance huddle, monthly PDPL review.

### 6. Capital assurance
- Owner: Head of Dealix Core + Proof Ledger owner.
- Signal: assets per project, asset reuse rate.
- Loop: every project ships with at least 2 `capital_asset_created` events.

### 7. Strategic assurance
- Owner: CEO.
- Signal: category position, inbound velocity, enterprise readiness.
- Loop: quarterly strategic review against `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Surfacing failure early
The [`STRATEGIC_CONTROL_TOWER.md`](./STRATEGIC_CONTROL_TOWER.md) is the single screen where all seven dimensions are visible. Any dimension entering a **red** state for two consecutive weeks triggers a CEO-level decision: sell, build, stop, raise, or hire — whichever unblocks the failing dimension.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| BU weekly P&L and pipeline | Commercial signal | Sales head | Weekly |
| QA reports per sprint | Delivery signal | QA lead | Per sprint |
| Proof Ledger entries | Proof signal | Proof owner | Per project |
| Core OS roadmap commits | Product signal | Head of Core | Bi-weekly |
| Audit log + incident log | Governance signal | DPO | Weekly |
| Capital Ledger entries | Capital signal | Head of Core | Per project |
| Market & competitor intel | Strategic signal | CEO | Quarterly |

## Metrics
- **Dimensions in green** — count of the 7 dimensions in green this week (target 7).
- **Cascade break events** — incidents where one dimension's failure caused another to fail.
- **Mean time to recover** — days from a dimension turning red to returning to green.
- **Decisions resolved** — sell/build/stop/raise/hire decisions issued per quarter.
- **Cross-dimension correlation** — for each pair (e.g. Proof × Retainer), measured as cohort-level statistical link.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard spec that materializes these dimensions.
- `docs/EXECUTIVE_DECISION_PACK.md` — weekly executive decision packet.
- `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md` — group-level evidence ledger.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — enforcement framework.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
