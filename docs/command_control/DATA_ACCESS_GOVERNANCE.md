# Data Access Governance

Dealix is data-policy-aware **from the first line of code**. Generative AI does not access raw data unless every governance precondition is met.

## 1. The decision vocabulary for data access

- `APPROVE`
- `DENY`
- `CONDITIONAL`

The default is **deny**.

## 2. Preconditions

No raw data access unless:

- Source is known and passported.
- Allowed use is defined.
- Sensitivity is classified.
- PII has been checked.
- Business purpose is documented.
- An audit event has been created.

If any precondition is missing, the decision is `DENY`.

## 3. Source Passport (canonical schema)

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "ai_access_allowed": true,
  "external_use_allowed": false
}
```

## 4. Policy-aware AI for data access

When Dealix uses LLMs to evaluate requests against policies, the LLM operates on **policies and metadata, not raw data**. Hard policy gates remain in code and default to deny.

## 5. Operating discipline

- The data plane logs every access decision.
- Denied requests are still recorded — with the reason — to detect rule drift.
- Conditional approvals carry the explicit conditions and an expiry.
- Cross-tenant access is forbidden regardless of role.

## 6. Why this matters

- It protects clients from a class of failure that compounds quickly when agents are added.
- It gives the firm an explicit defense against accidental PII exposure.
- It is the precondition for selling at enterprise tiers.

## 7. Failure modes

- “Just-this-once” raw data exceptions.
- Treating conditional approvals as permanent.
- Letting an agent access data without an audit event being emitted.
- Confusing data plane logs with audit events.
