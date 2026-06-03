# Release Day Runbook (T-0)

> Hour-by-hour playbook for GA. Pick a Tuesday or Wednesday. Start at 09:00 AST.

## Roles for the day

| Role | Name | Where they are |
|------|------|----------------|
| Release captain | _Sami_ | Slack `#dealix-launch` |
| Engineering on-call | _CTO/contractor_ | Slack + phone |
| Comms / marketing | _Growth_ | Slack + scheduled posts |
| DPO | _DPO name_ | Phone (reachable, not at terminal) |

War room: video call kept open from T-30m to T+4h. Don't multi-task in this window.

---

## T-24h — Code freeze
- [ ] CTO confirms: only hotfixes merged in the last 24h, all signed off.
- [ ] All open `claude/*` branches not in scope for GA → tagged "post-launch".
- [ ] Staging green: `bash scripts/revenue_os_master_verify.sh` returns `PASS`.
- [ ] Lighthouse + Pa11y green on landing.
- [ ] Backup drill from yesterday's drill log shows PASS.

## T-12h — Final staging smoke
```bash
bash scripts/revenue_os_master_verify.sh
APP_ENV=test python scripts/smoke_inprocess.py
bash scripts/check_alembic_heads.sh
```
All three return success. Record exit codes in `docs/ops/release_logs/<date>.md`.

## T-2h — DNS + env
- [ ] `dig +short A api.dealix.me` → expected Railway IPs, TTL ≤ 300
- [ ] `dig +short A dealix.sa` → expected static host (Netlify/Vercel), TTL ≤ 300
- [ ] `dig +short A dashboard.dealix.me` → expected, TTL ≤ 300
- [ ] Railway env vars audit: open vars panel, check every required key from `.env.example` (see master `GO_LIVE_INDEX.md` for the full list).

## T-1h — Pre-flight
- [ ] War room call started
- [ ] Slack `#dealix-launch` pinned with this runbook
- [ ] On-call has phone on, charger plugged in
- [ ] Press release embargo confirmed in journalists' mailboxes
- [ ] Calendly slots reserved (9:30 / 11:00 / 14:00) for first-customer calls

## T-30m — Final checks
- [ ] No active SEV-2+ from Sentry in last 24h
- [ ] UptimeRobot all monitors green
- [ ] PostHog ingest healthy
- [ ] No active deploys mid-stream

---

## T-0 (09:00 AST) — Go live

### Step 1 — Remove maintenance flag, deploy
```bash
# In Railway dashboard:
#   1. Production service → Variables → remove MAINTENANCE_MODE if present
#   2. Variables → save (triggers redeploy on dependent vars)
#   3. Deployments → trigger Manual Deploy from main
```

### Step 2 — Wait for /healthz (release captain)
```bash
URL="https://api.dealix.me"
for i in {1..20}; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" "$URL/healthz")
  echo "$(date -u +%T) attempt $i: $code"
  [[ "$code" == "200" ]] && break
  sleep 15
done
```
Expected: `200` within 5 minutes.

### Step 3 — Visual smoke (release captain, 5 minutes)
Open in browser and click through:
- [ ] https://dealix.sa loads, hero copy intact
- [ ] https://dealix.sa/pricing.html — 4 plans visible
- [ ] https://dealix.sa/diagnostic.html — interactive
- [ ] https://dealix.sa/proof.html — loads with proofs
- [ ] https://dashboard.dealix.me — login screen renders
- [ ] https://api.dealix.me/docs — OpenAPI loads

### Step 4 — 1 SAR end-to-end test (T+15m, CEO/captain personally)
```bash
curl -X POST https://api.dealix.me/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"plan":"pilot_1sar","email":"<ceo-personal>@gmail.com"}' | jq
```
- [ ] Open the `payment_url` in browser
- [ ] Complete payment with personal card (real 1 SAR)
- [ ] Within 60s: PostHog `checkout_success` event fires
- [ ] Within 60s: DB row updated to `paid`
- [ ] Sentry: zero new errors in the last 5 minutes
- [ ] Confirmation email arrives to CEO inbox

If any of the above fails → see **Abort criteria** below.

### Step 5 — Internal announcement (T+1h)
- [ ] Slack `#dealix-launch` post: "🚀 GA is live"
- [ ] Founder LinkedIn post goes live (already scheduled)
- [ ] X thread goes live (already scheduled)

### Step 6 — First batch outreach (T+2h)
- [ ] First 50 hand-picked targets get WhatsApp+Email (via `dealix_whatsapp_morning_brief.py` + Gmail batch)
- [ ] Confirm send counters increment in PostHog

### Step 7 — Mid-day pulse (T+4h)
- [ ] PostHog funnel review (landing → demo → pilot)
- [ ] Sentry error rate < 0.5% over the last 4 hours
- [ ] UptimeRobot: all monitors still green
- [ ] DLQ size on all queues ≤ 0–1

### Step 8 — Press wave (T+8h)
- [ ] Embargo officially lifted with reporters who replied
- [ ] LinkedIn newsletter issue sends
- [ ] Partner agencies receive "Day 1 numbers" Slack/WhatsApp

### Step 9 — EOD retro (T+12h)
- [ ] 15-min retro call (war room reconvenes)
- [ ] Fill `docs/ops/release_logs/<date>.md` with:
  - Timestamps for each step
  - Counts: visits, demos, pilots, paid
  - Issues encountered + how resolved
  - Action items for T+1

---

## Abort criteria — stop immediately if

- `/healthz` does NOT return 200 within 5 minutes of cutover
- Sentry error rate > 5% sustained 5 minutes
- Moyasar webhook returns 401 (signature mismatch) — config drift
- Any secret value appears in logs / Sentry / public response
- Customer reports money taken but no service granted (any single instance)

**On abort → execute `docs/ops/ROLLBACK_RUNBOOK.md` immediately.** Don't try to fix forward during launch.

---

## Communication during abort

- Status page `status.dealix.sa` → "Investigating" within 10 minutes
- Founder LinkedIn / X postpone scheduled launch posts (toggle off)
- Press email: "Brief delay, will follow up within the hour"
- Slack `#dealix-launch` → captain + IC actively in war room

---

## Definition of "GA day successful"

By T+12h, all of these are true:
- ≥ 1 real paying customer (paid checkout_success with non-`pilot_1sar` plan), OR ≥ 3 pilots
- Uptime ≥ 99% over the day
- Zero unresolved SEV-1
- ≤ 1 unresolved SEV-2
- DLQ depth ≤ 5 on all queues
- Press release published and visible at https://dealix.sa/news/2026-launch
- ≥ 500 unique visitors to landing

Below the bar = call out in the retro, plan recovery in T+1 daily.
