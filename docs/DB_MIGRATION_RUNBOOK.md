# DB Migration Runbook — `deals.hubspot_deal_id`

> Adds a single nullable column. No data drop. No table recreate. Idempotent.

## TL;DR — auto-runs on app startup

As of the cutover-hardening commit, `api/main.py` lifespan calls
`scripts.migrate_add_hubspot_deal_id.run_migration_if_needed()` right
after `init_db()`. This means **manual invocation is no longer required**
once the app boots with the new image — the column is added automatically
on the next Railway deploy. Keep this doc as a reference for local
testing or for situations where you want to verify the migration
out-of-band.

## What this fixes

Production Postgres is missing `deals.hubspot_deal_id`. The deploy-branch
`role-briefs/daily?role=sales_manager` and `whatsapp/brief?role=sales_manager`
queries select that column → 500 with `column deals.hubspot_deal_id does not exist`.

After this migration, both endpoints return 200.

## Command (run on Railway, against prod DATABASE_URL)

```bash
# Railway → service → Settings → Run Command
# OR locally with the prod URL:
DATABASE_URL='<prod url>' python scripts/migrate_add_hubspot_deal_id.py
```

Expected output (success):

```
MIGRATION_INFO  dialect=postgresql
MIGRATION_OK  added deals.hubspot_deal_id (nullable)
```

Or, if already present:

```
MIGRATION_INFO  dialect=postgresql
MIGRATION_OK  column 'hubspot_deal_id' already present
```

## Safety properties

| Property | How |
| --- | --- |
| Idempotent | reads `information_schema.columns` first; only ALTER if missing |
| Nullable | `ADD COLUMN ... NULL`; existing rows unaffected |
| No backfill | no UPDATE statements |
| No data loss | no DROP, no TRUNCATE, no recreate |
| Fails closed | if `deals` table itself is missing, exits 3 (does NOT auto-create — too risky) |
| Refuses unset env | exits 2 if `DATABASE_URL` empty |
| Driver agnostic | works for asyncpg + aiosqlite |

## Rollback

If you need to remove the column (very unlikely):

```sql
ALTER TABLE deals DROP COLUMN IF EXISTS hubspot_deal_id;
```

The application tolerates a NULL value, so removal is safe only if no
deploy-branch code reads the column non-null. Verify before rolling
back.

## Verification after migration

```bash
BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
# Expected: PASS=36 FAIL=0 (if operator wiring patch also applied)
#
# Specifically verify:
curl -s https://api.dealix.me/api/v1/role-briefs/daily?role=sales_manager | head -c 200
# → no `_errors` field; clean brief
```

## When to run

Right after PR #131 merges into the deploy branch, before Railway routes
production traffic to the new build. Order:

1. Merge PR #131
2. Apply 4-line operator wiring patch (`docs/OPERATOR_WIRING_PATCH.md`)
3. Run this migration  ← **here**
4. Railway redeploy
5. Re-run staging smoke
