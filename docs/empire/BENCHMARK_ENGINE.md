# Benchmark Engine — Delivery Data Becomes Authority / محرك المعايير

> Once enough anonymized Proof Packs exist, Dealix stops being only a service
> provider. The accumulated delivery data becomes a **market benchmark** — a
> reference others cite. This doc defines what data feeds the benchmark, the
> report it produces, and the consent rules that gate it.
>
> بعد تجميع عدد كافٍ من حِزم الأدلة المجهّلة، تتوقف Dealix عن كونها مزوّد خدمة
> فقط. تتحول بيانات التسليم المتراكمة إلى **معيار سوقي** — مرجع يستشهد به
> الآخرون. تحدد هذه الوثيقة البيانات التي تغذّي المعيار، والتقرير الناتج عنه،
> وقواعد الموافقة التي تحكمه.

**Date opened / تاريخ الفتح:** 2026-05-17
**Owner / المالك:** Founder
**Status / الحالة:** Strategic narrative — not a binding spec.

---

## 1. Why a benchmark / لماذا معيار

A service provider competes on price and effort. A market reference competes
on nobody else. When Dealix can describe how Saudi SMEs actually run their
post-lead operations — with evidence, not opinion — the company moves up the
trust ladder permanently.

مزوّد الخدمة ينافس على السعر والجهد. المرجع السوقي لا ينافسه أحد. حين تستطيع
Dealix وصف كيف تدير المنشآت الصغيرة والمتوسطة السعودية عمليات ما بعد العميل
المحتمل فعلياً — بالأدلة لا بالرأي — تصعد الشركة في سلم الثقة بشكل دائم.

The benchmark is a by-product of work already done. No new delivery is needed
to create it — only disciplined aggregation of Proof Packs that already exist.

المعيار ناتج جانبي لعمل أُنجز بالفعل. لا يلزم تسليم جديد لإنشائه — فقط تجميع
منضبط لحِزم أدلة موجودة مسبقاً.

---

## 2. What the data captures / ماذا تلتقط البيانات

Each Proof Pack contributes a small set of structured, anonymized signals.
Across 10–20 packs, patterns emerge.

كل حزمة أدلة تساهم بمجموعة صغيرة من الإشارات المنظّمة والمجهّلة. عبر 10–20
حزمة، تظهر الأنماط.

| Signal / الإشارة | What it measures / ما يقيسه |
|---|---|
| Common follow-up gaps / فجوات المتابعة الشائعة | Where the next action is dropped |
| Common CRM missing fields / حقول CRM الناقصة الشائعة | Which records are systematically incomplete |
| Common approval risks / مخاطر الموافقة الشائعة | Actions taken without a named approver |
| Average time-to-proof / متوسط الزمن حتى الإثبات | Days from sprint start to a finished Proof Pack |
| Common objection patterns / أنماط الاعتراضات الشائعة | What buyers push back on, by sector |
| Sprint-to-retainer rate / معدل التحول من السبرنت إلى الاحتفاظ | Share of sprints that become ongoing work |
| Data-quality score / درجة جودة البيانات | A composite of completeness and traceability |

None of these signals carry a customer name, logo, or identifiable detail.

لا تحمل أي من هذه الإشارات اسم عميل أو شعاراً أو تفصيلاً يمكن التعرف عليه.

---

## 3. The report / التقرير

The aggregated signals become a periodic publication:

تتحول الإشارات المجمّعة إلى منشور دوري:

> **State of Post-Lead Revenue Ops in Saudi SMEs** — also framed as the
> **Saudi Governed AI Ops Benchmark**.
>
> **حالة تشغيل الإيراد بعد العميل المحتمل في المنشآت السعودية** — وتُقدَّم أيضاً
> باسم **معيار التشغيل المحكوم بالذكاء الاصطناعي في السعودية**.

The report presents methodology and aggregated patterns only. It never
publishes a confidential metric, a per-customer figure, or a named result. It
reports estimated patterns and ranges, not promised outcomes.

يعرض التقرير المنهجية والأنماط المجمّعة فقط. لا ينشر أبداً مقياساً سرياً، أو
رقماً خاصاً بعميل، أو نتيجة منسوبة. يعرض أنماطاً ونطاقات تقديرية، لا نتائج
موعودة.

---

## 4. The consent gate / بوابة الموافقة

The benchmark is built **after** enough Proof Packs exist — never before.
Publishing pattern claims without a real data base would be fabricated proof.

يُبنى المعيار **بعد** وجود عدد كافٍ من حِزم الأدلة — لا قبله أبداً. نشر ادعاءات
نمطية دون قاعدة بيانات حقيقية يُعدّ إثباتاً مُلفّقاً.

| Rule / القاعدة | Detail / التفصيل |
|---|---|
| Anonymized only / مجهّل فقط | No record enters the benchmark with identifying detail |
| Signed permission / إذن موقّع | No customer name or logo appears without written consent |
| Minimum base / حد أدنى | Build only after 10–20 Proof Packs exist |
| Aggregation only / تجميع فقط | Patterns and ranges, never per-customer numbers |

---

## Doctrine alignment / المواءمة مع الدستور

- The benchmark uses **anonymized, consented data only**. No customer name or
  logo is used without signed permission. / المعيار يستخدم بيانات مجهّلة
  وبموافقة فقط.
- It is built only after enough Proof Packs exist — no pattern is claimed
  before a real base supports it. No fabricated proof. / لا ادعاء نمط قبل
  وجود قاعدة حقيقية تدعمه.
- The report states **estimated** patterns and ranges, never guaranteed
  outcomes or promised revenue.
- Data minimization governs every signal: only what the benchmark needs.

## Related docs / مراجع ذات صلة

- [`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) — the proof unit the benchmark aggregates
- [`TRUST_LAYER.md`](TRUST_LAYER.md) — trust as a commercial asset
- [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md) — canonical Proof Pack standard
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — hard limits
- [`CAPITAL_MODEL.md`](CAPITAL_MODEL.md) — the benchmark as Market Capital
