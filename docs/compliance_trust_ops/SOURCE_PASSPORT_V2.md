# Source Passport v2

## مثال JSON

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "collection_context": "uploaded_for_revenue_analysis",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "relationship_status": "existing_relationship",
  "ai_access_allowed": true,
  "external_use_allowed": false,
  "retention_policy": "project_duration",
  "deletion_required_after": "contract_end"
}
```

## قواعد

No Source Passport = no AI use.  
No allowed use = تحليل داخلي فقط.  
PII + external = موافقة.  
مصدر مجهول = لا outreach.

**الكود:** `SourcePassportV2` · `source_passport_v2_valid` — `compliance_trust_os/source_passport_v2.py`

**صعود:** [`AI_AGENT_COMPLIANCE.md`](AI_AGENT_COMPLIANCE.md)
