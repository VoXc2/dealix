# سياسة انجراف الإعدادات — Dealix Configuration Drift Policy

> **كل اختلاف بين `.env.example` و staging/production = drift.** هذا
> الـ doc يحدد ما هو مسموح، ما هو ممنوع، وكيف يُكشَف ويُعالَج.

**الحالة:** مسودة — Phase 1 من Agent #12
**التاريخ:** 2026-06-03

---

## 1. تعريف Drift

أي اختلاف بين:
- `.env.example` (master، في main)
- `.env.prod.example`
- `.env.staging.example`
- `.env.railway.example`
- staging environment variables (في Railway)
- production environment variables (في Railway)

## 2. التصنيف

| النوع | مثال | مسموح؟ |
| --- | --- | --- |
| **Variable added** to `.env.example` but not yet to staging | متغير جديد أُضيف | ✅ (grace week) |
| **Variable removed** from `.env.example` but still in staging | متغير قديم | ❌ ممنوع |
| **Value differs** between `.env.example` and `.env.prod.example` | `MOYASAR_LIVE_MODE` | ⚠️ يوثَّق + يعلَّق |
| **Tier mismatch** | `[REQUIRED]` في master، `[OPTIONAL]` في staging | ❌ ممنوع |
| **Production secret** appears in staging env | `sk_live_*` في staging | ❌ ممنوع |
| **Staging secret** appears in production env | test key في production | ❌ ممنوع |
| **Comment drift** | تعليق في staging لا يوجد في master | ⚠️ يدمج |

## 3. الكاشف (Drift Detection)

- **يومي:** `scripts/validate_railway_generated_env.py` +
  `scripts/sync_railway_generated_env.py` (في
  `.github/workflows/watchdog_drift.yml`).
- **يدوي:** `make env-check` عند أي تعديل على `.env.example`.
- **PR-time:** GitHub Action يقارن `.env.example` و `.env.prod.example`
  و `.env.staging.example`.

## 4. المعالجة (Drift Remediation)

1. **الاكتشاف:** الـ workflow يضع entry في
   `reports/infra/drift_log.md` مع timestamp.
2. **التنبيه:** Slack / email notification (مستقبلاً).
3. **الإصلاح:** PR تلقائي (لا merge تلقائي) يقترح الحل.
4. **المراجعة:** المؤسس يوافق.
5. **الإغلاق:** تحديث الـ drift_log بحلّ.

## 5. Grace Period

- إضافة متغير جديد: أسبوع واحد من `.env.example` إلى staging.
- تحديث قيمة: فوري (CI يفحص).
- حذف متغير: أسبوعان (grace + verify) قبل الحذف النهائي.

## 6. ما يُسجَّل في Drift Log

| الحقل | الوصف |
| --- | --- |
| `drift_id` | unique |
| `discovered_at` | timestamp |
| `source` | `.env.example` / `.env.prod.example` / Railway |
| `target` | staging / production |
| `variable` | اسم المتغير |
| `kind` | added/removed/value_diff/tier_mismatch/secret_leak |
| `severity` | info / warn / error |
| `remediation` | proposed fix |
| `remediation_status` | open / pr_open / merged / wontfix |
| `closed_at` | timestamp |

## 7. الـ Whitelist (Drift المسموح)

- اختلاف `ENVIRONMENT` بين staging و production (متوقع).
- اختلاف `MOYASAR_LIVE_MODE` (متوقع، staging=0).
- اختلاف `WHATSAPP_MOCK_MODE` (متوقع، staging=true).
- اختلاف `APP_URL` و `CORS_ORIGINS`.
- اختلاف `DATABASE_URL` (DBs مختلفة).

كل whitelist entry يوثَّق في `reports/infra/drift_whitelist.yaml`.

## 8. CI Failure

- أي drift في `[REQUIRED]` أو `[REVENUE]` ⇒ CI يفشل.
- أي drift في `[OPTIONAL]` ⇒ warning.
- أي production secret في staging ⇒ CI يفشل + alert.

## 9. المراجع

- `docs/infra/ENVIRONMENT_POLICY_AR.md`
- `docs/infra/STAGING_PRODUCTION_POLICY_AR.md`
- `docs/infra/ENV_CONTRACT_AR.md`
- `docs/infra/SECRETS_MANAGEMENT_AR.md`
- `scripts/check_env_contract.py`
- `scripts/validate_railway_generated_env.py`
- `scripts/sync_railway_generated_env.py`
- `.github/workflows/watchdog_drift.yml`
