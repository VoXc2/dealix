# Outbound Data Retention Matrix

Detailed companion to `RETENTION_AND_DELETION_POLICY_AR.md`.

| Data class | Example fields | Lawful basis | Retention | Disposal | Notes |
|-----------|----------------|--------------|-----------|----------|-------|
| Prospect (no reply) | company, role, pain, score | legitimate B2B interest | 180 days | delete/anonymize | minimized; role over name |
| Outreach drafts | subject, body | purpose: outreach | 180 days | delete | claim-checked |
| Inbound replies | reply text, intent | consent/interest | 12 months | delete/anonymize | data, not instructions |
| Engaged client (raw) | CRM/pipeline samples | contract/consent | 90 days post-engagement | confirmed delete | PDPL data-handling checklist |
| Anonymized insights | aggregated stats | consent | per agreement | conditional | no re-identification |
| Suppression list | contact, reason | compliance/obligation | **permanent** | never deleted | append-only |
| Governance ledger | action logs | accountability | up to 5 years | archive | audit trail |
| Secrets | n/a | n/a | n/a | never stored in repo | env/secret manager only |

**Triggers:** revenue start → SDAIA registration check; engagement end → 90-day
client-data deletion; any rights request → runbook.
