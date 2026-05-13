---
title: Audit Log Policy — Events, Retention, Queryability
doc_id: W6.T37.audit-log
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W3.T07b, W4.T14]
kpi:
  metric: audit_log_coverage
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: governance-foundation
---

# Audit Log Policy

## 1. Context

A queryable, complete audit log is what makes Dealix's governance claims
verifiable. Without it, every Trust statement is a promise; with it, every
statement is a fact a regulator or customer DPO can reproduce.

This policy sets what is logged, how long it is kept, who can query it,
and what coverage targets must hold.

## 2. Audience

Engineers (must emit events from every policy-relevant action), HoLegal /
DPO (queries the log for DSAR, incident response, regulator inquiry),
HoCS (uses the log during delivery for compliance gate evidence).

## 3. What Gets Logged

Every policy-relevant event. Canonical kinds:

| Category | Example events |
|----------|----------------|
| Identity & access | `user_login`, `role_changed`, `bypass_token_issued` |
| Data processing | `record_ingested`, `pii_detected`, `pii_redacted`, `pii_blocked` |
| Consent & legal basis | `consent_recorded`, `consent_withdrawn`, `lawful_basis_set` |
| Approvals | `action_proposed`, `action_approved`, `action_rejected` |
| Outbound | `message_sent`, `public_post_published`, `external_api_write_completed` |
| Project / delivery | `stage_entered`, `qa_evaluated`, `handoff_signed`, `renewal_decided` |
| Trust | `policy_check_decision`, `policy_override_recorded`, `forbidden_claim_blocked` |
| Lifecycle | `data_export_completed`, `dsar_opened`, `dsar_responded`, `data_deleted` |

Each event carries minimum metadata: `event_id`, `event_type`, `actor`,
`subject`, `tenant_id`, `policy_decision`, `at` (timestamp), and a
hashed reference to the underlying record (not the record itself).

## 4. Retention

- **Hot tier**: 1 year, full-fidelity, queryable in seconds. Encrypted at
  rest, access-controlled.
- **Cold tier**: years 2–7, full-fidelity, restored to hot on demand
  (≤ 24h). Encrypted at rest, sealed-key access.
- **Beyond year 7**: deletion unless held under legal hold.

Aligned with [`DATA_RETENTION.md`](DATA_RETENTION.md).

## 5. Queryability

- **Internal**: HoLegal and the DPO have query access via a dedicated
  audit query surface. Engineers do **not** have direct production
  query access; engineering queries go through a request-and-approval
  flow.
- **Customer**: customers receive audit exports relevant to their
  tenant on request (DSAR, regulator inquiry, contractual right).
- **Regulator**: SDAIA / sectoral regulator requests are routed through
  HoLegal and answered within the regulator's stated window.

A standard query returns the matching events redacted to omit any PII
that may have been captured in error.

## 6. Coverage Targets

- **100% of policy-relevant events** carry an audit log entry. Coverage
  is measured by comparing action counts at the action layer against
  event counts at the audit layer. Any drift > 0.1% is a P1 incident.
- **100% of approvals** are tied to an `action_proposed` and an
  `action_approved` or `action_rejected`.
- **100% of PII detections** carry a `pii_detected` event regardless of
  verdict.

## 7. Anti-Patterns

- **Selective logging**: emitting events only on the happy path. Both
  successes and failures are logged.
- **PII in audit logs**: the audit log is not a place to dump record
  bodies. Use hashed references.
- **Schema drift**: changing event field names without a migration. Use
  the event taxonomy as the contract.

## 8. Cross-links

- Event taxonomy: [`../analytics/event_taxonomy.md`](../analytics/event_taxonomy.md)
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- Data retention: [`DATA_RETENTION.md`](DATA_RETENTION.md)
- Approval matrix: [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)
- Code: `auto_client_acquisition/revenue_memory/event_store.py`, `dealix/trust/audit.py`

## 9. Owner & Review Cadence

- **Owner**: HoLegal.
- **Review**: monthly coverage check; quarterly retention review; annual
  external audit.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial audit log policy (events, retention, queryability) |
