# سكربت تشخيص الـ 30 دقيقة / 30-Min Diagnostic Script

> ما يقوله المؤسس + كيف يصنّف العميل + متى يقدّم Pilot.
> What the founder says + how to score the prospect + when to offer the Pilot.

**Owner:** Founder
**Hard rule:** No promises of guaranteed revenue/ranking. No live
sends during or after this call.

---

## ⏱ الجدول الزمني / Timeline

| دقيقة / Minute | المرحلة / Phase |
|---|---|
| 0–5 | تعارف + سياق العميل / Intro + customer context |
| 5–20 | أنت تقرأ الـ Diagnostic + يصحّح العميل الفجوات / Founder reads the brief, customer corrects |
| 20–25 | توضيح الـ Pilot (٧ أيّام، 499 ريال) / Explain the 7-day Pilot |
| 25–30 | قرار العميل + الخطوة التالية / Customer decision + next step |

---

## 📜 السكربت (عربيّ أساسيّ) / Script (Arabic primary)

### الافتتاح

> "السلام عليكم [الاسم]. أشكركم على وقتكم. الجلسة دقيقة 30 لا أكثر.
> هدفنا اليوم: أعرض على [اسم الشركة] قراءة سريعة لقمعكم التجاريّ، تقولوني
> أين أصبت وأين أخطأت، ثمّ نقرّر معاً هل الـ Growth Starter Pilot يناسبكم
> أم لا. لا أرسل لكم شيئاً اليوم — فقط تقييم. هل نبدأ؟"

### عرض الـ Diagnostic

اقرأ المسوّدة المُولّدة من `python scripts/dealix_diagnostic.py` بصوت عالٍ، ثمّ:

> "هذي قراءتي الأوّليّة. أتوقّع نصفها صحيح ونصفها يحتاج تصحيح منكم.
> الفجوة #1 أراها كذا: [قراءة]. هل هذا فعلاً ما يحدث؟"

> "الفجوة #2: [قراءة]. هل توافقون؟"

> "الفجوة #3: [قراءة]. هل توافقون؟"

### عرض Pilot

> "بناء على ما رأيتم، أقترح Pilot 7 أيّام. الباقة: **[اسم الباقة بالعربيّ]**.
> السعر التعريفيّ: 499 ريال — ثابت حتّى العميل الخامس.
> ما يحدث في الـ 7 أيّام:
> - 10 فرص مؤهَّلة جاهزة للمتابعة
> - مسوّدات عربيّة لكلّ فرصة (لا إرسال آليّ — أنتم تراجعون كلّ مسوّدة)
> - خطّة متابعة 72 ساعة
> - Proof Pack ثنائيّ اللغة موقَّع منكم
>
> ما لن نفعله:
> - لا cold WhatsApp ولا cold email
> - لا scraping
> - لا التزام بأرقام محدّدة — التزام بالعمل والـ Proof Pack"

### قرار العميل

> "هل ترون أنّ الـ Pilot يستحقّ تجربة؟ ثلاثة خيارات:
> ١. مهتمّون — أرسل فاتورة Moyasar test mode، تدفعون، ونبدأ.
> ٢. نحتاج جلسة 30 دقيقة قبل القرار — نحدّد موعد آخر.
> ٣. غير مناسب الآن — نتواصل بعد 90 يوم بمحتوى ذو قيمة (لا spam)."

---

## 📜 Script (English secondary)

### Opening

> "Thanks for the time. The session is exactly 30 minutes.
> Today's goal: I read [Company]'s pipeline diagnostic, you tell me
> where I'm right and wrong, then together we decide if the Growth
> Starter Pilot fits. I'm not sending anything today — just an
> assessment. Shall we start?"

### Diagnostic delivery

Read the generated brief out loud, then:

> "That's my initial read. I expect half right, half needs your
> correction.
> Gap #1 I see is: [read]. Is that actually what's happening?"

> "Gap #2: [read]. Do you agree?"

> "Gap #3: [read]. Do you agree?"

### Pilot offer

> "Based on what you've described, I suggest a 7-day Pilot. The
> bundle: **[bundle name]**.
> Introductory price: 499 SAR — locked until customer #5.
> What happens in 7 days:
> - 10 qualified opportunities ready for follow-up
> - Arabic drafts per opportunity (no auto-send — you approve each)
> - 72-hour follow-up plan
> - Bilingual Proof Pack signed by you
>
> What we will NOT do:
> - No cold WhatsApp / cold email
> - No scraping
> - No revenue/ranking commitment — only the work + Proof Pack"

### Customer decision

> "Does the Pilot feel worth trying? Three options:
> 1. Interested — I send a Moyasar test-mode invoice; you pay; we start.
> 2. Need a 30-min call first — let's schedule it.
> 3. Not now — I re-engage in 90 days with a useful content piece (no spam)."

---

## 🎯 Qualification rubric / معايير التأهيل

| معيار / Criterion | Score | Reason |
|---|---|---|
| Saudi B2B (matches ICP) | +20 | Dealix focus |
| 5–50 employees | +15 | within Pilot scope |
| Has existing prospect/lead flow | +20 | Pilot can deliver Day 1 |
| Founder is the buyer | +15 | reduces sales-cycle friction |
| Pain matches a top-5 service | +15 | clear service to apply |
| Decided budget for "growth experiment" | +10 | 499 SAR fits |
| No expectation of guaranteed outcome | +5 | aligns with hard rule |

**Pass threshold: 80+** → present Pilot offer.
**60–79** → present free Diagnostic only; defer Pilot until proof.
**< 60** → out of scope; recommend an alternative; archive politely.

---

## 🚫 Disqualification reasons (and how to phrase the no)

| Pattern | Phrase |
|---|---|
| Wants guaranteed sales numbers | "نحن نلتزم بالعمل والمسوّدات والمتابعة، لا بالأرقام. هذا قرار سياسة، ليس قابل للتفاوض." |
| Wants you to send cold messages | "Dealix لا يرسل cold messages. ما نقوم به: مسوّدات تراجعونها وترسلونها بأنفسكم بعد الموافقة." |
| Wants ranked organic content (SEO without proof) | "SEO يحتاج نتائج 90+ يوم. لا أبدأ خدمة سيو بدون pilot أوّلي يثبت العائد." |
| Wants scraping / purchased lists | "سياسة Dealix الثابتة: لا scraping ولا قوائم مشتراة. نلتزم بـ PDPL." |
| < 5 employees / pre-revenue | "الـ Pilot مناسب للشركات اللي عندها lead flow. لو ما عندكم بعد، أوصي تركّزون على Diagnostic مجاني فقط." |

---

## 🎬 الخطوة التالية بعد كلّ خيار / Next step per outcome

### إذا قال "نعم، أرسل الفاتورة":

```bash
# 1. تأكّد مفتاح Moyasar test mode:
python -c "import os; k=os.getenv('MOYASAR_SECRET_KEY','?'); print('OK' if k.startswith('sk_test_') else 'STOP — key is sk_live_')"

# 2. اصنع الفاتورة:
python scripts/dealix_invoice.py \
  --email <customer-email> \
  --amount-sar 499 \
  --description "Dealix Growth Starter Pilot — 7 days"

# 3. تقدّم في journey:
curl -X POST http://localhost:8000/api/v1/customer-loop/journey/advance \
  -d '{"current_state":"diagnostic_sent","target_state":"pilot_offered","customer_handle":"<slug>"}'

# 4. أرسل رابط الفاتورة يدويّاً (واتساب بعد opt-in / إيميل).

# 5. تقدّم journey: pilot_offered → payment_pending
```

### إذا قال "نحتاج جلسة ثانية":

- احجز موعد جديد
- اطلب 3 معلومات إضافيّة قبل الجلسة الثانية: hard numbers من قمعهم الحاليّ
- ابقَ في `diagnostic_sent` state؛ لا تتقدّم

### إذا قال "غير مناسب الآن":

- اشكره
- ضعه في nurture لمدّة 90 يوم
- سجّل ProofEvent: `risk_blocked` (لا، هذا ليس risk؛ سجّل في NurtureList بدلاً)
- ادخل التفاصيل في Decision Pack §S6 (لو يستحقّ تتبّع)

---

## 📝 ملاحظات نهائيّة / Final notes

- **30 دقيقة فقط.** لا تمدّد لو وافق العميل — احتفظ بالضغط الإيجابيّ.
- **عربيّ أوّلاً.** حتّى لو العميل يفضّل الإنجليزيّة، ابدأ بالعربيّة وانتقل بناء على إشارتهم.
- **لا تُسوّق الـ Roadmap.** عرض الباقات الحاليّة فقط (5 customer-facing).
- **سجّل ProofEvent لكلّ Diagnostic** — حتّى لو فشل، الـ event يفيد تعلّم الـ pricing وحجم السوق.

— First 3 Diagnostic Script v1.0 · 2026-05-05 · Dealix
