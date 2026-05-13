# Outbound Message Templates — 3 Sequences for 3 Starting Offers

> **Hard rule** — every message must:
> 1. Include PDPL Art. 13 notice text in the footer.
> 2. Pass `dealix/trust/forbidden_claims.py` scan (no unverifiable claims).
> 3. Be approved per the W6.T34 §3.6 Outreach OS gate before send.
> 4. Be logged in `event_store` as `message.drafted` → `message.approved` → `message.sent`.

## PDPL Footer (mandatory on every email/WhatsApp)

**AR:** "إذا لا ترغب في التواصل، رد بكلمة 'إلغاء' أو راسلنا على dpo@dealix.me. تتم المعالجة وفقًا لنظام حماية البيانات الشخصية في المملكة العربية السعودية."

**EN:** "If you do not wish to be contacted, reply 'STOP' or write to dpo@dealix.me. Processing is performed in accordance with the Saudi Personal Data Protection Law (PDPL)."

---

## Sequence A — Revenue Intelligence Sprint (3 emails over 10 days)

### Email A1 — Day 1 (Cold Open)

**Subject (AR):** فرص مبيعات سعودية مرتبة من بياناتك خلال 10 أيام
**Subject (EN):** Saudi ranked opportunities from your own data in 10 days

**Body (AR):**

> مرحبًا {{contact_first_name}},
>
> أنا {{sender_name}} من Dealix. لاحظنا أن {{company_name}} في {{vertical_ar}}
> من اللاعبين النشطين في {{region_ar}}، وعادةً ما يكون التحدي ليس في
> الـ Leads نفسها، بل في تحويل البيانات المبعثرة إلى **قرار مبيعات
> واضح**.
>
> نقدم Sprint مدته 10 أيام بسعر ثابت 9,500 ريال:
> - تنظيف بياناتك (حتى 5,000 سجل) + Saudi entity normalization.
> - أفضل 50 حسابًا مرتّبًا حسب ICP الخاص بك.
> - أفضل 10 إجراءات فورية مع رسائل تواصل (عربي/إنجليزي).
> - Mini CRM + تقرير تنفيذي + جلسة تسليم 60 دقيقة.
>
> 25 دقيقة معك تكفي لنحدد إن كان مناسبًا. هل لديك وقت {{day_option_1}} أو {{day_option_2}}؟
>
> شكرًا،
> {{sender_name}} · Dealix

**Body (EN):** (parallel version — same structure)

### Email A2 — Day 4 (Value Reinforcement)

**Subject (AR):** سؤال سريع عن بيانات {{company_name_ar}}
**Subject (EN):** Quick question about {{company_name_en}}'s sales data

**Body (AR — abbreviated):**
> بياناتك مرتّبة كيف؟ Excel، CRM، أم مختلطة؟ معظم الشركات السعودية التي عملنا
> معها كانت بياناتها مبعثرة 30–60%. هذا Sprint يحلّ هذا تحديدًا.
> [Calendly link]

### Email A3 — Day 8 (Break-up)

**Subject:** أغلق الموضوع — أو ادخل في Sprint

> إذا التوقيت غير مناسب الآن، سأتوقف عن المتابعة. وإذا تريد نبدأ، رد بكلمة "ابدأ" وسنرسل عقد SOW جاهز.

---

## Sequence B — AI Quick Win Sprint (3 emails over 7 days)

### Email B1 — Day 1

**Subject:** أتمتة عملية واحدة عندك خلال 7 أيام

> هل عندك تقرير أسبوعي يأخذ ساعات من فريقك؟ توزيع leads يدوي؟ فرز تذاكر؟
> اختر **واحدة** فقط، ونحن نُؤتمتها بـ AI Quick Win Sprint (7 أيام، 12,000 ريال،
> مع approval workflow وaudit log). جلسة 30 دقيقة لتحديد الـ use case المناسب؟

### Email B2 — Day 3 (Use-case bait)

> أكثر use cases نجاحًا عندنا:
> 1. تقرير CEO الأسبوعي → من 6 ساعات إلى ساعة.
> 2. فرز tickets → من 4 ساعات/يوم إلى 30 دقيقة.
> 3. مولّد عرض أولي → من ساعتين/عرض إلى 15 دقيقة.
> أيها يشبه ألمك الحالي؟

### Email B3 — Day 6 (Break-up)

> آخر إيميل. رد بـ "نعم" لجدولة المكالمة، أو سأتوقف هنا.

---

## Sequence C — Company Brain Sprint (3 emails over 14 days)

### Email C1 — Day 1

**Subject:** حول ملفات {{company_name_ar}} إلى مساعد داخلي بإجابات موثّقة

> فريقك يبحث في PDFs وملفات قديمة كل يوم؟ Company Brain Sprint يحوّل
> ملفاتك إلى مساعد يجيب على أسئلة الموظفين **مع مصادر** خلال 21 يومًا
> (20,000 ريال).
>
> القاعدة الذهبية عندنا: **لا مصدر = لا إجابة**. لا هلوسة، لا اختراع.

### Email C2 — Day 7 (Proof point)

> آخر عميل لنا في {{vertical_ar}}: 100% من الإجابات بمصادر، تقليل زمن البحث بنسبة 60%.
> هل تريد نسخة demo (مجاني، 15 دقيقة)؟

### Email C3 — Day 13 (Break-up)

> هذا آخر إيميل. لمعرفة المزيد أو الإيقاف، رد بكلمة واحدة.

---

## WhatsApp Variants (only after explicit consent / inbound interest)

**AR — short open:**

> {{contact_first_name}}، Dealix هنا. نقدم Sprint بـ {{price}} ريال لـ {{outcome}}.
> مهتم بمكالمة 25 دقيقة؟

**EN — short open:**

> Hi {{contact_first_name}}, this is Dealix. We run a {{duration}}-day fixed-scope
> Sprint at SAR {{price}} for {{outcome}}. Worth a 25-min call?

WhatsApp is **never** used for cold first-touch. Per W6.T34 Outreach OS rules
and W3.T07 Trust pack, WhatsApp requires Art. 14 consent or a prior business
relationship.

---

## Owner

CRO + Marketing Manager. Sequences are A/B tested per `docs/experiments/ab_framework.md` (W4.T26).
