# Dealix — Deployment Context (On-Demand Skill)

## Platform: Railway

```
Services:
├── web      → uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 2
├── frontend → Next.js (frontend/)
└── worker   → background tasks
```

Release command (auto on deploy): `alembic upgrade head`

## Key Files
- `railway.json` / `railway.toml` — Railway service config
- `Dockerfile` — API image
- `Dockerfile.worker` — Worker image
- `Dockerfile.watchdog` — Watchdog image
- `Procfile` — process definitions
- `docker-compose.yml` — local dev
- `docker-compose.prod.yml` — production reference

## Environment Variables (required in Railway)
```
DATABASE_URL          PostgreSQL connection string
SUPABASE_URL          Supabase project URL
SUPABASE_KEY          Supabase service role key
JWT_SECRET            Auth token signing
ANTHROPIC_API_KEY     Claude features
OPENAI_API_KEY        AI features
MOYASAR_API_KEY       Payment processing
MOYASAR_LIVE_MODE     1 = live, 0 = sandbox (default 0)
```

## Deploy Commands
```bash
# Local
make dev              # docker-compose up (full stack)
make build            # docker build test

# Railway (auto on push to main)
git push origin main  # triggers Railway deploy

# Database
make migrate          # alembic upgrade head
```

## Rollback
```bash
# Railway dashboard → Deployments → previous → Rollback
# Or via alembic:
alembic downgrade -1
```

## Health Check
```bash
curl https://app.dealix.sa/health
# → {"status": "ok", "version": "..."}
```

## Logs
```bash
# Railway dashboard → Service → Logs
# Or locally:
docker-compose logs -f web
docker-compose logs -f worker
```
