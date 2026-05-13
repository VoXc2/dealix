# AI Workforce Operating Model — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_WORKFORCE_OPERATING_MODEL_AR.md](./AI_WORKFORCE_OPERATING_MODEL_AR.md)

## Context
Dealix uses AI agents to deliver value at scale. To preserve quality and
trust, those agents must be operated like governed workers — not free-form
autonomous employees. This file defines the agent taxonomy, the mandatory
contract every agent honors, and how the workforce plugs into the delivery
flow described in `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` and the model
routing in `docs/AI_MODEL_ROUTING_STRATEGY.md`. It is enforced by the rules
in `docs/DEALIX_OPERATING_CONSTITUTION.md` and the controls in
`docs/AI_STACK_DECISIONS.md`.

## Principle

> AI agents in Dealix are **not autonomous employees**; they are governed
> workers inside controlled workflows.

Autonomy is granted by class of action, not by agent. Reading, drafting,
classifying, recommending — broadly allowed. Sending, publishing, or
acting on external systems — gated, approved, logged.

## Agent types

1. **Analyst Agents** — analyze data, classify, summarize, score.
2. **Drafting Agents** — create drafts, reports, scripts, recommendations.
3. **Retrieval Agents** — search knowledge and answer with sources.
4. **Workflow Agents** — move tasks through defined workflows.
5. **Guardrail Agents** — check safety, claims, PII, policy.
6. **Reporting Agents** — generate reports and proof packs.

Each instance of an agent (a *card*) lives in
`docs/product/agent_cards/`. A new agent is not allowed in production
without a card.

## Mandatory agent contract

Every agent — regardless of type — declares:

- **Role** — one-sentence purpose.
- **Allowed Tools** — explicit toolset whitelist.
- **Forbidden Actions** — explicit blacklist (sending, scraping, external
  writes, etc.).
- **Input Schema** — validated structure of inputs.
- **Output Schema** — validated structure of outputs.
- **QA Requirement** — eval, rubric, or check before delivery.
- **Approval Requirement** — where on the Human-in-the-Loop matrix it sits.
- **Audit Log** — every run, prompt version, cost, and output is recorded.

## Lifecycle

```
design → card → eval → pilot → promote → monitor → retire
```

1. **Design** — sketch role, IO schema, risk class.
2. **Card** — write the agent card.
3. **Eval** — run eval suite from `docs/EVALS_RUNBOOK.md`.
4. **Pilot** — limited use under heavy review.
5. **Promote** — formally allowed in workflow.
6. **Monitor** — Control Tower watches behavior and cost.
7. **Retire** — deprecated when superseded or stale.

## Workforce composition (target MVP)

| Agent | Type | Risk class |
|---|---|---|
| Data Quality Agent | Analyst | Medium |
| Revenue Agent | Analyst / Workflow | Medium |
| Outreach Agent | Drafting | High |
| Knowledge Agent | Retrieval | Medium |
| Reporting Agent | Reporting | Medium |
| Compliance Guard Agent | Guardrail | Critical |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement workflow | Routed agent runs | Workflow Agent | Per task |
| Agent run log | Cost + QA telemetry | Control Tower | Continuous |
| Eval suite | Agent promotion decision | Head of AI | Per agent change |
| Guardrail decisions | Action allow/block | Compliance Guard Agent | Per action |

## Metrics
- Agent QA Pass Rate — % of runs passing eval thresholds.
- Cost per Run — average cost per agent invocation by tier.
- Forbidden Action Attempts — blocked attempts by guardrails.
- Approval Latency — median wait for human approval where required.

## Related
- `docs/AI_STACK_DECISIONS.md` — model and infra decisions
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing strategy
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — workflow runtime
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — rules enforced here
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
