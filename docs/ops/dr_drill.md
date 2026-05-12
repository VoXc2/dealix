# Disaster Recovery — Quarterly Restore Drill

**Owner:** founder (until on-call deputy is hired — see `docs/QA_REVIEW.md` S.6).
**Cadence:** Quarterly (Q1 = Feb, Q2 = May, Q3 = Aug, Q4 = Nov).
**SLA targets:** RPO ≤ 24 h, RTO ≤ 4 h for SEV-1 (see `docs/sla.md` §7).

---

## Why we drill

Customers buy reliability. We don't earn that label by promising backups —
we earn it by proving we can restore from them. This drill validates the
end-to-end recovery chain (`backup_pg.sh` → S3 → scratch DB → smoke checks)
on a recurring cadence so that on the day production breaks, the procedure
is muscle memory and the timing is known.

## What this drill validates

1. The latest `dealix_*.sql.gz` snapshot exists and is < 24 h old (RPO).
2. The dump can be restored to a clean Postgres without error.
3. Core business tables (`users`, `tenants`, plus whatever else we add to
   the smoke checks) come back with sane row counts.
4. Time-to-restore from "decision to restore" to "smoke checks pass" is
   recorded so we know our true RTO.

## Pre-conditions

- A scratch Postgres instance — separate from production. Recommended:
  ephemeral Railway/Render Postgres or a local Docker container.
- Environment variables:
  - `DATABASE_URL` — production DSN (read-only; the script refuses to write
    to it).
  - `DR_TARGET_DSN` — scratch DSN; must not equal `DATABASE_URL`.
  - `BACKUP_DIR` — where `backup_pg.sh` writes (default `/var/backups/dealix`).
- `psql` and `gunzip` on `$PATH`.
- A timer (your phone is fine) for measuring RTO.

## Procedure

### Dry run (always safe)

```bash
bash scripts/infra/dr_restore_drill.sh --dry-run
```

Reads inputs, prints every step it would run, exits 0. Use this to confirm
the latest backup is fresh and that pointers are correct before touching a
real scratch DB.

### Live drill

```bash
# Start a stopwatch the moment you read this line.
bash scripts/infra/dr_restore_drill.sh
# When the smoke checks print, stop the stopwatch.
```

Record:

| Field | Value |
| --- | --- |
| Drill date | `YYYY-MM-DD` |
| Backup file used | `dealix_YYYYMMDD_HHMMSS.sql.gz` |
| Backup age at restore start | `Xh Ym` |
| Restore elapsed | `Xm Ys` |
| Smoke-check anomalies | _(table or count that surprised you)_ |
| RTO target met? | yes / no |
| Action items | _(bugs, gaps, next-quarter improvements)_ |

Append the row to the table below. **Do not delete history** — auditors and
enterprise customers will ask to see a continuous track record.

## Drill log

| Date | Backup age | Restore time | RTO met | Notes |
| --- | --- | --- | --- | --- |
| — | — | — | — | First entry expected by 2026-08-15 |

## When the drill fails

If any step fails (especially smoke checks):

1. **Do not** declare a real SEV-1 — production is unaffected.
2. File a P1 issue tagged `disaster-recovery` describing the gap.
3. Fix the gap (typical causes: schema migrations applied post-backup,
   missing extension in scratch DB, expired S3 credentials).
4. Re-run the drill within 30 days and update this log.

## What this drill does **not** cover

- Restoring Supabase RLS policies — those live in the dashboard. See the
  Supabase RLS section of `DEPLOYMENT.md` for the policy snapshot procedure.
- Redis state — Redis is treated as cache; loss is tolerated.
- Object storage — `auto_client_acquisition/data/` and any S3 buckets need a
  separate runbook, tracked as future work.
