# Database migrations (Alembic)

This directory is the **canonical** location for all database migrations.
`alembic.ini` at the repo root sets `script_location = db/migrations`.

Migration files live in `versions/`. A single head is enforced — if two
branches add migrations, merge them with `alembic merge`.

## Common commands

```bash
# create a new migration from model changes
alembic revision --autogenerate -m "describe change"

# apply all pending migrations
alembic upgrade head

# roll back the last migration
alembic downgrade -1

# show current revision
alembic current
```

On deploy, Railway runs `release: alembic upgrade head` (see `Procfile`).
In `development`/`test` the app calls `init_db()` to create tables directly;
production relies solely on these migrations.

## Naming convention

`YYYYMMDD_NNN_short_description.py` — e.g. `20260514_010_referral_program.py`.
