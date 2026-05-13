# Capability Factory Map — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Founder / Head of Sales
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_FACTORY_MAP_AR.md](./CAPABILITY_FACTORY_MAP_AR.md)

## Context

Clients arrive with raw problems, not capability names. This file is
the translation table that maps a stated problem to the capability that
must be built, the Dealix service that builds it, the proof type that
will be produced, and the natural expansion path. It is the operating
backbone of the sales-to-delivery handoff and a direct application of
the rule defined in `docs/company/AI_CAPABILITY_FACTORY.md` and the
service ladder in `docs/COMPANY_SERVICE_LADDER.md`. Maturity scoring
is anchored to
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Map

| Input Problem | Capability Built | Dealix Service | Proof Type | Expansion |
|---|---|---|---|---|
| Leads are messy | Revenue | Lead Intelligence Sprint | Revenue / Quality | Monthly RevOps |
| Reports are manual | Reporting | Executive Reporting Automation | Time / Quality | Monthly AI Ops |
| Knowledge scattered | Knowledge | Company Brain Sprint | Knowledge | Brain Management |
| Support overloaded | Customer | AI Support Desk | Time / Quality | Monthly Support |
| AI used unsafely | Governance | AI Governance Program | Risk | Governance Retainer |
| Data not ready | Data | Data Readiness Assessment | Quality / Risk | Data OS |

## How To Use This Map

1. At intake, capture the client's stated problem in their words.
2. Match the problem to a row in the table; if no row fits, escalate
   to the founder before quoting.
3. Name the capability and the service on the proposal.
4. Set the expected proof type so QA knows what to verify.
5. Pre-position the expansion offer (the right column) for the close.

## Sales Positioning

"We identify which capability you need to build first, then choose the
right service." This sentence replaces every long service menu in
sales conversations. It also disqualifies engagements that do not land
on a named capability, which is exactly what `docs/OFFER_LADDER_AND_PRICING.md`
expects from the top of the funnel.

## Multi-Capability Engagements

A single sprint can touch more than one capability (e.g. a Lead
Intelligence Sprint touches Data and Revenue). In that case:

- Choose the primary capability for the proof type.
- List secondary capabilities in the engagement record.
- Require all touched capabilities to clear governance.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client problem statement | Mapped capability + service | Sales | Per inbound |
| Mapped service | Quote + proof type | Sales | Per inbound |
| Quote accepted | Delivery brief + expansion plan | Delivery | Per engagement |
| Delivery outcome | Expansion offer | Sales | Post-proof |

## Metrics

- Map coverage — % of inbound problems that fit an existing row.
- Capability assignment rate — % of engagements with a named capability.
- Sprint-to-retainer conversion — % of sprints that expand on the planned path.
- Time to quote — hours from intake to mapped quote.

## Related

- `docs/COMPANY_SERVICE_LADDER.md` — services referenced by the map.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing for each mapped service.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan that frames the categories.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity levels referenced by the map (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
