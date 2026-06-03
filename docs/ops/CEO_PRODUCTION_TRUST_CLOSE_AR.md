# CEO Production Trust Close — P0 Runbook

**الغرض:** إغلاق Layer 0–4 قبل Phase 1 revenue marketing.  
**Verify:** `python scripts/ceo_production_trust_bundle.py`

---

## Checklist

### 1) DNS Frontend

- [ ] Railway Frontend service · root `frontend/`  
- [ ] CNAME `dealix.me` → Railway (remove GitHub Pages)  
- [ ] `/ar` returns 200 on Next.js

**Doc:** [DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md](DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md)

### 2) API Trust Endpoints

- [ ] `GET /version` → 200 + version + git_sha  
- [ ] `GET /api/v1/meta` → 200 + surfaces  
- [ ] `GET /healthz` → includes `version` field

**If 404:** `python scripts/railway_redeploy_checklist.py`

### 3) Observability

- [ ] `SENTRY_DSN` set on Railway API service  
- [ ] PostHog key configured (Layer 3)

**Template:** `.env.example` → `SENTRY_DSN=`

### 4) Verify bundle

```powershell
python scripts/ceo_production_trust_bundle.py --write-cache
python scripts/production_layers_verify.py --write-cache
```

**Target:** `overall_pct >= 80` · `CEO_PRODUCTION_TRUST_VERDICT=PASS`

---

## Founder-only (cannot automate)

- DNS registrar access  
- Railway deploy trigger  
- Sentry project creation
