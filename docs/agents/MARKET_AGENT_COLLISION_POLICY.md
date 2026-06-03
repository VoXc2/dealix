# Market Agent Collision Policy

When two market agents touch the same artifact (e.g.
`company_os/revenue/outreach_queue.json` or `approval_queue.json`):

1. **Preserve newer safety gates** (e.g. a newly-added suppression check wins).
2. **Never overwrite manual/founder edits** (approved/rejected items are immutable).
3. **Prefer the smaller PR.**
4. **Write a conflict report** to `reports/agents/`.
5. **Escalate to the founder** if the resolution is ambiguous.

Special rules for the queues:
- An item marked `approved=true` or `rejected=true` is **frozen** — agents may
  only append new items, never mutate decided ones.
- Suppression entries are append-only; no agent removes them.
- Concurrent draft regeneration must not resurrect a suppressed recipient.

Forbidden during resolution: force-push, deleting another agent's work,
weakening a test, or removing a gate.
