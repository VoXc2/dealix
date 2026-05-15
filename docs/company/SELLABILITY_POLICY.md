# Sellability Policy — سياسة البيع (CEO)

**قاعدة:** لا تُباع رسمياً إلا ما لديه **أدلة** كاملة. لا تعتمد على الإحساس.

المرجع: [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md)، [`DEALIX_STAGE_GATES_AR.md`](DEALIX_STAGE_GATES_AR.md).

---

## Official (بيع رسمي)

تُباع الخدمة رسمياً فقط إذا:

1. **Offer score ≥ 85** (وملف `offer.md` بأقسامه الإلزامية).
2. **Delivery score ≥ 85** (يدوياً في لوحة الجاهزية؛ ملفات تسليم موجودة).
3. **Governance score ≥ 90** (معيار يدوي صارم + نجاح [`verify_governance_rules.py`](../../scripts/verify_governance_rules.py)).
4. **Demo score ≥ 85** (حزمة `demos/` للخدمات المعروضة بقوة + [`DEMO_READINESS.md`](../delivery/DEMO_READINESS.md)).
5. **QA checklist** موجود لكل خدمة.
6. **Proof pack template** موجود لكل خدمة.
7. **Sales assets** (Gate 6) جاهزة.
8. **Scope** واضح في `scope.md`.
9. **الاستثناءات** واضحة في `offer.md` (Not included).
10. **لا** يتضمن العرض إجراءً من **FORBIDDEN_ACTIONS** بدون مسار موافقة ومسودة فقط.

---

## Beta (تجربة محدودة)

- Score **70–84** أو نقص محدود (مثلاً demo يتطور لكن العرض قوي).
- **Pilot** بتوقعات مكتوبة وسعر/نطاق يعكس التجربة.
- **لا تُ scale** في التسويق العام ولا تُعدّ «كتالوجاً رسمياً» حتى تصل إلى Official.

---

## Custom (مؤسسي / عميل محدد)

- خارج الكتالوج الرسمي؛ **عرض منفصل** + SOW واضح.
- لا يُعدّ في المصفوفة كـ «خدمة رسمية» حتى تُستنسخ كحزمة بعد التعلّم.

---

## Not Ready (ممنوع البيع)

- أقل من 70 نقطة تقريباً في تقييم الجاهزية، أو وجود **hard fail** (لا QA، لا scope، لا حوكمة، وعود مبيعات مضمونة، إرسال تلقائي غير محكوم، إلخ).
- **ممنوع:** الإعلان، الوعد العلني، أو إدراجها في عروض عامة.

---

## قواعد قرار سريعة

| الحالة | إجراء |
|--------|--------|
| Governance FAIL | **لا بيع** حتى تُصلح الحوكمة. |
| QA FAIL | **لا تسليم** للعميل النهائي. |
| Demo FAIL | **لا تسوق** الخدمة بقوة؛ أكمل الـdemo أولاً. |
| Product FAIL (MVP) | مسموح **service-assisted** فقط؛ ليس ادّعاء SaaS كامل. |
| Offer FAIL | **لا تعرض** الخدمة في الكتالوج الرسمي. |

---

## التحقق

```bash
python scripts/verify_dealix_ready.py
```
