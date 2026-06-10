# Backup + Restore Strategy

## What to back up
1. PostgreSQL database (Railway managed)
2. Application secrets (never in repo — 1Password vault `Dealix Production`)
3. Customer data exports (PDPL DSAR archive)

## Backup Frequency

| Tier | Frequency | Mechanism | Retention | Target |
|------|-----------|-----------|-----------|--------|
| Tier 1 | **Hourly** | `scripts/hourly_backup.sh` (cron) → encrypted pg_dump → S3 | 48 hours local + 7 days S3 | RPO ≤ 1h |
| Tier 2 | Daily | Railway managed snapshot | 7 days | RPO ≤ 24h |
| Tier 3 | Weekly | Manual `pg_dump` → cold S3 (Glacier) | 4 weeks | DR |
| Tier 4 | Monthly | Compliance archive (PDPL audit) | 12 months | Legal |
| Tier 5 | Yearly | Cold archive | 7 years | Legal (PDPL §11) |

## Hourly Backup — Operational

**Cron entry (Railway / VPS / cron worker):**
```cron
0 * * * *  /app/scripts/hourly_backup.sh >> /var/log/dealix-backup.log 2>&1
```

**Required env vars:**
- `DATABASE_URL` — production Postgres URL
- `BACKUP_ENCRYPTION_KEY` — 32-byte hex (generate: `python -c "import secrets; print(secrets.token_hex(32))"`). **Store in 1Password, not in the repo or Railway plaintext.**
- `BACKUP_S3_BUCKET` — e.g. `dealix-backups-ksa`
- `BACKUP_S3_PREFIX` — default `dealix/hourly`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION=me-south-1` (Riyadh region for data residency)
- `BACKUP_RETENTION_HOURS` — default `48`

**S3 bucket policy:** versioning on, lifecycle: STANDARD_IA after 1 day → GLACIER_IR after 7 days → DELETE after 30 days.

**Encryption:** AES-256-CBC with PBKDF2 KDF (OpenSSL). Key never written to disk.

## Restore Drill (Quarterly — mandatory)

Run on the 1st of each quarter. Drill is **PASS** only if exit-code 0:

```bash
RESTORE_DATABASE_URL=postgresql://drill:pass@scratch-db.local:5432/drill \
BACKUP_ENCRYPTION_KEY=<from-1password> \
EXPECTED_MIN_LEADS=100 \
bash scripts/restore_test.sh
```

`scripts/restore_test.sh` will:
1. Find the latest hourly backup
2. Decrypt (AES-256)
3. `pg_restore` to scratch DB
4. Verify `accounts` row count ≥ `EXPECTED_MIN_LEADS`
5. Exit 0 if all checks pass

**Track drill results in `docs/ops/RESTORE_DRILL_LOG.md`** (date, time-to-restore, exit code, notes).

## Disaster Recovery — RTO / RPO

| Scenario | RTO target | RPO target |
|----------|-----------|-----------|
| Single-row data loss (accidental DELETE) | 30 min | 1 hour |
| Schema corruption | 1 hour | 1 hour |
| Full DB loss (Railway region down) | 4 hours | 1 hour |
| Region-wide outage | 8 hours | 24 hours (Tier 3 weekly cold) |

## Secret backup

- All production secrets live in **1Password vault `Dealix Production`** (shared with founder + CTO).
- Railway dashboard variables are mirrors, not the source of truth.
- 1Password emergency kit (printed, sealed) held by founder.

## Customer Data Export (PDPL DSAR)

A data subject access request (DSAR) must be answerable within 30 days. See `docs/ops/PDPL_RETENTION_POLICY.md` for the procedure and the DSAR template.
