# Dealix Production Secrets Checklist

Use this checklist when connecting Dealix to the live domain, rotating keys, or moving between staging and production.

## Required repository / GitHub Actions secrets

| Secret | Required | Scope | Notes |
|---|---:|---|---|
| `DEALIX_PUBLIC_URL` | Yes | GitHub Actions | Public website URL, for example `https://dealix.me`. |
| `DEALIX_PRODUCTION_BASE_URL` | Yes | GitHub Actions | API base URL, for example `https://api.dealix.me`. |
| `DEALIX_API_KEY` | If protected smoke routes are used | GitHub Actions | Non-admin key only. |
| `DEALIX_ADMIN_API_KEY` | If admin automation is used | GitHub Actions / hosting | Server-side only. Never expose to browser JavaScript. |

## Required hosting variables

| Variable | Required | Service | Notes |
|---|---:|---|---|
| `ENVIRONMENT` | Yes | API | Set to `production`. |
| `LOG_LEVEL` | Yes | API | Usually `INFO`. |
| `APP_SECRET_KEY` | Yes | API | 64-byte hex recommended. |
| `DATABASE_URL` | Yes | API | Production database only. |
| `APP_URL` | Yes | API | Canonical app or public URL. |
| `CORS_ORIGINS` | Yes | API | Only production/staging origins. |
| `API_KEYS` | Recommended | API | Non-admin API keys. |
| `ADMIN_API_KEYS` | Yes | API | Admin-only keys. |
| `NEXT_PUBLIC_API_URL` | Yes | Web | Public API base URL. |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | Recommended | Web | Use `1` when privileged ops are proxied server-side. |

## Payment and webhook secrets

| Variable | Required when | Notes |
|---|---|---|
| `MOYASAR_SECRET_KEY` | Checkout/payment enabled | Production key only in production. |
| `MOYASAR_WEBHOOK_SECRET` | Moyasar webhook enabled | Rotate if webhook URL changes or leak suspected. |
| `CALENDLY_WEBHOOK_SECRET` | Calendly webhook enabled | Must match Calendly app setting. |
| `WHATSAPP_APP_SECRET` | WhatsApp webhook enabled | Required for signature verification. |
| `WHATSAPP_ACCESS_TOKEN` | WhatsApp outbound enabled | Server-side only. |

## AI and provider keys

At least one LLM provider should be configured for production workflows that require AI:

- `GROQ_API_KEY`
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `DEEPSEEK_API_KEY`
- `GLM_API_KEY`

Provider keys are optional only for flows that degrade gracefully without live AI.

## Validation commands

Run locally or in CI:

```bash
make env-check
make security-smoke
make prod-verify
```

For live deploys:

```bash
python scripts/dealix_smoke_test.py --base-url https://api.dealix.me
```

## Rotation rule

Rotate immediately if:

- A key appears in logs, commits, screenshots, support tickets, or browser code.
- A webhook secret was shared outside the deployment platform.
- Admin keys were used by frontend code.
- An employee, contractor, or automation token no longer needs access.

## Arabic summary

أي سر إنتاجي لازم يكون في منصة الاستضافة أو GitHub Secrets فقط. لا تضع admin key في المتصفح. بعد أي تغيير أسرار شغّل `make env-check` و smoke test على `api.dealix.me`.
