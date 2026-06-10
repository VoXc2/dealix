# LinkedIn Post 004 — Dealix-on-Dealix

> Bilingual long-form for the founder voice. AR first, EN second. No emojis. No model names. Methodology demonstration on synthetic data.
>
> Cross-link: [LINKEDIN_POST_001.md](./LINKEDIN_POST_001.md), [LINKEDIN_POST_002.md](./LINKEDIN_POST_002.md), [LINKEDIN_POST_003.md](./LINKEDIN_POST_003.md), [case_003_dealix_internal.md](../case-studies/case_003_dealix_internal.md), [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md).

---

**Title — العنوان**

أكلنا من طبخنا — Dealix استخدم Dealix على نفسه / We ate our own dogfood — Dealix used Dealix on itself.

---

## الخطّاف — Hook

معظم خدمات الذكاء الاصطناعي تَعِد برفع المبيعات. نحن في ديليكس وعدنا بمنهجية وأثر تدقيق. ثم شغّلنا منهجيتنا على خطّ أنابيبنا، وأودَعنا حزمة الإثبات في git.

Most AI services promise sales lift. We promised methodology + audit trail. Then we ran our own methodology on our own pipeline and committed the Proof Pack to git.

---

## العربية أولاً

### ماذا حدث

في الأسبوع الماضي اتّخذنا قراراً غير عاديّ: شغّلنا ديليكس على نفسه. الهدف لم يكن رقم مبيعات — كان البرهنة على أن المنهجية تُنتج أثراً قابلاً للتدقيق حتى على بيانات تركيبية.

ما الذي شغّلناه:

- **ملف الإدخال:** `data/demo/saudi_b2b_demo.csv` — قائمة تركيبية لعشرين شركة خدمات B2B سعودية مجهولة الهوية. لا بيانات عميل حقيقي. كل سجل مصنّف بقطاع، وحالة علاقة، ومنطقة.
- **المُشغِّل:** المنسّق `/api/v1/sprint/run` نفسه الذي يستلمه أي عميل يدفع 499 ريالاً.
- **المخرَج المُلزِم:** حزمة إثبات من 14 قسماً، مودَعة في `data/proofs/dealix_internal_v1_proof_pack.json`.
- **الملخّص العام الآمن:** `docs/case-studies/case_003_dealix_internal.md` — يُنشَر بدون اسم عميل حقيقي لأنه لا يوجد عميل حقيقي.

### الأرقام الثلاثة التي تستحق العرض

عند نشر هذا المنشور سيُحدِّث المؤسس الأرقام من ملف الحزمة فعلياً:

- **درجة الإثبات (Proof Score):** `XX/100`
- **الطبقة (Tier):** `<tier>`
- **الأصول الرأسمالية المسجَّلة (Capital Assets registered):** `Y`

لا أرقام إيرادات. لا "زيادة مبيعات بنسبة كذا". لا وعد بنتائج. المنهجية هي الأثر، لا الادّعاء.

### ماذا يُثبت هذا

ثلاث نقاط، لا أكثر:

1. **المنهجية أهم من السحر.** حتى على بيانات تركيبية، تُنتج المنهجية حزمة قابلة للقراءة، قابلة للتدقيق، قابلة للنقد.
2. **الأثر يسبق العميل.** قبل العميل الأول، لدينا الفعل: 14 قسماً، درجة محسوبة، أصل رأسمالي مودَع.
3. **الشفافية تُختبر بالتطبيق.** عندما نقول "لا ادّعاء بلا مصدر"، فإن هذا المنشور نفسه يستشهد بمسار ملف في المستودع.

ما الذي لا يُثبته:

- لا يُثبت أن ديليكس باع لعميل سعودي حقيقي. لم نَدَّعِ ذلك.
- لا يُثبت رفع إيراد. لم نَدَّعِ ذلك.
- لا يُثبت قدرة على عميل مُعقَّد بعينه. يُثبت أن المنهجية تعمل من الطرف إلى الطرف.

### دعوة

شغّل المنهجية ذاتها على بياناتك. تشخيص مجاني عبر `/diagnostic.html`. سبرنت كامل بسبعة أيام مقابل 499 ريالاً سعودياً.

---

## English

### What happened

Last week we made an unusual choice: we ran Dealix on Dealix. The goal was not a sales number — it was to demonstrate that the methodology produces an auditable artifact even on synthetic data.

What ran:

- **Input file:** `data/demo/saudi_b2b_demo.csv` — a synthetic list of 20 anonymized Saudi B2B services companies. No real customer data. Each row labeled by sector, relationship_status, and city.
- **Orchestrator:** the same `/api/v1/sprint/run` endpoint that any paying 499 SAR customer receives.
- **Required artifact:** a 14-section Proof Pack, committed at `data/proofs/dealix_internal_v1_proof_pack.json`.
- **Public, case-safe summary:** `docs/case-studies/case_003_dealix_internal.md` — published without a real customer name because there is no real customer.

### The three numbers worth showing

When this post is published, the founder will update the numbers below directly from the Proof Pack file:

- **Proof Score:** `XX/100`
- **Tier:** `<tier>`
- **Capital Assets registered:** `Y`

No revenue numbers. No "X% sales lift". No outcome promises. The methodology is the artifact, not the claim.

### What this proves

Three points, nothing more:

1. **Methodology beats magic.** Even on synthetic data, the methodology produces a readable, auditable, criticizable pack.
2. **The artifact precedes the customer.** Before the first paying customer, we have the act itself: 14 sections, a computed score, a capital asset deposited.
3. **Transparency is tested by application.** When we say "no claim without source", this post itself cites a file path in the repo.

What this does NOT prove:

- It does not prove Dealix has sold to a real Saudi customer. We did not claim that.
- It does not prove a revenue lift. We did not claim that.
- It does not prove capability on a specific complex customer. It proves the methodology runs end-to-end.

### Why we did this publicly

Three reasons we ran this in the open instead of in a private sandbox:

1. **Sales hygiene:** every Saudi B2B operator we talk to has met an AI vendor whose demo was on the vendor's laptop, with the vendor's data, with the vendor's prompts. The "demo" tells you nothing about whether the system runs end-to-end on data you can audit. Our demo is in a public git commit with a public file path. You can read it before you talk to us.
2. **Doctrine test:** we have 11 non-negotiables enforced in code. Running our own pipeline forces us to obey our own gates. If a gate would have refused a step, we'd have known immediately — and that's exactly what we want to find.
3. **Methodology > magic:** the only durable advantage in this market is process under audit. Numbers can be staged. A 14-section pack with a computed score is harder to stage and easier to falsify on inspection.

### CTA

Run the same on YOUR data — free diagnostic at `/diagnostic.html`. 499 SAR for the full Sprint.

---

`#SaudiAI` `#PDPL` `#RevenueOps` `#B2B` `#ProofOverPromise`

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
