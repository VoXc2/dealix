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

## Control IDs (EXE)

| Type | ID | Purpose |
|---|---|---|
| Gate | G-EXE-001 | Minimum release gate for execution engine architecture |
| Evidence | E-EXE-001 | Architecture evidence record for release review |
| Test | T-EXE-001 | Architecture conformance test |

