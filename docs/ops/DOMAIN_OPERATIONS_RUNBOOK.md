# Dealix Domain Operations Runbook

This runbook covers the production domains and the operational checks required when Dealix is connected to its live domain.

## Canonical domains

| Surface | Default URL | Purpose |
|---|---|---|
| Public website | `https://dealix.me` | Landing, pricing, service catalog, conversion pages |
| API | `https://api.dealix.me` | FastAPI backend, health checks, public API routes |

If these change, update:

- `.env.example`
- deployment platform variables
- GitHub Actions secrets
- public frontend config
- documentation links

## Required GitHub secrets

| Secret | Purpose |
|---|---|
| `DEALIX_PUBLIC_URL` | Public website URL, usually `https://dealix.me` |
| `DEALIX_PRODUCTION_BASE_URL` | API base URL, usually `https://api.dealix.me` |
| `DEALIX_API_KEY` | Non-admin API key for smoke workflows when needed |
| `DEALIX_ADMIN_API_KEY` | Server-side admin key only, never browser-exposed |

## DNS checklist

- [ ] Apex domain points to the production frontend host.
- [ ] `www` redirects to apex or the chosen canonical host.
- [ ] `api` points to the production API service.
- [ ] No stale A/CNAME records point to old hosts.
- [ ] DNS TTL is appropriate for launch and rollback.
- [ ] SPF/DKIM/DMARC are configured if Dealix sends email from the domain.

## TLS checklist

- [ ] `https://dealix.me` has a valid certificate.
- [ ] `https://api.dealix.me` has a valid certificate.
- [ ] Certificates auto-renew.
- [ ] HTTP redirects to HTTPS.
- [ ] HSTS is enabled only after confirming all subdomains are HTTPS-ready.

## Runtime checks

Run after every deploy:

```bash
BASE_URL=https://api.dealix.me make v5-smoke
python scripts/dealix_smoke_test.py --base-url https://api.dealix.me
```

Expected minimum:

- `/health` returns 200.
- Public pricing and demo routes respond.
- Founder dashboard and governance endpoints do not expose live-send approval accidentally.
- Webhook routes are reachable but protected by signature verification.

## Rollback

If domain checks fail after a deployment:

1. Confirm whether the failure is DNS, TLS, frontend, API, or database.
2. Roll back the application image or hosting deployment.
3. Do not change DNS unless the hosting target is wrong.
4. Re-run production smoke.
5. Record the incident and follow-up in `docs/ops/EXECUTION_BACKLOG.md`.

## Monitoring

Minimum monitoring:

- Scheduled GitHub `Production Smoke` workflow.
- Hosting platform uptime checks.
- Error capture for backend and frontend.
- Alert on `/health` failure.
- Alert when TLS expiry is under 14 days.

## Arabic summary

الدومين الحي يحتاج تشغيل واضح: DNS صحيح، TLS صالح، smoke test بعد كل نشر، أسرار GitHub مضبوطة، وخطة rollback. لا تغيّر DNS وقت الحوادث إلا إذا كان الهدف نفسه خطأ؛ غالبًا rollback للتطبيق أسرع وأقل مخاطرة.
