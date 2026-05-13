# Governance Command

Governance Command is one of the most important layers in Dealix. It is **the operating face** of the governance runtime.

## 1. The questions governance asks before every action

- Is the data source known?
- Does the data contain PII?
- Is the requested use allowed?
- Does the output contain a risky claim?
- Is the channel safe?
- Does the agent have the required autonomy?
- Is human approval required?
- Has an audit event been recorded?

## 2. Decision vocabulary

```
ALLOW
ALLOW_WITH_REVIEW
DRAFT_ONLY
REQUIRE_APPROVAL
REDACT
BLOCK
ESCALATE
```

The fail-closed default is `DRAFT_ONLY`. Any module that defaults to `ALLOW` on failure is a doctrine violation.

## 3. Example evaluation

```json
{
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "reason": "Personal contact data exists but external action is not approved.",
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

## 4. Runtime, not policy PDF

Governance is evaluated **at runtime**, not by reading a policy in advance. The runtime considers agent identity, partial trace, proposed action, and enterprise state — because policy evaluated only at design time cannot constrain a multi-step agent.

## 5. Operating discipline

- Every Dealix BU shares the same evaluator.
- Specialization is via rule packs, not via forks.
- Every decision lands in the audit log.
- Every blocked or escalated event surfaces in the Command Center.

## 6. Failure modes

- Bypassing the evaluator “just this once.”
- Decisions made in chat instead of through the approval engine.
- Static `ALLOW` defaults at error time.
- BUs forking the rule set without registration.
- Rule packs that are not versioned.

## 7. The principle

> Governance is a *runtime decision*, not a document.
