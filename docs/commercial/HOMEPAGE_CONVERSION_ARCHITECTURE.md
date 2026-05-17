# Dealix — بنية تحويل الصفحة الرئيسية · Homepage Conversion Architecture

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `SALES_MOTIONS.md` · `DEALIX_STANDARD.md` · `../MARKETING_AND_CONTENT_SYSTEM.md` · `../../landing/`

---

## الغرض · Purpose

تصف هذه الوثيقة الصفحة الرئيسية كـ**مسار قرار (decision path)**، لا كشرح تقني. القارئ مدير أعمال سعودي يريد أن يعرف خلال دقيقة: ما المشكلة، كيف تُحَل، وما الخطوة التالية. لا نشرح النماذج ولا المعمارية على الصفحة الرئيسية.

This document describes the homepage as a decision path, not a tech explainer. The reader is a Saudi business decision-maker who needs to know within a minute: what the problem is, how it is solved, and what the next step is. We do not explain models or architecture on the homepage.

---

## 1) القسم البطل · Hero

**العنوان · Headline:**
- **عربي:** "Dealix يثبت ماذا يحدث بعد الـlead. حوّل المتابعة الفوضوية إلى قرارات إيراد موثّقة."
- **English:** "Dealix proves what happens after the lead. Turn chaotic follow-up into documented revenue decisions."

العنوان يذكر اسماً ملموساً (lead، متابعة، قرار) ولا يَعِد بأرقام. لا "نضاعف مبيعاتك" ولا "ذكاء اصطناعي يحوّل عملك".

The headline uses concrete nouns (lead, follow-up, decision) and promises no numbers.

---

## 2) نداءات الفعل · CTAs

ثلاثة نداءات فعل، مرتّبة من الأخف التزاماً إلى الأثقل:

| النداء · CTA | الالتزام · Commitment | السطح · Surface |
|---|---|---|
| احصل على درجة مخاطر · Get a Risk Score | منخفض جداً · very low | تشخيص مصغّر · `free_mini_diagnostic` |
| اطّلع على عيّنة Proof Pack · See a Sample Proof Pack | بلا التزام · none | عيّنة جاهزة · sample asset |
| احجز عرضاً 10 دقائق · Book a 10-minute demo | متوسط · medium | تدفّق qualify → proposal |

النداء الأساسي هو "درجة المخاطر" لأنه يفتح محادثة `free_mini_diagnostic` بأقل احتكاك.

The primary CTA is the Risk Score because it opens a `free_mini_diagnostic` conversation with the least friction.

---

## 3) المشكلة · The problem

الإعلانات تجلب leads، لكن القيمة تتسرّب بعد ذلك. القسم يسمّي خمس نقاط تسرّب صريحة:

Ads bring leads, but value leaks afterwards. This section names five explicit leak points:

- بلا مالك · no owner — لا أحد مسؤول عن الـlead الآن.
- بلا متابعة موثّقة · no documented follow-up — لا أحد يعرف ماذا قيل ومتى.
- بلا موافقة · no approval — رسائل تخرج بلا سجل قرار.
- بلا دليل · no evidence — لا يمكن إثبات ما حدث بعد الحملة.
- بلا خطوة تالية · no next action — البيانات موجودة لكن القرار غائب.

هذه النقاط الخمس هي بالضبط حروف معيار SOAEN المفقودة — راجع [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md).

These five leaks are precisely the missing letters of the SOAEN standard.

---

## 4) كيف يعمل — 5 خطوات · How it works — 5 steps

| الخطوة · Step | الوصف · Description |
|---|---|
| 1 | خذ 10 leads أو سير عمل واحد · take 10 leads or one workflow |
| 2 | صنّف الحالة والمتابعة · classify status and follow-up |
| 3 | جهّز الرسائل والقرارات · prepare messages and decisions (مسودات فقط · drafts only) |
| 4 | سلّم Proof Pack · deliver the Proof Pack |
| 5 | قرّر: Sprint أو Retainer · decide: Sprint or Retainer |

الخطوة 5 توجّه العميل إلى `revenue_proof_sprint_499` أو إلى عرض شهري حسب الإشارة — راجع [`OFFER_MATRIX.md`](OFFER_MATRIX.md).

Step 5 routes the customer to `revenue_proof_sprint_499` or to a monthly offer depending on the signal.

---

## 5) الثقة · Trust

قسم الثقة يعيد ذكر **الحدود الـ11 غير القابلة للتفاوض (11 non-negotiables)** بلغة العميل. هذه ليست بنوداً قانونية، بل وعود تشغيل:

The trust section restates the 11 non-negotiables in customer language — operating promises, not legal fine print:

- لا واتساب بارد · `no_cold_whatsapp` — no cold WhatsApp.
- لا scraping ولا قوائم مشتراة · `no_scraping` — no scraping.
- لا أفعال مباشرة بلا موافقة بشرية · `no_live_send` — human approval for every external action.
- لا خصم مباشر بلا موافقة · `no_live_charge` — no live charge without consent.
- لا دليل مزيّف · `no_fake_proof` — no fabricated proof.
- لا بيانات بلا موافقة · `no_unconsented_data` — no unconsented data.
- لا نتائج غير مُتحقَّقة تُعرَض كحقيقة · `no_unverified_outcomes` — outcomes are labelled by tier.
- لا تسعير مخفي · `no_hidden_pricing` — all pricing transparent.
- لا أعطال صامتة · `no_silent_failures` — failures are surfaced.
- لا وكلاء بلا حدود · `no_unbounded_agents` — agents are bounded.
- لا تغييرات غير مُدقَّقة · `no_unaudited_changes` — every important step has an evidence trail.

**لا وعد بإيراد.** الصفحة لا تعرض نسب تحويل ولا أرقام مبيعات كحقيقة — فقط فرص مُثبتة بأدلة.

No revenue promise. The page shows no conversion rates or sales numbers as fact — only evidenced opportunities.

---

## تنفيذ الصفحة · Page implementation

الأسطح المرجعية في مجلد [`../../landing/`](../../landing/): `index.html` (البطل والمشكلة)، `diagnostic.html` (درجة المخاطر)، `proof.html` (عيّنة Proof Pack)، `trust.html` (قسم الثقة). تنسيق المحتوى يتبع [`../MARKETING_AND_CONTENT_SYSTEM.md`](../MARKETING_AND_CONTENT_SYSTEM.md).

Reference surfaces live in the landing folder. Content style follows the marketing and content system.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
