# Website Architecture — معمارية الموقع (آلة تحويل)

> الموقع ليس بروشور، بل **آلة تحويل**: من زائر → تشخيص → نظام مناسب → بدء. هذا المستند يحدد البنية والمحتوى، ويُغذّي صفحات `src/pages` لاحقًا.

---

## 1. خريطة الموقع (Site Architecture)

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

## 2. هيكل صفحة كل نظام

```
Hero · Pain · Who it is for · When you need it · What you get
· First Sprint · Delivery Pack · Required Inputs · Acceptance Criteria
· Starter Price · FAQ · CTA
```

التفاصيل الكاملة للأنظمة الخمسة في `docs/site/FIVE_SYSTEMS_CATALOG_AR.md`.

---

## 3. صفحات حالات الاستخدام (Use Cases — مهمة للـ SEO والإقناع)

| الصفحة | يربط بـ |
|--------|---------|
| Dealix for Marketing Agencies | Revenue OS / Follow-up Recovery |
| Dealix for Training Companies | Follow-up Recovery / WhatsApp Client |
| Dealix for Clinics | WhatsApp Client / Follow-up Recovery |
| Dealix for Real Estate Teams | Follow-up Recovery / Revenue OS |
| Dealix for Professional Services | Proposal & Proof / Executive Command |

كل صفحة تربط **القطاع** بالنظام الأنسب، مع مثال ألم ومخرج Sprint.

---

## 4. المحتوى (Content Engine — أسبوعيًا)

```
5 منشورات عن مشاكل الأنظمة الخمسة
2 founder insights
1 workflow sample
1 objection answer
1 mini case-style example
```

أمثلة عناوين:
```
لماذا تضيع الفرص قبل العرض؟
التقرير لا يساوي قرارًا
آخر متابعة لم تحدث قد تكون أغلى فرصة
واتساب ليس Inbox؛ هو workflow
العرض المقنع يحتاج Proof لا كلامًا أكثر
```

> كل نسخة موقع/محتوى تلتزم بـ `docs/proposals/PROPOSAL_COPY_LIBRARY_AR.md`: لا ادعاءات مضمونة، لا 10x.

---

## 5. الشركاء (Partners — قنوات توزيع)

| الشريك | أفضل نظام |
|--------|-----------|
| Marketing agency | Revenue OS / Follow-up Recovery |
| CRM implementer | Executive Command / Revenue OS |
| Training company | Follow-up Recovery / WhatsApp Client |
| Consultant | Executive Command / Proposal & Proof |
| Web agency | Proposal & Proof / Revenue OS |
| HR / recruitment firm | Follow-up Recovery / Executive Command |

عرض الشريك: «أنت تملك العلاقة، Dealix يشغّل النظام، ونقتسم القيمة عبر referral fee أو implementation margin».

---

## 6. حالة التنفيذ الحالية

الواجهة الحالية (`src/pages`) لوحة تشغيل داخلية (Dashboard, Finance, Governance, Prospects, LandingPage). هذا المستند هو **مواصفة المحتوى والمسارات** للموقع العام `/ar/*`؛ تنفيذ صفحات React يتم في دفعة لاحقة اعتمادًا على هذه المواصفة وكتالوج الأنظمة.

---

*Website Architecture | الإصدار 1.0 | آخر تحديث: 2026-06-03*
