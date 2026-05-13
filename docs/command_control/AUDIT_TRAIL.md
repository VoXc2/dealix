# Audit Trail

Any enterprise will ask the same six questions about an AI action:

1. Who did what?
2. With which data?
3. Which model?
4. What was the decision?
5. Who approved?
6. What is the proof?

The Dealix Audit Trail is built so that every one of these has a structured answer at any moment in time.

## 1. The audit event shape

```json
{
  "audit_event_id": "AUD-001",
  "actor": "RevenueAgent",
  "human_owner": "Dealix Revenue",
  "action": "score_accounts",
  "dataset_id": "DS-001",
  "policy_decision": "ALLOW_WITH_REVIEW",
  "approval_required": false,
  "timestamp": "2026-05-14T10:00:00Z"
}
```

## 2. Properties

- **Append-only** — events are never deleted or edited.
- **Signed** — provenance is verifiable.
- **Queryable** — by actor, dataset, decision, time window.
- **Exportable** — `governance_os.export_audit(period)`.

## 3. What the trail must connect

- Technical provenance — models, datasets, evaluations.
- Governance records — approvals, waivers, attestations.
- Engagement context — which client, which workflow, which sprint.

The trail must let the firm reconstruct **what changed, when, and who approved it** — without scrolling through chat threads.

## 4. Operating discipline

- A gap in the audit trail is a P1 incident.
- Quarterly audit exports are an SLA for enterprise tiers.
- Audit data is retained per the client’s contracted retention policy.
- Cross-tenant audit reads are forbidden.

## 5. Why this is part of the product

Enterprise buyers cannot sign off without an auditable record. Regulators expect it. Boards demand it. The Audit Trail is therefore part of the *product surface*, not a hidden engineering concern.

## 6. Failure modes

- Treating audit as logs — logs are unstructured.
- Mixing audit and observability data.
- Storing audit in places that allow deletes.
- Letting approvals sit only in chat and never in the engine.
