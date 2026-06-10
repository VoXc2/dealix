# Stakeholder Mapping — خريطة أصحاب المصلحة

> **Status:** READY (structure) / PARTIAL (message angles — قابلة للتحسين المستمر)
> **Evidence Level:** assumption (design-time framework)
> **Owner:** Sales Lead (Primary) · CS Lead (Secondary)
> **الاستخدام:** لكل حساب ABM نشط. الإلزامي قبل إرسال أي عرض سعر.

---

## 1. لماذا خريطة Stakeholders؟

في B2B المؤسسي السعودي، **لا يوجد "The Decision Maker" واحد**. يوجد **Buying Committee** يتكوّن من 6–10 أشخاص. تجاهل أيٍّ منهم = فشل الصفقة.

**القاعدة الذهبية:**

> **Multi-threading = النجاح. Single-threaded deal = حقل ألغام.**

**الـ Multi-threading Index المستهدف:** ≥ 4 أصحاب مصلحة في حالة `engaged` أو `supportive` قبل أي `proposal`.

---

## 2. الأدوار العشرة المعيارية

> كل دور أدناه له: ما يهمّه، اعتراضه المتوقّع، الإثبات المطلوب، الزاوية العربية للرسالة، درجة تأثير القرار (1–5).

### 2.1 Economic Buyer (صانع القرار الاقتصادي)

> **التعريف:** الشخص الذي يملك صلاحية التوقيع/الموافقة على الميزانية.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | العائد على الاستثمار (ROI)؛ تأثير على الأرباح؛ تقليل المخاطر المالية؛ مصداقية البائع |
| **الاعتراض المتوقّع** | «الميزانية غير متاحة هذا الربع» / «لم نرَ ROI كافٍ» / «عندنا مزوّد حالي» |
| **الإثبات المطلوب** | Business Case (صفحة واحدة)، TCO analysis، reference مشابهة، case study |
| **زاوية الرسالة (عربي)** | «هدفنا هو [X] من [Y] ريال. الاستثمار [Z] يعود خلال [W] شهرًا.» |
| **درجة التأثير** | 5 |
| **متى يُقابل** | في 3 لحظات: تعريف مبدئي (مع Champion)، بعد Business Case مكتمل، وقبل التوقيع |

### 2.2 Business Owner (مالك النشاط التجاري)

> **التعريف:** الشخص الذي يتبعه الفريق الذي سيستخدم المنتج (VP Sales, Head of Marketing, etc.).

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | تحقيق هدف فريقه (OKRs)؛ سهولة الاستخدام؛ عدم تعطيل العمليات؛ رضا فريقه |
| **الاعتراض المتوقّع** | «فريقي مشغول» / «لا وقت لتجربة شيء جديد» / «كيف سيؤثر على KPIs الحالية؟» |
| **الإثبات المطلوب** | Pilot SOW بنطاق محدود، demo مخصّص لفريقه، testimonial من peer |
| **زاوية الرسالة (عربي)** | «[الفريق] سيرى [نتيجة محددة] في [مدة]، بدون تغيير جذري في سير العمل.» |
| **درجة التأثير** | 4 |
| **متى يُقابل** | قبل وبعد كل اجتماع Discovery، وفي منتصف Pilot |

### 2.3 Technical Reviewer (المراجع التقني)

> **التعريف:** IT Lead، Data Engineering Lead، Solutions Architect — الشخص الذي يقيّم الجدوى التقنية.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | سهولة الـ integration؛ نظافة الـ APIs؛ أداء النظام؛ عدم تعطيل البنية القائمة |
| **الاعتراض المتوقّع** | «لا API متاح» / «أمناؤنا لا يثقون» / «Stack غير متوافق» |
| **الإثبات المطلوب** | Technical Architecture Overview، sandbox/demo، sample integration، list of integrations |
| **زاوية الرسالة (عربي)** | «نعمل فوق [stack] بدون أي تغيير في بنيتكم، عبر [integration pattern].» |
| **درجة التأثير** | 4 |
| **متى يُقابل** | بعد Business Case مباشرة، وقبل أي Security Review |

### 2.4 Security / Privacy Reviewer (مراجع الأمن والخصوصية)

> **التعريف:** CISO، Data Protection Officer، IT Security Manager.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | PDPL compliance؛ NCA ECC؛ مكان تخزين البيانات؛ التشفير؛ Audit logs؛ Data residency |
| **الاعتراض المتوقّع** | «أين تُخزّن البيانات؟» / «هل أنتم معتمدون؟» / «ما مدة الاحتفاظ؟» |
| **الإثبات المطلوب** | DPA موقّع، Security Overview، Privacy Overview، قائمة الحوادث السابقة (إن وُجدت) |
| **زاوية الرسالة (عربي)** | «بياناتكم تبقى في [region]. DPA مكتمل. ندعم PDPL وNCA ECC. لا نموذج لغوي يُدرّب على بياناتكم.» |
| **درجة التأثير** | 4 (يمكن أن يوقف الصفقة بالكامل) |
| **متى يُقابل** | فورًا بعد Technical Reviewer وقبل أي commit كتابي |

### 2.5 Operations (العمليات)

> **التعريف:** من يدير العمليات اليومية (Operations Manager, COO, Director of Service Delivery).

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | التشغيل السلس؛ الـ SLAs؛ الاستمرارية؛ توفّر الدعم |
| **الاعتراض المتوقّع** | «من سيستجيب عند انقطاع الخدمة؟» / «ما الـ uptime؟» / «كم وقت الاستجابة؟» |
| **الإثبات المطلوب** | SLA SLO، Support Model، Incident Response Plan |
| **زاوية الرسالة (عربي)** | «[SLA percentage] uptime، [MTTR] للاستجابة، فريق دعم محلي في [timezone].» |
| **درجة التأثير** | 3 |
| **متى يُقابل** | بعد Security وقبل توقيع العقد |

### 2.6 Daily User (المستخدم اليومي)

> **التعريف:** من سيستخدم المنتج فعليًا (SDR، Account Executive، Operations Analyst، إلخ).

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | سهولة الاستخدام؛ تقليل الجهد اليدوي؛ نتائج سريعة؛ لا منحنى تعلّم حاد |
| **الاعتراض المتوقّع** | «منتج آخر مشابه، لماذا نغيّر؟» / «لا وقت للتدريب» |
| **الإثبات المطلوب** | UI demo، تدريب مصغّر، quick-win خلال أسبوع |
| **زاوية الرسالة (عربي)** | «أول [مهمة] ستختصر من وقتك [N] دقيقة يوميًا.» |
| **درجة التأثير** | 2 (لكن حاسم للتجديد) |
| **متى يُقابل** | في Discovery المبكر، وخلال Pilot |

### 2.7 Procurement (المشتريات)

> **التعريف:** Procurement Manager، Vendor Manager، Contract Specialist.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | بنود العقد؛ الأسعار؛ شروط الدفع؛ خروج آمن؛ Risk mitigation |
| **الاعتراض المتوقّع** | «لا يوجد مزوّد معتمد في قائمتنا» / «السعر مرتفع» / «نحتاج بنود جديدة» |
| **الإثبات المطلوب** | MSA، SOW، قائمة بنود placeholders، جدول الدفع |
| **زاوية الرسالة (عربي)** | «[شروط دفع]، [فترات تجربة]، [خروج آمن خلال W أسبوع]، بنود مرنة لـ [حالة خاصة].» |
| **درجة التأثير** | 4 (Gate-keeper — يقدر يبطئ أو يوقف) |
| **متى يُقابل** | بعد Business Case وقبل التوقيع |

### 2.8 Legal (الشؤون القانونية)

> **التعريف:** Legal Counsel، General Counsel.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | امتثال؛ حماية IP؛ تحديد المسؤولية؛ Data processing |
| **الاعتراض المتوقّع** | «بند X غير مقبول» / «نحتاج Data Locality صريحة» / «ما Liability Cap؟» |
| **الإثبات المطلوب** | DPA موقّع، بنود Liability (placeholders)، Terms of Service v2 |
| **زاوية الرسالة (عربي)** | «بنودنا مبنية على [معيار]، Liability Cap قابل للتفاوض ضمن [نطاق]، IP ملكية العميل.» |
| **درجة التأثير** | 3 (لكنها Veto Power في بعض الشركات) |
| **متى يُقابل** | في نفس الوقت مع Procurement |

### 2.9 Champion (البطل الداخلي)

> **التعريف:** الشخص الذي يروّج داخليًا لحلكم، غالبًا لأن نجاحك = نجاحه.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | حلّ مشكلة حقيقية له؛ الظهور كفائز داخليًا؛ عدم المخاطرة السياسية بلا مقابل |
| **الاعتراض المتوقّع** | «كيف أقنع زملائي؟» / «ماذا لو فشل المشروع؟» |
| **الإثبات المطلوب** | Business Case، Pilot plan واضح، Reference calls، Political cover |
| **زاوية الرسالة (عربي)** | «مشروعك هذا سيظهر [نتيجة محددة] لـ [Board/EB]، وأنا معك خطوة بخطوة.» |
| **درجة التأثير** | 5 (حاسم — لا صفقة بدون بطل) |
| **متى يُقابل** | مبكرًا جدًا، ويُحافظ عليه أسبوعيًا |

### 2.10 Blocker (المعاكس)

> **التعريف:** شخص يُعارض داخليًا — قد يكون BISO سابق لمزود آخر، أو شخص خسارة سلطته بسبب منتجك.

| البُعد | التفصيل |
|--------|---------|
| **ما يهمّه** | الحفاظ على وضعه الراهن؛ تقليل المخاطر الشخصية |
| **الاعتراض المتوقّع** | «هذا المنتج لم يثبت في السوق» / «لا أرى ROI» / «منافسنا أفضل» |
| **الإثبات المطلوب** | تفهّم موقفه، إجابة علمية على أسئلته، Reference calls من خارج دائرته |
| **زاوية الرسالة (عربي)** | «أقدّر قلقك. هنا إجابات صريحة: [X]، [Y]، [Z]. أتطلع لفرصة توضيحها لك شخصيًا.» |
| **درجة التأثير** | 3 (يمكن أن يكون Veto) |
| **متى يُقابل** | في أقرب وقت ممكن — التجنّب يُفاقم المشكلة |

---

## 3. Multi-threading Rule (القاعدة الصارمة)

> **الشرط الأدنى قبل أي `proposal`:**
> - ≥ 4 stakeholders في حالة `engaged` أو `supportive`.
> - على الأقل 1 منهم `Economic Buyer` أو `Champion` نشط.
> - لا `blocker` نشط بدون mitigation plan.

**التعقّب:** راجع `data/enterprise_sales/stakeholders.jsonl` و `data/enterprise_sales/accounts.jsonl` (حقل `stakeholder_map`).

---

## 4. مراحل رسم الخريطة (Mapping Phases)

### المرحلة 1: قبل أي تواصل رسمي (Pre-Engagement)
- حدد 6–10 أسماء مُتوقّعة (معظمهم placeholders).
- صنّفهم حسب الدور.
- أضف `decision_influence` افتراضي (assumption).

### المرحلة 2: بعد الاجتماع الأول (After First Meeting)
- اسأل: «من سيراجع القرار من الناحية [X]؟». أضف stakeholders.
- اطلب **مُقدّمة رسمية** لكل شخص مؤثر (Referral).

### المرحلة 3: قبل Business Case (Before Business Case)
- تأكد أن EB و Business Owner و Champion على الأقل `engaged`.
- حدد Blocker (إن وُجد).

### المرحلة 4: قبل Proposal (Before Proposal)
- ≥ 4 stakeholders engaged.
- Procurement و Legal Reviewer على الأقل `not_contacted` (سنلتقي بهم في خطوة لاحقة).
- Security Reviewer `intro_made` على الأقل.

### المرحلة 5: قبل التوقيع (Before Signature)
- كل stakeholders in `signed_off` أو `supportive` أو `neutral`.
- لا blockers نشطين.

---

## 5. قالب Stakeholder Entry (يُحفظ في JSONL)

> يطابق `schemas/stakeholder.schema.json`.

**مثال (Placeholder):**

```json
{
  "stakeholder_id": "STK-001",
  "account_id": "ACC-ENT-001",
  "name_placeholder": "شخص_A_CRO",
  "role": "champion",
  "title_hint": "Chief Revenue Officer",
  "department": "Revenue",
  "seniority_band": "c_suite",
  "decision_influence": 5,
  "cares_about": ["OKRs", "تنفيذ مبادرة Digital Sales 2027", "مصداقية Board"],
  "objection": "كيف أضمن أن المشروع لن يفشل في أول 90 يومًا؟",
  "proof_needed": ["Business Case", "Pilot SOW", "Reference call"],
  "message_angle": "مبادرتك 'Digital Sales 2027' ستظهر أول نتائج قابلة للقياس خلال 8 أسابيع، مع Pilot محدود لا يعرقل العمليات.",
  "engagement_status": "engaged",
  "relationship_health": "warm",
  "evidence_level": "assumption"
}
```

---

## 6. دورة تحديث Stakeholder Map

| التكرار | المهمة | المالك |
|---------|--------|--------|
| أسبوعيًا | تحديث `engagement_status` و `last_touch_at` | Sales Lead |
| أسبوعيًا | تحديد stakeholders راكدين (no touch > 14 يوم) | Sales Lead |
| شهريًا | مراجعة `relationship_health` و `decision_influence` | Sales Lead |
| عند تغيير في الحساب | إضافة/حذف stakeholder | Sales Lead |
| ربع سنوي | تدقيق كامل للخريطة | Sales Lead + Founder |

---

## 7. Anti-Patterns (تجنّبها)

- ❌ خريطة stakeholders بدون قرار EB.
- ❌ الاعتماد على بطل واحد فقط (Single-Champion Risk).
- ❌ تجاهل Procurement حتى اليوم الأخير.
- ❌ تجاهل Blocker والأمل في انسحابه.
- ❌ نسخ رسالة واحدة لكل stakeholder (لا تخصيص).
- ❌ التعامل مع Daily User كـ Decision Maker.

---

## 8. الربط

- [`BUYING_COMMITTEE_PLAYBOOK_AR.md`](BUYING_COMMITTEE_PLAYBOOK_AR.md) — كيف تُشغّل الخريطة اجتماعيًا.
- [`ENTERPRISE_DISCOVERY_AR.md`](ENTERPRISE_DISCOVERY_AR.md) — كيف تكتشف stakeholders أثناء الاكتشاف.
- [`ENTERPRISE_DEAL_RISK_REVIEW_AR.md`](ENTERPRISE_DEAL_RISK_REVIEW_AR.md) — `champion` و `blocker` risks.

---

> **آخر تحديث:** 2026-06-03 · v0.1
