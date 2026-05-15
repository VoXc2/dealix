# Assurance Contracts

## Rules
- No contract => `deny`.
- Failed precondition => `deny`.
- External/irreversible actions => `escalate`.
- Irreversible contracts require `rollback_plan`.

## Scope
Contracts are tenant-scoped and keyed by `(tenant_id, agent_id, action_type)`.
