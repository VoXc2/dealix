# Audit Trail Standard

The Audit Trail is **not** logging. It is a structured, append-only, queryable record that lets the firm reconstruct what happened, when, and who approved.

## 1. Canonical audit event

```json
{
  "audit_event_id": "AUD-001",
  "actor_type": "agent",
  "actor_id": "AGT-REV-001",
  "human_owner": "Dealix Revenue",
  "action": "score_accounts",
  "dataset_id": "DS-001",
  "source_id": "SRC-001",
  "policy_decision": "ALLOW_WITH_REVIEW",
  "approval_required": false,
  "timestamp": "2026-05-14T10:00:00Z"
}
```

## 2. Coverage targets

Institutional grade requires:

- **100%** AI runs logged.
- **100%** governance decisions logged.
- **100%** client-facing outputs linked to an audit event.
- **100%** external actions backed by an approval event.

Falling below 100% on any of these is treated as a P1 incident.

## 3. Properties

- Append-only.
- Signed.
- Queryable by actor, dataset, decision, time window.
- Exportable per tenant, per period.

## 4. What the trail must connect

- Technical provenance — models, datasets, evaluations.
- Governance records — approvals, waivers, attestations.
- Engagement context — client, workflow, sprint.

A complete trail is the precondition for any case study, public claim, or audit export.

## 5. Operating discipline

- Audit data retention is per the buyer's contract.
- Cross-tenant audit reads are forbidden by code.
- Edits and deletes are forbidden by code, not just policy.
- Quarterly export is an SLA at enterprise tiers.

## 6. Anti-patterns

- "Audit" stored as plain logs.
- Approval recorded only in chat.
- Sampling audit instead of full coverage.
- Trail that exists but cannot answer the six audit questions.

## 7. The principle

> A gap in the audit trail is a P1 incident. The trail is the firm's memory.
