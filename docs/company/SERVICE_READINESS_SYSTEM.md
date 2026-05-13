# Service Readiness System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** COO / Service Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SERVICE_READINESS_SYSTEM_AR.md](./SERVICE_READINESS_SYSTEM_AR.md)

## Context

A service we cannot deliver predictably is not a service — it is a
liability. The Service Readiness System scores every Dealix service
against a fixed 100-point rubric and assigns one of four selling
statuses. This document operationalizes the strategic guardrail in
`docs/DEALIX_OPERATING_CONSTITUTION.md` ("nothing is sold before it
is ready to ship") and complements the readiness scorecard in
`docs/company/SERVICE_READINESS_BOARD.md`. The CEO uses this monthly
to decide which offers are public, which are pilot-only, and which
must be removed from the website.

## The 100-Point Rubric

Every service is scored on ten weighted areas totaling 100 points.

| Area | Points | What we score |
|---|---:|---|
| Clear buyer | 10 | The role, industry, and company size are written. |
| Clear problem | 10 | The problem the buyer feels in plain language. |
| Clear outcome | 10 | The measurable change after delivery. |
| Clear scope | 10 | Included and excluded boundaries with examples. |
| Intake form | 10 | A repeatable form that gathers all required inputs. |
| Delivery checklist | 10 | A documented step-by-step delivery flow. |
| QA checklist | 10 | A gate aligned with `docs/quality/QA_SYSTEM.md`. |
| Product module support | 15 | Reusable modules (templates, prompts, evals) exist. |
| Governance rules | 10 | Approvals, forbidden actions, PDPL notes. |
| Upsell path | 5 | Clear retainer or expansion path. |
| **Total** | **100** | |

Scoring rules:

- Each area is scored 0, 50%, or 100% of its weight. No fractional
  scores between those bands.
- Reviewer must cite the document or asset proving the score (link or
  path).
- Disputed scores are resolved by the COO.

## Status Thresholds

| Score | Status | What the company is allowed to do |
|---|---|---|
| 85-100 | **Sellable** | Publish on website, run ads, send proposals, accept new clients at standard pricing. |
| 70-84 | **Paid Pilot** | Sell carefully with limited scope, manual oversight, capped engagements/month, pilot pricing. |
| 50-69 | **Demo / Internal** | Show in demos and customer success conversations but do not sell yet. |
| <50 | **Idea** | Document only, do not show externally, prove value internally first. |

Promotion rules:

- A service moves up only after re-scoring (no informal promotion).
- A "Paid Pilot" service that runs three consecutive successful
  engagements with QA pass earns a re-score for "Sellable".
- A "Sellable" service that misses QA twice in a quarter is
  automatically downgraded to "Paid Pilot" pending root-cause fix.

## Example Service Readiness Table

| Service | Buyer | Problem | Outcome | Scope | Intake | Delivery | QA | Modules | Gov | Upsell | Score | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Lead Intelligence Sprint | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 15 | 10 | 5 | **100** | Sellable |
| AI Quick Win Sprint | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 5 | **95** | Sellable |
| Company Brain Sprint | 10 | 10 | 10 | 10 | 10 | 5 | 10 | 10 | 10 | 5 | **90** | Sellable |
| Arabic Support AI Pilot | 10 | 10 | 10 | 10 | 5 | 5 | 10 | 5 | 10 | 5 | **80** | Paid Pilot |
| Enterprise Governance Audit | 10 | 10 | 5 | 5 | 5 | 5 | 5 | 0 | 10 | 0 | **55** | Demo / Internal |

The Service Readiness Board (`docs/company/SERVICE_READINESS_BOARD.md`)
is the live tracker; this doc defines the system behind it.

## Review Cadence

- **Weekly** — each Service Owner updates their service's row when
  any column changes.
- **Monthly** — COO reviews all rows, signs off promotions and
  demotions.
- **Quarterly** — CEO removes any service that has been stuck in
  Idea/Demo for two consecutive quarters.

## What Failure Looks Like

A service that scores 65 but is being sold on the website is the
single most damaging operational failure for Dealix: it generates
revenue we cannot reliably deliver, burns founder hours, breaks the
proof model, and erodes Trust Capital. The COO has standing
authority to pull such a service from public surfaces within 24
hours.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Service collateral, delivery logs, QA results, governance docs | Readiness scores, sellability status | COO + Service Owners | Weekly / Monthly |
| Pricing engine inputs | Approved offers list | CEO | Monthly |
| Productization ledger | Product module support score | CTO | Monthly |

## Metrics

- **# services at "Sellable"** — target ≥3 (the top 3 offers).
- **# services at "Paid Pilot"** — target ≤3 (pipeline of next ready).
- **# services stuck at <70 for >2 quarters** — target 0.
- **Demotion rate** — target ≤1/quarter (signal of overselling).

## Related

- `docs/COMPANY_SERVICE_LADDER.md` — service ladder.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing pairs to readiness.
- `docs/company/SERVICE_READINESS_BOARD.md` — live tracker sibling.
- `docs/company/SERVICE_READINESS_SCORE.md` — score detail sibling.
- `docs/company/SERVICE_CATALOG_V1.md` — service catalog.
- `docs/company/DEALIX_CEO_STRATEGY.md` — umbrella strategy.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
