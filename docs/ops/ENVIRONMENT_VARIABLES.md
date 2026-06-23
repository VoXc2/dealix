# Environment Variables

This document is the single source of truth for Dealix environment variables. See `.env.example` for a copy-paste template.

---

## Required for Local Development

| Variable | Default | Description |
|---|---|---|
| `NODE_ENV` | `development` | Node environment: `development`, `test`, or `production` |
| `PORT` | `3000` | Port the API server listens on |
| `DATABASE_URL` | `mysql://dealix:dealix_pass_2026@localhost:3306/dealix` | MySQL connection string |
| `DB_USER` | `dealix` | MySQL user (used by Docker Compose) |
| `DB_PASSWORD` | `dealix_pass_2026` | MySQL password (used by Docker Compose) |
| `DB_NAME` | `dealix` | MySQL database name |
| `DB_PORT` | `3306` | MySQL host port |
| `DB_ROOT_PASSWORD` | `dealix_root_2026` | MySQL root password (Docker Compose) |

## Auth / App

| Variable | Required? | Description |
|---|---|---|
| `APP_ID` | Yes in production | Kimi OAuth app ID |
| `APP_SECRET` | Yes in production | Kimi OAuth app secret |
| `KIMI_AUTH_URL` | Yes in production | Kimi auth endpoint |
| `KIMI_OPEN_URL` | Yes in production | Kimi API base URL |
| `OWNER_UNION_ID` | No | Owner user union ID for admin access |
| `VITE_APP_ID` | No | App ID exposed to the frontend |
| `VITE_KIMI_AUTH_URL` | No | Auth URL exposed to the frontend |

## Safety Defaults (DO NOT CHANGE without explicit approval)

| Variable | Required Default | Description |
|---|---|---|
| `EXTERNAL_SEND_ENABLED` | `false` | Master switch for any external send |
| `EMAIL_SEND_ENABLED` | `false` | Email send switch |
| `WHATSAPP_SEND_ENABLED` | `false` | WhatsApp send switch |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | Allow real WhatsApp sends |
| `SMS_SEND_ENABLED` | `false` | SMS send switch |
| `OUTBOUND_MODE` | `draft_only` | Operating mode: `draft_only` or `live` |
| `WHATSAPP_AGENT_MODE` | `dry_run` | WhatsApp mode: `dry_run` or `live` |

## Optional Integrations

### WhatsApp Cloud API

| Variable | Description |
|---|---|
| `WHATSAPP_ACCESS_TOKEN` | Meta access token |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp phone number ID |
| `WHATSAPP_WEBHOOK_VERIFY_TOKEN` | Webhook verification token |

### Email (SMTP)

| Variable | Default | Description |
|---|---|---|
| `SMTP_HOST` | — | SMTP host |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USER` | — | SMTP username |
| `SMTP_PASSWORD` | — | SMTP password |
| `EMAIL_FROM` | `noreply@dealix.me` | Default sender address |

### AWS / S3 (optional)

| Variable | Description |
|---|---|
| `AWS_REGION` | AWS region |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `S3_BUCKET_NAME` | S3 bucket for file uploads |

---

## Usage

```bash
# Local development
cp .env.example .env.local
# Edit .env.local with your values
npm run dev
```

```bash
# Docker Compose local
mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS dealix;"
docker compose up -d
```

```bash
# Production (Railway)
# Set DATABASE_URL via Railway Postgres/MySQL service reference variables.
# See docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md
```

---

## Security Notes

- Never commit `.env.local`, `.env.production`, or any file containing real secrets.
- `.env.example` must contain only placeholder or safe default values.
- Live outbound variables must remain `false` unless explicitly approved and tracked.
