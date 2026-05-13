# Dealix Enterprise Trust Pack

The single, written document Dealix ships to every enterprise buyer. It explains what Dealix does, what it refuses to build, and how trust is operated as a product.

## 1. What Dealix does

Dealix is an AI **operating** company. It installs governed AI capabilities inside organizations:

- Revenue Intelligence
- Company Brain
- Governance Runtime
- Workflow OS

Every engagement runs on the Dealix Core OS, passes through the Governance Runtime, and ends with a Proof Pack.

## 2. What Dealix refuses to build

- Unsafe outbound automation (no cold WhatsApp, no scraping, no auto-send without approval).
- Outcome guarantees of any kind.
- AI agents with autonomous external action.
- Cross-tenant data flows.
- AI on data without a Source Passport.

## 3. Data handling model

- Source Passport per dataset.
- In-region data residency by default.
- PII detection and redaction before transit.
- Per-tenant retention; never cross-tenant.
- Data subject requests honored within published SLAs.

## 4. Source Passport standard

See `docs/sovereignty/SOURCE_PASSPORT_STANDARD.md`.

## 5. AI Run Ledger

Every model invocation is logged with:

- Agent identity
- Action and inputs
- Model and version
- Decision and risk level
- Approval status
- Audit event ID

## 6. Governance Runtime

The runtime evaluates every action against the active policy bundle and emits one of:

```
ALLOW
ALLOW_WITH_REVIEW
DRAFT_ONLY
REQUIRE_APPROVAL
REDACT
BLOCK
ESCALATE
```

The fail-closed default is `DRAFT_ONLY`. The runtime never defaults to `ALLOW` on error.

## 7. Human oversight model

- All external actions are drafts until approved.
- Approvals are recorded by the Approval Engine, not in chat.
- The approval matrix is per BU and per channel.
- Emergency stop is available to revoke any agent mid-run.

## 8. Approval workflows

- Role-based approvals.
- Channel-aware (email, WhatsApp, SMS, voice).
- Escalation rules for high-risk actions.
- Audit-event linkage required.

## 9. Audit trail

- Append-only.
- Signed.
- Queryable by actor, dataset, decision, time window.
- Exportable quarterly to the buyer at enterprise tiers.

## 10. Proof Pack standard

Every engagement ends with a Proof Pack containing:

- Problem
- Inputs
- Work Completed
- Metrics + Before/After
- AI Outputs
- Governance Events
- Business Value
- Risks
- Limitations
- Recommended Next Step

## 11. Incident response

- Defined severity levels.
- Runbooks owned by Governance.
- Buyer notification SLA stated in contract.
- Postmortem and decision log entry within agreed window.

## 12. Client responsibilities

- Designate a workflow owner.
- Provide data sources with permission to passport.
- Designate approvers and channels.
- Accept the QA process.
- Participate in the monthly proof review.

## 13. Versioning

This Trust Pack is versioned alongside the Dealix Method. Updates trigger a notice to active enterprise tenants.

## 14. The principle

> Trust is operated, not promised. The Trust Pack is the artifact that proves it.
