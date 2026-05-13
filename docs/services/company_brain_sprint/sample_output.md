# تقرير تنفيذي — Company Brain Sprint
## Sample Executive Report — Company Brain Sprint

**العميل (مجهول الهوية) / Customer codename:** HEALTH-C3
**القطاع / Vertical:** الرعاية الصحية / Healthcare network (6 hospitals + 12 outpatient clinics)
**المنطقة / Region:** الرياض (المقر) + جدة + مكة + الدمام + المدينة + الطائف
**النطاق المُختار / Scoped use case:** **مساعد سياسات وإجراءات داخلي** للموظفين الإداريين والممرضات وكبار الأطباء (≤ 20 مقعدًا)
**نافذة المشروع / Sprint window:** Day 1 → Day 21 (21 يوم عمل)
**تاريخ التسليم / Delivery date:** Day 21
**المعدّل بواسطة / Prepared by:** Dealix Knowledge Engineering · `engagement_id: CBS-2026-008`

> **Sample disclaimer:** التقرير اصطناعي ويوضّح جودة Sprint. لا توجد بيانات حقيقية لأي مريض. الأسماء مُستعارة، والأرقام منطقية ضمن سوق صحي سعودي.

---

## 1. الملخص التنفيذي / Executive Summary

**AR:** قمنا بـ **استيعاب 412 وثيقة** من بيئة HEALTH-C3 (سياسات، إجراءات، حلقات تدريب، عقود موردي مستلزمات، نماذج جودة JCI، إرشادات MOH/CBAHI). تم **اكتشاف 18 وثيقة حساسة** (حُجِزت في طبقة وصول مقيدة)، و**تنقيح 9 وثائق إضافية** لإخفاء PII (أسماء/أرقام هوية ظهرت في نماذج مرفقة بحوادث جودة). على 30 سؤال اختبار، أعطى المساعد **29 إجابة مع استشهاد كامل بالمصدر** و**رفض 1 سؤال خارج النطاق** (السلوك المطلوب: "لا مصدر = لا إجابة")، مع **0 تسريب PII**.

**EN:** We ingested **412 documents** from HEALTH-C3 (policies, SOPs, training, vendor contracts, JCI quality forms, MOH/CBAHI guidelines), **flagged 18 sensitive documents** (locked behind restricted-tier access), and **redacted 9 additional documents** containing PII. On a 30-question eval set, the assistant returned **29 cited answers** and **correctly refused 1 out-of-corpus question** (the desired "no source = no answer" behavior), with **zero PII leakage** across all responses.

**رقم واحد للجهة التنفيذية / One number for the CEO:**
> "Our staff now find a cited policy answer in under 8 seconds instead of 14 minutes — with 100% PDPL-compliant redaction and zero hallucinated medical instructions."

**الإجراء التالي المقترح / Recommended next step:** ترقية إلى **Policy Assistant Premium** (SAR 28,000 one-shot) لتوسيع 3 شخصيات إلى 7، إضافة 500 وثيقة جديدة، وتفعيل قناة Teams/WhatsApp. التفاصيل في القسم 9.

---

## 2. مخزون الوثائق / Document Inventory

### 2.1 الموجز / Snapshot

| المقياس / KPI | القيمة / Value | الملاحظة |
|---|---|---|
| وثائق مُستوعَبة / Documents ingested | **412** | ضمن السقف الأساسي 500 |
| Chunks مفهرَسة / Indexed chunks | 11,872 | متوسط 28.8 chunks/doc |
| الحجم الإجمالي | 1.84 GB (بعد ضغط النص) | — |
| وثائق حساسة مُعلَّمة / Sensitive flagged | **18** | RBAC مقيّد |
| وثائق تم تنقيحها لإخفاء PII / Redacted for PII | **9** | 27 حقل PII أُزيلت |
| لغة الوثائق | عربي 64%, إنجليزي 31%, مختلطة 5% | — |
| متوسط عمر الوثيقة | 84 يوم | — |
| وثائق > 90 يومًا (stale flag) | **12** | تنبيه freshness |

### 2.2 توزيع حسب الفئة / Distribution by category

| الفئة / Category | عدد الوثائق | حساسة (مقيّدة) | منقّحة (PII) | منتهية / Stale |
|---|---|---|---|---|
| سياسات سريرية / Clinical policies | 142 | 8 | 4 | 5 |
| إجراءات تشغيلية موحدة (SOPs) | 89 | 3 | 2 | 3 |
| إرشادات MOH/CBAHI | 67 | 1 | 0 | 1 |
| نماذج جودة JCI | 41 | 4 | 2 | 0 |
| سياسات الموارد البشرية | 31 | 0 | 1 | 2 |
| عقود الموردين (مستلزمات) | 26 | 2 | 0 | 1 |
| مواد تدريبية / Training | 16 | 0 | 0 | 0 |
| **المجموع** | **412** | **18** | **9** | **12** |

### 2.3 سياسة "لا مصدر = لا إجابة" / Hard rule

كل إجابة يجب أن تكون مدعومة بـ chunk واحد على الأقل من corpus موثّق (categorized) و(within scope). إذا لم يوجد مصدر، يجب أن يرد المساعد بالعبارة المعتمدة: *"لم أجد مصدرًا داخل سياسات [العميل]. يُرجى التواصل مع مالك السياسة قبل اتخاذ أي إجراء."*

---

## 3. خريطة التغطية / Coverage Map

أي فئة من الوثائق تجيب عن أي نوع من الأسئلة؟

| نوع السؤال / Question type | فئة الوثائق المُغطية | التغطية المُقاسة |
|---|---|---|
| "كيف أتعامل مع شكوى مريض؟" | Clinical policies, JCI quality forms | 100% (142 سياسة + 41 نموذج JCI) |
| "ما إجراء معايرة الجهاز X؟" | SOPs, Vendor contracts | 92% (تنقص 3 أجهزة لم تُستوعَب عقودها) |
| "ما إجازة الأمومة؟" | HR policies | 100% (31 سياسة موارد بشرية) |
| "كيف نلتزم بمتطلبات CBAHI لـ Y؟" | MOH/CBAHI guidelines, JCI forms | 100% (67 + 41) |
| "متى ينتهي عقد المورّد Z؟" | Vendor contracts | 96% (26 من ~27 عقد مفعّل) |
| "ما البروتوكول السريري لـ W؟" | Clinical policies | 100% |
| **متوسط التغطية الموزون** | — | **98%** |

> الفجوات: 3 أجهزة طبية فرعية بدون عقود محدّثة، وعقد مورّد قديم بصيغة JPG غير قابلة للقراءة الآلية. سيتم استيعاب هذه ضمن Sprint v2 المقترح.

---

## 4. نتائج التقييم / Eval Results

تم تشغيل **30 سؤال اختبار** (15 AR + 15 EN)، موزعة على الفئات الست، مع 3 شخصيات وصول مختلفة. النتائج كاملة في `eval_set_HEALTH-C3_v1.csv`.

### 4.1 ملخص النتائج / Summary

| المقياس / Metric | الهدف / Target | المحقّق / Achieved | الحالة |
|---|---|---|---|
| تغطية الاستشهاد (Citation coverage) | ≥ 95% | **96.7%** (29/30) | ✓ |
| الإجابات داخل النطاق المُستشهَدة بمصادر صحيحة | 100% (من 29) | **29/29 = 100%** | ✓ |
| سلوك "لا مصدر = لا إجابة" (out-of-corpus) | 100% رفض | **1/1 رفض صحيح** | ✓ |
| تسرّب PII في الإجابات / PII surfacing | 0% | **0/30 = 0%** | ✓ |
| دقة التحكم بالوصول / Restricted-access correctness | 100% | **3/3 شخصيات تم اختبارها** | ✓ |
| متوسط زمن الإجابة / Mean latency | ≤ 3.0s | **2.1s** | ✓ |

### 4.2 السؤال المرفوض (هذا سلوك مطلوب) / Correctly refused

السؤال: *"ما عقوبة عدم ارتداء بطاقة التعريف؟"*
السلوك: المساعد ردّ بـ: *"لم أجد سياسة حالية تنصّ على عقوبة محددة لعدم ارتداء بطاقة التعريف داخل وثائق HEALTH-C3. يُرجى التواصل مع إدارة الموارد البشرية."* ← **هذا السلوك المرغوب** (السياسة لم تكن ضمن corpus).

### 4.3 المتقصاة الإضافية / Robustness checks

| الفحص / Check | النتيجة |
|---|---|
| 5 محاولات prompt injection ("تجاهل التعليمات السابقة...") | 0/5 نجحت |
| 3 محاولات استخراج بيانات شخصية ("أعطني هوية فلان") | 0/3 نجحت |
| 4 أسئلة بلهجات سعودية (نجدية، حجازية، شرقية) | 4/4 فُهمت + ردود فصحى |
| 2 أسئلة Code-switching (عربي + إنجليزي) | 2/2 فُهمت |

---

## 5. أمثلة على أسئلة وأجوبة مع استشهادات / Sample Q&A Pairs

### 5.1 — سؤال إداري (AR)

**السؤال:** "ما الإجراء عند تسجيل ملاحظة جودة من مريض؟"

**الإجابة:**
> عند تسلّم ملاحظة جودة من مريض، يجب اتباع التالي خلال 4 ساعات من التسجيل:
> 1. تسجيل الملاحظة في نموذج **PCF-007** (Patient Complaint Form) `[POL-HC-014 §3.1]`.
> 2. إرسال نسخة إلى مكتب الجودة المركزي عبر النظام الإلكتروني `[POL-HC-014 §3.2]`.
> 3. الردّ المبدئي للمريض خلال **48 ساعة** بإقرار استلام رسمي `[POL-HC-014 §3.4]`.
> 4. الإغلاق النهائي خلال **14 يوم عمل** بحدّ أقصى `[POL-HC-014 §4.1]`.
> 5. إذا كانت الملاحظة تتضمن سلامة المرضى، إحالة فورية إلى **لجنة سلامة المرضى** `[JCI-FORM-022 §A]`.
>
> **المصادر / Sources:**
> - `POL-HC-014` — سياسة معالجة ملاحظات المرضى (rev 3.2, 2026-02)
> - `JCI-FORM-022` — نموذج تصعيد سلامة المرضى (rev 1.4, 2025-11)

### 5.2 — سؤال HR (EN)

**Question:** "How many days of maternity leave is a female nurse entitled to?"

**Answer:**
> A female employee, including nurses, is entitled to **10 weeks of paid maternity leave**, of which **4 weeks must be taken after the date of delivery** `[POL-HR-008 §5.1]`. An additional **1 month of half-pay leave** may be requested after exhausting paid maternity leave, subject to manager approval `[POL-HR-008 §5.3]`. A female employee returning to work is entitled to **a daily 1-hour nursing break for 24 months** post-delivery `[POL-HR-008 §5.4]`. These provisions align with the Saudi Labor Law update of 2023 `[REF-MOL-2023-014]`.
>
> **Sources:**
> - `POL-HR-008` — Maternity Leave Policy (rev 2.1, 2025-09)
> - `REF-MOL-2023-014` — Ministry of Labor circular (2023-06)

### 5.3 — سؤال إجراء سريري (AR)

**السؤال:** "ما خطوات تعقيم غرفة العمليات بعد الجراحة من النوع 3؟"

**الإجابة:**
> بعد جراحة من النوع 3 (متّسخة / محتمل عدوى)، يجب تطبيق بروتوكول التعقيم **Terminal Cleaning Tier 3** التالي:
> 1. إخلاء الغرفة وفصل التيار عن الأجهزة الحساسة `[SOP-OR-031 §2.1]`.
> 2. تطبيق محلول **Sodium Hypochlorite 0.5%** على جميع الأسطح غير المسامية لمدة 10 دقائق `[SOP-OR-031 §3.2]`.
> 3. تشغيل **UV-C disinfection unit** لمدة 30 دقيقة (طول موجي 254 nm) `[SOP-OR-031 §3.5]`.
> 4. تبديل **HEPA filter** إذا تجاوز عمر الفلتر 90% من العمر المعتمد `[SOP-OR-031 §4.1]`.
> 5. أخذ مسحة بيولوجية (Biological indicator) وانتظار النتيجة قبل إعادة استخدام الغرفة (لا تزيد عن 48 ساعة) `[SOP-OR-031 §4.4]`.
> 6. توثيق العملية في **سجل التعقيم الإلكتروني** قبل التسليم `[POL-IPC-007 §6]`.
>
> **المصادر / Sources:**
> - `SOP-OR-031` — تعقيم غرف العمليات (rev 4.0, 2026-01)
> - `POL-IPC-007` — سياسة مكافحة العدوى (rev 2.5, 2025-10)

> **ملاحظة:** كل استشهاد قابل للنقر في الواجهة، ويفتح الـ chunk الأصلي في الوثيقة المصدر.

---

## 6. قواعد الوصول حسب الشخصية / Access Rules (3 Personas Tested)

### 6.1 الشخصيات المُختبَرة / Personas tested

| الشخصية / Persona | الدور / Role | الوصول الافتراضي | اختبار |
|---|---|---|---|
| **P1 — موظف إداري عام** | استقبال، خدمات | فئات: HR, Training, MOH/CBAHI العامة | ✓ يرى الإجابات العامة فقط |
| **P2 — ممرضة سريرية** | تمريض | فئات: Clinical policies, SOPs, IPC, JCI forms | ✓ يرى الإجراءات السريرية لكن ليس عقود الموردين |
| **P3 — مدير جودة** | الجودة والامتثال | كل الفئات بما فيها 18 وثيقة حساسة (بعد signoff) | ✓ يصل لكل شيء |

### 6.2 نتائج اختبار التحكم بالوصول / Access-control test results

كل شخصية اختُبرت بـ 6 أسئلة (إجمالي 18): 6 ضمن وصولها (يجب أن يجيب) + 6 خارج وصولها (يجب أن يرفض).

| الشخصية | داخل النطاق (يجب الإجابة) | خارج النطاق (يجب الرفض) | الدقة الإجمالية |
|---|---|---|---|
| P1 | 6/6 إجابات صحيحة | 6/6 رفض صحيح | **100%** |
| P2 | 6/6 إجابات صحيحة | 6/6 رفض صحيح | **100%** |
| P3 | 6/6 إجابات صحيحة (تشمل sensitive) | 0/0 — كلها داخل النطاق | **100%** |

**مثال على رفض RBAC:** عندما طلبت P1 (موظف عام) عقد مورّد، ردّ النظام: *"هذا المستند مقيّد. تواصل مع مدير الجودة (P3) للوصول."*

---

## 7. تقرير حداثة الوثائق / Freshness Report

12 وثيقة تجاوز عمرها 90 يومًا (آخر تحديث رسمي معتمد). موزّعة كالتالي:

| الفئة | عدد الوثائق القديمة | أقدمها (أيام) | الإجراء الموصى به |
|---|---|---|---|
| Clinical policies | 5 | 412 يوم | مراجعة فورية مع رئيس القسم |
| SOPs | 3 | 287 يوم | مراجعة خلال 30 يومًا |
| HR | 2 | 198 يوم | مراجعة عادية |
| MOH/CBAHI | 1 | 154 يوم | تأكد من نشر تعديل CBAHI الأخير |
| Vendor contracts | 1 | 391 يوم | تجديد قبل الانتهاء |
| **المجموع** | **12** | — | — |

**النظام يُرسل تنبيه تلقائي** إلى مالك الوثيقة عند تجاوز عتبة 90 يومًا (يُسجَّل في `event_store` كـ `freshness.alert.sent`). تمت إعادة جدولة 4 وثائق للمراجعة هذا الأسبوع نتيجة هذا التنبيه.

---

## 8. المخاطر وملاحظات PDPL / Risks & PDPL Notes

### 8.1 المخاطر التشغيلية / Operational risks

| المخاطرة / Risk | الشدة | الحالة | التخفيف |
|---|---|---|---|
| وثيقة قديمة تُستخدم كمصدر بعد انتهاء صلاحيتها | متوسطة | freshness flag مفعّل | إعادة تأكيد سنوي بالـ document owner |
| تخمين الـ LLM لإجابة بدون مصدر | منخفضة جدًا | 0 حالة في الاختبار | "لا مصدر = لا إجابة" مُطبَّقة بـ guardrail |
| صلاحية موسّعة غير مقصودة | منخفضة | RBAC v2 مفعّل | مراجعة ربع سنوية للأدوار |
| نسخة استشهاد قديمة في الإجابة | منخفضة | versioning مفعّل | إعادة فهرسة عند كل تعديل وثيقة |

### 8.2 ملاحظات حول المادة 27 من PDPL (البيانات الصحية)

نظام حماية البيانات الشخصية السعودي يُصنّف بيانات الصحة كـ **بيانات حساسة** (المادة 1)، وتُعامَل بقيود أعلى وفق المادة 27. ضمن هذا Sprint:

- **لم تُستوعب أي ملفات مرضى**. النطاق محصور على سياسات/إجراءات/تدريب/عقود — لا توجد سجلات سريرية لمرضى أفراد.
- 9 وثائق احتوت على PII بشكل عرضي (مثلًا اسم موظف في نموذج حادثة جودة قديم) تم تنقيحها بالكامل قبل الفهرسة.
- صلاحيات الوصول مُسجّلة في `event_store` كـ `access.policy.applied` لكل query.
- ملف **Data Processing Record** تم تجهيزه حسب المادة 31 (الجدول 1) — مرفق في `dpia_HEALTH-C3.pdf`.
- جهة الاتصال الخاصة بحماية البيانات (DPO) عند العميل تم تحديدها في الـ SOW.

### 8.3 ملاحظات حول CBAHI

تمت مواءمة مساعد السياسات مع متطلبات CBAHI **IMK.1** (Information Management — Knowledge resources) و**IMK.2** (Currency of resources)، وتم تضمين سجل الحداثة كدليل مباشر للمراجع CBAHI القادم.

---

## 9. الإجراء التالي المقترح / Next Step Proposal

نقترح **مسارين** للنمو على هذا الأساس:

### **خيار A — Sales Knowledge Assistant (تكاملي)**

| البند | التفاصيل |
|---|---|
| **السعر** | **SAR 18,000** (one-shot, 14 يوم عمل) |
| **النطاق** | بناء مساعد منفصل لفريق المبيعات (عروض الأسعار، الخدمات، الشركاء) — حتى 250 وثيقة جديدة |
| **القيمة المتوقعة** | تقليص زمن إعداد العرض من 4 ساعات إلى 35 دقيقة (≈ SAR 102,000 توفير سنوي) |

### **خيار B — Policy Assistant Premium (موصى به)**

| البند | التفاصيل |
|---|---|
| **السعر** | **SAR 28,000** (one-shot, 21 يوم عمل) |
| **يشمل** | توسيع corpus من 412 إلى 900 وثيقة + إضافة 4 شخصيات وصول (إجمالي 7) + قناة Microsoft Teams + قناة WhatsApp Business + تدريب 50 موظف |
| **القيمة المتوقعة** | تقليص زمن البحث عبر الشبكة من ~14 دقيقة إلى < 12 ثانية على 800+ موظف = توفير **SAR 540,000+ سنويًا** (تقدير محافظ) |

### **خيار C — Monthly Knowledge Ops Retainer**
- **SAR 7,500/شهريًا** لصيانة فهرس Corpus + 20 وثيقة شهريًا + monthly eval refresh + QBR.
- يُوصى به كإضافة لـ A أو B.

> **للقبول، رد على هذا التقرير بـ "A" أو "B" أو "B+C"، وسنرسل SOW جاهزًا للتوقيع خلال 24 ساعة.**

---

## 10. ملخص حزمة الإثبات / Proof Pack Summary

| المقياس / KPI | قبل / Before | بعد / After | الفرق / Δ |
|---|---|---|---|
| Documents searchable (with citations) | 0 | 412 | +412 |
| Citation coverage on answers | n/a | 96.7% (29/30) | ✓ |
| PII surfacing in answers | unknown | **0%** | safer |
| Out-of-corpus refusal rate | unknown | 100% (correct) | ✓ |
| RBAC tests passed | 0 | 18/18 | +18 |
| Mean search time (employee survey) | 14 min | < 12 sec | -98% |
| Stale-document tracking | none | automated > 90d | ✓ |
| Audit-log coverage | 0% | 100% of queries | ✓ |
| Prompt-injection attempts succeeded | unknown | 0/5 | ✓ |

### المرفقات / Deliverables shipped

- `corpus_inventory_HEALTH-C3.csv` (412 وثيقة + metadata)
- `eval_set_HEALTH-C3_v1.csv` (30 سؤال + إجابات + استشهادات)
- `rbac_persona_matrix_HEALTH-C3.pdf`
- `freshness_report_HEALTH-C3.pdf`
- `dpia_HEALTH-C3.pdf` (PDPL Art. 31 record)
- `runbook_company_brain_HEALTH-C3.pdf` (16 صفحة)
- `training_recording_2h.mp4` (جلسة تدريب الفريق)
- `proof_pack_HEALTH-C3_v1.pdf`

### شهادة العميل (مسودة بانتظار الموافقة) / Customer testimonial (draft)

> "أصبحت الإجابات تأتي مع مصدر مرقّم — وهذا ما غيّر الثقة عند فريق التمريض. لن نعود للبحث اليدوي مرة أخرى."
> — مدير الجودة، HEALTH-C3

---

**تواصل / Contact:** sales@dealix.me · `engagement_id: CBS-2026-008`

*هذا تقرير اصطناعي (Sample) من Dealix Knowledge Engineering. يوضّح جودة الإخراج، لا يمثّل عميلًا حقيقيًا.*
