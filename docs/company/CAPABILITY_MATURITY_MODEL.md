# Capability Maturity Model — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_MATURITY_MODEL_AR.md](./CAPABILITY_MATURITY_MODEL_AR.md)

## Context
Once the seven capabilities exist (see `CAPABILITY_OPERATING_MODEL.md`),
Dealix needs a single, sales-grade language to describe where a client
sits today and where each Sprint will take them. The Capability
Maturity Model gives every capability a score from 0 to 5. This is the
ladder referenced by `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and by
`docs/DEALIX_OPERATING_CONSTITUTION.md` as the canonical way to scope,
price, and prove engagements. It is also the input that the Layer-4
Capability Factory consumes to schedule capability work.

## The 0–5 Levels
Each client capability is scored 0–5:

- **Level 0 — Absent.** No process, no data, no owner, no metric.
- **Level 1 — Manual.** Work is manual and inconsistent.
- **Level 2 — Structured.** Process, owner, and inputs are documented.
- **Level 3 — AI-Assisted.** AI helps with drafts, reports, scoring,
  summaries; humans remain in the loop.
- **Level 4 — Governed AI Workflow.** AI is embedded with approvals, QA,
  logs, and measurement.
- **Level 5 — Optimized Operating System.** Recurring, measured,
  improved, partially self-serve.

The same five levels apply to every one of the seven capabilities,
which keeps the language consistent across Sales, Delivery, QA, and
Customer Success.

## Worked Example — Revenue Capability
- **L0 — Absent:** leads scattered across inboxes and WhatsApp.
- **L1 — Manual:** manual follow-up on a personal list.
- **L2 — Structured:** pipeline stages documented in a CRM.
- **L3 — AI-Assisted:** AI scores accounts and drafts outreach for human
  review.
- **L4 — Governed:** scoring + approvals + reports + CRM hygiene with
  audit and eval.
- **L5 — Optimised:** monthly AI RevOps OS with dashboard, proof pack,
  and continuous optimisation.

Sales line used in client conversations:
> "We raise your Revenue Capability from L1 to L3 in one Sprint, then to
> L4 in Pilot."

This template applies to every capability — only the L0…L5 evidence
changes.

## Scoring Method
Scoring is evidence-based, not opinion-based. To claim a level the
client must show at least one artefact:

| Level | Required evidence |
|---|---|
| L0 | None — the absence itself is the evidence. |
| L1 | Named person doing the work + a recent example. |
| L2 | A document describing the process + a named owner. |
| L3 | Working AI assist on real cases + screenshots of outputs. |
| L4 | Approval log + QA review + governance event trail. |
| L5 | Recurring report + cost ledger + improvement loop. |

Scores are captured by the AI Ops Diagnostic and stored in the
`capability_scores` table (see `ADVANCED_DATA_MODEL.md`).

## Factory Application
This section is the anchor used by Layer-4 (Capability Factory) files
and by automation that schedules capability work.

- **Capability Factory input:** for each engagement, the Factory reads
  the current and target levels per capability from
  `CAPABILITY_ASSESSMENT.md` and turns them into a Sprint plan.
- **Service mapping:** services in `COMPANY_SERVICE_LADDER.md` declare
  the minimum starting level they accept and the maximum target level
  they can deliver. The Factory uses this to choose the right service.
- **QA gates:** every level transition has a fixed checklist
  (governance, eval, proof). The Factory will not mark a level as
  achieved until all checklist items have passed.
- **Roadmap generation:** the Factory generates a 90-day capability
  roadmap by stacking level transitions across capabilities, respecting
  data-readiness prerequisites from
  `docs/services/data_readiness_assessment/scoring_model.md`.
- **Anchor links:** Layer-4 files reference this section directly as
  `CAPABILITY_MATURITY_MODEL.md#factory-application` so that future
  edits to the Factory pipeline can rely on a stable contract.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Capability Assessment per client | Current/target level matrix | Diagnostic Lead | Per engagement |
| Sprint and Pilot outcomes | Updated level evidence, level transitions | Delivery Lead, QA Lead | Per delivery |
| Portfolio of clients | Capability ladder distribution across book of business | Founder | Monthly |

## Metrics
- **Average Capability Level (per client)** — mean of the seven
  capability levels (target +1 level per quarter for active clients).
- **Level Transition Rate** — share of declared level transitions that
  pass the evidence checklist (target ≥ 90%).
- **Time-to-L3** — median days to move a capability from L1 to L3
  (target ≤ 30 days).
- **L4 Coverage** — percentage of active clients with at least one
  capability at L4 (target ≥ 60% by month 12).

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — capability ladder
  positioning at company level.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating rules each level
  must satisfy.
- `docs/COMPANY_SERVICE_LADDER.md` — services mapped onto level
  transitions.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability the Factory uses
  to verify L3 and L4 claims.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
