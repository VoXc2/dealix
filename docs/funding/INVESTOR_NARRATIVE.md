# السردية الاستثمارية — Investor Narrative
## القوس من المشكلة إلى الطلب — Arc from problem to ask

---

## ١. المشكلة · The problem

**AR.** السوق المتوسط الخليجي المنظَّم (٥٠–٥٠٠ موظف) يواجه فجوة لا يحلّها لا الموديل ولا الاستشاري. الموديل يقدّم إجابة، لكنه لا يقدّم مصدراً ولا موافقة ولا إثباتاً قابلاً للتدقيق. الاستشاري يقدّم تقريراً، لكنه لا يقدّم بنية تشغيلية تستمر بعد انتهاء الارتباط. النتيجة: المشتري المنظَّم يجمّد قرار التبنّي لأن CISO أو DPO ليس عندهما طريقة لقول "نعم" بثقة. PDPL وNDMO فعّالان، لكن لا يوجد مرجع تشغيلي واحد للامتثال يومياً.

**EN.** The regulated GCC mid-market (50–500 employees) faces a gap neither the model nor the consultant resolves. The model gives an answer; it does not give source, approval, or auditable proof. The consultant gives a report; the report does not become an operating system that outlives the engagement. The regulated buyer freezes adoption because the CISO or DPO has no way to say "yes" with confidence. PDPL and NDMO are active, but no single operational reference exists for day-to-day compliance.

---

## ٢. البصيرة · The insight

**AR.** الخندق ليس الموديل — الموديل يُستنسخ في ربع سنة. الخندق هو العقيدة المُنفَّذة في الكود: ١١ التزاماً غير قابلة للتفاوض، كل التزام مرتبط باختبار CI يُسقط البناء عند الإخلال. هذه العقيدة معلنة (`/api/v1/dealix-promise`) ومفتوحة (open-doctrine repo). من ينسخها بدون ثقافة التسليم خلفها، يحصل على نص ولا يحصل على نظام.

**EN.** The moat is not the model — models clone in a quarter. The moat is the doctrine enforced in code: 11 non-negotiables, each backed by a CI test that fails the build on violation. The doctrine is public (`/api/v1/dealix-promise`) and openly published (open-doctrine repo). Cloning the text without the delivery culture yields words, not a system. See [`docs/funding/DEALIX_MOAT_STACK.md`](./DEALIX_MOAT_STACK.md).

---

## ٣. المنتج · The product

**AR.** سلّم تجاري بثلاث درجات + إطار عقيدة مفتوحة:

| الدرجة | السعر | المدة | المخرَج المُحوري |
|---|---|---|---|
| التشخيص الاستراتيجي | مجاني | يوم عمل | Decision Passport + ٣ فرص |
| ريتينر العمليات المحوكمة | ٤٬٩٩٩ ر.س / شهر | ٣ أشهر حد أدنى | تقرير قيمة شهري + Proof Pack |
| سبرنت ذكاء الإيرادات | ٢٥٬٠٠٠ ر.س | ٣٠ يوم | Capital Asset + نموذج تنبؤ |

كل ارتباط مغلق يودع أصلاً رأسمالياً (CAP-XXX) في السجل العام، فترتفع كفاءة الارتباط التالي.

**EN.** A three-rung commercial ladder plus the Open Doctrine framework. Source registry: `auto_client_acquisition/service_catalog/registry.py`. Every closed engagement deposits a Capital Asset (CAP-XXX) into the registry, so the next engagement starts ahead. The Open Doctrine is a public reference implementation that positions Dealix as the de-facto standard before alternatives appear.

---

## ٤. وضع الجرّ · Traction posture

**AR.** الجرّ يُقاس بما هو مبني وقابل للتحقق، ليس بأرقام إيرادات لم تُسجَّل بعد:

- **الإنتاج حي.** خمس نقاط نهاية عامة، كل واحدة مُختبَرة في CI. CAP-001 إلى CAP-015 مسجَّلون.
- **العقيدة معلنة.** [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) + open-doctrine repo.
- **أربعة أسواق خليجية مُخطَّط لها.** السعودية (التركيز)، الإمارات، قطر، الكويت — مع مصفوفة توطين وأنماط شركاء (`docs/gcc-expansion/`).
- **الفاتورة #١ أمامنا.** نُسرد هذا صراحة، لا نُخفيه. المرحلة "محادثات قبل البذرة"، لا "جولة بذرة جارية".

**EN.** Traction is what is built and verifiable, not revenue numbers not yet booked. Production endpoints are live and test-backed. CAP-001 through CAP-015 are registered (`auto_client_acquisition/capital_os/capital_asset_registry.py`). Four GCC markets are posture-mapped: Saudi (focus), UAE, Qatar, Kuwait. Invoice #1 is still ahead and we say so. The stage is pre-seed conversation, not pre-seed round.

---

## ٥. الفئة · The category

**AR.** Governed AI Operations. ليست "AI consulting" ولا "AI agents" ولا "MLOps". هي طبقة العمليات بين الموديل والمشتري المنظَّم — تشمل: وضوح المصدر، الموافقة البشرية، إثبات تشغيل الذكاء الاصطناعي، إنفاذ السياسة، إثبات القيمة، ثقة المشتري المنظَّم، وهوية وصلاحيات العميل الذكي. الفئة جديدة بما يكفي ليكون المرجع العلني الأول مَن يحدّد حدودها.

**EN.** Governed AI Operations. Not "AI consulting", not "AI agents", not "MLOps". It is the operating layer between the model and the regulated buyer: source clarity, human approval, AI run evidence, policy enforcement, proof of value, regulated buyer trust, agent identity + permissions. The category is new enough that the first public reference defines its perimeter. See [`docs/funding/WHY_NOW_GCC_AI_OPS.md`](./WHY_NOW_GCC_AI_OPS.md).

---

## ٦. الطلب · The ask

**AR.** ثلاثة طلبات محدّدة:

1. **تعريف واحد بشريك مرسٍ.** Big 4 GCC، أو معالج مرخَّص من SAMA، أو CISO خدمات B2B سعودية.
2. **مستشار استراتيجي واحد.** سجل تنفيذي في عمليات منظَّمة سعودية أو خليجية. لا نوظّف "للإمكان"، نوظّف لسجل مُنفَّذ.
3. **مراجعة لاحقة عند الفاتورة #٢.** ليس وعداً بفاتورة، بل اتفاق على نافذة مراجعة.

**EN.** Three specific asks: (1) one anchor partner intro (Big 4 GCC, SAMA-licensed processor, Saudi B2B services CISO); (2) one strategic advisor with an executed track record in regulated Saudi or GCC operations — we hire for executed records, not for potential; (3) a revisit window when Invoice #2 lands — not a revenue promise, a review agreement.

---

## ٧. الحدود · The boundaries

**AR.** لا نعرض ضمانات إيرادات. لا نَعِد بأعداد تحويل. لا نقدّم تقديرات سوقية كبيرة (TAM) دون مرجع عام. لا نسوّق التجريف ولا الواتساب البارد ولا أتمتة LinkedIn — كل واحد منها محجوب في الكود. الفرص المُسرَدة هنا "فرص مُثبَتة بأدلة"، ليست أرقاماً مضمونة.

**EN.** We do not offer revenue guarantees. We do not promise conversion rates. We do not present TAM figures without a public reference. We do not market scraping, cold WhatsApp, or LinkedIn automation — each is blocked at code level. Opportunities are "evidenced opportunities", not guaranteed numbers.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
