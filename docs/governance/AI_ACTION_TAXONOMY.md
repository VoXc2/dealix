# AI Action Taxonomy — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_ACTION_TAXONOMY_AR.md](./AI_ACTION_TAXONOMY_AR.md)

## Context
Not every AI action carries the same risk. Reading a permitted document
is not the same as sending an email to a real customer. The AI Action
Taxonomy classifies every AI action by risk level and tells the rest of
the system — sales, delivery, runtime governance, evals — which actions
are allowed in MVP, which need approval, and which are forbidden. The
taxonomy is the reference cited by
`docs/AI_OBSERVABILITY_AND_EVALS.md`, by
`docs/AI_STACK_DECISIONS.md`, and by the strategic plan in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## The Seven Levels

- **Level 0 — Read allowed data.** Retrieve from sources the user can
  already access. No external surface.
- **Level 1 — Draft.** Create draft output (text, list, table) that is
  not yet visible to anyone outside the workspace.
- **Level 2 — Recommend.** Suggest a next action for a human to take.
  Recommendation must include a reason.
- **Level 3 — Queue.** Prepare an action (e.g. a ready-to-send email)
  for human approval, with the full payload visible.
- **Level 4 — Execute Internal.** After approval, update internal
  state — CRM, workspace, internal records.
- **Level 5 — Execute External.** After approval, send/publish/contact
  externally. Restricted to enterprise contexts and named users.
- **Level 6 — Autonomous External Action.** AI acts on the outside world
  without human approval. **NOT allowed in Dealix MVP.**

## MVP Rules
- **Allowed by default:** Levels 0–3 for every Dealix service.
- **Approval required:** Level 4 requires named human approval in the
  workspace before state change.
- **Enterprise-only:** Level 5 is allowed only for enterprise clients
  with a signed agreement, audit logging on, and the action explicitly
  scoped per workflow.
- **Forbidden:** Level 6 is not implemented in any Dealix system. Any
  workflow that drifts towards autonomous external action must be
  blocked by runtime governance and reviewed by Governance Lead.

## How the Taxonomy Is Used
- **Sales:** every proposal declares the maximum action level it will
  reach (e.g. "Lead Intelligence Sprint operates at Level 3 max").
- **Delivery:** every workflow is annotated with its action level and
  approver chain.
- **Runtime governance:** the external-action check in
  `RUNTIME_GOVERNANCE.md` reads the level and selects the right
  decision verb.
- **Evals:** higher levels require stricter evals (claims safety,
  governance) per `EVALUATION_REGISTRY.md`.
- **Pricing:** Level 5 workflows price differently because of approval
  overhead and audit requirements.

## Worked Examples
- **Lead scoring** = Level 0/1. Reads CRM, drafts a ranked list.
- **Outreach draft** = Level 2/3. Suggests next account and queues a
  draft email; nothing leaves the workspace.
- **CRM hygiene update** = Level 4. After approval, AI updates account
  fields based on enrichment.
- **Customer email reply send** = Level 5. Enterprise-only; sent only
  after named human approval.
- **Auto-respond to inbound** without human = Level 6. Forbidden.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Workflow definition | Declared action level per step | Delivery Lead | Per build |
| AI run context | Action level lookup for runtime check | Governance Lead | Per run |
| Evals + audit log | Drift report (level vs. behaviour) | QA Lead | Weekly |

## Metrics
- **Action Level Conformance** — share of runs whose observed action
  level matched the declared level (target = 100%).
- **Approval Wait Time (L4/L5)** — median minutes to approval (target ≤
  30 min during work hours).
- **Forbidden Action Attempts** — count of attempts to perform Level 6
  actions (target = 0).
- **Enterprise L5 Coverage** — share of enterprise workflows that have
  an approved Level 5 scope document on file (target = 100%).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability that surfaces
  action-level conformance.
- `docs/AI_STACK_DECISIONS.md` — stack decisions referencing this
  taxonomy.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic constraint
  blocking Level 6 in MVP.
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime check using the
  taxonomy.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
