# Dealix — Affiliate Governance Spec — مواصفة حوكمة المسوّقين بالعمولة
<!-- PHASE 13 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **حالة المستند — Status: NOT-YET-LAUNCHED.** هذا **مواصفة موثَّقة
> فقط**. لا يوجد محرّك مسوّقين تشغيلي، ولا صرف عمولات حيّ، ولا تسجيل
> ذاتي. أي تفعيل لاحق يبدأ يدوياً وبموافقة المؤسس. This is a
> documented spec only — no live affiliate engine, no live payouts.
>
> **قاعدة ذهبية:** لا صرف عمولة قبل دفع فاتورة العميل. لا استثناء.
> **No payout before the customer invoice is paid. No exception.**

---

## 1. لماذا مواصفة قبل البناء / Why a spec before code

محرّك المسوّقين يُضخّم التوزيع — ويُضخّم المخاطر بنفس القدر. مسوّق
واحد يكتب "نضمن لكم مبيعات" يُلحق ضرراً يفوق قيمته. لذلك نكتب الحوكمة
أولاً: من يُسمح له، ماذا يقول، كيف يُفصِح، ومتى يُدفع له. البناء يأتي
بعد ظهور طلب حقيقي. الكود الحالي
`auto_client_acquisition/sales_os/partner_engine.py` يحتوي **حكم
أهلية فقط** — لا مسار صرف.

---

## 2. البداية — 5 إلى 10 أشخاص موثوقين فقط

| القاعدة / Rule | التفاصيل / Detail |
|---|---|
| العدد الأولي | 5–10 أشخاص موثوقين فقط — لا تسجيل عام |
| المصدر | شبكة المؤسس المباشرة، علاقة قائمة |
| الموافقة | كل مسوّق يُعتمد يدوياً من المؤسس |
| الرسائل | لا يستخدم المسوّق إلا رسائل معتمدة مسبقاً |
| المراجعة | كل إحالة تُراجَع يدوياً قبل احتسابها |

> لا توسّع إلى ما بعد 10 مسوّقين قبل مراجعة أداء كاملة وإثبات أن
> الحوكمة صمدت.

---

## 3. شرائح العمولة / Commission tiers (spec)

| الشريحة / Tier | الحدث / Trigger | العمولة / Commission |
|---|---|---|
| Referral | إحالة دافئة أغلقت Pilot 499 SAR | نسبة ثابتة من قيمة الـ Pilot |
| Implementation | شريك ينفّذ التسليم لعميله | حصة من إيراد العميل |
| Co-selling / Agency | راجع سلّم العروض الدرجة 5 | 15–30% rev-share |

> النسب الدقيقة وآلية الدفع مصدرها سلّم العروض
> [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
> و[`docs/partners/PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md).
> هذا المستند لا يخترع أرقاماً.

---

## 4. الممارسات الممنوعة / Forbidden practices

ممنوع على أي مسوّق، تحت طائلة إنهاء الاتفاق فوراً:

- ❌ ادّعاء ROI أو أرقام مبيعات مضمونة ("نضمن مبيعات").
- ❌ spam أو إرسال جماعي.
- ❌ cold WhatsApp / واتساب بارد.
- ❌ أتمتة LinkedIn أو scraping أو قوائم مشتراة.
- ❌ إثبات مزيّف أو حالة عميل بلا دليل.
- ❌ الترويج دون إفصاح واضح عن العلاقة التجارية.
- ❌ التحدّث باسم Dealix أو الالتزام بما لا تلتزم به Dealix.

---

## 5. الإفصاح — واضح وبارز / Clear-and-conspicuous disclosure

كل منشور أو رسالة من مسوّق يجب أن يحمل إفصاحاً **واضحاً وبارزاً**
(على نمط FTC) — قبل الرابط، لا في الهامش، لا مخفياً خلف "المزيد".

### نص الإفصاح الجاهز / Ready disclosure text

**عربي:**
> "إفصاح: أنا شريك مُحيل لـ Dealix وقد أحصل على عمولة إذا اشتركت عبر
> هذا الرابط. هذا لا يغيّر السعر عليك."

**English:**
> "Disclosure: I am a referral partner for Dealix and may earn a
> commission if you sign up through this link. This does not change the
> price you pay."

> الإفصاح إلزامي في كل قناة. منشور بلا إفصاح = خرق يوقف الأهلية.

---

## 6. القاعدة الصارمة — لا صرف قبل الدفع / The hard rule

> **لا تُصرف عمولة قبل أن تُدفع فاتورة العميل.**

هذه القاعدة ليست سياسة ورقية — يفرضها **حارس في الكود**:
`commission_eligible()` في
`auto_client_acquisition/sales_os/partner_engine.py`. الدالة تُرجع
`(eligible, reason)`:

- إذا `invoice_paid` ليست `True` → `(False, "no_payout_before_invoice_paid")`.
- إذا الشريك `white_label` و`completed_proof_packs < 3` →
  `(False, "white_label_requires_3_proof_packs")`.

الحارس نفسه يمنع شراكة white-label قبل **3 Proof Packs مكتملة**
(`WHITE_LABEL_MIN_PROOF_PACKS = 3`). لا يمكن تجاوز سياق فاشل في هذه
الدالة — الحارس صارم.

| الشرط / Condition | النتيجة / Verdict |
|---|---|
| الفاتورة غير مدفوعة | غير مؤهَّل — `no_payout_before_invoice_paid` |
| white-label + Proof Packs < 3 | غير مؤهَّل — `white_label_requires_3_proof_packs` |
| الفاتورة مدفوعة + الشروط مستوفاة | مؤهَّل — `eligible` |

> الوحدة `partner_engine.py` تُرجع **حكماً فقط** — لا تنفّذ صرفاً.
> أي صرف فعلي يدوي وبموافقة، ولا يُبنى قبل ظهور طلب حقيقي.

---

## 7. شروط التفعيل / Activation gate

لا يُفعَّل أي محرّك مسوّقين قبل:

1. إتمام ≥ 3 Proof Packs.
2. مراجعة قانونية للإفصاح ولاتفاقية المسوّق.
3. اختيار 5–10 أشخاص موثوقين باسمهم.
4. موافقة المؤسس الصريحة على إطلاق محدود.

---

*Affiliate Governance Spec v1.0 · 2026-05-17 · Dealix · NOT-YET-LAUNCHED.*

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
