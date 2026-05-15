# Workflow Execution DAGs

كل workflow يجب أن يكون versioned وauditable وretryable.

## Required Blocks

- trigger
- conditions
- actions
- approvals
- retries
- compensation
- analytics

## Required Metadata

- `workflow_id`
- `workflow_version`
- `tenant_id`
- `idempotency_key`
- `policy_version`
