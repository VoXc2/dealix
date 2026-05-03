# Dependency & Tooling Matrix

> Pinned vs. installed vs. fallback. Run command shown for every check.

| Tool / Library | Purpose | Required? | Installed | Fallback | Test | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `python` ≥ 3.11 | runtime | yes | 3.11.15 | n/a | `python --version` | PROVEN_LOCAL |
| `fastapi` ≥ 0.115 | HTTP framework | yes | from pyproject | n/a | `python -c "import fastapi"` | PROVEN_LOCAL |
| `uvicorn[standard]` | ASGI server | yes | from pyproject | n/a | `python -m uvicorn --version` | PROVEN_LOCAL |
| `pydantic` v2 | models | yes | from pyproject | n/a | `python -c "import pydantic"` | PROVEN_LOCAL |
| `pydantic-settings` | env loader | yes | from pyproject | n/a | `python -c "import pydantic_settings"` | PROVEN_LOCAL |
| `sqlalchemy[asyncio]` ≥ 2.0 | ORM + async | yes | from pyproject | n/a | `python -c "from sqlalchemy.ext.asyncio import create_async_engine"` | PROVEN_LOCAL |
| `aiosqlite` ≥ 0.20 | local/test sqlite driver | dev-only | added in this branch | n/a | `python -c "import aiosqlite"` | PROVEN_LOCAL |
| `asyncpg` | prod Postgres driver | prod | from pyproject | n/a | `python -c "import asyncpg"` | PROVEN_LOCAL |
| `httpx` | HTTP client | yes | from pyproject | requests fallback | `python -c "import httpx"` | PROVEN_LOCAL |
| `tenacity` | retries | yes | from pyproject | n/a | `python -c "import tenacity"` | PROVEN_LOCAL |
| `python-dotenv` | env file loader | optional | from pyproject | env vars work without it | `python -c "import dotenv"` | PROVEN_LOCAL |
| `pytest` ≥ 8.3 | tests | dev | from pyproject | n/a | `python -m pytest --version` | PROVEN_LOCAL |
| `pytest-asyncio` | async tests | dev | from pyproject | n/a | `python -m pytest --version` | PROVEN_LOCAL |
| `structlog` | logging | yes | from pyproject | std logging | `python -c "import structlog"` | PROVEN_LOCAL |
| `langfuse` | LLM tracing | optional | from pyproject | no-op without keys | `python -c "import langfuse"` | PROVEN_LOCAL (optional) |
| `anthropic` SDK | Claude provider | optional | from pyproject | rule-based fallback | `python -c "import anthropic"` | PROVEN_LOCAL (optional) |
| `openai` SDK | OpenAI provider | optional | from pyproject | rule-based fallback | `python -c "import openai"` | PROVEN_LOCAL (optional) |
| `google-generativeai` | Gemini | optional | from pyproject | rule-based fallback | `python -c "import google.generativeai"` | PROVEN_LOCAL (optional) |
| `hubspot-api-client` | HubSpot CRM | optional | from pyproject | n/a (graceful) | `python -c "import hubspot"` | PROVEN_LOCAL (optional) |
| `google-api-python-client` | Google API (Gmail OAuth, Calendar) | optional | from pyproject | drafts-only fallback | `python -c "import googleapiclient"` | PROVEN_LOCAL (optional) |
| `resend` | email | optional | from pyproject | n/a | `python -c "import resend"` | PROVEN_LOCAL (optional) |
| `phonenumbers` | E.164 parsing | yes | from pyproject | n/a | `python -c "import phonenumbers"` | PROVEN_LOCAL |
| `email-validator` | email parsing | yes | from pyproject | n/a | `python -c "import email_validator"` | PROVEN_LOCAL |
| `redis` | cache + idempotency | yes | from pyproject | in-memory fallback | `python -c "import redis"` | PROVEN_LOCAL |
| `motor` | mongo (project memory) | optional | from pyproject | local file fallback | `python -c "import motor"` | PROVEN_LOCAL (optional) |

## Proof / PDF stack

| Library | Status |
| --- | --- |
| `jinja2` | available transitively via fastapi/starlette — PROVEN_LOCAL |
| `reportlab` | NOT in `requirements.txt` — proof packs are Markdown today — BACKLOG |
| `weasyprint` | not present — BACKLOG |
| `hmac` / `hashlib` | stdlib — available — PROVEN_LOCAL but not yet wired into Proof Pack response — BACKLOG |

## Integration clients

| Integration | Status |
| --- | --- |
| Moyasar invoice + webhook | client `dealix/payments/moyasar.py` — PROVEN_LOCAL; webhook 401-on-unsigned PROVEN_LIVE |
| Meta WhatsApp Cloud (inbound) | webhook `webhooks/whatsapp` — PROVEN_LIVE (verify-token gate enforced) |
| Meta WhatsApp Cloud (outbound) | gated false by default — PROVEN_LIVE blocked |
| SMTP / Gmail | drafts-only when configured; live send blocked by default — PROVEN_LIVE blocked |
| Google Search API | optional; graceful fallback when keys missing — PROVEN_LIVE (test_provider_smoke skips when unset) |
| LLM providers | router selects from available; deterministic fallback when no keys — PROVEN_LIVE (groq active on prod) |
| Railway | hosting — PROVEN_LIVE |
| GitHub Pages | static landing — not directly probed |

## What is missing (BACKLOG, not blocker)

- `reportlab` for hosted Proof Pack PDFs.
- HMAC signature on Proof Pack JSON.
- Alembic-driven migration framework (current: ad-hoc safe scripts).
- Sentry breadcrumbs wired into structlog events (skeleton present).
