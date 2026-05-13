# Data Schema Library — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DATA_SCHEMA_LIBRARY_AR.md](./DATA_SCHEMA_LIBRARY_AR.md)

## Context
Dealix workflows operate on a small set of recurring datasets across
every engagement. To prevent re-inventing field names, types, and
validation rules in every project, this library defines the canonical
schemas. It plugs into `docs/BEAST_LEVEL_ARCHITECTURE.md` for the data
pipeline, into `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` for the
backend storage layer, and into `docs/AI_STACK_DECISIONS.md` for prompt
engineering and validation. Every dataset used in a Dealix engagement
must declare which library schema it conforms to.

## Conventions
- Snake_case field names.
- ISO 8601 dates and timestamps.
- Phone numbers in E.164.
- Required fields are marked `(required)`. Other fields are optional.
- PII fields are marked `(PII)` and trigger the rules in
  `docs/governance/PDPL_DATA_RULES.md`.

## AccountSchema
Business account / company record used in revenue, customer, and ops
workflows.

```json
{
  "company_name": "string (required)",
  "sector": "string (required)",
  "city": "string (required)",
  "source_type": "enum: referral|public|enrichment|client_supplied (required)",
  "allowed_use": "enum: research|outreach|service_delivery|none (required)",
  "relationship_status": "enum: cold|consented|existing_relationship|do_not_contact (required)",
  "website": "string",
  "contact_role": "string",
  "email": "string (PII)",
  "phone": "string (PII)",
  "estimated_size": "enum: 1-10|11-50|51-200|201-1000|1000+",
  "last_interaction_date": "date",
  "notes": "string (required)"
}
```

## LeadSchema
Extends AccountSchema with sales pipeline fields.

```json
{
  "$extends": "AccountSchema",
  "stage": "enum: new|qualified|engaged|opportunity|won|lost (required)",
  "owner": "string (required)",
  "source_event": "string (required)"
}
```

## SupportMessageSchema
Inbound customer message.

```json
{
  "message_id": "string (required)",
  "channel": "enum: whatsapp|email|web|phone (required)",
  "timestamp": "datetime (required)",
  "customer_type": "enum: existing|prospect|unknown (required)",
  "category": "string",
  "resolution_status": "enum: open|in_progress|resolved|escalated"
}
```

## DocumentSchema
Internal document used for the Company Brain.

```json
{
  "doc_id": "string (required)",
  "title": "string (required)",
  "owner": "string (required)",
  "last_updated": "date (required)",
  "sensitivity": "enum: low|medium|high (required)",
  "source_type": "enum: policy|sop|playbook|contract|email|other (required)",
  "allowed_users": ["string"]
}
```

## ProjectSchema
A Dealix engagement record.

```json
{
  "project_id": "string (required)",
  "client_id": "string (required)",
  "service_id": "string (required)",
  "start_date": "date (required)",
  "end_date": "date",
  "capability_targets": ["string"],
  "owners": ["string"]
}
```

## Versioning
- Schema versions follow semantic versioning. Adding optional fields is
  a minor change; renaming or removing fields is a major change.
- Major changes require a written migration note in the change log and
  parallel propagation to the Arabic mirror.
- Every dataset in production must declare its schema version.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client raw data | Conformed dataset | Data lead | Per dataset |
| Schema PR | Validated schema version | Data lead | Per change |
| Schema version tag | Pipeline migration plan | Backend lead | Per major change |

## Metrics
- **Schema conformance rate** — datasets in production that match a
  library schema. Target: 100%.
- **Schema fork count** — number of project-local schema variants
  outside the library. Target: 0.
- **Migration latency** — days from major version release to all
  pipelines migrated. Target: ≤ 30 days.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — data pipeline architecture.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — backend storage and
  validation layer.
- `docs/AI_STACK_DECISIONS.md` — model and prompt decisions that rely
  on these schemas.
- `docs/data/DATA_READINESS_STANDARD.md` — readiness standard that
  references these schemas.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
