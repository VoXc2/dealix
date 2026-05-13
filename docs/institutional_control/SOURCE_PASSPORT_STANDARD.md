# Source Passport Standard (Institutional Edition)

The institutional edition extends `docs/sovereignty/SOURCE_PASSPORT_STANDARD.md` with the enforcement rules that gate every AI access.

## 1. Canonical schema

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

## 2. Enforcement rules

- **No Source Passport** → no AI use.
- **No allowed use** → internal analysis only.
- **PII + unclear basis** → redact or block.
- **External action** → approval required.
- **Unknown source** → no outreach.

Each rule maps to a `governance_os` evaluator that fires at the relevant call site.

## 3. Why this is institutional

Regional and global studies of digital privacy disclosure indicate that only a minority of organizations expose complete privacy disclosures by default. Dealix turns that gap into a trust feature by making source passports a hard precondition.

## 4. Lifecycle

1. **Created** at engagement intake.
2. **Reviewed** when allowed use, sensitivity, or PII status changes.
3. **Revoked** when retention expires or the client requests removal.

## 5. Operating discipline

- Passports are required, not optional.
- A passport without an active owner is rejected.
- A passport edit creates an audit event; previous versions are retained.
- The governance runtime reads the passport at every access decision.

## 6. Anti-patterns

- "Lightweight" passports without sensitivity or PII fields.
- Free-text allowed-use that the runtime cannot evaluate.
- Stale passports that have not been reviewed in months.
- Shared passport templates pre-filling allowed_use across tenants.

## 7. The principle

> Every dataset, every time. The passport is the price of admission to Dealix.
