---
title: Approval Matrix — Action × Risk × Approver
doc_id: W6.T37.approval-matrix
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T14]
kpi:
  metric: actions_without_required_approval
  target: 0
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 0.5
  score: governance-foundation
---

# Approval Matrix

## 1. Context

Every action that touches the outside world (sending a message, writing to
a third-party API, exporting data, generating an invoice, overriding policy)
requires a named human approver mapped to the action's evidence level. This
document is the human-readable mirror of `dealix/trust/approval_matrix.py` —
the code is authoritative if the two diverge.

## 2. Audience

Engineers (must wire approvals into action paths), CSMs (must obtain
approvals before triggering actions), HoLegal (owns escalations), founders /
exec (CEO sign-off on policy override).

## 3. The Matrix

| Action | Min evidence | Default approver | Escalation when evidence below floor |
|--------|-------------|------------------|--------------------------------------|
| `OUTBOUND_EMAIL` | L2 | CSM | Head of CS |
| `OUTBOUND_WHATSAPP` | L3 | Head of CS | Head of Legal |
| `OUTBOUND_SMS` | L3 | Head of CS | Head of Legal |
| `PUBLIC_POST` | L4 | Head of Legal | CEO |
| `EXTERNAL_API_WRITE` | L3 | CTO | CEO |
| `DATA_EXPORT` | L2 | Head of Legal | CEO |
| `CRM_BULK_UPDATE` | L2 | AE | Head of CS |
| `INVOICE_GENERATION` | L3 | Head of CS | Head of Legal |
| `POLICY_OVERRIDE` | L5 | CEO | CEO (no further escalation) |

**Evidence levels**: L0 (unverified) → L5 (multi-source, audited). The
floor enforces the minimum confidence before a default approver is enough.
If evidence is below the floor, the approver auto-escalates one role up.

## 4. Operating Rules

- An action without a recorded approval **does not execute** — the
  Governance OS rejects it pre-flight.
- An approval is recorded as an event in the event store with: actor,
  action kind, evidence level, approver role, reason, timestamp.
- The approver and the action initiator **cannot be the same person** —
  separation of duties is enforced.
- A `POLICY_OVERRIDE` requires CEO sign-off in writing, even when CSM has
  asserted L5 evidence. No exceptions.

## 5. How Auto-Escalation Works

Implemented in `required_approver(action, evidence_level)`:

```python
# Pseudocode of the rule
if evidence_level >= base.min_evidence_level:
    return base.approver
else:
    return escalation_map[base.approver]  # one step up
```

The escalation map:

```
AUTO   → CSM
CSM    → Head of CS
AE     → Head of CS
HEAD_CS → Head of Legal
HEAD_LEGAL → CEO
CTO    → CEO
CEO    → CEO  (terminal)
```

## 6. Audit Trail

Every approval (or rejection) is queryable through the audit log
([`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md)). Quarterly review by HoLegal:
sample 20 approvals across action kinds, verify each had the right
evidence and the right approver.

## 7. Anti-Patterns

- **Pre-signed approvals**: "Send anything outbound today, I'm approving in
  advance." Banned. Approvals are per-action.
- **Approver-of-record vs actual approver**: the person who clicked must
  be the recorded approver. No proxying.
- **Evidence inflation**: marking a record L5 to dodge escalation. Audit-
  logged; repeat is a performance issue.

## 8. Cross-links

- Code: `dealix/trust/approval_matrix.py`
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- Forbidden actions: [`FORBIDDEN_ACTIONS.md`](FORBIDDEN_ACTIONS.md)
- Audit log: [`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md)
- Policy rules: [`../policy/revenue_os_policy_rules.md`](../policy/revenue_os_policy_rules.md)

## 9. Owner & Review Cadence

- **Owner**: HoLegal.
- **Review**: quarterly with HoCS, CTO; immediate on incident.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial matrix mirroring code |
