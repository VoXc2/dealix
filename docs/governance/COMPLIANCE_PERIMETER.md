---
title: Compliance Perimeter — Forbidden Actions, Required Practices
doc_id: W6.T37.compliance-perimeter
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W3.T07, W4.T14]
kpi:
  metric: policy_violation_incidents
  target: 0
  window: rolling_90d
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 0.5
  score: governance-foundation
---

# Compliance Perimeter

## 1. Context

Dealix operates under a hard perimeter of forbidden actions and required
practices. The perimeter exists because Saudi enterprise buyers are
governance-sensitive and PDPL is enforced. A breach is a business-ending
event for our reputation, not a fix-on-Monday concern. This one-page summary
points to the operating policies that implement the perimeter.

## 2. Audience

Every employee, contractor, partner, and integrator. New starters read this
in the first 24 hours and acknowledge it in writing.

## 3. Forbidden Actions (Hard "No")

- **No PII in customer-facing artifacts** — outputs, reports, dashboards,
  outbound messages. Verified by `dealix/trust/pii_detector.py`.
- **No outbound messages without policy check + (where required) human
  approval.** Verified by `dealix/trust/approval_matrix.py`.
- **No unverifiable / superlative claims** in AR or EN content. Verified by
  `dealix/trust/forbidden_claims.py`.
- **No data export, no policy override, no public post** without the
  required approver listed in [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md).
- **No training on customer data**, no sharing customer data with model
  providers for their training.
- **No cross-border transfer** outside the documented bases in
  [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md).
- **No bypass tokens** without audit logging and a documented business
  reason.

The exhaustive list is [`FORBIDDEN_ACTIONS.md`](FORBIDDEN_ACTIONS.md).

## 4. Required Practices

- **Lawful basis recorded** before processing any personal data (PDPL Art.
  5/6).
- **Source attribution** on every record, claim, and AI-generated answer.
- **Audit log** of every policy-relevant event — hot 1 year, cold 7 years
  ([`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md)).
- **Decision Passport** on every outbound action.
- **DSAR SLA**: acknowledge in 2 business days; substantive response in
  25 calendar days.
- **PII redaction** before any cross-system pass-through unless policy
  explicitly permits internal Trust view.

## 5. Enforcement

The perimeter is enforced in code. Governance OS gates every action; the
event store records every decision; the approval matrix routes every
non-auto action to a named role. Manual workarounds are forbidden — a
gate that fails is a fix to the gate, not a bypass.

## 6. Cross-links

- PDPL rules: [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md)
- Approval matrix: [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)
- Data retention: [`DATA_RETENTION.md`](DATA_RETENTION.md)
- PII policy: [`PII_REDACTION_POLICY.md`](PII_REDACTION_POLICY.md)
- Audit policy: [`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md)
- Forbidden actions: [`FORBIDDEN_ACTIONS.md`](FORBIDDEN_ACTIONS.md)
- Data governance: [`../trust/data_governance.md`](../trust/data_governance.md)

## 7. Owner & Review Cadence

- **Owner**: HoLegal (DPO is functional owner of PDPL items).
- **Review**: quarterly + ad-hoc when PDPL Implementing Regulations change.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial compliance perimeter summary |
