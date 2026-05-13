# Offer Ladder — Internal Tier Framework

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OFFER_LADDER_AR.md](./OFFER_LADDER_AR.md)

## Context
This file is the *internal* tier framework — the shape of how Dealix
takes a buyer from clarity to scale. It is distinct from
`docs/OFFER_LADDER.md` (the public/commercial pricing surface) and from
`docs/OFFER_LADDER_AND_PRICING.md` (the line-item commercial catalog).
The internal ladder enforces the discipline that no buyer skips a rung
without justified cause: a Diagnostic precedes a Sprint, a Sprint
precedes a Pilot, and so on. It plugs into the operating doctrine in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and L7 execution.

## The Five Tiers

| Tier | Price (SAR) | Purpose | Time to value |
|---|---|---|---|
| Diagnostic | 3.5k - 7.5k | Clarity | 1-2 weeks |
| Sprint | 7.5k - 25k | First proof | 2-4 weeks |
| Pilot | 22k - 60k | Operational validation | 4-8 weeks |
| Retainer | 8k - 60k / month | Continuity | Ongoing |
| Enterprise | 85k - 300k+ | Scale | Multi-quarter |

### Diagnostic (SAR 3.5k - 7.5k)
- Revenue Diagnostic.
- AI Ops Diagnostic.
- Data Readiness Assessment.

Purpose: clarity. Buyer leaves with a written diagnosis and a
recommended next rung. Never sell a Sprint to a buyer that has not
shown they can afford and absorb a Diagnostic.

### Sprint (SAR 7.5k - 25k)
- Lead Intelligence Sprint.
- AI Quick Win Sprint.
- Company Brain Sprint.

Purpose: first proof. Tight scope, fixed price, 2-4 weeks, one
artifact, one decision.

### Pilot (SAR 22k - 60k)
- Pilot Conversion.
- Workflow Pilot.
- Support Desk Pilot.

Purpose: operational validation. Tests the work inside the client's
real environment with light governance.

### Retainer (SAR 8k - 60k / month)
- Monthly RevOps OS.
- Monthly AI Ops.
- Monthly Company Brain.

Purpose: continuity. Each retainer must replace at least one manual
process and produce a monthly proof artifact.

### Enterprise (SAR 85k - 300k+)
- Enterprise AI OS.
- Governed AI Operations Platform.

Purpose: scale. Eligible only after at least 2 retainers have been run
for ≥ 6 months with QA ≥ 85 and zero PII incidents.

## Ladder Discipline

- Skipping a rung is allowed only when the buyer brings their own
  diagnostic and the founder signs off in writing.
- Discounting downward is allowed; price ceilings are not.
- A buyer may not be on two rungs simultaneously inside the same
  vertical without an explicit expansion plan.

## Relationship to Other Ladder Files

| File | Purpose | Source of truth for |
|---|---|---|
| `docs/OFFER_LADDER.md` | Public/commercial pricing | What we publish to buyers |
| `docs/OFFER_LADDER_AND_PRICING.md` | Line-item commercial catalog | Proposal generation |
| `docs/company/OFFER_LADDER.md` (this) | Internal tier framework | Sales sequencing discipline |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Buyer state (clarity / value / scale) | Tier recommendation | Founder | Per conversation |
| Tier recommendation | Service from `SERVICE_CATALOG_V1` | Founder | Per proposal |
| Retainer performance | Enterprise eligibility decision | Founder | Quarterly |

## Metrics
- Tier-to-tier conversion — % moving Diagnostic → Sprint → Pilot.
- Average revenue per buyer — sum across tiers.
- Skip-rung exceptions — count per quarter (target ≤ 1).
- Time on ladder — months from Diagnostic to Retainer.

## Related
- `docs/OFFER_LADDER.md` — public pricing surface this internal ladder is gated by.
- `docs/OFFER_LADDER_AND_PRICING.md` — line-item commercial catalog.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot tier reference design.
- `docs/COMPANY_SERVICE_LADDER.md` — full internal service ladder.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
