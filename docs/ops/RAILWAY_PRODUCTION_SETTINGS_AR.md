# إعدادات إنتاج Railway — مرجع المؤسس (api.dealix.me)

**المستودع:** `VoXc2/dealix` · **الفرع:** `main` · **Config-as-code:** [`railway.toml`](../../railway.toml) · [`railway.json`](../../railway.json) · **قائمة نسخ:** [`dealix/config/railway_ui_canonical.yaml`](../../dealix/config/railway_ui_canonical.yaml)

**تحقق محلي (مع محاكاة خطأ UI):**

```bash
py -3 scripts/verify_railway_production_config.py \
  --ui-start-command "./start.sh" \
  --ui-predeploy 'echo "no migration needed"'
bash scripts/railway_ui_alignment.sh
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS https://api.dealix.me/api/v1/meta
```

---

## إعدادات واجهة Railway (يجب أن تطابق هذا الجدول)

| الإعداد | القيمة الصحيحة | خطأ شائع |
|---------|----------------|----------|
| **Builder** | Dockerfile | — |
| **Start Command** | **فارغ** أو `/app/start.sh` فقط | `./start.sh` أو `uvicorn ...` مباشرة |
| **Pre-deploy** | `sh /app/scripts/railway_predeploy.sh` (من [`railway.toml`](../../railway.toml)) | `echo "no migration needed"` |
| **Healthcheck Path** | `/healthz` | `/health` فقط |
| **Healthcheck Timeout** | `300` | — |
| **Public domain target port** | نفس `PORT` الذي تحقنه Railway (غالبًا **8080** على المنصة؛ التطبيق يقرأ `$PORT` عبر `/app/start.sh`) | منفذ ثابت 8000 في Start Command |
| **Restart policy** | ON_FAILURE · max 3 | — |
| **Wait for CI** | مفعّل (موصى به) | — |

---

## لماذا لا `./start.sh`؟

الصورة تضع السكربت في **`/app/start.sh`**. أمر `./start.sh` من مجلد عمل خاطئ يسبب فشل النشر أو خطأ المنفذ (`Invalid value for '--port': '${PORT:-8000}'`).

**الحل:** امسح Start Command في Railway UI → يستخدم Dockerfile `CMD ["/app/start.sh"]`.

---

## الترحيل (Alembic)

- **config-as-code:** [`railway.toml`](../../railway.toml) يشغّل `sh /app/scripts/railway_predeploy.sh` قبل كل نشر.
- **افتراضي (آمن):** السكربت يطبع `SKIP` ولا يشغّل ترحيلاً.
- **ترحيل تلقائي عند النشر:** عيّن `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1` + `DATABASE_URL` على خدمة API.
- **خطأ شائع في UI:** `echo "no migration needed"` — **استبدله** بـ `sh /app/scripts/railway_predeploy.sh` أو اترك الحقل فارغاً ليأخذ `railway.toml`.
- **مرة واحدة:** `bash scripts/railway_prod_bootstrap.sh`
- **بذرة أول مرة (اختياري):** `bash scripts/railway_prod_bootstrap.sh` بعد أول نشر ناجح.

تحقق محلي (ومحاكاة انحراف لوحة Railway):

```bash
bash scripts/railway_ui_alignment.sh --with-smoke
# Windows:
powershell -File scripts/railway_ui_alignment.ps1 -WithSmoke
python scripts/verify_railway_production_config.py --ui-start-command "./start.sh"
python scripts/verify_railway_production_config.py --ui-predeploy 'echo "no migration needed"'
```

مرجع آلي: [`dealix/config/railway_ui_canonical.yaml`](../../dealix/config/railway_ui_canonical.yaml)

---

## متغيرات بيئة API (حد أدنى)

| متغير | الغرض |
|--------|--------|
| `DATABASE_URL` | Postgres (مرجع `${{Postgres.DATABASE_URL}}`) |
| `APP_SECRET_KEY` | جلسات وتوقيع |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | دومينات الفرونت |
| `ADMIN_API_KEYS` | `/api/v1/ops-autopilot/*` |
| `DEALIX_ADMIN_API_KEY` | CI / سكربتات محلية |

تحقق:

```bash
python scripts/railway_launch_env_check.py
```

---

## فرونت إند (خدمة منفصلة إن وُجدت)

| متغير | مثال |
|--------|------|
| `NEXT_PUBLIC_API_URL` | `https://api.dealix.me` |
| `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` | نفس مفتاح `ADMIN_API_KEYS` |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | `1` في الإنتاج للوحة `/ops/founder` |

---

## بعد النشر

```bash
curl -fsS https://api.dealix.me/healthz
bash scripts/official_launch_verify.sh --api-base https://api.dealix.me
bash scripts/verify_dealix_commercial_go_live.sh
```

---

## مراجع

- [`DEPLOYMENT.md`](../../DEPLOYMENT.md) · [`docs/RAILWAY_DEPLOY_GUIDE_AR.md`](../RAILWAY_DEPLOY_GUIDE_AR.md)
- [`docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md`](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)
- [`docs/commercial/PAID_LAUNCH_INTEGRATIONS_RUNBOOK_AR.md`](../commercial/PAID_LAUNCH_INTEGRATIONS_RUNBOOK_AR.md)
