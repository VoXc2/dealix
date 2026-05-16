# Executive Agent Permissions

## Permission Scope

- Namespace: `executive_agent`
- Default profile: `default_executive_agent`
- Deny by default outside explicit allowlist.

## Required Permissions

| Permission | Purpose | Gate ID | Test ID |
|---|---|---|---|
| executive_agent.run | execute assigned tasks | G-AGT-EXC-030 | T-AGT-EXC-030 |
| executive_agent.read | access scoped context | G-AGT-EXC-031 | T-AGT-EXC-031 |
| governance.request_approval | request human decision for high risk | G-AGT-EXC-032 | T-AGT-EXC-032 |

## Hard Denials

- No direct external messaging without approval token.
- No cross-tenant data retrieval.
- No policy override by prompt instruction.
