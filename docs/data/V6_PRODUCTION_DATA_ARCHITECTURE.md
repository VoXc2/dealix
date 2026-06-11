# V6 Production Data Architecture (Dealix)

## Modes
1. **demo_json** (default)
   - Uses `business/_data/*.json`
   - No database required
   - CI-friendly
   - Every write creates backup in `reports/backups/auto/`
2. **sqlite_local**
   - Set `DATABASE_URL=sqlite:///path/to/file.db`
   - Local dev
   - Operator runs Alembic migrations
3. **postgres**
   - Set `DATABASE_URL=postgresql://...`
   - Production
   - Alembic migrations required

## Schemas
- `business/_schemas/*.schema.json`
- Validated at the adapter boundary
- Operator adds new fields via migration, not by ad-hoc edits

## Audit
- Every mutation logs to `reports/audit/audit-YYYY-MM.jsonl`
- Fields: id, ts, actor, action, target, metadata, demo

## Backups
- Manual: `python3 scripts/backup_business_data.py`
- Auto: every JSON write to `_data/*.json`
- Restore: `python3 scripts/restore_business_data.py --from path.zip --confirm`

## Integrity
- `python3 scripts/check_data_integrity.py` validates JSON

## Operator Notes
- demo_json mode is the default and should pass in CI
- Switching to postgres requires:
  1. `pip install -r requirements.txt`
  2. alembic upgrade head
  3. set `DATABASE_URL`
  4. restart app
