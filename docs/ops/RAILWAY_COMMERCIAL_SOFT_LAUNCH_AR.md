# Railway — إطلاق تجاري ناعم

## إعدادات

| الحقل | القيمة |
|--------|--------|
| Pre-deploy | `sh /app/scripts/railway_predeploy.sh` |
| Healthcheck | `/healthz` |

## تحقق

```powershell
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS https://api.dealix.me/api/v1/meta
$env:DEALIX_VERIFY_WITH_API="1"
powershell -File scripts/verify_dealix_commercial_go_live.ps1
```

Moyasar live لاحقاً: `MOYASAR_SECRET_KEY=sk_live_…` + `DEALIX_MOYASAR_MODE=live`.
