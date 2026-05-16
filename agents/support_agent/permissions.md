# Support Agent Permissions

## Permission Scope

- Namespace: `support_agent`
- Default profile: `default_support_agent`
- Deny by default outside explicit allowlist.

## Required Permissions

| Permission | Purpose | Gate ID | Test ID |
|---|---|---|---|
| support_agent.run | execute assigned tasks | G-AGT-SUP-030 | T-AGT-SUP-030 |
| support_agent.read | access scoped context | G-AGT-SUP-031 | T-AGT-SUP-031 |
| governance.request_approval | request human decision for high risk | G-AGT-SUP-032 | T-AGT-SUP-032 |

## Hard Denials

- No direct external messaging without approval token.
- No cross-tenant data retrieval.
- No policy override by prompt instruction.
