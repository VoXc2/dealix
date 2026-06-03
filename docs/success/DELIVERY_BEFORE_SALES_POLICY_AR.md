# التسليم قبل البيع — Delivery Before Sales Policy

> القاعدة الحاكمة: **لا تبِع أي Sprint إلا وله Delivery Pack جاهز.**
> هذا هو الفرق بين "نكتب كلاماً" و"نبيع شيئاً قابلاً للتسليم".

---

## 1. لماذا التسليم قبل البيع؟

البيع بلا تسليم جاهز يخلق:

```txt
- وعوداً لا نقدر نفي بها.
- scope creep يأكل الهامش.
- عميلاً غير راضٍ يضرّ السمعة المبكرة.
- مؤسساً غارقاً في تسليم مرتجل.
```

لذلك: **التسليم يُبنى أولاً، ثم يُباع.**

---

## 2. عقد الـ Delivery Pack (6 مكوّنات إلزامية)

لكل Sprint قابل للبيع، يجب أن يوجد Delivery Pack يحتوي:

```txt
1. Required Inputs        ← ماذا نطلب من العميل بالضبط
2. Delivery Steps         ← خطوات التنفيذ يوماً بيوم
3. Templates              ← القوالب الجاهزة للمخرجات
4. Acceptance Criteria    ← متى نعتبر التسليم مكتملاً
5. Weekly Value Report    ← كيف نُثبت القيمة أسبوعياً
6. Expansion Path         ← مسار التوسّع بعد الإثبات
```

أي Sprint ينقصه مكوّن واحد = **غير قابل للبيع** حتى يكتمل.

---

## 3. مثال مرجعي: Enrollment Recovery Sprint

### Required Inputs

```txt
- قائمة البرامج/الدورات
- عينة استفسارات
- رسائل متابعة حالية
- خطوات التسجيل
- قنوات التواصل
```

### Delivery Pack (المخرجات)

```txt
- Enrollment Inquiry Queue
- Student Status Model
- Course Inquiry Message Set
- Weekly Registration Recovery Report
- Next-step Handoff
```

### Acceptance Criteria

```txt
- كل استفسار له حالة.
- كل حالة لها رسالة.
- كل تسجيل محتمل له next action.
- يوجد تقرير أسبوعي واضح.
```

### Weekly Value Report (يثبت)

```txt
- عدد الاستفسارات الداخلة هذا الأسبوع.
- كم استفسار له حالة ورسالة.
- كم تسجيل محتمل تحرّك خطوة.
- أين ما زال يوجد تسرّب.
```

### Expansion Path

```txt
Enrollment Recovery Sprint
  → Retainer شهري لإدارة قمع التسجيل
  → إضافة WhatsApp Client OS
```

---

## 4. قالب Delivery Pack الموحّد (انسخه لكل Sprint جديد)

```txt
# [اسم الـ Sprint] — Delivery Pack

## Required Inputs
- ...

## Delivery Steps (Day 0 → Day N)
- Day 0: Intake
- Day 1: ...
- ...

## Templates
- [قالب 1]
- [قالب 2]

## Acceptance Criteria
- [ ] معيار 1
- [ ] معيار 2

## Weekly Value Report
- المؤشرات التي تُثبت القيمة أسبوعياً

## Expansion Path
- المسار من Sprint إلى Retainer/نظام إضافي
```

> النموذج المرجعي القائم: `company_os/delivery/p1_delivery_sop.md` (Revenue Intelligence Sprint)
> و`company_os/delivery/p1_intake_template.md` و`company_os/delivery/proof_pack_template.md`.

---

## 5. بوابة التسليم (Delivery Gate)

لا يبدأ تسليم فعلي إلا بعد:

```txt
[ ] Delivery Pack مكتمل المكوّنات الستة.
[ ] Required Inputs مستلمة وكاملة.
[ ] موافقة المؤسس على بدء التسليم.
[ ] تأكيد سعة التسليم (عدد الـ Sprints المتزامنة ضمن الطاقة).
```

بدء التسليم إجراء يتطلّب موافقة بشرية صريحة (Hard Rule).

---

## 6. سعة التسليم (Delivery Capacity)

| البند | القاعدة |
|-------|---------|
| الحد الأقصى المتزامن | حدّد عدداً واقعياً للـ Sprints المتوازية بجودة |
| إشارة التحذير | تجاوز السعة = خطر جودة، يُؤجَّل البيع لا التسليم |
| التوسّع | لا ترفع السعة قبل تثبيت Delivery Pack وأتمتة خطواته المتكررة |

تأثير السعة على القرار التشغيلي مذكور في [FOUNDER_OPERATING_MODEL_AR](./FOUNDER_OPERATING_MODEL_AR.md).

---

## 7. الربط بباقي البنية

- العروض التي تحتاج Packs: [OFFER_STRATEGY_AR](./OFFER_STRATEGY_AR.md).
- أثر التسليم على الهامش: [UNIT_ECONOMICS_AND_MARGIN_AR](./UNIT_ECONOMICS_AND_MARGIN_AR.md).
- مخاطر التسليم بلا جاهزية: [FAILURE_MODES_AND_COUNTERMEASURES_AR](./FAILURE_MODES_AND_COUNTERMEASURES_AR.md).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Status: Active*
