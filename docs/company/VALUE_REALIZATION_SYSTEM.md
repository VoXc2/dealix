# Value Realization System — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** CEO / Head of Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [VALUE_REALIZATION_SYSTEM_AR.md](./VALUE_REALIZATION_SYSTEM_AR.md)

## Context
Dealix sells "AI Operations" — an abstract category. Buyers and operators
alike need a concrete way to know whether each engagement actually produced
value. This file defines the five proof categories Dealix uses, and the rule
that every project must produce at least one measurable value plus one
"next-value" opportunity. It is the operating spine of L3 and binds the
service ladder in `docs/COMPANY_SERVICE_LADDER.md` to the financial picture
in `docs/FINANCE_DASHBOARD.md` and the strategy in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`. Without this system, Dealix can
deliver work but not prove value — which collapses retention and pricing
power.

## The five proof categories

1. **Revenue Value** — leads ranked, pipeline created, opportunities
   clarified. Examples: top-50 ranked account list, segmented ICP, scored
   open opportunities, follow-up surfaced.
2. **Time Value** — hours saved, manual steps reduced, response time
   improved. Examples: hours/week before vs after; median first-response
   time; number of manual touches removed.
3. **Quality Value** — fewer errors, better consistency, cleaner data,
   better reports. Examples: data-quality score uplift, report
   standardization, error rate reduction.
4. **Risk Value** — PII protected, approvals logged, unsafe actions blocked.
   Examples: PDPL exposure removed, governance rule prevented X actions,
   audit log completeness.
5. **Knowledge Value** — faster answers, source-backed knowledge, fewer
   repeated questions. Examples: median answer latency, citation coverage,
   repeat-question rate.

## Mandatory rule

> Every Dealix project must produce **at least one measurable value
> category** AND **one next-value opportunity** before it can be marked
> complete.

If neither exists, the engagement is incomplete regardless of artifacts
delivered. The next-value opportunity is the seed of the next sale and the
input to the retainer offer in `docs/OFFER_LADDER_AND_PRICING.md`.

## How a value claim is constructed

Each claim must include:

- **Metric** — exact name (e.g., "hours/week spent on lead enrichment").
- **Baseline** — measured or estimated pre-engagement.
- **Result** — measured post-engagement.
- **Evidence** — proof pack reference (workflow report, dataset snapshot,
  governance log, screenshot, executive summary).
- **Owner** — the Dealix delivery owner who signs.
- **Client sign-off** — the client contact who acknowledges.

## Value lifecycle

```
discover → baseline → deliver → measure → record → next-value
```

1. **Discover** — capability conversation (Capability Value Map).
2. **Baseline** — measure or estimate pre-state.
3. **Deliver** — service from the service ladder.
4. **Measure** — re-measure or score post-state.
5. **Record** — entry in `docs/ledgers/VALUE_LEDGER.md`.
6. **Next-value** — propose the next service to the client.

## Anti-patterns

- "We delivered the workflow" — not a value claim.
- "Client is happy" — not a metric.
- Self-reported uplift without before/after baseline.
- Proof pack with no Value Ledger entry (incomplete by definition).
- Value claim without a next-value opportunity.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Scoped engagement, baseline metrics | Value claim record | Delivery owner | Per engagement |
| Proof pack artifacts | Ledger entry + next-value offer | Delivery owner + CSM | Per engagement |
| Monthly aggregation | Value-by-capability report | Head of Delivery | Monthly |
| Quarterly review | Pricing and packaging signal | CEO | Quarterly |

## Metrics
- Value Claim Coverage — % of completed engagements with a ledger entry.
- Next-Value Conversion — % of engagements that produced a follow-on offer
  accepted within 60 days.
- Value Mix — distribution of claims across the five categories.
- Time-to-Proof — days from project start to first published value claim.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic frame for value
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI surfaces consuming these signals
- `docs/FINANCE_DASHBOARD.md` — finance view that depends on proven value
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating rules referenced here
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
