# لماذا الآن — Why Now
## فجوة عمليات الذكاء الاصطناعي المحوكمة في الخليج — The Governed AI Ops Gap in the GCC

---

## ١. ما تَمَّ الإعلان عنه عامّاً · What has been publicly announced

**AR.** الاستثمار في البنية التحتية للذكاء الاصطناعي الخليجي عَلَني وضخم وموثَّق:

- **HUMAIN (السعودية)** — شركة وطنية أعلنت لتطوير البنية التحتية والموديلات والمنتجات.
- **MGX (الإمارات)** — صندوق استثمار تكنولوجي يركّز على الذكاء الاصطناعي والبنية التحتية.
- **قطر** — استراتيجية وطنية معلنة للذكاء الاصطناعي.
- **البحرين، الكويت، عُمان** — كلٌّ منها نشر إطاراً وطنياً للتحوّل الرقمي يتضمّن الذكاء الاصطناعي.

هذه الاستثمارات عامّة. لا نقدّم أرقاماً غير مَنْسوبة. ما يهمّنا هنا ليس حجم الاستثمار، بل ما يَنقُص بجواره.

**EN.** GCC AI infrastructure investment is publicly announced and well documented: HUMAIN (Saudi Arabia) as a national AI development entity; MGX (UAE) as a tech-focused investment vehicle; Qatar's national AI strategy; Bahrain, Kuwait, and Oman each publishing national digital frameworks that include AI components. These announcements are public. We cite their existence, not unsourced figures. What matters is not the size of investment, but what sits next to it unbuilt.

---

## ٢. الفجوة · The gap

**AR.** البنية التحتية للموديلات تتقدّم. ولكن "كيف نُشغّل الذكاء الاصطناعي بحوكمة قابلة للتدقيق في شركة منظَّمة سعودية أو خليجية" ليست مسألة بنية تحتية. هي مسألة طبقة تشغيلية. هذه الطبقة "تنظيم لين" حالياً:

- PDPL سارٍ، لكن تفسير "ما يعدّ موافقة كافية" يتغيّر بحسب القطاع.
- NDMO يطلب مسار بيانات، لكن لا يوجد مرجع تشغيلي مفتوح لما يَعدّه CISO سعودي مقبولاً.
- "وكلاء" الذكاء الاصطناعي يَنتشرون، لكن لا توجد طبقة هوية معلنة لكل وكيل تَنفُذ منها الموافقات.
- "أصول" الذكاء الاصطناعي تَنشأ كل شهر، لكن لا توجد عقيدة علنية تَستوعِب كيف تَنتقِل عبر الارتباطات.

**EN.** Model infrastructure progresses. "How do we run AI with auditable governance inside a regulated Saudi or GCC company?" is not an infrastructure question; it is an operations layer question. That layer is currently "soft regulation": PDPL is in force, but interpretation of "sufficient consent" varies by sector; NDMO requires data lineage, but no open operational reference defines what a Saudi CISO will accept; AI "agents" proliferate, but no public identity layer carries approvals through them; AI "assets" multiply, but no public doctrine codifies how they carry across engagements.

---

## ٣. ما تَبنيه Dealix · What Dealix builds

**AR.** طبقة العمليات بين الموديل والمشتري المنظَّم. سبع وظائف صريحة:

1. **وضوح المصدر** — Source Passport لكل صف بيانات.
2. **الموافقة البشرية** — لا فعل خارجي بدون موافقة موثّقة (الالتزام #٨ في [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md)).
3. **إثبات تشغيل الذكاء الاصطناعي** — سلسلة تدقيق قابلة للتصدير (CAP-008).
4. **إنفاذ السياسة** — `decide(action, context)` يَمنع المحظور قبل التشغيل.
5. **إثبات القيمة** — Proof Pack بـ ١٤ قسماً لكل ارتباط مُغلَق (CAP-006).
6. **ثقة المشتري المنظَّم** — Trust Pack PDF بـ ١١ قسماً لمراجعة CISO (CAP-007).
7. **هوية وصلاحيات العميل الذكي** — لا وكيل بلا هوية مُسجَّلة (الالتزام #٩).

**EN.** Seven explicit functions: source clarity (Source Passport per row), human approval (commitment #8), AI run evidence (audit chain, CAP-008), policy enforcement (runtime `decide()`), proof of value (Proof Pack 14 sections, CAP-006), regulated buyer trust (Trust Pack PDF 11 sections, CAP-007), agent identity + permissions (commitment #9). Each function is enforced by tests cited in [`docs/funding/CAPITAL_ASSET_TRACTION.md`](./CAPITAL_ASSET_TRACTION.md).

---

## ٤. لماذا الفجوة لا تَسدّ نفسها · Why the gap does not self-close

**AR.** ثلاثة أسباب:

- **Big 4 الخليجي** يقدّم تقريراً، لا منصة. التقرير لا يَستمرّ بعد انتهاء الارتباط.
- **مزوّدو الموديلات الأجانب** يقدّمون قدرة، لا حوكمة محلية. لا يحملون استجابة CISO سعودي بالعربية في عمليتهم اليومية.
- **منصات الذكاء الاصطناعي العامّة** تَفترض موافقة المستخدم النهائي، ولا تَفترض موافقة الشركة على كل فعل خارجي.

كل نقص من هذه الثلاثة هو فُسحة لـ Dealix.

**EN.** Three reasons: (a) GCC Big 4 delivers reports, not platforms — the report does not survive engagement close; (b) foreign model vendors ship capability, not local governance — they do not carry Saudi-CISO response patterns in Arabic in their daily operation; (c) general-purpose AI platforms assume end-user consent and do not assume firm-level approval on every external action. Each gap is a Dealix opening.

---

## ٥. النافذة · The window

**AR.** فترة "التنظيم اللين" تَنغلق. خلال ١٢–٢٤ شهراً، ستَنشر الجهات التنظيمية الخليجية معايير أكثر تفصيلاً. اليوم: مرجع علَني واحد يَمكنه أن يُصبح المرجع. غداً: المعيار يَأتي من المُنظِّم، والشركات تَختار من يَنفّذه. نريد أن نَكون من يَنفّذه، لا من يَستجيب له بعد فوات الأوان.

**EN.** The "soft regulation" window is closing. Within 12–24 months, GCC regulators will publish more detailed standards. Today: one public reference can become the reference. Tomorrow: the standard arrives from the regulator and firms choose who implements it. We aim to be the implementer, not the late responder. This is a posture, not a guarantee.

---

## ٦. ما لا نَدّعيه · What we do not claim

**AR.** لا نَدّعي حجم سوق دون مرجع عام. لا نَدّعي أن PDPL أو NDMO سَيُلزمان بالضرورة كل شركة بمنصة طرف ثالث. لا نَدّعي أن HUMAIN أو MGX أو أي جهة أخرى تُؤيّد Dealix. نَذكُرها لأنها عامّة، ونَترُك المراجعة المستقلّة للقارئ.

**EN.** We do not claim TAM without a public source. We do not claim PDPL or NDMO will mandate every firm to use a third-party platform. We do not claim HUMAIN, MGX, or any other entity endorses Dealix. We cite them because they are public, and we leave independent verification to the reader.

---

## مراجع داخلية · Internal references

- [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) — ١١ التزاماً.
- [`docs/gcc-expansion/GCC_EXPANSION_THESIS.md`](../gcc-expansion/GCC_EXPANSION_THESIS.md) — أطروحة التوسّع.
- [`docs/funding/DEALIX_MOAT_STACK.md`](./DEALIX_MOAT_STACK.md) — مكدّس الخندق.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
