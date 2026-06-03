# Dealix Railway Founder OS Runbook

## الخدمات المطلوبة

| الخدمة | النوع | Public Domain | Start Command |
|---|---|---|---|
| dealix / cv | API | api.dealix.me | empty أو /app/start.sh |
| web | Web | web-production... | حسب Next.js |
| Postgres | Database | لا | Railway Postgres |
| founder-os-worker | Worker دائم | لا | python scripts/founder_os_worker.py |
| dealix-watchdog | Cron | لا | python scripts/railway_watchdog.py |

## متغيرات خدمة API

- APP_ENV=production
- ENVIRONMENT=production
- APP_URL=https://api.dealix.me
- BASE_URL=https://api.dealix.me
- RAILWAY_DOCKERFILE_PATH=Dockerfile
- PYTHONUTF8=1
- PYTHONIOENCODING=utf-8
- DATABASE_URL=${{Postgres.DATABASE_URL}}
- APP_SECRET_KEY=secret قوي
- JWT_SECRET_KEY=secret قوي
- API_KEYS=key قوي
- ADMIN_API_KEYS=admin key قوي
- DEALIX_ADMIN_API_KEY=admin key قوي

## متغيرات Founder OS Worker

- APP_ENV=production
- ENVIRONMENT=production
- DATABASE_URL=${{Postgres.DATABASE_URL}}
- APP_URL=https://api.dealix.me
- DEALIX_API_URL=https://api.dealix.me
- FOUNDER_OS_ENABLED=true
- HERMES_AGENTS_ENABLED=true
- AGENT_RUNTIME=railway
- AGENT_MODE=founder_os
- AGENT_APPROVAL_MODE=required
- AUTO_SEND_ENABLED=false
- EXTERNAL_OUTREACH_ENABLED=false
- FOUNDER_OS_INTERVAL_SECONDS=900

## Watchdog

- Service: dealix-watchdog
- Start Command: python scripts/railway_watchdog.py
- Cron: */15 * * * *
- Variables:
  - APP_URL=https://api.dealix.me
  - DEALIX_HEALTH_PATH=/healthz
