# Dealix — سكربت اكتشاف الألم السريع · Rapid Pain Discovery

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `SALES_MOTIONS.md` · `OFFER_MATRIX.md` · `OBJECTION_ENGINE.md` · `../sales/DISCOVERY_SCRIPT.md` · `../29_sales_os/DISCOVERY_CALL_SCRIPT.md`

---

## الغرض · Purpose

هذا **طبقة اكتشاف سريعة (rapid-discovery layer)** — سبعة أسئلة تكشف الألم خلال محادثة قصيرة أو رسالة أولى. الإطار هنا مختلف عن سكربتات المكالمة الكاملة: لا تأهيل عميق، لا عرض، فقط تحديد سريع لما إذا كان هناك ألم حقيقي ولأي حرف من SOAEN ينتمي.

This is a rapid-discovery layer — seven questions that surface pain in a short conversation or a first message. The framing differs from the fuller call scripts: no deep qualification, no pitch, just a fast read on whether real pain exists and which SOAEN letter it belongs to.

للسكربتات الكاملة راجع [`../sales/DISCOVERY_SCRIPT.md`](../sales/DISCOVERY_SCRIPT.md) و[`../29_sales_os/DISCOVERY_CALL_SCRIPT.md`](../29_sales_os/DISCOVERY_CALL_SCRIPT.md).

---

## الأسئلة السبعة · The seven questions

| # | السؤال · Question | يكشف · Reveals |
|---|---|---|
| 1 | من أين تأتي الـleads عندك؟ · Where do your leads come from? | Source — المصدر |
| 2 | كم lead يدخل أسبوعياً؟ · How many leads per week? | حجم العملية · workflow volume |
| 3 | من يردّ أولاً؟ · Who replies first? | Owner — المالك |
| 4 | أين تسجّل الردود؟ · Where do you record replies? | Evidence — الدليل |
| 5 | كيف تعرف من يحتاج متابعة؟ · How do you know who needs follow-up? | Next Action — الخطوة التالية |
| 6 | هل تستطيع إثبات ما حدث بعد الحملة للعميل/الإدارة؟ · Can you prove to the client what happened after the campaign? | Evidence + Approval |
| 7 | لو أصلحنا سير عمل واحداً، أيها تختار؟ · If we fixed one workflow, which would you pick? | نقطة دخول العرض · offer entry point |

اطرح الأسئلة بالترتيب. لا تشرح بينها. السؤال 7 يحدّد نطاق التشخيص الأول.

Ask in order. Do not explain between questions. Question 7 defines the scope of the first diagnostic.

---

## منطق التأهيل · Qualify logic

**القاعدة الأساسية:** إذا لم يملك العميل إجابات على الأسئلة 3–6، فهذا **ليس فشلاً في المحادثة — هذا هو ألم Dealix نفسه.**

The core rule: if the prospect has no answers to questions 3–6, that is not a failed conversation — that is the Dealix value itself.

الرد المعتمد عند غياب الإجابات:

> "هذا بالضبط ما يكشفه أول Proof Pack." — "This is exactly what the first Proof Pack reveals."

لا تعالج غياب الإجابة كاعتراض. عالجه كإشارة دخول واضحة إلى `free_mini_diagnostic` بعنوان تموضع "10-Lead Follow-up Audit" — راجع [`OFFER_MATRIX.md`](OFFER_MATRIX.md).

Do not treat a missing answer as an objection. Treat it as a clear entry signal into `free_mini_diagnostic`.

---

## منطق الاستبعاد · Disqualify logic

استبعد العميل — أو أوقف المحادثة — في أي من الحالات التالية:

Disqualify the prospect, or stop the conversation, in any of these cases:

- **لا ميزانية ولا نية إنفاق.** Dealix خدمة مدفوعة بعد التشخيص المجاني؛ لا متابعة بلا نية شراء.
  No budget and no intent to spend.
- **لا مالك للعملية.** إذا لم يوجد شخص واحد مسؤول، فلا توجد عملية لتشغيلها بعد.
  No owner — nobody accountable means there is no workflow to operate yet.
- **لا leads أصلاً.** Dealix يشغّل طبقة ما بعد الـlead؛ لا يولّد الطلب الأوّلي.
  No leads at all — Dealix runs the post-lead layer, it does not generate primary demand.
- **يريد إرسالاً جماعياً أو spam.** يتعارض مع `no_cold_whatsapp` و`no_live_send`.
  Wants spam or bulk blasting.
- **يريد scraping أو قوائم مشتراة.** يتعارض مع `no_scraping` و`no_unconsented_data`.
  Wants scraping or purchased lists.
- **يريد ضمان ROI أو نسبة تحويل رقمية.** يتعارض مع `no_unverified_outcomes`؛ Dealix يقدّم فرصاً مُثبتة بأدلة، لا أرقاماً مضمونة.
  Wants guaranteed ROI or a guaranteed conversion rate.

في حالات الاستبعاد المتعلقة بـ scraping أو الإرسال البارد، الرد يكون توضيحياً وحازماً — لا اعتذارياً. هذه حدود منتج، لا قيود تفاوض.

For scraping or cold-send disqualifications, the response is clear and firm — these are product boundaries, not negotiation limits.

---

## بعد السكربت · After the script

| النتيجة · Outcome | الخطوة التالية · Next step |
|---|---|
| ألم واضح + مالك + leads · clear pain + owner + leads | وجّه إلى `free_mini_diagnostic` · route to the free mini diagnostic |
| ألم واضح لكن لا إجابات · clear pain, no answers | استخدم رد "Proof Pack" وأغلِق على التشخيص · use the Proof Pack line and close on the diagnostic |
| حالة استبعاد · disqualify case | أنهِ المحادثة بأدب، لا متابعة · close politely, no follow-up |

راجع [`OBJECTION_ENGINE.md`](OBJECTION_ENGINE.md) للاعتراضات التي قد تظهر أثناء الأسئلة.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
