# Dealix — ماكينة الاعتراضات · Objection Engine

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `DISCOVERY_SCRIPT.md` · `DEALIX_STANDARD.md` · `OFFER_MATRIX.md` · `../sales-kit/dealix_objection_handler.md` · `../OBJECTION_HANDLING_V6.md`

---

## الغرض · Purpose

هذه الوثيقة **طبقة تأطير (framing layer)**، وليست مكتبة ردود خام. كل اعتراض يُعالَج كثلاثية: **اعتراض ← رد ← أصل محتوى / دليل (objection → response → content/proof asset)**. الفكرة أن كل اعتراض متكرر يجب أن يُنتج أصلاً قابلاً لإعادة الاستخدام — منشوراً، صفحة، أو سياسة — بدلاً من رد شفهي يُنسى.

This document is a framing layer, not a raw rebuttal library. Each objection is handled as a triple: objection → response → content/proof asset. The idea is that every recurring objection should produce a reusable asset — a post, a page, or a policy — rather than a verbal answer that gets forgotten.

لمكتبة الردود الخام راجع [`../sales-kit/dealix_objection_handler.md`](../sales-kit/dealix_objection_handler.md) و[`../OBJECTION_HANDLING_V6.md`](../OBJECTION_HANDLING_V6.md).

For the raw rebuttal library, see the sales-kit objection handler and the V6 objection handling doc.

---

## الاعتراضات الأساسية الأربعة · The four core objections

### 1) "عندنا CRM" · "We have a CRM"

**الموقف · Situation:** العميل يعتقد أن وجود CRM يعني أن مشكلة ما بعد الـlead محلولة. الواقع: الـCRM يخزّن، لكنه لا يحرّك.

**الرد · Response:** الـCRM يخزّن البيانات؛ Dealix يحرّكها — من يحتاج متابعة الآن، ما الرسالة التالية، أين الدليل. الـCRM يجيب جزئياً عن O (المالك)، لكن A (الموافقة) وE (الدليل) وN (الخطوة التالية) غالباً مفقودة — راجع [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md).

The CRM stores data; Dealix moves it — who needs follow-up now, what the next message is, where the evidence is. A CRM answers part of O; A, E, and N are usually missing.

**أصل المحتوى / الدليل · Content/proof asset:** منشور بعنوان "الـCRM يخزّن البيانات، لكن من يملك الخطوة التالية؟" — "CRM stores data, but who owns the next action?"

---

### 2) "عندنا وكالة" · "We have an agency"

**الموقف · Situation:** العميل يفترض أن الوكالة تغطّي كل شيء بعد الحملة. الواقع: الوكالة تجلب الاهتمام، لكنها نادراً ما تثبت ما حدث بعد الـlead.

**الرد · Response:** الوكالة تجلب الاهتمام؛ Dealix يثبت ماذا حدث بعد ذلك. لا تنافس بين الاثنين — Dealix يشغّل طبقة ما بعد الـlead التي لا تغطّيها الوكالة. هذا هو منطق حركة Agency Proof Pilot في [`SALES_MOTIONS.md`](SALES_MOTIONS.md).

The agency brings the interest; Dealix proves what happened after. The two do not compete — Dealix runs the post-lead layer the agency does not cover.

**أصل المحتوى / الدليل · Content/proof asset:** منشور بعنوان "وجود وكالة لا يحلّ مشكلة ما بعد الـlead." — "Having an agency doesn't solve the post-lead problem."

---

### 3) "السعر مرتفع" · "The price is high"

**الموقف · Situation:** العميل يرى الرقم كبيراً مقارنةً بثقته الحالية في النتيجة.

**الرد · Response:** لا تخفّض السعر — قلّص النطاق. ابدأ بـ10 leads فقط عبر `free_mini_diagnostic` ثم `revenue_proof_sprint_499`. العميل يدفع مقابل دليل ملموس على نطاق صغير قبل أي التزام أكبر. التسعير يبقى شفّافاً كما هو منشور في [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) — لا خصم مرتجل (`no_hidden_pricing`).

Do not cut the price — cut the scope. Start with 10 leads only. The customer pays for concrete evidence on a small scope before any larger commitment.

**أصل المحتوى / الدليل · Content/proof asset:** منشور بعنوان "لماذا تبدأ بمراجعة 10 leads؟" — "Why start with a 10-lead audit?"

---

### 4) "عندنا AI داخلي" · "We have internal AI"

**الموقف · Situation:** العميل بنى أو اشترى أدوات AI داخلية ويرى Dealix تكراراً لها.

**الرد · Response:** Dealix لا ينافس الـAI الداخلي — يضيف حوله المصدر والموافقة والدليل وتتبّع القرار. الـAI الداخلي قد يولّد إجراءً، لكنه نادراً ما يسجّل من وافق عليه، وبأي دليل، وما القرار الناتج. Dealix يغلّف الـAI الداخلي بطبقة SOAEN.

Dealix does not compete with internal AI — it adds source, approval, evidence, and decision tracking around it. Internal AI may generate an action, but it rarely records who approved it, on what evidence, and what decision followed.

**أصل المحتوى / الدليل · Content/proof asset:** سياسة بعنوان "سياسة موافقة الذكاء الاصطناعي — نسخة مبسّطة" — "AI Approval Policy Lite."

---

## جدول الثلاثيات · Objection triple summary

| الاعتراض · Objection | جوهر الرد · Response core | الأصل المنتَج · Asset produced |
|---|---|---|
| عندنا CRM · We have a CRM | الـCRM يخزّن، Dealix يحرّك · CRM stores, Dealix moves | منشور: من يملك الخطوة التالية؟ |
| عندنا وكالة · We have an agency | الوكالة تجلب، Dealix يثبت · agency brings, Dealix proves | منشور: الوكالة لا تحلّ ما بعد الـlead |
| السعر مرتفع · Price is high | قلّص النطاق لا السعر · cut scope, not price | منشور: لماذا تبدأ بـ10 leads؟ |
| عندنا AI داخلي · We have internal AI | Dealix يغلّف لا ينافس · Dealix wraps, not competes | سياسة: AI Approval Policy Lite |

---

## قاعدة التشغيل · Operating rule

لا اعتراض يُغلَق شفهياً فقط. كل مرة يتكرّر اعتراض، تأكّد أن أصله موجود ومحدَّث. الأصول تُنشَر وفق [`../MARKETING_AND_CONTENT_SYSTEM.md`](../MARKETING_AND_CONTENT_SYSTEM.md). أي رد يَعِد بنتيجة رقمية مضمونة مرفوض — استبدله بـ"فرص مُثبتة بأدلة".

No objection is closed verbally only. Every time an objection recurs, confirm its asset exists and is current. Any response that promises a guaranteed numeric result is rejected — replace it with "evidenced opportunities".

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
