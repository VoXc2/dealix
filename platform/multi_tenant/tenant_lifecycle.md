# Tenant Lifecycle

## States

1. `provisioning`
2. `active`
3. `suspended`
4. `offboarding`
5. `archived`

## Provisioning Checklist

- tenant identity created
- default RBAC roles assigned
- policy baseline attached
- observability tags configured
- audit stream enabled

## Suspension

- block external actions
- keep read-only audit visibility
- preserve evidence and logs

## Offboarding

- export permitted data artifacts
- revoke credentials
- finalize audit snapshot
- retain compliance evidence window
