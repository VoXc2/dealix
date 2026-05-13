# Scope Control — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SCOPE_CONTROL_AR.md](./SCOPE_CONTROL_AR.md)

## Context
Scope drift is the leading cause of margin loss and missed proof in
small AI engagements. This file defines the change-request process,
scope creep prevention rules, out-of-scope detection patterns, and the
pricing rules for changes. It pairs with the Delivery Standard
(`docs/delivery/DELIVERY_STANDARD.md`), the Customer Success Playbook
(`docs/CUSTOMER_SUCCESS_PLAYBOOK.md`), and the founder oversight in
`docs/V14_FOUNDER_DAILY_OPS.md`.

## Definitions
- **In-scope** — items explicitly listed in the signed Scope of Work.
- **Out-of-scope** — items explicitly listed under "NOT included" in
  the Scope of Work.
- **Implicit-scope** — items not listed but reasonably required to
  meet the in-scope success metric. Treated as in-scope unless time
  cost is material.
- **Change request** — any request to add, remove, or modify an
  in-scope or out-of-scope item.

## Change Request Process
1. **Capture** — any scope-affecting request goes into a change
   request record within 24 hours. No verbal-only changes.
2. **Classify** — the delivery lead classifies the request as
   `clarification`, `additive`, `substitution`, or `cancellation`.
3. **Estimate** — AI platform lead and delivery lead estimate hours,
   risk, and dependency impact.
4. **Price** — apply the pricing rules below.
5. **Approve** — client sponsor and delivery lead sign the change
   request.
6. **Implement** — only after a signed change request.

## Scope Creep Prevention
- Weekly check-ins include a scope reconfirmation slot.
- Any request that touches a different capability than the contracted
  one is automatically a change request.
- Drafts produced for out-of-scope items are not delivered until a
  change request is signed.
- The QA checklist includes a scope-conformance line.

## Out-of-Scope Detection Patterns
- New entity types not in the signed scope (e.g., adding "Lead
  scoring" to a Company Brain project).
- New channels (e.g., adding WhatsApp to an email-only outreach).
- New languages beyond the contracted bilingual default.
- New target audience tiers.
- Custom integrations not in the data request.

## Pricing Rules For Changes
| Change class | Pricing | Approver |
|---|---|---|
| Clarification | No fee | Delivery lead |
| Additive (≤ 4 hours) | Hourly rate | Delivery lead |
| Additive (> 4 hours) | New SOW addendum | Sponsor + Founder |
| Substitution (equivalent effort) | No fee | Delivery lead |
| Substitution (different effort) | Hourly delta or addendum | Sponsor |
| Cancellation | Pro-rata refund per contract | Founder |

## Founder Override
The founder may override any classification or pricing decision in
writing. The override is logged as an audit event.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client request | Change request record | Delivery lead | Per request |
| Classification | Estimate and price | Delivery lead | Per request |
| Signed change request | Workflow update | AI platform lead | Per request |
| Quarterly review | Scope-control trends | Founder | Quarterly |

## Metrics
- **Change request capture rate** — share of scope-affecting requests
  recorded within 24 hours. Target: 100%.
- **Unsigned-change deliveries** — drafts delivered without a signed
  change request. Target: 0.
- **Scope-driven margin variance** — variance of project margin from
  budget caused by scope changes. Target: ≤ ±10%.
- **Founder override count** — Tracked monthly.

## Related
- `docs/delivery/DELIVERY_STANDARD.md` — sibling delivery standard.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — customer success motion.
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily ops.
- `docs/business/MANAGED_PILOT_OFFER.md` — productized pilot offer.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
