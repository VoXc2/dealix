# Sentry — Setup Runbook

> Code wiring already exists at `dealix/observability/sentry.py` (called via `setup_sentry()` in `api/main.py:148`). This runbook is the ops + alerting side.

## Account
- URL: https://sentry.io
- Org: `dealix`
- Plan: Developer (free, 5k events/mo). Upgrade to Team ($26/mo) if event volume exceeds free tier.

## Projects
Create **2** projects:

1. **`dealix-backend`** (Python / FastAPI)
   - Platform: Python
   - Framework: FastAPI
   - DSN → goes into Railway env var `SENTRY_DSN`
2. **`dealix-landing`** (Browser / JS)
   - Platform: Browser JavaScript
   - DSN → goes into `landing/assets/js/sentry.js` (loaded on every page)

## Environment Variables (Railway production)

```env
SENTRY_DSN=https://<key>@<org>.ingest.sentry.io/<project>
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1        # 10% of requests get full traces
SENTRY_PROFILES_SAMPLE_RATE=0.0      # off in cost-saving mode; bump to 0.1 if needed
SENTRY_RELEASE=$RAILWAY_GIT_COMMIT_SHA
```

Code at `dealix/observability/sentry.py` already reads `SENTRY_DSN` and sets
`environment` + `traces_sample_rate`. Verify on first deploy that
`sentry_sdk.Hub.current.client` is not None.

## PII Scrubbing — critical

Sentry must **not** receive PII. Configure in `sentry_sdk.init(...)`:

```python
send_default_pii=False              # never send IP / auth headers
before_send=scrub_pii               # custom hook (see below)
```

Scrubber rules (already partially in `sentry.py`):
- Strip `Authorization`, `Cookie`, `X-API-Key` headers
- Strip query strings on `/api/v1/admin/*`, `/api/v1/auth/*`
- Mask request bodies on `/checkout`, `/webhooks/*` (replace with `<redacted>`)
- Drop events from `tests/` paths

**Verify after each release**: pick 1 random event, confirm no email/phone/national ID.

## Alert Rules

Configure in Sentry → Alerts → Create Alert.

1. **SEV-1: Webhook 5xx**
   - Conditions: An event triggers on `tags.url` matches `*/webhooks/*` AND `level == error`
   - Action: page on-call (email + WhatsApp via integration)
   - Frequency: at most every 5 min

2. **SEV-2: Error spike**
   - Conditions: Number of new events > 10 in 5 minutes
   - Action: email on-call
   - Frequency: at most every 15 min

3. **SEV-3: Performance regression**
   - Conditions: P95 transaction `POST /api/v1/checkout` > 1500ms over 10 min
   - Action: email engineering

4. **Release-gate: pre-existing issue resurrects**
   - Conditions: a resolved issue re-occurs
   - Action: email engineering

## Test Sentry is working (post-deploy smoke)

```bash
# Intentionally-throwing endpoint (already wired in api/routers/health.py)
curl https://api.dealix.me/_test_sentry

# Expected: 500 from API + new event visible in Sentry within 30s
# Endpoint is undocumented (include_in_schema=False); the path is intentional
# so probing scanners don't find it without insider knowledge.
```

If no event appears within 1 minute → check:
1. `SENTRY_DSN` env var actually set in Railway
2. `setup_sentry()` ran without exception (look for `sentry_init_ok` in Railway logs)
3. Network egress from Railway to `sentry.io` not blocked

## Quota management

Free tier = 5k events/month. To prevent burning quota:
- Rate limit at the SDK: `sample_rate=0.5` on noisy events (e.g. transient 502s)
- Use Sentry inbound filters to drop browser noise (extension crashes, etc.)
- Set spike-protection threshold to **150% of monthly avg**

## Monthly review
DPO + Eng review on the 1st of each month:
- Any unresolved P0 issues? → assign owner
- Quota usage trending? → upgrade plan or tighten sampling
- New PII leakage detected? → tighten scrubber + post-mortem
