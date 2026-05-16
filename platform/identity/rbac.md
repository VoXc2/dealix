# Identity and RBAC Model

## Objective

Ensure every action is authorized by tenant, role, and permission policy before execution.

## Role Model (Initial)

- `owner`: full tenant-level control including approvals.
- `manager`: can run workflows and approve medium-risk actions.
- `operator`: can execute low-risk actions only.

## Permission Pattern

Permission key format:

`<domain>.<resource>.<action>`

Examples:
- `sales.lead.qualify`
- `governance.approval.grant`
- `execution.crm.update`

## Authorization Gates

| Gate ID | Control | Test ID |
|---|---|---|
| G-RBAC-001 | deny by default | T-RBAC-001 |
| G-RBAC-002 | role -> permission mapping validated | T-RBAC-002 |
| G-RBAC-003 | forbidden action returns explicit denial reason | T-RBAC-003 |
| G-RBAC-004 | auth decision is audited | T-RBAC-004 |

## Session Contract

Every request context must include:
- `tenant_id`
- `user_id`
- `roles[]`
- `permissions[]`
- `session_id`

Missing any field -> request rejected.

## Evidence

- RBAC policy file version and checksum.
- Authorization test report.
- Audit log records for allow/deny decisions.
