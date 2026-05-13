# Permission Mirroring — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PERMISSION_MIRRORING_AR.md](./PERMISSION_MIRRORING_AR.md)

## Context
Permission Mirroring is the rule that an AI agent inside Dealix does
nothing the user is not authorised to do. It exists because the most
expensive failure mode in B2B AI is an agent that can read or write
data its requesting user could not. The rule is inherited from
`docs/DEALIX_OPERATING_CONSTITUTION.md` and is the enforcement spine
behind the runtime checks in `RUNTIME_GOVERNANCE.md`. It also implements
data-handling commitments from `docs/DPA_DEALIX_FULL.md` and
`docs/DATA_RETENTION_POLICY.md`.

## Rules
1. **AI inherits user permissions.** Any agent invoked by a user reads
   data and triggers actions under that user's role only.
2. **AI cannot bypass role-based access.** The agent's effective ACL
   is the user's ACL intersected with the workspace ACL.
3. **AI cannot send, publish, delete, or modify externally** without
   explicit, named permission on the action.
4. **Sensitive actions require approval** even if the user has access
   — for example, sending an outbound communication or deleting client
   data.
5. **All actions are logged** with `user_id`, `project_id`, `run_id`,
   action class, and outcome (see `AI_RUN_LEDGER.md`).

These five rules apply to every Dealix-built agent, every Dealix-built
workflow, and every Dealix service.

## Examples
- **Sales rep** sees only their own leads; the agent cannot pull
  another rep's pipeline even if asked.
- **Support lead** sees the support KB; the agent cannot read finance
  data even if a single search query would return it.
- **CEO** sees executive reports; the agent never reveals individual-
  level personnel data unless explicitly scoped.
- **External client user** sees only their workspace; the agent cannot
  surface another client's content even in aggregate form.

## Implementation Notes
- The agent runtime resolves the requesting user's identity and roles
  on every call.
- The LLM Gateway attaches the user's effective ACL to every prompt and
  filters retrieved context before generation.
- Tool calls (search, write, send) are wrapped in a permission guard
  that re-checks the user's ACL at call time.
- Approval-required actions enter the workspace approval queue with a
  named approver from the client's RACI.
- Permission violations are routed as **Escalate** decisions in
  `RUNTIME_GOVERNANCE.md` and trigger an incident per
  `INCIDENT_RESPONSE.md`.

## What Permission Mirroring Is Not
- It is not the same as authentication: SSO and login are
  pre-requisites, not substitutes.
- It is not a content filter: filtering removes words; mirroring
  controls scope.
- It is not retroactive: a mirrored permission denial cannot be
  bypassed by re-asking with different wording — the guard sits below
  the prompt.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| User identity, roles, workspace ACL | Effective ACL applied to retrieval, generation, tools | Governance Lead, Platform | Per request |
| Approval queue | Approved/denied sensitive actions | Workspace Approver | Continuous |
| Permission incidents | Incident records and updated rules | Governance Lead | Per incident |

## Metrics
- **Permission Coverage** — share of agent calls executed under an
  explicit ACL resolution (target = 100%).
- **Permission Violations** — count of detected violations per month
  (target = 0; any non-zero triggers an incident).
- **Approval Bypass Attempts** — count of attempts to perform a Level
  4/5 action without approval (tracked, not bounded).
- **Audit Completeness** — share of agent actions with a complete log
  entry (target = 100%).

## Related
- `docs/DPA_DEALIX_FULL.md` — data processing commitments mirrored in
  these rules.
- `docs/DATA_RETENTION_POLICY.md` — retention boundaries the ACL must
  respect.
- `docs/ops/INCIDENT_RUNBOOK.md` — runbook for permission incidents.
- `docs/governance/RUNTIME_GOVERNANCE.md` — sibling file consuming the
  permission decision.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
