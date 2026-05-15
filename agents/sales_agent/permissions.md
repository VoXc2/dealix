# Sales Agent Permissions

## Permission Scope

- Namespace: `sales_agent`
- Default profile: `default_sales_agent`
- Deny by default outside explicit allowlist.

## Required Permissions

| Permission | Purpose | Gate ID | Test ID |
|---|---|---|---|
| sales_agent.run | execute assigned tasks | G-AGT-SLS-030 | T-AGT-SLS-030 |
| sales_agent.read | access scoped context | G-AGT-SLS-031 | T-AGT-SLS-031 |
| governance.request_approval | request human decision for high risk | G-AGT-SLS-032 | T-AGT-SLS-032 |

## Hard Denials

- No direct external messaging without approval token.
- No cross-tenant data retrieval.
- No policy override by prompt instruction.
