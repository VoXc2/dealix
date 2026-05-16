# Governance Agent Permissions

## Permission Scope

- Namespace: `governance_agent`
- Default profile: `default_governance_agent`
- Deny by default outside explicit allowlist.

## Required Permissions

| Permission | Purpose | Gate ID | Test ID |
|---|---|---|---|
| governance_agent.run | execute assigned tasks | G-AGT-GOV-030 | T-AGT-GOV-030 |
| governance_agent.read | access scoped context | G-AGT-GOV-031 | T-AGT-GOV-031 |
| governance.request_approval | request human decision for high risk | G-AGT-GOV-032 | T-AGT-GOV-032 |

## Hard Denials

- No direct external messaging without approval token.
- No cross-tenant data retrieval.
- No policy override by prompt instruction.
