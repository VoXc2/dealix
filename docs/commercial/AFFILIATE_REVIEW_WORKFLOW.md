# مسار مراجعة الأفلييت / Affiliate Review Workflow

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `../sales-kit/dealix_referral_program.md` · `../AGENCY_PARTNER_PROGRAM.md` · `PARTNER_ONBOARDING_KIT.md`

---

الأفلييت لا ينشر بحرّية. أي مادة تواصل قبل النشر تمر بمراجعة امتثال. هذه الوثيقة آلة حالة (state machine) واضحة: من تقديم المادة حتى استحقاق العمولة.

Affiliates do NOT publish freely. Any pre-publication copy passes a compliance review. This document is a clear state machine: from copy submission to commission eligibility.

---

## 1. آلة الحالة / State machine

```
affiliate_submits_copy
        │
        ▼
  compliance_review
        │
   ┌────┼─────────────┐
   ▼    ▼             ▼
approved  edit_required  blocked
   │         │            │
   │     (إعادة تقديم)   (نهاية المسار)
   │     (resubmit)      (end of path)
   ▼
tracking_link_issued
        │
        ▼
  lead_submitted
        │
        ▼
  lead_qualified
        │
        ▼
   invoice_paid
        │
        ▼
commission_eligible
```

---

## 2. وصف الحالات / State descriptions

| الحالة / State | الوصف / Description |
|---|---|
| `affiliate_submits_copy` | يقدّم الأفلييت مسودة المحتوى (منشور، مقال، بريد) قبل أي نشر. / Affiliate submits draft content (post, article, email) before any publishing. |
| `compliance_review` | يراجع فريق Dealix المادة مقابل الـ 11 لا-تنازل والإفصاح المطلوب. / Dealix reviews the copy against the 11 non-negotiables and the disclosure requirement. |
| `approved` | المادة متوافقة ويُسمح بنشرها كما هي. / Copy is compliant and may be published as-is. |
| `edit_required` | المادة تحتاج تعديلات محددة؛ يُعيد الأفلييت التقديم. / Copy needs specific edits; affiliate resubmits. |
| `blocked` | المادة تخالف لا-تنازلًا أساسيًا؛ تُرفض ولا يُصدَر رابط تتبّع. / Copy violates a core non-negotiable; rejected, no tracking link. |
| `tracking_link_issued` | بعد الاعتماد، يُصدَر رابط تتبّع منسوب للأفلييت. / After approval, a tracking link attributed to the affiliate is issued. |
| `lead_submitted` | دخل lead عبر رابط التتبّع. / A lead entered via the tracking link. |
| `lead_qualified` | تأكد فريق Dealix من وجود ميزانية ومالك قرار وبيانات. / Dealix confirmed budget, decision owner, and data. |
| `invoice_paid` | دفع العميل فاتورة فعلية. / The client paid an actual invoice. |
| `commission_eligible` | استوفيت كل بوابات العمولة؛ العمولة مؤهلة للصرف. / All commission gates met; commission is eligible for payout. |

`blocked` حالة نهائية لتلك المادة؛ يمكن للأفلييت تقديم مادة جديدة من البداية. / `blocked` is terminal for that copy; the affiliate may submit fresh copy from the start.

---

## 3. بوابات العمولة / Commission gates

لا تُصرف العمولة قبل تحقّق **كل** الشروط التالية مجتمعةً:

- `invoice_paid` = true — دفع العميل فاتورة فعلية. / the client paid an actual invoice.
- لا مشكلة استرداد / no refund issue — لا استرداد ولا نزاع مفتوح.
- الـ lead ليس مكرّرًا / the lead is not a duplicate — لا إحالة سابقة لنفس الجهة.
- المادة متوافقة / the copy is compliant — مرّت بحالة `approved`.
- الإفصاح موجود / a disclosure is present — إفصاح واضح ومرئي عن علاقة الأفلييت.

إذا تخلّف أي شرط واحد، تبقى الحالة دون `commission_eligible`. النِّسب والمبالغ مرجعها `../AGENCY_PARTNER_PROGRAM.md` ولا تُذكر هنا. / If any single gate fails, the state stays below `commission_eligible`. Rates and amounts are referenced in `../AGENCY_PARTNER_PROGRAM.md` and not stated here.

---

## 4. شرط الإفصاح / Disclosure requirement

محتوى الأفلييت يجب أن يُفصح بوضوح وبشكل مرئي عن علاقة الأفلييت. الإفصاح القصير أو المخفي غير مقبول.

Affiliate content must clearly and visibly disclose the affiliate relationship. Short or hidden disclosures are not acceptable.

**مقبول / Acceptable:**
- جملة إفصاح كاملة في أول المنشور أو المقال، بحجم خط المحتوى نفسه. / a full disclosure sentence at the top of the post or article, in the same font size as the body.
- مثال: «إفصاح: أنا شريك أفلييت لـ Dealix وقد أحصل على عمولة عند تحويل ناتج عن هذا المحتوى.» / "Disclosure: I am a Dealix affiliate and may earn a commission from a conversion resulting from this content."

**غير مقبول / Not acceptable:**
- إفصاح في الهامش السفلي بخط صغير. / a small-font footer disclosure.
- إفصاح مخفي خلف رابط أو زر «المزيد». / a disclosure hidden behind a link or a "more" button.
- اختصارات غامضة دون شرح. / vague abbreviations without explanation.

غياب الإفصاح المقبول ينقل المادة إلى `edit_required` أو `blocked`. / Absence of an acceptable disclosure moves copy to `edit_required` or `blocked`.

---

## 5. أسباب الانتقال إلى blocked / Reasons for blocked

تُرفض المادة مباشرةً إذا تضمّنت أيًّا مما يلي:

| السبب / Reason | اللا-تنازل / Non-negotiable |
|---|---|
| إثبات أو شهادة عميل غير حقيقية / fabricated proof or testimonial | `no_fake_proof` |
| رقم نتيجة أو ROI كحقيقة مضمونة / a guaranteed outcome or ROI number as fact | `no_unverified_outcomes` |
| وصف واتساب بارد كخدمة / describing cold WhatsApp as a service | `no_cold_whatsapp` |
| وصف scraping أو قوائم مشتراة كخدمة / describing scraping or purchased lists as a service | `no_scraping` |
| إخفاء أو تصغير الإفصاح / hiding or shrinking the disclosure | `no_hidden_pricing` (روح القاعدة / spirit) |

النتائج تُوصَف دائمًا بأنها «تقديرية» أو «نمط آمن الحالة»، لا حقائق. / Outcomes are always described as "estimated" or "case-safe pattern", never facts.

---

## 6. ملخص المسؤوليات / Responsibility summary

- **الأفلييت / Affiliate:** يقدّم مادة متوافقة، يضيف الإفصاح، لا ينشر قبل `approved`.
- **مراجع الامتثال / Compliance reviewer:** يقيّم المادة، يصنّفها، يوثّق السبب عند `edit_required` أو `blocked`.
- **عمليات Dealix / Dealix ops:** تصدر رابط التتبّع، تتحقق من بوابات العمولة، توثّق القرار (`no_silent_failures`, `no_unaudited_changes`).

كل قرار مراجعة يُسجَّل مع سبب مكتوب. / Every review decision is logged with a written reason.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
