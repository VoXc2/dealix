# Sales Agent Rollback

## Rollback policy

1. Stop current workflow run (state: blocked or paused).
2. Revoke pending external actions from approval queue.
3. Mark failed run with root-cause tag in audit.
4. Re-run from last safe checkpoint with corrected policy/tool binding.

## Safety rule

Rollback never auto-executes external compensating actions without explicit approval.
