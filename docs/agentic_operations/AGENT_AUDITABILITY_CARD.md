# Agent Auditability Card

## مرجع JSON

```json
{
  "agent_id": "AGT-REV-001",
  "audit_scope": ["inputs", "tool_calls", "policy_checks", "outputs", "human_reviews", "approvals"],
  "action_recoverability": "required",
  "lifecycle_coverage": "created_modified_decommissioned",
  "policy_checkability": "required",
  "responsibility_attribution": "required",
  "evidence_integrity": "append_only_logs_mvp",
  "external_actions_allowed": false
}
```

## الكود

`auto_client_acquisition/agentic_operations_os/agent_auditability_card.py`
