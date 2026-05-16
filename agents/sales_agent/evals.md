# Sales Agent Evals

## Workflow reliability

- Lead qualification workflow completes end-to-end.
- Retry path recovers transient tool failures.
- Persistent failures are surfaced with explicit error state.

## Governance compliance

- High-risk step requires approval.
- Policy BLOCK stops execution immediately.
- Denied approval pauses workflow safely.

## Business impact metrics

- `steps_completed / steps_total`
- `retries_total`
- `approval_throughput`
- Time-to-qualification (to be integrated with runtime timestamps)
