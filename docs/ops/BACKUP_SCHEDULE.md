# Backup Schedule (Dealix)

## Daily (auto, demo mode)
- Every JSON write creates a backup in `reports/backups/auto/`

## Daily (manual, recommended)
- `python3 scripts/backup_business_data.py`
- Output: `reports/backups/dealix-business-data-YYYY-MM-DD.zip`

## Weekly
- Verify backup integrity
- Copy to off-site storage (when configured)

## Monthly
- Review retention
- Archive old backups

## Quarterly
- Test restore
- Update runbook
