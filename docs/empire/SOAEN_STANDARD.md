<!-- LAYER: empire/doctrine | Owner: Founder | Bilingual AR+EN | draft_only -->
<!-- Part of the Dealix Operating Standard — see INDEX.md -->

# معيار SOAEN — The Dealix SOAEN Standard

> **AR:** أي workflow لا يحتوي الخمسة لا يصلح للأتمتة ولا يصلح أن يُباع كـAI workflow.
> **EN:** A workflow missing any of the five is not automatable — and must not be sold as an AI workflow.

---

## التعريف / Definition

**SOAEN** = الاختبار الأدنى لصلاحية أي workflow للتشغيل المحكوم:

| الحرف | EN | بالعربي | السؤال / The Question |
|-------|----|---------|------------------------|
| **S** | Source | مصدر | من أين جاءت الإشارة/المعرفة؟ |
| **O** | Owner | مالك | من المسؤول عن المتابعة؟ |
| **A** | Approval | موافقة | هل التصرف الخارجي معتمد؟ |
| **E** | Evidence | دليل | هل يوجد أثر مُسجّل؟ |
| **N** | Next Action | خطوة تالية | ما الخطوة الواضحة بعدها؟ |

---

## قاعدة المعيار / The Standard Rule

> **AR:** workflow ينقصه أي حرف من SOAEN = noise، لا يُؤتمت ولا يُباع.
> **EN:** A workflow missing any SOAEN letter is noise — do not automate it, do not sell it.

جمل المعيار للسوق:

- Lead بلا **Owner** = ليس pipeline.
- AI action بلا **Approval** = خطر.
- إجابة بلا **Source** = معرفة بلا مصدر.
- تشغيل بلا **Evidence** = ادعاء.
- لوحة بلا **Next Action** = تقرير فقط.

---

## كيف يُفرض المعيار في Dealix / How the Standard Is Enforced

المعيار ليس شعاراً — هو مُطبَّق في الكود:

| حرف SOAEN | حيث يُفرض / Enforced in |
|-----------|--------------------------|
| Source | Source Passport — لا إجابة معرفية بلا مصدر |
| Owner | `owner` في [`decision_passport`](../../auto_client_acquisition/decision_passport/) — «بلا owner = غير تشغيلي» |
| Approval | `action_mode` + [`governance_os`](../../auto_client_acquisition/governance_os/) — الإرسال الخارجي يحتاج موافقة |
| Evidence | [`proof_os`](../../auto_client_acquisition/proof_os/) + سجلّات Dealix (ledgers) |
| Next Action | `recommended_action` في Decision Passport |

---

## العلاقة بغير القابل للتفاوض / Relation to the Non-Negotiables

SOAEN هو الوجه الإيجابي لقائمة «غير القابل للتفاوض»: المعيار يقول ما يجب أن
يوجد، والقائمة تقول ما يُمنع. الاثنان معاً يحميان الثقة.

**EN:** SOAEN is the positive face of the non-negotiables — the standard states
what *must* exist; the non-negotiables state what is *forbidden*.

---

## روابط / Cross-links

- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — غير القابل للتفاوض / non-negotiables
- [`TRUST_LAYER.md`](TRUST_LAYER.md) — وعد الثقة / the Trust Promise
- [`DEALIX_METHOD.md`](DEALIX_METHOD.md) — السلسلة الكاملة / the full chain
- [`../../auto_client_acquisition/decision_passport/`](../../auto_client_acquisition/decision_passport/) — جواز القرار / Decision Passport
