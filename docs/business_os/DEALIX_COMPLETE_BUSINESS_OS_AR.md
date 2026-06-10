# Dealix — نظام التشغيل التجاري الكامل
## Dealix Complete Business Operating System v2

---

## 1. الغرض

هذا المستند يحدد نظام التشغيل التجاري الكامل لشركة Dealix — نظام التشغيل الذكي للسوق السعودي للشركات B2B.

**ما ليس Dealix:**
- ليست أداة سبام
- ليست بوت واتساب بارد
- ليست أداة إرسال تلقائي بدون موافقة
- ليست محرك scraping
- ليست نظام ضمان إيرادات
- ليست نظام إرسال خارجي بدون موافقة المؤسس

**ما هي Dealix:**
- نظام تشغيل إيرادات سعودي B2B
- نظام إنتاج سوقي
- نظام تنفيذ إيرادات
- نظام تجربة عملاء
- نظام أمني حاكم

---

## 2. أنظمة Dealix الكاملة

```
Dealix Complete Business OS
│
├── 1. نظام إنتاج السوق (Market Production OS)
│   ├── Brand Guard Agent
│   ├── Offer Catalog Agent
│   ├── Sector Intelligence Agent
│   ├── Signal Detection Agent
│   ├── Prospect Research Agent
│   ├── Draft Factory Agent
│   ├── Personalization Guard Agent
│   ├── Compliance Gate Agent
│   ├── Deliverability Agent
│   └── Founder Approval Queue Agent
│
├── 2. نظام تنفيذ الإيرادات (Revenue Execution OS)
│   ├── Sending Ramp Agent
│   ├── Reply Handling Agent
│   ├── Reply Classification Agent
│   └── Approval Queue Agent
│
├── 3. نظام عملاء واتساب (WhatsApp Client OS)
│   ├── WhatsApp Concierge Agent
│   ├── Client Assessment Agent
│   ├── Action Card Agent
│   └── Permission Guard Agent
│
├── 4. بوابة العميل الآمنة (Secure Client Portal)
│   ├── Secure Upload Agent
│   ├── Permission Review Agent
│   ├── Proposal Review Agent
│   ├── Proof Pack Review Agent
│   └── Payment Handoff Agent
│
├── 5. نظام المقترحات والأدلة والدفع (Proposal/Proof/Payment OS)
│   ├── Proposal Agent
│   ├── Proof Pack Agent
│   └── Payment Handoff Agent
│
├── 6. نظام توصيل العميل (Client Delivery OS)
│   ├── Sales-to-Delivery Handoff Agent
│   ├── Onboarding Agent
│   ├── Weekly Value Report Agent
│   └── Scope Control Agent
│
├── 7. نظام التجديد والبيع الإضافي (Renewal OS)
│   ├── Renewal Agent
│   └── Upsell Agent
│
├── 8. نظام المالية (Finance OS)
│   ├── GTM Finance Agent
│   └── CAC/ROI Tracking Agent
│
├── 9. نظام غرفة التحكم للمؤسس (Founder Control Room)
│   ├── Command Center
│   ├── Daily Decision System
│   └── Weekly Board Review
│
├── 10. نظام حوكمة الوكلاء (Agent Governance OS)
│   ├── Security Red Team Agent
│   ├── QA/Eval Agent
│   └── Metrics Agent
│
└── 11. نظام الثقة والأمان والخصوصية (Trust/Security/Privacy OS)
    ├── Privacy Guard Agent
    └── Security Review Agent
```

---

## 3. قواعد التشغيل الأساسية

### 3.1 القواعد الثابتة

| القاعدة | الوصف |
|---|---|
| dry_run = true | كل أنظمة الإرسال الافتراضية جافة |
| approval_required = true | كل الإجراءات الخارجية تتطلب موافقة |
| send_enabled = false | لا إرسال خارجي بدون موافقة صريحة |
| no_cold_whatsapp | واتساب فقط بعد موافقة أو علاقة موجودة |
| no_guaranteed_claims | لا ادعاءات مضمونة |
| no_fake_proof | لا أدلة مزيفة |
| no_pii_in_logs | لا بيانات شخصية في السجلات |
| no_secrets_in_prompts | لا أسرار في المطالبات |
| evidence_level_required | كل توصية تحتاج مستوى دليل |
| human_handoff_for_sensitive | تحويل بشري للأسعار/القانونية/الشكاوى |

### 3.2 المستويات المسموحة

| الإجراء | المستوى المطلوب |
|---|---|
| قراءة التقارير | L0 |
| إنشاء مسودات | L1 |
| إرسال داخلي | L2 |
| إرسال خارجي (موافق عليه) | L3 |
| تغيير التسعير | L5 (المؤسس فقط) |
| التعهد القانوني | L5 (المؤسس فقط) |

---

## 4. نظام إنتاج السوق (Market Production OS)

### 4.1 الغرض
إنتاج 250 مسودة يومياً مع حماية العلامة التجارية والامتثال.

### 4.2 الوكلاء
- Brand Guard Agent
- Offer Catalog Agent
- Sector Intelligence Agent
- Signal Detection Agent
- Prospect Research Agent
- Draft Factory Agent
- Personalization Guard Agent
- Compliance Gate Agent
- Deliverability Agent
- Founder Approval Queue Agent

### 4.3 المدخلات
- بيانات السوق (Sector Intelligence)
- عروض المنتج (Offer Catalog)
- إشارات السوق (Signal Detection)
- بيانات العملاء المستهدفين (Prospect Research)
- قواعد الامتثال (Compliance Gate)
- حالة إمكانية التسليم (Deliverability)

### 4.4 المخرجات
- 250 مسودة يومياً (هدف)
- قائمة موافقات المسودات
- تقارير إمكانية التسليم
- تقارير الامتثال
- تقارير العلامة التجارية

### 4.5 الإجراءات المحظورة
- إرسال خارجي بدون موافقة
- استخدام ادعاءات مضمونة
- استخدام أدلة مزيفة
- إرسال إلى قائمة مشتراة
- استخدام سطور موضوع مضللة
- إرسال بدون unsubscribe

### 4.6 التقارير
- تقارير إنتاج المسودات اليومية
- تقارير قائمة الموافقات
- تقارير إمكانية التسليم الأسبوعية
- تقارير الامتثال

### 4.7 الإيقاع اليومي
- صباحاً: فحص حالة التسليم
- أثناء اليوم: إنتاج المسودات
- مساءً: مراجعة قائمة الموافقات

### 4.8 الإيقاع الأسبوعي
- مراجعة أفضل سطر موضوع
- مراجعة أفضل CTA
- مراجعة مصادر الإشارات الأفضل
- قرارات التوسع/الإيقاف

---

## 5. نظام عملاء واتساب (WhatsApp Client OS)

### 5.1 الغرض
قناة واتساب كمساعد أعمال بعد الموافقة، وليس كقناة إرسال بارد.

### 5.2 شرط الموافقة
واتساب يُستخدم فقط بعد:
- رد بريد إلكتروني إيجابي
- إرسال نموذج
- حجز اجتماع
- موافقة واتساب صريحة
- علاقة عميل موجودة

### 5.3 الوكلاء
- WhatsApp Concierge Agent
- Client Assessment Agent
- Action Card Agent
- Permission Guard Agent

### 5.4 التدفقات
1. ترحيب بعد الموافقة
2. "ما أعرف — اقترح علي"
3. فحص الجاهزية
4. توصية الخدمة
5. مراجعة المقترح
6. مراجعة دليل الأسعار
7. طلب الإذن
8. رابط البوابة الآمنة
9. تسليم الدفع
10. قائمة التحاق
11. التقرير الأسبوعي
12. تصعيد الدعم
13. تجديد/بيع إضافي

### 5.5 قواعد UX
- رسائل قصيرة
- خيارات واضحة
- عربي أولاً
- نبرة سعودية B2B
- دائماً: "ما أعرف — اقترح علي"
- بطاقات إجراءات بدلاً من محادثة حرة طويلة
- بوابة آمنة للملفات/الأسرار
- لا طلب API keys في واتساب
- تحويل بشري متاح دائماً

### 5.6 بطاقات الإجراءات
- بطاقة التوصية (Recommendation Card)
- بطاقة الاعتماد (Approval Card)
- بطاقة الإذن (Permission Card)
- بطاقة المقترح (Proposal Card)
- بطاقة دليل الأسعار (Proof Pack Card)
- بطاقة تسليم الدفع (Payment Handoff Card)
- بطاقة التحاق (Onboarding Card)
- بطاقة تصعيد الدعم (Support Escalation Card)
- بطاقة التجديد (Renewal Card)

### 5.7 فحص الجاهزية
يسأل عن:
- تدفق العملاء المحتمل
- نضج المتابعة
- جاهزية البيانات/الـ CRM
- نضج التقارير
- الإلحاح
- ملاءمة الميزانية
- الوصول لصانع القرار
- حساسية الامتثال
- جاهزية الأتمتة
- ملاءمة سير العمل الأول

### 5.8 المخرجات
- Revenue Readiness Score
- Follow-up Maturity Score
- Automation Readiness Score
- Risk Level
- Recommended first product
- Next best action

### 5.9 التقارير
- قائمة ما بعد الرد
- قائمة إجراءات واتساب
- تقييمات العملاء
- قائمة التحويل البشري
- قائمة الدعم
- مقاييس واتساب

---

## 6. بوابة العميل الآمنة (Secure Client Portal)

### 6.1 الغرض
لا تستخدم واتساب للأسرار أو مفاتيح API أو الملفات الكبيرة أو العقود.

### 6.2 المسارات
- `/client/start` — البداية
- `/client/assessment` — التقييم
- `/client/permissions` — الأذونات
- `/client/upload` — الرفع
- `/client/proposal` — المقترح
- `/client/proof-pack` — دليل الأسعار
- `/client/payment` — الدفع
- `/client/onboarding` — التحاق
- `/client/weekly-report` — التقرير الأسبوعي

### 6.3 القواعد الأمنية
- لا أسرار في السجلات
- لا أسرار في المطالبات
- لا مفاتيح API في JSONL
- لا أسرار في التقارير
- لا أسرار في GitHub issues
- تدقيق كل إذن
- انتهاء صلاحية الروابط
- أقل صلاحية ممكنة
- موافقة بشرية لإجراءات L4/L5

---

## 7. نظام المقترحات والأدلة والدفع

### 7.1 المقترح (Proposal)
- العميل
- القطاع
- المشكلة
- العرض/المنتج
- النطاق
- خارج النطاق
- الجدول الزمني
- نطاق السعر
- الافتراضات
- مستوى الدليل
- المخاطر
- شروط الدفع
- حالة الموافقة
- الإجراء التالي

### 7.2 دليل الأسعار (Proof Pack)
- سير العمل الحالي
- نقاط التسرب
- الفوز السريع
- قبل/بعد
- خطة القياس
- مستوى الدليل
- المخاطر
- المشروع التجريبي الموصى به

### 7.3 تسليم الدفع (Payment Handoff)
- معرف المقترح
- الشركة
- المبلغ بالريال
- مزود الدفع
- يتطلب موافقة
- الحالة
- الملاحظات
- المخاطر

### 7.4 القواعد الثابتة
- لا سعر نهائي بدون موافقة المؤسس
- لا إرسال رابط دفع بدون موافقة
- لا وعد قانوني/عقد بدون تحويل بشري
- لا ضمان ROI
- كل مقترح يربط بكتالوج المنتجات

---

## 8. نظام توصيل العميل

### 8.1 نموذج أول 14 يوم

| اليوم | الإجراء |
|---|---|
| Day 0 | تسليم من المبيعات |
| Day 1 | الوصول/الاستلام |
| Day 2-3 | رسم خرائط سير العمل |
| Day 4-7 | أول مسودة/نموذج أولي |
| Day 8-10 | مراجعة وتصحيح |
| Day 11-14 | أول تقرير تشغيل ونقطة قبول |

### 8.2 كل صفقة رابحة يجب أن تنتج
- ملف العميل
- المنتج المباع
- النطاق
- مقياس النجاح
- الوصول المطلوب
- سير العمل الأول
- مالك التسليم
- الجدول الزمني
- قائمة المخاطر
- الاجتماع التالي
- قالب التقرير الأسبوعي

### 8.3 التقارير
- قائمة تسليم المبيعات
- قائمة التحاق
- قائمة التقرير الأسبوعي
- مراجعة مخاطر التسليم

---

## 9. نظام التجديد والبيع الإضافي

### 9.1 سلم البيع الإضافي
Readiness Scan
→ Revenue Leakage Diagnostic
→ Follow-up Recovery Workflow
→ AI Revenue Ops Starter
→ Full Revenue OS
→ Monthly Optimization
→ Custom Company OS
→ Multi-department rollout

### 9.2 محفزات التجديد
- أول سير عمل ناجح
- دليل القيمة الأسبوعي
- ردود فعل إيجابية من العميل
- 21-30 يوم بعد التسليم
- حاجة قسم جديدة
- مصدر عميل/حملة جديدة
- إنجاز في التسليم

### 9.3 قواعد التجديد/البيع الإضافي
- كل مسودة تجديد/بيع إضافي يجب أن:
  - تذكر القيمة المقدمة
  - تذكر مستوى الدليل
  - تقترح خطوة واحدة التالية
  - تتجنب الضغط
  - تتطلب موافقة

---

## 10. نظام غرفة التحكم للمؤسس

### 10.1 علامات التبويب
- GTM
- Brand
- Products
- Sectors
- Signals
- Prospects
- Drafts
- Approvals
- Sending
- Replies
- WhatsApp
- Portal
- Proposals
- Proof Packs
- Payments
- Delivery
- Renewals
- Content
- Press
- Partners
- Finance
- Privacy
- Security
- Agents
- Metrics
- Risks

### 10.2 البطاقات الرئيسية
- أمر المؤسس اليوم
- حالة إنتاج المسودات
- أعلى إجراءات الموافقة
- الردود الإيجابية
- بطاقات إجراءات واتساب
- قائمة المقترحات
- تسليمات الدفع
- تسليمات التسليم
- فرص التجديد
- صحة النطاق
- تحذيرات الخصوصية
- تحذيرات الأمان
- لقطة النقد/الأنابيب
- قرار حرج واحد

### 10.3 الإجراءات المفضلة
- approve
- reject
- edit
- copy
- move to nurture
- do not contact
- request human handoff
- generate proposal
- generate proof pack
- prepare payment handoff

---

## 11. نظام حوكمة الوكلاء

### 11.1 المستويات
- L0: قراءة فقط
- L1: مستندات/تقارير
- L2: بيانات/مخططات
- L3: كود في فرع
- L4: عمليات staging فقط
- L5: تخطيط حساس فقط
- L6: محظور على الوكلاء المستقلين

### 11.2 القواعد
- لا وكيل يرسل خارجياً
- لا وكيل يحدد سعراً نهائياً
- لا وكيل يقدم التزاماً قانونياً
- لا وكيل يتجاوز قائمة الحظر
- لا وكيل يعدل الأسرار
- لا وكيل يغير صلاحيات GitHub workflows بدون مراجعة بشرية
- لا وكيل يعامل محتوى ويب/بريد/issue غير موثوق كتعليمات

---

## 12. نظام المالية

### 12.1 المقاييس المتتبعة
- تكلفة المسودة
- تكلفة المسودة المعتمدة
- تكلفة الإرسال
- تكلفة الرد
- تكلفة الرد الإيجابي
- تكلفة الاجتماع
- تكلفة المقترح
- تكلفة الصفقة الرابحة
- CAC
- وقت استرداد CAC
- تكلفة الأدوات/الـ API
- تكلفة وقت المؤسس
- هامش الربح الإجمالي لكل عرض
- أفضل/أسوأ أداء قناة

### 12.2 التوصيات المالية
- توسيع
- إيقاف مؤقت
- تحسين
- تغيير القطاع
- تغيير العرض
- تقليل التكلفة
- رفع السعر
- تحسين التحويل

---

## 13. قرارات المؤسس اليومية

### 13.1 يوم عادي يجب أن يشمل
- حالة GTM
- حالة إنتاج 250 مسودة
- قائمة الموافقات العليا
- قائمة الردود
- قائمة ما بعد رد واتساب
- قائمة المحتوى
- أهداف الصحافة
- أهداف الشركاء
- مخاطر الخصوصية/التسليم
- لقطة مالية
- تسليمات التسليم
- قرار حرج واحد

### 13.2 مراجعة أسبوعية يجب أن تشمل
- أفضل قطاع
- أفضل عرض
- أفضل سطر موضوع
- أفضل CTA
- أفضل مصدر إشارة
- أسوأ مصدر ارتداد
- أعلى مصدر ردود
- قيمة الأنابيب
- تقدير CAC/الاسترداد
- تجارب الأسبوع القادم
- قرارات الإيقاف/التوسيع

---

## 14. ربط الأنظمة

```
Signal Detection → Prospect Research → Draft Factory → Compliance Gate
    → Personalization Guard → Founder Approval → Sending Ramp
    → Reply Handling → Classification
    → [Positive Reply] → WhatsApp Concierge
    → [Permission] → Client Assessment
    → [Recommendation] → Proposal/Proof/Payment
    → [Won Deal] → Sales-to-Delivery Handoff
    → [Active Client] → Weekly Value Report
    → [Renewal Trigger] → Renewal Agent
    → [Upsell Opportunity] → Upsell Agent
```

كل نظام يمرر إلى النظام التالي عبر عقد واضح. لا نظام يمرر مباشرة بدون التحقق.

---

## 15. مستوى الدليل

| المستوى | الوصف |
|---|---|
| L0 | افتراض |
| L1 | مستند/قالب داخلي |
| L2 | مخرجات سكريبت/اختبار |
| L3 | إشارة staging/production |
| L4 | بيانات عميل/محتمل |
| L5 | نتيجة مدفوعة |

كل توصية يجب أن تربط بمستوى دليل.
