# sales_agent Permissions

## Scope

All permissions are tenant-scoped only.

## Allowed

- `lead:read:tenant`
- `lead:score:tenant`
- `knowledge:retrieve:tenant`
- `response:draft:tenant`
- `workflow:run:tenant`
- `approval:request:tenant`
- `audit:write:tenant`
- `metrics:write:tenant`

## Conditionally Allowed (requires approved policy path)

- `crm:update:tenant`

Condition:

1. Risk evaluation completed.
2. Policy check passed.
3. Approval check passed for medium/high actions.

## Explicitly Denied

- `message:send_external:any`
- `calendar:create_external:any`
- `lead:read:any` (cross-tenant)
- `policy:manage:tenant`

## Break-glass

No break-glass override in v0.1.0 for external actions.
