# Contact Targeting Matrix — مصفوفة استهداف التواصل

أي دور نستهدف لكل نظام، والدور الثانوي البديل.

---

## 1. الدور حسب النظام

| النظام | الدور الأساسي | الدور الثانوي |
|--------|---------------|----------------|
| Revenue Operating System | Founder / Head of Sales / GM | Sales Operations Lead |
| Executive Command OS | Founder / CEO / GM | Executive Assistant |
| Follow-up Recovery OS | Sales Manager / Marketing Manager / Founder | Customer Service Lead |
| WhatsApp Client OS | Operations / Customer Service / Founder | Marketing Manager |
| Proposal & Proof OS | Founder / Partner / BD / Sales Lead | Proposal Writer |

---

## 2. الدور حسب القطاع (صانع القرار الأرجح)

| القطاع | صانع القرار الأرجح |
|--------|--------------------|
| Marketing Agencies | Founder / CEO |
| Training Companies | CEO / Head of Sales |
| Clinics | Operations Manager / Owner |
| Real Estate | Sales Manager / Owner |
| Professional Services | Partner / Managing Director |
| Recruitment | Founder / BD Lead |
| Logistics | Operations Director / GM |

---

## 3. أفضل مسار للتواصل (بالترتيب)

```
1) قناة عامة رسمية منشورة (إيميل/هاتف عام)  ← الأعلى ثقة
2) صفحة تواصل رسمية / نموذج تواصل
3) صفحة عامة على وسائل التواصل
4) استهداف بالدور (role-based) حين لا توجد قناة شخصية
```

كل مسار يُسجَّل مع `contact_confidence` المناسب (C0…C4).

---

## 4. القاعدة

> النظام يربط دائمًا **recommended_system → دور تواصل**. لا يُقبل Pack بلا دور أساسي وثانوي.
> يتحقق المدقّق من هذا الربط لكل 400 سجل.

---

*Version 1.0 — يقرأ مع PUBLIC_CONTACT_CHANNELS_AR و CONTACT_CONFIDENCE_LEVELS_AR*
