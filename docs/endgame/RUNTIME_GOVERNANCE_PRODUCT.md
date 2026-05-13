# Runtime Governance — A Product, Not a Document

Static policies, prompt rules, and fixed permissions do not govern agentic AI. Agent behavior emerges from execution paths, so governance must evaluate at runtime — using agent identity, the partial trace, the proposed action, and the current state of the enterprise.

Dealix Governance Runtime is therefore treated as a **product**, not a compliance artifact.

## 1. Position in the Core OS

`auto_client_acquisition/governance_os/`

- `policy_check.py` — pre-action evaluation against policy bundles.
- `runtime_guardrails.py` — in-flight evaluation during an AI run.
- `approval_matrix.py` — who approves what, when.
- `audit_log.py` — immutable AI run ledger.
- `rules/` — versioned, scoped rule packs (per BU, per channel, per sector).

## 2. Components

- **Policy Engine** — evaluates context vs. active policy bundle.
- **PII Detection** — identifies and redacts personal data before transit.
- **Allowed-Use Checker** — verifies the action is in-scope for the agent.
- **Claim Safety Checker** — refuses unverifiable claims in client-facing outputs.
- **Channel Risk Checker** — applies channel-specific limits (e.g., WhatsApp, email, voice).
- **Approval Engine** — orchestrates human approvals.
- **Audit Log** — append-only, signed, queryable.
- **AI Run Ledger** — per-run record of inputs, outputs, decisions, cost, model.
- **Risk Index** — running risk score per agent and per workflow.
- **Escalation Rules** — when to break-glass, pause an agent, or page a human.

## 3. Decision vocabulary

The runtime emits one of:

- `ALLOW`
- `ALLOW_WITH_REVIEW`
- `DRAFT_ONLY`
- `REQUIRE_APPROVAL`
- `REDACT`
- `BLOCK`
- `ESCALATE`

Any code path that does not honor this vocabulary is a defect.

## 4. Example decision record

```json
{
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "matched_rules": ["external_action_requires_approval"],
  "redactions": ["phone"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

## 5. Productization

The runtime ships in three forms:

1. **Embedded** — inside every Dealix engagement; no opt-out.
2. **Standalone Review** — the `AI Governance Review` offer (`PRODUCTIZED_OFFER_STACK.md`).
3. **Managed** — Monthly Governance retainer with rule tuning, audit reporting, and drift detection.

## 6. Why it is a moat

- Static guardrails do not bind a multi-step agent. Runtime governance does.
- Regulated industries cannot adopt AI without an audit trail and approval matrix.
- The runtime accumulates rules and patterns engagement by engagement — every project makes the next one safer and faster.
- It pairs naturally with the Proof Economy: every blocked, redacted, or approved event becomes evidence.

## 7. Interfaces

- `governance_os.evaluate(action, context) -> Decision`
- `governance_os.approve(event_id, approver) -> ApprovalRecord`
- `governance_os.audit(event_id) -> AuditRecord`
- `governance_os.risk_index(agent_id, window) -> float`

## 8. Failure modes to design against

- A model output goes to a customer without `evaluate` being called.
- An approval is recorded without an immutable audit row.
- Rules drift between BUs without a shared evaluator.
- Cost or rate-limit failures cause `ALLOW` to be returned by default. The default must be **DRAFT_ONLY**.
