# Dealix Quick Reference (< 50 lines)

## Commands
```bash
make dev          # uvicorn + next dev
make test         # pytest -x -q
make lint         # ruff check + mypy
make migrate      # alembic upgrade head
make build        # docker build
```

## Env Vars (core/config.py)
- `DATABASE_URL` — PostgreSQL connection
- `SUPABASE_URL` + `SUPABASE_KEY` — Supabase access
- `JWT_SECRET` — auth token signing
- `OPENAI_API_KEY` — AI features
- `ANTHROPIC_API_KEY` — Claude features

## Common Files
- `core/config.py` — all settings
- `core/models/` — SQLAlchemy models
- `api/routers/` — FastAPI endpoints (120+ routers)
- `api/routers/commercial.py` — 13 commercial chain endpoints
- `dealix/commercial/` — business logic (diagnostic, pilot, proof, upsell)
- `dealix/payments/` — Moyasar payment links
- `data/templates/` — AR/EN content templates
- `tests/conftest.py` — test fixtures

## Key Patterns
- Async everywhere: `async def` + `await`
- Arabic: all user-facing strings bilingual
- Currency: SAR only (rounding to 2 decimals)
- Pagination: `page` + `page_size` query params
