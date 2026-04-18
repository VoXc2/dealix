# Dealix — سجل نقاط الإثبات والأدلة (Proof Points Registry)

> **الغرض:** مرجع الأدلة الجاهزة — ما يمكن إثباته اليوم، وما ينتظر بيانات Pilot  
> **المستخدمون:** فريق المبيعات، التسويق، Solutions Engineering  
> **آخر تحديث:** مايو 2026  
> **المالك:** sami.assiri11@gmail.com  
> **المرجع:** [CLAIMS_REGISTRY_AR.md](./CLAIMS_REGISTRY_AR.md) · [MARKETING_OS_AR.md](./MARKETING_OS_AR.md)

---

## 1. ما يمكن إثباته اليوم

| الادعاء | الدليل المتاح | طريقة العرض |
|---------|--------------|-------------|
| النظام مبني وشغّال (MVP) | repository live في GitHub + landing page | عرض مباشر للنظام |
| عربي أولاً — RTL حقيقي | landing page ar_SA + واجهة النظام | لقطة شاشة / عرض حي |
| WhatsApp Business API يعمل | اختبار ناجح (TRUTH.yaml INFRA-001) | إرسال رسالة تجريبية حية |
| مسار اعتماد موثّق يعمل تقنياً | workflow engine في الـ backend | demo مُسيطر عليه |
| بنية PDPL مُدمجة في التصميم | COMP-002 في TRUTH.yaml | وثيقة التصميم + code review |
| مُصمَّم لمتطلبات SAMA/SDAIA/NCA | SYSTEM_DESIGN_AR.md §8 | وثيقة compliance |
| فريق مؤسس تقني له خبرة سوق | سيرة ذاتية / LinkedIn | ورقة تعريفية |

---

## 2. ما ينتظر بيانات Pilot (PENDING PILOT DATA)

> هذه الادعاءات **ممنوع استخدامها خارجياً** حتى تُجمع البيانات.

| الادعاء | البيانات المطلوبة | target_date |
|---------|-----------------|-------------|
| نسبة تقليص وقت الموافقات | قياس قبل/بعد في بيئة Pilot حقيقية | Q3 2026 |
| معدل رفع إغلاق الصفقات | win rate مقارن 90 يوم | Q3 2026 |
| توفير ساعات العمل الأسبوعية | مقارنة موقوتة للتقارير اليدوية vs آلية | Q3 2026 |
| قيمة الهامش المحفوظ من الخصومات | حساب الخصومات غير المصرح بها قبل/بعد | Q3 2026 |
| نسبة خطأ AI <5% | telemetry 30 يوم على الـ Pilot | Q2 2026 |
| معدل استجابة WhatsApp >30% | telemetry 30 يوم | Q2 2026 |

---

## 3. قوالب دراسات الحالة (Case Study Templates)

### قالب دراسة حالة — ICP-1 (SaaS)

```
العميل: [PENDING PILOT DATA]
القطاع: B2B SaaS
حجم الشركة: [X] موظف — MRR [Y] ر.س
التحدي: خصومات بلا توثيق + تجديدات مفوّتة
الحل المطبّق: Revenue OS + Pricing Control
النتائج:
  - وقت الموافقة على الخصم: من [X أيام] إلى [Y ساعات]  [PENDING PILOT DATA]
  - عقود تجديد مُنبَّه لها: [X]%  [PENDING PILOT DATA]
  - هامش محفوظ: [Y] ر.س/شهر  [PENDING PILOT DATA]
اقتباس العميل: [PENDING PILOT DATA]
```

### قالب دراسة حالة — ICP-2 (Enterprise)

```
العميل: [PENDING PILOT DATA]
القطاع: Large Enterprise (متعدد الفرق)
حجم الشركة: [X]+ موظف
التحدي: فوضى الاعتمادات + تقارير يدوية متأخرة
الحل المطبّق: Executive Control Room + Approval OS
النتائج:
  - وقت إعداد التقرير الأسبوعي: من [X أيام] إلى تلقائي  [PENDING PILOT DATA]
  - قرارات معلقة ظهرت: [X]% من إجمالي القرارات  [PENDING PILOT DATA]
  - رضا القيادة التنفيذية: [PENDING PILOT DATA]
اقتباس العميل: [PENDING PILOT DATA]
```

### قالب دراسة حالة — ICP-3 (Regulated Sector)

```
العميل: [PENDING PILOT DATA]
القطاع: بنوك / تأمين / حكومة
الجهة الرقابية: [SAMA / NCA / SDAIA]
التحدي: audit trail غير كامل + امتثال PDPL معقد
الحل المطبّق: Trust & Evidence Layer + GCC Readiness
النتائج:
  - وقت إعداد تقرير audit: من [X أيام] إلى [Y دقائق]  [PENDING PILOT DATA]
  - نسبة التوافق مع PDPL: موثّقة رسمياً  [PENDING PILOT DATA]
  - ملاحظات المراجع الخارجي: [PENDING PILOT DATA]
اقتباس العميل: [PENDING PILOT DATA]
```

---

## 4. تدفقات العرض الآمنة (Demo Flows — APPROVED)

> هذه التدفقات **آمنة للاستخدام** في العروض الحية — مبنية على ما يعمل فعلاً.

### Demo-1: مسار الخصم والاعتماد (آمن)

```
✅ ابدأ من: لوحة Revenue OS
✅ أظهر: صفقة معلقة تحتاج خصماً
✅ انقر: "طلب خصم" → يظهر workflow الاعتماد
✅ أظهر: إشعار للمعتمد (simulation)
✅ أظهر: سجل audit trail مكتمل بعد الموافقة
✅ الرسالة: "من طلب الخصم حتى الموافقة — كل خطوة موثّقة"
⚠️ تجنّب: أرقام ROI فعلية حتى تتوفر بيانات Pilot
⚠️ تجنّب: ادعاء أن النظام في production مع عملاء حقيقيين
```

### Demo-2: مسار الشراكة (آمن)

```
✅ ابدأ من: Partnership OS
✅ أظهر: شريك محتمل في قاعدة البيانات
✅ انقر: scorecard الشريك — المعايير والدرجة
✅ أظهر: مراحل onboarding التلقائي
✅ أظهر: تقرير أداء الشريك
✅ الرسالة: "كل شريك من الاكتشاف حتى التقييم في نظام واحد"
⚠️ تجنّب: أسماء شركاء حقيقيين
```

### Demo-3: لوحة التنفيذ (آمن)

```
✅ ابدأ من: Executive Control Room
✅ أظهر: ملخص أسبوعي — الإيراد والقرارات المعلقة
✅ أظهر: filter: "قرارات تأخرت أكثر من 48 ساعة"
✅ أظهر: تقرير PDF بضغطة واحدة
✅ الرسالة: "القيادة تعرف كل شيء — بدون اجتماع طارئ"
⚠️ تجنّب: أرقام مالية حقيقية
```

### Demo-4: طبقة Trust (آمن)

```
✅ ابدأ من: Trust & Evidence Layer
✅ أظهر: PDPL consent log
✅ أظهر: audit trail بـ hash
✅ أظهر: تصدير تقرير كامل (PDF)
✅ الرسالة: "SAMA أو NCA تسأل — تصدّر التقرير في دقيقة واحدة"
⚠️ تجنّب: ادعاء "SOC 2" أو "ISO 27001" أو "HIPAA"
```

---

## 5. تدفقات العرض قيد البناء (Under Construction)

> **ممنوع استخدامها في عروض حقيقية** حتى يُصنَّف الـ status "approved demo".

| التدفق | السبب | المتوقع |
|--------|-------|---------|
| Voice AI Demo (وكيل صوتي) | Retell مؤجّل | Q3 2026 |
| M&A Track Demo | مرحلة ثانية | 2027 |
| Real-time Lead Discovery من السجل السعودي | في التطوير | Q2 2026 |
| Integration Salesforce / HubSpot مباشر | قيد التقييم | Q2 2026 |

---

## 6. سجل الموافقة على لقطات الشاشة (Screenshot Approval Registry)

| id | الوصف | الحالة | تاريخ الموافقة | الملاحظات |
|----|-------|--------|----------------|-----------|
| SCR-001 | لقطة لوحة Revenue OS | ✅ معتمدة | 2026-05 | بيانات تجريبية — أزل أي اسم حقيقي |
| SCR-002 | workflow الاعتماد على الخصم | ✅ معتمدة | 2026-05 | تجنّب أرقام مالية حقيقية |
| SCR-003 | export تقرير audit PDF | ✅ معتمدة | 2026-05 | يجب أن يكون بيانات demo واضحة |
| SCR-004 | Partnership scorecard | 🟡 بانتظار مراجعة | — | — |
| SCR-005 | Voice Agent interface | 🔴 محظورة | — | ميزة غير متاحة بعد |

---

## 7. مخزون الأدلة (Evidence Inventory)

### ما لدينا اليوم

| نوع الدليل | الحالة | المرجع |
|-----------|--------|--------|
| Landing page حية | ✅ موجودة | landing/index.html |
| Repository code مفتوح للمراجعة | ✅ موجود | github.com/VoXc2/dealix |
| WhatsApp Business API اختبار ناجح | ✅ موجود | TRUTH.yaml INFRA-001 |
| وثيقة تصميم compliance (PDPL/SAMA) | ✅ موجودة | SYSTEM_DESIGN_AR.md §8 |
| سيرة تقنية للفريق | 🟡 بالإعداد | — |

### ما نحتاجه من الـ Pilot

| نوع الدليل | الأولوية | المسؤول |
|-----------|----------|---------|
| شهادة عميل Pilot (quote) | عالية جداً | Customer Success |
| قياس وقت الموافقة قبل/بعد | عالية | Pilot team |
| حساب الهامش المحفوظ | عالية | Finance + Pilot team |
| Net Promoter Score (NPS) Pilot | متوسطة | Customer Success |
| case study مكتوبة (أول عميل) | عالية | Marketing |

---

*المرجع: [CLAIMS_REGISTRY_AR.md](./CLAIMS_REGISTRY_AR.md) · [DEMO_NARRATIVES_AR.md](./DEMO_NARRATIVES_AR.md)*  
*آخر مراجعة: مايو 2026*
