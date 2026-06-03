# قائمة الاعتماد — أفضل 100 (Top 100 System Approval Queue)

**التاريخ:** 2026-06-03
**الغرض:** ترتيب أفضل 100 مسودة من أصل 400 لمراجعة بشرية قبل أي إرسال.
**الحالة:** كل الصفوف `approval_status = pending` افتراضيًا.

---

## 1. معايير الترتيب

تُرتّب المسودات حسب (`APPROVAL_RANKING_SIGNALS` في `src/data/draftFactory.ts`):

```txt
1) ألم واضح
2) قطاع مناسب
3) إشارة شراء
4) قابلية الدفع
5) جودة التخصيص
6) انخفاض المخاطر
```

---

## 2. توزيع أفضل 100 حسب النظام

| النظام | عدد في Top 100 |
| --- | ---: |
| Revenue Operating System | 28 |
| Follow-up Recovery OS | 24 |
| Executive Command OS | 16 |
| WhatsApp Client OS | 16 |
| Proposal & Proof OS | 16 |
| **المجموع** | **100** |

---

## 3. عيّنة من القائمة (أعلى 10)

| # | الشركة (مثال) | القطاع | النظام الموصى به | إشارة | risk | approval |
| ---: | --- | --- | --- | --- | :---: | :---: |
| 1 | Digital Rise Agency | وكالة تسويق | Revenue Operating System | leads بلا متابعة | low | pending |
| 2 | TrainMe KSA | تدريب | Follow-up Recovery OS | استفسارات واتساب تضيع | low | pending |
| 3 | CloudShift Consulting | استشارات B2B | Proposal & Proof OS | إغلاق صفقات بطيء | medium | pending |
| 4 | Growth Labs SA | وكالة تسويق | Revenue Operating System | لا pipeline واضح | low | pending |
| 5 | SkillUp Arabia | تدريب | Follow-up Recovery OS | تحويل تسجيل منخفض | low | pending |
| 6 | Riyadh Smile Clinic | عيادة | WhatsApp Client OS | واتساب فوضوي | medium | pending |
| 7 | Amaken Real Estate | عقار | Follow-up Recovery OS | متابعة معاينات تضيع | low | pending |
| 8 | NextGen GM Office | شركة خدمات | Executive Command OS | لا رؤية قرار يومية | medium | pending |
| 9 | BrightAds Agency | وكالة تسويق | Proposal & Proof OS | عروض غير مقنعة | low | pending |
| 10 | CareDent Clinics | عيادة | WhatsApp Client OS | حجوزات تضيع بالرسائل | medium | pending |

> الأسماء أعلاه أمثلة تمثيلية لتوضيح بنية القائمة، وليست بيانات عملاء حقيقية.

---

## 4. سياسة الإرسال بعد الاعتماد

- يبدأ الإرسال بـ **20–80 فقط** من القائمة حسب صحة الدومين.
- لا يُرسَل أي صف قبل أن يصبح `approval_status = approved` و `send_readiness = ready`.
- أي صف عالي المخاطر (`risk = high`) يحتاج مراجعة إضافية من المؤسس.

---

## 5. ضوابط الحوكمة

مرتبطة بـ `company_os/governance/agent_permissions.md`:

```txt
AI drafts → Human reviews → Approve/Reject → If approved: execute → Log
```

لا يملك الذكاء الاصطناعي صلاحية الإرسال أو اتخاذ قرار التسعير.
