# Permission Mirroring Design — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Technical Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PERMISSION_MIRRORING_DESIGN_AR.md](./PERMISSION_MIRRORING_DESIGN_AR.md)

## Context
The most common way AI breaks enterprise security models is by acting as a privileged super-user when the requesting human is not. Dealix prevents this by mirroring permissions: an agent acting on behalf of a user can only access or do what that user is allowed to access or do. This file specifies the design of permission mirroring inside Dealix, in line with the Data Processing Agreement at `docs/DPA_DEALIX_FULL.md`, the retention boundaries at `docs/DATA_RETENTION_POLICY.md`, and the architectural placement in `docs/BEAST_LEVEL_ARCHITECTURE.md`.

## Principle
**AI can only access or act on what the requesting user is allowed to.** The agent never inherits broader privileges than its calling principal. The agent is not a back door into a workspace.

## Required checks
Every AI run must pass the following checks before executing:

- **User identity** — the calling user is authenticated and present.
- **Workspace** — the user has access to the workspace and the agent is allowed to run in that workspace.
- **Role** — the user's role is recorded and is sufficient for the requested capability.
- **Data permissions** — the agent's effective dataset scope is the intersection of agent permissions and user permissions.
- **Tool permissions** — the agent's effective tool list is the intersection of agent permissions and user permissions.
- **Action permissions** — the action class requested is allowed for the user's role and the workspace policy.
- **Approval requirement** — if the action class requires approval, the approval token is checked and bound to a named human approver.

## Implementation
Every AI run is initialized with a typed context object containing:

```
{
  user_id,
  workspace_id,
  role,
  allowed_source_ids,     // intersect with agent.data_access
  allowed_tool_ids,       // intersect with agent.tool_access
  allowed_action_classes  // intersect with agent.action_permissions
}
```

The runtime governance layer rejects any agent call that attempts to act outside the intersected scopes. Rejections are logged with reason and surfaced to the user with a human-readable explanation.

## Future API
Once the governance service is exposed for client-side enforcement, the public surface becomes:

```
POST /governance/permission-check
{
  "user_id": "...",
  "workspace_id": "...",
  "agent_id": "...",
  "requested_sources": ["..."],
  "requested_action": "ClassC.update_crm_stage"
}
```

The response is either `allowed` with an audit ID, `requires_approval` with the approver role, or `denied` with reason and policy reference.

## Edge cases
- **Delegation.** If a user delegates an action to an agent for asynchronous execution, the delegation is time-bounded and limited to the user's scope at the moment of delegation. Expanded scopes after delegation do not retroactively apply.
- **Service accounts.** Service principals used by scheduled agents are configured with their own permission profile and treated as named principals — never as "all-access".
- **Client admin.** A workspace admin grants permissions to roles, not to agents. Agents always inherit through users.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| User identity, agent card, workspace policy | Run context with intersected scopes | Technical Owner | Per run |
| Permission-check API call | Allowed / requires_approval / denied | Governance Service | Per request |
| Rejection logs | Council review for repeated rejections | Governance | Monthly |

## Metrics
- Mirroring Compliance — % of runs that pass through the permission-check function (target: 100%).
- Over-Scope Attempts — count of runs blocked because of scope-exceeding requests, by agent.
- Approval-Required Latency — median seconds from agent action attempt to approval decision.
- Audit-ID Coverage — % of allowed runs that received an audit ID linked to provenance.

## Related
- `docs/DPA_DEALIX_FULL.md` — Data Processing Agreement framing the permissions model
- `docs/DATA_RETENTION_POLICY.md` — retention rules binding the source scopes
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural placement of the governance service
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
