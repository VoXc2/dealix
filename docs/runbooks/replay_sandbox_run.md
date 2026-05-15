# Runbook: Replay Sandbox Run

1. Export original run trace and event payloads.
2. Rehydrate into sandbox environment with same tenant context.
3. Replay step-by-step without external side effects.
4. Compare resulting control events against original.
5. Mark drift and attach findings to incident review.
