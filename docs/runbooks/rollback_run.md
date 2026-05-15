# Runbook: Rollback Run

1. Create rollback request with `tenant_id`, `run_id`, reason, actor.
2. Verify approval ticket appears in oversight queue.
3. Grant approval by authorized operator.
4. Finalize rollback with granted `ticket_id`.
5. Verify trace contains `rollback_requested`, `approval_granted`, `rollback_finalized`.
