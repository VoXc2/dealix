# إعدادات إنتاج Railway — مرجع المؤسس (api.dealix.me)

**المستودع:** `Dealix-sa/dealix` · **الفرع:** `main` · **Config-as-code:** [`railway.toml`](../../railway.toml) · [`railway.json`](../../railway.json) · **قائمة نسخ:** [`dealix/config/railway_ui_canonical.yaml`](../../dealix/config/railway_ui_canonical.yaml)

**تحقق محلي (مع محاكاة خطأ UI):**

```bash
py -3 scripts/verify_railway_production_config.py \
  --ui-start-command "./start.sh" \
  --ui-predeploy 'echo "no migration needed"' \
  --ui-restart-max-retries 10
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
| **Pre-deploy** | **فارغ / Disabled** | أي أمر تلقائي، بما فيه migration |
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

- **config-as-code:** [`railway.toml`](../../railway.toml) و[`railway.json`](../../railway.json) لا يعرّفان `preDeployCommand`؛ automatic pre-deploy معطّل.
- **افتراضي (آمن):** لا تعمل أي migration داخل deploy. يبقى `scripts/railway_predeploy.sh` أداة fail-closed منفصلة ولا تمنح صلاحية تنفيذ.
- **Automatic production migration:** disabled fail-closed. `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1` expresses migration intent only and blocks pre-deploy; DDL requires a separate one-shot executor plus an exact action-bound approval receipt binding environment, revision payload, expiry, idempotency key, and `ACTION_HASH`.
- **واجهة Railway:** اترك Pre-deploy فارغًا. أي migration إنتاجية تحتاج one-shot executor وصلاحية L5 مرتبطة بالفعل.
- **Legacy bootstrap:** `bash scripts/railway_prod_bootstrap.sh` is fail-closed (exit 75) and performs no migration, seed, or API mutation.
- **Material bootstrap/seed:** requires a separate one-shot executor with an exact action-bound approval receipt; no legacy script or persistent environment flag grants authority.
- **Prepare only:** `python scripts/ops/prepare_railway_migration_packet.py ...` يبني حزمة `PENDING_EXACT_L5_AUTHORITY` مرتبطة بـ release SHA + Railway project/environment/service + Alembic head + provider-scoped structured SUCCESS `--backup-receipt` matching Railway project/environment/service + existing repo rollback artifact + expiry + idempotency + `ACTION_HASH`. الباني لا يتصل بقاعدة البيانات ويُبقي `execution_allowed=false`.

تحقق محلي (ومحاكاة انحراف لوحة Railway):

```bash
bash scripts/railway_ui_alignment.sh --with-smoke
# Windows:
powershell -File scripts/railway_ui_alignment.ps1 -WithSmoke
python scripts/verify_railway_production_config.py --ui-start-command "./start.sh"
python scripts/verify_railway_production_config.py --ui-predeploy 'echo "no migration needed"'
python scripts/verify_railway_production_config.py --ui-restart-max-retries 10
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
