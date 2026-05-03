# Railway Cutover Runbook (production redeploy)

> Order matters. Each step is non-destructive and verifiable.

## Pre-cutover state

- Production runs on `claude/launch-command-center-6P4N0` (deploy branch).
- This PR (`claude/dealix-staging-readiness-LJOju`, #131) is staged for merge.
- 22/22 read smoke green. 3/4 Arabic Saudi cold-WA blocks fail at the
  operator chat layer (channel layer already blocks).

## Cutover steps (do these in order)

### Step 1 — Merge PR #131

GitHub → PR #131 → Merge. Squash or merge-commit; do NOT rebase
(history-preserving merge keeps the AsyncSession fix attribution).

### Step 2 — Apply the 4-line operator wiring patch

Open `api/routers/operator.py` on the deploy branch. Apply the patch
documented in `docs/OPERATOR_WIRING_PATCH.md`. Push.

### Step 3 — Run the Postgres migration

```bash
DATABASE_URL='<railway pg url>' python scripts/migrate_add_hubspot_deal_id.py
```

Expected: `MIGRATION_OK`. See `docs/DB_MIGRATION_RUNBOOK.md`.

### Step 4 — Railway redeploy

Railway dashboard → deployments → trigger redeploy on the merged commit.
Wait for healthcheck to flip green. Railway will not switch traffic until
`/health` returns 200.

### Step 5 — Re-run staging smoke

```bash
BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
```

Expected: `PASS=36  FAIL=0`. Specifically:

- `[7] Service Tower` 6/6 pass
- `[8] Role briefs` 4/4 pass (incl. sales_manager — only after migration)
- `[9] Operator unsafe Arabic block` 4/4 BLOCKED

## Required Railway env (must remain unchanged)

```
APP_ENV=production
APP_SECRET_KEY=<generated 32-byte; do NOT commit>
DATABASE_URL=<Railway Postgres>
WHATSAPP_ALLOW_LIVE_SEND=false
WHATSAPP_ALLOW_INTERNAL_SEND=false
WHATSAPP_ALLOW_CUSTOMER_SEND=false
MOYASAR_ALLOW_LIVE_CHARGE=false
GMAIL_ALLOW_LIVE_SEND=false
CALLS_ALLOW_LIVE_DIAL=false
LINKEDIN_ALLOW_AUTOMATION=false
MOYASAR_MODE=sandbox
PYTHONUNBUFFERED=1
```

## Hard rules

- Do NOT add `MOYASAR_SECRET_KEY` (live).
- Do NOT flip any `*_ALLOW_LIVE_*` to true.
- Do NOT add `WHATSAPP_ACCESS_TOKEN` for outbound until template + opt-in path is wired.
- Do NOT add Gmail OAuth tokens for live send.

## Rollback

If healthcheck fails after redeploy:

1. Railway → previous deployment → "Redeploy" — instant revert.
2. The migration is forward-compatible (nullable column); no rollback needed.
3. The operator wiring patch is forward-compatible too — old code continues to
   work; the new code adds blocks but never changes existing safe responses.

## Post-cutover verification (must all be true)

| Check | Command | Expected |
| --- | --- | --- |
| Health | `curl -fsS https://api.dealix.me/health` | 200 with providers populated |
| Service catalog | `curl -fsS https://api.dealix.me/api/v1/services/catalog` | 6 bundles |
| Role brief sales_manager | `curl -fsS 'https://api.dealix.me/api/v1/role-briefs/daily?role=sales_manager'` | 200, no `_errors` |
| WhatsApp brief sales_manager | `curl -fsS 'https://api.dealix.me/api/v1/whatsapp/brief?role=sales_manager'` | 200 |
| Compliance check (DB write) | `curl -X POST https://api.dealix.me/api/v1/compliance/check-outreach -H 'Content-Type: application/json' -d '{"to_email":"x@y.sa","contact_opt_out":true,"allowed_use":"cold_purchased"}'` | 200 with `allowed:false` |
| Cold WA arabic blocked | `curl -X POST https://api.dealix.me/api/v1/operator/chat/message -H 'Content-Type: application/json' -d '{"text":"أبي أرسل واتساب لأرقام مشتريها"}'` | `blocked:true` |
| WhatsApp test-send | `curl -X POST 'https://api.dealix.me/api/v1/os/test-send?phone=...&body=hi'` | `{"status":"blocked","error":"whatsapp_allow_live_send_false"}` |
| Moyasar webhook unsigned | `curl -X POST -H 'Content-Type: application/json' -d '{}' https://api.dealix.me/api/v1/webhooks/moyasar` | 401 |
