# نموذج رأس المال التجاري / Commercial Capital Model
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->
> القانون / Canonical: see [docs/company/DEALIX_CAPITAL_MODEL.md](../company/DEALIX_CAPITAL_MODEL.md)

## 1. الغرض / Purpose

**العربية:** كل مشروع في دياليكس يجب أن يبني أصولًا، لا أن يجني نقدًا فقط. المشروع الذي يبادل الوقت بالمال ثم ينتهي بلا أثر هو مشروع ضعيف بنيويًا، حتى لو دفع العميل بالكامل. هذا المستند يحوّل كل تسليم إلى فرصة لمراكمة رأس مال يبقى بعد انتهاء العقد.

**English:** Every Dealix project must build assets, not just earn cash. A project that trades time for money and then ends with no residue is structurally weak, even if the client pays in full. This document turns every delivery into an opportunity to accumulate capital that outlives the contract.

كل أصل مُسجَّل يحمل وسم حقيقة: Estimate / Observed / Client-confirmed / Payment-confirmed.
Every logged asset carries a truth label: Estimate / Observed / Client-confirmed / Payment-confirmed.

## 2. أنواع رأس المال الخمسة / The Five Capital Types

| النوع / Type | يشمل / Includes | لماذا يهم / Why it matters |
|---|---|---|
| رأس مال الخدمة / Service Capital | العروض، النطاقات، قوائم التحقق، معايير الجودة / Offers, scopes, checklists, QA standards | يجعل التسليم القادم أسرع وأكثر اتساقًا / Makes the next delivery faster and more consistent |
| رأس مال المنتج / Product Capital | الأدوات، الوحدات، الـAPIs، اللوحات، الأتمتة / Tools, modules, APIs, dashboards, automation | يقلّل جهد التسليم اليدوي مع كل تكرار / Cuts manual delivery effort with each repeat |
| رأس مال المعرفة / Knowledge Capital | أدلة التشغيل، الاعتراضات، رؤى القطاعات، مخاطر الحوكمة / Playbooks, objections, sector insights, governance risks | يحوّل تجربة فردية إلى ميزة مؤسسية / Turns one experience into an institutional advantage |
| رأس مال الثقة / Trust Capital | حزم الإثبات، دراسات الحالة، الشهادات، سجلات التدقيق / Proof packs, case studies, testimonials, audit logs | يقصّر دورة البيع للعميل التالي / Shortens the next client's sales cycle |
| رأس مال السوق / Market Capital | الجمهور، الشركاء، الإحالات، المعايير، محتوى السلطة / Audience, partners, referrals, benchmarks, authority content | يخفض تكلفة اكتساب الطلب / Lowers the cost of acquiring demand |

## 3. القاعدة الصارمة / The Hard Rule

**العربية:** كل مشروع يجب أن ينتج أصل ثقة واحدًا على الأقل + أصل معرفة أو منتج واحدًا على الأقل. هذان الأصلان شرط إغلاق المشروع — لا يُعدّ المشروع مكتملًا قبل تسجيلهما في سجل رأس المال. النقد وحده لا يكفي لإغلاق ملف.

**English:** Every project must produce at least one Trust Asset + at least one Knowledge or Product Asset. These two assets are a project-close condition — a project is not complete until both are logged in the capital ledger. Cash alone does not close a file.

```text
PROJECT CLOSE GATE
  cash collected            -> necessary, not sufficient
  >= 1 Trust Asset          -> REQUIRED
  >= 1 Knowledge|Product    -> REQUIRED
  all assets truth-labelled -> REQUIRED
  ----------------------------------------
  missing any -> project stays OPEN in the ledger
```

## 4. قائمة التقاط رأس المال لكل مشروع / Per-Project Capital-Capture Checklist

تُملأ عند إغلاق كل مشروع. كل سطر يحمل وسم حقيقة ومالكًا.
Completed at every project close. Each line carries a truth label and an owner.

| # | السؤال / Question | ناتج مقترح / Suggested artifact | إلزامي / Required |
|---|---|---|---|
| 1 | هل تحسّن عرض أو نطاق أو قائمة تحقق؟ / Did an offer, scope, or checklist improve? | نطاق محدّث / Updated scope | اختياري / Optional |
| 2 | هل بُنيت أو حُسّنت أداة أو وحدة؟ / Was a tool or module built or improved? | إدخال في سجل المنتج / Product-ledger entry | اختياري / Optional |
| 3 | هل ظهرت رؤية قطاع أو اعتراض جديد؟ / Did a sector insight or new objection emerge? | إدخال دليل تشغيل / Playbook entry | واحد على الأقل / At least one |
| 4 | هل نتج Proof Pack أو دراسة حالة مجهّلة؟ / Did a Proof Pack or anonymized case study result? | أصل ثقة / Trust asset | إلزامي / Mandatory |
| 5 | هل وافق العميل كتابةً على القيمة؟ / Did the client confirm value in writing? | اقتباس Client-confirmed / Client-confirmed quote | مُستحسَن / Preferred |
| 6 | هل نتجت إحالة أو تعريف بشريك؟ / Did a referral or partner intro result? | إدخال رأس مال السوق / Market-capital entry | اختياري / Optional |
| 7 | هل سُجّلت مخاطرة حوكمة جديدة؟ / Was a new governance risk logged? | إدخال سجل المخاطر / Risk-register entry | اختياري / Optional |
| 8 | هل وُسم كل رقم بوسم حقيقة واحد؟ / Is every number tagged with one truth label? | تدقيق وسم / Label audit | إلزامي / Mandatory |

البندان 3 و 4 يستوفيان القاعدة الصارمة معًا. / Items 3 and 4 together satisfy the Hard Rule.

## 5. كيف يربط النقد برأس المال / How Cash Links to Capital

**العربية:** العروض المربوطة بالدفع هي قناة النقد، لكن كل عرض يجب أن يولّد رأس مال أيضًا. التشخيص المجاني يبني رأس مال السوق، والسبرنت يبني رأس مال الثقة، والاحتفاظ الشهري يبني رأس مال المنتج عبر التكرار.

**English:** The wired offers are the cash channel, but each offer must also generate capital. The free diagnostic builds Market Capital, the sprint builds Trust Capital, and a monthly retainer builds Product Capital through repetition.

| العرض / Offer | السعر / Price | رأس المال الأساسي المتوقَّع / Primary capital expected |
|---|---|---|
| Free Mini Diagnostic | 0 | رأس مال السوق / Market Capital |
| Revenue Proof Sprint | 499 one-time | رأس مال الثقة / Trust Capital |
| Data-to-Revenue Pack | 1,500 one-time | رأس مال المعرفة / Knowledge Capital |
| Growth Ops Monthly | 2,999/mo | رأس مال المنتج / Product Capital |
| Support OS Add-on | 1,500/mo | رأس مال الخدمة / Service Capital |
| Executive Command Center | 7,500/mo | رأس مال المنتج + الثقة / Product + Trust Capital |
| Agency Partner OS | custom | رأس مال السوق / Market Capital |

أي طبقة أكبر من هذه العروض: Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع.

## 6. الانضباط ضد الإثبات المزيّف / Discipline Against Fake Proof

**العربية:** أصل الثقة لا يُسجَّل إلا بدليل حقيقي. لا دراسة حالة بأسماء عملاء حقيقيين دون موافقة، ولا اقتباس بلا تأكيد كتابي، ولا رقم بلا وسم. رأس مال الثقة المبني على مبالغة هو دَين خفيّ، لا أصل.

**English:** A Trust Asset is logged only with real evidence. No case study uses real client names without consent, no quote appears without written confirmation, no number appears without a label. Trust Capital built on exaggeration is a hidden liability, not an asset.

## 7. مسؤولية السجل / Ledger Ownership

**العربية:** المؤسس يملك سجل رأس المال. يُراجَع أسبوعيًا للتأكد من أن كل مشروع مغلق استوفى القاعدة الصارمة، وأن لا أصل ثقة بلا دليل موسوم.

**English:** The Founder owns the capital ledger. It is reviewed weekly to confirm every closed project met the Hard Rule and that no Trust Asset exists without labelled evidence.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
