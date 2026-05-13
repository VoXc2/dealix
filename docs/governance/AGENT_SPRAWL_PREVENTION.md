# Agent Sprawl Prevention — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AGENT_SPRAWL_PREVENTION_AR.md](./AGENT_SPRAWL_PREVENTION_AR.md)

## Context
The fastest way to destroy enterprise trust — and Dealix margin — is to let agents multiply unchecked. Shadow agents, duplicated agents, dormant agents holding wide data access, and agents that no one owns are how AI programs go from "transformational" to "audit finding". This file defines the controls Dealix uses to keep the agent inventory clean, useful, and audit-defensible. It enforces the operating principles in `docs/DEALIX_OPERATING_CONSTITUTION.md` and supports the eval and stack discipline in `docs/AI_STACK_DECISIONS.md` and `docs/EVALS_RUNBOOK.md`.

## Sprawl risks
The risks Dealix actively guards against:

1. **Duplicate agents** — two agents doing essentially the same job, drifting in different directions.
2. **Unused agents** — agents that never run but still hold permissions and incur platform overhead.
3. **Agents with excessive data access** — broad scopes inherited from convenience rather than need.
4. **Agents without owners** — no Dealix role accountable; impossible to govern.
5. **Agents exceeding scope** — silent expansion of capability beyond what was approved.
6. **Hidden AI cost** — agents running outside FinOps visibility, consuming tokens off-budget.
7. **Inconsistent outputs** — different agents producing different answers for the same question to the same client.

## Eight controls
The controls are mutually reinforcing — together they keep the inventory clean.

1. **Central agent inventory** — single source of truth for every agent across every workspace.
2. **Owner for every agent** — no entry exists in the inventory without a named owner.
3. **Autonomy classification** — every agent has its autonomy level recorded and reviewed.
4. **Approved tools only** — agents may only invoke tools on the approved tool list.
5. **Data access limits** — least-privilege data scopes; no agent inherits broad workspace access by default.
6. **Monitoring** — runs, costs, errors, eval scores tracked per agent.
7. **Retirement process** — explicit lifecycle path with named approver.
8. **Cost review** — monthly cost-per-agent review against expected workflow value.

## Hard rule
**No agent exists outside the inventory.** Any agent caught running without an inventory entry is suspended pending registration. Any inventory entry that fails the monthly review (no use, no owner, no value) is retired.

## Monthly Agent Review
Every month the Governance Council walks the inventory using the following table:

| Agent | Used? | QA | Cost | Incidents | Decision |
|---|---|---|---|---|---|
| RevenueAgent | Yes | 92 | $$ | 0 | Keep |
| OutreachAgent | Yes | 88 | $$ | 1 | Keep, fix prompt |
| ComplianceGuardAgent | Yes | 95 | $ | 0 | Keep |
| LegacyCRMSyncAgent | No | n/a | $ | 0 | Retire |

`Used?` = had at least one production run in the last 30 days. `QA` = average QA score. `Cost` = relative monthly token cost band. `Incidents` = count of governance incidents.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Inventory feed, run logs, cost data | Monthly Agent Review table | Governance Reviewer | Monthly |
| Sprawl alerts (duplicate / unused / over-scoped) | Suspension, scope reduction, or retirement | Council | Within 7 days |
| Agent registration requests | Inventory entry or rejection | Governance + Technical | Per request |

## Metrics
- Inventory Completeness — % of running agents with an inventory entry (must be 100%).
- Owner Coverage — % of inventory entries with named owner (must be 100%).
- Dormant-Agent Count — agents with no runs in 30 days still listed as active.
- Cost-per-Active-Agent — monthly token cost divided by count of agents with ≥1 run.

## Related
- `docs/AI_STACK_DECISIONS.md` — approved stack tools the inventory enforces
- `docs/EVALS_RUNBOOK.md` — eval cadence feeding the review
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution behind the no-sprawl rule
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
