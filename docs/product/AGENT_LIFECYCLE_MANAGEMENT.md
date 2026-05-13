# Agent Lifecycle Management

> Every AI agent in Dealix moves through eight stages. No agent enters
> production without an Agent Card, a passing eval, and a clean
> governance check. The lifecycle is the antidote to Gartner's
> "agent sprawl" — agents are born, monitored, and retired on purpose.

## The lifecycle stages

```
Proposed → Designed → Simulated → Evaluated → Approved
        → Monitored → Improved → Retired
```

| Stage | Definition | Entry artifact | Exit gate |
|-------|------------|----------------|-----------|
| Proposed | A capability gap is identified; an agent is suggested | One-page proposal in `docs/product/agent_proposals/` | CRO + HoP sign |
| Designed | Agent Card written: scope, tools, data, autonomy, risk | `docs/product/agent_cards/<agent>.md` | HoLegal reviews scope |
| Simulated | Dry-run against staging fixtures with prompt + schema | Sim log in `evals/sim/` | No Hard Fail on safety / claim / PII |
| Evaluated | At least one eval in `EVALUATION_REGISTRY.md` active | Eval ID + dataset | Eval passes threshold |
| Approved | Production promotion approved | Decision logged in Decision Ledger | CTO + HoLegal co-sign |
| Monitored | Live in production with Control Tower visibility | Dashboard tile + alert routing | 30 days stable |
| Improved | Iteration loop: prompt / model / dataset updates | Bumped prompt version in `PROMPT_REGISTRY.md` | Eval re-passes after change |
| Retired | Agent removed from production routing | Retirement note in Decision Ledger | Replacement (or "not needed") declared |

## Hard rule (the gate)

```
No agent runs in production without ALL of:
  1. Agent Card in docs/product/agent_cards/<agent>.md
  2. At least one Active eval in EVALUATION_REGISTRY.md at or above threshold
  3. Clean governance pass (no open Hard Fail in dealix/trust/policy.py for this agent)
  4. Owner role assigned (HoData / HoP / CRO / HoLegal / HoCS)
  5. Prompt version pinned (PROMPT_REGISTRY.md row in MVP/Production status)
```

A merge that introduces an agent without all five is rejected at review.

## Triggers for moving stages

- Proposed → Designed: capability not covered by existing agents in
  `AI_AGENT_INVENTORY.md`.
- Designed → Simulated: Agent Card reviewed and scope is bounded.
- Simulated → Evaluated: at least one customer-realistic dataset exists.
- Evaluated → Approved: eval pass on the agreed threshold, three supervised
  runs with no Hard Fail.
- Approved → Monitored: deployment cutover with rollback plan.
- Monitored → Improved: any of (eval score dip, customer complaint, new
  failure mode in `AI_MONITORING_REMEDIATION.md`).
- Improved → Monitored: bumped version re-passes eval and stabilises 7 days.
- Anything → Retired: see retirement criteria below.

## Retirement criteria

Retire an agent if **any** of:

- No active workflow has invoked it in 30 days.
- Eval pass rate fell below the agent's threshold for two consecutive cycles
  and improvement has stalled.
- A better-scoring replacement exists for the same capability.
- The agent's risk (sensitivity × autonomy × scope) rose above its measured
  business value per `PRODUCT_TELEMETRY.md`.
- Regulatory or contractual change makes the agent non-compliant.

Retirement is logged with date, reason, replacement (if any), and is
mirrored in `AI_AGENT_INVENTORY.md` (status flips to `Retired`).

## Operating cadence

| Cadence | What happens | Owner |
|---------|--------------|-------|
| Per-PR | Eval regression vs. prompt change | Agent owner |
| Weekly | Friday Control Tower review; flag drifting agents | HoP |
| Monthly | Promotion / retirement decisions | CTO + HoLegal |
| Quarterly | Portfolio review against `MODEL_PORTFOLIO.md` cost & quality | CRO + CTO |

## Cross-links

- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/governance/AI_MONITORING_REMEDIATION.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/auto_client_acquisition/agent_governance/`
