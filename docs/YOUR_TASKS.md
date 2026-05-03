# YOUR TASKS — قائمتك الوحيدة

**كل شيء في الكود + الوثائق + الـ tooling انتهى.** هذي قائمة الأشياء الإنسانية
التي **فقط أنت** تقدر تسويها — لأنها تتطلب هويتك أو credentials أو موافقة قانونية.

كل بند له:
- ⏱ الوقت المتوقع
- 📍 الرابط/الأمر الجاهز
- ✅ Definition of Done

---

## ⚡ روتين الصباح (30 ثانية كل يوم — بعد الـ deploy)

```bash
export DEALIX_BASE_URL=https://app.dealix.me
python scripts/dealix_cli.py today
```

ينتج تقرير ملوّن يحتوي:
- CEO Brief (3 قرارات اليوم)
- KPIs آخر 7 أيام (subscriptions، MRR، proof events، unsafe blocked)
- Quality KPIs (acceptance rate، override rate، complaint rate)
- AI cost (SAR + agent runs + latency)
- Open incidents (P0/P1)
- Recent daily-ops runs
- 8 live-action gates status
- Next morning actions

أمر واحد = كل ما تحتاجه. **استبدل الـ 6 URLs السابقة بهذا.**

أوامر CLI الأخرى:
```bash
python scripts/dealix_cli.py outreach pick 5     # أول 5 رسائل اليوم
python scripts/dealix_cli.py run-window morning  # شغّل morning brief يدوياً
python scripts/dealix_cli.py proof demo_cust_X  # Proof Pack لعميل
python scripts/dealix_cli.py smoke              # smoke test كامل
python scripts/dealix_cli.py gates              # تأكد كل الـ gates FALSE
```

اختصار:
```bash
sudo ln -s "$(pwd)/scripts/dealix_cli.py" /usr/local/bin/dealix
# الآن: dealix today
```

---

## 🔴 D0 — اليوم (90 دقيقة)

### [1] Railway Deploy ⏱ 15 دقيقة
- 📍 افتح: [`docs/RAILWAY_ONE_CLICK.md`](RAILWAY_ONE_CLICK.md)
- اتبع الخطوات 1-5 (تسجيل، إضافة Postgres+Redis، env vars، deploy، smoke)
- ✅ DoD: `python scripts/staging_smoke.py --base-url $URL` يرجع `STAGING_SMOKE_PASS`

### [2] Seed Demo Data ⏱ 2 دقيقة
- 📍 الأمر:
  ```bash
  export DATABASE_URL="postgresql://..."  # من Railway
  python scripts/seed_commercial_demo.py
  ```
- ✅ DoD: `TOTAL ROWS INSERTED: 68`

### [3] Browser Sanity Check ⏱ 5 دقائق
افتح في المتصفح + تأكد:
- 📍 `https://YOUR-URL/index.html` — homepage
- 📍 `https://YOUR-URL/command-center.html` — الـ 3 widgets تعرض بيانات
- 📍 `https://YOUR-URL/agency-partner.html?partner_id=demo_partner_riyadh` — KPIs + جدول
- 📍 `https://YOUR-URL/proof-pack.html?customer_id=demo_cust_training_co` — proof pack حقيقي
- ✅ DoD: لا 404 + لا 500 + الـ data تعرض

### [4] إنشاء Domain (إذا لم يكن جاهز) ⏱ 30 دقيقة
- سجّل `dealix.me` (أو ما تختاره) من Namecheap/Cloudflare
- اربط `app.dealix.me` → Railway URL (CNAME)
- ✅ DoD: `curl https://app.dealix.me/healthz` → 200

### [5] LinkedIn Profile Update ⏱ 10 دقائق
- Headline: "Founder @ Dealix — Saudi Revenue Execution OS"
- Featured: ضع رابط `app.dealix.me/proof-pack.html`
- About: انسخ من `landing/index.html` hero copy
- ✅ DoD: profile يبدو مهنياً + يعكس Dealix

### [6] WhatsApp Business Setup ⏱ 20 دقيقة
- نزّل **WhatsApp Business app** على هاتفك
- استخدم رقم **منفصل** (لا تستخدم رقمك الشخصي)
- ضع profile name: "Dealix"
- ضع greeting message: "أهلاً، تواصلك حول Dealix Saudi Revenue OS — أحد فريقنا سيرد خلال ساعة"
- ضع الرابط `wa.me/9665XXXXXXXX` في footer كل صفحة
- ✅ DoD: تستلم رسالة test من حسابك الشخصي

---

## 🟡 D1-D7 — الأسبوع الأول (يومياً 90 دقيقة)

### [7] LinkedIn Outreach Manual ⏱ 30 دقيقة/يوم
- 📍 افتح: [`docs/READY_OUTREACH_MESSAGES.md`](READY_OUTREACH_MESSAGES.md)
- يومياً: اختر 5 وكالات/شركات → انسخ template → عدّل [الاسم] → أرسل
- سجّل في Google Sheets (template في READY_OUTREACH_MESSAGES.md §Tracking)
- ✅ DoD أسبوعي: 30 رسالة مُرسَلة

### [8] الردّ على Inbound ⏱ 15 دقيقة/يوم
- WhatsApp + LinkedIn + Email خلال **ساعة**
- لا ترد بـ template آلي — رد بأسلوبك الشخصي
- ✅ DoD: response time ≤ 60 دقيقة في ساعات العمل

### [9] Diagnostic Calls (عند توفر) ⏱ 30 دقيقة/call
- استخدم Google Meet / Zoom / WhatsApp call
- اتبع `docs/OUTREACH_PLAYBOOK.md §5` (10 أسئلة)
- بعد الـ call بساعة: أرسل diagnostic report
- ✅ DoD: 2-3 diagnostic calls في الأسبوع الأول

### [10] Pilot 499 Offer ⏱ 30 دقيقة (لكل عميل مهتم)
- استخدم email Template 02 من `READY_OUTREACH_MESSAGES.md`
- في Moyasar dashboard: أنشئ invoice manual بـ 499 SAR
- أرسل الرابط
- ✅ DoD: 1+ pilot paid قبل D+7

### [11] Founder Content (LinkedIn Posts) ⏱ 15 دقيقة/يوم
- يوم 1: "أطلقت Dealix اليوم — Saudi Revenue Execution OS"
- يوم 3: thread عن "لماذا approval-first يهم في السعودية" (مع PDPL stats)
- يوم 5: "أول Pilot 499 — تجربة + درس" (إذا حصل)
- ✅ DoD: 3 LinkedIn posts في الأسبوع

---

## 🟢 D8-D14 — الأسبوع الثاني (أول Proof Pack)

### [12] تنفيذ Pilot 499 الأول ⏱ 60-90 دقيقة/يوم
- 📍 افتح: [`docs/FIRST_PILOT_INTAKE.md`](FIRST_PILOT_INTAKE.md)
- اتبع كل قسم: intake → execution (curls جاهزة) → DoD checklist
- يوم 7: ابن Proof Pack PDF (manual أو من `/api/v1/proof-ledger/customer/{id}/pack`)
- أرسله للعميل
- ✅ DoD: أول Proof Pack مُسلَّم + ServiceSession في حالة `proof_generated`

### [13] Upgrade Conversation ⏱ 30 دقيقة
- بعد Proof Pack بـ 24-48 ساعة: احجز call 30 دقيقة
- اتبع `docs/FIRST_PILOT_INTAKE.md §4` (Upgrade Call Script)
- العرض: Executive Growth OS بـ 2,999 SAR/شهر
- ✅ DoD: قرار upgrade (Yes/No/Later) موثَّق

### [14] إعداد Cron Schedule ⏱ 10 دقائق
- 📍 من `docs/RAILWAY_ONE_CLICK.md` خطوة 8
- أضف 4 cron jobs (08:30 / 12:30 / 16:30 / 18:00 KSA)
- ✅ DoD: 4 daily-ops runs تظهر في `/api/v1/daily-ops/history`

---

## 🔵 D15-D30 — الأسبوع 3-4

### [15] أول 3 Paid Pilots ⏱ متغير
- التركيز على conversion من diagnostic → pilot
- استخدم objection responses من `READY_OUTREACH_MESSAGES.md` Email 04
- ✅ DoD: 3 pilots paid + 2 Proof Packs مُسلَّمة

### [16] First Agency Partnership ⏱ 60 دقيقة
- استخدم Email 05 (Agency Partnership Pitch)
- عرض: Co-branded Proof Pack لعميل واحد + 15% MRR commission
- ✅ DoD: 1 وكالة شريكة + 1 عميل مشترك

### [17] Saudi B2B LinkedIn Content ⏱ 30 دقيقة/أسبوع
- post أسبوعي عن: PDPL · approval-first · Proof Pack · Saudi market insights
- ✅ DoD: 4 posts/شهر + engagement حقيقي

---

## 🟣 D30+ — التوسع

### [18] أول Executive Growth OS Subscription ⏱ بعد 3+ pilots
- 2,999 SAR/شهر — أول MRR حقيقي
- ✅ DoD: subscription نشط في `SubscriptionRecord`

### [19] Full Control Tower (Custom) ⏱ بعد 5 paid customers
- لا تفتح هذي القناة قبل 5 paid pilots ناجحة
- ✅ DoD: 1 enterprise lead في Negotiation Engine

### [20] WhatsApp Business API Cloud ⏱ متى ما توفر CR + Meta Business Manager
- اربط Meta Business Manager بحسابك التجاري
- احصل على `WHATSAPP_PHONE_NUMBER_ID` + `ACCESS_TOKEN`
- اقلب `WHATSAPP_ALLOW_INTERNAL_SEND=true` **فقط** بعد:
  - أول Proof Pack مُسلَّم
  - موافقة Compliance review
- ✅ DoD: internal team brief يصل عبر WhatsApp

### [21] Live Charge Cutover ⏱ بعد Proof Pack مُسلَّم
- في Moyasar: انتقل من sandbox إلى live keys
- اقلب `MOYASAR_ALLOW_LIVE_CHARGE=true` **فقط** بعد:
  - استلام أول دفعة manual ناجحة
  - موافقة Legal review
- ✅ DoD: subscription auto-renew يعمل

---

## ❌ ما لن أفعله أبداً (لحمايتك)

| الفعل | السبب |
|---|---|
| Cold WhatsApp مجموعات | غرامة 5M SAR (PDPL) + suspension Meta |
| LinkedIn auto-DM | حظر فوري + ToS violation |
| Email blast بدون consent | PDPL violation |
| شراء قائمة جوالات | غير قانوني |
| "نضمن نتائج" في marketing | فقدان ثقة + كذب |
| Auto-charge قبل Proof | يحرق سمعة الـ brand |

**هذي ليست محدودية تقنية — هذي حماية لـ brand + المال + الحرية القانونية.**

---

## 📊 KPIs أسبوعية للمتابعة

اعرضها كل خميس مع نفسك (15 دقيقة):

```bash
curl https://YOUR-URL/api/v1/observability/quality?days=7
curl https://YOUR-URL/api/v1/observability/costs/summary?days=7
curl https://YOUR-URL/api/v1/observability/unsafe/summary?days=7
curl https://YOUR-URL/api/v1/daily-ops/history?limit=28
```

| Metric | Target Week 1 | Target Week 4 |
|---|---|---|
| Outreach manual | 30 | 100+ |
| Reply rate | 10% | 20% |
| Diagnostic calls | 2-3 | 6-8 |
| Pilot offers | 1-2 | 4-6 |
| Pilot paid | 1 | 3-5 |
| Proof Packs delivered | 1 | 3 |
| MRR | 0 | 2,999+ |
| Unsafe actions executed | **0** | **0** (دائماً) |
| AI cost | ≤ 200 SAR | ≤ 800 SAR |

---

## 🆘 إذا تعطّلت

1. **Build fails:** `docs/RAILWAY_ONE_CLICK.md §Troubleshooting`
2. **API down:** `docs/RUNBOOK.md §4 Incident Playbook`
3. **First customer angry:** `docs/RUNBOOK.md §5 Escalation Matrix`
4. **رفض Pilot:** `docs/READY_OUTREACH_MESSAGES.md` Email 02 (Diagnostic recap)
5. **سؤال قانوني:** اوقف فوراً + استشر محامي PDPL

---

## ✅ Final Checklist قبل البدء

- [ ] قرأت `docs/LAUNCH_DAY_CHECKLIST.md` كاملاً
- [ ] قرأت `docs/RUNBOOK.md` (الـ 4 daily windows)
- [ ] قرأت `docs/OUTREACH_PLAYBOOK.md` (sections 5-7)
- [ ] قرأت `docs/FIRST_PILOT_INTAKE.md`
- [ ] فهمت لماذا 8 live-action gates **false** (PDPL + ToS)
- [ ] فهمت لماذا outreach manual فقط (لا automation)
- [ ] جاهز للبند [1] الآن

---

## 🎯 السطر الأخير

**الكود + الوثائق + الأدوات = جاهزة 100%.**

عندك 21 بند هنا. المطلوب الإنساني الفعلي = ~15 ساعة موزّعة على 14 يوم
لتصل إلى **أول 499 SAR + أول Proof Pack مُسلَّم**.

ابدأ بالبند **[1]** الآن. الباقي يتبعه.

كل سؤال تقني → اقرأ الوثائق `docs/*.md`. كل سؤال تجاري → ارجع لـ
`docs/OUTREACH_PLAYBOOK.md` و `docs/FIRST_PILOT_INTAKE.md`.

**يوماً موفقاً.**
