# Dealix — Distribution Sprint — سبرنت التوزيع 14 يوماً
<!-- PHASE 13 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** السبرنت يُثبت أن القمع يتحرّك بيد المؤسس، لا أن
> السوق يضمن نتيجة. كل فعل خارجي مسوّدة تُراجَع قبل الإرسال. لا واتساب
> بارد، لا scraping، لا أرقام مضمونة.
>
> **Golden rule:** the sprint proves the funnel moves under the founder's
> hand — not that the market guarantees an outcome. Every external action
> is a draft reviewed before sending. No cold WhatsApp, no scraping, no
> guaranteed numbers.

> **الموضع — Positioning.** هذا السبرنت هو **الأسبوعان الافتتاحيان**
> من [`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md)
> (المرحلة 1 + بداية المرحلة 2). يُشغّل قمع الـ12 مرحلة المعرّف في
> [`docs/DISTRIBUTION_OS.md`](../DISTRIBUTION_OS.md). الأرقام المذكورة
> أهداف تشغيلية وتقديرات — ليست ضمانات.

---

## نظرة عامة / Overview

| الأسبوع / Week | الهدف / Goal | مرحلة القمع / Funnel stage |
|---|---|---|
| الأسبوع 1 (أيام 1–7) | إثبات الحركة على 10 أهداف وإغلاق أول pilot | `target` → `proof_pack` |
| الأسبوع 2 (أيام 8–14) | تكرار على 50 هدفاً وتضييق الاستهداف | `target` → `referral_partner_loop` |

---

## الأسبوع 1 / Week 1

### اليوم 1 — إعداد War Room / Day 1 — War Room setup

**عربي.** افتح طاولة War Room الواحدة (القمع كاملاً) واربط مولّد لوحة
النتائج. لا تواصل اليوم — فقط بنية.

- جدول War Room: عمود لكل مرحلة من المراحل الـ12.
- تأكّد أن `scripts/war_room_scorecard.py` يقرأ تيار الأحداث ويبني صف اليوم.
- افتح [`docs/ops/daily_scorecard.md`](../ops/daily_scorecard.md) وانسخ بلوك "Day N".
- اكتب 10 أهداف مبدئية: مدينة، قطاع، صانع قرار لكلٍّ (مرحلة `target`).

**English.** Open the single War Room table (the full funnel) and wire
the scorecard generator. No outreach today — structure only.

### اليوم 2 — أول 10 لمسات يدوية / Day 2 — first 10 manual touches

التوزيع: **5 رسائل دافئة / 3 إيميل / 1 LinkedIn / 1 محادثة شريك**.

- لكل هدف: اكتب فرضية ألم ملموسة واحدة (مرحلة `pain_hypothesis`).
- صُغ كل رسالة مسوّدةً من قوالب
  [`docs/FIRST_10_WARM_MESSAGES_AR_EN.md`](../FIRST_10_WARM_MESSAGES_AR_EN.md).
- كل مسوّدة تمرّ بموافقة المؤسس قبل الإرسال — `message.drafted` →
  `message.approved` → `message.sent`.
- الرسائل تُرسل عبر القناة التي توجد فيها العلاقة أصلاً. لا واتساب
  بارد ولا أتمتة LinkedIn.

> رسالة LinkedIn الواحدة تُرسَل يدوياً من حساب المؤسس — ليست أتمتة.

### اليوم 3 — أصول الإثبات / Day 3 — proof assets

- لكل هدف ردّ: أرفق أصل الإثبات الذي يُغلق المحادثة — Proof Pack
  نموذجي أو one-pager (مرحلة `proof_asset`).
- أعد استخدام الأصول المعتمدة فقط؛ لا تبنِ 20 صفحة جديدة.
- صنّف الردود وحضّر متابعة واحدة لكلٍّ (مرحلة `conversation`).

### اليوم 4 — يوم الديمو / Day 4 — demo day

- شغّل ديمو الإغلاق 12 دقيقة لكل من حجز موعداً —
  [`DEMO_12MIN_SCRIPT.md`](DEMO_12MIN_SCRIPT.md).
- اختم كل ديمو بطلب الـ pilot. لا جولة منتج كاملة.
- سجّل `meeting.held` لكل ديمو مكتمل.

### اليوم 5 — النطاق + الفاتورة / Day 5 — scope + invoice

- أرسل نطاقاً مكتوباً لكل عميل مهتمّ: سير عمل واحد أو 10 فرص
  (مرحلة `pilot_diagnostic`). النطاق يُراجَع قبل الإرسال.
- عند الموافقة: أرسل فاتورة الدرجة 1 — **499 SAR** — يدوياً بعد الموافقة.
  لا سحب مباشر للبطاقة (مرحلة `payment_commitment`).
- إذا تردّد العميل على السعر: قلّص النطاق، لا تخصم.

### الأيام 6–7 — التسليم السريع / Days 6-7 — fast delivery

- سلّم أول مخرَج خلال **24–48 ساعة** من الدفع (مرحلة `delivery`).
- جمّع Proof Pack من
  [`docs/templates/PROOF_PACK_TEMPLATE.md`](../templates/PROOF_PACK_TEMPLATE.md)
  (مرحلة `proof_pack`). يُعتمد قبل المشاركة.
- Proof Pack بلا قيمة قابلة للقياس وخطوة تالية = غير مكتمل.

---

## الأسبوع 2 / Week 2 — التكرار والتضييق

**عربي.** كرّر دورة الأيام 1–7 على **50 هدفاً** بدل 10. الهدف ليس
المزيد من الحجم فقط — بل **تضييق الاستهداف** بناءً على ما ردّ فعلاً.

- وسّع جدول War Room إلى 50 صفاً (مرحلة `target`).
- بعد منتصف الأسبوع: راجع `reply_rate` حسب القطاع. أوقف القطاع الأضعف،
  ضاعف على الأقوى.
- شغّل عرض الترقية لأي عميل سلّمنا له Proof Pack
  (مرحلة `sprint_retainer`) — راجع سلّم الإغلاق في
  [`docs/DISTRIBUTION_OS.md`](../DISTRIBUTION_OS.md).
- اطلب إحالة واحدة وافتح محادثة شريك واحدة (مرحلة `referral_partner_loop`)
  — راجع [`AGENCY_WEDGE_ONEPAGER.md`](AGENCY_WEDGE_ONEPAGER.md).

**English.** Repeat the Day 1-7 cycle on 50 targets, then narrow.
The goal is not raw volume — it is sharper targeting based on what
actually replied. Kill the weakest segment, double down on the strongest.

---

## أهداف السبرنت / Sprint targets (estimates, not guarantees)

| المقياس / Metric | اليوم 7 | اليوم 14 |
|---|---|---|
| Targets in War Room | 10 | 50 |
| Messages sent (approved) | 10 | 50 |
| Demos held | 1–2 | 4–6 |
| Pilots closed | 0–1 | 1–2 |
| Proof Packs delivered | 0–1 | 1–2 |
| Partner conversations | 1 | 2 |

> هذه أهداف تشغيلية وتقديرات. الأرقام الفعلية تعتمد على السوق وجهد
> المؤسس. أي رقم لم يتحقق = `insufficient_data`.

---

*Distribution Sprint v1.0 · 2026-05-17 · Dealix.*

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
