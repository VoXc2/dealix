# استراتيجية العرض — Offer Strategy

> داخلياً نملك كتالوج أنظمة واسع. خارجياً نعرض **5 أنظمة فقط**.
> الواجهة بسيطة، والكتالوج الداخلي يُستخدم لتخصيص الـ Sprint.
> ترتيب الأولوية العملي في [OFFER_PRIORITY_REVIEW](../../reports/success/OFFER_PRIORITY_REVIEW.md).

---

## 1. الأنظمة الخمسة العامة (Core Systems)

```txt
1. Revenue Operating System
2. Executive Command OS
3. Follow-up Recovery OS
4. WhatsApp Client OS
5. Proposal & Proof OS
```

هذه هي الواجهة الوحيدة للعميل. كل ما عداها يبقى تفصيلاً داخلياً.

| النظام | المخرج للعميل | الألم الذي يعالجه |
|--------|----------------|-------------------|
| Revenue Operating System | تشغيل إيرادات منظّم | فوضى المبيعات والمتابعات |
| Executive Command OS | قرار يومي واضح | غياب رؤية تنفيذية |
| Follow-up Recovery OS | استرجاع فرص ضائعة | متابعات تسقط |
| WhatsApp Client OS | واتساب كـ workflow | محادثات بلا نظام |
| Proposal & Proof OS | عرض مقنع بدليل | عروض غامضة تطيل القرار |

---

## 2. الـ Sprints المتخصّصة التي تبيع فعلياً

| Sprint | لمن؟ | لماذا قوي؟ | السعر الافتتاحي |
|--------|------|------------|----------------:|
| Enrollment Recovery Sprint | تدريب | يحوّل الاستفسار لتسجيل | 3,500–4,500 SAR |
| Proposal & Scope Proof Sprint | استشارات/خدمات | يرفع وضوح العرض ويقلّل التردد | 3,000–5,000 SAR |
| Campaign Lead Recovery Sprint | وكالات | يربط الحملات بالمتابعة | 4,500–6,000 SAR |
| Clinic Appointment Flow Sprint | عيادات | ينظّم الحجز والواتساب | 4,500–6,500 SAR |
| Executive Daily Command Sprint | مؤسسون | يعطي قرار يومي واضح | 5,500–8,000 SAR |

> **ملاحظة تسعير:** هذه أسعار افتتاحية. الأسعار النهائية تمرّ عبر بوابة موافقة المؤسس
> (لا يحدّد أي وكيل سعراً نهائياً). راجع [UNIT_ECONOMICS_AND_MARGIN_AR](./UNIT_ECONOMICS_AND_MARGIN_AR.md).

---

## 3. نموذج "ابدأ صغيراً ثم وسّع"

```txt
Sprint افتتاحي (أيام)
  → إثبات قيمة (Weekly Value Report)
  → توسعة (Sprint إضافي أو Retainer)
```

العرض الافتتاحي مصمّم ليكون **قرار شراء صغير**، والتوسعة تأتي من **الإثبات** لا من الإلحاح.

---

## 4. خريطة الاحتياج → النظام → الـ Sprint

| الاحتياج | النظام العام | الـ Sprint | القطاع الأنسب |
|----------|--------------|------------|----------------|
| استفسارات تضيع قبل التسجيل | Follow-up Recovery OS | Enrollment Recovery | تدريب |
| Leads حملات بلا متابعة | Follow-up Recovery OS | Campaign Lead Recovery | وكالات |
| عرض غامض يطيل القرار | Proposal & Proof OS | Proposal & Scope Proof | استشارات |
| حجوزات وواتساب فوضى | WhatsApp Client OS | Clinic Appointment Flow | عيادات |
| لا قرار يومي للمؤسس | Executive Command OS | Executive Daily Command | مؤسسون |

---

## 5. شرط البيع: لا Sprint بلا Delivery Pack

**قاعدة صارمة:** لا يُعرض أي Sprint للبيع إلا وله Delivery Pack جاهز يتضمّن:

```txt
1. Required Inputs
2. Delivery Steps
3. Templates
4. Acceptance Criteria
5. Weekly Value Report
6. Expansion Path
```

التفاصيل الكاملة والقالب في [DELIVERY_BEFORE_SALES_POLICY_AR](./DELIVERY_BEFORE_SALES_POLICY_AR.md).

> **حالة اليوم:** يوجد Delivery Pack واحد جاهز (Revenue Intelligence في
> `company_os/delivery/p1_delivery_sop.md`). باقي الـ Sprints تحتاج Delivery Packs قبل عرضها للبيع.

---

## 6. أفضل العروض للبداية (مبدئياً)

من زاوية: ألم واضح + بيع سريع + تسليم سريع + هامش جيد + توسّع لاحق:

```txt
1. Proposal & Proof OS
2. Follow-up Recovery OS
3. Executive Command OS
4. Lead Qualification OS
5. Client Onboarding OS
```

الترتيب النهائي المبني على الحالة الفعلية في
[OFFER_PRIORITY_REVIEW](../../reports/success/OFFER_PRIORITY_REVIEW.md).

---

## 7. ممنوعات العرض

```txt
- scope مفتوح.
- وعود ROI مضمونة.
- سعر نهائي بدون موافقة المؤسس.
- إرسال تلقائي لأي عرض.
- عرض Sprint بلا Delivery Pack.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Status: Active*
