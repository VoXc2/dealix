# V6 Admin Access Model (Dealix)

## Internal routes (V1 protect)
- `/crm`
- `/command-center`
- `/war-room`
- `/pipeline`
- `/review-queue`
- `/proof-vault`
- `/operator`
- `/launch`
- `/kpi-finance`
- `/data-room`
- `/client-portal`
- `/deals`
- `/outreach-lab`

## Env vars
- `DEALIX_ADMIN_TOKEN` (random 32+ chars)
- `DEALIX_ADMIN_PASSWORD` (set by operator)
- `NEXT_PUBLIC_DEMO_MODE=true|false`

## Demo mode
- All internal pages show a clear "demo mode" banner
- No real auth check
- Public marketing pages still public

## Production mode
- Internal pages require `Authorization: Bearer <DEALIX_ADMIN_TOKEN>`
- OR session cookie set via `/login`
- Public marketing pages remain public

## Limitation
- This is a pragmatic gate, not a full identity provider
- For 50+ employee enterprise, integrate SSO (out of V6 scope)

## Migration to SSO
- Replace middleware with NextAuth.js or Clerk
- Keep internal route list
- Add role checks
