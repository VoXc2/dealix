# Service Catalog v1 — Five Public Doors

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SERVICE_CATALOG_V1_AR.md](./SERVICE_CATALOG_V1_AR.md)

## Context
Externally, Dealix presents five doors. Internally, the company runs
many services across maturity tiers. This file enforces the separation
so the website never overwhelms a buyer, the proposal never lists more
than one service, and the internal roadmap stays free to evolve. It
operationalizes the catalog discipline described in
`docs/COMPANY_SERVICE_LADDER.md` and the offer architecture in
`docs/OFFER_LADDER_AND_PRICING.md`, under L7 of the Dealix layers.

## The Three Surfaces

> Public website = 5 doors. Proposal = one clear service. Internal
> roadmap = all services.

| Surface | Audience | Surface count | Source of truth |
|---|---|---|---|
| Public website | Prospect | 5 doors | This file |
| Proposal | Buyer | 1 service | Sales conversation |
| Internal roadmap | Team | All services | `docs/COMPANY_SERVICE_LADDER.md` |

## The Five Doors

### Door 1 — Grow Revenue
Outcome the buyer wants: more pipeline, better conversion, fewer wasted
leads.

| Service | Tier |
|---|---|
| Revenue Diagnostic | Diagnostic |
| Lead Intelligence Sprint | Sprint |
| Pilot Conversion Sprint | Pilot |
| Monthly RevOps OS | Retainer |

### Door 2 — Automate Operations
Outcome the buyer wants: less manual ops work, faster cycle time.

| Service | Tier |
|---|---|
| AI Quick Win Sprint | Sprint |
| Workflow Automation Sprint | Sprint |
| Executive Reporting Automation | Sprint |
| Monthly AI Ops | Retainer |

### Door 3 — Build Company Brain
Outcome the buyer wants: knowledge that answers questions and onboards
people.

| Service | Tier |
|---|---|
| Company Brain Sprint | Sprint |
| Sales Knowledge Assistant | Sprint |
| Policy Assistant | Sprint |
| Monthly Company Brain | Retainer |

### Door 4 — Serve Customers
Outcome the buyer wants: faster support, better tone, useful feedback
analysis.

| Service | Tier |
|---|---|
| AI Support Desk Sprint | Sprint |
| Inbox Operations Setup | Sprint |
| Feedback Intelligence | Sprint |
| Monthly Support AI | Retainer |

### Door 5 — Govern AI
Outcome the buyer wants: confidence that AI use is safe, compliant,
auditable.

| Service | Tier |
|---|---|
| AI Readiness Review | Diagnostic |
| AI Usage Policy | Sprint |
| PDPL-Aware Data Review | Sprint |
| AI Governance Program | Retainer |

## Rule of One

In every sales conversation, the proposal contains exactly one service.
The catalog is a menu only on the website. In the room, the founder
picks the one that fits the pain.

## Door Selection Heuristic

| Buyer signal | Door |
|---|---|
| "Our pipeline is small / unqualified" | Grow Revenue |
| "We waste hours on manual ops" | Automate Operations |
| "Our team can't find anything" | Build Company Brain |
| "Support is slow / inconsistent" | Serve Customers |
| "Compliance / legal blocked AI" | Govern AI |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Buyer pain signal | Door selection | Founder | Per conversation |
| Door selection | Single service in proposal | Founder | Per opportunity |
| Internal service set | Public catalog refresh | Founder | Quarterly |

## Metrics
- Door fit rate — % of proposals where buyer agreed the door was right.
- Single-service proposal rate — target 100%.
- Service close rate per door — conversion by door.
- Catalog cycle — quarters until door composition is reviewed.

## Related
- `docs/COMPANY_SERVICE_LADDER.md` — internal complete ladder.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing by tier and offer.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot tier reference design.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
