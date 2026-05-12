# PDPL Data Retention & DSAR Policy

> **Authority:** Saudi PDPL Art. 18 (purpose limitation), Art. 11 (retention), Art. 12 (rights of the data subject).
> **Owner:** DPO. **Reviewed:** every 12 months and after every breach.
> **Source of truth:** this document. The DB schema enforces these limits via scheduled jobs.

---

## 1. Retention principle

Personal data is kept **only as long as needed for the purpose** for which it was collected. After that, it is either:
- **Deleted** (hard delete from primary store + backups expired), or
- **Anonymised** (irreversibly: hash with random salt, drop direct identifiers, replace email/phone with `null`).

When in doubt → delete.

---

## 2. Retention schedule

| Data category | Purpose | Retention | Trigger to delete | Where stored |
|---------------|---------|-----------|-------------------|--------------|
| **Prospect contact data** (name, company, email, phone) | Cold outreach for B2B | 12 months from last interaction | Last activity older than 12 mo | `accounts`, `contacts` |
| **Demo request** (name, email, phone, company, consent flag) | Sales follow-up | 24 months from submission | 24 mo elapsed | `demo_requests` |
| **Pilot/paying customer record** (contract + contact) | Service delivery + accounting | Duration of contract + 7 years (tax law) | Contract end + 7 yrs | `customers`, `contracts` |
| **Payment records** (transaction id, amount, partial card mask, billing address) | Financial accounting | 10 years (Saudi tax + Moyasar) | 10 yrs from transaction | `payments` |
| **Webhook payloads** (Moyasar, Calendly, WhatsApp inbound) | Reliability + audit | 90 days | rolling cron | Redis + cold log archive |
| **Audit logs** (AuditLogMiddleware) | Security + compliance | 24 months | rolling cron | logs/audit |
| **DLQ items** | Operational recovery | 30 days | rolling cron | Redis DLQ |
| **Application/access logs** (HTTP, errors) | Operational | 90 days | log retention policy | Railway + Sentry |
| **Marketing analytics** (PostHog events) | Funnel optimisation | 24 months (rolling) | PostHog retention setting | PostHog cloud |
| **Backups** (pg_dump) | Disaster recovery | per tier (see BACKUP_RESTORE.md) | tiered lifecycle | S3 me-south-1 |
| **DSAR archives** (data given to a subject) | Proof of fulfilment | 24 months from issue | rolling cron | S3 (encrypted) |

**Sensitive categories** (national ID, health, biometric, religious, political) — **Dealix does not collect these**. If accidentally received (e.g. in a free-text demo form), purge within 7 days and log under `docs/ops/sensitive_data_purge_log.md`.

---

## 3. Implementation — enforcement

Retention is enforced by code, not by docs. Required scheduled jobs:

```
db/jobs/retention/
├── purge_stale_prospects.sql       # accounts/contacts older than 12mo, no activity
├── purge_webhook_payloads.sql      # >90 days
├── anonymise_pilot_dropouts.sql    # customers who never paid + >12mo
├── trim_audit_logs.sql             # >24mo
└── purge_dlq.sql                   # >30 days
```

Each job:
- Runs daily at 03:00 AST via cron / Railway scheduled job
- Logs counts to `logs/retention/<date>.json`
- Emits a PostHog event `retention_job_completed { job, deleted_count }`

Quarterly: DPO verifies job logs exist and counts are non-zero where expected.

---

## 4. DSAR — Data Subject Access Request

A data subject (Saudi resident) may request:
- **Access** — copy of all personal data Dealix holds about them.
- **Rectification** — correction of inaccurate data.
- **Erasure** ("right to be forgotten").
- **Restriction** — pause processing.
- **Withdrawal of consent** — for processing based on consent.
- **Data portability** — machine-readable export.

### Response SLA
- **30 days** from receipt (PDPL Art. 12)
- May extend by 30 days for complex requests (notify subject)

### Intake channels
1. Email: `privacy@dealix.sa` (route to DPO)
2. Form: `https://dealix.sa/privacy.html` → submits to `/api/v1/pdpl/dsar`
3. Phone: published on `/privacy`

### Procedure

```bash
# 1. Verify identity (national ID + matching contact, or signed letter)
#    NEVER process a DSAR without verifying identity.

# 2. Gather data
python scripts/export_subject_data.py \
  --email <subject_email_or_phone> \
  --output dsar_<request_id>.zip

# 3. Encrypted hand-off
#    - ZIP password-protected (AES-256), password shared via separate channel
#    - Log handover in dsar_log.md

# 4. For erasure: dry-run first, then execute, then re-verify by re-running export → empty.
```

### Logging
Every DSAR is logged in `docs/ops/dsar_log.md` with: request id, intake date, type, decision, response date, evidence ref.

---

## 5. Sub-processors

A sub-processor is any third party that processes personal data on behalf of Dealix. Current list: see `landing/sub-processors.html` (public) and `docs/ops/SUB_PROCESSORS_DETAILS.md` (internal).

For every sub-processor:
- DPA signed
- Listed publicly
- Reviewed annually
- New sub-processors added → 30-day notice to customers before activation

---

## 6. Annual review

The DPO reviews this policy by 31 December each year. The review covers:
- Retention periods (still proportionate?)
- New data categories collected?
- Sub-processor list still accurate?
- Job logs show enforcement?
- Any DSAR delayed past SLA? Why?

Review outcomes recorded in `docs/ops/pdpl_annual_review/<year>.md`.
