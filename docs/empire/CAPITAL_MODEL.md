# Capital Model — Every Project Builds an Asset / نموذج رأس المال

> Revenue alone is consumed. Assets compound. This doc defines the five
> capital types every project must feed, and the rule that turns each
> engagement into a permanent gain — not just an invoice.
>
> الإيراد وحده يُستهلك. الأصول تتراكم. تحدد هذه الوثيقة أنواع رأس المال الخمسة
> التي يجب أن يغذّيها كل مشروع، والقاعدة التي تحوّل كل ارتباط إلى مكسب دائم —
> لا مجرد فاتورة.

**Date opened / تاريخ الفتح:** 2026-05-17
**Owner / المالك:** Founder
**Status / الحالة:** Strategic narrative — not a binding spec.

---

## 1. The principle / المبدأ

A project that brought money but left no asset is worth **less** than a
smaller project that produced a Proof Pack and a playbook. Cash funds the
month; assets fund the company.

مشروع جلب مالاً لكنه لم يترك أصلاً يساوي **أقل** من مشروع أصغر أنتج حزمة أدلة
وكُتيّب تشغيل. النقد يموّل الشهر؛ الأصول تموّل الشركة.

Every engagement is therefore measured twice: what it earned, and what it
**built**.

لذلك يُقاس كل ارتباط مرتين: ماذا كسب، وماذا **بنى**.

---

## 2. The five capital types / أنواع رأس المال الخمسة

| Capital type / نوع رأس المال | What it includes / ما يشمله |
|---|---|
| Service Capital / رأس مال الخدمة | Offers, scopes, checklists, QA standards — العروض، النطاقات، قوائم التحقق، معايير الجودة |
| Product Capital / رأس مال المنتج | Tools, modules, APIs, dashboards, automation — الأدوات، الوحدات، الواجهات البرمجية، اللوحات، الأتمتة |
| Knowledge Capital / رأس مال المعرفة | Playbooks, objections, sector insights, governance risks — كُتيّبات التشغيل، الاعتراضات، رؤى القطاعات، مخاطر الحوكمة |
| Trust Capital / رأس مال الثقة | Proof Packs, case-style insights, testimonials, audit logs — حِزم الأدلة، رؤى نمط الحالة، الشهادات، سجلات التدقيق |
| Market Capital / رأس مال السوق | Audience, partners, referrals, benchmarks, authority content — الجمهور، الشركاء، الإحالات، المعايير، محتوى السلطة |

---

## 3. The asset rule / قاعدة الأصول

Every project must produce **at least one Trust Asset, plus at least one
Knowledge or Product Asset**. This is the minimum. A project that closes
without meeting it is logged as incomplete capital, regardless of revenue.

كل مشروع يجب أن ينتج **أصل ثقة واحداً على الأقل، بالإضافة إلى أصل معرفة أو
منتج واحد على الأقل**. هذا هو الحد الأدنى. المشروع الذي يُغلق دون تحقيقه
يُسجَّل كرأس مال ناقص، بغض النظر عن الإيراد.

| Project outcome / نتيجة المشروع | Capital verdict / حكم رأس المال |
|---|---|
| Money + Proof Pack + playbook | Strong — compounding gain / قوي — مكسب متراكم |
| Money only, no asset | Weak — consumed, not built / ضعيف — مُستهلك لا مَبني |
| Smaller fee + Proof Pack + module | Preferred over money-only / مفضّل على المال وحده |

---

## 4. Where the assets live / أين تُسجَّل الأصول

Capital is not a metaphor — it is a ledger. The repo's `capital_os` module
holds the **capital asset ledger**: each asset is recorded by type, source
project, and date, so the company can see its accumulated capital, not just
its bank balance.

رأس المال ليس استعارة — بل سجل. وحدة `capital_os` في المستودع تحتفظ بـ**سجل
الأصول الرأسمالية**: كل أصل يُسجَّل بنوعه، ومشروعه المصدر، وتاريخه، حتى ترى
الشركة رأس مالها المتراكم، لا رصيدها البنكي فقط.

The ledger turns the asset rule from intention into a tracked, reviewable
record.

السجل يحوّل قاعدة الأصول من نية إلى سجل متتبَّع وقابل للمراجعة.

---

## Doctrine alignment / المواءمة مع الدستور

- Trust Capital is built only from real Proof Packs and consented case-style
  insights — never fabricated proof. / رأس مال الثقة يُبنى من حِزم أدلة حقيقية
  ورؤى بموافقة فقط.
- Testimonials and case-style insights use no customer name or logo without
  signed permission.
- The model values **assets and proof**, never guaranteed revenue. Capital
  estimates are estimates, not promised outcomes.
- Audit logs as Trust Capital reinforce the evidence-trail non-negotiable.

## Related docs / مراجع ذات صلة

- [`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) — the core Trust Asset
- [`BENCHMARK_ENGINE.md`](BENCHMARK_ENGINE.md) — Market Capital from delivery data
- [`PLATFORM_PATH.md`](PLATFORM_PATH.md) — how Product Capital becomes a platform
- [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md) — canonical Proof Pack standard
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — hard limits
