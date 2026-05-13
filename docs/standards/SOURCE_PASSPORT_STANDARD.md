# Source Passport Standard

## Canonical schema

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "relationship_status": "existing_relationship",
  "retention_policy": "project_duration",
  "ai_access_allowed": true,
  "external_use_allowed": false
}
```

## Five rules

- No Source Passport = no AI use.
- No allowed use = internal analysis only.
- PII + unclear basis = redact or block.
- External action = approval required.
- Unknown source = no outreach.

Typed: `global_grade_os.enterprise_trust.SourcePassport` + `institutional_control_os.source_passport.enforce_source_passport_use()`.
