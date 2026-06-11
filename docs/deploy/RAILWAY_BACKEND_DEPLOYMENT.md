# Railway Backend Deployment

## 1. Connect repo
- New project from GitHub
- Root: `api/`

## 2. Env vars
- `APP_ENV=production`
- `DATABASE_URL` — Postgres URL
- `APP_SECRET_KEY` — long random
- `ENVIRONMENT=production`
- `MOYASAR_*` — only if billing live

## 3. Health check
- `GET /healthz` — should return 200

## 4. Smoke
- `python3 scripts/post_deploy_smoke.py --base-url https://<railway-domain>`

## 5. Rollback
- Railway → Deployments → Redeploy previous
