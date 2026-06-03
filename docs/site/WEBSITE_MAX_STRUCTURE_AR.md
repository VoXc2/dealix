# Website Max Structure — بنية الموقع النهائية (Arabic-first)

مواصفة الموقع التسويقي لـDealix: الخريطة، تشريح صفحة النظام، وربط القطاعات بالأنظمة.
(هذه مواصفة تنفيذية للواجهة في `src/`؛ المخرج الحالي هو هذه الوثيقة + صفحة الهبوط القائمة `src/pages/LandingPage.tsx`.)

---

## 1. خريطة الموقع

```
/ar
/ar/systems
/ar/systems/revenue-operating-system
/ar/systems/executive-command-os
/ar/systems/follow-up-recovery-os
/ar/systems/whatsapp-client-os
/ar/systems/proposal-proof-os
/ar/pricing
/ar/diagnostic
/ar/start
/ar/contact
/ar/resources
/ar/partners
/ar/use-cases/marketing-agencies
/ar/use-cases/training-companies
/ar/use-cases/clinics
/ar/use-cases/real-estate
/ar/use-cases/professional-services
```

---

## 2. تشريح صفحة النظام

كل صفحة نظام تحتوي:

```
Hero · Pain · Who it is for · When you need it · What you get
First Sprint · Delivery Pack · Required Inputs · Acceptance Criteria
Starter Price · FAQ · CTA
```

البيانات تأتي من نفس مصدر الأنظمة (`scripts/dealix_account_lib.py:SYSTEMS`) لضمان اتساق السعر والمخرجات بين الموقع والـPacks.

---

## 3. صفحات Use Case → النظام الأساسي

| الصفحة | النظام الأساسي |
|--------|----------------|
| Marketing Agencies | Revenue OS / Follow-up Recovery |
| Training Companies | Follow-up Recovery / WhatsApp Client |
| Clinics | WhatsApp Client / Follow-up Recovery |
| Real Estate | Follow-up Recovery / WhatsApp Client |
| Professional Services | Proposal & Proof / Executive Command |

---

## 4. قواعد النسخ على الموقع

- **بلا ادعاءات مضمونة** (نفس قائمة `GUARANTEED_CLAIM_TOKENS`).
- لغة واعية بالدليل، تركيز على Sprint افتتاحي ومخرج ملموس.
- CTA واضح لكل صفحة: «ابدأ Sprint» أو «اطلب Mini Proposal».
- خصوصية ظاهرة: رابط سياسة البيانات (يتسق مع `docs/privacy/`).

---

## 5. التقاط العملاء (Website Leads)

- نموذج `/ar/start` و`/ar/diagnostic` ينشئ Lead يدخل نفس خط الأنابيب.
- لا إرسال تلقائي؛ الـLead يصبح Account Pack بمستوى دليل L4 (بيانات مزوّدة) وثقة تواصل C4 عند تأكيد العميل.

> الحالة: المواصفة جاهزة. تنفيذ المسارات الكاملة في React مُدرَج كبند تالٍ في `reports/gtm/MAXIMUM_REVENUE_FACTORY_COMPLETION_FINAL_REPORT.md`.

---

*Version 1.0*
