# Dealix — Context for Claude

## Stack
Python 3.11 · FastAPI · PostgreSQL (Supabase) · React/Next.js · Railway deployment

## Rules
1. Async/await everywhere in Python. No sync blocking calls.
2. Arabic-first content (العربية أولاً), bilingual UI.
3. All DB access via `core/database.py`. Never raw SQL outside models.
4. Tests in `tests/`. Run: `pytest tests/ -x -q`
5. SAR currency only. Never USD display to end users.

## Key Files
- `core/config.py`: env vars & settings
- `api/routes/`: all FastAPI endpoints
- `AGENTS.md`: multi-agent orchestration rules

## Commands
```bash
make dev          # start dev server
make test         # run tests
make lint         # ruff + mypy
make migrate      # alembic upgrade head
```

## Skills (load on demand)
- `@token-optimizer/02-claude-md/skills/database.md` — DB schema & patterns
- `@token-optimizer/02-claude-md/skills/api.md` — API conventions (120+ routers)
- `@token-optimizer/02-claude-md/skills/commercial.md` — Commercial chain (diagnostic→pilot→proof→payment→upsell)
- `@token-optimizer/02-claude-md/skills/frontend.md` — Frontend patterns
- `@token-optimizer/02-claude-md/skills/testing.md` — Test conventions
- `@token-optimizer/02-claude-md/skills/deployment.md` — Deploy procedures
