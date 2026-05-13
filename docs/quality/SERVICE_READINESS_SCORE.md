---
title: Service Readiness Score — 80/100 Floor to Sell a Service Officially
doc_id: W6.T37.service-readiness
owner: HoP
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T37, W6.T33, W6.T34]
kpi:
  metric: services_at_or_above_80_score
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: quality-foundation
---

# Service Readiness Score

## 1. Context

Before Dealix officially sells a service, that service is graded against a
100-point readiness rubric. **A service can be sold only at score ≥ 80.**
Below 80 the service is *beta only* — internal pilots or selected design
partners, with the score gap disclosed to the customer.

This rubric is part of the four Readiness Gates in
[`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
§5.1 (Service Readiness Score). This file is the operator-friendly summary.

## 2. Audience

HoP (rubric owner), HoCS (consumer — won't book a project for a sub-80
service), CRO (won't quote it commercially), CEO (ratifies promotion to
sellable).

## 3. The Rubric

| # | Criterion | Weight | What "ready" looks like |
|---|-----------|------:|-------------------------|
| 1 | Clear offer + price | 10 | Public offer page; SAR price; included scope, excluded scope |
| 2 | Intake form ready | 10 | Customer intake captures every input the build needs |
| 3 | Scope template ready | 10 | Standard SOW with included + out-of-scope lists |
| 4 | Supporting module/tool | 15 | The OS module that powers it is in production, not a spike |
| 5 | Report template ready | 10 | Executive artifact template tested with a real run |
| 6 | QA checklist ready | 15 | 5 gates + question bank covers this offering |
| 7 | Demo / sample output | 10 | Runnable demo with sample data; ≤ 30-minute walkthrough |
| 8 | Compliance checks defined | 10 | PDPL, PII, forbidden-claims gates wired in |
| 9 | Upsell path defined | 10 | Stage 8 (Expand) anchor proposal exists |
| | **Total** | **100** | Sell at ≥ 80; beta below |

## 4. Operating Rule

- **Score ≥ 80**: service appears in the catalog with a price and is sold
  freely. AE can quote without HoP approval per deal.
- **Score 60–79**: beta-only. HoP signs off on every deal. The score gap is
  disclosed to the buyer in writing.
- **Score < 60**: no commercial sale. Internal pilots and design partners
  only.

## 5. How Scoring Happens

Every quarter (and on demand when a service changes materially), HoP runs
the rubric in a 30-minute review with HoCS + CTO. Score is published in
[`../product/MODULE_MAP.md`](../product/MODULE_MAP.md) (column: readiness).
The "Build only after repetition" rule
([`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
§7) gates promoting criteria 4 (module) and 7 (demo).

## 6. The "Two Customers Test"

A separate sanity check overlaid on the rubric: the same service must be
deliverable to two different customers within the documented timebox at
the same QA score. If the second delivery scored materially lower or ran
over time, the rubric is re-checked and the service may be demoted to
beta until the gap is fixed.

## 7. Anti-Patterns

- **Sales-led promotion**: AE pushing a sub-80 service into the catalog
  because a deal is hot. The score gates the catalog, not the deal.
- **Documentation as completion**: writing the templates without testing
  them in a real run. Criteria 5 and 7 require *tested* artifacts.
- **One-off elevations**: scoring a service 80 because the only delivery
  went well. Two-customer evidence is the test.

## 8. Cross-links

- Canonical model: [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
- Quality Standard: [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)
- Module map: [`../product/MODULE_MAP.md`](../product/MODULE_MAP.md)
- Service catalog: [`../strategy/service_portfolio_catalog.md`](../strategy/service_portfolio_catalog.md)

## 9. Owner & Review Cadence

- **Owner**: HoP.
- **Review**: quarterly score refresh; ad-hoc on material service change.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoP | Initial 80/100 rubric summary |
