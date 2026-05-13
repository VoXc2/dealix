# Production `.env` — paste in this order

> Order matters. Paste each section, restart the API, run
> `bash scripts/ops/post_deploy_smoke.sh --base-url <prod>`,
> then move to the next section. This is the fastest way to find
> which key broke what.

The file lives at `/opt/dealix/.env` on the prod host (or as a K8s
Secret named `dealix-secrets`). NEVER commit the populated version.

## 1. CORE — app will not boot without these

```ini
APP_ENV=production
APP_URL=https://api.dealix.me
JWT_SECRET_KEY=          # python -c "import secrets; print(secrets.token_urlsafe(64))"
SECRET_KEY=              # same as JWT_SECRET_KEY
ADMIN_API_KEYS=          # python -c "import secrets; print(secrets.token_urlsafe(32))"  (comma-separated for multi)
POSTGRES_PASSWORD=       # python -c "import secrets; print(secrets.token_urlsafe(32))"
DATABASE_URL=postgres://dealix:${POSTGRES_PASSWORD}@pgbouncer:5432/dealix
REDIS_URL=redis://redis:6379/0
MEILI_MASTER_KEY=        # python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Smoke after this section:** `curl ${APP_URL}/healthz` → 200 / `{"status":"ok"}`.

## 2. REVENUE — paste FIRST among optional keys

These are the keys that earn money. Paste them in this exact order:

```ini
MOYASAR_SECRET_KEY=      # dashboard.moyasar.com → API Keys → "Secret key"  (SANDBOX FIRST)
# Leave DEALIX_MOYASAR_MODE blank for sandbox. After 5 successful
# sandbox payments + the smoke script green, flip to "live".
DEALIX_MOYASAR_MODE=
ANTHROPIC_API_KEY=       # console.anthropic.com → API keys
RESEND_API_KEY=          # resend.com/api-keys
```

**Smoke after this section:**
- `curl ${APP_URL}/api/v1/billing/health` → `moyasar_configured: true`.
- Take a test payment per `docs/ops/go_live_one_pager.md` SECTION A step 9.
- Confirm the bilingual receipt + signed invoice URL land in your inbox.

## 3. TRUST — paste BEFORE your first enterprise pilot

```ini
SENTRY_DSN=              # sentry.io → project → SDK Setup
POSTHOG_API_KEY=         # app.posthog.com → settings → "Project API Key"
BETTERSTACK_HEARTBEAT_URL=
WORKOS_API_KEY=          # workos.com → API → secret key  (enterprise SSO only)
WORKOS_CLIENT_ID=
KNOCK_API_KEY=
PLAIN_API_KEY=
```

**Smoke after this section:** `${APP_URL}/health/deep` shows
`vendors.{sentry,posthog,workos,knock,plain}` = `"ok"`.

## 4. LLM COST BINDING — paste at >10 paying customers

```ini
PORTKEY_API_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LAGO_API_KEY=
LLM_MAX_USD_PER_REQUEST=0.50
LLM_MAX_USD_PER_TENANT_DAY=20.0
```

## 5. SAUDI GOV — paste only when a customer needs it

```ini
WATHQ_API_KEY=           # wathq.sa  (1–4 wk issuance)
ETIMAD_API_KEY=
MAROOF_API_KEY=
NAJIZ_API_KEY=
TADAWUL_API_KEY=
MISA_API_KEY=
NAFATH_API_KEY=          # SDAIA-issued
YAKEEN_API_KEY=
```

## 6. INTL / GCC PAYMENTS — paste when expanding outside KSA

```ini
STRIPE_API_KEY=          # USD / EUR / AED international
STRIPE_WEBHOOK_SECRET=
KNET_TRANPORTAL_ID=      # Kuwait
KNET_RESOURCE_KEY=
BENEFIT_API_KEY=         # Bahrain
BENEFIT_MERCHANT_ID=
BENEFIT_WEBHOOK_SECRET=
MAGNATI_API_KEY=         # UAE
MAGNATI_MERCHANT_ID=
MAGNATI_WEBHOOK_SECRET=
TABBY_API_KEY=
TAMARA_API_KEY=
TAP_API_KEY=
```

## 7. ADVANCED AI — defer until trust + cost are stable

```ini
OPENAI_API_KEY=
VOYAGE_API_KEY=
COHERE_API_KEY=
LAKERA_API_KEY=
LETTA_URL=
```

## 8. CONTAINER TAGS — bump on each release

```ini
API_TAG=v3.8.1
WEB_TAG=v3.8.1
PUBLIC_API_BASE=https://api.dealix.me
```

## Rollback per key

If the smoke fails after pasting a key:

1. Comment out the offending line in `/opt/dealix/.env`.
2. Restart only the API:
   `docker compose -f deploy/docker-compose.prod.yml restart api`.
3. Re-run `bash scripts/ops/post_deploy_smoke.sh --base-url <prod>`.

Every key in this file is inert-by-default — removing it never breaks
the rest of the platform, the feature just goes back to its graceful-
degrade path.

## Founder rule

**Don't pay for a vendor before a paying customer needs it.** See
`docs/ops/vendor_cost_sheet.md` for the price-per-vendor breakdown.
Week-1 minimum spend to launch: **< $100/month**.
