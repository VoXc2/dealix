# نشر Railway API — جلسة واحدة (~15 دقيقة)

**الغرض:** نشر أحدث `main` على `api.dealix.me` حتى `/version` و `/api/v1/meta` يعملان.

**تحقق:** `py -3 scripts/railway_redeploy_checklist.py`

---

## المتطلبات

1. `main` محدّث على GitHub (`powershell -File scripts/push_main_with_gh.ps1`)
2. `.env.railway.generated` مكتمل (`py -3 scripts/validate_railway_generated_env.py --from-railway-env`)
3. `RAILWAY_TOKEN` في GitHub Secrets (للـ CI) أو وصول Railway UI

---

## خطوات Railway UI (خدمة API)

| # | الإعداد | القيمة |
|---|---------|--------|
| 1 | **Source** | branch `main` · repo `VoXc2/dealix` |
| 2 | **Start Command** | **فارغ** (Dockerfile `CMD /app/start.sh`) |
| 3 | **Pre-deploy** | `sh /app/scripts/railway_predeploy.sh` |
| 4 | **Variables** | Raw Editor ← الصق `.env.railway.generated` → Save |
| 5 | **Deploy** | Deployments → **Deploy latest commit** (ليس Redeploy لنشر قديم) |
| 6 | **Wait** | healthcheck `/healthz` = 200 |
| 7 | **Verify** | `curl https://api.dealix.me/version` · `/api/v1/meta` |

---

## أتمتة (بعد push)

```powershell
# إذا RAILWAY_TOKEN مضبوط في GitHub:
gh workflow run "Deploy to Railway" --ref main
gh run list --workflow=railway_deploy.yml --limit 1
powershell -File scripts/poll_production_trust_layer.ps1
```

أو:

```powershell
powershell -File scripts/autonomous_production_close.ps1
```

---

## مراجع

- [RAILWAY_PRODUCTION_SETTINGS_AR.md](RAILWAY_PRODUCTION_SETTINGS_AR.md)
- [CEO_PRODUCTION_TRUST_CLOSE_AR.md](CEO_PRODUCTION_TRUST_CLOSE_AR.md)
- `scripts/railway_ui_alignment.ps1`

---

*آخر تحديث: 2026-05-24*
