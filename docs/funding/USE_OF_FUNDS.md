# استخدام التمويل — Use of Funds
## سيناريوهان صريحان، لا نِسَب بلا خطة مُكلِّفة — Two scenarios, no percentages without a costed plan

---

## ١. الفرضية · The premise

**AR.** نَعرض سيناريوهَين فقط: التمويل الذاتي من الفواتير، والتمويل الملائكي / قبل البذرة. لا نَعرض نِسَب توزيع مالية دون خطة مُكلِّفة بنداً بنداً. الأرقام التقديرية الواردة هنا أرضيات تشغيل، لا تَوقّعات نتائج.

**EN.** Two scenarios only: bootstrapped from invoices, and angel / pre-seed funded. No percentage allocations without a costed plan. Figures here are operating floors, not outcome forecasts.

---

## ٢. السيناريو أ — تمويل ذاتي من الفواتير · Scenario A — Bootstrapped from invoices

**AR.** الفرضية: لا يَدخُل تمويل خارجي، الإيراد يَأتي من سلّم العروض الثلاثة (`auto_client_acquisition/service_catalog/registry.py`). الأولويات بترتيب:

### الأولوية ١ — بيع يَقوده المؤسس
- المؤسس يَخصص ٤ ساعات / يوم للبيع (وفق التزام تَقويم المؤسس في [`docs/sales-kit/PRICING_REFRAME_2026Q2.md`](../sales-kit/PRICING_REFRAME_2026Q2.md)).
- لا اكتساب مدفوع. لا إعلانات. لا تجريف. التشخيص المجاني هو أعلى القمع.
- مقاييس: عَدَد التشخيصات المُسلَّمة، تحويل تشخيص → ريتينر، تحويل تشخيص → سبرنت.

### الأولوية ٢ — أتمتة التسليم
- كل ارتباط يَستهلك ساعات. لا توظيف قبل الفاتورة #٣.
- التحسين عَبْر Claude يَكتب الكود، والمؤسس يَراجع ويَعتمد.
- مقاييس: ساعات تسليم لكل ارتباط، عَدَد ارتباطات متزامنة قابلة للتشغيل.

### الأولوية ٣ — مُولِّد Proof Pack
- CAP-006 يُؤتمت توليد Proof Pack من سجل الارتباط.
- يَقلّص زمن الإغلاق من أيام إلى ساعات.

### الأولوية ٤ — مكتبة الأصول الرأسمالية
- كل ارتباط يَودع أصلاً واحداً على الأقل (الالتزام #١١).
- السجل العام يَنمو بصمت.

### الأولوية ٥ — حركة الشركاء
- CAP-009 — Anchor Partner Outreach Kit يُفعَّل عَبْر `scripts/seed_anchor_partner_pipeline.py`.
- ثلاثة لقاءات شركاء مَستهدَفة في الربع الأول من تَفعيل القناة.

**EN.** Bootstrapped path: no outside capital. Revenue from the 3-offer ladder. Priorities, in order: (1) founder-led sell, 4 hours/day per the cadence in [`docs/sales-kit/PRICING_REFRAME_2026Q2.md`](../sales-kit/PRICING_REFRAME_2026Q2.md) — no paid acquisition, no scraping; (2) delivery automation, Claude writes code, founder reviews; (3) Proof Pack generator (CAP-006) — close in hours, not days; (4) Capital Asset Library, one deposit per engagement (commitment #11); (5) partner motion, activate CAP-009 via `scripts/seed_anchor_partner_pipeline.py`. Hiring is deferred until ≥ 50K SAR ARR per [`docs/funding/FIRST_3_HIRES.md`](./FIRST_3_HIRES.md).

---

## ٣. السيناريو ب — تمويل ملائكي / قبل البذرة (~٥٠٠ ألف ر.س) · Scenario B — Angel / pre-seed (~500K SAR)

**AR.** الفرضية: مبلغ تقديري ٥٠٠ ألف ر.س يُغطّي ١٢–١٥ شهراً من المدرَج التشغيلي، مع توظيف مَشروط بالإيراد لا بالنقد. الأولويات بترتيب:

### الأولوية ١ — أول مهندس عمليات ذكاء اصطناعي
- يَملك خط Source Passport + governance runtime + أتمتة Proof Pack + Evidence Graph.
- بَوّابة التوظيف: ≥ ٥٠٬٠٠٠ ر.س ARR متَحقّق. لا تَوظيف قبل الإيراد، حتى مع وجود نقد.
- تفاصيل في [`docs/funding/FIRST_3_HIRES.md`](./FIRST_3_HIRES.md).

### الأولوية ٢ — أول مشغّل تسليم / RevOps
- يَملك تسليم Revenue Intelligence Sprint + تَجميع بيانات العميل + مسوّدات Proof Pack + تقارير القيمة الشهرية.
- بَوّابة التوظيف: ≥ ١٠٠٬٠٠٠ ر.س ARR.

### الأولوية ٣ — تَمنيج طبقة الإثبات والثقة
- تَحويل Proof Pack + Trust Pack من تَشغيل يَدوي بمساعدة الكود إلى منتَج قابل للبيع كوحدة منفصلة.
- يَفتح أَفقاً ثانياً للإيراد بَعْد سلّم العروض.

### الأولوية ٤ — تَطوير شركاء الخليج
- تَفعيل ٣ أنماط شركاء معرَّفة (Big 4 GCC، معالج مرخَّص من SAMA، VC سعودي).
- ميثاق شركاء + نموذج رِبْحٍ تشاركي مُوقَّع.

### الأولوية ٥ — جاهزية الأمن والتدقيق
- مُراجعة أمنية مستقلّة لـ governance_os + secure_agent_runtime_os.
- جاهزية ISO/SOC 2 خفيفة كَأَساس لمُحادثات الشركات المنظَّمة.

**EN.** Pre-seed estimate ~500K SAR covers 12–15 months of operating runway, with hires gated on revenue, not on cash. Order: (1) First AI Ops Engineer — owns Source Passport pipeline, governance runtime, Proof Pack automation, evidence graph; gate ≥ 50K SAR ARR. (2) First Delivery/RevOps Operator — owns Sprint delivery, client data intake, Proof Pack drafts, monthly Value Reports; gate ≥ 100K SAR ARR. (3) Trust/Evidence productization — Proof Pack + Trust Pack as standalone purchasable units. (4) GCC partner development — activate three archetypes. (5) Security + audit readiness — independent review of `governance_os` + `secure_agent_runtime_os`; ISO/SOC 2 lite groundwork for regulated buyers.

---

## ٤. ما لا نُخصِّصه · What we do not allocate

**AR.** لا نُخصِّص للإعلانات. لا للتجريف ولا لأدوات الواتساب البارد ولا لأتمتة LinkedIn — كلها محجوبة في الكود. لا للمؤتمرات الكبيرة قبل الفاتورة #٥. لا لمستشار تسويق قبل الفاتورة #٥. كل بَنْد مُستبعَد هنا مُستبعَد بسبب الانضباط، لا بسبب الميزانية.

**EN.** No allocation to: paid advertising; scraping, cold WhatsApp, or LinkedIn automation tooling (all blocked in code per the 11 commitments); large conferences before Invoice #5; a marketing advisor before Invoice #5. Each exclusion is by discipline, not by budget.

---

## ٥. نقطة قرار · Decision point

**AR.** نُعيد فتح هذا الملف عند الفاتورة #٢، وعند بلوغ ٥٠ ألف ر.س ARR، وعند توقيع أول قطاع منظَّم. كل واحدة من الثلاث تَفتح بَوّابة قرار جديدة، لا بَنْد إنفاق جديد.

**EN.** This doc reopens at Invoice #2, at 50K SAR ARR, and at the first signed regulated-sector engagement. Each event opens a new decision gate, not a new spend line.

---

## مراجع · References

- [`docs/funding/FUNDING_MEMO.md`](./FUNDING_MEMO.md)
- [`docs/funding/HIRING_PLAN.md`](./HIRING_PLAN.md)
- [`docs/funding/FIRST_3_HIRES.md`](./FIRST_3_HIRES.md)

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
