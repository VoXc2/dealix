# أول ثَلاث تَوظيفات — First 3 Hires
## بَوّابات مَشروطة بالإيراد، لا بالنقد — Revenue-gated, not cash-gated

---

## ١. الفرضية · The premise

**AR.** لا تَوظيف قبل إِيراد مُتَحقّق. حتى مع تَمويل ملائكي، البَوّابة بَوّابة. الفلسفة: التَوظيف قبل الإيراد يُحوّل الشركة من "تُسلّم قيمة" إلى "تُموّل رواتب". هذا الترتيب يُقدّم القُدرة على التَسليم على القُدرة على الحَجم، والإيراد المُتَحقّق على الإمكان المُحتمَل. التفاصيل التَكميلية في [`docs/funding/HIRING_PLAN.md`](./HIRING_PLAN.md) و [`docs/funding/HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md).

**EN.** No hire before revenue. Even with angel funding, the gate is the gate. Hiring before revenue converts the firm from "delivers value" to "funds salaries". This order privileges delivery capacity over scale capacity, and realized revenue over potential. Companion docs: [`docs/funding/HIRING_PLAN.md`](./HIRING_PLAN.md) and [`docs/funding/HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md).

---

## ٢. التَوظيف #١ — مهندس عمليات الذكاء الاصطناعي · Hire #1 — AI Ops Engineer

### بَوّابة التَفعيل · Activation gate
**AR.** ≥ ٥٠٬٠٠٠ ر.س ARR مُتَحقّق. هذه عَتَبة الفاتورة الثالثة أو الرابعة، لا الأولى. قبلها، Claude يَكتب الكود والمؤسس يَراجع.  
**EN.** ≥ 50K SAR ARR realized. This is roughly the third or fourth invoice, not the first. Before it, Claude writes code and the founder reviews.

### النِطاق · Scope
**AR.** يَملك أربع طبقات:
1. **خط Source Passport** — كل بَيان مَصدره مَعروف على نفس الصف.
2. **Governance Runtime** — `decide(action, context)` يَمنع المحظور قبل التَشغيل.
3. **أتمتة Proof Pack** — توليد ١٤ قسم لكل ارتباط مُغلَق.
4. **Evidence Graph** — سلسلة تَدقيق قابلة للتصدير لـ CISO / SAMA.

**EN.** Owns four layers: Source Passport pipeline, governance runtime (`decide(action, context)`), Proof Pack automation (14 sections per engagement), Evidence Graph (audit chain exportable for CISO / SAMA review).

### شُروط عَدَم التَوظيف · Do-not-hire conditions
**AR.**
1. لا حركة سبرنت قابلة للتكرار (آخر سبرنتَين لم يُسلَّما في الوقت).
2. لا خَطّ مَبيعات يَقوده المؤسس بعَدَد ≥ ٥ مُحادَثات أسبوعياً.
3. لا إِشارة عَميل مدفوع (الفاتورة #١ لم تَصل بَعد).
4. لم يَجتز إِشارات عَدَم التَوظيف في [`HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md) (بطاقة #١).

**EN.** Do not hire if: (a) no repeatable sprint motion — the last two sprints slipped; (b) no founder-led sales pipeline at ≥ 5 conversations/week; (c) no paid customer signal — Invoice #1 has not landed; (d) candidate fails Card #1 no-hire signals.

### لماذا هذا الدور أولاً · Why this role first
**AR.** البنية التحتية الهندسية للحوكمة تَتراكم. كل ارتباط يَستهلك جزءاً من وقت المؤسس على الكود. تَحرير المؤسس من الكود يَفتح ٤ ساعات / يوم إضافية للبيع والتَسليم. لا يُوظَّف مهندس قبل الفاتورة #٣ لأن Claude يَستطيع تَغطية الحاجة الهندسية حتى ذلك الوقت.

**EN.** Governance engineering compounds. Every engagement consumes founder time on code. Freeing the founder from code opens four additional hours/day for sell + deliver. No engineer before Invoice #3 because Claude can cover engineering need until then.

---

## ٣. التَوظيف #٢ — مشغّل التَسليم / RevOps · Hire #2 — Delivery / RevOps Operator

### بَوّابة التَفعيل · Activation gate
**AR.** ≥ ١٠٠٬٠٠٠ ر.س ARR مُتَحقّق. بَعْد الفاتورة #٥ تقريباً، حين يَبدأ التَسليم اليَدوي يَستهلك أكثر من ٣ ساعات / يوم من المؤسس.  
**EN.** ≥ 100K SAR ARR realized. Roughly after Invoice #5, when manual delivery consumes more than 3 hours/day of founder time.

### النِطاق · Scope
**AR.** يَملك أربع طبقات:
1. **تَسليم Revenue Intelligence Sprint** — ٣٠ يوم × ١٠ مُخرَجات.
2. **تَجميع بَيانات العميل** — Source Passport يَدوي ثم آلي.
3. **مسوّدات Proof Pack** — قبل أتمتتها الكاملة.
4. **تقارير القيمة الشهرية** — قابلة للتدقيق، بَوّابة الريتينر.

**EN.** Owns four layers: Revenue Intelligence Sprint delivery (30 days × 10 deliverables), client data intake (Source Passport manual → automated), Proof Pack drafts (pre-full-automation), monthly Value Reports (audit-ready, retainer gate).

### شُروط عَدَم التَوظيف · Do-not-hire conditions
**AR.**
1. لم تُوَثَّق دفاتر التَشغيل (لا playbook فعلي يَستطيع المرشّح قراءته).
2. المؤسس لم يُسلّم ٣ مَشاريع مُماثلة بنَفسه. لا يَستطيع المرشّح تَكرار ما لم يُؤَدِّه المؤسس.
3. لا CRM فَعّال يَستطيع المرشّح قراءته في الأسبوع الأول.
4. لم يَجتز إِشارات عَدَم التَوظيف في [`HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md) (بطاقة #٢).

**EN.** Do not hire if: (a) playbooks not documented — no actual playbook the candidate can read; (b) founder has not delivered 3 similar projects personally — the candidate cannot replicate what the founder did not perform; (c) no functioning CRM the candidate can read in week one; (d) candidate fails Card #2 no-hire signals.

### لماذا هذا الدور ثانياً · Why this role second
**AR.** المهندس فَعّل التَسليم تقنياً. المُشغّل يَفعّله بَشَرياً. الفَرق بَيْنهما: المهندس يَبني الخَط، والمُشغّل يَركض عليه. لا تَركيب قبل خَطّ.

**EN.** The engineer enables delivery technically. The operator runs it humanly. Distinction: the engineer builds the rail; the operator runs on it. No runner before a rail.

---

## ٤. التَوظيف #٣ — مشغّل شراكات / نمو خليجي · Hire #3 — Partnerships / GCC Growth Operator

### بَوّابة التَفعيل · Activation gate
**AR.** ≥ ٢٥٠٬٠٠٠ ر.س ARR مُتَحقّق **أو** أول قطاع منظَّم (بنك / طاقة / صحة / حُكومة) مُوقَّع.  
**EN.** ≥ 250K SAR ARR realized **or** first regulated-sector engagement signed (banking / energy / healthcare / government).

### النِطاق · Scope
**AR.** يَملك خَمسة عَناصر:
1. **خَطّ شركاء مُرسَيين** — Big 4 خليجي، معالج مرخَّص من SAMA، VC سعودي.
2. **التَواصل** — مُسوَّدات ثنائية اللغة، بدون تجريف / واتساب بارد / LinkedIn auto.
3. **ميثاق الشركاء** — مَوَقَّع قبل أي تَعاون تَشغيلي.
4. **مَلاحظات الاجتماعات** — قابلة للتدقيق في Audit Chain.
5. **تَتبّع التَعريفات** — كل تَعريف يَنتهي بنَتيجة مُوَثَّقة.

**EN.** Owns five elements: anchor partner pipeline (Big 4 GCC, SAMA-licensed processor, Saudi VC), outreach (bilingual drafts, no scraping / cold WhatsApp / LinkedIn auto), Partner Covenant (signed before any operational collaboration), meeting notes (auditable in the audit chain), intro tracking (every intro ends in a documented outcome).

### شُروط عَدَم التَوظيف · Do-not-hire conditions
**AR.**
1. لا اهتمام شريك حقيقي (لا اجتماع شريك واحد بدا فيه ميثاق الشركاء).
2. لا نَموذج رِبْحٍ تشاركي مُوَضَّح (الأرقام بَعد لم تَستقرّ).
3. المؤسس لم يَلتقِ بنَفسه ٣ شركاء مُحتمَلين على الأقل قبل التَوظيف.
4. لم يَجتز إِشارات عَدَم التَوظيف في [`HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md) (بطاقة #٣).

**EN.** Do not hire if: (a) no real partner interest — no partner meeting in which the Covenant was tabled; (b) no clear rev-share model — numbers not yet settled; (c) founder has not met at least 3 prospective partners personally before hiring; (d) candidate fails Card #3 no-hire signals.

### لماذا هذا الدور ثالثاً · Why this role third
**AR.** التَوسّع بقيادة الشركاء يَتطلّب أَوّلاً وجود إثبات قابل للعَرض. قبل ٢٥٠ ألف ARR أو قطاع منظَّم موقَّع، لا يوجد ما يَستحق ميثاق شركاء. شَريك Big 4 لا يَلتزم بمنصة بلا إثبات.

**EN.** Partner-led expansion requires a showable proof first. Before 250K ARR or a signed regulated sector, there is nothing worth a Partner Covenant for. A Big 4 partner does not commit to a platform without proof.

---

## ٥. الانضباط العامّ · General discipline

**AR.** أربع قَواعد تَنطبق على الثلاثة:
1. التَوظيف لسَجل تَنفيذي مُنجَز، لا للإمكان.
2. كل دور له بطاقة في [`HIRING_SCORECARDS.md`](./HIRING_SCORECARDS.md). لا تَوظيف بلا بطاقة.
3. ٩٠ يوم تَجريبية مَع OKR صريحة. الإِخفاق في OKR لا يَستدعي تَمديداً، بل خُروجاً.
4. كل تَوظيف يَنتج Capital Asset جَديداً في السجل (إِضافة إلى أَدائه).

**EN.** Four rules across all three: hire for executed track record, not potential; every role has a scorecard — no hire without one; 90-day probation with explicit OKRs — failure does not extend, it exits; every hire ships at least one new Capital Asset into the registry on top of their day-to-day output.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
