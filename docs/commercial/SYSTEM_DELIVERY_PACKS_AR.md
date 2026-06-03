# Dealix — حزم التسليم لكل نظام (Delivery Packs)

> كل نظام لازم يكون **قابلًا للتسليم فورًا**. هذه قائمة المخرجات الملموسة لكل نظام في
> أول Sprint.
>
> **مصدر الحقيقة:** حقل `deliveryPack` في `src/data/systems.ts`، ويتحقق منه
> `tests/systems.test.ts` (لا يقل عن 3 مخرجات لكل نظام).

---

## 1. Revenue OS — Delivery Pack

```txt
- خريطة تسرب الإيرادات (Revenue leakage map)
- مراحل الفرص (Opportunity stages)
- Workflow متابعة
- قوالب مسودات (Draft templates)
- تقرير يومي/أسبوعي
```

**أول Sprint (7–10 أيام):** نحلل مسار الفرص، نبني أول revenue workflow، ونجهّز تقريرًا
يوضح أين تضيع الفرص وماذا تفعل بعدها.

---

## 2. Executive Command OS — Delivery Pack

```txt
- خريطة مؤشرات (KPI map)
- مواصفات لوحة القرار (Decision dashboard spec)
- تقرير القيادة اليومي (Daily command report)
- مصفوفة المخاطر/الأولويات (Risk/priority matrix)
- سجل قرارات المؤسس (Founder action log)
```

**أول Sprint (7–14 يوم):** نجهّز Daily Executive Command يوضح أهم المؤشرات والقرارات
اليومية.

---

## 3. Follow-up Recovery OS — Delivery Pack

```txt
- Follow-up queue
- نموذج حالة العميل (Customer status model)
- حزمة رسائل متابعة (Follow-up message set)
- إيقاع التذكير (Reminder rhythm)
- تقرير استرجاع أسبوعي (Weekly recovery report)
```

**أول Sprint (7 أيام):** نبني follow-up queue، ونجهّز أول حزمة رسائل متابعة قابلة
للمراجعة والإرسال بعد الاعتماد.

---

## 4. WhatsApp Client OS — Delivery Pack

```txt
- خريطة WhatsApp flow
- Readiness scan
- Action cards
- سياسة التصعيد للإنسان (Human handoff policy)
- دليل التحويل لبوابة آمنة (Secure portal handoff guide)
```

**أول Sprint (7–10 أيام):** نصمّم أول WhatsApp flow ونجهّز action cards للعميل،
**بدون طلب مفاتيح أو أسرار داخل واتساب**.

> ملاحظة امتثال: واتساب يُستخدم كقناة خدمة عملاء وتجارة حوارية عبر WhatsApp Business
> Platform، **بعد اهتمام أو موافقة العميل** — وليس كـ cold WhatsApp.

---

## 5. Proposal & Proof OS — Delivery Pack

```txt
- نموذج Proposal (Proposal template)
- نموذج Proof Pack (Proof pack template)
- Scope / Out-of-scope
- افتراضات المخاطر (Risk assumptions)
- بطاقة الخطوة التالية (Next-step card)
```

**أول Sprint (5–7 أيام):** نجهّز نموذج عرض و Proof Pack لأول خدمة أو عميل مستهدف.

---

## 6. قاعدة الجودة قبل التسليم

| القاعدة | الحالة |
| --- | --- |
| كل نظام له Delivery Pack ≥ 3 مخرجات | مُلزِم (اختبار آلي) |
| كل مخرج قابل للمراجعة البشرية قبل التسليم | مُلزِم (حوكمة) |
| لا بيانات شخصية خام (PII) داخل التحليل | مُلزِم — تجهيل قدر الإمكان |
| التسليم النهائي للعميل يمر باعتماد المؤسس | مُلزِم (`Act with Approval`) |
| لا أسماء وحدات داخلية في مخرج موجّه للعميل | مُلزِم |
