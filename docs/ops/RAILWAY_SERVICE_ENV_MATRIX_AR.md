# Dealix — Railway Service & Environment Matrix

هذا الملف هو المرجع التنفيذي لإعداد خدمات Railway ومتغيرات البيئة بدون تخمين. المرجع الآلي الأعلى هو `dealix/config/railway_services.json`، وتُرفض أي خدمة لا تطابق role/authority الكنسي عبر `scripts/verify_railway_surfaces.py`.

## 1) Service Matrix

| Service | Role | Production Authority | Root Directory | Dockerfile | Repository Config | Provider Config File | Healthcheck |
|---|---|---:|---|---|---|---|---|
| `dealix-api` | `canonical_api` | `true` | `.` | `Dockerfile` | `railway.json` | provider evidence required | `/healthz` |
| `dealix-apps-web` | `canonical_public_web` | `true` | `apps/web` | `Dockerfile` | `apps/web/railway.toml` | `/apps/web/railway.toml` | `/healthz` |
| `dealix-frontend` | `legacy_public_web` | `false` | `frontend` | `Dockerfile` | `frontend/railway.json` | legacy only | `/healthz` |
| `founder-os-worker` | `background_worker` | `false` | `.` | `Dockerfile.worker` | — | — | private |
| `dealix-watchdog` | `background_watchdog` | `false` | `.` | `Dockerfile.watchdog` | — | — | private |

**قاعدة cutover:** `dealix.me`/`www` لا يُربطان إلا بالخدمة التي تثبت `name=dealix-apps-web`, `role=canonical_public_web`, `productionAuthority=true`, `repo=Dealix-sa/dealix`, `root=apps/web`, `providerConfigFile=/apps/web/railway.toml` وعلى exact deployment SHA المقبول. اسم Railway مثل `web` لا يثبت الهوية.

`dealix-frontend` موجود كـLegacy/compatibility فقط؛ لا تستخدمه كهدف production domain ولا تعتبر نجاح build له دليلًا على جاهزية الواجهة الكنسية.

### Provider Config separation — mandatory

الخدمة الكنسية `dealix-apps-web` لا تشغّل API/DB pre-deploy migration. ملفها المخصص هو `apps/web/railway.toml`، ومساره الفعلي لدى Railway يجب أن يكون `/apps/web/railway.toml`.

ملف repo-root `/railway.toml` يخص عقد backend/API وقد يحتوي `preDeployCommand`. إذا أبلغ provider receipt أن web يعمل على `/railway.toml` فالحالة **HOLD** حتى لو نجح build أو كان HTTP reachable. لا تُزل backend pre-deploy من الملف الجذري كحل للويب؛ أصلح Config File للخدمة المرشحة فقط بعد exact-head acceptance وإجراء إنتاجي محدد.

## 2) API Environment

### Required

| Variable | Example | Notes |
|---|---|---|
| `APP_ENV` | `production` | يفعّل production checks. |
| `APP_SECRET_KEY` | 64-byte hex | لا تستخدم placeholder. |
| `JWT_SECRET_KEY` | strong secret | لا يقل عن 32 حرفًا. |
| `API_KEYS` | comma-separated | مفاتيح API العامة للخدمة. |
| `ADMIN_API_KEYS` | comma-separated | مفاتيح Admin فقط. |

Generate secrets locally/server-side only:

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
| `TAVILY_API_KEY`, `SERPAPI_API_KEY`, `APIFY_TOKEN`, `FIRECRAWL_API_KEY` | bounded enrichment fallbacks only when approved by capability intake. |

## 3) Canonical Apps Web Environment

لـ`dealix-apps-web` فقط:

| Variable | Example | Visibility |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_SITE_URL` | `https://dealix.me` | Public/browser-safe. |

`apps/web` لا يحتاج `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` كشرط cutover ولا يحتاج Admin/API private key في browser config. `apps/web/next.config.js` يوجه `/api/v1/*` إلى الـAPI الكنسي بدون تضمين مفتاح إداري.

ممنوع وضع أي Admin/API private key داخل متغير يبدأ بـ `NEXT_PUBLIC_`.

## 4) Legacy Frontend Environment — compatibility only

إذا احتجت تشغيل `frontend/` التاريخي في اختبار معزول فقط:

| Variable | Example | Visibility |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_SITE_URL` | `https://dealix.me` | Public/browser-safe. |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | `1` | Public toggle، ليس credential. |
| `DEALIX_OPS_PROXY_SECRET` | strong secret | Server-only if that legacy proxy is actually used. |

وجود هذه المتغيرات لا يمنح `frontend/` سلطة production.

## 5) Verification Commands

Canonical source acceptance:

```bash
python scripts/verify_railway_surfaces.py
python -m py_compile \
  scripts/verify_railway_surfaces.py \
  scripts/railway_frontend_dns_gate.py \
  scripts/railway_production_identity_gate.py
pytest -q \
  tests/test_railway_web_config_contract.py \
  tests/test_railway_frontend_dns_gate_truth.py \
  tests/test_railway_production_identity_gate_truth.py \
  tests/test_production_ops_gates.py
cd apps/web && npm ci && npm run typecheck && npm run build
cd ../..
```

API verification عند الحاجة:

```bash
docker build -t dealix-api .
```

لا تجعل build `frontend/` legacy شرطًا لإعلان `dealix-apps-web` جاهزًا.

Live checks — بعد وجود provider-bound accepted release فقط:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
curl -fsS https://dealix.me/healthz
```

HTTP وحده لا يثبت service identity. يجب أن يقترن بـfresh Railway provider receipts تربط project/environment/service/repo/root/config/deployment SHA/domain/TLS بالعقد الكنسي.

## 6) Launch Gate

الإطلاق يعتبر جاهزًا فقط عندما:

- `dealix-api` deployment الكنسي أخضر وعلى SHA مثبت.
- `dealix-apps-web` deployment الكنسي أخضر على **نفس accepted release SHA**.
- provider receipt للويب يثبت `/apps/web/railway.toml` وليس `/railway.toml`.
- healthcheck لكل خدمة كنسية أخضر.
- `dealix.me`/`www` يثبت أنهما يخدمان `dealix-apps-web` لا GitHub Pages/Legacy.
- CI يمر أو يتم توثيق أي فشل execution-plane خارجي بدون اعتباره code PASS.
- لا توجد أسرار في الريبو أو browser bundle.
- لا توجد مفاتيح Admin داخل `NEXT_PUBLIC_*`.
- DNS/TLS يعملان على الدومينات النهائية مع rollback before-state محفوظ.
- أي معلومة غير مثبتة تبقى `UNKNOWN_NOT_EVIDENCE_BACKED` وتمنع cutover.
