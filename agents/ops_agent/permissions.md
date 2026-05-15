# Ops Agent Permissions

## Permission Scope

- Namespace: `ops_agent`
- Default profile: `default_ops_agent`
- Deny by default outside explicit allowlist.

## Required Permissions

| Permission | Purpose | Gate ID | Test ID |
|---|---|---|---|
| ops_agent.run | execute assigned tasks | G-AGT-OPS-030 | T-AGT-OPS-030 |
| ops_agent.read | access scoped context | G-AGT-OPS-031 | T-AGT-OPS-031 |
| governance.request_approval | request human decision for high risk | G-AGT-OPS-032 | T-AGT-OPS-032 |

## Hard Denials

- No direct external messaging without approval token.
- No cross-tenant data retrieval.
- No policy override by prompt instruction.
