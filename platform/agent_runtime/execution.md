# Agent Execution Contract

## Required Runtime Envelope

- `run_id`
- `agent_id`
- `tenant_id`
- `trace_id`
- `plan_id`
- `policy_version`

## Execution Steps

1. resolve permissions
2. run policy checks
3. execute allowed tool calls
4. capture outputs + citations
5. run validation gates
6. route for approval when required

## Forbidden

- direct external sends without approval
- unscoped memory access
- tool invocation outside policy envelope
