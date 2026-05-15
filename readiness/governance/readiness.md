# Governance Layer — readiness

- Owner: `Governance + Compliance`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `approval_sla_minutes`
  - `policy_violation_rate`
  - `audit_trail_completeness_rate`
  - `compliance_check_pass_rate`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `approvals_enforced` — Approval matrix and approval engine are enforced.
  - [ ] `audit_trails_complete` — Audit trail is modeled and exported.
  - [ ] `policies_versioned` — Policy registries/rules are centrally organized.
  - [ ] `risk_scoring_working` — Risk scoring and runtime decision are available.
  - [ ] `compliance_checks_passing` — Compliance rule engine has test coverage.

