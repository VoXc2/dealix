# Runtime Governance

> Policy on paper is necessary but not sufficient. Real governance happens
> **during execution** — at the moment an AI workflow is about to read
> data, generate output, or take an action. Dealix enforces 8 runtime
> checks before any sensitive operation completes.

## The 8 runtime checks

Every AI-assisted workflow passes through these in order. Any check that
returns BLOCK halts the operation.

1. **Data source check** — every input record carries provenance. Records without source are quarantined to `research-only`.
2. **PII check** — `dealix/trust/pii_detector.py` scans for email / Saudi mobile / National ID / IBAN / card. Card and IBAN are auto-blocked from any output.
3. **Permission check** — the requesting user has the right to read these inputs and perform this action (per Permission Mirroring rule below).
4. **Output claim check** — `dealix/trust/forbidden_claims.py` scans generated text for "نضمن / guarantee / 100% / best in / risk-free" and refuses to ship.
5. **External action check** — if the action would write/send/publish outside Dealix's perimeter, the Approval Matrix is consulted.
6. **Approval requirement** — the named approver (per `dealix/trust/approval_matrix.py`) must sign before the side-effect runs.
7. **Audit log write** — the action and its decision are appended to the event store (`auto_client_acquisition/revenue_memory/event_store.py`).
8. **Proof event write** — for outputs that close a project stage, a Proof event is written so it surfaces in the Proof Ledger.

## Runtime Decision values

```
ALLOW                  → proceed normally
ALLOW_WITH_REVIEW      → proceed; human reviews output before customer-facing use
REQUIRE_APPROVAL       → halt until named approver signs
REDACT                 → strip PII / sensitive data, then proceed
BLOCK                  → refuse; log reason
ESCALATE               → CEO / Head-of-Legal review
```

## Permission Mirroring

Hard rule, enforced at runtime:

> An AI agent or workflow may only access data and perform actions that
> the requesting user is authorized to access or perform.

Implications:

- AI inherits the user's RBAC scope. No "super-user AI".
- AI cannot bypass role-based access checks.
- Sensitive actions (external comms, data export, policy override) require an explicit approval **even when the user has the permission to do them manually**.
- All accesses are logged with `actor: user_id` or `actor: agent_id`.

## AI Action Taxonomy (used by the runtime to classify)

| Level | Action | Allowed in MVP? |
|------:|--------|:---------------:|
| 0 | Read allowed data | ✅ |
| 1 | Generate draft (text/data) | ✅ |
| 2 | Recommend next action | ✅ |
| 3 | Queue an action for human approval | ✅ |
| 4 | Execute internal state change (after approval) | ✅ |
| 5 | Execute external (send / publish / contact / write API) | ⚠️ enterprise-only, with explicit per-action approval |
| 6 | Autonomous external action (no human in loop) | ❌ Forbidden, no exceptions |

## Enforcement code references

- `dealix/trust/policy.py` — policy engine evaluator.
- `dealix/trust/pii_detector.py` — Level 2 check.
- `dealix/trust/forbidden_claims.py` — Level 4 check.
- `dealix/trust/approval_matrix.py` — Levels 5–6 routing.
- `auto_client_acquisition/revenue_memory/event_store.py` — Level 7 audit append.
- `auto_client_acquisition/delivery_factory/event_writer.py` — Level 8 Proof event write.

## Why this matters

Agentic AI is moving from "generate text" to "take action". Industry
guidance (Gartner, Anthropic, public agentic-AI playbooks) converges on:
permission mirroring + human oversight + per-action audit. Dealix bakes
all three into the runtime, not into a policy PDF.

## Cross-links

- `docs/governance/APPROVAL_MATRIX.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/AUDIT_LOG_POLICY.md`
- `docs/governance/PII_REDACTION_POLICY.md`
- `docs/governance/INCIDENT_RESPONSE.md` *(to be added)*
- `docs/policy/revenue_os_policy_rules.md` (W4.T14)
