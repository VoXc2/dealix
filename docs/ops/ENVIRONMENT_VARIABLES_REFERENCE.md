# Environment Variables Reference

## Core Application
| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| APP_ENV | development | Yes | development \| staging \| production \| test |
| ENVIRONMENT | development | Yes | Legacy alias for APP_ENV (env contract checker) |
| APP_LOG_LEVEL | INFO | No | DEBUG \| INFO \| WARNING \| ERROR \| CRITICAL |
| LOG_LEVEL | INFO | No | Legacy alias for APP_LOG_LEVEL |
| APP_SECRET_KEY | change-me | Yes | 64-byte hex secret |
| JWT_SECRET_KEY | change-me | Yes | 64-byte hex JWT secret |
| API_KEYS | (empty) | No | Comma-separated client API keys |
| ADMIN_API_KEYS | (empty) | No | Comma-separated admin API keys |
| DATABASE_URL | postgresql+asyncpg://... | Yes | Postgres connection string |
| REDIS_URL | redis://localhost:6379/0 | No | Redis connection string |
| CORS_ORIGINS | http://localhost:3000 | Yes | Comma-separated CORS origins |
| APP_URL | http://localhost:8000 | No | Public API URL |
| BASE_URL | http://localhost:8000 | No | Base URL for links |
| DEALIX_API_BASE | http://localhost:8000 | No | API base for frontend |
| DEALIX_ORCHESTRATOR_BACKEND | automatic | Production | `memory`, `json`, or `postgres`. Production defaults to and requires `postgres`; non-production defaults to JSON when a state path exists, otherwise memory. |
| DEALIX_ORCHESTRATOR_DATABASE_URL | DATABASE_URL | No | Optional dedicated PostgreSQL URL for workflow/task state. Empty reuses `DATABASE_URL`. |
| DEALIX_ORCHESTRATOR_STATE_PATH | (empty) | JSON only | Prefix for atomic JSON task/run state in single-node non-production deployments. Creates `.tasks.json` and `.runs.json`. |

## Outbound Safety (all disabled by default)
| Variable | Default | Description |
|----------|---------|-------------|
| EXTERNAL_SEND_ENABLED | false | Master switch for external sending |
| OUTBOUND_MODE | draft_only | draft_only \| controlled_live |
| EMAIL_SEND_ENABLED | false | Email channel switch |
| WHATSAPP_SEND_ENABLED | false | WhatsApp channel switch |
| WHATSAPP_ALLOW_LIVE_SEND | false | WhatsApp live send (template-only by default) |
| SMS_SEND_ENABLED | false | SMS channel switch |

## Railway Production
- DATABASE_URL is set by Railway Postgres plugin: `${{Postgres.DATABASE_URL}}`
- REDIS_URL is set by Railway Redis plugin: `${{Redis.REDIS_URL}}`
- All outbound safety flags must remain false unless explicitly approved

## Safety Rules
- Never commit real secrets to the repo
- Never set EXTERNAL_SEND_ENABLED=true in .env.example
- Never set OUTBOUND_MODE to anything other than draft_only in examples
- Generate secrets with: `python -c "import secrets; print(secrets.token_hex(32))"`
