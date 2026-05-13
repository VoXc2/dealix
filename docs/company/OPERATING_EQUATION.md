# Operating Equation — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OPERATING_EQUATION_AR.md](./OPERATING_EQUATION_AR.md)

## Context
Every Dealix engagement runs through the same equation. The purpose of
this file is to make the equation explicit, so every offer, sprint,
delivery, and renewal can be traced through it. It plugs into the
operating model in `docs/DEALIX_OPERATING_CONSTITUTION.md`, the
strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, and the
execution discipline in `docs/company/EXECUTION_ENGINE.md`. If a
project skips a stage in this equation, it is treated as a process
defect and logged for review.

## The Equation
> Offer → Intake → Data Readiness → Governance Check → AI Output →
> QA Review → Delivery → Proof Pack → Capital Asset → Upsell →
> Productization

Each arrow is a hand-off with a defined input, a defined output, and a
named owner. Each stage has entry and exit criteria; see
`docs/delivery/DELIVERY_STANDARD.md` for the detailed runbook.

## Stage Definitions
| # | Stage | Definition | Owner |
|---|---|---|---|
| 1 | Offer | Productized service positioning and pricing | Founder / Revenue |
| 2 | Intake | Client problem, scope, success metric captured | Delivery lead |
| 3 | Data Readiness | Datasets scored against the data readiness standard | Data lead |
| 4 | Governance Check | Action class identified, rules evaluated | Governance lead |
| 5 | AI Output | Drafts produced by AI workforce under LLM Gateway | AI platform lead |
| 6 | QA Review | Bilingual quality + safety review against QA checklist | QA reviewer |
| 7 | Delivery | Approved output sent to client with hand-off note | Delivery lead |
| 8 | Proof Pack | Before/after evidence pack assembled | Delivery lead |
| 9 | Capital Asset | Reusable artifact (prompt, schema, playbook) registered | AI platform lead |
| 10 | Upsell | Renewal or expansion offer triggered from proof | Revenue |
| 11 | Productization | Repeated demand promoted to productized feature | Founder |

## Required Output From Every Project
Every Dealix project must produce all four of the following, or it is
not closed. Missing any one of them blocks invoicing and renewal
discussion.

1. **Cash now** — revenue collected against the signed scope.
2. **Proof for the next sale** — a sanitized proof pack suitable for
   the next client.
3. **Product or knowledge asset for future leverage** — a reusable
   asset entered into `docs/company/IP_REGISTRY.md`.
4. **Next offer for client expansion** — a renewal or upsell offer
   ready to send within seven days of delivery.

If any one is missing at closeout, the delivery lead opens a defect
ticket and the project is reviewed in the next weekly ops loop
(`docs/ops/DAILY_OPERATING_LOOP.md`).

## Closing The Loop
The equation is a loop, not a line. Capital Assets feed back into
Offer; Proof Packs feed back into Intake credibility; Productization
feeds back into the next Offer ladder iteration. The loop is
instrumented by the metrics below.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed scope | Stage gate checklist | Delivery lead | Per project |
| Data readiness score | Go / cleanup / no-go decision | Data lead | Per project |
| QA score | Delivery approval / rework | QA reviewer | Per delivery |
| Proof pack | Renewal proposal | Revenue | Within 7 days of delivery |
| Capital asset register | Productization candidate list | Founder | Monthly |

## Metrics
- **Equation completion rate** — projects that produce all four
  required outputs. Target: 100%.
- **Stage skip count** — number of projects that skipped a defined
  stage. Target: 0 per quarter.
- **Upsell within 30 days** — share of projects that produce a signed
  renewal or expansion within 30 days. Target: ≥ 60%.
- **Capital asset yield** — reusable assets registered per project.
  Target: ≥ 1 per project.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating rules cited by
  this equation.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan that
  this equation operationalizes.
- `docs/company/EXECUTION_ENGINE.md` — execution discipline that
  enforces this equation.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — operating
  system map.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
