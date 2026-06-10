# Agent Governance Runtime

قبل أي إجراء من الوكيل يُفحص: الهوية، مستوى الاستقلالية، أداة، جواز مصدر، PII، allowed use، سياسة قناة، مخاطر ادّعاء، حاجة موافقة.

## Governance Decision (مرجع JSON)

```json
{
  "agent_id": "AGT-REV-001",
  "proposed_action": "generate_whatsapp_draft",
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "matched_rules": ["pii_requires_review", "external_action_requires_approval", "no_cold_whatsapp_automation"],
  "allowed_next_step": "create draft for human review only"
}
```

## الكود

`auto_client_acquisition/agentic_operations_os/agent_governance.py`
