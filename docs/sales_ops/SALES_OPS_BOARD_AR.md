# لوحة عمليات المبيعات (Sales Ops Board)

> لوحة بسيطة للفرص، تسمح بتسليم المتابعة لشخص آخر دون فوضى.
> AI drafts. Human approves. System logs.

---

## 1. الفكرة

كل فرصة تمر بمسار واضح من ١٦ حالة (انظر `LEAD_STATUS_MODEL_AR.md`)، ولكل حالة مالك. هذا يتيح للمؤسس تفويض المتابعة بدون ضياع.

```txt
Researched → Need Card Ready → Draft Ready → Approved → Sent
→ Call Due → Called → Interested → Mini Proposal Ready → Proposal Sent
→ Won → Delivery Started → Active → Renewal Candidate
(Lost / Do Not Contact في أي وقت)
```

---

## 2. أعمدة اللوحة

| العمود | الوصف |
|--------|-------|
| Company | الشركة |
| Segment | القطاع (Marketing Agency / Training / B2B Services) |
| Stage | الحالة الحالية |
| Draft Score | درجة المسودة (إن وُجدت) |
| Recommended System | النظام المقترح من الخمسة |
| Owner | المالك المسؤول |

---

## 3. الأنظمة الخمسة (Focus-5)

| النظام | الاسم الظاهر للعميل |
|--------|----------------------|
| Revenue Operating System | نظام تشغيل الإيرادات |
| Follow-up Recovery OS | نظام استرجاع المتابعات |
| Executive Command OS | نظام القيادة التنفيذية |
| WhatsApp Client OS | نظام عملاء واتساب |
| Proposal & Proof OS | نظام العروض والإثبات |

> المرجع الكنسي: `company_os/commercial/systems.json`.

---

## 4. المخرج اليومي

`reports/sales_ops/SALES_OPS_BOARD_STATUS.md` (يُولَّد عبر `npm run commercial:plan`) ويحتوي:
- عدّادات الحالات الـ16
- جدول الشركات
- Call Brief Queue لليوم
- Mini Proposal Queue

---

## 5. حدود الأمان

- `do_not_contact` يعني suppression قاطع؛ أي مسودة تستهدف شركة مكبوتة تفشل في Email Gate.
- لا اتصال آلي، ولا واتساب بارد آلي، ولا قوائم مشتراة.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
