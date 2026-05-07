# Dealix — النجم الشمالي (North Star)

هذا الملف يحدد **ماذا نفوز** و**كيف نعرف أننا نفوز**، بصيغة واحدة لا تتغير كل أسبوع. تفاصيل التدشين: [LAUNCH_MASTER_PLAN_AR.md](../LAUNCH_MASTER_PLAN_AR.md). الفئة والمعمارية: [CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md](CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md).

---

## 1) المخرج النهائي (Outcome) — هذا هو النجم الشمالي

**Dealix ينجح عندما:**

```text
عميل سعودي (أو وكالة) يدخل من قناة آمنة
→ يحصل على قرار واضح (كرت / تشخيص)
→ يمرّ تنفيذ بموافقة (لا حرق قنوات)
→ يستلم Proof Pack بأرقام
→ يدفع أو يجدد أو يحيل
→ والشركة تقيس ذلك أسبوعياً بدل السوالف
```

**جملة واحدة**

```text
النجم الشمالي = إثبات تنفيذ إيرادات سعودي متكرر: Proof Pack + دفع/تجديد + تعلّم أسبوعي
```

هذا **ليس** «أكبر عدد ميزات» ولا «أكثر automation» ولا «CRM كامل».

---

## 2) المقياس الرئيسي حسب المرحلة (لا تخلط المراحل)

| المرحلة | المقياس الرئيسي (North Star لهذه المرحلة) | لماذا |
|---------|--------------------------------------------|--------|
| التدشين (0–90 يوم أولاً) | **عدد Proof Packs مسلّمة + عدد Pilots المدفوعة/المؤكدة** | بدون إثبات تسليم لا يوجد تكرار ولا ثقة |
| بعد تكرار التسليم | **MRR** (اشتراكات شهرية نشطة) كما في [dealix_kpi_framework.md](../sales-kit/dealix_kpi_framework.md) | MRR معنى فقط بعد وجود عملاء يدفعون شهرياً |

**مرجع المبيعات الطموح (Y1):** ملف [DEALIX_MASTER_PLAYBOOK.md](../sales-kit/DEALIX_MASTER_PLAYBOOK.md) يضع MRR كـ North Star metric على أفق أطول — **استخدمه بعد** أن يثبت مسار Pilot + Proof في السوق.

---

## 3) مؤشرات قيادية أسبوعية (Leading — لا أكثر من 5)

راقبها كل اثنين (أو يوم Scorecard). مأخوذة ومطابقة لفلسفة [dealix_kpi_framework.md](../sales-kit/dealix_kpi_framework.md) مع تركيز التدشين:

1. **Leads بـ `next_step` غير فارغ** — هدف: 100% من الصفوف النشطة في [Operating Board](../ops/full_ops_pack/GOOGLE_SHEET_MODEL_AR.md).
2. **Diagnostics مرسلة** — حسب `diagnostic_status` في اللوحة أو الـ Dashboard.
3. **Pilots معروضة ومتابَعة** — `pilot_status` + تاريخ لمسة.
4. **Proof Packs مسلّمة** — `proof_pack_status = delivered` + مستند/لقطة.
5. **مخاطر محجوبة** — `risks_blocked` أو سجل قرارات Policy (واتساب بارد = 0).

**تنبيه أحمر:** أسبوع بلا Proof ولا Pilot معروض رغم وجود leads مؤهّلة = انحراف عن النجم الشمالي.

---

## 4) كيف تربط النجم الشمالي بخطة التدشين

| مرحلة [LAUNCH_MASTER_PLAN_AR](../LAUNCH_MASTER_PLAN_AR.md) | ما يثبت للنجم الشمالي |
|----------------------------------------------------------|------------------------|
| 0–1 | البنية التحتية تعطي **ثقة** في القياس (صحة API، smoke) |
| 2 | **قناة دخول** موثّقة + قائمة قبول Level 1 |
| 3 | **أول Proof + أول دفع/التزام** — نقطة تحوّل |
| 4 | إطلاق عام فقط مع [LAUNCH_GATES](../LAUNCH_GATES.md) + [PUBLIC_LAUNCH](../PUBLIC_LAUNCH_CHECKLIST.md) |

---

## 5) بوابات الريبو ذات الصلة

- [LAUNCH_GATES.md](../LAUNCH_GATES.md) — خصوصاً G4/G5 (leads حقيقية / صفقة مدفوعة) عندما تنتقل من Pilot إلى مقياس تجاري أوسع.
- [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](../ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md) — أدلة لكل محور.

---

## 6) ممنوعات (تخرجك عن النجم الشمالي)

- بيع «AI» بدون Proof.
- cold WhatsApp أو أتمتة قنوات محظورة.
- بناء ميزات جديدة قبل **أول Proof Pack حقيقي** لعميل (انظر [POST_LAUNCH_BACKLOG](../ops/POST_LAUNCH_BACKLOG.md)).

---

## 7) مراجع إضافية

- [SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md) — الحلقات والأدلة.
- [DAILY_SCORECARD_TEMPLATE_AR.md](../ops/full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md) — يومياً على الأرض.
