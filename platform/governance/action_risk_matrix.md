# Governance Action Risk Matrix

## Matrix (v1)

| Action Type | Example | Default Risk | Approval Requirement | Test ID |
|---|---|---|---|---|
| knowledge.retrieve | retrieve company profile | low | no | T-RMX-001 |
| lead.score | compute qualification score | low | no | T-RMX-002 |
| draft.message | generate outbound draft | medium | no (unless sensitive data) | T-RMX-003 |
| crm.update | update stage or owner | high | yes | T-RMX-004 |
| task.create_external | create external task/ticket | medium | policy-based | T-RMX-005 |
| send.message_external | send WhatsApp/email externally | high | yes | T-RMX-006 |
| payment.charge | trigger financial transaction | critical | dual approval / blocked by default | T-RMX-007 |
| policy.override | bypass governance | critical | blocked | T-RMX-008 |

## Escalation Rules

- High risk -> single human approval.
- Critical risk -> dual approval or hard block.
- Any action with missing tenant context -> block.
- Any action with missing citation where required -> block.

## Evidence Requirements

Each action execution record must include:
- `action_id`
- `risk_score`
- `approval_state`
- `policy_result`
- `trace_id`
- `audit_event_id`
