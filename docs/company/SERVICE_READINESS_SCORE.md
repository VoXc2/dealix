# Service Readiness Score — The Scoring Model

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SERVICE_READINESS_SCORE_AR.md](./SERVICE_READINESS_SCORE_AR.md)

## Context
This is the *scoring model* that decides whether a service is ready
to be sold. It is distinct from the Master Blueprint's
`SERVICE_READINESS_BOARD` (which tracks a portfolio of services); this
file is the rubric. Every service gets a score before it gets a price,
and that score governs how it may be sold. It plugs into the operating
doctrine in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the service
ladder in `docs/COMPANY_SERVICE_LADDER.md`.

## The Rubric (100 points)

| Area | Points |
|---|---:|
| Clear offer | 10 |
| Clear price | 10 |
| Intake form | 10 |
| Scope template | 10 |
| Delivery checklist | 10 |
| Product module | 15 |
| QA checklist | 15 |
| Report template | 10 |
| Governance rules | 10 |
| Upsell path | 10 |
| **Total** | **100** |

## Rubric Definitions

- **Clear offer (10)** — a one-sentence description of who it is for,
  what they get, and what changes for them.
- **Clear price (10)** — published or stable internal price band; no
  per-conversation pricing.
- **Intake form (10)** — a written intake template that captures
  everything needed before kickoff.
- **Scope template (10)** — a reusable SOW with deliverables, dates,
  exclusions.
- **Delivery checklist (10)** — step-by-step delivery procedure.
- **Product module (15)** — at least one reusable code, prompt, or
  data module that backs the service.
- **QA checklist (15)** — pre-handoff quality gate with named
  reviewer.
- **Report template (10)** — the report the buyer receives, in
  template form.
- **Governance rules (10)** — PDPL / policy / data-handling rules for
  the service.
- **Upsell path (10)** — the named next step on the ladder for a
  satisfied buyer.

## Thresholds

| Score | Selling status |
|---|---|
| 80+ | Sell publicly. Listed on website. |
| 70 - 79 | Paid pilot only. Not on public catalog. |
| 50 - 69 | Demo or internal only. No price quoted externally. |
| < 50 | Do not sell. Internal R&D. |

## How a Service Climbs

A service starts at < 50 (concept). It climbs by closing the named
gaps. The fastest gains usually come from:

1. Writing the intake form (10).
2. Writing the scope template (10).
3. Building the first product module (15).
4. Writing the QA checklist (15).

Doing those four moves a service from concept (≈ 30) to demo-ready
(≈ 80).

## Scoring Cadence

- Score is reviewed monthly per active service.
- A service's score may only be raised when the evidence (intake
  doc, SOW template, etc.) exists and is linked.
- Score regressions (e.g., a module was removed) require founder sign-off.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Service portfolio | Score per service | Founder | Monthly |
| Score per service | Selling status | Founder | Monthly |
| Selling-status changes | Website / catalog update | Founder | Monthly |

## Metrics
- Services at 80+ — count.
- Average portfolio score.
- Time to reach 80 — average months from concept to sellable.
- Regression count — services whose score dropped in the period.

## Related
- `docs/COMPANY_SERVICE_LADDER.md` — the ladder of services this rubric scores.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing reference once a service is sellable.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan that depends on this gate.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
