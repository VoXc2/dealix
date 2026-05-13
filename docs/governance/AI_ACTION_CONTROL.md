# AI Action Control — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_ACTION_CONTROL_AR.md](./AI_ACTION_CONTROL_AR.md)

## Context
Once an agent exists and has an identity, the next governance question is: *what may it actually do?* Not all actions carry the same risk. A summary read by a Dealix analyst is not the same as a message sent to a client's customer. This file defines the five Action Classes, the default policy applied at MVP, and how those defaults are tightened for enterprise environments. It enforces the action-related clauses of `docs/DEALIX_OPERATING_CONSTITUTION.md`, plugs into the observability stack in `docs/AI_OBSERVABILITY_AND_EVALS.md`, and links to the incident handling in `docs/ops/INCIDENT_RUNBOOK.md`.

## Action classes

### Class A — Internal Insight
Summarize, classify, score, extract, transform, label. Output consumed by Dealix or client team members only.
- **Default:** Allowed with logging.

### Class B — Client-Facing Output
Reports, drafts, recommendations, decks, briefs sent to or read by the client.
- **Default:** QA required before delivery; provenance attached.

### Class C — Internal System Change
Update a CRM stage, create a task, change a workflow status, write to an internal data store.
- **Default:** Approval required; rollback plan documented.

### Class D — External Communication
Send email, send WhatsApp, post to LinkedIn, publish content, message a third party.
- **Default:** Explicit approval per action; some channels restricted entirely; preview and recipient list confirmed before send.

### Class E — Autonomous External Action
Take consequential external action without per-action human approval.
- **Default:** **Blocked.** Allowed only by named exception, signed off by Governance Council and client executive sponsor, with full mitigation plan.

## MVP policy
At MVP and through the early enterprise stage, the default global policy is:

- **A** — allowed.
- **B** — QA required.
- **C** — approval required.
- **D** — restricted (only specific approved channels, only with explicit per-message approval).
- **E** — blocked.

The policy can be tightened per workspace but never loosened beyond the Dealix default without Council approval.

## Per-engagement configuration
Each enterprise workspace stores its own action policy table:

| Action Class | Workspace Default | Approver Role | Audit Required |
|---|---|---|---|
| A | Allowed | n/a | Yes |
| B | QA required | QA Reviewer | Yes |
| C | Approval required | Delivery Owner | Yes |
| D | Restricted | Client Sponsor + Delivery Owner | Yes |
| E | Blocked | n/a | Yes |

## Enforcement
- The action class is encoded in the agent card and the workflow definition.
- The runtime governance layer blocks any action whose class is not allowed for the calling user and workspace.
- Every blocked action is logged with reason; the log feeds the Enterprise AI Report Card.
- A pattern of blocks for a given agent triggers a Council review for either training the user or adjusting the agent's design.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Workflow definitions, agent cards | Action class per workflow step | Technical Owner + Governance | Per release |
| Client policy pack | Workspace action policy table | Governance + Delivery | Per engagement |
| Runtime block events | Report Card metrics + Council triggers | Governance | Continuous |

## Metrics
- Class-D Approval Rate — % of attempted Class-D actions that received explicit approval before send.
- Class-E Incidents — count (must be 0).
- Blocked-Action Ratio — blocked attempts per 1000 agent runs by class.
- QA-Before-Delivery Rate — % of Class-B outputs that passed QA before client delivery (target: 100%).

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution behind action limits
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability supporting action logging
- `docs/ops/INCIDENT_RUNBOOK.md` — incident response for action failures
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
