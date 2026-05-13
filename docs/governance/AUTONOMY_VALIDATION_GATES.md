# Autonomy Validation Gates — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AUTONOMY_VALIDATION_GATES_AR.md](./AUTONOMY_VALIDATION_GATES_AR.md)

## Context
Autonomy is not a feature — it is a risk classification. The further along the autonomy spectrum an agent operates, the more validation is required before it is allowed to act. This file defines the validation gates an agent must pass to operate at each autonomy level. It implements clauses of `docs/DEALIX_OPERATING_CONSTITUTION.md` related to AI behavior limits, and binds Dealix delivery to the stack choices documented in `docs/AI_STACK_DECISIONS.md` and the eval discipline in `docs/EVALS_RUNBOOK.md`.

## The seven autonomy levels

### Level 0 — Read
Agent only reads data; produces no output to humans except diagnostics.
- **Gate:** Access scope check; logging in place.

### Level 1 — Analyze
Agent reads data and produces analytical artifacts (scores, summaries, classifications) for internal use.
- **Gate:** Schema validation on inputs and outputs; sample QA on a representative dataset before activation.

### Level 2 — Draft / Recommend
Agent produces drafts or recommendations intended to support a human decision.
- **Gate:** QA review of sample outputs; forbidden-claims check (no fabricated facts, no guarantees, no PII leaks); mandatory human review before any external delivery.

### Level 3 — Queue
Agent queues actions for human approval (e.g., proposed CRM updates, outreach drafts).
- **Gate:** Approval workflow wired and tested; full audit log; named owner confirms readiness.

### Level 4 — Execute Internal
Agent executes actions inside Dealix-controlled systems (e.g., updates a stage in an internal CRM, files an internal task).
- **Gate:** Role permission check enforced; rollback plan documented; audit trail captured; incident response procedure linked.

### Level 5 — Execute External
Agent executes actions that touch external parties or external systems on behalf of a client (e.g., sending a message after explicit client approval).
- **Gate:** Enterprise controls in place; consent and lawful basis evidenced; explicit approval record per action; rollback or mitigation plan executable within the action's reversibility window.

### Level 6 — Autonomous External
Agent acts externally without per-action human approval.
- **Gate:** **Not allowed in the Dealix standard.** Reserved exclusively for narrowly scoped, contractually negotiated exceptions reviewed and signed off by the Governance Council and named client executive sponsor. The default answer is "no".

## How gates are validated
- Gates are encoded as a checklist in the agent card.
- Gate evidence (eval IDs, QA report IDs, rollback document IDs, approval workflow IDs) is attached to the agent record.
- The Governance Council cannot approve an agent at autonomy level *n* until all gate evidence for levels 0..n is present.
- Demotion is automatic: if any gate evidence becomes stale (eval older than 90 days, missing rollback owner, broken approval flow), the agent is demoted one level pending refresh.

## Per-engagement override
Some clients set their own ceiling — e.g., "no autonomy above Level 3 in our workspace". The Governance Council enforces the lower of the Dealix default and the client ceiling, and records the chosen autonomy level for each agent on each workspace.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent card with autonomy claim | Gate verification checklist | Governance Reviewer | Per agent registration |
| Eval runs, QA reports, rollback docs | Evidence package per autonomy level | Technical Owner + QA | Per release |
| Client policy ceiling | Workspace-specific autonomy cap | Governance + Delivery | Per engagement |

## Metrics
- Gate-Pass Rate — % of agents that pass all gates for the claimed autonomy level on first submission.
- Autonomy Drift — number of agents demoted due to stale evidence per quarter.
- Level-3+ Approval Time — median hours to approve an agent at autonomy ≥3.
- Override-Compliance — % of workspaces where the configured autonomy cap matches the client policy ceiling.

## Related
- `docs/AI_STACK_DECISIONS.md` — model and stack choices these gates assume
- `docs/EVALS_RUNBOOK.md` — eval discipline backing gate evidence
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution behind the autonomy ceiling
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
