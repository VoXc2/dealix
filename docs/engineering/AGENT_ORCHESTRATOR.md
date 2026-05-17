# Agent Orchestrator — Full Ops System

> STATUS: design spec for a later build phase (V3). No orchestrator code is added
> in this phase. This document defines the contract that the build implements.

## Why

The Full Ops System runs many agents (sales, support, marketing, governance —
see [`data/config/agent_permissions.yaml`](../../data/config/agent_permissions.yaml)).
Agents must never act freely. The orchestrator is the single choke point that
enforces non-negotiable #1 (no live send), #2 (no live charge), #10 (no unbounded
agents), and #11 (no unaudited changes).

## The loop

```
event
  -> orchestrator receives it
  -> policy check        (governance_os: is this event/agent/action allowed?)
  -> select agent        (per agent_permissions.yaml scope)
  -> run agent           (agent prepares output only)
  -> validate output     (schema + claim check + source check)
  -> approval gate       (approval_center, IF risk_level requires it)
  -> log evidence        (evidence event + agent_run_log)
  -> update state        (only after the gate clears)
```

An agent **prepares**; a human **approves** anything risky; the orchestrator
**records** every step. No agent reaches an external surface directly.

## Where it lives

| Concern | Module (existing) |
| --- | --- |
| Agent runtime / identity | `auto_client_acquisition/agent_os/`, `auto_client_acquisition/agent_identity_access_os/` |
| Multi-agent coordination | `core/agents/` |
| Policy decision | `auto_client_acquisition/governance_os/`, `dealix/governance/` |
| Approval gate | `auto_client_acquisition/approval_center/` |
| Evidence | `dealix/contracts/`, `auto_client_acquisition/evidence_control_plane_os/` |

The orchestrator is new code in `agent_os/`; it does not replace the existing
agent docs in `docs/16_agents/` or `docs/10_agents/`.

## agent_run_log shape

Every agent run emits one record (non-negotiable #11):

```json
{
  "agent_name": "ScopeBuilderAgent",
  "input_event": "scope_requested",
  "input_refs": ["meeting_notes_123"],
  "output_type": "scope_draft",
  "risk_level": "high",
  "sources_used": ["meeting_notes_123"],
  "approval_rule": "approval_at_risk",
  "approval_required": true,
  "approval_status": "pending",
  "policy_result": "allowed_with_approval",
  "evidence_event_id": "evt_..."
}
```

`approval_rule` is read from `agent_permissions.yaml`. `policy_result` is one of
`allowed`, `allowed_with_approval`, `blocked`.

## Invariants

- An agent with no entry in `agent_permissions.yaml` cannot run (#10).
- `external_send` and `charge` are never autonomous, regardless of agent (#1, #2).
- A `high`/`critical` output cannot reach a customer without an approval record.
- Every run produces an `agent_run_log` and an evidence event (#11, #9).
- Outputs that make claims must carry `sources_used` or be blocked (#7).

## Out of scope (this phase)

- Orchestrator implementation, agent prompt files, and the run-log store.
- The future test gates named in `agent_permissions.yaml`.
