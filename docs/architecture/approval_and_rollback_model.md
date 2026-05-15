# Approval and Rollback Model

## Model
- Rollback request creates approval ticket.
- Rollback finalize is blocked until ticket state is `approved`.
- Policy edits follow the same request→grant→finalize pattern.

## Auditability
Each transition emits a control event:
- `rollback_requested`
- `approval_granted`
- `rollback_finalized`
- `policy_edit_requested`
- `policy_edit_finalized`
