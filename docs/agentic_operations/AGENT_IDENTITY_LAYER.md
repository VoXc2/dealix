# Agent Identity Layer

## Agent Identity Card (مرجع JSON)

```json
{
  "agent_id": "AGT-REV-001",
  "name": "Revenue Intelligence Agent",
  "business_unit": "Dealix Revenue",
  "owner": "Revenue Owner",
  "purpose": "Score accounts, identify opportunities, and generate draft-only outreach recommendations.",
  "autonomy_level": 3,
  "status": "active",
  "created_at": "2026-05-14",
  "last_reviewed_at": "2026-05-14"
}
```

## القواعد

- **No identity = no agent.**  
- **No owner = no agent.**  
- **No purpose = no agent.**

## الكود

`auto_client_acquisition/agentic_operations_os/agent_identity.py`
