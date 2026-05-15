# Agent Permission Layer

## Permission Card (مرجع JSON)

```json
{
  "agent_id": "AGT-REV-001",
  "allowed_inputs": ["client_uploaded_accounts", "approved_public_data", "source_passported_datasets"],
  "allowed_tools": ["classify_accounts", "score_accounts", "generate_draft_pack", "summarize_opportunities"],
  "forbidden_tools": ["send_email", "send_whatsapp", "scrape_web", "linkedin_automation", "export_pii"],
  "requires_approval_for": ["outputs_containing_pii", "external_action_recommendations", "client-facing_claims"]
}
```

## قواعد الصلاحيات

- **Least privilege** افتراضيًا.  
- **رفع مؤقت** للصلاحية فقط بموافقة وتدقيق.  
- **أي تغيير صلاحية** = حدث audit.  
- **طلب صلاحية جديد من الوكيل** = risk signal.

## الكود

`auto_client_acquisition/agentic_operations_os/agent_permissions.py`
