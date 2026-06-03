# Dealix — خطة التشغيل الكاملة (Full Ops Master Plan)

**الغرض:** إطار شركة كاملة حول منتج قوي — بيع، تسويق، خدمة، تسليم، شركاء، مسوقون بالعمولة، حوكمة AI، وتحويل كل ذلك إلى إيراد وأدلة وتكرار.  
**القاعدة التنفيذية:** منتج قوي → إثبات قوي → قمع قوي → مبيعات قوية → تسليم قوي → دعم قوي → شركاء/عمولة قوية → أدلة قوية → ريتينر → منصة لاحقاً.

**ارتباط بالمستودع:** بنية V12 التساعية (9 أنظمة تشغيل) موثّقة في [`docs/V12_FULL_OPS_ARCHITECTURE.md`](../V12_FULL_OPS_ARCHITECTURE.md). هذه الوثيقة تترجم الاستراتيجية إلى **12 ماكينة** حول المنتج (Revenue Expansion System) مع بوابات موافقة وأحداث أدلة.

---

## 1) القرار الاستراتيجي الأعلى

- لا توسّع عشوائي باسم «V13»؛ ابنِ **Dealix Revenue Expansion System**.
- كل ماكينة يجب أن تحتوي: **مدخل (Input) → وكيل (Agent) → أتمتة (Automation) → بوابة موافقة (Approval Gate) → حدث أدلة (Evidence Event) → KPI → نمط فشل (Failure Mode)**.  
  من دون KPI أو Evidence Event، النشاط ليس Full Ops.

---

## 2) التموضع النهائي

**English (سوق / مواد):**  
Dealix helps companies turn AI experiments and revenue operations into governed, measurable workflows — with source clarity, approval boundaries, evidence trails, and proof of value.

**Arabic:**  
Dealix تساعد الشركات على تحويل تجارب الذكاء الاصطناعي وعمليات الإيراد إلى تشغيل محكوم وقابل للقياس، عبر وضوح المصادر، حدود الموافقة، مسارات الأدلة، وإثبات القيمة.

**قل (وليس «منصة AI عامة» أو chatbot أو agency عامة أو مجرد dashboard):**  
ننشغل الإيراد والذكاء الاصطناعي بطريقة **محكومة، مثبتة، وقابلة للتوسع**.

**إطار ثقة (مرجع تشغيلي):** مواءمة الممارسات مع **NIST AI RMF** كمرجع لإدارة مخاطر AI وإدخال اعتبارات الثقة في التصميم والاستخدام والتقييم — دون استخدام الوثيقة كادّعاء امتثال قانوني كامل دون مراجعة مختصة.

التفصيل في: [`DEALIX_CATEGORY_STRATEGY_AR.md`](DEALIX_CATEGORY_STRATEGY_AR.md).

---

## 3) العرض الوحيد في الواجهة (البداية)

اعرض خدمة واحدة كمدخل واضح:

### 7-Day Governed Revenue & AI Ops Diagnostic

| العنصر | المحتوى |
|--------|---------|
| **الوعد** | أين يضيع الإيراد؛ أين CRM/البيانات غير جاهزة؛ أين AI/automation غير محكوم؛ أول 3 قرارات تشغيلية قابلة للتنفيذ **بدليل**. |
| **المخرجات** | Revenue Workflow Map · CRM/Source Quality Review · Approval Boundary Map · Evidence Trail Gaps · Top 3 Governed Decisions · Proof Pack · توصية Sprint/Retainer |
| **التسعير (مرجع)** | Starter 4,999 SAR · Standard 9,999 SAR · Executive 15,000 SAR · Enterprise 25,000 SAR · Sprint 25,000+ SAR · Retainer 4,999–35,000 SAR/شهر |

**سلم البيع:** Diagnostic → Sprint عند ظهور قيمة → Retainer عند تكرار الـworkflow (يتوافق مع Sales Kit الحالي).

---

## 4–15) الـ12 ماكينة + ماكينتان داعمتان

### 4) Market Signal Machine
- **هدف:** يومياً معرفة من يستحق التواصل ولماذا.
- **إشارات:** توظيف sales/RevOps/AI؛ وكالات بمتابعة ضعيفة؛ «AI» بلا حوكمة؛ عيادات follow-up؛ B2B founder-led؛ مستشارو CRM؛ محفظة شركات VC/accelerator؛ إلخ.
- **التدفق:** Signal → target account → ICP → pain hypothesis → زاوية مقترحة → مسودة تواصل → موافقة المؤسس → إرسال يدوي → evidence event.
- **Agent:** `MarketSignalAgent`
- **KPI (أمثلة):** 50 حساب مستهدف/أسبوع؛ 15 عالية الملاءمة؛ 10 مسودات معتمدة؛ 3 محادثات حقيقية.

### 5) Founder Media Machine
- **أفضل قناة الآن:** بناء فئة عبر المؤسس (ليست إعلانات ثقيلة مبكرة).
- **أعمدة محتوى:** AI بلا حوكمة؛ جاهزية CRM للـAI؛ تسرّب إيراد؛ حدود موافقة؛ مسارات أدلة؛ Decision Passports؛ عدم الإرسال الخارجي المستقل؛ Saudi/GCC AI Ops؛ build-in-public؛ أمثلة Proof Pack.
- **حلقة المحتوى:** اعتراض مبيعات → منشور → فيديو قصير → قسم نشرة → FAQ → بريد مبيعات → أصل شريك.
- **KPI:** 5 منشورات/أسبوع؛ نشرة/أسبوع؛ ويبينار/شهر؛ 10 طلبات proof pack/شهر؛ 3 اجتماعات مؤهلة/شهر من المحتوى.

### 6) Lead Magnet Machine
- **المغناطيسات:** Risk Score · Sample Proof Pack · Decision Passport Template · AI Approval Policy · CRM Readiness Checklist · No Autonomous External Send Policy · Revenue Workflow Maturity Score.
- **قمع مفضل:** محتوى/DM/شريك → Risk Score → Sample Proof Pack → Lead Score → حجز → نطاق Diagnostic.
- **أتمتة بعد الإرسال:** create lead → score → مرحلة → إرسال عيّنة بموافقة/موافقة صريحة → إجراء تالي → إشعار المؤسس → evidence event.

### 7) Sales Autopilot
- **الحالات:** `new_lead` … `closed_lost` (كما في المواصفة الكاملة لديك).
- **تسجيل نقاط (مثال):** +4 CEO/Founder/COO/CRO/Head Ops؛ +3 B2B؛ +3 CRM/pipeline؛ +3 يستخدم أو يخطط AI؛ +2 Saudi/GCC؛ +2 عاجل ≤30 يوم؛ +2 ميزانية 5k+؛ +2 إحالة/شريك؛ سالب للوظائف/غموض/لا ألم workflow.
- **توجيه:** 15+ Qualified A؛ 10–14 B؛ 6–9 تثقيف/شريك؛ &lt;6 أرشفة.
- **وكلاء (أسماء مرجعية):** LeadCapture، ICPScoring، Positioning، OutreachDraft، ReplyClassifier، MeetingBrief، SalesCoach، ScopeBuilder، BillingDraft، Upsell، Governance.
- **ممنوعات:** لا إرسال تلقائي خارجي؛ لا cold WhatsApp؛ لا أتمتة LinkedIn؛ لا scraping؛ لا ادّعاء إيراد قبل دفع؛ لا ضمان؛ لا إثبات مزيف — متوافق مع V12.

### 8) Demo & Proof Machine
- **مسار ديمو (12 دقيقة تقريباً):**  
  `/ar/business-now#strategy` → توضيح أنها **Founder Decision Console** → قطاع → simulate → التركيز الحالي → GTM أول 10 → Sales Script → Proof Demo → ختام بنطاق Diagnostic.
- **Proof Pack يثبت:** Source clarity · Approval boundary · Evidence trail · Decision passport · Value report · عدم بيع أي score تجريبي كحقيقة (`is_estimate` عند اللزوم).

### 9) Closing & Billing Machine
- **التدفق:** scope_requested → … → invoice_paid → delivery_started.
- **حراس:** لا `invoice_sent` بدون نطاق معتمد؛ لا `delivery_started` بدون دفع؛ لا إيراد مسجّل بدون إثبات دفع؛ لا خصم/استرداد بدون مراجعة.
- **KPI:** meeting→scope؛ scope→invoice؛ invoice→paid؛ أيام للدفع؛ أسباب الخسارة بعد النطاق.

### 10) Delivery Factory
- **بعد الدفع:** onboarding → مدخلات مطلوبة → خريطة workflows → مراجعة مصادر → فجوات موافقة → فجوات أدلة → أعلى 3 قرارات → proof pack → مكالمة تسليم → upsell مقترح.
- **هيكل Proof Pack (10 أقسام):** كما حددتَ (ملخص تنفيذي … خطة 30 يوم).
- **قواعد جودة:** كل finding له مصدر؛ كل رقم له مصدر أو `is_estimate=true`؛ المفقودات ظاهرة؛ لا ادّعاء أمني بلا مصدر؛ لا ملف نهائي بلا مراجعة.

### 11) Customer Support Autopilot
- **طبقات:** 0 FAQ ذاتي → 1 إجابة من KB معتمد → 2 مسودة + موافقة بشرية → 3 مؤسس/اختصاصي → 4 سياسة/أمن/قانون.
- **إجابة آلية مسموحة (منخفضة المخاطر):** نظرة عامة، نطاق تسعير، عملية diagnostic، جدول تسليم، شرح proof pack، مساعدة حجز، حالة فاتورة، FAQ.
- **تصعيد:** أمن/امتثال، استرداد، خصم، نطاق مخصص، تشخيص عميل، شكوى، إذن دراسة حالة، حذف/تصدير بيانات.

**السياق السعودي (خصوصية):** اجعل **معالجة البيانات، الموافقة، الشكاوى** واضحة في الواجهة والدعم. دراسات عيّنية عن مواقع تجارة إلكترونية و**PDPL** أظهرت تبايناً كبيراً في اكتمال عناصر سياسات الخصوصية — استخدم ذلك كمؤشر **سوقي** لتشديد الشفافية، مع مراجعة قانونية للنصوص النهائية.

### 12) Partner Distribution Machine
- **أفضل الشركاء:** منفّذو CRM/ERP؛ مستشارو AI؛ GRC؛ مشغّلو محافظ؛ وكالات B2B؛ COO/CRO جزئيون؛ مسرّعات.
- **نموذج:** Dealix يشخّص · الشريك ينفّذ · العميل يحصل على إثبات · الشريك يحصل على عمل تنفيذ · Dealix تحتفظ بطبقة الحوكمة/الإثبات.
- **حزم:** راجع [`docs/partners/PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md) و[`PARTNER_PROGRAM.md`](../partners/PARTNER_PROGRAM.md).
- **KPI:** مكالمات شركاء؛ leads/اجتماعات/مدفوعات عبر الشريك؛ تسليم تنفيذ؛ إيراد شريك.

### 13) Affiliate / Commission Machine
- **طبقات:** Applicant → Approved → Qualified Referral → Strategic → Implementation.
- **عمولات (مرجع):** 5% lead→diagnostic مدفوع؛ 10% intro دافئة لصاحب قرار؛ 15–20% صفقة استراتيجية؛ مخصص للتنفيذ/مشاركة إيراد.
- **لا تدفع على:** زيارات فقط؛ lead غير مؤهل؛ مكرر؛ بلا موافقة؛ خارج ICP؛ لا ألم/ميزانية؛ استرداد ضمن فترة clawback.
- **إفصاح:** واضح ومرئي مع رسالة التوصية نفسها — ممارسات مثل إرشادات **FTC** تشدد أن الإفصاح عن العلاقة المالية يكون بلا إخفاء خلف «About» أو «more».

### 14) الإعلانات والـRetargeting (لاحقاً)
ابدأ بعد: 3–5 اجتماعات؛ اعتراضان متكرران؛ طلب proof pack؛ ICP واضح. حملات: Cold Risk Score · Warm Proof Pack · Hot مراجعة Diagnostic · شريك · إعادة استهداف.

### 15) النشرة والويبينار
- **نشرة:** «GCC AI & Revenue Ops Notes» — رؤية، خطأ، إطار، قصة إثبات، CTA.
- **ويبينار شهري:** Before AI Agents: Govern Your Revenue Workflows (الأجندة كما حددتَ).

### 16) Governance & Evidence Machine (الخندق)
- **عقيدة:** Signal → Source → Approval → Action → Evidence → Decision → Value → Asset.
- **بوابات وأحداث:** راجع [`docs/governance/APPROVAL_POLICY.md`](../governance/APPROVAL_POLICY.md) و[`EVIDENCE_LEDGER.md`](../governance/EVIDENCE_LEDGER.md) وملفات `dealix/config/*.yaml`.
- **KPI حوكمة:** امتثال موافقات؛ عدم إرسال آلي عالي المخاطر؛ اكتمال أدلة؛ صيد ادّعاءات غير مدعومة؛ امتثال شركاء/مسوقين؛ دقة تصعيد الدعم.

**مرجع تقني:** وثائق وكلاء OpenAI تفصل orchestration وguardrails وintegrations/observability/evaluation — يدعم تصميم Dealix حول **orchestrator + policies + approval + evidence** بدل وكلاء منفصلين بلا حدود.

---

## 17–18) خريطة Frontend / Backend (هدف)

**عامة:** `/ar/dealix-diagnostic`، `/ar/risk-score`، `/ar/proof-pack`، … ومسارات `/ar/ops/*` للتشغيل الداخلي — كما في مواصفتك.

**وحدات Backend مقترحة تحت `dealix/`:** `growth/` · `sales/` · `support/` · `partners/` · `affiliates/` · `delivery/` · `governance/` · `evidence/` · `agents/` · `billing/` · `reports/` · `config/`

**أهم واجهات API (هدف تنفيذ تدريجي):**  
`POST /api/v1/public/risk-score` · `proof-pack-request` · `partner-apply` · `affiliate-apply` · `support`؛ ومسارات `ops/*` للوحات التشغيل؛ و`approvals` و`evidence/events`؛ إلخ — كامل القائمة في المواصفة الأصلية.

> **الواقع الحالي:** جزء كبير من القدرات موجود تحت أسماء V12 (`/api/v1/*-os`) وFull Ops وBusiness Now — الربط تدريجي وليس إعادة بناء من الصفر.

---

## 19) ملفات الإعداد (`dealix/config/`)

YAML مرجعي في المستودع: `offers.yaml` · `pricing.yaml` · `lead_scoring.yaml` · `stage_transitions.yaml` · `approval_policy.yaml` · `claim_policy.yaml` · `affiliate_rules.yaml` · `partner_rules.yaml` · `support_intents.yaml` · `agent_permissions.yaml` · `no_build_rules.yaml`

---

## 20–22) الاختبارات وخطة الطريق والأهداف

- **اختبارات أساسية (أسماء مرجعية):** `test_lead_scoring.py` · `test_stage_transitions.py` · `test_approval_policy.py` · `test_claim_guard.py` · `test_evidence_events.py` · `test_invoice_guard.py` · `test_support_classifier.py` · `test_knowledge_base.py` · `test_affiliate_commissions.py` · `test_affiliate_compliance.py` · `test_partner_referrals.py` · `test_agent_orchestrator.py` · `test_no_build_warning.py` · `test_proof_pack_generator.py`
- **اختبارات قبول:** High-fit → Qualified A + مهمة موافقة؛ Security claim بدون مصدر → محظور؛ Invoice بدون نطاق معتمد → محظور؛ إلخ.

**Roadmap:**  
- **14 يوم — V1:** صفحات عامة، risk score، التقاط lead، تسجيل، Command Center، Approvals، Evidence، Pipeline، KB دعم v1، طلب شريك/مسوق.  
- **30 يوم — V2:** Marketing dashboard، تسلسل نشرة، محرك webinar، تتبع affiliate، احتساب عمولة، مصنف دعم، مولدات مسودات، حراسة فاتورة، هيكل Proof Pack.  
- **90 يوم — V3:** بوابات شريك/مسوق، Customer workspace أولي، orchestrator، Governance health، Proof Pack generator، أتمتة تسليم، أحداث إعادة استهداف، SEO.

**أهداف 30/90 يوم:** كما حددتَ (حسابات مستهدفة، محادثات، proof packs، مدفوعات، شركاء، webinars، إلخ).

---

## 23–25) التشغيل اليومي والقرار النهائي

- **يومي ~90 دقيقة:** موافقات عالية المخاطر؛ متابعة مبيعات؛ شركاء/مسوقين؛ تصعيدات دعم؛ محتوى/قصة إثبات.
- **أسبوعي:** pipeline · marketing · partners · support · governance · قرار no-build.
- **شهري:** Board Pack ([`docs/company/BOARD_PACK.md`](../company/BOARD_PACK.md)) · سرد تنفيذي · تسعير · مدفوعات شركاء · مكتبة proof packs · فرص retainer · إشارات منصة.

**القرار:** لا تبنِ من أجل البناء؛ ابنِ **نظاماً يجعل المنتج يبيع ويخدم ويسلّم** مع أدلة وحوكمة.

---

## وثائق تفصيلية مرتبطة

| الموضوع | الملف |
|---------|--------|
| التموضع والفئة | [`DEALIX_CATEGORY_STRATEGY_AR.md`](DEALIX_CATEGORY_STRATEGY_AR.md) |
| مبيعات | [`../sales/SALES_AUTOPILOT.md`](../sales/SALES_AUTOPILOT.md) |
| دعم | [`../support/SUPPORT_AUTOPILOT.md`](../support/SUPPORT_AUTOPILOT.md) |
| تسويق | [`../marketing/MARKETING_FACTORY.md`](../marketing/MARKETING_FACTORY.md) |
| مسوقون بالعمولة | [`../affiliates/AFFILIATE_PROGRAM.md`](../affiliates/AFFILIATE_PROGRAM.md) |
| شركاء | [`../partners/PARTNER_PROGRAM.md`](../partners/PARTNER_PROGRAM.md) |
| موافقات | [`../governance/APPROVAL_POLICY.md`](../governance/APPROVAL_POLICY.md) |
| أدلة | [`../governance/EVIDENCE_LEDGER.md`](../governance/EVIDENCE_LEDGER.md) |
| Proof Pack | [`../delivery/PROOF_PACK_TEMPLATE.md`](../delivery/PROOF_PACK_TEMPLATE.md) |
| هندسة | [`../engineering/FULL_OPS_ARCHITECTURE.md`](../engineering/FULL_OPS_ARCHITECTURE.md) · [`AGENT_ORCHESTRATOR.md`](../engineering/AGENT_ORCHESTRATOR.md) · [`TEST_PLAN.md`](../engineering/TEST_PLAN.md) |
