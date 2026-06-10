# Buying Committee Playbook — دليل لجنة الشراء

> **Status:** READY (structure) / PARTIAL (Arabic scripts — تتطلب تعديلًا سياقيًا لكل حساب)
> **Evidence Level:** assumption (design-time framework)
> **Owner:** Sales Lead (Primary) · CS Lead (Secondary)
> **المُدخلات:** TAP + Stakeholder Map

---

## 1. الهدف

**تحويل Buying Committee من مجموعة غير منسّقة إلى coalition يدعمنا.** هذا الدليل يقدّم:
- ورشة رسم خريطة Committee.
- شبكة Power vs Interest.
- تسلسل بناء Coalition.
- تمكين البطل.
- تحييد Blocker (بدون تلاعب).
- Cadence أسبوعي.

---

## 2. ورشة رسم Committee (90 دقيقة)

> **المشاركون من Dealix:** Sales Lead + (عند الحاجة) CS Lead.
> **المشاركون من العميل:** لا أحد في الورشة الأولى (داخلية).

### Agenda

| الوقت | النشاط | المخرج |
|------|--------|--------|
| 00–10 | مراجعة TAP → تحديث `pain` و `trigger` | تحديث TAP |
| 10–25 | عصف ذهني: من يملك القرار النهائي؟ (3–5 أسماء) | قائمة EB |
| 25–40 | من يوصي؟ (3–5 أسماء) | قائمة Champion + Influencer |
| 40–55 | من يقيّم تقنيًا/أمنيًا؟ | قائمة Technical + Security |
| 55–70 | من يوقّع على العقد؟ | Procurement + Legal |
| 70–90 | من قد يعارض؟ (Blocker) + لماذا؟ | قائمة Blocker + دوافعه |

### المُخرج
ملف `stakeholders.jsonl` محدّث بـ ≥ 6 stakeholders، ولكلٍّ `decision_influence` و `engagement_status` افتراضي.

---

## 3. شبكة Power vs Interest (2×2 Grid)

> **المحاور:**
> - **Power:** القدرة على اتخاذ/عكس القرار.
> - **Interest:** الاهتمام الشخصي بنتيجة المشروع.

```
        High Power
            │
   Keep     │   Manage
   Satisfied│   Closely
            │
   ────────●──────── Interest
            │   High
   Monitor  │   Engage &
   (Min)   │   Empower
            │
        Low Power
```

### كيف نتعامل مع كل ربع

| الربع | الاستراتيجية |
|------|--------------|
| **High Power + High Interest** | **Manage Closely.** اجتمع معهم أسبوعيًا. أطعمهم معلومات جديدة. |
| **High Power + Low Interest** | **Keep Satisfied.** أرسل تحديثات مختصرة. لا تطلب قرارات. |
| **Low Power + High Interest** | **Engage & Empower.** هؤلاء Champions المحتملون. أعطهم أدوات ليقنعوا غيرهم. |
| **Low Power + Low Interest** | **Monitor.** الحد الأدنى من الجهد. |

### تطبيق مؤسسي سعودي نموذجي

| الدور | Power | Interest | الربع | الإجراء |
|------|-------|---------|------|---------|
| CRO | 5 | 5 | Manage Closely | اجتماع Executive نصف شهري |
| CFO | 5 | 3 | Keep Satisfied | تحديث شهري، Business Case مختصر |
| IT Director | 4 | 4 | Manage Closely | اجتماع تقني نصف شهري |
| CISO | 4 | 3 | Keep Satisfied | Security pack + مكالمة فصلية |
| Procurement Manager | 4 | 2 | Keep Satisfied | لقاء مبكر لبناء علاقة |
| SDR Lead (Daily User) | 2 | 5 | Engage & Empower | تدريب + early wins |
| VP Strategy | 3 | 4 | Manage Closely | ربط المشروع بمبادرة استراتيجية |
| Legal Counsel | 3 | 2 | Monitor | يُدخل في اللحظة المناسبة |
| مستشار خارجي | 2 | 4 | Engage & Empower | قنوات تواصل مخصّصة |

---

## 4. Coalition-Building Sequence (تسلسل بناء التحالف)

> **القاعدة:** لا تتحدّث عن الحل حتى يكون عندك ≥ 2 من أقوى 3 صنّاع قرار في صفّك (rough coalition).

### الخطوة 1: Champion الداخلي (يوم 1–14)
- حدد البطل في أول Discovery.
- اجتمع معه 1:1 (45 دقيقة، غير رسمي).
- اعطه 1–2 أدوات يستخدمها مع زملائه (one-pager، demo قصير).
- **القاعدة:** لا تطلب منه أن يبيع داخليًا. اعطه «ما يقوله» فقط.

### الخطوة 2: Business Owner (يوم 14–30)
- اجتمع مع VP/Director الذي يتبعه الفريق المستهدف.
- أظهر كيف يخدم OKR خاص به.
- **القاعدة:** أظهر، لا تقل.

### الخطوة 3: Technical Reviewer (يوم 30–45)
- اجتماع تقني عميق (90 دقيقة).
- شارك Architecture Overview و Integration map.
- **القاعدة:** لا تستعجل. الـ Technical Reviewer يثق ببطء.

### الخطوة 4: Security/Privacy (يوم 30–60)
- أرسل Security و Privacy Overviews (من `docs/enterprise/`).
- أجب على أسئلة CISO بدون ضغط زمني.
- **القاعدة:** إذا لم يرد CISO خلال 14 يوم، أبلغ Champion.

### الخطوة 5: Economic Buyer (يوم 45–75)
- **فقط** بعد أن يكون Champion و Business Owner في صفّك.
- اجتماع Executive 60 دقيقة.
- Business Case صفحة واحدة.
- **القاعدة:** لا تذهب لـ EB بدون Business Case.

### الخطوة 6: Procurement + Legal (يوم 60–90)
- لقاءات منفصلة مع Procurement و Legal.
- اعرض بنود placeholders (من `PROCUREMENT_SALES_PLAYBOOK_AR.md`).
- **القاعدة:** قدّم مسودة DPA موقّعة مسبقًا (من `docs/enterprise/DPA_DEALIX_FULL.md`).

### الخطوة 7: Blocker (مستمر)
- لا تتجنّبه.
- اعرض عليه جلسة Q&A مع فريقنا.
- **القاعدة:** لا تحوّل Blocker إلى Champion قسرًا. اعطه «مخرج مشرّف» (face-saving exit).

---

## 5. تمكين البطل (Champion Enablement)

### ماذا يحتاج البطل؟

1. **لغة دفاعية** — يجيب عن أسئلة الزملاء.
2. **أدلة بصرية** — شرائح/مخططات يستخدمها.
3. **Cover سياسي** — يشعر أنه ليس وحده.
4. **Quick wins** — نتائج سريعة يستخدمها في عرض Board.

### كيف نُفعّله؟

| الإجراء | التكرار | المالك |
|---------|---------|--------|
| إرسال one-pager مخصّص (صفحة واحدة) | أسبوعي | Sales Lead |
| مكالمة 15 دقيقة (محتوى + أسئلة) | أسبوعي | Sales Lead |
| جلسة Q&A مع Founder (نادر) | شهري | Founder |
| Reference call من peer | ربع سنوي | Sales Lead |
| بطاقة «كيف تتحدّث عن المشروع» | مرة | Sales Lead |

### بطاقة "كيف تتحدّث عن المشروع" (Card)

> نموذج مختصر يُرسل للبطل:

```
عنوان المشروع: [Dealix Pilot — Initiative Name]
صاحب القرار: [EB Name]
الفائدة المتوقعة: [X] خلال [Y] أسبوع
المخاطر التي تم معالجتها: [أمن، بيانات، تكامل]
السؤال المتوقع من الزملاء: [سؤال]
الإجابة: [إجابة مختصرة]
من في صفّنا: [Champion] + [Business Owner]
```

---

## 6. تحييد Blocker (بدون تلاعب)

> **القاعدة:** نحن لا نكذب، لا نخفي، لا نحرج Blocker. نُحيّده بحقائق ووقار.

### أنماط Blocker الشائعة

| النمط | السلوك | الاستجابة |
|------|--------|----------|
| **Defender of Status Quo** | "المنتج الحالي يكفينا" | أظهر فجوة محددة بـ metric واحد |
| **Power Defender** | "هذا ليس دوري" | اربط المبادرة بأهداف EB مباشرة |
| **Ideological Skeptic** | "AI لا يعمل في [القطاع]" | شارك reference مشابهة، اسمح له بالاتصال |
| **Political Enemy** | "صديقنا [منافس] أفضل" | لا تهاجم. أعطه مقارن محايد |
| **Genuine Risk-Officer** | قلق حقيقي على البيانات | أجب على أسئلته بدقة. أظهر DPA |

### سكريبتات عربية (غير مُتلاعب)

#### سكريبت 1: "منتجنا الحالي يعمل"
> «أقدّر رأيك. هل يمكننا النظر معًا في [metric محدد] خلال 30 يومًا فقط؟ إذا لم يتحسّن، سأوافق شخصيًا على إيقاف المشروع.»

#### سكريبت 2: "صديقنا [منافس] أفضل"
> «منافسينا يقدمون قيمة مختلفة. أترك لكم أمر المقارنة. هل يمكنني أن أعرض عليكم نقاط الاختلاف الجوهرية في جلسة 30 دقيقة مع فريقكم التقني؟»

#### سكريبت 3: "AI لا يعمل في [قطاع]"
> «اتفهم معك. في الواقع، [X]% من مشاريعنا في [القطاع] حقّقت [نتيجة محددة] خلال [N] شهر. هل يمكنني مشاركة [anonymized] case study معك؟»

#### سكريبت 4: "متى أعرف أنكم لن تُسربون بياناتنا؟"
> «سؤال مشروع. لدينا [شهادة/اعتماد/تدقيق]، وبياناتكم تبقى في [region]. يسعدني أن أعرض DPA كاملاً وأدخل في تفاصيل البند [X].»

> **القاعدة:** السكريبتات تُعدَّل سياقيًا لكل Blocker. هذه نقطة بداية.

---

## 7. Cadence (الوتيرة)

### أسبوعي
- **1:1 مع Champion** (15 دقيقة، نفس اليوم كل أسبوع).
- **تحديث مكتوب** قصير (5 bullets) لكل من: Business Owner، Technical Reviewer، EB (إذا كان في صفّنا).

### نصف شهري
- **اجتماع Executive** (60 دقيقة) مع EB + Champion.
- **جلسة تقنية** مع Technical/Security (60 دقيقة).

### شهري
- **Recap** (صفحة واحدة) يُرسل لـ EB + Champion + Business Owner.
- **مراجعة Blocker** (جلسة قصيرة 30 دقيقة) مع Champion.

### ربع سنوي
- **تقييم Committee كامل** — هل ما زلنا في الصفحة الصحيحة؟

---

## 8. KPIs على مستوى Committee

| المؤشر | الهدف placeholder |
|--------|-------------------|
| Multi-Threading Index | ≥ 4 stakeholders engaged |
| Champion Strength Score | ≥ 4 لحسابات المرحلة المتأخرة |
| Blocker إلى Neutral/Engaged | tracked |
| EB Touchpoint Frequency | ≥ 2 شهريًا للحسابات النشطة |
| Total Committee Coverage | ≥ 80% من الأدوار الـ 10 |

---

## 9. الربط

- [`STAKEHOLDER_MAPPING_AR.md`](STAKEHOLDER_MAPPING_AR.md) — الأساس.
- [`ENTERPRISE_DEAL_RISK_REVIEW_AR.md`](ENTERPRISE_DEAL_RISK_REVIEW_AR.md) — `champion` و `blocker` risks.
- [`MUTUAL_ACTION_PLAN_AR.md`](MUTUAL_ACTION_PLAN_AR.md) — ترتيب المراحل.
- `docs/enterprise/ENTERPRISE_OBJECTION_BANK_AR.md` — بنك الاعتراضات.

---

> **آخر تحديث:** 2026-06-03 · v0.1
