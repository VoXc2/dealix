# Dealix — Launch Day Checklist (D-7 → D+7)

هذي الوثيقة هي السكربت الرسمي لليوم الذي تنشر فيه Dealix على staging
وتبدأ outreach حقيقي. اقرأها بالكامل قبل D-7. لا تتجاوز أي بند بدون
سبب موثّق في commit message.

---

## D-7 — التحضير الأسبوعي

### تقني
- [ ] git pull آخر commit على `claude/launch-command-center-6P4N0`
- [ ] محلياً: `python scripts/launch_checklist.py` → **LAUNCH_READY (5/5)**
- [ ] محلياً: `docker build -t dealix:staging .` → ينجح
- [ ] محلياً: `docker run --rm -p 8000:8000 -e APP_ENV=test ... dealix:staging` → `/healthz` 200
- [ ] أنشأ Railway project + أضف PostgreSQL + Redis services
- [ ] انسخ `.env.staging.example` → اضبط 30+ متغير في Railway dashboard
- [ ] **تحقق صراحة:** كل live-action gate = `false` (8 gates)

### تجاري
- [ ] CR (السجل التجاري) جاهز ومُحدَّث
- [ ] Moyasar dashboard مفعّل (manual invoice mode فقط)
- [ ] Resend domain verified (DKIM + SPF + DMARC)
- [ ] PostHog production project مُنشأ
- [ ] أول 30 وكالة من `OUTREACH_PLAYBOOK.md` مُختارة (LinkedIn URLs جاهزة)
- [ ] WhatsApp Business inbound يعمل + رابط `wa.me/...` جاهز

### قانوني
- [ ] Privacy Policy منشورة (PDPL aligned) — موجودة في `landing/trust-center.html`
- [ ] Terms of Service منشورة
- [ ] Refund policy موجودة في `docs/REFUND_POLICY.md`
- [ ] DPA pilot template جاهز للعميل الأول (`docs/DPA_PILOT_TEMPLATE.md`)

---

## D-1 — اليوم السابق

### إعدادات نهائية
- [ ] Push آخر commit على الفرع
- [ ] Railway: `Manual Deploy` من `claude/launch-command-center-6P4N0`
- [ ] انتظر 3-5 دقائق حتى ينتهي البناء
- [ ] استخرج `STAGING_BASE_URL` من Railway
- [ ] `python scripts/staging_smoke.py --base-url $STAGING_BASE_URL` → **STAGING_SMOKE_PASS**
- [ ] DNS: أضف `app.dealix.me` → Railway (CNAME)
- [ ] انتظر TTL (10-30 دقيقة)

### نهائي قبل D0
- [ ] افتح `https://app.dealix.me/healthz` → 200
- [ ] افتح `https://app.dealix.me/api/v1/services/catalog` → 6 bundles
- [ ] افتح `https://app.dealix.me/api/v1/cards/feed?role=ceo` → 200 + cards
- [ ] افتح `https://app.dealix.me/api/v1/observability/unsafe/summary` → invariant true
- [ ] جهّز LinkedIn outreach drafts (5 رسائل من القوالب) في document
- [ ] جهّز قائمة الـ 30 وكالة في spreadsheet مع: name / linkedin / status

### Sleep
- [ ] نَم باكراً. اليوم التالي طويل.

---

## D0 — يوم التدشين (KSA Time)

### 06:30 — التحضير الشخصي
- [ ] قهوة + هدوء
- [ ] راجع `RUNBOOK.md §1` — Daily Operating Rhythm
- [ ] افتح Railway dashboard + Logtail/Datadog tab

### 07:00 — Preflight (60 دقيقة قبل أول outreach)
- [ ] `curl https://app.dealix.me/healthz` → 200
- [ ] `curl https://app.dealix.me/health/deep` → كل subsystem healthy
- [ ] `python scripts/staging_smoke.py --base-url $STAGING_BASE_URL` → PASS
- [ ] افتح `app.dealix.me/command-center.html` → role-switcher يعمل + observability widgets يعرضون
- [ ] افتح `app.dealix.me/operator.html` → اضغط "أرسل واتساب لقائمة باردة" → يجب الرفض الآمن
- [ ] افتح `app.dealix.me/proof-pack.html` → demo Proof Pack يظهر
- [ ] أرسل تجربة `POST /api/v1/auth/magic-link/send` بـ test email → احتفظ بـ dev_magic_url للتجربة
- [ ] PostHog يستلم events (cta_clicked, page_viewed)

### 08:00 — Soft Launch Internal
- [ ] أرسل WhatsApp للـ co-founder/family/inner circle: "Dealix على staging الآن — جرّب operator.html و قل لي رأيك"
- [ ] راقب inbox + Slack/WhatsApp business
- [ ] أصلح أي bug فوراً (انظر RUNBOOK §4 incidents)

### 08:30 — Daily Ops Morning
```bash
curl -X POST $STAGING/api/v1/daily-ops/run -d '{"window":"morning"}'
```
- [ ] تأكد runs بدون errors
- [ ] اقرأ CEO brief

### 09:00 — Outreach Wave 1 (5 رسائل LinkedIn)
- [ ] افتح `OUTREACH_PLAYBOOK.md` → Template 1
- [ ] أرسل لـ 5 وكالات (manual، personal account، لا automation)
- [ ] سجّل في spreadsheet: timestamp + name + template_id

### 10:00 — Outreach Wave 2 (10 رسائل إضافية)
- [ ] استخدم Templates 2-3
- [ ] اطلب من 1-2 من شبكتك intro warm

### 11:00 — Founder content
- [ ] انشر LinkedIn post بصيغة:
  > "أطلقت Dealix اليوم. Saudi Revenue Execution OS — نشغّل النمو لشركات
  > B2B والوكالات. approval-first. لا cold WhatsApp. لا scraping. كل شيء
  > بـ Proof Pack قابل للقياس. Pilot 499 ريال 7 أيام. تجربة مجانية: app.dealix.me"
- [ ] انشر على X/Twitter بنفس الفكرة + رابط

### 12:30 — Daily Ops Midday
```bash
curl -X POST $STAGING/api/v1/daily-ops/run -d '{"window":"midday"}'
```
- [ ] راقب أول الردود

### 13:00 — استراحة + متابعة
- [ ] رد على inbound (WhatsApp + LinkedIn + Email) خلال ساعة
- [ ] إذا أحدهم طلب Diagnostic → احجز call فوراً (15 دقيقة)

### 15:00 — Outreach Wave 3 (10 رسائل إضافية)
- [ ] استخدم Templates 4-6
- [ ] هدف: إجمالي 25 رسالة في D0

### 16:30 — Daily Ops Closing
```bash
curl -X POST $STAGING/api/v1/daily-ops/run -d '{"window":"closing"}'
```
- [ ] راجع pipeline: من ردّ؟ من احتاج follow-up؟

### 17:00 — Customer Support
- [ ] رد على كل support ticket
- [ ] إذا في P0 → اتبع RUNBOOK §4

### 18:00 — Daily Ops Scorecard
```bash
curl -X POST $STAGING/api/v1/daily-ops/run -d '{"window":"scorecard"}'
```
- [ ] اقرأ scorecard
- [ ] دوّن: عدد outreach، عدد ردود، عدد diagnostic مجدول

### 19:00 — End-of-Day Review (15 دقيقة)
- [ ] `curl $STAGING/api/v1/observability/costs/summary?days=1` → التكلفة اليومية
- [ ] `curl $STAGING/api/v1/observability/unsafe/summary?days=1` → refusals
- [ ] أرسل Slack/Telegram update لنفسك:
  > "Day 0: X رسالة، Y ردود، Z diagnostic مجدول، 0 unsafe action، تكلفة AI: SAR W."

### 20:00 — إغلاق
- [ ] اقفل التابات
- [ ] لا تردّ على الـ inbox بعد 20:00 (إلا P0)

---

## D+1 — اليوم التالي

- [ ] 08:30: morning daily-ops
- [ ] راجع spreadsheet — كم ردّ بين الـ 25 رسالة؟
- [ ] أرسل follow-up emails لمن لم يردّ بعد 24 ساعة (انظر OUTREACH §3)
- [ ] أكمل Wave 4 (10 رسائل إضافية)
- [ ] إذا في diagnostic مجدول → اتبع `FIRST_PILOT_INTAKE.md`
- [ ] انشر LinkedIn thread (3 tweets):
  - tweet 1: لماذا Dealix مختلف عن CRMs
  - tweet 2: ما يعنيه approval-first في الممارسة
  - tweet 3: مثال على Proof Pack

---

## D+3 — منتصف الأسبوع

- [ ] إجمالي outreach: 50-60 رسالة
- [ ] إجمالي ردود: 8-12 (هدف ~15-20% reply rate)
- [ ] إجمالي diagnostic: 2-3
- [ ] **هدف:** أول Pilot 499 invoice مُرسَل قبل D+7

---

## D+7 — نهاية الأسبوع الأول

### تقني
- [ ] راجع `/api/v1/observability/quality?days=7` → kpis معقولة
- [ ] راجع `/api/v1/observability/costs/summary?days=7` → التكلفة الإجمالية ≤ 500 SAR للأسبوع
- [ ] لا breach في `/observability/unsafe/summary` → invariant true

### تجاري
- [ ] إجمالي outreach: 120-150 رسالة
- [ ] إجمالي ردود: 20-30
- [ ] إجمالي Pilot offers: 3-5
- [ ] إجمالي Pilot paid: **1 على الأقل** (إذا 0 → تحدّى outreach + offer)

### تعلم
- [ ] أكتب Weekly Learning في `docs/`:
  - أي template كان الأعلى استجابة؟
  - أي قطاع أعطى أكبر ردود؟
  - أي objection كان متكرر؟
  - تحسين واحد للأسبوع القادم.

---

## ⛔ Stop Conditions (متى توقف وتراجع)

أوقف outreach وعد للبناء إذا:
- 3 شكاوى من نفس النوع في يوم
- `unsafe_action_executed = true` في أي endpoint (P0 incident)
- Railway 5xx > 5 دقائق متواصلة
- Moyasar invoice `paid` لم يُسجَّل في `payments` table (webhook broken)
- `forbidden_claims_audit` يفشل بعد أي edit

---

## ✅ Success Criteria للأسبوع الأول

| المؤشر | الهدف الأدنى | الهدف الطموح |
|---|---|---|
| Outreach manual | 100 | 150 |
| Reply rate | 10% | 20% |
| Diagnostic calls | 3 | 8 |
| Pilot offers | 2 | 5 |
| Pilot paid | 1 | 3 |
| Proof Packs delivered | 1 | 3 |
| Unsafe actions executed | **0** | **0** |
| AI cost | ≤ 500 SAR | ≤ 300 SAR |
| Uptime | ≥ 99% | ≥ 99.9% |

عند تحقق "الهدف الأدنى" بكل البنود → أنت في **REAL PAID BETA**.
