# Environment Variables (Dealix)

## Frontend (`apps/web`)
- `NEXT_PUBLIC_API_URL` — backend URL (default `http://localhost:8000`)
- `NEXT_PUBLIC_DEMO_MODE` — `true` for demo

## Backend (`api/`)
- `APP_ENV=production`
- `APP_SECRET_KEY` — long random
- `DATABASE_URL` — Postgres URL
- `ENVIRONMENT=production`
- `MOYASAR_LIVE_MODE=0` (sandbox) or `1` (live)
- `MOYASAR_PUBLISHABLE_KEY`
- `MOYASAR_SECRET_KEY`

## Optional connectors
- `GOOGLE_PLACES_API_KEY`
- `HUBSPOT_PRIVATE_APP_TOKEN`
- `WHATSAPP_BUSINESS_TOKEN`
- `EMAIL_PROVIDER_API_KEY`

## Admin
- `DEALIX_ADMIN_PASSWORD`
- `DEALIX_ADMIN_TOKEN`

## Do NOT commit
- Real keys
- Real passwords
- Real tokens
- Production DATABASE_URL with credentials
