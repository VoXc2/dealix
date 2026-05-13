# Cost Governance — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Finance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [COST_GOVERNANCE_AR.md](./COST_GOVERNANCE_AR.md)

## Context
AI cost is a real cost of goods. Without governance, model spend
expands silently and erodes the unit economics that the company is
sized against. This file defines how Dealix tracks, budgets, and
optimises AI cost, extending `docs/COST_OPTIMIZATION.md`, executing on
the policy in `docs/V7_COST_CONTROL_POLICY.md`, and feeding the unit
economics in `docs/UNIT_ECONOMICS_AND_MARGIN.md`.

## Principle
> AI cost is treated like a controllable cost of goods sold. Every
> client-facing run has a budget, an owner, and a route to optimise.

## What We Track
AI cost is tracked per:

- **Project** — total AI cost for the engagement.
- **Service** — running average and budget per service package.
- **Client** — cumulative AI cost per client per month.
- **Report** — cost to produce each management report.
- **Proof pack** — cost to produce a delivery proof pack.

Source data comes from the AI Run Ledger (`AI_RUN_LEDGER.md`), priced
in SAR.

## Rules
- **Budgets per service.** Every service has an AI budget; running
  beyond budget triggers a review.
- **Expensive models need a reason.** Calls to the top-cost model class
  must be justified by risk class or by report importance.
- **Cache or optimise repeats.** Prompts called repeatedly with similar
  inputs must be cached or refactored.
- **Cheaper models for low-risk classification.** Routing follows
  `docs/AI_MODEL_ROUTING_STRATEGY.md`.
- **Stronger models for executive reports.** Reports going to client
  C-suite may use higher-cost models.

## Budgets (per Service, SAR per Sprint)
- **Lead Intelligence** — 50 to 200.
- **Company Brain** — 200 to 800.
- **AI Quick Win** — 50 to 300.
- **Support Desk** — 100 to 500.

Overruns trigger a prompt/model/workflow review and an entry in
`docs/COST_OPTIMIZATION.md` as a candidate optimisation.

## Optimisation Loop
1. **Detect.** Weekly review flags services trending over budget.
2. **Diagnose.** Identify whether the cause is prompt design, model
   choice, repeated calls, or scope creep.
3. **Fix.** Land a prompt update, routing change, caching layer, or
   scope re-negotiation.
4. **Verify.** Re-run cost report for the next 14 days; confirm
   return to budget.

## Cost vs. Quality Trade-off
- A cheaper model may be used only if it passes the relevant evals in
  `EVALUATION_REGISTRY.md`.
- A more expensive model is justified when claims-safety or governance
  evals require it.
- Quality regressions caused by cost-driven model swaps are treated
  as incidents.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI Run Ledger (cost rows) | Cost-per-project/service/client reports | Finance Lead | Weekly |
| Budget definitions | Service budget cards | Founder | Quarterly |
| Cost incidents | Optimisation backlog | Founder, Delivery Lead | Per incident |

## Metrics
- **Budget Conformance** — share of projects within service budget
  (target ≥ 90%).
- **Cost per Sprint (SAR)** — median AI cost per Sprint per service
  (track vs. budget bands above).
- **Optimisation Yield** — SAR saved per month from optimisations
  (target ≥ 10% of baseline AI spend by month 6).
- **Cost-Quality Incidents** — count of quality incidents caused by
  cost-driven model changes (target = 0).

## Related
- `docs/COST_OPTIMIZATION.md` — backlog and patterns for cost
  optimisations.
- `docs/V7_COST_CONTROL_POLICY.md` — policy this file executes against.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics consuming these
  numbers.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing layer used to control
  cost.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
