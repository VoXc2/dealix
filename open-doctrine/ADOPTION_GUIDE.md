# Adoption Guide — دليل التبنّي

_Four tiers. Read, align, comply, or certify. Tiers 1–3 are free and open. Tier 4 is the only commercial relationship in this repository._

## EN — Choosing a tier

Most teams will start at tier 1 (awareness) and progress as their operations mature. There is no requirement to advance, and there is no penalty for stopping. The doctrine is more useful as a careful tier-1 read than as a sloppy tier-3 implementation. Pick the tier the team can sustain.

## AR — اختيار المرحلة

تبدأ معظم الفِرق من المرحلة الأولى (الوعي) وتتقدّم مع نضج العمليات. لا إلزام بالتقدّم ولا عقوبة على التوقف. القراءة المتأنية للمرحلة الأولى أنفع من تطبيق متعجّل للمرحلة الثالثة. اختر المرحلة التي تستطيع إدامتها.

---

## Tier 1 — Doctrine awareness — الوعي بالدستور

**EN.** The team reads the doctrine. No code changes. No tests. The team gains a shared vocabulary for AI-operations risk and a yardstick for evaluating vendors and internal builds.

**AR.** يقرأ الفريق الدستور. لا تعديل على الشيفرة ولا اختبارات. يحصل الفريق على مفردات مشتركة لمخاطر تشغيل AI ومعيار لتقييم الموردين والبناء الداخلي.

**What to read:**

1. [`README.md`](./README.md)
2. [`GOVERNED_AI_OPS_DOCTRINE.md`](./GOVERNED_AI_OPS_DOCTRINE.md) — the canonical text.
3. [`11_NON_NEGOTIABLES.md`](./11_NON_NEGOTIABLES.md) — the 5-minute reference.

**Time investment:** 60–90 minutes for one engineer; one all-hands for a small team.

**Outcome:** the team can name the 11 commitments and explain why each exists. The team can identify which of its current practices align and which do not. No claim of adoption is appropriate at this tier.

**Cost:** free.

---

## Tier 2 — Doctrine alignment — مواءمة الدستور

**EN.** The team runs the implementation checklist against its own codebase and remediates every "no". No formal test suite yet; the goal is to close the operational gaps the checklist exposes.

**AR.** يُنفّذ الفريق قائمة التبنّي على قاعدته البرمجية ويعالج كل "لا". لا توجد بعد مجموعة اختبارات رسمية؛ الهدف إغلاق الفجوات التشغيلية التي تكشفها القائمة.

**What to do:**

1. Walk [`IMPLEMENTATION_CHECKLIST.md`](./IMPLEMENTATION_CHECKLIST.md) end-to-end.
2. For each "no" answer, file a remediation ticket with the suggested fix.
3. Close every remediation ticket; re-walk the checklist until every item is "yes".
4. Document the evidence per item in an internal control register the team can show on request.

**Time investment:** 4–12 weeks for a typical AI consultancy, depending on legacy debt.

**Outcome:** the team's day-to-day operations match the doctrine. Public messaging can state "operations aligned with the Governed AI Operations Doctrine" — not "certified", not "Dealix-approved".

**Cost:** free. (Internal engineering time is the only cost.)

---

## Tier 3 — Doctrine compliance — التوافق المُختبَر

**EN.** The team writes the test suite that enforces each control. Every commitment is covered by at least one passing automated test. The test suite runs on every PR. A commitment with zero passing tests is documented as a gap, not claimed as covered.

**AR.** يكتب الفريق مجموعة الاختبارات التي تُنفّذ كل ضابط. كل التزام مُغطّى باختبار آلي ناجح واحد على الأقل. مجموعة الاختبارات تعمل على كل PR. الالتزام بلا اختبار يُوثَّق كفجوة، لا يُدّعى تغطيته.

**What to do:**

1. For each row in [`CONTROL_MAPPING.md`](./CONTROL_MAPPING.md), identify the test category the team will implement.
2. Write a test in the team's own framework that exercises the control on a real code path.
3. Wire the test suite into the team's PR pipeline; a failing doctrine test blocks the PR.
4. Publish a short internal monthly report listing the doctrine tests, pass rate, and remediations.

**Time investment:** 6–16 weeks once tier 2 is complete.

**Outcome:** the team can demonstrate the doctrine is enforced in production, not aspirational. Public messaging can state "doctrine tests run on every release". The team can hire and onboard against a measurable bar.

**Cost:** free. (Internal engineering time is the only cost.)

---

## Tier 4 — Certified by Dealix — مُعتمَد من Dealix

**EN.** The team requests a paid review by Dealix, the doctrine's maintainer. Dealix examines the team's control register, runs sample evidence retrievals, and produces a Proof Pack of the review. If the review passes, the team receives a time-bounded statement of certification (12 months) with a versioned doctrine reference. The certification is the only commercial relationship offered by this repository.

**AR.** يطلب الفريق مراجعة مدفوعة من Dealix، الجهة المُشرفة على الدستور. تفحص Dealix سجل الضوابط الداخلي، وتُشغّل عيّنات لاسترجاع الإثباتات، وتُنتج Proof Pack للمراجعة. إذا اجتازت المراجعة، يستلم الفريق بياناً معتمداً محدّد المدة (١٢ شهراً) مع إشارة إلى إصدار الدستور. هذه المرحلة هي العلاقة التجارية الوحيدة التي يقدّمها هذا المستودع.

**What it is:**

- An independent, paid review against the 11 commitments.
- A bilingual Proof Pack of the review, signed by the Dealix maintainer.
- A versioned doctrine reference (e.g., "Doctrine 0.1.0 certified, 2026-05-14, valid until 2027-05-14").
- Permission to state "certified by Dealix against Governed AI Operations Doctrine vX.Y.Z" for the duration.

**What it is NOT:**

- Not a legal certification.
- Not regulatory approval.
- Not a substitute for jurisdictional law (PDPL, GDPR, NDMO, sector regulators).
- Not a guarantee of any outcome; the certification confirms the controls were observed during the review window. Operations after the review are the team's responsibility.

**Commercial review terms:**

The fee, scope, exclusions, deliverables, and dispute resolution for the paid review are documented in the Dealix commercial pack. Adopters considering tier 4 should request that document directly. Pricing and the commercial pack are intentionally outside this open repository; see [`docs/sales-kit/INVESTOR_ONE_PAGER.md`](../docs/sales-kit/INVESTOR_ONE_PAGER.md) for the commercial-review intake link maintained by Dealix.

**Time investment:** 2–6 weeks of Dealix review time after submission.

**Cost:** paid. Quoted per engagement after a scoping call. No published list price.

**Constraint.** Tier 4 is the **only** commercial relationship in this repository. Tiers 1, 2, and 3 are free and open in perpetuity. The doctrine is not gated; only the certification is.

---

## Frequently expected questions — أسئلة متوقّعة

### EN

**Q. Do we need Dealix's permission to adopt the doctrine?**
No. Tiers 1, 2, and 3 are free and open. Attribution per the CC BY 4.0 license is required.

**Q. Can we claim "certified" without tier 4?**
No. "Certified by Dealix" is reserved to tier 4. Teams at tier 2 or tier 3 may state "aligned with" or "doctrine tests run on every release".

**Q. Will the doctrine change?**
Yes. The doctrine is versioned. Existing certifications reference the version under which they were issued. A new version does not invalidate an older certification mid-term.

**Q. Does Dealix offer implementation services?**
This repository does not. The doctrine is open; Dealix's commercial implementation work is separate from the open framework and is not covered here.

### AR

**س. هل نحتاج إذناً من Dealix للتبنّي؟**
لا. المراحل الأولى والثانية والثالثة مفتوحة ومجانية. يلزم الإسناد بموجب CC BY 4.0.

**س. هل يمكننا ادعاء "مُعتمَد" دون المرحلة الرابعة؟**
لا. "مُعتمَد من Dealix" محصور بالمرحلة الرابعة. الفِرق في المرحلتين الثانية أو الثالثة تقول "متوافق مع" أو "اختبارات الدستور تعمل على كل إصدار".

**س. هل سيتغيّر الدستور؟**
نعم. الدستور مُصدَّر. الاعتمادات القائمة تُشير إلى الإصدار الذي صدرت تحته. الإصدار الجديد لا يُلغي اعتماداً سابقاً قبل انتهاء مدته.

**س. هل تقدّم Dealix خدمات تطبيق؟**
ليس عبر هذا المستودع. الدستور مفتوح؛ أعمال التطبيق التجارية لـ Dealix منفصلة عن الإطار المفتوح وليست مشمولة هنا.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
