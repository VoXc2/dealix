# Vercel Frontend Deployment

## 1. Connect repo
- Link GitHub repo to Vercel
- Framework preset: Next.js
- Root directory: `apps/web` (if monorepo)

## 2. Env vars
- `NEXT_PUBLIC_API_URL` — backend URL
- `NEXT_PUBLIC_DEMO_MODE` — `true` for demo

## 3. Build command
- `cd apps/web && npm install && npm run build`

## 4. Output
- `.next/` (default)

## 5. Smoke test
- After deploy, run:
  `python3 scripts/post_deploy_smoke.py --base-url https://<vercel-domain>`

## 6. Rollback
- Vercel → Deployments → Promote previous
