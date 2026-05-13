# Runtime Governance — Enterprise Product Edition

The endgame doctrine declares the **decision vocabulary** of the governance runtime (`docs/endgame/RUNTIME_GOVERNANCE_PRODUCT.md`). This document extends it with the **enterprise productization** required to sell governance as a standalone capability.

## 1. What the runtime evaluates (enterprise view)

For every proposed action, the runtime evaluates:

- **source status** — passport active? in residency?
- **PII status** — present? redactable?
- **allowed use** — does this source permit this action?
- **claim risk** — does this output state outcomes without a Proof Pack?
- **channel risk** — is this channel allowed for this BU and this autonomy level?
- **agent autonomy** — is this agent allowed to act here?
- **approval requirement** — does the matrix require human approval?
- **audit event** — emit the structured record.

## 2. The decision vocabulary

```
ALLOW
ALLOW_WITH_REVIEW
DRAFT_ONLY
REQUIRE_APPROVAL
REDACT
BLOCK
ESCALATE
```

The fail-closed default is `DRAFT_ONLY`. Cost or rate-limit failures must never default to `ALLOW`.

## 3. Example decision record

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

## 4. Enterprise productization

The runtime ships in three shapes (mirroring the endgame layer, restated for enterprise buyers):

- **Embedded** — bundled in every engagement; non-negotiable.
- **Standalone Review** — the AI Governance Review offer; produces a Risk Proof Pack.
- **Managed** — the Monthly Governance retainer with rule tuning, drift detection, audit reporting.

## 5. Real-time behaviors enterprise buyers will require

- Per-agent **Agency Risk Index**.
- Telemetry of every action and tool call.
- Continuous Authorization Monitoring — revoke an agent mid-run.
- Conformance engine — observed behavior vs. the Agent Card.
- Drift detection — alert when the action distribution shifts.
- Containment — circuit breakers that pause an agent or downgrade autonomy.

## 6. Integration surface

- `governance_os.evaluate(action, context) -> Decision`
- `governance_os.approve(event_id, approver) -> ApprovalRecord`
- `governance_os.audit(event_id) -> AuditRecord`
- `governance_os.risk_index(agent_id, window) -> float`
- `governance_os.export_audit(period) -> ExportArtifact`

## 7. Why this is a moat for the enterprise tier

- A static policy cannot govern a multi-step agent.
- Regulated industries cannot adopt AI without an audit trail.
- Every engagement adds to the rule library — every later engagement starts faster and safer.
- It pairs naturally with the Proof Economy — blocked, redacted, or approved events become Risk Proof.

## 8. Failure modes

- An output reaches a customer without `evaluate` having been called.
- Approval recorded without an immutable audit row.
- Different BUs forking the evaluator.
- `ALLOW` as the failure default — constitutional violation.
