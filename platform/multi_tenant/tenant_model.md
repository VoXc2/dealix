# Tenant Model (Dealix)

## Core Entities

- `tenant`
- `tenant_user`
- `tenant_role_binding`
- `tenant_data_boundary`
- `tenant_audit_stream`

## Mandatory Fields

كل record مرتبط بعميل يجب أن يحتوي:

- `tenant_id`
- `created_at`
- `created_by`
- `updated_at`
- `updated_by`

## Isolation Principle

لا يسمح بأي:

- shared memory بين tenants
- shared vector namespaces
- shared workflow state
- shared audit logs

## Super Admin Rule

وصول `super_admin` عبر tenants مسموح فقط عند:

- break-glass justification
- explicit audit event
- bounded session window
