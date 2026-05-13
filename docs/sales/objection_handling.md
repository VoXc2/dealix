# إجابات الاعتراضات / Objection Handling (Dealix)

دليل عملي لـ 12 اعتراضًا شائعًا من العملاء السعوديين. كل اعتراض يحتوي:
- **الاعتراض كما يُقال** (AR + EN).
- **ما خلف الاعتراض** (الخوف الحقيقي).
- **الرد المُعتمد** (بأدلة لا بادعاءات).
- **سؤال التوجيه** للانتقال للخطوة التالية.

> **مبدأ:** الاعتراض = طلب معلومات، وليس رفضًا. أجب بهدوء، باستشهاد، ودائمًا بسؤال يفتح الحوار.

> **مراجع:** [`sales_script.md`](./sales_script.md) · [`offer_pages/`](./offer_pages/) · [`../../templates/outbound_messages.md`](../../templates/outbound_messages.md)

---

## 1. "غالي" / "Too expensive"

**الاعتراض (AR):** "9,500 ريال كثير على عشرة أيام."
**الاعتراض (EN):** "SAR 9,500 for 10 days is too much."

**ما خلف الاعتراض:** العميل لا يرى القيمة المباشرة، أو يقارن بسعر "موظف فريلانس".

**الرد (AR):**
> "أفهم. لو نظرنا للأرقام: مندوب مبيعات سعودي متوسط راتبه 12,000 ريال شهريًا. يصرف ~30% من وقته على فلترة بيانات يدويًا، أي ≈ 3,600 ريال شهريًا تكلفة مخفية. Sprint بـ 9,500 ريال = شهرين ونصف من هذه التكلفة المخفية فقط. والفرق: تستلم **أصلًا** (top 50 مرتّبة + مسودات بيلينغوال + تقرير تنفيذي للمجلس)، لا ساعات عمل. النموذج الكامل في `roi_model_saudi.md`."

**الرد (EN):**
> "Understood. The math: a Saudi sales rep at SAR 12K/month spends ~30% filtering data manually — ~SAR 3,600/month in hidden cost. The Sprint at SAR 9,500 equals 2.5 months of that hidden cost only. The difference: you receive an **asset** (ranked Top 50, bilingual drafts, executive report), not just hours. See `roi_model_saudi.md`."

**سؤال التوجيه:** "ما الميزانية المتاحة لـ Q1؟ نقدر نشتغل لها."

---

## 2. "نحن نستخدم ChatGPT أصلًا" / "We already use ChatGPT"

**الاعتراض:** "عندنا اشتراك ChatGPT Team، يعمل لنا كل شيء."

**ما خلف الاعتراض:** الإدارة لا تعرف الفرق التقني/الحوكمي بين شات بوت عام ومنتج مبني على بياناتهم.

**الرد (AR):**
> "ChatGPT أداة ممتازة للأفكار العامة. لكنه يفتقد ثلاثة أشياء حاسمة لـ B2B السعودي:
> 1. **استشهاد بالمصدر** — كل إجابة Dealix تحتوي على [DOC-ID §section]. ChatGPT لا.
> 2. **بوابة موافقة بشرية** قبل أي إرسال — Dealix إلزامية، ChatGPT لا.
> 3. **سجل تدقيق + PDPL footer** — Dealix كل خطوة في `event_store`. ChatGPT يخالف PDPL لو رفعت بيانات شخصية.
>
> هذا ليس مقارنة سلبية لـ ChatGPT — هو ليس مصمَّمًا لذلك. شاهد نموذج تقرير حقيقي في `sample_output.md` — ستلاحظ الفرق فورًا."

**الرد (EN):**
> "ChatGPT is excellent for general ideation. It lacks 3 things for Saudi B2B:
> 1. **Source citations** — every Dealix answer carries [DOC-ID §section]. ChatGPT doesn't.
> 2. **Human approval gate** before any send — Dealix mandatory; ChatGPT not.
> 3. **Audit log + PDPL footer** — Dealix logs every step to `event_store`; ChatGPT can put you out of PDPL compliance if you upload personal data.
>
> Not a knock on ChatGPT — it wasn't built for this. See `sample_output.md` for the contrast."

**سؤال التوجيه:** "كيف تتأكد حاليًا أن إجابات ChatGPT لا تستند لمعلومات غير موجودة في سياستكم؟"

---

## 3. "بياناتنا فوضى — مستحيل تطلع شيء منها" / "Our data is too messy"

**الاعتراض:** "تنسى الموضوع — بياناتنا في ملفات Excel متفرقة، CRM نص فاضي، WhatsApp."

**ما خلف الاعتراض:** خوف من إحراج "كشف الفوضى" أمام مزود خارجي.

**الرد (AR):**
> "هذا تمامًا حالنا في 80% من العملاء. Sprint مُصمَّم لهذا. نقبل بيانات حتى مع 30-60% فوضى. أول 3 أيام كلها تنظيف، dedupe، Saudi entity normalization. بعدها نصنّف. **النموذج الذي شاهدته (BFSI-A1) بدأ بـ 5,000 سجل، 84% فقط كانت صالحة بعد التنظيف.** ما يعني 800 سجل خرجوا — والباقي صار assets قابلة للاستخدام. الفوضى لا تخيفنا، بل تثبت أن Sprint مناسب لكم."

**الرد (EN):**
> "That's exactly the case for 80% of our customers. The Sprint is designed for this. We accept data with 30-60% mess. The first 3 days are cleanup + dedupe + Saudi entity normalization. **The sample you saw (BFSI-A1) started at 5,000 records — only 84% were valid after cleanup.** 800 rows dropped — the rest became usable assets. Mess doesn't scare us; it proves the Sprint fits you."

**سؤال التوجيه:** "ممكن ترسل لي عينة 100 سجل عشوائية، حتى أوضّح لك كيف نتعامل معها؟"

---

## 4. "أرنا حالة دراسية" / "Show me proof"

**الاعتراض:** "ما عندك case study مع عميل حقيقي؟ ما أصدّق."

**ما خلف الاعتراض:** خوف مشروع من الالتزام مع شركة ناشئة.

**الرد (AR):**
> "سؤال عادل. نقطة الصدق: شركتنا في المرحلة التي يحرص فيها العملاء الأوائل على السرّية، لذلك لا نطرح أسماء حقيقية. لكن:
> 1. **نموذج تقرير تنفيذي كامل** بـ 12 صفحة على بيانات اصطناعية تعكس عميل BFSI سعودي حقيقي: `sample_output.md`. ادرسه، وسترى تركيب الأرقام واتساقها.
> 2. **حزمة إثبات** لكل sprint منجَز: KPIs قبل/بعد بأرقام. تُسلَّم بعد Sprint كأصل قابل للاستخدام الداخلي.
> 3. **ضمان مرتبط بالأرقام**: Data Quality Score ≥ 80 أو إعادة معالجة. ROI ≥ X أو خصم.
>
> نحن نُفضّل العمل مع عميل يطلب أدلة، لأنه عميل ناضج."

**الرد (EN):**
> "Fair question. Honest answer: at our stage, early customers value confidentiality, so we don't publish real names. However:
> 1. **A full 12-page sample executive report** on synthetic-but-realistic Saudi BFSI data: `sample_output.md`. Study it; the numbers add up.
> 2. **Proof pack per Sprint** with before/after KPIs.
> 3. **Number-tied guarantees**: Data Quality Score ≥ 80 or re-run; ROI ≥ X or refund.
>
> We prefer customers who demand evidence — they're the mature ones."

**سؤال التوجيه:** "هل ترسل لي 100 سجل اختبار، ونقدّم تحليلًا مجانيًا لـ 20 منهم خلال 3 أيام، كإثبات قبل الالتزام؟"

---

## 5. "العربي عندكم مستوى كيف؟" / "How's your Arabic quality?"

**الاعتراض:** "عملت تجربة مع شركة سابقة، رسائلهم العربية فيها أخطاء وركيكة."

**ما خلف الاعتراض:** تجربة سابقة سيئة مع AI/Translation محلي.

**الرد (AR):**
> "نفهم تمامًا — هذا أكبر سبب لرفض حلول AI في السوق السعودي. عندنا 3 طبقات حماية:
> 1. **مرحلة كتابة بيلينغوال متوازنة**: لا ترجمة آلية. النص العربي يُكتب أصالةً، لا يُترجَم من الإنجليزي.
> 2. **مراجعة لغوية بشرية** قبل التسليم، بمعايير DIN-EN-17100 (ترجمة مهنية).
> 3. **اختبار مع 4 لهجات** (نجدية، حجازية، شرقية، خليجية عامة) في 4 أسئلة لكل sprint.
>
> في النموذج `sample_output.md`، الجزء العربي **هو الأصل** — اقرأه أولًا، ستحكم بنفسك."

**الرد (EN):**
> "Completely understand — this is the #1 reason AI fails in Saudi B2B. We have 3 layers:
> 1. **Bilingual parity authoring**: Arabic is written natively, not machine-translated.
> 2. **Human linguistic review** before delivery, to DIN-EN-17100 standards.
> 3. **4-dialect testing** (Najdi, Hejazi, Eastern, Gulf-general) per Sprint.
>
> In `sample_output.md`, Arabic is the source — read it first and judge."

**سؤال التوجيه:** "ممكن ترسل لي 3 رسائل تواصل سابقة من فريقك؟ نشتغل عليها معًا في Sprint لتقارن النتيجة."

---

## 6. "نظام حماية البيانات السعودي يقلقني" / "PDPL concerns me"

**الاعتراض:** "نخاف أن نخالف PDPL ونتعرض لغرامة."

**ما خلف الاعتراض:** قلق قانوني حقيقي — أحيانًا الإدارة لم تستوعب PDPL بعد.

**الرد (AR):**
> "قلق مشروع 100%. نشتغل مع PDPL وليس ضدّه:
> 1. **تذييل المادة 13** على كل رسالة (الإبلاغ الصريح). 100% تغطية.
> 2. **PII redaction آلي** عبر `pii_detector.py` قبل أي معالجة.
> 3. **Data Processing Record** جاهز حسب المادة 31، نسلّمه مع Sprint.
> 4. **سجل تدقيق بـ retention 365 يوم** لو طلبت SDAIA دليلًا.
> 5. **لا بيانات حساسة (Art. 27)** في sprints العامة — بيانات الصحة في Company Brain Sprint فقط، تحت DPIA منفصل.
>
> هل توجد سياسة DPO عندكم؟ نُنسّق معهم مباشرة."

**الرد (EN):**
> "Legitimate concern. We work *with* PDPL, not around it:
> 1. **Art. 13 footer** on every outbound message. 100% coverage.
> 2. **Auto PII redaction** via `pii_detector.py` pre-processing.
> 3. **Data Processing Record** per Art. 31, delivered with Sprint.
> 4. **365-day audit log retention** in case SDAIA requests evidence.
> 5. **No sensitive data (Art. 27)** in general Sprints — health data only in Company Brain Sprint under separate DPIA.
>
> Do you have a DPO? We coordinate directly with them."

**سؤال التوجيه:** "هل تريد مكالمة 30 دقيقة بين DPO عندكم وDPO عندنا قبل التوقيع؟ بدون التزام."

---

## 7. "نريد ضمانات نتائج محددة" / "We want guaranteed results"

**الاعتراض:** "اضمن لي 10 صفقات جديدة، نوقّع."

**ما خلف الاعتراض:** ضغط على المندوب من إدارته للحصول على ROI مضمون.

**الرد (AR):**
> "بصراحة، نرفض أي مزوّد يضمن لك 'صفقات' — وأنت كذلك ترفضه لأنه يكذب. الصفقات تعتمد على فريقك، منتجك، السوق، التوقيت — أمور خارج سيطرتنا.
>
> ما **نضمنه** فعلًا:
> 1. **Data Quality Score ≥ 80** بعد التنظيف، أو إعادة معالجة بدون رسوم.
> 2. **تغطية استشهاد ≥ 95%** على المساعد، أو إعادة معالجة.
> 3. **خفض زمن العملية ≥ 50%** على AI Quick Win، أو استرداد 50% من الرسوم.
> 4. **0 ادعاءات محظورة** في أي مسودة (يمر بـ `forbidden_claims.py`).
>
> هذه ضمانات تشغيلية يمكن قياسها. أعطنا ضمانات قابلة للقياس، وستبني ثقة أطول."

**الرد (EN):**
> "Honestly, refuse any vendor that 'guarantees deals' — they're lying. Deals depend on your team, product, market, timing.
>
> What we **do** guarantee:
> 1. **Data Quality Score ≥ 80** post-cleanup or free re-run.
> 2. **Citation coverage ≥ 95%** on the assistant, or free re-run.
> 3. **≥ 50% process time reduction** on AI Quick Win, or 50% refund.
> 4. **Zero forbidden claims** in any draft (passes `forbidden_claims.py`).
>
> These are measurable, operational guarantees — they build longer trust."

**سؤال التوجيه:** "أيٌّ من هذه الضمانات هو الأهم لمجلس إدارتك؟"

---

## 8. "عندنا فريق IT داخلي يقدر يبنيها" / "Our IT team can build it"

**الاعتراض:** "عندنا فريق تقني — يقدر يبني عند مثله."

**ما خلف الاعتراض:** فخر داخلي + ضغط على ميزانية خارجية.

**الرد (AR):**
> "محقّ، فريقك التقني قادر تمامًا. السؤال: **خلال كم؟** متوسط بناء RAG داخلي مع حوكمة كاملة في الشركات السعودية: 4-7 أشهر، ثم 2-3 أشهر صيانة لتحقيق eval coverage 95%. Sprint عندنا: 21 يومًا، مع 96.7% eval coverage **مُثبَتة في نموذج** `sample_output.md`.
>
> اقتراح عملي: **Sprint مع تسليم Code + Runbook** = فريقك يستلم النظام بعد 21 يومًا، يطوّره، ويصبح ملكًا لكم. لا حاجة لإعادة بناء من الصفر."

**الرد (EN):**
> "Your team is fully capable. Question: **how long?** Average internal RAG build with full governance at Saudi firms: 4-7 months, plus 2-3 more to reach 95% eval. Our Sprint: 21 days, with 96.7% eval coverage **proven in the sample** `sample_output.md`.
>
> Pragmatic offer: **Sprint delivers code + runbook**. Your team takes over after 21 days — no rebuild from scratch."

**سؤال التوجيه:** "ما تكلفة 4-7 أشهر من وقت فريق IT عندكم على مشروع موازٍ؟"

---

## 9. "لا توجد عميل سعودي مماثل" / "No Saudi customer like us"

**الاعتراض:** "ما عندك مرجعية في القطاع الصحي/التعليمي/الحكومي."

**ما خلف الاعتراض:** الرغبة في "أحد آخر جربها قبلي".

**الرد (AR):**
> "صادق معك: نحن في الموجة الأولى. هذه الميزة: تختار طريقتك دون عبء 'كيف فعلها المنافس'. لكن لا تشتري الموجة الأولى أعمى:
> 1. **Sprint بسعر ثابت** — لا تكاليف خفية.
> 2. **ضمانات مرتبطة بالأرقام** — قابلة للتنفيذ قانونيًا.
> 3. **Sprint يُسلَّم في 7-21 يومًا** — لو ما عجبك، تخرج بعد Sprint، عندك في يدك code + runbook + بيانات نظيفة.
> 4. **القطاع غير مرتبط بالمشكلة** — تنظيف بيانات في BFSI نفس آلية تنظيف بيانات في الصحة، اختلاف 5-10% فقط في المرادفات.
>
> القطاع الأول الذي يجرّب يحصل دائمًا على أفضل سعر."

**الرد (EN):**
> "Honestly, you'd be in our first wave. The upside: you set the playbook, not follow it. But don't buy first-wave blind:
> 1. **Fixed-price Sprint** — no hidden costs.
> 2. **Number-tied guarantees** — legally enforceable.
> 3. **7-21 days delivery** — if you don't like it, you walk away with code + runbook + clean data.
> 4. **Vertical doesn't change the engine** — data cleanup in BFSI ≈ in healthcare, only 5-10% lexicon delta.
>
> First-wave always gets the best terms."

**سؤال التوجيه:** "هل تقبل سعر first-wave (خصم 20%) مقابل حق الاستشهاد بحالتك بشكل مجهول؟"

---

## 10. "نحن مشغولون — نراجع الربع القادم" / "We're busy — review next quarter"

**الاعتراض:** "ما عندنا وقت هذا الربع — نتواصل في Q3."

**ما خلف الاعتراض:** غالبًا تسويف مهذّب، أحيانًا حقيقي.

**الرد (AR):**
> "أحترم انشغالك. سؤال صريح: ما الذي **بالضبط** سيتغيّر في Q3 يجعل المشروع أسهل؟ غالبًا ما نسمع 'بعد التخطيط السنوي' لكن التخطيط السنوي يفترض بيانات نظيفة، لا فوضى. هذا يعني أن Sprint **قبل** التخطيط يساعد على تخطيط أدق.
>
> اقتراح: **اقرأ `sample_output.md`** (يأخذ 15 دقيقة)، ثم 25 دقيقة معي بعد أسبوع. لا التزام. لو ما زلت مشغولًا، نُحدّد Q3."

**الرد (EN):**
> "Respect that. Honest question: what **specifically** changes in Q3 to make this easier? We often hear 'after annual planning', but annual planning needs clean data — not mess. A Sprint **before** planning makes planning sharper.
>
> Offer: **read `sample_output.md`** (15 min), then 25 min with me next week. If you're still pinned, we book Q3."

**سؤال التوجيه:** "أيهما أكثر تكلفة: 25 دقيقة معي الأسبوع القادم، أم 6 أشهر من بيانات مبعثرة في فريق المبيعات؟"

---

## 11. "خبرة AI قليلة عندنا، نخاف نفشل" / "We're new to AI — we're afraid we'll fail"

**الاعتراض:** "نحن جدد على الـ AI. ما عندنا خبرة. كيف نتأكد؟"

**ما خلف الاعتراض:** قلق التغيير، أو خوف فشل أمام الإدارة العليا.

**الرد (AR):**
> "هذا تمامًا سبب وجود Sprint قصير وثابت السعر — لتقليل المخاطر. الفوائد:
> 1. **التزام ≤ 21 يومًا**، ميزانية ≤ SAR 20K — لو فشل، لا يهدد ميزانيتك السنوية.
> 2. **Runbook + تدريب 2h** — فريقك يتعلم خلال Sprint، لا بعدها.
> 3. **بوابة موافقة بشرية إلزامية** — لا تخرج إجابات خاطئة بدون رؤية بشرية.
> 4. **Rollback في 5 دقائق** — لو شيء غلط، نرجع للوضع السابق فورًا.
> 5. **حزمة إثبات قبل التوسيع** — تعرضها على المجلس قبل أي قرار توسعة.
>
> الفشل في Sprint = خسارة 21 يومًا + 20K ريال. الفشل في عدم البدء = شركاؤك ينمون أسرع منكم في 12 شهرًا."

**الرد (EN):**
> "Exactly why the Sprint is short and fixed-price — to de-risk you. Benefits:
> 1. **≤ 21-day commitment**, ≤ SAR 20K budget — failure won't dent your annual budget.
> 2. **Runbook + 2h training** — your team learns *during* Sprint.
> 3. **Mandatory human approval gates** — no wrong answers reach external parties.
> 4. **5-minute rollback** — any issue, we revert instantly.
> 5. **Proof pack before scaling** — you show the board before any expansion.
>
> Failure-in-Sprint = 21 days + SAR 20K. Failure-not-to-start = competitors compound for 12 months."

**سؤال التوجيه:** "هل تفضّل أن نبدأ بأصغر use case ممكن (مثلًا تقرير CEO الأسبوعي) كاختبار منخفض المخاطر؟"

---

## 12. "أحتاج مراجعة داخلية" / "Let me check internally"

**الاعتراض:** "حلوة. لازم آخذ موافقة المدير/المجلس. أرجع لك."

**ما خلف الاعتراض:** أحيانًا حقيقي، أحيانًا تأجيل لـ "بدون نعم".

**الرد (AR):**
> "أكيد — وأقدّر الحوكمة الداخلية. سؤالان لمساعدتك في النقاش الداخلي:
> 1. **ما السؤال الأول** الذي سيطرحه مديرك/مجلسك؟ نتأكد أن لدينا الإجابة جاهزة في الـ SOW.
> 2. **متى التاريخ التقريبي** للقرار؟ نحجز سعتنا الزمنية له.
>
> اقترح خطوة: **أرسل لي اسم مديرك**، نعدّ صفحة واحدة مخصصة لاجتماعه الداخلي. لا التزام منك — أنت ترسلها له فقط."

**الرد (EN):**
> "Of course — and I respect internal governance. Two questions to help your internal discussion:
> 1. **What's the first question** your manager/board will ask? Let me make sure the SOW preempts it.
> 2. **Rough timeline** for the decision? So we can hold our capacity.
>
> Suggestion: **send me your manager's name**; we'll prepare a single-page memo tailored to their meeting. No commitment from you — you just forward it."

**سؤال التوجيه:** "هل يساعد أن أحضر معك جزءًا قصيرًا (10 دقائق) من اجتماعك الداخلي للإجابة الفنية؟"

---

## قواعد عامة لإجابة الاعتراضات / Universal rules

1. **اعترف بالاعتراض أولًا.** "أفهمك / Understood" قبل أي رد.
2. **استشهد بدليل**، لا بادعاء. (الأرقام، نماذج التقارير، الـ event_store.)
3. **اطرح سؤالًا** بعد كل رد — تحول من الدفاع إلى الحوار.
4. **لا تتجادل** على الميزانية — اقترح حجمًا أصغر أو ربعًا لاحقًا.
5. **لا تَعِد** بشيء خارج perimeter حوكمتك.
6. **سجّل كل اعتراض** في CRM (يُفيد التدريب الداخلي).
7. **بعد 3 ردود اعتراضية في مكالمة واحدة**: لا تستمر — اقترح موعدًا لاحقًا.

---

## نمط الإجابة المُقترَح / Suggested response template

```
1. أعترف:        "أفهم — هذا قلق مشروع."
2. أعد التأطير:  "لو نظرنا للزاوية الأخرى..."
3. استشهد بدليل: "في النموذج/التقرير/الحوكمة، نرى X."
4. اطرح سؤالًا:  "أيٌّ من هذه النقاط هو الأهم لكم؟"
```

---

## روابط داخلية / Cross-links

- سيناريو المبيعات: [`sales_script.md`](./sales_script.md)
- صفحات العروض: [`offer_pages/grow_revenue_sprint.md`](./offer_pages/grow_revenue_sprint.md) · [`offer_pages/automate_work_sprint.md`](./offer_pages/automate_work_sprint.md) · [`offer_pages/company_brain_sprint.md`](./offer_pages/company_brain_sprint.md)
- قوالب الرسائل: [`../../templates/outbound_messages.md`](../../templates/outbound_messages.md)
- نموذج ROI السعودي: [`roi_model_saudi.md`](./roi_model_saudi.md)
- مصفوفة الشخصية والقيمة: [`persona_value_matrix.md`](./persona_value_matrix.md)
- نموذج تقرير LIS: [`../services/lead_intelligence_sprint/sample_output.md`](../services/lead_intelligence_sprint/sample_output.md)
- نموذج تقرير AQW: [`../services/ai_quick_win_sprint/sample_output.md`](../services/ai_quick_win_sprint/sample_output.md)
- نموذج تقرير CBS: [`../services/company_brain_sprint/sample_output.md`](../services/company_brain_sprint/sample_output.md)

---

*Dealix Objection Handling · revision 2026-05 · 12 objections · `playbook_id: dealix_obj_v1`*
