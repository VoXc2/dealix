# Delivery Acceptance Gates — بوابات قبول التسليم

**الهدف:** ضمان أن التسليم لا يبدأ ناقصًا، وأن العميل لا يُسلَّم إلا ما يطابق معايير القبول.

---

## 1. بوابة البدء — الخمسة الإلزامية

لا تبدأ أي مرحلة تسليم (`delivery_started` فأعلى) قبل توفّر:

```txt
1. النظام الذي اشتراه العميل      (system)
2. Scope واضح                    (scope)
3. Required inputs مكتملة         (required_inputs كلها provided = true)
4. Success metric                (success_metric)
5. Delivery owner / مسؤول التسليم (delivery_owner)
```

إذا نقص أي عنصر، الحالة تكون:

```txt
Delivery Not Ready
```

وتظهر الشركة في [`reports/delivery/DELIVERY_BLOCKERS.md`](../../reports/delivery/DELIVERY_BLOCKERS.md) مع تحديد الناقص بالضبط.

> **مثال حالي (من البيانات):**
> - `TechVenture Partners` (Executive Command OS, won) → ناقص: `delivery_owner` + 5 مدخلات.
> - `TrainMe KSA` (WhatsApp Client OS, intake_required) → ناقص: سياسة الملفات + قواعد التصعيد.

## 2. الفرض الآلي

الفحص **C05** في [`acquisition_delivery_check.py`](../../scripts/acquisition_delivery_check.py) يرفع **CRITICAL** ويُفشل البناء إذا وُجد خط في `delivery_started` فأعلى بأي عنصر ناقص. (أثبتنا فعليًا أنه يلتقط الخرق عند اختبار سلبي.)

## 3. معايير القبول (acceptance)

عند `client_review`، يُقبل المخرج فقط إذا طابق **Acceptance Criteria** للنظام في [SYSTEM_DELIVERY_CHECKLISTS_AR.md](SYSTEM_DELIVERY_CHECKLISTS_AR.md). الحالات الممكنة في تقرير القيمة الأسبوعي:

```txt
pending            → بانتظار مراجعة العميل/الموافقة
accepted           → مقبول
changes_requested  → مطلوب تعديلات
```

## 4. ما الذي لا يُؤتمت عند البوابة؟

```txt
- التسعير النهائي وروابط الدفع
- العقود والالتزامات القانونية
- طلب API keys أو بيانات حساسة
- نشر case study (يحتاج موافقة صريحة)
```

> الأتمتة تتوقف عند حافة المخاطرة: الإرسال والالتزام والتسعير قرارات بشرية.
