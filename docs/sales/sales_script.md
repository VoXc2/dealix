# سيناريو المبيعات / Sales Script (Dealix)

دليل تشغيلي للمندوب من اللحظة الأولى للتواصل حتى الإغلاق. بيلينغوال. يلتزم بقواعد PDPL والـ governance perimeter.

> **القاعدة الذهبية:** العميل يتحدث 60%، المندوب 40%. الأهم: لا تَعِد بشيء غير قابل للتحقق.

> **روابط مرجعية:**
> - قوالب الرسائل الكاملة: [`templates/outbound_messages.md`](../../templates/outbound_messages.md)
> - إجابات الاعتراضات: [`objection_handling.md`](./objection_handling.md)
> - صفحات العروض: [`offer_pages/grow_revenue_sprint.md`](./offer_pages/grow_revenue_sprint.md) · [`offer_pages/automate_work_sprint.md`](./offer_pages/automate_work_sprint.md) · [`offer_pages/company_brain_sprint.md`](./offer_pages/company_brain_sprint.md)

---

## المرحلة 1 — الرسالة الأولى / First Message

### 1.1 المبدأ / The principle

**AR:** الرسالة الأولى يجب أن:
- تحترم وقت العميل (≤ 110 كلمة).
- تذكر دليلًا واحدًا مرئيًا (إعلان، تعيين، نمو، RFP).
- تطلب اجتماع 25 دقيقة فقط، لا 60.
- تنتهي بسؤال مغلق (yes/no) بخيارَيْ موعد محدّدين.
- تضع تذييل PDPL المادة 13 في كل بريد.

**EN:** First message must:
- Respect the prospect's time (≤ 110 words).
- Reference one visible signal (announcement, hire, growth, RFP).
- Ask for **25 minutes**, not 60.
- End with a closed question (yes/no) + two date options.
- Include PDPL Art. 13 footer.

### 1.2 قالب الرسالة الأولى (EN) / First message template (EN)

> **Subject:** Quick idea after seeing {{signal}}
>
> Hi {{first_name}},
>
> Noticed {{public_signal}} (e.g., your recent expansion to Dammam / your new CDO appointment / your RFP for automation). For Saudi {{vertical}} teams at your stage, the bottleneck usually isn't leads — it's **ranking the leads you already have**.
>
> Dealix runs a fixed 10-day Sprint that turns up to 5,000 records into 50 ranked Saudi accounts + 10 bilingual outreach drafts, priced at **SAR 9,500**. Sample output available on request.
>
> Would a 25-min call on {{day_1}} or {{day_2}} work to see if it fits?
>
> Thanks,
> {{sender_name}} · Dealix
>
> *If you do not wish to be contacted, reply "STOP" or write to dpo@dealix.me. Processing per Saudi PDPL (Art. 13).*

### 1.3 قالب الرسالة الأولى (AR)

> **الموضوع:** فكرة سريعة بعد {{signal_ar}}
>
> الأستاذ/ة {{first_name_ar}}،
>
> لاحظت {{public_signal_ar}} (مثلًا: توسعكم في الدمام / تعيين CDO الجديد / RFP الأتمتة المنشور). عادةً ما يكون التحدي ليس في الـ Leads، بل في **ترتيب الـ Leads** الموجودة فعلًا.
>
> Dealix تنفّذ Sprint مدته 10 أيام يحوّل حتى 5,000 سجل إلى 50 حسابًا مرتّبًا + 10 رسائل تواصل بيلينغوال، بسعر ثابت **9,500 ريال**. نموذج تقرير تنفيذي متاح عند الطلب.
>
> هل 25 دقيقة يوم {{day_1_ar}} أو {{day_2_ar}} تناسبك؟
>
> شكرًا،
> {{sender_name}} · Dealix
>
> *إذا لا ترغب في التواصل، رد بكلمة "إلغاء" أو راسلنا على dpo@dealix.me. تتم المعالجة وفق نظام حماية البيانات الشخصية السعودي (المادة 13).*

---

## المرحلة 2 — جلسة التأهيل (25 دقيقة) / Qualification Call

### 2.1 الافتتاحية (3 دقائق) / Opening

**AR:** "شكرًا على الوقت {{first_name}}. هدف اليوم: أفهم وضعكم، وأقول لك بصراحة هل عندنا حاجة تناسبكم أم لا. لو لقينا أن مو مناسب، سأقترح بدائل. هل هذا يناسبك؟"

**EN:** "Thanks for the time, {{first_name}}. The goal today: I understand your situation and tell you honestly whether we can help — and if not, suggest alternatives. Sound fair?"

### 2.2 الأسئلة الأربعة الجوهرية / The four qualification questions

> **مهم:** اسأل **الأربعة كلها**. لا تنتقل للسعر قبل أن تكمل الأربعة.

**سؤال 1 — الألم / Pain**
**AR:** "ما العملية الأكثر إيلامًا في فريقك حاليًا؟ شيء يأخذ ساعات أسبوعيًا ويُنفّذ يدويًا؟"
**EN:** "What's the most painful repetitive process in your team right now — something that eats hours weekly and is done manually?"
**استمع لـ:** ساعات/أسبوع، عدد الأشخاص، الأخطاء، التأخر.

**سؤال 2 — الأثر / Impact**
**AR:** "لو حُلّت هذه المشكلة، كم ساعة أسبوعيًا يربح فريقك؟ وما الذي ستفعلونه بهذا الوقت؟"
**EN:** "If this was solved, how many hours/week does your team get back? And what would they do with that time?"
**استمع لـ:** قيمة الوقت بالـ SAR، التأثير على القرارات/الإيرادات.

**سؤال 3 — الميزانية والقرار / Budget & decision**
**AR:** "هل عندكم ميزانية مخصصة لمشاريع AI/أتمتة هذا الربع؟ ومن يوقّع على عقد بين 10-20 ألف ريال؟"
**EN:** "Do you have a budget allocated for AI/automation projects this quarter? And who signs on a SAR 10-20K engagement?"
**استمع لـ:** صلاحية التوقيع، التوقيت، عوائق المشتريات.

**سؤال 4 — التوقيت والبيانات / Timing & data**
**AR:** "لو وقّعنا اليوم، متى ممكن نبدأ؟ وهل عندكم بيانات/وثائق جاهزة للمشاركة (CSV، PDF، CRM export)؟"
**EN:** "If we signed today, when could we start? And do you have data/documents ready to share (CSV, PDF, CRM export)?"
**استمع لـ:** هل البيانات جاهزة فعلًا، أم سيكون هناك تأخر بسبب IT/legal.

### 2.3 شجرة القرار (5 دقائق) / The 5-minute decision tree

بعد الأسئلة الأربعة:

| الإجابات | ما العرض المناسب |
|---|---|
| Pain = بيانات/مبيعات، Impact > 30K SAR/yr، Budget = نعم، Timing = الآن | **Lead Intelligence Sprint** (SAR 9,500) |
| Pain = عملية يدوية متكررة، Impact = ساعات أسبوعيًا، Budget = نعم | **AI Quick Win Sprint** (SAR 12,000) |
| Pain = "وين ذاك الـ PDF؟"، Impact = موظفون كثر يبحثون، Budget = نعم | **Company Brain Sprint** (SAR 20,000) |
| Pain موجود لكن Budget = لا | حدّد محادثة Q3، أرسل [sample report](#) |
| Pain غير واضح / حماس عام | اطلب رؤية CRM/process map قبل الاقتراح |
| Pain = خارج perimeter | اعتذر بأدب، أحِله لشريك (لا تأخذ المشروع) |

### 2.4 العرض الأولي (15 دقيقة) / Shaping the proposal

- ابدأ بإعادة سرد ما سمعته: "لو فهمت صح، التحدي هو X، الأثر سيكون Y، الموعد المناسب Z."
- اعرض **نموذج تقرير تنفيذي** (sample_output.md المناسب) — هذا يفصِل بين Dealix والمنافسين.
- اشرح **الـ Sprint** المناسب: السعر الثابت، المدة، التسليمات.
- اذكر **الضمان** المرتبط: ROI ≥ X أو إعادة معالجة بدون رسوم.
- اعرض **شرط واحد للقبول السريع**: "إذا وقّعنا خلال 7 أيام، نضيف [bonus محدّد]."

### 2.5 إغلاق الجلسة (2 دقيقة) / Close the call

**AR:** "هل ترى أن هذا يستحق التجربة؟"
- لو **نعم**: "ممتاز. سأرسل SOW الجاهز خلال 24 ساعة. هل يناسبك التوقيع قبل يوم {{date}}؟"
- لو **ربما**: "ما السؤال الذي يجب الإجابة عليه قبل القرار؟"
- لو **لا**: "أقدّر صراحتك. هل تسمح أن أتابع معك في {{Q+1}}؟"

**EN:** "Do you see this worth trying?"
- If **yes**: "Excellent. I'll send the ready SOW within 24 hours. Can you sign by {{date}}?"
- If **maybe**: "What's the one question you need answered before deciding?"
- If **no**: "I appreciate the directness. May I follow up in {{Q+1}}?"

---

## المرحلة 3 — إرسال العرض / Sending the Quote

### 3.1 محتوى البريد بعد المكالمة (خلال 4 ساعات)

**AR:**
> الأستاذ {{first_name}}،
>
> شكرًا على وقتك اليوم. كما اتفقنا، إليك:
> - **العرض المقترح:** {{Sprint_name}} بسعر **{{price}} SAR** (مدة {{duration}} أيام عمل).
> - **SOW** مرفق (4–6 صفحات، جاهز للتوقيع).
> - **نموذج تقرير تنفيذي** مماثل: {{sample_output_link}}.
> - **صفحة العرض الكاملة:** {{offer_page_link}}.
> - **مسار الترقية بعد Sprint:** {{retainer_summary}}.
>
> للقبول: وقّع SOW المرفق، أو رد بكلمة **"موافق"** — وسنبدأ Day 1 خلال 5 أيام عمل من تأكيد الدفع المبدئي (إن وُجد).
>
> *تذييل PDPL المعتمد*

**EN:** parallel structure, same fields.

### 3.2 المرفقات الإلزامية مع العرض

| المرفق | الحالة |
|---|---|
| SOW (PDF + قابل للتوقيع إلكترونيًا) | إلزامي |
| نموذج تقرير تنفيذي (sample_output.md المناسب) | إلزامي |
| Data intake checklist | إلزامي (في حال Sprint بيانات) |
| ROI worksheet (Excel) | اختياري لكن مُفضَّل |
| رابط Calendly لجلسة Day-1 Kickoff | إلزامي |

---

## المرحلة 4 — المتابعة والإغلاق / Follow-up & Close

### 4.1 جدول المتابعة الموصى به

| اليوم | الإجراء |
|---|---|
| Day 0 | البريد بعد المكالمة + SOW |
| Day 2 | بريد متابعة (سؤال محدّد: "هل وصلتك المرفقات؟") |
| Day 4 | اتصال هاتفي قصير (≤ 7 دقائق) |
| Day 6 | بريد "summary + closing" مع تذكير بـ bonus |
| Day 9 | بريد "break-up" (انظر 4.2) |
| Day 14 | إغلاق رسمي + جدولة الربع التالي |

### 4.2 بريد الـ Break-up (يوم 9)

**AR:**
> الأستاذ {{first_name}}، فهمت أن التوقيت قد لا يكون مناسبًا الآن. هذا تمامًا مفهوم. سأتوقف عن المتابعة، وأبقى هنا متى احتجت. إذا أردت إعادة فتح الحوار في **{{Q+1}}**، رد فقط بكلمة "نعم".
>
> شكرًا،
> {{sender_name}}
>
> *PDPL Art. 13 footer*

**EN:** parallel version.

### 4.3 إشارات الإغلاق الإيجابية / Closing signals

| الإشارة | الإجراء |
|---|---|
| العميل يسأل عن الفواتير / IBAN / VAT details | أرسل تفاصيل الدفع وSOW فورًا |
| يسأل "ممكن نضيف X في Sprint؟" | وضّح ما داخل/خارج النطاق، أعرض ترقية مدفوعة |
| يطلب مكالمة مع شخص فني | جدّد المكالمة + احضِر مهندس حلول |
| يحجز Day-1 Kickoff عبر Calendly | تم الإغلاق — أرسل welcome email |

### 4.4 إشارات الرفض المهذّب / Polite-decline signals

| الإشارة | الإجراء |
|---|---|
| "نحتاج نراجع داخليًا" بدون موعد | اطلب تحديد موعد متابعة، لا تترك بلا اتفاق |
| تأخر الرد > 7 أيام دون تفاعل | بريد Break-up |
| رد بـ "STOP" / "إلغاء" | احذفه من القائمة، سجّل في `event_store` |

---

## المرحلة 5 — الإغلاق الإيجابي / The Close

**AR (سيناريو موصى به للمكالمة الإغلاقية):**
> "{{first_name}}، بناء على ما اتفقنا، عندنا 3 طرق نمشي بها:
> 1. **نمضي قدمًا** بـ {{Sprint_name}} هذا الأسبوع.
> 2. نأخذ **خطوة أصغر** بـ {{cheaper_offer}}.
> 3. **نحدد موعد للربع القادم** إذا التوقيت غير مناسب.
> أي خيار يبدو الأنسب لك الآن؟"

**EN:**
> "{{first_name}}, based on what we've discussed, there are 3 ways forward:
> 1. **Move ahead** with {{Sprint_name}} this week.
> 2. Take a **smaller step** with {{cheaper_offer}}.
> 3. **Schedule for next quarter** if timing isn't right.
> Which feels most fitting?"

---

## قواعد لا تُكسَر / Hard rules (no exceptions)

1. **لا تَعِد** بزيادة إيرادات أو تخفيض موظفين.
2. **لا تخفي** ما خارج النطاق — العميل يحترم الصدق.
3. **لا ترسل** أي رسالة آلية بدون موافقة بشرية.
4. **لا تجاوز** ميزانية العميل المُعلَنة.
5. **لا تُرسِل** sample يحتوي اسم عميل حقيقي.
6. **لا تتفاوض** على PDPL أو حوكمة الموافقة — ثابتة.
7. **لا تُنهي** مكالمة بدون **next step** محدّد.
8. **لا تتحدث** أكثر من 40% من وقت المكالمة.

---

## روابط داخلية / Cross-links

- قوالب الرسائل: [`../../templates/outbound_messages.md`](../../templates/outbound_messages.md)
- إجابات الاعتراضات: [`objection_handling.md`](./objection_handling.md)
- مصفوفة الشخصية والقيمة: [`persona_value_matrix.md`](./persona_value_matrix.md)
- نموذج ROI: [`roi_model_saudi.md`](./roi_model_saudi.md)
- نموذج تقرير LIS: [`../services/lead_intelligence_sprint/sample_output.md`](../services/lead_intelligence_sprint/sample_output.md)
- نموذج تقرير AQW: [`../services/ai_quick_win_sprint/sample_output.md`](../services/ai_quick_win_sprint/sample_output.md)
- نموذج تقرير CBS: [`../services/company_brain_sprint/sample_output.md`](../services/company_brain_sprint/sample_output.md)

---

*Dealix Sales Playbook · revision 2026-05 · `script_id: dealix_v1`*
