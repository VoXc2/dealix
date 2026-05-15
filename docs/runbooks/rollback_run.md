# Runbook: Rollback a Workflow Run

1. Create rollback approval ticket for target `run_id`.
2. Wait for human grant.
3. Finalize rollback with granted ticket.
4. Verify run state is `rolled_back`.
5. Verify trace contains `rollback.requested` and `rollback.finalized`.
