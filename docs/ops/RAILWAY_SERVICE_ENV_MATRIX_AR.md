# Dealix — Railway Service & Environment Matrix

هذا الملف هو المرجع التنفيذي لإعداد خدمات Railway ومتغيرات البيئة بدون تخمين.

## 1) Service Matrix

| Service | Root Directory | Dockerfile | Config | Healthcheck | Predeploy |
|---|---|---|---|---|---|
| `dealix-api` | `.` | `Dockerfile` | `railway.json` | `/healthz` | نعم، للـ API فقط |
| `dealix-frontend` | `frontend` | `Dockerfile` | `frontend/railway.json` | `/healthz` | لا |
| `dealix-apps-web` | `apps/web` | `Dockerfile` | `apps/web/railway.json` | `/healthz` | لا |

النسخة الآلية من هذا الجدول موجودة في `dealix/config/railway_services.json`، ويتم فحصها في CI عبر `scripts/verify_railway_surfaces.py`.

## 2) API Environment

### Required

| Variable | Example | Notes |
|---|---|---|
| `APP_ENV` | `production` | يفعّل production checks. |
| `APP_SECRET_KEY` | 64-byte hex | لا تستخدم placeholder. |
| `JWT_SECRET_KEY` | strong secret | لا يقل عن 32 حرفًا. |
| `API_KEYS` | comma-separated | مفاتيح API العامة للخدمة. |
| `ADMIN_API_KEYS` | comma-separated | مفاتيح Admin فقط. |

Generate secrets:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Recommended

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Postgres persistence. |
| `REDIS_URL` | queues/cache/rate/supporting infra. |
| `SENTRY_DSN` | error tracking. |
| `DEALIX_API_BASE` | production smoke and launch scripts. |
| `DEALIX_API_KEY` | smoke/automation key if required. |
| `DEALIX_ADMIN_API_KEY` | admin scripts; keep server-side only. |

### Optional provider keys

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | LLM provider. |
| `OPENAI_API_KEY` | LLM provider. |
| `GROQ_API_KEY` | LLM provider. |
| `GOOGLE_API_KEY` | Google/Gemini provider. |
| `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX` | search enrichment. |
| `GOOGLE_MAPS_API_KEY` | local Saudi discovery. |
| `TAVILY_API_KEY`, `SERPAPI_API_KEY`, `APIFY_TOKEN`, `FIRECRAWL_API_KEY` | enrichment fallbacks. |

## 3) Frontend Environment

| Variable | Example | Visibility |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_SITE_URL` | `https://dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | `1` | Public/browser-safe. |
| `DEALIX_OPS_PROXY_SECRET` | strong secret | Server-only if proxy is used. |

ممنوع وضع أي Admin/API private key داخل متغير يبدأ بـ `NEXT_PUBLIC_`.

## 4) Apps Web Environment

| Variable | Example | Visibility |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_SITE_URL` | `https://dealix.me` | Public/browser-safe. |

## 5) Verification Commands

```bash
python scripts/verify_railway_surfaces.py
python scripts/founder_launch_final_check.py
python scripts/founder_launch_final_check.py --live
```

Docker verification:

```bash
docker build -t dealix-api .
docker build -t dealix-frontend frontend
docker build -t dealix-apps-web apps/web
```

Live checks:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
curl -fsS https://dealix.me/healthz
```

## 6) Launch Gate

الإطلاق يعتبر جاهزًا عندما:

- كل Railway service deploy أخضر.
- healthcheck لكل خدمة أخضر.
- CI يمر أو يتم توثيق أي فشل خارجي.
- لا توجد أسرار في الريبو.
- لا توجد مفاتيح Admin داخل `NEXT_PUBLIC_*`.
- DNS/TLS يعملان على الدومينات النهائية.
