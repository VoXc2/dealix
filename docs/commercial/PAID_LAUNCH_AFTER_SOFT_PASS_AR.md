# مسار الإطلاق المدفوع — بعد نجاح Soft Launch

**المتطلب:** `DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS` من `verify_dealix_commercial_go_live` (Soft + Founder OS).

لا تنتقل لهذا المسار قبل 3–5 اجتماعات تشخيص حقيقية وملء KPI من CRM.

## 1) تحققات إضافية

```bash
py -3 scripts/verify_commercial_launch_ready.py --strict
py -3 scripts/verify_paid_launch_readiness.py
```

مع بناء Frontend (بطيء):

```bash
py -3 scripts/verify_commercial_launch_ready.py --with-frontend-build
```

## 2) Railway / إنتاج

| خطوة | أمر |
|------|-----|
| Bootstrap DB + War Room seed | `bash scripts/railway_prod_bootstrap.sh` |
| فحص env | `python3 scripts/railway_launch_env_check.py` |
| إطلاق رسمي | `bash scripts/official_launch_verify.sh` → `OFFICIAL_LAUNCH_VERDICT=PASS` |
| تنفيذ كامل A–D | `bash scripts/launch_execution_railway.sh` |

وثيقة المرحلة: [PHASE_C_PRODUCTION_LAUNCH_AR.md](../ops/PHASE_C_PRODUCTION_LAUNCH_AR.md)

## 3) متغيرات إنتاج إلزامية

- `MOYASAR_SECRET_KEY` · `MOYASAR_WEBHOOK_SECRET`  
- `DATABASE_URL` · `APP_SECRET_KEY` · `ENVIRONMENT=production`  
- `ADMIN_API_KEYS` = `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` (أو `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1`)  
- `CORS_ORIGINS` يشمل نطاق الواجهة  

## 4) GitHub Actions (تشغيل سحابي يومي)

Secrets في المستودع:

| Secret | الغرض |
|--------|--------|
| `DEALIX_API_BASE` | API للوحة |
| `DEALIX_ADMIN_API_KEY` | `X-Admin-API-Key` |
| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة الأحداث |

Workflows: `founder_commercial_daily.yml` · `daily-revenue-machine.yml`

## 5) تتبع مدفوع

- [PAID_LAUNCH_TRACKER_AR.md](PAID_LAUNCH_TRACKER_AR.md)  
- [../LAUNCH_GATES.md](../LAUNCH_GATES.md)  
- أول Diagnostic مدفوع: [operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)
