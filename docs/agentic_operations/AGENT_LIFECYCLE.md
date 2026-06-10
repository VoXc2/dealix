# Agent Lifecycle

المراحل: Proposed → Reviewed → Approved → Registered → Tested → Deployed → Monitored → Reviewed Monthly → Restricted/Expanded → Decommissioned.

## لا deploy بدون

- Agent Identity Card  
- Permission Card  
- Auditability Card  
- Governance tests  
- Owner  
- Decommission rule  

## Decommission Rule (مرجع JSON)

```json
{
  "agent_id": "AGT-REV-001",
  "decommission_if": [
    "owner_removed",
    "policy_violation",
    "unused_for_90_days",
    "repeated_low_qa_score",
    "permission_boundary_violation"
  ]
}
```

## الكود

`auto_client_acquisition/agentic_operations_os/agent_lifecycle.py`
