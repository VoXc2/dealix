# Proof-to-Upsell Map — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder / CSM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PROOF_TO_UPSELL_MAP_AR.md](./PROOF_TO_UPSELL_MAP_AR.md)

## Context
Every proof Dealix produces during a sprint is also a sales signal.
The Proof-to-Upsell Map turns the closing artifact of one engagement
into the opening artifact of the next, in line with the revenue
playbook in `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and the customer
success motion described in `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`. It is
the bridge between Layer 1 (capital) and the revenue engine that funds
further capital accumulation.

## The map

| Proof Found | Meaning | Upsell |
|---|---|---|
| Top 50 accounts identified | Client now needs execution | Pilot Conversion Sprint |
| Data quality improved but CRM messy | Client needs ongoing hygiene | Monthly RevOps OS |
| Support categories identified | Client needs reply system | AI Support Desk |
| Documents indexed | Client needs ongoing updates | Monthly Company Brain |
| Workflow saves hours | Client needs more workflows | Monthly AI Ops |
| Governance risks found | Client needs policy | AI Governance Program |

## How it is used

At project closure the delivery lead runs the proof-pack against this
map and identifies the **one** highest-fit upsell. The recommendation
is recorded in the closure report and routed to the founder or CSM
for an upsell conversation within ten business days. Multiple
recommendations are allowed only when proofs are independent.

## Why one recommendation at a time

Pushing multiple upsells immediately dilutes trust and signals
salesiness. The map is intentionally one-to-one: every proof has one
canonical next step. Variants are handled by sequencing, not bundling.

## When no upsell fits

If no proof in the closure matches a row in the map, the project is
classified as **flat capital** — value was delivered but no expansion
path was opened. The team logs a capital-debt note and reviews whether
the engagement scope should be reshaped for the next similar client.

## Adding to the map

A new row is added when a recurring proof pattern emerges across three
or more sprints without a defined upsell. The new row must declare:

- The exact proof artifact (e.g., a section of the proof pack).
- The unmet client need it implies.
- The canonical Dealix offer that addresses it.
- A reference to the matching row in
  `docs/OFFER_LADDER_AND_PRICING.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Closure proof pack | Upsell recommendation | Delivery lead | Per project |
| Sales outcome | Upsell conversion data | Founder / CSM | Per attempt |
| Quarterly review | New rows or removals | Founder | Quarterly |
| Customer-success log | Renewal vs. upsell split | CSM | Monthly |

## Metrics
- Upsell-recommendation rate — share of closed projects that produced a recommendation; target ≥ 80%.
- Upsell conversion — share of recommendations converted to signed offers within 60 days; target ≥ 30%.
- Time-to-upsell-conversation — median business days from closure to conversation; target ≤ 10.
- Flat-capital rate — share of closures with no recommendation; target ≤ 20%.

## Related
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue motion this map plugs into.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — operational playbook for the upsell conversation.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot offer the top row recommends.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model that closes the loop.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
