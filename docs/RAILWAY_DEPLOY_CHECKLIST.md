# Railway Deploy Checklist (Dealix prod)

> Source of truth: `railway.json`, `Dockerfile`, `core/config/settings.py`,
> live behavior on `https://api.dealix.me`.

## Branch + start command

| Setting | Value | Verified |
| --- | --- | --- |
| Branch | `claude/launch-command-center-6P4N0` (current deploy) | live |
| After this PR merges | rebuild from the merged branch | needed |
| Builder | Dockerfile (multi-stage, non-root) | `railway.json` line 4 |
| Start command | `uvicorn api.main:app --host 0.0.0.0 --port $PORT` | implemented in `Dockerfile` start.sh |
| Healthcheck path | `/healthz` (current `railway.json`) — also `/health` works | both routes return 200 |

> **Note:** `railway.json` is set to `/healthz`, but the spec asked for `/health`.
> Both paths return 200 today (`api/routers/health.py` registers both).
> If you prefer `/health` for clarity, change `railway.json` line 7 from
> `"healthcheckPath": "/healthz"` → `"healthcheckPath": "/health"` and redeploy.

## Required env on Railway (safe defaults)

| Variable | Value | Why |
| --- | --- | --- |
| `APP_ENV` | `production` | non-test mode |
| `APP_SECRET_KEY` | `<32-byte random>` (do NOT put in repo) | session signing |
| `DATABASE_URL` | Railway-Postgres connection URL | persistent state |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | hard rule |
| `WHATSAPP_ALLOW_INTERNAL_SEND` | `false` | hard rule |
| `WHATSAPP_ALLOW_CUSTOMER_SEND` | `false` | hard rule |
| `MOYASAR_ALLOW_LIVE_CHARGE` | `false` | hard rule (env not currently consumed by code; presence is documentation) |
| `GMAIL_ALLOW_LIVE_SEND` | `false` | hard rule |
| `CALLS_ALLOW_LIVE_DIAL` | `false` | hard rule |
| `LINKEDIN_ALLOW_AUTOMATION` | `false` | hard rule |
| `MOYASAR_MODE` | `sandbox` | until paid-beta gate |
| `PYTHONUNBUFFERED` | `1` | clean log streaming |

**Do NOT add until paid-beta is explicitly approved:**

- `MOYASAR_SECRET_KEY` (live key)
- `WHATSAPP_ACCESS_TOKEN` with `WHATSAPP_ALLOW_LIVE_SEND=true`
- `GMAIL_REFRESH_TOKEN` + `GMAIL_SENDER_EMAIL` with live send true

## Railway healthcheck constraint (operational)

Railway gates traffic switchover behind a 200 from the configured health
path. If the path returns non-200 during boot, the new deploy is rejected
and the previous deploy keeps serving. To debug a boot failure:

1. Tail logs: Railway → Deployments → latest → Logs
2. Common boot failures:
   - missing `APP_SECRET_KEY` → app refuses to start (settings validator)
   - missing `DATABASE_URL` → app boots, but health may return degraded
   - import error → check `python -m compileall api auto_client_acquisition` locally first

## Post-deploy smoke

After every redeploy, run:

```bash
BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
```

Expected after this PR is merged + redeployed:

- 6/6 service tower bundles → 200
- 4/4 role briefs probed → 200 (incl. sales_manager once schema is fixed)
- whatsapp/brief growth_manager → 200
- 4/4 operator Arabic+English unsafe phrasings → blocked
- moyasar webhook unsigned → 401
- whatsapp test-send → blocked

## What this PR will turn green on prod

| Endpoint | Before redeploy | After redeploy |
| --- | --- | --- |
| `/api/v1/automation/status` | 500 | 200 |
| `/api/v1/compliance/check-outreach` | 500 | 200 |
| operator chat — 3 Arabic Saudi phrasings | not blocked | blocked (after wiring patch) |

## What this PR does NOT fix (still BLOCKER)

| Endpoint | Status | Fix |
| --- | --- | --- |
| `/api/v1/role-briefs/daily?role=sales_manager` | 500 (schema drift) | Postgres migration to add `deals.hubspot_deal_id` |
| `/api/v1/whatsapp/brief?role=sales_manager` | 500 (same) | same migration |
| `/api/v1/whatsapp/brief?role=ceo` | 500 (same) | same migration |
| role aliases `marketing_manager`, `finance_manager` | 400 | one-line alias map in deploy-branch role-briefs router |

These are tracked in `docs/REAL_CUSTOMER_OPS_TRUTH_REPORT.md` §11 and
`docs/ROLE_BRIEFS_OPERATING_MODEL.md`.
