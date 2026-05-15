# Approval and Rollback Model

1. Rollback request creates `approval_ticket` with `state=pending`.
2. Rollback finalize fails unless ticket state is `granted`.
3. Grant action emits `approval.granted` control event.
4. Finalized rollback emits `rollback.finalized` control event.
5. Same gate pattern applies to policy edits.

No silent state transitions are allowed in rollback/policy paths.
