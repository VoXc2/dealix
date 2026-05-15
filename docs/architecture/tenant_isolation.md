# Tenant Isolation

## Core rule

Every operational object includes `tenant_id` and tenant-scoped repositories filter by `(tenant_id, object_id)` keys.

## Covered objects

- Workflow runs
- Control events
- Approval tickets
- Agent descriptors
- Assurance contracts
- Runtime safety states
- Value engine metrics
- Improvement proposals

Cross-tenant reads and writes are denied by repository boundaries and tested.
