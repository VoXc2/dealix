# GCC Go-To-Market Sequence — تَسلسل الدخول إلى السوق الخليجيّ

> ١٢ شهراً. السعودية أوّلاً وثانياً وثالثاً. الإمارات بعد دراسة الحالة. قطر أو الكويت بعد الإمارات. لا قَفز.

مرجع الإيقاع التشغيلي للمؤسّس: `docs/ops/FOUNDER_90_DAY_CADENCE.md`.

## ١. التَسلسل — بالعربية

### المرحلة ١ — الأشهر ١–٣: ترسيخ السعودية

**الهدف**: ٣ ريتينرات سعوديّة موقّعة + Sprint رئيسي واحد مُغلق.

- **الأسبوع ١–٤**: تَفعيل قناة تَشخيص استراتيجي مجاني، ١٥–٢٠ تَشخيصاً مُسلَّماً. مَعلمة: ٥ تَشخيصات/أسبوع.
- **الأسبوع ٥–٨**: رَفع ٥ تَشخيصات إلى ريتينر بسعر ٤٬٩٩٩ ر.س/شهر. مَعلمة: ٣ ريتينرات موقّعة.
- **الأسبوع ٩–١٢**: إطلاق Sprint ذكاء الإيرادات بسعر ٢٥٬٠٠٠ ر.س مع عميل واحد. مَعلمة: Proof Pack موقّع.

**بوّابة قرار يوم ٩٠**: إذا لم تُغلَق ٣ ريتينرات أو Sprint واحد، تُؤجَّل المرحلة ٢ ولا تُفتَح أي محادثة إماراتيّة. لا تَوسيع قبل الإثبات.

### المرحلة ٢ — الأشهر ٤–٦: نَشر دراسة الحالة + فتح تَجريب إماراتي

**الهدف**: دراسة حالة مجهولة الهويّة منشورة + محادثة إماراتيّة أوّلى عبر إحالة شريك.

- **الأسبوع ١٣–١٦**: تَوليد دراسة حالة من Sprint سعودي. مَعلمة: مسوَّدة موقّعة من العميل.
- **الأسبوع ١٧–٢٠**: تَوظيف شريك Big 4 أو منصّة VC لإحالة إماراتيّة. مَعلمة: ٣ محادثات إماراتيّة مُسجَّلة في friction_log.
- **الأسبوع ٢١–٢٤**: تَسليم ٣ تَشخيصات استراتيجيّة مجانيّة لمشترين إماراتيّين. مَعلمة: ٣ تَشخيصات بَسلسلة تدقيق كاملة.

**بوّابة قرار يوم ١٨٠**: إذا لم تُسجَّل ٣ محادثات إماراتيّة بإحالة شريك موثَّقة، تُؤجَّل المرحلة ٣. لا فتح كيان قبل عقد.

### المرحلة ٣ — الأشهر ٧–٩: أوّل ريتينر إماراتي + نَطاق قطر

**الهدف**: ريتينر إماراتي موقّع + خطّة قطر مَكتوبة.

- **الأسبوع ٢٥–٢٨**: تَرقية تَشخيص إماراتي إلى ريتينر بـ ٤٬٩٩٩ ر.س ما يُعادل بالدرهم. مَعلمة: عقد موقّع.
- **الأسبوع ٢٩–٣٢**: تَوثيق انحرافات ADGM/DIFC في Trust Pack الإماراتي. مَعلمة: خرائط مَناطق حرّة محدَّثة.
- **الأسبوع ٣٣–٣٦**: مَسح أوّلي لقطر مع شريك محلّي محتمَل. مَعلمة: مَوقف من ٣ مَشترين قطريين موثَّق.

**بوّابة قرار يوم ٢٧٠**: إذا لم يُوقَّع ريتينر إماراتي واحد، يَتوقّف التَوسّع جنوباً.

### المرحلة ٤ — الأشهر ١٠–١٢: تَجريب قطر أو الكويت

**الهدف**: تَجريب مَدفوع واحد في قطر أو الكويت.

- **الأسبوع ٣٧–٤٠**: اختيار قطر أو الكويت بناءً على قُرب شريك مَوثوق. مَعلمة: قرار موقّع.
- **الأسبوع ٤١–٤٤**: تَسليم Sprint مُصغّر (ليس مُخفَّض السعر) لعميل واحد. مَعلمة: Proof Pack موقّع.
- **الأسبوع ٤٥–٤٨**: تَحديث `gcc_markets.py` لرَفع حالة السوق إلى `pilot_ready`. مَعلمة: اختبار e2e ناجح.

**بوّابة قرار يوم ٣٦٥**: مراجعة كامل التَسلسل. تَحديد ما إذا كان التَسلسل الـ ١٢-شهري الثاني يَتجه إلى قطر+الكويت أو إلى تَعميق السعودية والإمارات.

### كَتالوج الأنماط المُضادّة

- **لا تَدخل سوقاً بدون كيان قانوني محلّي أو شريك مرخَّص**. الفاتورة بالعملة المحلّيّة ليست تَكتيكاً، هي اشتراط.
- **لا تُتَرجم العقيدة قبل الإطلاق**. الـ ١١ موجود بـ AR + EN في `non_negotiables.py`. تَرجمة قبل وجود مُشتري هي مَضيعة وقت.
- **لا تُخفّض السعر لدخول سوق جديد**. السعر السعودي هو السقف. تَخفيضه يَكسر دوّاب الإحالة.
- **لا تَعلن قبل الفَوترة**. أوّل خبر عن سوق جديد هو الفاتورة المُرسَلة، ليس البيان الصحفي.
- **لا تَستخدم بيانات سعوديّة في تَدريب يَخدم عميلاً إماراتياً**. PDPL Article 18 يَحكم هذا.

---

## 1. The sequence — English

### Phase 1 — Months 1–3: Saudi consolidation

**Goal**: 3 Saudi retainers signed + 1 flagship Sprint closed.

- **Weeks 1–4**: activate the Strategic Diagnostic channel; deliver 15–20 diagnostics. Milestone: 5 diagnostics per week.
- **Weeks 5–8**: convert 5 diagnostics to the 4,999 SAR/month Governed Ops Retainer. Milestone: 3 retainers signed.
- **Weeks 9–12**: run the 25,000 SAR Revenue Intelligence Sprint with one client. Milestone: signed Proof Pack.

**Day-90 decision gate**: if 3 retainers or 1 Sprint are not closed, Phase 2 is postponed and no UAE conversation is opened. No expansion before proof.

### Phase 2 — Months 4–6: case study published + UAE pilot opened

**Goal**: anonymized case study published + first UAE conversation via partner referral.

- **Weeks 13–16**: generate a case study from the Saudi Sprint. Milestone: client-signed draft.
- **Weeks 17–20**: engage a Big 4 partner or VC platform for a UAE referral. Milestone: 3 UAE conversations logged in the friction log.
- **Weeks 21–24**: deliver 3 Strategic Diagnostics to UAE buyers. Milestone: 3 diagnostics with full audit chain.

**Day-180 decision gate**: if 3 partner-referred UAE conversations are not recorded, Phase 3 is postponed. No entity opened without a contract.

### Phase 3 — Months 7–9: first UAE retainer + Qatar scoping

**Goal**: UAE retainer signed + written Qatar plan.

- **Weeks 25–28**: convert a UAE diagnostic to a retainer at 4,999 SAR-equivalent in AED. Milestone: signed contract.
- **Weeks 29–32**: document ADGM / DIFC deviations inside the UAE Trust Pack. Milestone: updated free-zone maps.
- **Weeks 33–36**: initial Qatar scan with a possible local partner. Milestone: documented stance from 3 Qatari buyers.

**Day-270 decision gate**: if no UAE retainer is signed, southern expansion halts.

### Phase 4 — Months 10–12: Qatar OR Kuwait pilot

**Goal**: one paid pilot in Qatar or Kuwait.

- **Weeks 37–40**: pick Qatar or Kuwait based on partner proximity. Milestone: signed decision.
- **Weeks 41–44**: deliver a scoped-down Sprint (not price-discounted) for one client. Milestone: signed Proof Pack.
- **Weeks 45–48**: update `gcc_markets.py` to promote the market to `pilot_ready`. Milestone: passing e2e test.

**Day-365 decision gate**: review the full sequence. Decide whether the second 12-month cycle targets Qatar + Kuwait expansion or deeper consolidation in Saudi + UAE.

### Anti-pattern catalog

- **Do not enter a market without a local legal entity or licensed partner**. Local-currency invoicing is not a tactic; it is a precondition.
- **Do not translate the Doctrine before launch**. The 11 already exist in AR + EN inside `non_negotiables.py`. Translating before a buyer exists is wasted motion.
- **Do not discount pricing to enter a new market**. The Saudi price is the floor. Discounting it breaks the referral loop.
- **Do not announce before invoicing**. The first news from a new market is the sent invoice, not the press release.
- **Do not use Saudi data to train output serving a UAE client**. PDPL Article 18 governs this.

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
