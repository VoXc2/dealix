# Foundation Architecture

## Scope

Foundation provides secure multi-tenant runtime primitives:
- identity context,
- tenant boundaries,
- environment separation,
- auditability,
- backup/restore,
- deployment rollback.

## Core Components

1. Identity resolver (`tenant_id`, `user_id`, `role`).
2. Policy-aware request middleware.
3. Tenant-safe persistence contracts (`tenant_id` required).
4. Audit event writer for all privileged actions.
5. Deployment pipeline with immutable version tags.
6. Backup + restore workflow with verification tests.

## Mandatory Foundation Gates

| Gate ID | Control | Test ID |
|---|---|---|
| G-FND-001 | All business entities carry `tenant_id` | T-FND-001 |
| G-FND-002 | Tenant boundary enforced in reads/writes | T-FND-002 |
| G-FND-003 | RBAC enforcement active on protected routes | T-FND-003 |
| G-FND-004 | Audit logs emitted for privileged actions | T-FND-004 |
| G-FND-005 | Backup and restore validated | T-FND-005 |
| G-FND-006 | Rollback drill validated | T-FND-006 |

## Deployment Model

- Environments: `dev` -> `staging` -> `production`.
- Promotion requires readiness gates + eval checks.
- Rollback uses previous signed release artifact and data safety checks.

## Evidence Artifacts

- Schema and migration checks proving `tenant_id` presence.
- Access control test reports.
- Backup/restore logs.
- Rollback drill report.
- Audit log samples with actor and reason.
