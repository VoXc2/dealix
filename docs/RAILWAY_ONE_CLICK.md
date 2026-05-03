# Railway One-Click Deploy (15 دقيقة)

دليل من 8 خطوات للنشر على Railway. كل خطوة لها أمر/زر واضح.

---

## التحضير (5 دقائق — مرة واحدة)

1. **سجّل على Railway:** [railway.app](https://railway.app) → Sign in with GitHub
2. **أضف بطاقة دفع:** Railway مجاني $5/شهر، بعدها يطلب بطاقة (قد تحتاج USD card).
3. **تحقق أن الفرع على GitHub:**
   ```
   https://github.com/voxc2/dealix/tree/claude/launch-command-center-6P4N0
   ```
   آخر commit يجب أن يكون `d9b1666` أو أحدث.

---

## الخطوة 1 — إنشاء Project (دقيقتان)

1. Railway dashboard → **New Project**
2. اختر **Deploy from GitHub repo**
3. ابحث عن `voxc2/dealix` → **Deploy Now**
4. عند سؤال **Branch**: اختر `claude/launch-command-center-6P4N0`
5. Railway سيقرأ الـ `Dockerfile` و `railway.json` تلقائياً

---

## الخطوة 2 — أضف PostgreSQL + Redis (دقيقتان)

في الـ project canvas:
- اضغط **+ Add Service** → **Database** → **Add PostgreSQL**
- اضغط **+ Add Service** → **Database** → **Add Redis**

Railway سيُنشئ المتغيرات تلقائياً:
- `DATABASE_URL` (للـ Postgres)
- `REDIS_URL` (للـ Redis)

---

## الخطوة 3 — أضف Environment Variables (5 دقائق)

في الـ Dealix service → **Variables tab** → اضغط **Raw Editor**:

```bash
APP_ENV=staging
APP_DEBUG=false
APP_SECRET_KEY=GENERATE_NEW_HEX_HERE_64_CHARS
APP_URL=https://YOUR-PROJECT.up.railway.app

# Live-action gates (8) — كلها FALSE (PDPL + Meta + LinkedIn ToS)
WHATSAPP_ALLOW_LIVE_SEND=false
GMAIL_ALLOW_LIVE_SEND=false
MOYASAR_ALLOW_LIVE_CHARGE=false
LINKEDIN_ALLOW_AUTO_DM=false
RESEND_ALLOW_LIVE_SEND=false
WHATSAPP_ALLOW_INTERNAL_SEND=false
WHATSAPP_ALLOW_CUSTOMER_SEND=false
CALLS_ALLOW_LIVE_DIAL=false

# LLM keys (احصل عليها من كل provider)
ANTHROPIC_API_KEY=sk-ant-REPLACE
DEEPSEEK_API_KEY=sk-REPLACE
GROQ_API_KEY=gsk_REPLACE
GLM_API_KEY=REPLACE
GOOGLE_API_KEY=REPLACE

# CORS
CORS_ORIGINS=https://YOUR-PROJECT.up.railway.app,https://app.dealix.me
```

**توليد APP_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## الخطوة 4 — Deploy (3 دقائق)

Railway سيبني تلقائياً عند إضافة المتغيرات. لمراقبة البناء:
- اضغط على Dealix service → **Deployments tab**
- آخر deployment يجب أن يصير **Active** خلال 3-5 دقائق

عند الـ "Active":
- اضغط **Settings tab** → **Domains** → **Generate Domain**
- ستحصل على URL مثل `https://dealix-production-abc.up.railway.app`

---

## الخطوة 5 — Smoke Test (دقيقة واحدة)

من جهازك:
```bash
git pull origin claude/launch-command-center-6P4N0
export STAGING_BASE_URL=https://YOUR-PROJECT.up.railway.app
python scripts/staging_smoke.py --base-url $STAGING_BASE_URL
```

**Expected output:** `STAGING_SMOKE_PASS` (12+ probes كلها OK).

إذا فشل: راجع Railway logs → `Settings → Logs`.

---

## الخطوة 6 — Seed Demo Data (دقيقة واحدة)

اربط بقاعدة Postgres الحية + شغّل seeder:

```bash
# احصل على DATABASE_URL من Railway dashboard → Postgres → Connect → Public Network
export DATABASE_URL="postgresql://postgres:PASSWORD@HOST.railway.app:PORT/railway"
python scripts/seed_commercial_demo.py
```

**Expected:**
```
TOTAL ROWS INSERTED: 68
```

الآن `agency-partner.html?partner_id=demo_partner_riyadh` يعرض بيانات حقيقية.

---

## الخطوة 7 — Custom Domain (10 دقائق — اختياري)

إذا عندك `dealix.me`:
1. في domain registrar (Namecheap/Cloudflare):
   - أضف **CNAME**: `app` → `YOUR-PROJECT.up.railway.app`
2. في Railway: Settings → Domains → Add Custom Domain → `app.dealix.me`
3. انتظر TTL (10-30 دقيقة)
4. تحقق: `curl https://app.dealix.me/healthz` → 200

---

## الخطوة 8 — Cron Schedule (5 دقائق)

Railway يدعم cron عبر **Cron Jobs**:
1. Add Service → Empty Service → اسمه `dealix-cron`
2. Settings → Cron Schedule → أضف 4 jobs:

```cron
# KSA = UTC+3
30 5 * * *  curl -X POST $APP_URL/api/v1/daily-ops/run -H "Content-Type: application/json" -d '{"window":"morning"}'
30 9 * * *  curl -X POST $APP_URL/api/v1/daily-ops/run -H "Content-Type: application/json" -d '{"window":"midday"}'
30 13 * * * curl -X POST $APP_URL/api/v1/daily-ops/run -H "Content-Type: application/json" -d '{"window":"closing"}'
0 15 * * *  curl -X POST $APP_URL/api/v1/daily-ops/run -H "Content-Type: application/json" -d '{"window":"scorecard"}'
```

---

## ✅ تأكيد نهائي

```bash
# 1. Health
curl https://YOUR-URL/healthz                          # → 200

# 2. Services catalog
curl https://YOUR-URL/api/v1/services/catalog          # → 6 bundles

# 3. Live partner dashboard (after seeding)
curl https://YOUR-URL/api/v1/partners/demo_partner_riyadh/dashboard

# 4. Live Proof Pack
curl https://YOUR-URL/api/v1/proof-ledger/customer/demo_cust_training_co/pack

# 5. Daily ops trigger
curl -X POST https://YOUR-URL/api/v1/daily-ops/run \
     -H "Content-Type: application/json" \
     -d '{"window":"morning"}'

# 6. Browser sanity
open https://YOUR-URL/index.html
open https://YOUR-URL/command-center.html
open https://YOUR-URL/agency-partner.html?partner_id=demo_partner_riyadh
open https://YOUR-URL/proof-pack.html?customer_id=demo_cust_training_co
```

كل واحد منهم يجب يعرض بيانات (ليس demo banner).

---

## 🚨 Troubleshooting

| المشكلة | الحل |
|---|---|
| Build fails | راجع Railway logs. عادة: pip install error → تحقق `pyproject.toml` |
| 502 Bad Gateway | uvicorn لم يبدأ. logs → ابحث عن Python traceback |
| 404 on `/healthz` | الـ Dockerfile لم يبدأ uvicorn — راجع CMD line |
| Postgres connection error | احذف Dealix service + redeploy، Railway يعيد ربط `DATABASE_URL` |
| `/auth/me` returns 500 | `APP_SECRET_KEY` ناقص — أضفه في Variables |
| Magic link لا يصل | `RESEND_ALLOW_LIVE_SEND=false` (مقصود في staging) — استخدم `dev_magic_url` من response |

---

## بعد النشر

1. **اقرأ:** `docs/LAUNCH_DAY_CHECKLIST.md` — ساعة بساعة
2. **افتح:** `docs/READY_OUTREACH_MESSAGES.md` — أول 5 رسائل LinkedIn
3. **اقرأ:** `docs/RUNBOOK.md` — Daily Operating Rhythm

النظام جاهز. باقي عليك الـ outreach + الـ Pilot الأول.
