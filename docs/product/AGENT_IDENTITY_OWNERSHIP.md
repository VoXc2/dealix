# Agent Identity & Ownership — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Technical Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AGENT_IDENTITY_OWNERSHIP_AR.md](./AGENT_IDENTITY_OWNERSHIP_AR.md)

## Context
Enterprise governance cannot start until every agent in the Dealix stack has an identity, an owner, and a lifecycle. An unnamed, unowned agent is — by definition — ungoverned. This file defines the minimum metadata every Dealix agent must carry, the lifecycle states it must move through, and the audit obligations attached to it. It enforces the agent-related clauses of `docs/DEALIX_OPERATING_CONSTITUTION.md` and is the precondition for the Governance Council reviews defined in `docs/enterprise/AI_AGENT_GOVERNANCE_COUNCIL.md`.

## Every agent carries four blocks

### 1. Identity
The non-negotiable identity attributes are:

- `agent_id` — globally unique identifier.
- `name` — short human-readable name.
- `version` — semantic version, incremented on prompt or tool changes.
- `owner` — named Dealix role accountable for behavior.
- `workspace` — Dealix-internal or client workspace where the agent is allowed to run.
- `service` — the Dealix service (Revenue, Customer, Operations, Knowledge, Data, Governance, Reporting) the agent belongs to.
- `capability` — the capability slot it fills in the Capability Map.
- `autonomy_level` — 0..5 (see Autonomy Validation Gates).

### 2. Permissions
- **Data access** — explicit list of dataset and source IDs the agent may read.
- **Tool access** — explicit list of tool IDs the agent may invoke.
- **Action permissions** — which action classes (A–E) the agent is allowed to attempt.
- **Approval requirements** — which actions require human approval and from which role.

### 3. Lifecycle
Every agent moves through six lifecycle states:

`created → approved → active → monitored → deprecated → retired`

State transitions are recorded with timestamp, actor, and reason. No agent may serve client output while in `created`, `deprecated`, or `retired` state.

### 4. Audit
- Every run logged with run ID, inputs, outputs, model, tokens, cost, governance status.
- Every blocked action logged with reason and policy reference.
- Every approval logged with approver, approval scope, and time-to-decision.

## Sample registered agents

| Agent | Owner | Capability | Autonomy | Data Access | Action Access | Status |
|---|---|---|---:|---|---|---|
| RevenueAgent | Delivery | Revenue | 2 | lead datasets | draft/recommend | Active |
| OutreachAgent | Delivery | Revenue | 2 | approved accounts | draft only | Active |
| ComplianceGuardAgent | Governance | Governance | 3 | metadata | block/escalate | Active |

## Hard rules
- **No agent without an owner.** If no Dealix role accepts accountability, the agent is not registered.
- **No agent without permissions.** Data, tool, and action permissions must be set before activation.
- **No agent without a lifecycle.** Every agent has a known state and the next required review date.
- **No silent prompt changes.** A prompt or tool change increments `version` and triggers Council notification.

## Registration flow
1. Author submits agent card (identity + permissions + capability claim + eval plan).
2. Governance Reviewer checks against policy and existing inventory (sprawl check).
3. Technical Owner verifies eval coverage and rollback plan.
4. Council approves with explicit autonomy level and workspace scope.
5. Agent moves to `active` and is added to the central inventory.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent card submissions | Approved entries in agent inventory | Technical Owner + Governance | Per request |
| Prompt/tool change requests | Versioned agent updates | Technical Owner | Per change |
| Eval results, incident reports | Lifecycle state changes | Council | Weekly |

## Metrics
- Owner Coverage — % of agents with named owner (must be 100%).
- Versioned-Change Compliance — % of prompt/tool changes that incremented `version` and notified Council.
- Stale-Agent Count — agents with no run in 30 days still listed as active.
- Lifecycle Hygiene — % of agents with a recorded next-review date.

## Related
- `docs/AI_STACK_DECISIONS.md` — stack decisions binding agent design choices
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval framework agents must satisfy
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural placement of agents
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
