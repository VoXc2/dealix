# Data Boundary Statement (Dealix)

## What we store
- Industry, city, sector
- Visible public signal (URL or quote)
- Weakness hypothesis
- Score, stage, owner
- Review status

## What we do NOT store (without consent)
- Personal phone numbers
- Personal email addresses
- ID numbers
- Financial figures
- Private message content

## Where it lives
- Demo: `business/_data/*.json`
- Production: Postgres (Alembic-managed)

## Who can read
- Founder
- Future: delivery lead (read), sales (read)

## Cross-border
- V1: KSA only
- Future: GCC, with regional scoping

## Backup / restore
- See `docs/data/BACKUP_RESTORE_STRATEGY.md`

## Deletion
- Client request: 14 days
- Auto-cleanup: per retention policy
