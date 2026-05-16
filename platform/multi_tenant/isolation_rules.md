# Isolation Rules

## Request Path

1. Resolve `tenant_id` from trusted source.
2. Stamp `tenant_id` into request context.
3. Enforce object-level tenant match before response.

## Data Path

- SQL queries must filter by `tenant_id`.
- Vector retrieval must include tenant namespace filters.
- Cache keys must be tenant-prefixed.

## Logging Path

- logs include `tenant_id` and `trace_id`.
- audit logs are tenant-scoped by default.

## Workflow Path

- each workflow instance carries immutable `tenant_id`.
- retries and compensation cannot switch tenant context.

## Rejection Policy

أي غموض في ملكية البيانات => reject by default.
