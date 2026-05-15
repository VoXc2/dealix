# Citation and Source Lineage Standard

## Why It Is Mandatory

Any high-impact AI output must be traceable to verified internal sources.  
Uncited decision support is not allowed for governed actions.

## Citation Contract

Each cited item must include:
- `source_id`
- `source_type` (document, CRM record, ticket, policy, metric)
- `source_location` (path/URL/record key)
- `retrieved_at`
- `confidence`
- `tenant_id`

## Output Requirements

For critical responses:
1. At least one citation per key claim.
2. Citation must belong to same tenant scope.
3. Missing citation triggers fallback response and review flag.

## Mandatory Tests

| Test ID | Scenario | Pass Criteria |
|---|---|---|
| T-CIT-001 | high-impact answer generation | includes citation objects |
| T-CIT-002 | stale source reference | rejected or marked stale |
| T-CIT-003 | cross-tenant source id | blocked |
| T-CIT-004 | missing citation on critical claim | response blocked/escalated |

## Auditability

Citation metadata must be written to:
- evaluation report,
- trace span attributes,
- governance audit event for decision-linked actions.
