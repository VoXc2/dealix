# Execution Engine Architecture

The execution engine performs external side-effect actions after governance approval:
- CRM updates
- outbound messages
- task creation

## Safety Requirements

- idempotent action execution
- policy/approval token validation
- compensation on failure
- audit log emission
