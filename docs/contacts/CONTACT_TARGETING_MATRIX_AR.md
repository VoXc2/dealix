# Contact Targeting Matrix — مصفوفة استهداف الأدوار

> من نكلّم؟ لكل نظام دورٌ أول وثانٍ وثالث. إذا لم يوجد اسم شخص منشور، نستهدف **الفريق/الدور** — ولا نخترع اسمًا.

---

## 1. المصفوفة

| النظام | الدور الأول | الدور الثاني | الدور الثالث |
|--------|-------------|--------------|--------------|
| **Revenue Operating System** | Head of Sales | Founder / GM | Marketing Manager |
| **Executive Command OS** | Founder / CEO | General Manager | Operations Manager |
| **Follow-up Recovery OS** | Sales Manager | Marketing Manager | Founder |
| **WhatsApp Client OS** | Operations Manager | Customer Service Manager | Founder |
| **Proposal & Proof OS** | Founder / Partner | BD Manager | Sales Lead |

> هذه المصفوفة **مفروضة آليًا**: `likely_decision_maker_role` في كل Pack يجب أن يطابق أحد أدوار النظام الموصى به، وإلا يفشل `npm run factory:check`.

---

## 2. عند غياب اسم الشخص

يرسل النظام إلى الدور/الفريق عبر القناة العامة:

```
فريق الإدارة · فريق المبيعات · فريق التسويق · فريق العمليات
```

ولا يخترع اسمًا أو منصبًا لشخص بعينه.

---

## 3. تطبيق على العيّنة الحالية

| الحساب | النظام | الدور المستهدف | مطابق؟ |
|--------|--------|-----------------|:-----:|
| `ACC-001` Madar | Revenue Operating System | Head of Sales | ✅ |
| `ACC-002` Tadreeb Plus | Follow-up Recovery OS | Sales Manager | ✅ |
| `ACC-003` Afaq | Follow-up Recovery OS | Marketing Manager | ✅ |
| `ACC-004` Noor Clinics | WhatsApp Client OS | Operations Manager | ✅ |
| `ACC-005` Rased | Proposal & Proof OS | Founder / Partner | ✅ |
| `ACC-006` Tawteen | Executive Command OS | General Manager | ✅ |
| `ACC-007` BinaaPro | Proposal & Proof OS | BD Manager | ✅ |
| `ACC-008` Mohtawa | Revenue Operating System | Founder | ✅ |

---

## 4. لماذا الدور وليس الشخص؟

1. **خصوصية:** نتجنب جمع/تخزين بيانات شخصية بلا حاجة (PDPL).
2. **دقة:** الدور أكثر استقرارًا من اسم قد يتغير.
3. **احترافية:** رسالة موجّهة للدور الصحيح أقوى من اسم مخمَّن خاطئ.

---

*Contact Targeting Matrix | الإصدار 1.0 | آخر تحديث: 2026-06-03*
