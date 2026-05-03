# Dealix — Dependency Map

> Every capability → the library that powers it → the import path. Used as
> a quick "what would break if I removed X?" reference.

| Capability | Library | Import path | Notes |
|---|---|---|---|
| HTTP API framework | fastapi | `from fastapi import APIRouter` | core |
| ASGI server | uvicorn | `uvicorn api.main:app` | Railway entrypoint |
| Schema validation | pydantic | implicit via FastAPI | core |
| Settings / env | pydantic-settings | `core/config/settings.py` | env-driven |
| Async ORM | sqlalchemy[asyncio] | `from sqlalchemy.ext.asyncio import AsyncSession` | core |
| Postgres driver | asyncpg | implicit via SQLAlchemy URL `postgresql+asyncpg://...` | production |
| SQLite driver (test) | aiosqlite | `DATABASE_URL=sqlite+aiosqlite:///...` | tests + local acceptance |
| HTTP client (outbound) | httpx | `import httpx` | Moyasar invoices, etc. |
| Templates | jinja2 | `auto_client_acquisition/revenue_company_os/proof_pack_pdf.py` | Proof Pack HTML |
| PDF rendering (optional) | weasyprint | optional fallback in `proof_pack_pdf.py` | HTML fallback if missing |
| HMAC signatures | hmac, hashlib (stdlib) | `proof_pack_pdf.py:_signature` | no external dep |
| Structured logging | structlog | `core/logging.py` | hooked into RequestIDMiddleware |
| Tests | pytest, pytest-asyncio | `tests/` | required |
| LLM SDK | anthropic | `auto_client_acquisition/agents/...` | optional, gate-guarded |
| LLM SDK (alt) | openai | optional | optional |
| LLM SDK (alt) | google-generativeai | optional | optional |

## Capability fallbacks

| Capability | Primary | Fallback |
|---|---|---|
| Proof Pack PDF | weasyprint binary | printable HTML (browser save-as-PDF) |
| Moyasar invoice | API call with `MOYASAR_SECRET_KEY` | `https://api.dealix.me/manual-pay?...` link |
| WhatsApp send | Meta Cloud API (gate=False today) | Copy-to-clipboard from preview UI |
| LLM-generated drafts | provider via `core/ai/router.py` | Static deterministic templates |

## Audit commands

```bash
# Confirm all imports resolve
python -c "
from api.main import app
from auto_client_acquisition.compliance.forbidden_claims import scan
from auto_client_acquisition.revenue_company_os.proof_ledger import record
from auto_client_acquisition.revenue_company_os.role_brief_builder import build
print('imports OK')
"

# pip check
python -m pip check
```
