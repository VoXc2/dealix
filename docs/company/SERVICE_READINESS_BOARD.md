# Service Readiness Board — Master · Operating Blueprint

**Layer:** Master · Operating Blueprint
**Owner:** Head of Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SERVICE_READINESS_BOARD_AR.md](./SERVICE_READINESS_BOARD_AR.md)

## Context
The Service Readiness Board tracks every Dealix service against the
mandatory 10-per-service rule defined in
`docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md`. It is the single
source of truth for what we can sell publicly, sell as a pilot, or
should keep hidden. It complements
`docs/COMPANY_SERVICE_LADDER.md` (catalogue scaffold) and
`docs/OFFER_LADDER_AND_PRICING.md` (pricing) by enforcing readiness
gates before a service is listed.

## How to read the board
Each row scores a service against the 10 mandatory elements:
1. Offer (one-pager)
2. Scope (in / out)
3. Intake form
4. Data request list
5. Delivery checklist
6. QA checklist
7. Product module (or "n/a" if not applicable)
8. Governance rules
9. Proof Pack template
10. Upsell path

Marks: `✓` = present and current · `partial` = drafted but incomplete ·
`–` = missing · `n/a` = legitimately not applicable (must be justified
in the service's notes).

## Status definitions
- **Ready** — all 10 elements present (or justified n/a). OK to sell at
  full price.
- **Beta** — ≥ 6 elements present. Sell only as a pilot, with discount
  or strategic relationship, never at full list price.
- **Concept** — < 6 elements present. Do not list publicly. May be
  pitched 1:1 only after CEO approval.

## The Board

| Service | Offer | Scope | Intake | Data Req | Delivery Chk | QA Chk | Product Module | Governance | Proof Pack | Upsell | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Lead Intelligence Sprint | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Ready |
| AI Quick Win Sprint | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | partial | ✓ | ✓ | ✓ | Ready |
| Company Brain Sprint | ✓ | ✓ | ✓ | ✓ | partial | partial | partial | ✓ | partial | ✓ | Beta |
| Revenue Diagnostic | ✓ | ✓ | partial | ✓ | ✓ | ✓ | n/a | ✓ | ✓ | ✓ | Ready |
| Pipeline Setup | partial | partial | – | – | – | – | – | partial | – | partial | Concept |
| Pilot Conversion Sprint | partial | partial | – | – | – | – | – | – | – | – | Concept |
| Monthly RevOps OS | partial | – | – | – | – | – | – | – | – | – | Concept |
| AI Support Desk Sprint | partial | – | – | – | – | – | – | – | – | – | Concept |
| Inbox Operations Setup | – | – | – | – | – | – | – | – | – | – | Concept |
| Feedback Intelligence | – | – | – | – | – | – | – | – | – | – | Concept |
| Monthly Support AI | – | – | – | – | – | – | – | – | – | – | Concept |
| Workflow Automation Sprint | – | – | – | – | – | – | – | – | – | – | Concept |
| Executive Reporting Automation | – | – | – | – | – | – | – | – | – | – | Concept |
| Monthly AI Ops | – | – | – | – | – | – | – | – | – | – | Concept |
| Sales Knowledge Assistant | – | – | – | – | – | – | – | – | – | – | Concept |
| Policy Assistant | – | – | – | – | – | – | – | – | – | – | Concept |
| Monthly Brain Management | – | – | – | – | – | – | – | – | – | – | Concept |
| AI Readiness & Risk Review | partial | partial | – | – | – | – | n/a | ✓ | – | – | Beta |
| AI Usage Policy | partial | – | – | – | – | – | n/a | ✓ | – | – | Beta |
| PDPL-Aware Data Review | partial | – | – | – | – | – | n/a | ✓ | – | – | Beta |
| AI Governance Program | – | – | – | – | – | – | – | ✓ | – | – | Concept |
| Data Cleanup & Unification | – | – | – | – | – | – | – | – | – | – | Concept |
| AI Business Dashboard | – | – | – | – | – | – | – | – | – | – | Concept |
| Forecasting & Scoring | – | – | – | – | – | – | – | – | – | – | Concept |
| Data Readiness for AI | partial | partial | – | – | – | – | partial | ✓ | – | partial | Beta |

## Snapshot counts (2026-05-13)
- Ready: 3
- Beta: 5
- Concept: 17
- Total: 25

## Owners
Every service has one named owner accountable for moving it to Ready.
Owners are listed in the Sunday CEO Review board. If a service has no
owner, it is automatically de-listed from any sales material until an
owner is assigned.

## Cadence
- **Weekly** — Sunday CEO Review. Status of each row, plus net
  movement (Ready ↔ Beta ↔ Concept). Block any sales motion against
  services not Ready unless a CEO-approved exception is logged.
- **Monthly** — Trim list. Any service "Concept" for > 60 days without
  a customer signal is either parked or killed.
- **Quarterly** — Add net-new services only if they pass the
  10-per-service gate at "≥ Beta" on day 1.

## Promotion rule
A service moves to Ready only when:
1. All 10 elements are `✓` (or justified `n/a`).
2. At least one paid delivery has shipped against the service.
3. A signed and anonymized Proof Pack exists.
4. The upsell path has been triggered at least once (even if not yet
   accepted).
5. QA Lead and CEO have both signed the promotion in the Sunday review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| 10-per-service evidence per service | Status (Ready/Beta/Concept) | Head of Delivery | Weekly |
| Signed Proof Packs | Promotion triggers | Delivery Lead | Per delivery |
| Pricing changes | Re-rank of upsell paths | CEO | Quarterly |
| Kill / park decisions | Service de-listing | CEO | Monthly |

## Metrics
- **Ready count** — target: ≥ 3 by day 90, ≥ 6 by day 180.
- **Beta count** — keep ≤ 6 in active sale; older Betas must promote or park.
- **Concept ageing** — 0 services in "Concept" > 60 days without a customer.
- **Owner coverage** — 100% of listed services have a named owner.

## Related
- `docs/OFFER_LADDER_AND_PRICING.md` — prices the Ready services are sold at.
- `docs/COMPANY_SERVICE_LADDER.md` — catalogue scaffold this board enforces.
- `docs/business/MANAGED_PILOT_OFFER.md` — template for Beta pilot sales.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic priorities feeding the kill / double-down list.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — defines the 10-per-service rule.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
