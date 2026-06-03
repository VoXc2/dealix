# Dealix Frontend Production Runbook

This runbook covers the Next.js frontend in `apps/web` when connected to the live Dealix domain.

## Canonical URLs

| Variable | Default | Purpose |
|---|---|---|
| `NEXT_PUBLIC_SITE_URL` | `https://dealix.me` | Metadata, sitemap, robots, canonical URLs. |
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` | Browser-safe API base URL. |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | `1` | Prefer server-side proxy for privileged operations. |

## Required before deploy

```bash
cd apps/web
npm ci
npm run verify
```

`npm ci` requires `apps/web/package-lock.json`. This is intentional: production builds must be reproducible.

## Domain checks

After deployment:

- [ ] `https://dealix.me` loads successfully.
- [ ] `https://dealix.me/status` loads successfully.
- [ ] `https://dealix.me/robots.txt` exists.
- [ ] `https://dealix.me/sitemap.xml` exists.
- [ ] Metadata title and description render correctly.
- [ ] Browser console has no production-blocking errors.
- [ ] Links to operational surfaces resolve correctly.

## Security headers

The frontend config sets security headers in `apps/web/next.config.mjs`:

- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Permissions-Policy`

Review CSP after adding analytics, payments, chat, or embedded media. Do not add broad wildcards unless required and risk-reviewed.

## SEO assets

The app includes:

- `app/layout.tsx` metadata.
- `app/robots.ts`.
- `app/sitemap.ts`.
- `app/manifest.ts`.
- JSON-LD structured data on the homepage.

## Rollback

If frontend deployment fails:

1. Roll back to the previous successful frontend deployment.
2. Confirm `https://dealix.me` and `/status` load.
3. Confirm `NEXT_PUBLIC_API_URL` still points to the correct API.
4. Record the incident in `docs/ops/EXECUTION_BACKLOG.md`.

## Arabic summary

واجهة Dealix لازم تُبنى بـ `npm ci` مع lockfile، وتستخدم `NEXT_PUBLIC_SITE_URL` و`NEXT_PUBLIC_API_URL` الصحيحين، وتتحقق من `/status` و`robots.txt` و`sitemap.xml` بعد كل نشر.
