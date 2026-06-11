# SQLite Local Dev Plan (Dealix)

## When to use
- Single-developer setup
- Local experimentation
- No external Postgres available

## Setup
1. Install SQLAlchemy
2. `export DATABASE_URL=sqlite:///./dealix-dev.db`
3. `alembic upgrade head`
4. Run scripts as in production

## Safety
- Local file only
- Backups via `python3 scripts/backup_business_data.py`
- DO NOT use the same file across machines
