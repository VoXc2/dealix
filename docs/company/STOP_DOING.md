# Stop Doing — The Negative Operating List

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [STOP_DOING_AR.md](./STOP_DOING_AR.md)

## Context
A founder-led AI company dies from the wrong yeses, not the wrong nos.
This file enumerates the things Dealix will not do. Every entry below
removes a class of failure observed in adjacent companies in MENA AI
services. It plugs into the discipline defined by
`docs/DEALIX_OPERATING_CONSTITUTION.md` and the incident runbook in
`docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — when a stop-doing
rule is broken, it is treated as an incident.

## The List

> Dealix will not:

1. **Build features before repeated demand.** A feature must show up
   in at least three customer conversations before it enters a
   sprint plan.
2. **Sell enterprise before delivery is repeatable.** Enterprise tier
   is gated on ≥ 2 retainers running ≥ 6 months with QA ≥ 85 (see
   `docs/company/OFFER_LADDER.md`).
3. **Promise guaranteed leads or sales.** Outcomes are influenced, not
   guaranteed. We sell processes and proof.
4. **Accept unknown-source personal contact lists.** PDPL applies. If
   the buyer cannot show consent or lawful basis, we decline.
5. **Build cold WhatsApp automation.** Regional regulation and brand
   risk make it a no.
6. **Build LinkedIn automation.** ToS, account-loss risk, and signal
   degradation make it a no.
7. **Deliver client-facing AI output without QA.** Every AI artifact
   that reaches the buyer passes a named QA reviewer.
8. **Start AI implementation before data readiness.** Data readiness
   gate is mandatory; if data fails the gate, scope is reshaped or
   the project paused.
9. **Take projects that do not create proof or assets.** Every
   engagement must produce at least one anonymizable proof artifact
   and one reusable module element.

## Why Each Rule Exists

| Rule | Failure mode it prevents |
|---|---|
| 1 | Founder builds; nobody buys. |
| 2 | Enterprise contract fails; reputation broken. |
| 3 | Guarantee is missed; refund + churn. |
| 4 | PDPL exposure; legal risk. |
| 5 | Brand burn; user complaints. |
| 6 | LinkedIn ban; lead-gen surface lost. |
| 7 | Bad AI output reaches buyer; trust lost. |
| 8 | AI on bad data → bad results → blamed AI. |
| 9 | Time spent, nothing reusable, no upsell. |

## Enforcement

- Each rule maps to a *gate* in `delivery_os` or `revenue_os`.
- A breach triggers an incident entry in
  `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.
- Repeat breaches of the same rule trigger a constitution review.

## When the List Changes

The list only grows by addition. Removing a rule requires:

- Written evidence that the failure mode no longer applies.
- Founder sign-off.
- Update to the constitution.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Incoming SOWs, sprint proposals | Accept / reject decision | Founder | Per proposal |
| Breach events | Incident entry | Founder | Per breach |
| Quarterly review | List additions | Founder | Quarterly |

## Metrics
- Rule breaches per quarter — target 0.
- Proposals declined under rule N — count.
- Repeat-breach count — target 0.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitution this list operationalizes.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan that depends on these constraints.
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — incident runbook for breaches.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
