# قائمة التحقق — تدشين Dealix التجاري
# Go-Live Checklist — Dealix Commercial Launch
**الإصدار**: 1.0 | **التاريخ**: 2026-05-30 | **المسؤول**: الفاوندر

---

## المرحلة 1 — إعداد Railway (يوم واحد)

### متغيرات البيئة المطلوبة (Railway → Variables)

```bash
# ── الدفع (Moyasar) ─────────────────────────────────
MOYASAR_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxx   # من dashboard.moyasar.com
MOYASAR_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxx   # من Moyasar → Webhooks
MOYASAR_LIVE_MODE=1                             # تفعيل الدفع الحقيقي

# ── ZATCA (الفوترة الإلكترونية) ──────────────────────
ZATCA_CSID=xxxxxxxxxxxxxxxxxx                   # من Fatoorah portal
ZATCA_SECRET=xxxxxxxxxxxxxxxxxx                 # من Fatoorah portal
ZATCA_SANDBOX=false                             # تغيير للإنتاج
ZATCA_SELLER_VAT_NUMBER=3000000000000000       # رقم الضريبة السعودي
ZATCA_SELLER_NAME=Dealix                        # اسم الشركة
ZATCA_SELLER_CITY=Riyadh                        # مدينة التسجيل

# ── البريد الإلكتروني (Gmail API) ───────────────────
GMAIL_CREDENTIALS_JSON={"installed":{...}}      # من Google Cloud Console
GMAIL_SENDER_EMAIL=your@gmail.com               # بريد الإرسال

# ── WhatsApp للفاوندر ────────────────────────────────
DEALIX_FOUNDER_PHONE=+966XXXXXXXXX             # بصيغة E.164
WHATSAPP_ALLOW_LIVE_SEND=true                   # تفعيل التنبيهات
WHATSAPP_API_TOKEN=EAAxxxxxxxxxxxxxxxxxx        # من Meta Business

# ── الذكاء الاصطناعي ─────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx   # للتشخيصات والإيميلات
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx      # (احتياطي)

# ── قاعدة البيانات (Railway auto-sets) ───────────────
DATABASE_URL=postgresql://...                    # Railway يضيفه تلقائياً
REDIS_URL=redis://...                           # Railway يضيفه تلقائياً

# ── الأمان ───────────────────────────────────────────
DEALIX_ADMIN_API_KEY=your-strong-secret-key     # للـ /api/v1/commercial/* endpoints
SECRET_KEY=your-32-char-random-key              # لتشفير الجلسات
```

### خطوات Railway

- [ ] افتح Railway → مشروعك → Variables
- [ ] أضف كل المتغيرات أعلاه
- [ ] تحقق: `GET https://api.dealix.me/health` يرجع `{"status":"ok"}`
- [ ] تحقق: `GET https://api.dealix.me/health/deep` يرجع `{"status":"ok"}`

---

## المرحلة 2 — إعداد Moyasar (ساعتان)

- [ ] سجّل حساباً في dashboard.moyasar.com (أو استخدم الحساب الحالي)
- [ ] فعّل Live Mode (يتطلب OTP من SAMA)
- [ ] أنشئ API Key (Live) وضعه في `MOYASAR_SECRET_KEY`
- [ ] اضبط Webhook URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
- [ ] اختبر بـ `pilot_1sar` plan (1 ريال):
  ```bash
  curl -X POST https://api.dealix.me/api/v1/checkout \
    -H "Content-Type: application/json" \
    -d '{"plan":"pilot_1sar","email":"test@yourdomain.com","lead_id":"e2e-test"}'
  ```
- [ ] تحقق أن الـ webhook وصل وتم معالجته

---

## المرحلة 3 — إعداد ZATCA (يوم واحد)

- [ ] سجّل في بوابة Fatoorah (Sandbox → Production)
- [ ] احصل على CSID + Secret
- [ ] اختبر sandbox: `ZATCA_SANDBOX=true` (الافتراضي)
- [ ] عند الجاهزية: غيّر `ZATCA_SANDBOX=false`
- [ ] تحقق: بعد أي دفعة، يظهر في الـ logs:
  ```
  zatca_invoice_issued action=clearance uuid=xxx amount_sar=499.00
  ```

---

## المرحلة 4 — التحقق من التشين الكامل (ساعة واحدة)

### الاختبار النهائي (E2E):

```bash
ADMIN_KEY="your-admin-api-key"
API="https://api.dealix.me"

# 1. تشخيص مجاني
curl -X POST $API/api/v1/commercial/diagnostic/generate \
  -H "X-API-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"شركة الاختبار","sector":"b2b_services","pain_points":["lead_gen"]}'

# 2. مسودة warm intro
curl -X POST $API/api/v1/commercial/warm-intro/draft \
  -H "X-API-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prospect_name":"أحمد","company_name":"شركة الاختبار","sector":"b2b_services"}'

# 3. رابط دفع
curl -X POST $API/api/v1/commercial/payment/link \
  -H "X-API-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"service_tier":"sprint_499","customer_name":"أحمد"}'

# 4. بدء pilot
curl -X POST $API/api/v1/commercial/pilot/start \
  -H "X-API-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"account_id":"test-001","company_name":"شركة الاختبار"}'

# 5. ملخص يومي
curl $API/api/v1/commercial/daily-brief -H "X-API-Key: $ADMIN_KEY"
```

### نقاط التحقق:
- [ ] التشخيص يرجع 10 أقسام AR+EN
- [ ] Warm intro يرجع 5 واتساب + 3 إيميل
- [ ] رابط الدفع يرجع Moyasar URL
- [ ] ريسيبت الإيميل يصل للعميل بعد الدفع
- [ ] تنبيه واتساب يصل للفاوندر
- [ ] فاتورة ZATCA تُصدَر

---

## المرحلة 5 — الإطلاق التجاري (اليوم الأول)

### قائمة العملاء المستهدفين الأوائل

استخدم `data/templates/warm_intro_whatsapp_ar.md` للتواصل مع:

| الاسم | الشركة | القطاع | القالب |
|-------|--------|--------|--------|
| --- | --- | --- | V1 |
| --- | --- | --- | V3 |
| --- | --- | --- | V5 |

### جدول الإطلاق (الأسبوع الأول)

| اليوم | الفعل |
|-------|-------|
| **السبت** | إرسال 5 warm intros (V1+V2+V5) → طلب موافقتك |
| **الأحد** | متابعة الردود + جدولة diagnostic مجاني |
| **الاثنين** | تسليم أول تشخيص + عرض Sprint 499 ريال |
| **الثلاثاء** | إغلاق أول صفقة (499 ريال) + بدء البرنامج |
| **الأربعاء-الخميس** | تنفيذ الأيام 1-3 من pilot |
| **الجمعة** | تقرير الأسبوع + تخطيط الأسبوع القادم |

---

## الحماية والامتثال

- [ ] تأكد أن PDPL consent موجود في نموذج التشخيص
- [ ] تأكد أن ZATCA Live قبل إصدار فواتير حقيقية
- [ ] لا ترسل أي رسالة بدون مراجعتك (NO_LIVE_SEND)
- [ ] لا تُشغّل Live Moyasar بدون Live ZATCA (الالتزام القانوني)

---

## مؤشرات النجاح — الأسبوع الأول

| المؤشر | الهدف |
|---------|-------|
| warm intros مُرسَلة | ≥5 |
| ردود مستلمة | ≥2 |
| تشخيصات مُجدولة | ≥1 |
| صفقة مُغلقة | ≥1 (499 ريال) |
| إيميل ريسيبت وصل | ✅ |
| فاتورة ZATCA صدرت | ✅ |

---

*Dealix — كل شيء جاهز، ابدأ.*
