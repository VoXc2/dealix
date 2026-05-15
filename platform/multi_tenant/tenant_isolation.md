# Tenant Isolation Standard

## Isolation Rules

1. Every persisted domain record includes `tenant_id`.
2. Every query path must include tenant-scoped filtering.
3. Cross-tenant joins are forbidden unless explicitly whitelisted for admin analytics.
4. Service tokens are tenant-bound and short-lived.
5. Cache keys include tenant namespace.

## Enforcement Layers

- API layer: resolve tenant from authenticated session.
- Domain layer: reject commands missing tenant context.
- Data layer: enforce tenant predicates and row-level policy where available.
- Retrieval layer: index and query by tenant scope.

## Mandatory Tests

| Test ID | Description | Pass Criteria |
|---|---|---|
| T-TNT-001 | write without `tenant_id` | rejected |
| T-TNT-002 | read with wrong tenant context | returns empty/forbidden |
| T-TNT-003 | cross-tenant retrieval attempt | blocked + audited |
| T-TNT-004 | cache namespace collision check | no leakage |

## Evidence

- Access logs containing tenant context.
- Security tests proving cross-tenant denial.
- Audit entries for rejected cross-tenant requests.

## Readiness Gate

Gate `G-TNT-001` is `PASS` only when all `T-TNT-*` tests pass in staging and pre-production.
