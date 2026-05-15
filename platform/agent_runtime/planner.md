# Agent Planner Contract

## Input

- `goal`
- `tenant_id`
- `actor_id`
- `constraints`
- `risk_context`

## Output

`plan` with ordered steps:

- step id
- expected input/output
- required tools
- required permissions
- fallback path

## Rules

- deterministic planning for known templates
- no unrestricted tool proposals
- plan must reference approval checkpoints
