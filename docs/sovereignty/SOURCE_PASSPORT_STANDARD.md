# Source Passport Standard

The Source Passport is the canonical record for **every** dataset that enters Dealix.

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

## 2. Field definitions

| Field | Definition |
| --- | --- |
| `source_id` | Stable Dealix identifier; never reused |
| `source_type` | `client_upload`, `client_system`, `licensed_public`, `partner_share`, etc. |
| `owner` | The legal owner (e.g., `client`, `partner`, `dealix`) |
| `allowed_use` | One or more of `internal_analysis`, `draft_only`, `approved_external`, `aggregated_benchmark`, `public_publication` |
| `contains_pii` | Boolean |
| `sensitivity` | `public`, `internal`, `confidential`, `restricted` |
| `relationship_status` | `existing_relationship`, `new_lead`, `no_relationship` |
| `retention_policy` | e.g., `project_duration`, `12_months`, `client_dictated` |
| `ai_access_allowed` | Whether AI can read this source at all |
| `external_use_allowed` | Whether outputs derived from this source can leave the system |

Optional but recommended: `residency`, `license`, `refresh_cadence`, `last_reviewed_at`.

## 3. Lifecycle

1. **Created** at engagement intake.
2. **Reviewed** when allowed use, sensitivity, or PII status changes.
3. **Revoked** when retention expires or the client requests removal.

## 4. Operating discipline

- Passports are required, not optional.
- A passport without an active owner is rejected.
- A passport edit creates an audit event; previous versions are retained.
- The governance runtime reads the passport at every access decision.

## 5. Why standardize the passport

- Multiple engagements share one schema, which makes governance composable.
- Partner and academy participants can adhere to a single discipline.
- Public benchmarks can be built only from passports that explicitly permit it.
- The auditor needs one document, not many.

## 6. Anti-patterns

- “Lightweight” passports without sensitivity or PII fields.
- Free-text allowed-use that the runtime cannot evaluate.
- Stale passports that have not been reviewed in months.
- Shared passport templates across tenants that pre-fill allowed_use.

## 7. The principle

> Every dataset, every time. The passport is the price of admission to Dealix.
