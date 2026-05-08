# AGENTS.md

## Cursor Cloud specific instructions

### Services Overview

| Service | Port | Required | Start Command |
|---------|------|----------|---------------|
| PostgreSQL 16 | 5432 | Yes | `docker compose up -d postgres` |
| Redis 7 | 6379 | Yes | `docker compose up -d redis` |
| MongoDB 7 | 27017 | Optional | `docker compose up -d mongo` |
| FastAPI Backend | 8000 | Yes | `uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload` |
| Next.js Frontend | 3000 | Optional | `cd frontend && npm run dev` |

### Starting Infrastructure Services

```bash
docker compose up -d postgres redis mongo
```

Wait ~10 seconds for containers to become healthy before starting the backend.

### Starting the Backend

```bash
export PATH="$HOME/.local/bin:$PATH"
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Known Dependency Gotchas

1. **FastAPI version**: The `requirements.txt` pins `fastapi>=0.115.0,<0.116`, but this range has a 204-body assertion bug with `-> None` return type annotations. Use `pip install -e ".[dev]"` (pyproject.toml, no upper bound) which installs FastAPI 0.136+ where this is fixed. Also install `python-jose[cryptography]` separately as it's in `requirements.txt` but not in `pyproject.toml`.

2. **Starlette MutableHeaders**: The `api/middleware.py` `SecurityHeadersMiddleware` uses `response.headers.pop()` which doesn't exist on starlette's `MutableHeaders`. A fix using `del response.headers[key]` is required (already applied in this branch).

3. **Frontend missing modules**: The `frontend/src/lib/utils.ts` and `frontend/src/lib/hooks/useAuth.tsx` files are referenced but missing from the repo. Stub implementations are needed for the Next.js dev server to compile.

4. **PATH**: Tools installed via pip (ruff, black, pytest, uvicorn, etc.) land in `~/.local/bin` which may not be on PATH. Always export: `export PATH="$HOME/.local/bin:$PATH"`

### Running Tests

```bash
export PATH="$HOME/.local/bin:$PATH"
pytest tests/unit/ --tb=short -q    # Unit tests (~442 pass, ~15 pre-existing failures)
```

Integration tests that import `create_app` require the infrastructure services running and are slower.

### Running Lint

```bash
ruff check .       # ~1140 pre-existing issues
black --check .    # ~812 files need formatting
```

Both tools run correctly; issues are pre-existing in the codebase.

### Environment

- Python 3.12 (system), Node.js 22 (nvm)
- `.env` is created from `.env.example` with dev defaults during setup
- `APP_ENV=development` avoids production secret validation
- Docker required for PostgreSQL/Redis/MongoDB containers
