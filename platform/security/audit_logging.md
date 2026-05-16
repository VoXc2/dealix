# Audit Logging Requirements (Release 1)

## Objective

Every meaningful action in the pilot must be traceable, reviewable, and explainable.

## Mandatory audit event fields

Each audited event must include:

1. `audit_id`
2. `timestamp`
3. `tenant_id`
4. `actor_type` and `actor_id`
5. `action`
6. `entity_id` or `workflow_id` (as applicable)
7. `outcome` (`ok|denied|failed|blocked|escalated`)
8. `reason` (for non-success outcomes)
9. `trace_id` and/or `correlation_id`
10. `details` (sanitized; no secrets/PII leakage)

## Coverage requirements

Audit logging is required for:

- policy evaluations (allow/deny/escalate),
- approval request/grant/reject/timeout,
- workflow start/step/failure/completion,
- sensitive tool usage,
- access-denied events,
- data export actions.

## Integrity and retention requirements

1. Audit stream is append-only.
2. Log mutations are forbidden.
3. Retention policy is documented and enforced.
4. Export path must preserve redaction and tenant boundaries.

## Pilot operational requirements

1. Any high-risk action without audit entry is treated as incident.
2. Dashboard and API should support filtering by tenant, actor, action, and time.
3. Incident review references audit IDs, not anecdotal notes.

## Acceptance checklist (Release 1)

- [ ] All pilot workflow steps emit audit events
- [ ] Approval events include requester and approver identities
- [ ] Denied/failed paths are visibly logged
- [ ] Trace and audit records can be correlated
- [ ] Exported audit records stay tenant-safe and redacted
