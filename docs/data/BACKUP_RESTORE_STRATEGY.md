# Backup & Restore Strategy (Dealix)

## Backup
- Manual: `python3 scripts/backup_business_data.py`
- Auto: every JSON write via `JSONAdapter._backup()`
- Output: `reports/backups/*.zip` and `reports/backups/auto/*.json`

## Schedule
- Daily: full zip
- On every write: incremental JSON snapshot
- Weekly: verify backup integrity

## Restore
- From zip: `python3 scripts/restore_business_data.py --from PATH --confirm`
- From single JSON: copy from `reports/backups/auto/`

## Off-site
- For production, copy `reports/backups/*.zip` to a separate location daily
- Encrypt at rest

## RTO/RPO
- RTO (recovery time objective): 1 hour
- RPO (recovery point objective): 24 hours
