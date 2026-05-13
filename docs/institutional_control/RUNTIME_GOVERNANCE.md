# Runtime Governance

A policy PDF does not govern a multi-step agent. Runtime governance is the **moat**: governance evaluated *at runtime*, against the live trace.

## 1. What the runtime inspects

Before every proposed action:

- source status
- PII status
- allowed use
- claim risk
- channel risk
- agent autonomy
- approval requirement
- audit event

## 2. Example decision record

```json
{
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "reason": "Personal contact data exists but external action is not approved.",
  "matched_rules": ["external_action_requires_approval"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

## 3. Why this matters commercially

A serious enterprise buyer does not want blind automation. They want a system that can answer:

- What data was used?
- Who approved?
- What was blocked?
- Where is the evidence?
- What are the risks?
- What is the next action?

A Dealix engagement answers these questions for every consequential action by reading the runtime record.

## 4. Failure modes

- An output reaches a customer without `evaluate` being called.
- Approval is recorded only in chat, not in the engine.
- BUs run forked rule packs with different decisions.
- A cost or rate-limit error returns `ALLOW` by default — constitutional violation.

## 5. Operating discipline

- Every BU shares the same evaluator.
- Specialization is via versioned rule packs, not via forks.
- Every decision lands in the Audit Trail with full inputs.
- Blocked and escalated events surface in the Command Center.

## 6. The principle

> Governance is a runtime decision. Anything else is paper.
