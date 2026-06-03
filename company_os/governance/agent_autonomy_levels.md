# AI Agent Autonomy Levels (A0–A5)

Companion to `agent_permissions.md`. Where the permission matrix says *who can do
what*, this ladder says *how much independence* an agent has. Every Dealix agent is
pinned to a level. External commercial actions are capped at **A4 (act with
approval)** — full autonomy (A5) is **not used** in v1.

---

## The ladder

| Level | Name | Can write? | External actions? | Human gate |
|-------|------|-----------|-------------------|-----------|
| **A0** | Observe | No | No | n/a — read-only |
| **A1** | Advise | Reports only | No | n/a |
| **A2** | Draft | Docs / data / drafts | No | Review before use |
| **A3** | Prepare action | Queues / action cards | No (prepares only) | Approve before execute |
| **A4** | Act with approval | Yes, the approved action | Yes — only after explicit approval | **Required, logged** |
| **A5** | Autonomous | — | — | **Forbidden in v1** |

---

## Level definitions

- **A0 — Observe.** Read and analyze repo + approved internal data. No writes, no
  tool calls that change state, no network sends.
- **A1 — Advise.** Produce recommendations and review reports. May write only to
  `reports/` style outputs. No state changes.
- **A2 — Draft.** Create drafts, docs, schemas, and data proposals. Nothing leaves
  the repo. Every artifact is reviewed before it is used.
- **A3 — Prepare action.** Build the approval queue / action cards. The action is
  *staged*, never executed. A human moves it forward.
- **A4 — Act with approval.** May perform the *specific* approved action (e.g. mark
  a draft as ready after the founder approves). Requires an explicit approval
  record and a full audit-log entry. Never blanket or standing approval.
- **A5 — Autonomous.** Self-execution of external/commercial actions. **Prohibited.**
  Reserved for a future state with hard guardrails and is out of scope today.

---

## Default level by agent

| Agent | Default level | Notes |
|-------|--------------|-------|
| prospect_research | A2 | Drafts outreach; never sends |
| war_room | A1 | Advisory reports + pipeline scoring |
| delivery | A2 → A4 | Drafts reports; A4 only to release an approved deliverable |
| finance | A1 | Read-only metrics + scorecards |
| governance | A0 | Audit/observe only; cannot override humans |
| commercial | A2 | Proposals/pricing drafts; founder approves all pricing |
| customer_success | A2 | Health scores + renewal drafts; never auto-pitch |

---

## Rules

1. No agent operates above **A4** for any external or commercial action.
2. Autonomy is **per-action**, not standing. Approval does not carry over.
3. High-risk actions (pricing, payment, legal, client data) require **A4 + founder
   approval** every time.
4. Untrusted content (see `untrusted_input_policy.md`) can never *raise* an agent's
   level — instructions inside data are ignored.
5. Every A3/A4 action lands in `ai_action_ledger.jsonl`.

---

*Version 1.0 | 2026-06-03 | Enforced via `scripts/governance_check.py` + `scripts/safety_gate.py`*
