# AI FinOps — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Finance Lead + Technical Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_FINOPS_AR.md](./AI_FINOPS_AR.md)

## Context
AI cost is the silent margin killer. It compounds invisibly across agents, prompts, and re-runs unless explicitly governed. Dealix runs an explicit FinOps discipline so that AI cost is always known per service, per client, per workflow, and so that cost optimization choices never quietly degrade quality. This file connects the cost-control playbook in `docs/COST_OPTIMIZATION.md`, the policy in `docs/V7_COST_CONTROL_POLICY.md`, and the margin model in `docs/UNIT_ECONOMICS_AND_MARGIN.md`.

## Purpose
The purpose of AI FinOps at Dealix is to control AI cost without hurting output quality. Cost cuts that break QA or eval thresholds are not allowed — they are deferred until a quality-preserving alternative is found.

## What we track
- Cost per **service** (Revenue, Customer, Operations, Knowledge, Data, Governance, Reporting).
- Cost per **client** (workspace).
- Cost per **AI run** by agent.
- Cost per **report** delivered.
- Cost per **proof pack** assembled.
- Cost per **workflow**.

For each metric we track absolute value, trend, and contribution to gross margin.

## Optimization levers
Allowed and active optimization levers, in priority order:

1. **Cache repeated outputs** when inputs are stable, with TTL aligned to data freshness.
2. **Route simple tasks to cheaper models** using the routing policy in `docs/AI_MODEL_ROUTING_STRATEGY.md`.
3. **Use stronger models for high-risk outputs** to avoid expensive rework and incidents.
4. **Reduce unnecessary context** — trim prompts, retrieve narrowly, avoid speculative tool calls.
5. **Batch when possible** — combine independent tasks within model and rate limits.

## Rules
- **Every service has an AI budget.** Budget is set at the offer/SKU level and tracked monthly.
- **Overruns require review.** A service exceeding budget by more than the configured threshold triggers a FinOps review with Council escalation if it persists.
- **Enterprise clients get AI cost reporting.** The Enterprise AI Report Card includes a Cost section by default for every enterprise account.
- **Cost cuts cannot break quality.** A change that lowers cost but drops eval pass rate below threshold is rolled back.

## Budget ladder
| Service Type | Default Budget Posture | Owner |
|---|---|---|
| Fixed-scope deliverable | Hard cap with alerting | Delivery Owner |
| Retainer service | Monthly soft cap + review on overrun | Delivery Owner |
| Enterprise control tower | Variable cap tied to active workflows | Finance + Delivery |
| Internal Dealix experiments | Sandbox cap with explicit owner | Technical Owner |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Token-level cost telemetry | Cost dashboards by service/client | Finance + Tech | Weekly |
| Eval scores + cost trends | Optimization or rollback decision | Tech + QA | Per change |
| Enterprise Report Card draft | Validated cost section | Finance | Monthly |

## Metrics
- Cost-per-Workflow — token cost / workflows executed.
- Cost-as-%-of-Service-Revenue — cost / billed revenue per service per month.
- Cache Hit Rate — % of eligible runs served from cache.
- Model-Routing Compliance — % of runs that obeyed the routing policy.
- Budget-Breach Count — count of service-month breaches per quarter.

## Related
- `docs/COST_OPTIMIZATION.md` — operational playbook for cost cuts
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — margin model FinOps feeds into
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
