# DNS dealix.me → Railway Frontend (Next.js)

**المشكلة:** `dealix.me/ar` يعيد 404 و `Server: GitHub.com` — الموقع على GitHub Pages وليس Railway.

**الهدف:** `https://dealix.me/ar` → 200 على Next.js (Railway Frontend).

**تحقق:**

```powershell
curl -I https://dealix.me/ar
py -3 scripts/post_redeploy_verify_dealix.py
```

---

## 1) مزامنة env الفرونت

```powershell
py -3 scripts/sync_railway_generated_env.py
py -3 scripts/validate_railway_generated_env.py --from-railway-env
```

**ملف:** `.env.railway.frontend.generated` — الحد الأدنى:

- `NEXT_PUBLIC_API_URL=https://api.dealix.me`
- `NEXT_PUBLIC_SITE_URL=https://dealix.me`
- `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1`
- `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` = نفس `ADMIN_API_KEYS` على API
- `DEALIX_ADMIN_API_KEY` = نفس القيمة (لـ ops proxy)

---

## 2) Railway Frontend service

| الإعداد | القيمة |
|---------|--------|
| **Root directory** | `frontend` |
| **Builder** | Dockerfile (في `frontend/Dockerfile` إن وُجد) أو Nixpacks |
| **Variables** | Raw Editor ← `.env.railway.frontend.generated` |
| **Custom domains** | `dealix.me` · `www.dealix.me` |

**Deploy:** Deploy latest commit على `main`.

---

## 3) DNS عند الم registrar

1. **أزل** سجلات GitHub Pages:
   - A records → `185.199.108.153` / `185.199.109.153` / …
   - CNAME `@` → `VoXc2.github.io` أو مشابه
2. **أضف** ما يعرضه Railway في Custom Domains:
   - عادة CNAME `@` أو `www` → `<project>.up.railway.app`
3. انتظر propagation (5–30 دقيقة)

---

## 4) تحقق نجاح Layer 4

```powershell
# يجب 200 وليس GitHub.com
Invoke-WebRequest -Uri https://dealix.me/ar -Method Head -UseBasicParsing
py -3 scripts/production_layers_verify.py --from-railway-env --strict --write-cache
```

**PASS:** Layer 4 Frontend ≥ 80% · `Server` ≠ `GitHub.com`

---

## مراجع

- [RAILWAY_ONE_SHOT_DEPLOY_AR.md](RAILWAY_ONE_SHOT_DEPLOY_AR.md)
- [PRODUCTION_LAYERS_GO_LIVE_AR.md](PRODUCTION_LAYERS_GO_LIVE_AR.md)

---

*آخر تحديث: 2026-05-24*
