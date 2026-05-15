# Cross-Layer Validation

## Golden path
Lead intake → agent route → contract evaluate → control run register → approval escalation (if risk) → approval grant → value metric record → trace export.

## Validation matrix
- **Runtime import:** `api.main` import and route registration.
- **Governance:** `runtime_decision.decide` + assurance contracts.
- **Execution:** control-plane state transitions and audit events.
- **Safety:** kill switch propagation and circuit breakers.
- **Value:** source discipline for measured/verified tiers.
- **Evolution:** propose-only with approval gate before apply.
