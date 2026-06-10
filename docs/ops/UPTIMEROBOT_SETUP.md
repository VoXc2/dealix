# UptimeRobot — Setup Runbook

> Replaces the previous "see Issue #85" reference. Self-contained instructions.

## Why
External, third-party monitor that verifies Dealix from outside the Railway network. Catches DNS, TLS, and full-stack outages that internal health-checks miss.

## Account
- URL: https://uptimerobot.com
- Owner: founder (`sami.assiri11@gmail.com`)
- Plan: Free tier (50 monitors, 5-min interval). Upgrade to Pro ($7/mo) only if 1-min interval is needed.

## Monitors (configure in order)

### 1. Backend health (P0)
- Type: **HTTPS**
- URL: `https://api.dealix.me/healthz`
- Interval: **5 minutes**
- Timeout: 30s
- Alert when: down for **2+ consecutive checks** (avoid one-off blips)
- Keyword (optional, recommended): expect `"ok"` in response body
- Name: `dealix-api-healthz`

### 2. Public landing (P0)
- Type: **HTTPS**
- URL: `https://dealix.sa`
- Interval: 15 minutes
- Alert when: down for 2+ consecutive checks
- Keyword: expect `Dealix` in response body
- Name: `dealix-landing`

### 3. Pricing endpoint = DB liveness (P1)
- Type: **HTTPS**
- URL: `https://api.dealix.me/api/v1/pricing/plans`
- Interval: 15 minutes
- Alert when: down for 2+ checks **OR** keyword `pilot_1sar` missing
- Name: `dealix-pricing-db-liveness`

### 4. Dashboard (P1)
- Type: **HTTPS**
- URL: `https://dashboard.dealix.me/_stcore/health` (Streamlit health endpoint)
- Interval: 15 minutes
- Name: `dealix-dashboard`

### 5. Webhook receiver (P1)
- Type: **HTTPS**
- URL: `https://api.dealix.me/api/v1/webhooks/moyasar` (POST with empty body → expects 4xx, not 5xx)
- Interval: 15 minutes
- Expected status: anything `< 500`
- Name: `dealix-moyasar-webhook`
- _(Moyasar's own pings will create activity here — that's fine.)_

## Alert Contacts

1. **Email — primary**
   - `sami.assiri11@gmail.com` → trigger after 2 minutes of downtime

2. **Email — on-call rotation alias**
   - `oncall@dealix.sa` (or interim: founder personal email)

3. **WhatsApp webhook** (optional but recommended)
   - URL: paste a custom webhook that hits an internal Lambda which forwards to WhatsApp
   - Format: `{"event":"down","monitor":"$monitorFriendlyName","url":"$monitorURL"}`

4. **Better Stack / status page push** (P3)
   - Public status page consumed from `https://status.dealix.sa`

## Status Page (public)
- Better Stack free tier publishes `status.dealix.sa`
- Shows: api, landing, dashboard, payments
- Subscribers can self-subscribe by email

## Drill — kill-switch test (T-7 days before launch)

```bash
# 1. In Railway, scale dealix service to 0 replicas
# 2. Wait 2-3 min
# 3. Verify UptimeRobot alert fires (email + WhatsApp)
# 4. Scale back to 1
# 5. Verify UptimeRobot marks restored
```

Document the result in `docs/ops/observability_drills.md`.

## Monthly verification
On the 1st of each month, DPO+CTO confirm:
- All 5 monitors are green or recovered
- Alert contacts unchanged
- No missed alerts in the last 30 days

## Rotation when founder is unreachable
If founder is unavailable >24h:
- Secondary contact is added to alert list (CTO when hired, interim: trusted advisor)
- Document in `docs/ops/ON_CALL_ROTATION.md`
