# Runbook: Investigate Failed Workflow

1. Fetch workflow trace by `tenant_id` + `run_id`.
2. Identify first failing event and upstream decision.
3. Check approval and contract state for that action.
4. Check runtime safety status (kill switch / breaker).
5. Execute rollback drill if required and safe.
6. Document root cause and remediation controls.
