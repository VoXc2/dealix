# Data Retention Policy (AR)

> **Default retention table** + **per-class overrides**.

---

## Master Retention Table

| Data class | Retention | Trigger | Deletion method |
|------------|-----------|---------|-----------------|
| D0 public | unlimited | — | N/A |
| D1 metadata | 24mo | last interaction | anonymize |
| D2 contact | 24mo | opt-out | secure delete + audit |
| D3 client operational | contract + 90d | contract end | secure delete + audit |
| D4 sensitive client | contract + 30d | contract end | secure delete + audit |
| D5 secrets | rotation cycle | expiry | auto-rotate + delete |
| Audit logs | 7y | creation | append-only, then archive |
| Backup data | 90d | backup date | auto-expire |
| Financial records | 7y | creation | per ZATCA |
| AI training data | never (we don't train on client data) | — | — |

---

## Per-Entity Retention

| Entity | Retention | Notes |
|--------|-----------|-------|
| Prospect | 24mo after last interaction | anonymize on expiry |
| Contact | 24mo after opt-out | delete + audit |
| Company | lifetime + 7y (legal) | if no client relation |
| Draft | contract + 90d | then delete |
| Approval | 7y | compliance |
| SendBatch | contract + 90d | then delete |
| Reply | contract + 90d | then delete |
| WhatsAppSession | contract + 90d | then delete thread |
| ClientAssessment | contract + 90d | then anonymize |
| ClientPermission | contract + 90d | then revoke |
| PortalSession | 30d | sliding |
| Upload | contract + 30d | then delete |
| Proposal | 7y | legal/audit |
| ProofPack | 7y | legal/audit |
| PaymentHandoff | 7y | ZATCA |
| DeliveryHandoff | contract + 90d | then anonymize |
| DeliveryTask | contract + 90d | then delete |
| ClientHealth | contract + 90d | then delete |
| WeeklyReport | contract + 90d | then anonymize |
| Renewal | 7y | legal |
| Partner | lifetime + 7y | if partnership ends |
| Vendor | lifetime + 7y | if contract ends |
| MetricEvent | 24mo | then aggregate-only |
| FounderDecision | 7y | legal |
| Risk | 7y | compliance |
| AgentRun | 12mo | then aggregate-only |
| AuditEvent | 7y | legal |

---

## Deletion Process

1. **Identify:** daily job scans for expiring records
2. **Notify:** if client-facing, notify 30 days before
3. **Confirm:** check no active relationship blocks deletion
4. **Soft delete:** mark deleted_at, hide from queries
5. **Hard delete:** after 30 days soft period
6. **Backup deletion:** within backup retention
7. **Audit:** write audit_event for deletion
8. **Confirm to client:** if requested

## Opt-Out vs Deletion

- **Opt-out:** mark `opted_out=true`, suppress from all comms
- **Deletion:** remove all data per PDPL

---

## PDPL Specific

- Erasure request: 30 days to fulfill
- Confirmation: written
- Backup deletion: 90 days
- Subject access request: 30 days

---

> **Owner:** Data Lead + Legal · **Review:** سنوي
> **Cross-ref:** `docs/governance/DATA_RETENTION.md` (existing)
