# ⚙️ Railway + Moyasar — خطوة بخطوة (12 دقيقة بالضبط)

**الهدف:** Backend شغّال + Moyasar يستقبل دفعات حقيقية.

**اللي ستسويه:** 3 مراحل، كل واحدة مقطعة لخطوات واضحة.

**ملاحظة مهمة:** جرّبت الـ URL `dealix-production-up.railway.app` الآن — يرد لكن من Railway نفسه (404 من تطبيقك). يعني خدمتك لم تُنشر بعد أو Deploy متوقف. الخطوات أدناه تحل ذلك.

---

## 🅰️ المرحلة A — Railway Settings (5 دقائق)

### A1. افتح المشروع
رابط مباشر: https://railway.com/project/54bb60b4-d059-4dd1-af57-bc44c702b9f0

### A2. اختر خدمة `dealix` من الـ sidebar

### A3. تأكد أن الـ repo متصل بـ GitHub
- **Settings** → **Source**
- يجب أن يكون: `VoXc2/dealix` — branch: `main`
- إذا لم يكن — اضغط **Connect GitHub Repo**

### A4. امسح Start Command
- **Settings** → **Deploy**
- ابحث عن **Start Command**
- **امسح المحتوى كامل** (يصير فارغ)
- اضغط خارج الحقل → يحفظ تلقائياً

> ⚠️ سبب أهمية هذا: Railway UI Start Command يتجاوز Dockerfile. نريد Dockerfile يتحكم.

### A5. تأكد من Health Check
- نفس قسم **Deploy**
- **Healthcheck Path:** `/health`
- **Healthcheck Timeout:** 300 ثانية

### A6. احفظ + نشر يدوي
- **Deployments** → **Deploy** (زر أزرق في الأعلى)
- انتظر 2-3 دقائق

**تحقق:**
- Status يصير **Active** (أخضر)
- Logs تعرض: `Uvicorn running on http://0.0.0.0:XXXX`

### A7. انسخ الـ Public URL
- **Settings** → **Networking** → **Public Domain**
- مثال: `dealix-production-up.railway.app`
- **احفظ هذا الرابط** — ستستخدمه في B وفي Landing

---

## 🅱️ المرحلة B — Environment Variables (4 دقائق)

### B1. افتح Raw Editor
- Service `dealix` → **Variables** → زر صغير أعلى يسار: **Raw Editor**

### B2. الصق هذا المحتوى (عدّل CHANGE_ME الأربعة في النهاية)

```env
# ── Application Core ──
APP_ENV=production
ENVIRONMENT=production
APP_NAME=Dealix
APP_VERSION=3.0.0
APP_SECRET_KEY=ec11871ba7100c04368fd52d356fe0463c0d1e510fa8da0cbbc58abb3ff479c6
APP_LOG_LEVEL=INFO
LOG_LEVEL=INFO
APP_DEFAULT_LOCALE=ar
APP_DEFAULT_CURRENCY=SAR
APP_TIMEZONE=Asia/Riyadh

# ── CORS (عدّل الدومين بعد ربط dealix.sa) ──
CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa,http://localhost:3000

# ── Public URL (يُستخدم في Moyasar callback) ──
APP_URL=https://dealix-production-up.railway.app

# ── Moyasar Payments ──
MOYASAR_SECRET_KEY=CHANGE_ME_sk_live_from_moyasar_dashboard
MOYASAR_WEBHOOK_SECRET=9b4bf9e94175eb25cf4c8ec0c4e3915f518215503f848c633cf34c4598b7ff82

# ── PostHog (اختياري لكن موصى به) ──
POSTHOG_API_KEY=CHANGE_ME_phc_from_posthog
POSTHOG_HOST=https://us.i.posthog.com

# ── Calendly ──
CALENDLY_URL=https://calendly.com/sami-assiri11/dealix-demo

# ── WhatsApp (عدّل إذا ربطت Meta) ──
WHATSAPP_VERIFY_TOKEN=CHANGE_ME
WHATSAPP_ACCESS_TOKEN=CHANGE_ME
```

**قيم CHANGE_ME الأربعة:**
1. `MOYASAR_SECRET_KEY` → من https://dashboard.moyasar.com/settings/basic-integration
2. `POSTHOG_API_KEY` → من https://us.posthog.com/settings (اختياري)
3. `WHATSAPP_VERIFY_TOKEN` → اختر أي نص عشوائي (ستضعه في Meta)
4. `WHATSAPP_ACCESS_TOKEN` → من Meta Developer Console (اختياري الآن)

### B3. احفظ
- اضغط **Update Variables** (زر أزرق)
- Railway سيعيد deploy تلقائياً

### B4. أضف PostgreSQL إذا غير موجود
- الخدمة الرئيسية → **+ New** → **Database** → **PostgreSQL**
- Railway يحقن `DATABASE_URL` تلقائياً في `dealix` service

### B5. تحقق من النشر
- انتظر 60-90 ثانية
- افتح terminal:
```bash
curl https://dealix-production-up.railway.app/health
# يجب أن يرجع: {"status":"ok","service":"dealix-api"}
```

إذا ما رجع 200 — راجع Railway Logs.

---

## 🅲️ المرحلة C — Moyasar Webhook (3 دقائق)

### C1. افتح Moyasar Dashboard
https://dashboard.moyasar.com/webhooks

### C2. اضغط **Add Webhook**

### C3. عبّي:
- **URL:**
  ```
  https://dealix-production-up.railway.app/api/v1/webhooks/moyasar
  ```
  (استبدل بـ Railway URL الفعلي إذا مختلف)

- **Events (اختر الثلاثة):**
  - ☑ `payment_paid`
  - ☑ `payment_failed`
  - ☑ `payment_refunded`

- **Secret:**
  ```
  9b4bf9e94175eb25cf4c8ec0c4e3915f518215503f848c633cf34c4598b7ff82
  ```
  (نفس قيمة `MOYASAR_WEBHOOK_SECRET` في Railway)

### C4. احفظ
- Moyasar يرسل ping اختباري
- يجب أن يظهر **Last Delivery: 200 OK**

### C5. بدّل لـ Live Keys (متى كنت جاهز)
- **Settings** → **Basic Integration**
- بدّل من `sk_test_*` لـ `sk_live_*`
- حدّث `MOYASAR_SECRET_KEY` في Railway بنفس القيمة

---

## ✅ التحقق النهائي — اختبار 1 ريال

شغّل السكريبت (موجود في `dealix_1_riyal_test.sh`):

```bash
bash dealix_1_riyal_test.sh
```

التوقع:
- ✅ `/health` → 200
- ✅ `/api/v1/pricing/plans` → يرجع الباقات
- ✅ `/api/v1/public/demo-request` → 200 + Calendly URL
- ✅ `/api/v1/checkout` → يرجع `payment_url` من Moyasar

**الخطوة النهائية:** افتح `payment_url` في المتصفح، ادفع 1 ريال ببطاقتك → ✅ **أول دفعة حقيقية في Dealix**.

---

## 🚨 المشاكل الشائعة

### `/health` يرجع 404
- Railway لم ينشر بعد — راجع **Deployments** → شوف آخر deploy
- إذا Failed → افتح Logs → ابحث عن `Error` أو `ModuleNotFoundError`
- أرسل Logs وأنا أحلها

### `/api/v1/checkout` يرجع 502
- `MOYASAR_SECRET_KEY` خاطئ أو ما محدث
- تأكد من الـ sk_live prefix وأنه الصحيح

### Moyasar webhook 401
- `MOYASAR_WEBHOOK_SECRET` في Railway **مختلف** عن اللي في Moyasar dashboard
- تأكد من تطابقهما حرفياً (لا مسافات)

### Landing form ما يرد
- افتح Console في Chrome → ابحث عن `CORS` error
- إذا موجود → أضف domain landing في `CORS_ORIGINS` وحدّث Railway

---

## 🎯 بعد نجاح الـ 3 مراحل

1. افتح `dealix_personalized_messages.md`
2. ابدأ بـ **عبدالله العسيري** (نفس اسم العائلة = أعلى فرصة)
3. أرسل 2-3 رسائل اليوم
4. افتح `dealix_14day_tracker.html` → سجّل كل رسالة

**الهدف:** أول pilot بـ 1 ريال خلال 7 أيام، أول Starter 999 خلال 14 يوم.
