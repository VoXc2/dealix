# Runtime Governance — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [RUNTIME_GOVERNANCE_AR.md](./RUNTIME_GOVERNANCE_AR.md)

## Context
Most AI failures in mid-market companies happen at runtime — wrong
output delivered, personal data leaked, unsupported claim sent to a
customer — not during the build phase. Dealix's operating principle,
inherited from `docs/DEALIX_OPERATING_CONSTITUTION.md` and the strategic
plan `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, is that governance must
happen during execution, not after delivery. This file defines the
runtime check set, the decision verbs, and the path to making them
platform middleware.

## Principle
> Governance is something that happens while the workflow runs, not
> something that is reviewed afterwards.

Any AI-assisted workflow must pass runtime governance before its output
is delivered to a human or external system, and before any external
action is taken. After-the-fact governance is treated as a failure.

## Runtime Checks
For every AI run, the following checks fire in order. Any failed check
either redacts, blocks, or routes the run for approval (see Decision
Verbs).

1. **Data source check** — every input has a registered source and is
   permitted for this workflow.
2. **PII check** — personal data is detected, classified, and either
   redacted or routed through PII-safe paths.
3. **Permission check** — the requesting user is allowed to see the
   referenced data and to trigger this action (see
   `PERMISSION_MIRRORING.md`).
4. **Output claim check** — claims in the output are grounded in the
   permitted sources; no fabricated guarantees or testimonials.
5. **External action check** — any send/publish/contact action is
   classified per `AI_ACTION_TAXONOMY.md` and matched to the user's
   approval rights.
6. **Approval requirement** — the run is held for approval if the
   action level requires it.
7. **Audit log write** — a structured audit event is written
   (governance_events table).
8. **Proof event write** — a proof event is written for the Proof
   Ledger when the run produces a client-facing artefact.

## Decision Verbs
The runtime emits one of six decisions per run. These verbs are the
only allowed governance outcomes:

- **Allow** — all checks pass; output delivered.
- **Allow with review** — output delivered with a flag for human review
  inside the next QA pass.
- **Require approval** — output held until a permitted human approves
  in the workspace.
- **Redact** — output delivered with sensitive content removed; redaction
  is logged.
- **Block** — output not delivered; run is closed with reason; user is
  notified.
- **Escalate** — sent to Governance Lead; workflow paused for the
  affected workspace.

## Coverage Rules
- Every service in `docs/COMPANY_SERVICE_LADDER.md` must declare which
  checks apply and which decision verbs are valid.
- Level 0–3 actions (per `AI_ACTION_TAXONOMY.md`) require checks 1, 2,
  4, 7, 8. Level 4 adds checks 3 and 6. Level 5 adds check 5 and a
  second approver.
- Every governance event is keyed to a `project_id`, `run_id`, and
  `user_id` for traceability.

## From Policy to Middleware
Today these checks are enforced by playbook + delivery review. The
roadmap puts them inside the platform as middleware, called once before
any AI output is shown to a user or routed to an external system:

- **Phase 1 (now):** human checklist + audit log entry.
- **Phase 2:** library helper called from every workflow before output.
- **Phase 3:** platform middleware, evaluated as part of the LLM
  Gateway, with metrics surfaced in `docs/AI_OBSERVABILITY_AND_EVALS.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI run context (project, user, data sources, action) | Decision verb, redacted output, audit + proof events | Governance Lead, Delivery Lead | Per run |
| Approval queue | Approved/blocked runs | Workspace Approver | Continuous |
| Governance metrics | Weekly governance report | Founder | Weekly |

## Metrics
- **Runtime Coverage** — share of AI runs that passed through the full
  check set (target = 100% by Phase 2).
- **Block-Before-Send Rate** — share of incidents caught at runtime
  vs. caught after delivery (target ≥ 95%).
- **Approval Latency** — median minutes a Level-4/5 run waits for
  approval (target ≤ 30 min during work hours).
- **False Block Rate** — share of runs blocked that a human later
  reverses (target ≤ 5%).

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution that
  makes runtime governance non-negotiable.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability layer that
  surfaces the runtime checks.
- `docs/EVALS_RUNBOOK.md` — eval runbook that informs the output claim
  check.
- `docs/governance/PERMISSION_MIRRORING.md` — sibling file feeding the
  permission check.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
