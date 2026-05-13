# Agent Control Doctrine — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** Head of AI Ops + Head of Governance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AGENT_CONTROL_DOCTRINE_AR.md](./AGENT_CONTROL_DOCTRINE_AR.md)

## Context
Agents are the muscle of Dealix's Core OS, but the Intelligence Layer is
where their decisions become strategy. An untracked agent is a liability —
to PDPL, to brand, to capital. This doctrine specifies the minimum
contract every agent must meet before it can run inside Dealix, and the
runtime conditions that keep it in bounds. It cites the sibling product
spec `docs/product/AGENT_IDENTITY_OWNERSHIP.md` (which defines identity
and ownership) and the governance spec
`docs/governance/AUTONOMY_VALIDATION_GATES.md` (which defines autonomy
gates). See `docs/DEALIX_OPERATING_CONSTITUTION.md` for the constitutional
basis and `docs/AI_OBSERVABILITY_AND_EVALS.md` for the runtime telemetry.

## The ten controls every agent must declare
Every agent — internal automation, client-facing copilot, or strategic
brain — must declare and maintain the following before running in
production:

1. **Identity.** Stable agent_id, name, version, and lineage. See
   `docs/product/AGENT_IDENTITY_OWNERSHIP.md` for the identity contract.
2. **Owner.** A named human accountable for the agent's outputs,
   incidents, and decommissioning. No nameless ownership.
3. **Permissions.** Explicit allow-list of data sources, ledgers, and
   external systems the agent may read or write — mirrored from the
   owner's role per `docs/governance/PERMISSION_MIRRORING.md`.
4. **Autonomy level.** One of the bands defined in
   `docs/governance/AUTONOMY_VALIDATION_GATES.md`: suggest, draft,
   execute-with-approval, execute-autonomous. Defaults to draft.
5. **Tool access.** Declared set of tools (APIs, MCP servers, code
   execution surfaces). Anything not listed is blocked at runtime.
6. **Allowed outputs.** Output types the agent may emit (recommendation,
   document, transaction draft, transaction commit). Each output type is
   bound to an autonomy level.
7. **Forbidden actions.** Explicit deny-list — PII exfiltration, sending
   external email without approval, financial commitments, contractual
   language, etc. — enforced at runtime by the governance guard.
8. **Audit.** Every run writes to the AI Run Ledger and, where it
   touches client or policy boundaries, to the Audit Ledger.
9. **Eval.** A named eval suite from `docs/EVALS_RUNBOOK.md` that
   gates promotion between autonomy levels. Failing eval blocks
   promotion.
10. **Decommission rule.** A written trigger (cost overrun, eval
    regression, owner departure, demand collapse) that retires the
    agent. No agent is immortal.

## No agent runs without
Four artefacts are required and re-verified at every deployment:

- **Agent card.** Living document covering all ten controls above. Lives
  in `docs/product/AGENT_IDENTITY_OWNERSHIP.md`'s catalog.
- **Runtime governance.** The guard described in
  `docs/governance/RUNTIME_GOVERNANCE.md` is active and reading the
  agent's permission set.
- **AI Run log.** Confirmed write path to the AI Run Ledger
  (see `LEDGER_ARCHITECTURE.md`).
- **Human approval path.** A defined route for approval requests when
  the agent hits its autonomy boundary, per
  `docs/governance/AUTONOMY_VALIDATION_GATES.md`.

An agent missing any of these artefacts is blocked at deploy time.

## Autonomy promotion
An agent's autonomy level is promoted only when:
- Eval pass rate exceeds the threshold defined in
  `docs/EVALS_RUNBOOK.md` for the target band, sustained for 30 days.
- The owner submits a written promotion proposal with the last 30 days
  of AI Run Ledger evidence.
- Head of Governance signs off, with reference to incidents in the
  Audit Ledger.

Promotion is reversible. A single high-severity incident drops the
agent down at least one band pending review.

## Inter-agent rules
- Agents do not invoke each other directly across owner boundaries.
  Cross-owner invocations route through the event bus from
  `EVENT_TO_DECISION_SYSTEM.md`.
- Multi-agent flows declare a coordinator agent whose owner is
  accountable for the composite outcome.
- Loops between agents require a maximum step count and a token budget
  enforced at runtime.

## Decommissioning
- The decommission rule from control 10 is checked monthly by the
  agent's owner.
- A decommissioned agent's history remains in the ledgers; the agent
  card is marked retired with the decommission rationale and date.
- Capital assets produced by the agent transfer to a named successor or
  are archived.

## Failure modes
- **Shadow agents.** Agents running outside the card system. Mitigation:
  runtime guard refuses unidentified callers.
- **Phantom ownership.** Owner left the company. Mitigation: ownership
  is reverified quarterly.
- **Eval rot.** Eval suite outdated. Mitigation: every promotion
  refreshes the eval baseline; orphan evals are pruned.
- **Permission drift.** Agent grants beyond owner role. Mitigation:
  mirror at deploy and on owner role change.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent card | Deploy approval | Head of AI Ops + Head of Governance | Per deploy |
| AI Run Ledger + evals | Autonomy promotions/demotions | Head of Governance | Continuous |
| Audit Ledger incidents | Agent reviews | Head of Governance | Per incident |
| Decommission triggers | Retirement actions | Agent owner | Monthly |

## Metrics
- **Card Completeness** — share of running agents with all ten controls
  declared (target: 100%).
- **Promotion Reversal Rate** — share of autonomy promotions reversed
  within 30 days (target: <10%).
- **Shadow Agent Count** — runtime-detected unidentified callers
  (target: 0).
- **Decommission Discipline** — share of agents past decommission
  trigger retired within 30 days (target: 100%).

## Related
- `docs/product/AGENT_IDENTITY_OWNERSHIP.md` — identity and ownership contract (cited)
- `docs/governance/AUTONOMY_VALIDATION_GATES.md` — autonomy gates (cited)
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime guard the doctrine relies on
- `docs/EVALS_RUNBOOK.md` — eval suites gating promotion
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — runtime telemetry
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
