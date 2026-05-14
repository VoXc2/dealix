# الأسئلة الاستثمارية الحادّة — Investor Q&A
## ١٢ سؤالاً، ١٢ إجابة، كل إجابة تَستشهد بسطر كود أو وَثيقة — 12 sharp questions, each answer cites a code surface or doc

---

## س ١ · Q1 — من مُنافسوكم؟ · Who are your competitors?

**AR.** ثلاث فئات: (أ) ممارسات Big 4 الخليجية — تُقدّم تَقارير لا منصّات. (ب) مَزوّدو الموديلات الأَجانب (OpenAI، Anthropic، Google) — يُقدّمون قُدرة لا حوكمة محلّية. (ج) منصّات MLOps العامّة — تَفترض موافقة المستخدم النهائي لا موافقة الشركة على كل فِعل خارجي. لا أَحد من الثلاث يَملك طَبقة العمليات بين الموديل والمشتري المنظَّم سعودياً. مرجع: [`docs/funding/WHY_NOW_GCC_AI_OPS.md`](./WHY_NOW_GCC_AI_OPS.md).

**EN.** Three categories: (a) GCC Big 4 practices — they ship reports, not platforms; (b) foreign model vendors — capability, not local governance; (c) general MLOps platforms — assume end-user consent, not firm-level approval on every external action. None of the three owns the operations layer between the model and the regulated Saudi buyer. Reference: [`docs/funding/WHY_NOW_GCC_AI_OPS.md`](./WHY_NOW_GCC_AI_OPS.md).

---

## س ٢ · Q2 — لماذا الخندق ليس مُجرَّد مَيزة منتَج يَنسخها مُنافس في رُبع سَنة؟ · Why isn't the moat just a product feature competitors clone in a quarter?

**AR.** المُنافس يَستطيع نَسخ نَصّ ١١ التزاماً (إنه عَلَني في `docs/THE_DEALIX_PROMISE.md`). لا يَستطيع نَسخ ١٢–١٨ شهراً من ارتباطات قابلة لإعادة التَشغيل عَبْر سلسلة التدقيق (`auto_client_acquisition/auditability_os/audit_event.py`)، ولا ثَقافة تَسقُط فيها مَطالب التَسليم لا الالتزامات. الخندق وَقت + مَوقف، لا نَصّ. تفاصيل في [`DEALIX_MOAT_STACK.md`](./DEALIX_MOAT_STACK.md).

**EN.** A competitor can clone the text of the 11 commitments (it's public). They cannot clone 12–18 months of audit-replay-able engagements (`auto_client_acquisition/auditability_os/audit_event.py`), nor a delivery culture in which deadlines bend before commitments do. The moat is time + posture, not text. See [`DEALIX_MOAT_STACK.md`](./DEALIX_MOAT_STACK.md).

---

## س ٣ · Q3 — تكلفة اكتساب العميل (CAC)؟ · Customer acquisition cost?

**AR.** غير مَقيسة بَعْد كَمّياً. المؤسس يُدير القَناة يَدوياً (٤ ساعات بَيع / يوم). لا اكتساب مَدفوع، لا تَجريف، لا واتساب بارد. التشخيص المجاني هو القَمع الأَعلى وتَكلفته يَوم عَمل لكل تَشخيص. سَنُسجّل CAC نَفترضه ≤ ٣٠٪ من قيمة الارتباط الأول بَعْد الفاتورة #٥، ونُعلنه عندَها. الافتراض ليس وَعداً.

**EN.** Not yet quantified. Founder runs the channel manually (4 hours sell / day). No paid acquisition, no scraping, no cold WhatsApp. Free Strategic Diagnostic is the top of funnel, costing one working day per diagnostic. We will report a measured CAC after Invoice #5, with a working assumption of ≤ 30% of first-engagement value — this is an assumption, not a promise.

---

## س ٤ · Q4 — كيف لا يُصبح التَوسّع الخليجي تَشتيتاً؟ · How does GCC expansion not become focus dilution?

**AR.** التَوسّع بقيادة الشركاء، لا بقيادة فِرَق محلّية. السعودية تَجاريّاً، الخليج عَقيدةً (`docs/gcc-expansion/GCC_EXPANSION_THESIS.md`). لا فَرع خليجي قبل أَوَّل قطاع منظَّم سعودي مُوَقَّع. CAP-012 (GCC Standardization Pack) قابل للقراءة عَبْر `/api/v1/gcc-market-intel`، وهو مَوقف عَلَني لا فَرع تَشغيلي. التَوسّع الحقيقي يَنتظر بَوّابة التَوظيف #٣.

**EN.** Partner-led, not local-team-led. Saudi commercially, GCC doctrinally (`docs/gcc-expansion/GCC_EXPANSION_THESIS.md`). No GCC branch before the first signed regulated Saudi sector. CAP-012 (GCC Standardization Pack) is readable via `/api/v1/gcc-market-intel` — it is a public posture, not an operational branch. Real expansion waits for Hire #3 gate.

---

## س ٥ · Q5 — ماذا لو بَنَت Big 4 نُسختها الخاصّة؟ · What if a Big 4 builds their own version?

**AR.** نَموذج Big 4 يَستند إلى الفَواتير بالساعة. المنصّة تَتنافس مَع الساعات القابلة للفَوْتَرة. لو بَنَت Big 4 منصّة، تُعارض نَموذج عَملها. الأَكثر تَرجيحاً: تَستخدم Dealix كَتَطبيق مَرجعي ضِمن خَدماتها، وهذا ما يُعالجه CAP-009 (Anchor Partner Outreach Kit) + ميثاق الشركاء.

**EN.** The Big 4 model is billable hours. A platform competes with billable hours. If a Big 4 builds a platform, it conflicts with their own model. The more likely outcome: they use Dealix as a reference implementation inside their services — which is exactly what CAP-009 (Anchor Partner Outreach Kit) and the Partner Covenant in [`docs/40_partners/PARTNER_COVENANT.md`](../40_partners/PARTNER_COVENANT.md) address.

---

## س ٦ · Q6 — ماذا لو خَفّت إِنفاذات PDPL؟ · What if PDPL enforcement loosens?

**AR.** الفَرضية لا تَستند فقط إلى PDPL. تَستند إلى أَربع قُوى مُتَقاطعة: PDPL + NDMO + رؤية ٢٠٣٠ + ضَخّ استثمار الذكاء الاصطناعي الخليجي. تَراجُع واحدة لا يُلغي الثلاث. وحتى بدون PDPL، CISO سعودي يَطلب سلسلة تَدقيق قبل تَوقيع تَكامل ذكاء اصطناعي مَع موديل أجنبي — هذا سُلوك مُشترٍ، لا إِلزام تَنظيمي.

**EN.** The thesis does not rest on PDPL alone. It rests on four intersecting forces: PDPL + NDMO + Vision 2030 + GCC AI infrastructure investment. One easing does not cancel the other three. And even without PDPL, a Saudi CISO requires an audit chain before signing an AI integration with a foreign model — this is buyer behavior, not regulatory mandate.

---

## س ٧ · Q7 — كيف تَحمي ضِدّ تَبَنّي العَقيدة المفتوحة بدون Dealix كَتَطبيق مَرجعي؟ · How do you defend against open-doctrine adoption without Dealix as reference implementation?

**AR.** التَبَنّي العَلَني للعَقيدة هو الهَدف، لا التَهديد. لو تَبَنّت ١٠ شَركات إطار `open-doctrine/`، يُصبح المعيار. التَطبيق المَرجعي هو الذي يَتلقّى المُكافأة، لأن المعيار يَكون له ١٠ مُسَوِّقين بدلاً من واحد. سَجل تاريخي مُماثل: Kubernetes (مَفتوح) + Red Hat (تَطبيق مَرجعي).

**EN.** Open-doctrine adoption is the goal, not the threat. If 10 firms adopt the `open-doctrine/` framework, it becomes a standard. The reference implementation reaps the reward because the standard then has 10 advocates instead of one. Historical pattern: Kubernetes (open) + Red Hat (reference implementation).

---

## س ٨ · Q8 — ما حَجم السوق (TAM)؟ · What is the TAM?

**AR.** لا نَعرض TAM بدون مَرجع عام. عدد شركات خَدمات B2B السعودية في الفئة المُستهدَفة (٥٠–٥٠٠ موظف) قابل للحساب من سجلّات هيئة الإِحصاء والغُرَف التجارية، لكنه ليس "السوق القابل للالتقاط". القابل للالتقاط هو فِئة فَرعيّة قابلة للتَأهيل عَبْر التشخيص المجاني. سَنُحدّد رقماً مَنشوراً عند الفاتورة #١٠.

**EN.** We do not present a TAM without a public source. The count of Saudi B2B services firms in the target band (50–500 employees) is derivable from public registries (GASTAT, Chamber of Commerce filings), but that is not "addressable market". Addressable is a sub-band qualifiable via the free Strategic Diagnostic. We will publish a number at Invoice #10, sourced.

---

## س ٩ · Q9 — لماذا الآن وليس قبل سَنتَين؟ · Why now and not two years ago?

**AR.** قبل سَنتَين: لم يَكن PDPL في تَطبيقه التَشغيلي، NDMO لم يَنشر إِطار المسار، الموديلات اللغوية الكُبرى لم تَدخل قاعدة المُشترين السعوديين، الاستثمار في البنية التحتية الخليجية لم يَكن بحَجمه الحالي. الفجوة التي يَملؤها Dealix تَفتحت في ٢٠٢٥. مَن يَستجيب أَوَّلاً، يَكتب القَواعد.

**EN.** Two years ago: PDPL was not yet operational, NDMO had not published the lineage framework, large language models had not entered the Saudi buyer base at current scale, GCC infrastructure investment was not at its current magnitude. The gap Dealix fills opened in 2025. The first responder writes the rules.

---

## س ١٠ · Q10 — كم تَحتاجون من الفاتورة #١ إلى البَذرة الكاملة؟ · How much from Invoice #1 to a full seed round?

**AR.** ٥٠٠ ألف ر.س تَقديريّاً تُغطّي ١٢–١٥ شهراً (السيناريو ب في [`USE_OF_FUNDS.md`](./USE_OF_FUNDS.md)). البَذرة الكاملة (≥ ٢ مليون ر.س) تُؤجَّل إلى ٢٥٠ ألف ARR أو أول قطاع منظَّم. لا نَطلب بَذرة الآن لأن السوق لم يُؤكّد المُنتَج بَعْد. الطَلب الحالي: تَعريف بشريك واحد + مستشار واحد + نَافذة مُراجَعة عند الفاتورة #٢.

**EN.** ~500K SAR covers 12–15 months (Scenario B in [`USE_OF_FUNDS.md`](./USE_OF_FUNDS.md)). A full seed (≥ 2M SAR) waits until 250K ARR or first regulated sector. We are not asking for a seed now because the market has not yet validated the product. Current ask: one partner intro + one advisor + a review window at Invoice #2.

---

## س ١١ · Q11 — ماذا لو وَصلت الفاتورة #١ مُتأخّرة ٦ أشهر؟ · What if Invoice #1 arrives 6 months late?

**AR.** نُعيد فَتْح [`PRICING_REFRAME_2026Q2.md`](../sales-kit/PRICING_REFRAME_2026Q2.md) عند الشهر الثالث إذا لم يَصل ARR إلى ١٥ ألف. خَفض الأرضية إلى ٢٬٩٩٩ ر.س / شهر مَفتوح ضِمن سَجل القرارات، لكن لن نَنزل تَحت ٢٬٩٩٩ هذه السَنة. لو الفاتورة #١ تأخّرت أكثر من ٦ أشهر، نُعيد كتابة الفَرضية كاملةً، لا نَزيد إِنفاق التَسويق.

**EN.** We reopen [`PRICING_REFRAME_2026Q2.md`](../sales-kit/PRICING_REFRAME_2026Q2.md) at month 3 if ARR has not reached 15K. Lowering the floor to 2,999 SAR/month is on the decision log, but we will not go below 2,999 this year. If Invoice #1 slips past 6 months, we rewrite the thesis — we do not increase marketing spend.

---

## س ١٢ · Q12 — لماذا يَجب أن يَتحدّث المُستثمر إليكم الآن وليس عند البَذرة؟ · Why should an investor talk to you now and not at the seed?

**AR.** السبب الوحيد: الوَصول إلى شريك مُرسٍ. المُستثمر الذي يُعرّفنا اليوم بشريك Big 4 خليجي أو معالج SAMA، يَدخُل الجولة لاحقاً بمَوقع أفضل من المُستثمر الذي يَنتظر مَلَفّ الإيراد. خِلاف ذلك، الجواب الصادق: لا حاجة عاجلة الآن، انتظر الفاتورة #٢. هذه أَمانة لا فَرض ضَغط.

**EN.** Only reason: access to an anchor partner. The investor who introduces us today to a GCC Big 4 partner or SAMA-licensed processor enters a later round in a better position than the investor waiting for the revenue file. Otherwise the honest answer: no urgency now, wait for Invoice #2. This is honesty, not pressure.

---

## مراجع · References

- [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md)
- [`docs/funding/FUNDING_MEMO.md`](./FUNDING_MEMO.md)
- [`docs/funding/DEALIX_MOAT_STACK.md`](./DEALIX_MOAT_STACK.md)
- [`docs/funding/CAPITAL_ASSET_TRACTION.md`](./CAPITAL_ASSET_TRACTION.md)

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
