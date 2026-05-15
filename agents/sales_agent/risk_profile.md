# Sales Agent Risk Profile

## Risk level

`medium`

## Primary risks

- Incorrect qualification score drives wrong sales prioritization.
- Unauthorized external commit to CRM.
- Tool failure leading to silent data loss.

## Runtime controls

- Risk scoring per step.
- Policy decision per step.
- Approval gate for external commit.
- Retry budget with deterministic fail state.
- Full audit records for each governance stage.
