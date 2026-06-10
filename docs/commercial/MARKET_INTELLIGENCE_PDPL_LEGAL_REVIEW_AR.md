# مراجعة داخلية: PDPL · DPA · إقامة البيانات · لغة العقود والموقع

**الحالة:** مراجعة تشغيلية داخلية (ليست استشارة قانونية)  
**الجمهور:** المؤسس، المبيعات، الهندسة قبل توقيع عميل مؤسسي  
**آخر تحديث:** 2026-05-18  
**مصدر السياق السوقي:** مختصر استخبارات 2025–2026 (سوق SaaS سعودي، PDPL، إقامة/نقل عبر الحدود)

> **تنبيه:** أي وعد في عقد أو صفحة عامة يجب أن يمر بمحامٍ سعودي قبل النشر النهائي. راجع [`docs/LEGAL_ENGAGEMENT.md`](../LEGAL_ENGAGEMENT.md) و[`docs/wave8/DPA_CHECKLIST_AR_EN.md`](../wave8/DPA_CHECKLIST_AR_EN.md).

---

## 1) خريطة المراجع داخل الريبو

| الموضوع | وثيقة / أصل |
|---------|-------------|
| خريطة مواد PDPL ↔ تنفيذ | [`docs/legal/COMPLIANCE_CERTIFICATIONS.md`](../legal/COMPLIANCE_CERTIFICATIONS.md) |
| DPA كامل | [`docs/DPA_DEALIX_FULL.md`](../DPA_DEALIX_FULL.md) · قالب pilot [`docs/DPA_PILOT_TEMPLATE.md`](../DPA_PILOT_TEMPLATE.md) |
| قائمة تحقق قبل التوقيع | [`docs/wave8/DPA_CHECKLIST_AR_EN.md`](../wave8/DPA_CHECKLIST_AR_EN.md) |
| DSAR (طلبات أصحاب البيانات) | [`docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md) |
| خرق بيانات | [`docs/ops/PDPL_BREACH_RUNBOOK.md`](../ops/PDPL_BREACH_RUNBOOK.md) · [`docs/PDPL_BREACH_RESPONSE_PLAN.md`](../PDPL_BREACH_RESPONSE_PLAN.md) |
| قواعد بيانات وحوكمة | [`docs/governance/PDPL_DATA_RULES.md`](../governance/PDPL_DATA_RULES.md) |
| تشغيل واعٍ بالخصوصية | [`docs/saudi/PDPL_AWARE_OPERATIONS.md`](../saudi/PDPL_AWARE_OPERATIONS.md) |
| معالجون فرعيون (عام) | [`docs/legal/COMPLIANCE_CERTIFICATIONS.md`](../legal/COMPLIANCE_CERTIFICATIONS.md) § Sub-Processor · `landing/sub-processors.html` |
| سياسة خصوصية | `landing/privacy-policy.html` · [`docs/PRIVACY_POLICY_v2.md`](../PRIVACY_POLICY_v2.md) |
| جدول استضافة وقرار region | [`INFRA_HOSTING_REGION_RUBRIC_AR.md`](INFRA_HOSTING_REGION_RUBRIC_AR.md) |

---

## 2) ما يُقال بأمان في العروض والموقع (مسودة معتمدة داخلياً)

### مسموح (مع وجود تنفيذ في المنتج)

| العبارة (AR) | الشرط التشغيلي |
|--------------|----------------|
| «مسودات خارجية فقط — لا إرسال واتساب/لينكد إن بارد ولا Gmail خارجي بدون موافقتك» | قواعد AGENTS.md + حوكمة وكلاء |
| «سجل تدقيق لإجراءات AI والبيانات الشخصية حيث يُفعَّل المسار» | `api/middleware/http_stack.py` · Revenue Memory |
| «Decision Passport: قرار + مستوى أدلة قبل إجراء خارجي» | Revenue OS / anti-waste |
| «نعالج بيانات العملاء بموجب عقد (DPA) عند التعاقد» | DPA موقّع قبل معالجة بيانات طرف ثالث |
| «نُمكّن حقوق أصحاب البيانات وفق SOP داخلي (وصول، تصحيح، محو حيث يسمح القانون)» | [`PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md) |
| «بيانات الدفع عبر Moyasar — Dealix لا يخزّن بيانات البطاقة» | تكامل Moyasar |

### يُتجنَّب أو يُقيَّد (حتى مراجعة محامٍ)

| لا تقل | بدلاً منه |
|--------|-----------|
| «معتمد من SDAIA» / «PDPL certified» | «مصمم وفق مبادئ PDPL» + إحالة لسياسة الخصوصية وDPA |
| «جميع البيانات داخل السعودية 100%» | صِف **منطقة الاستضافة الفعلية** و**المعالجين** (انظر rubric الاستضافة) |
| «لا نقل عبر الحدود أبداً» | «نقل محدود لمعالجين مدرجين بموافقة/بنود عقدية» إن كان واقعياً |
| «امتثال كامل مضمون» | «إجراءات امتثال قابلة للتدقيق» + قائمة sub-processors |
| أرقام غرامات أو مواد قانونية بدون مصدر رسمي | أحِل للعميل إلى مستشارهم القانوني |

---

## 3) DPA — نقاط إلزامية قبل التوقيع (ملخص تنفيذي)

استخدم القائمة الكاملة في [`docs/wave8/DPA_CHECKLIST_AR_EN.md`](../wave8/DPA_CHECKLIST_AR_EN.md). الحد الأدنى:

1. **الأدوار:** العميل = Controller لبيانات عملائه؛ Dealix = Processor (أو Controller لبيانات علاقة Dealix فقط).
2. **النطاق:** فئات البيانات، الغرض، مدة الاحتفاظ، منطقة التخزين **مطابقة لـ INFRA rubric**.
3. **الحقوق:** وصول، تصحيح، محو (مع استثناءات قانونية/فوترة ZATCA).
4. **الخرق:** إخطار Controller؛ مساعدة في إخطار SDAIA عند اللزوم — **لا تلتزم بـ 72 ساعة في العقد إلا بعد تأكيد محامٍ** (المراجع السوقية تذكر 72h؛ ثبّت النص قانونياً).
5. **نقل عبر الحدود:** إما حظر، أو قائمة معالجين + ضمانات تعاقدية (SCC/موافقة).
6. **المعالجون الفرعيون:** قائمة محدثة + حق اعتراض معقول.
7. **حذف عند إنهاء العقد:** إجراء محو/إرجاع موثّق.

**قبل عميل > 50K SAR/سنة:** [`COMPLIANCE_CERTIFICATIONS.md`](../legal/COMPLIANCE_CERTIFICATIONS.md) § Pre-Enterprise-Customer Checklist.

---

## 4) إقامة البيانات — وعود متسقة مع الواقع التقني

| طبقة | الواقع الحالي (تحقق قبل كل عقد) | وعد آمن في العقد |
|------|----------------------------------|------------------|
| Postgres (إنتاج) | غالباً Railway / مزود سحابي — **تحقق من region في لوحة المزود** | «منطقة الاستضافة: [X] كما في الملحق التقني» |
| نسخ احتياطي | قد يكون GCC (مثلاً S3 me-south-1) أو مزود المنصة | «نسخ مشفّرة؛ منطقة النسخ: [Y]» |
| LLM (Anthropic/OpenAI) | معالجة خارج المملكة محتملة | «معالجة نماذج لغوية عبر معالجين مدرجين؛ تقليل PII في الموجهات» |
| بوابة دفع | Moyasar (KSA) | «الدفع خارج نطاق تخزين Dealix للبطاقات» |

**لا تُدرج «إقامة سعودية كاملة» في MSA** حتى يُثبت region الإنتاج + النسخ + قائمة المعالجين في [`INFRA_HOSTING_REGION_RUBRIC_AR.md`](INFRA_HOSTING_REGION_RUBRIC_AR.md).

---

## 5) فجوات وإجراءات (من المراجعة الداخلية)

| # | الفجوة | الأولوية | الإجراء |
|---|--------|----------|---------|
| G1 | تسجيل Controller لدى SDAIA | متوسطة (بعد عميل مؤسسي #1) | [`COMPLIANCE_CERTIFICATIONS.md`](../legal/COMPLIANCE_CERTIFICATIONS.md) |
| G2 | نموذج DSAR على الموقع | منخفضة | `dealix.me/privacy#dsar` — backlog Wave 8 |
| G3 | توحيد نصوص المبيعات مع rubric الاستضافة | عالية قبل كل عقد | تحديث ملحق تقني لكل عميل |
| G4 | مراجعة محامٍ لـ DPA/MSA v2 | عالية قبل عميل #4+ | [`LEGAL_ENGAGEMENT.md`](../LEGAL_ENGAGEMENT.md) |
| G5 | DPIA لكل use case عمودي (وكالات، عقار، إلخ) | متوسطة عند أول عميل في القطاع | قالب في enterprise package |

---

## 6) جمل جاهزة للعقود والموقع (نسخ بعد مراجعة محامٍ)

**عربي — فقرة قصيرة (MSA ملحق امتثال):**

> تلتزم Dealix بمعالجة البيانات الشخصية وفق نظام حماية البيانات الشخصية (PDPL) المعمول به في المملكة العربية السعودية، وبموجب اتفاقية معالجة البيانات (DPA) الموقّعة بين الطرفين. لا تنفّذ Dealix اتصالات تسويقية خارجية تلقائية دون موافقة صريحة مسبقة من العميل على كل إجراء. تُحدَّد مناطق التخزين والمعالجون الفرعيون في الملحق التقني وقائمة المعالجين المنشورة.

**English — short (website trust block):**

> Dealix is built PDPL-aware: draft-and-approve external actions, auditable revenue memory, and a published sub-processor list. Storage regions and DPAs are defined per customer contract.

---

## 7) خريطة مواد PDPL → تنفيذ (ملحق)

| موضوع | مرجع سوقي/قانوني | تنفيذ Dealix | ملاحظة مبيعات |
|-------|------------------|--------------|---------------|
| أساس قانوني | موافقة / عقد / مصلحة مشروعة | consent builders في `integrations/pdpl.py` | وثّق الأساس per قناة |
| إشعار الخصوصية | قبل الجمع | privacy policy + just-in-time | landing + in-app |
| حقوق أصحاب البيانات | وصول، تصحيح، محو، نقل | DSAR SOP + export/erasure | 30 يوم هدف |
| سجل معالجة | 5 سنوات أدبيات | middleware + revenue events | لا PII خام في logs |
| خرق | إخطار جهة — **ثبّت المدة قانونياً** | breach runbook + builder | لا تعد 72h في عقد بدون محامٍ |
| معالجون فرعيون | إفصاح + عقد | sub-processors.html | حدّث عند كل مزود جديد |
| نقل عبر الحدود | قيود قطاعية | DPA + ملحق INFRA | لا وعد «صفر نقل» |
| DPO | عند معالجة واسعة | template appointment | بعد enterprise #1 |
| تسجيل Controller | NDGP عند اللزوم | G1 في فجوات | بعد أول عميل مؤسسي |

**مصادر خارجية:** [SDAIA PDPL Knowledge](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPLCP/) · [PwC PDPL series PDF](https://www.pwc.com/m1/en/blogs/pdf/ksa-personal-data-protection-law-series-part-1.pdf)

---

## 8) أسئلة قسم قانوني العميل (10) — إجابات قصيرة

| # | سؤال | إجابة |
|---|------|--------|
| 1 | من Controller؟ | العميل لبيانات عملائه؛ Dealix Processor |
| 2 | أين التخزين؟ | ملحق INFRA — region مؤكد من المزود |
| 3 | قائمة المعالجين؟ | sub-processors.html + ملحق العقد |
| 4 | حق المحو؟ | نعم حسب SOP مع استثناءات ZATCA/قانون |
| 5 | تدريب نماذج على بياناتنا؟ | لا بيع بيانات؛ معالجة لأداء العقد فقط |
| 6 | إرسال تسويقي تلقائي؟ | لا — موافقة per إجراء |
| 7 | سجل تدقيق؟ | نعم على مسارات محددة |
| 8 | DPIA؟ | عند طلب عمودي منظّم — G5 |
| 9 | إخطار خرق؟ | runbook + تعاون مع Controller |
| 10 | SCC / نقل؟ | بنود DPA — مراجعة محامٍ |

تفصيل RFP: [`MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md`](MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md)

---

## 9) قطاعات منظّمة — تصعيد

| قطاع | سؤال إضافي | إجراء |
|------|------------|--------|
| مالية | SAMA / نقل بيانات | محامٍ + استضافة D أو C |
| صحة | بيانات حساسة | DPIA إلزامي قبل POC |
| حكومة | إقامة محلية | VPS KSA + عقد ثنائي اللغة |
| وكالة (افتراضي) | PDPL + contactability | DPA قياسي + rubric A/B |

---

## 10) سجل المراجعة

| التاريخ | من | ملاحظة |
|---------|-----|--------|
| 2026-05-18 | Agent (خطة استخبارات سوق) | إنشاء وثيقة مراجعة داخلية + ربط بالمراجع القائمة |
| 2026-05-18 | Agent (توسع) | خريطة مواد PDPL · FAQ قانوني · قطاعات |
