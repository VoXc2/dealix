# Railway Production Runbook

This guide deploys Dealix to Railway using the canonical production path: MySQL database + Node API worker + static frontend served by the API.

---

## Prerequisites

- Railway account and CLI (`npm i -g @railway/cli`)
- GitHub repo connected to Railway project (`VoXc2/dealix` or `Dealix-sa/dealix`)
- Domain configured (optional)

---

## 1. Create Railway Project

```bash
railway login
railway init --name dealix
```

Or connect the existing GitHub repo in the Railway dashboard.

---

## 2. Add MySQL Service

In the Railway dashboard:

1. Click **New** → **Database** → **Add MySQL**.
2. Wait for provisioning.
3. Copy the generated `DATABASE_URL`.

Alternatively, use a managed MySQL provider and add `DATABASE_URL` as a variable.

---

## 3. Configure Service Variables

Go to your Dealix service → **Variables** → **New Variable**.

### Required

| Variable | Source | Example |
|---|---|---|
| `NODE_ENV` | Raw | `production` |
| `PORT` | Raw | `3000` |
| `DATABASE_URL` | Reference | `${{MySQL.DATABASE_URL}}` |
| `APP_ID` | Raw | from Kimi app |
| `APP_SECRET` | Raw | from Kimi app |
| `KIMI_AUTH_URL` | Raw | `https://kimi-auth.example.com` |
| `KIMI_OPEN_URL` | Raw | `https://kimi-open.example.com` |

### Safety Defaults (must stay false)

```text
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
WHATSAPP_AGENT_MODE=dry_run
```

### Optional

```text
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_WEBHOOK_VERIFY_TOKEN=
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=noreply@dealix.me
AWS_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
```

---

## 4. Build Settings

Railway will detect the `Dockerfile.prod` or `Dockerfile` automatically. If not, set:

- **Builder:** Dockerfile
- **Dockerfile path:** `Dockerfile.prod`
- **Healthcheck path:** `/health`

---

## 5. Deploy

```bash
railway up
```

Or deploy from the Railway dashboard after pushing to `main`.

---

## 6. Run Database Migrations

After first deploy, run migrations from a Railway shell:

```bash
railway shell
npm run db:push
```

For production, prefer `npm run db:migrate` once migration files are generated.

---

## 7. Verify Deployment

```bash
curl https://YOUR_RAILWAY_DOMAIN/health
curl https://YOUR_RAILWAY_DOMAIN/ready
```

Expected:

```json
{ "status": "healthy", ... }
{ "status": "ready", ... }
```

---

## 8. Safety Gate Before Enabling Outbound

Before flipping any outbound flag to `true`, you must:

1. Create `.dealix_allow_external_send` locally with explicit whitelists.
2. Run `python scripts/verify_no_auto_external_send.py` and confirm PASS.
3. Get explicit founder approval.
4. Update only via Railway variables, never via code.

---

## 9. Monitoring

- Railway dashboard: logs, metrics, deployments.
- Health: `/health`
- Readiness: `/ready`
- API status: `/api/status` (after Phase 2)
- Outbound safety: `/api/outbound/safety` (after Phase 2)

---

## 10. Rollback

In Railway dashboard:

1. Go to **Deployments**.
2. Click the previous healthy deployment.
3. Click **Redeploy**.

Or via CLI:

```bash
railway deployment
# select previous deployment to rollback
```

---

## Checklist

- [ ] MySQL service provisioned
- [ ] `DATABASE_URL` referenced from MySQL service
- [ ] `NODE_ENV=production`
- [ ] Safety defaults all false
- [ ] `Dockerfile.prod` selected as builder
- [ ] Healthcheck path set to `/health`
- [ ] Migrations pushed
- [ ] `/health` and `/ready` respond 200
- [ ] No live outbound enabled without override
