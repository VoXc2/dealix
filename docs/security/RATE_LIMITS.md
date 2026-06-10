# Rate Limits — Policy & Configuration

> Source of truth for production rate-limit configuration. Implementation lives in `api/security/rate_limit.py`.

## Goals
1. Protect API + DB from abuse (no single tenant can starve others).
2. Provide isolation between authenticated tenants (per-key bucket).
3. Protect public endpoints (demo, checkout) from scrapers and credential stuffers.
4. Keep webhooks responsive but bounded (no DoS via spoofed Moyasar/Calendly).

## Bucket strategy
- **Authenticated** request → bucket by **first 16 chars of `X-API-Key`** (tenant isolation, no full key in logs).
- **Unauthenticated** request → bucket by **client IP** (`X-Forwarded-For` first hop, validated against Railway proxies).
- **Admin** request → bucket by **first 16 chars of `X-Admin-API-Key`** (separate, stricter limit).
- **Webhook signature-validated** request → bucket by **source** (`moyasar`, `calendly`, etc.) with high ceiling.

Window: moving 1-minute window (smooths bursts).
Storage: `RL_STORAGE_URI=redis://...` in production (set on Railway). In-memory only for dev.

## Production limits (current — review quarterly)

| Bucket | Limit | Env var | Rationale |
|--------|-------|---------|-----------|
| **Global per tenant** | 1000 / min | `RL_GLOBAL=1000/minute` | Sane ceiling; legit usage rarely exceeds 100/min |
| **Admin endpoints** | 120 / min | `RL_ADMIN=120/minute` | Tighter — admin tools are interactive, not automated |
| **POST /api/v1/leads** | 10 / min | route decorator | Anti-scrape; lead import has bulk endpoint for legit bulk |
| **POST /api/v1/sales/*** | 30 / min | route decorator | Normal sales activity ceiling |
| **POST /api/v1/public/demo-request** | 5 / min per IP | route decorator | Anti-spam |
| **POST /api/v1/checkout** | 10 / min per IP | route decorator | Anti card-testing |
| **POST /api/v1/auth/*** | 5 / min per IP | route decorator | Anti credential stuffing |
| **POST /api/v1/webhooks/whatsapp** | 100 / min per source | route decorator | Meta can burst 60+/s briefly |
| **POST /api/v1/webhooks/moyasar** | 200 / min per source | route decorator | Moyasar ping retries can burst |
| **GET /healthz** | unlimited | bypass | Required by UptimeRobot + Railway probes |
| **GET /api/v1/pricing/plans** | 300 / min | route decorator | Heavily cached; high ceiling acceptable |

## Headers (RFC 6585)
Responses include:
- `X-RateLimit-Limit` — bucket ceiling
- `X-RateLimit-Remaining` — current allowance
- `X-RateLimit-Reset` — UTC epoch when window resets
- `Retry-After` — seconds (on 429)

Middleware: `RateLimitHeadersMiddleware` in `api/main.py:138`.

## On 429
Response body:
```json
{"error":"RateLimitExceeded","detail":"too many requests","retry_after_sec":42}
```

## Per-customer overrides
Some enterprise customers need higher limits. Override mechanism:
- Set `tenant_rate_overrides` JSON in Redis: `rl:overrides:<first-16-of-key> = {"global":"5000/minute"}`
- Loaded at process start; cached 5 minutes; reload via `POST /api/v1/admin/rate-limits/reload`
- Document overrides in `docs/security/rate_limit_overrides.md` (not in this file — overrides change frequently)

## Alerting
- PostHog event `rate_limit_hit` on every 429
- Sentry alert: > 50 rate_limit_hits/min from a single bucket → SEV-3 (possible abuse, investigate)

## Bypass list (DO NOT EXTEND without security review)
Only `/healthz`, `/livez`, `/readyz` (Kubernetes/Railway probes). All other endpoints are limited.

## Annual review
Q4 each year, review:
- Are limits too tight (causing legit 429s)? Check PostHog `rate_limit_hit` by route.
- Are limits too loose (abuse slipping through)? Check Sentry abuse incidents.
- Adjust env vars or route decorators; re-deploy.

## Test
```bash
# Burst test (should see 429 after threshold)
for i in {1..20}; do
  curl -X POST https://api.dealix.me/api/v1/public/demo-request \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.sa","name":"x","company":"x","phone":"+966500000000","consent":true}' \
    -o /dev/null -w "%{http_code}\n"
done
# Expected: first 5 → 200, next 15 → 429
```
