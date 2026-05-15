# RBAC Requirements (Release 1)

## Objective

Control who can do what per tenant before serving any pilot customer.

## Minimum pilot identity model

- Tenant: `Demo Real Estate Co` (example)
- Users: `owner`, `sales_manager`, `agent_operator`
- Roles (minimum two):
  - `sales_manager`
  - `agent_operator`

The owner may map to tenant admin in early pilot operations.

## RBAC policy requirements

1. Every API action must map to a permission string.
2. Every request must authenticate actor identity before authorization.
3. Authorization decisions must evaluate:
   - tenant match
   - role permissions
   - system-role override (if applicable)
4. High-risk actions must not rely on role alone; they also require governance checks.

## Permission model baseline

- `sales_manager`: lead/deal lifecycle, reporting, supervised agent operations
- `agent_operator`: agent run operations within approved boundaries, no external send without policy pass
- `tenant_admin` (optional in pilot hardening): tenant settings, user/role administration

## API design standard

1. Endpoint handler declares minimum role/permission.
2. Service layer re-checks critical permissions for defense in depth.
3. Denials return explicit reason code and are audit-logged.

## Acceptance checklist (Release 1)

- [ ] One tenant contains exactly the pilot user set
- [ ] Two baseline roles are configured and mapped
- [ ] Permission matrix exists for every pilot API used in workflow
- [ ] Unauthorized actions are denied and logged
- [ ] Role changes are auditable
