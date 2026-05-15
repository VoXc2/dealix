# Scope

This service productizes Dealix's internal governance modules
([`auto_client_acquisition/governance_os/`](../../../auto_client_acquisition/governance_os/),
[`compliance_trust_os/`](../../../compliance_trust_os/)) for a client company.

## Included

- company-wide AI policy aligned to PDPL principles
- AI risk matrix across departments and use cases
- approval classes and data-handling rules
- employee AI usage rules and guidance
- audit logging design + human-approval workflows
- PDPL readiness assessment (gap analysis, not certification)
- vendor / model risk review for current AI tools
- executive governance dashboard specification
- readiness review against agreed criteria

## Excluded

- legal advice or legal sign-off (external counsel)
- formal PDPL certification or regulatory filing
- full technical penetration test
- building every technical control in-product (separately scoped)
- multi-entity / group-wide rollout beyond the agreed company

## Hard Gates

This program operates strictly within Dealix gates: `no_live_send`,
`no_live_charge`, `no_cold_whatsapp`, `no_scraping`, `no_fake_proof`.

See also: [`offer.md`](offer.md) · [`../ai_governance_program/scope.md`](../ai_governance_program/scope.md).
