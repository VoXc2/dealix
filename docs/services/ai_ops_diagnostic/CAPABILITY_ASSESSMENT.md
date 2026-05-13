# Capability Assessment — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Diagnostic Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_ASSESSMENT_AR.md](./CAPABILITY_ASSESSMENT_AR.md)

## Context
The Capability Assessment is the structured output of the AI Ops
Diagnostic. It scores all seven Dealix capabilities for one client,
ties evidence to each score, and recommends a single first service.
It is the canonical input to the Layer-4 Capability Factory and the
artefact that turns a client conversation into a priced Sprint. The
assessment grid is referenced by `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`
as the pre-engagement gate, and the levels follow
`docs/company/CAPABILITY_MATURITY_MODEL.md`.

## Pre-Project Assessment Grid
Filled once per client during the AI Ops Diagnostic.

| Capability | Current Level | Target Level | Evidence | Recommended Service |
|---|---:|---:|---|---|
| Revenue | 1 | 3 | leads in spreadsheet | Lead Intelligence Sprint |
| Customer | 1 | 3 | WhatsApp overload | AI Support Desk |
| Operations | 0 | 2 | no workflow map | AI Quick Win |
| Knowledge | 1 | 3 | files scattered | Company Brain |
| Data | 1 | 3 | duplicates/missing fields | Data Cleanup |
| Governance | 0 | 2 | no AI policy | AI Readiness Review |
| Reporting | 1 | 3 | manual reports | Executive Reporting |

The numbers above are an example, not a default. Real assessments must
record concrete artefacts, names, and dates in the Evidence column.

## How to Fill the Grid
- **Current Level** uses the evidence rules in
  `CAPABILITY_MATURITY_MODEL.md` (Required evidence column). No
  evidence ⇒ score one level down.
- **Target Level** is the level we promise to reach in the next Sprint
  or Pilot. Never skip more than 2 levels in one engagement.
- **Evidence** is a one-line factual observation, with a date or
  artefact pointer.
- **Recommended Service** comes from
  `docs/COMPANY_SERVICE_LADDER.md` and must respect the service's
  declared min/max starting and target levels.

## Decision Rule
For each engagement, pick the row where:

> highest (Target − Current) gap × business value × (1 − risk) wins.

Plain rule: **highest gap + highest value + lowest risk = first
Sprint.** The runner-up row becomes Sprint #2 on the 30-day roadmap.

## Output Artefacts
- Capability Assessment grid (this file, per client).
- A short justification per recommendation (3–5 sentences).
- A 30-day roadmap drawn from the top three rows.
- An optional governance memo if any row has unacceptable risk.
- A SAR-denominated proposal for the recommended first Sprint, taken
  from `docs/OFFER_LADDER_AND_PRICING.md`.

## Quality Checks
- Every row must have an Evidence entry; "unknown" is not allowed.
- Every Recommended Service must exist in the service ladder.
- No row may target Level 5 from a starting point below Level 3.
- Governance Capability target must be ≥ 2 before any external-action
  Sprint can be proposed (see `AI_ACTION_TAXONOMY.md`).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client interviews, data samples, process walkthroughs | Capability Assessment grid, recommended Sprint | Diagnostic Lead | Per engagement |
| Assessment grid | Sprint proposal, 30-day roadmap | Founder, Delivery Lead | Per engagement |
| Delivered Sprint outcomes | Updated current-level evidence | Delivery Lead | Per delivery |

## Metrics
- **Assessment Accuracy** — share of assessments where the post-Sprint
  current level matches the predicted target (target ≥ 85%).
- **Recommendation Acceptance** — share of clients who buy the
  recommended first Sprint (target ≥ 60%).
- **Risk Block Rate** — share of assessments where governance risk
  forced a readiness service first (tracked, not bounded).
- **Time-to-Assessment** — calendar days from kickoff to signed grid
  (target ≤ 5 days).

## Related
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing the assessment feeds
  into.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot scoped from the
  assessment.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — how the assessment fits
  the 90-day plan.
- `docs/services/ai_ops_diagnostic/offer.md` — parent offer of this
  assessment.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
