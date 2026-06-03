# معايير قبول التسليم (Delivery Acceptance)
## نقطة القبول الرسمي — Day 11-14

> **السكيمة المرجعية:** [`schemas/delivery_acceptance.schema.json`](../../schemas/delivery_acceptance.schema.json)
> **قاعدة:** لا `ACC-XXXX` = لا اعتبار للتسليم مكتملًا. القبول يتطلب موافقة العميل الصريحة.

---

## 1. ما هو الـAcceptance Checkpoint

الـAcceptance Checkpoint هو اللحظة الرسمية التي يؤكد فيها العميل أن ما سُلِّم يستوفي المعايير المتفق عليها. يحدث في Day 11-14 من أول دورة تسليم، ثم عند كل مرحلة رئيسية لاحقة.

**بدون قبول رسمي:**
- التسليم لا يُعتبر مكتملًا
- لا يمكن إصدار فاتورة الدفع المتبقية
- لا يمكن الانتقال لمرحلة تالية أو تجديد

---

## 2. الحقول الإلزامية في `delivery_acceptance.schema.json`

| الحقل | النوع | الوصف | مثال من ACC-1001 |
|---|---|---|---|
| `id` | string | معرّف `ACC-XXXX` | `ACC-1001` |
| `created_at` | datetime | وقت إنشاء وثيقة القبول | `2026-06-03T17:00:00+03:00` |
| `company` | string | اسم الشركة | `Digital Rise Agency` |
| `handoff_id` | string | ربط بـ DHO-XXXX | `DHO-1001` |
| `criteria` | array | قائمة معايير القبول | (انظر §3) |
| `accepted` | boolean | هل قبِل العميل رسميًا؟ | `true` |

---

## 3. هيكل معايير القبول (`criteria`)

كل معيار في المصفوفة يحتوي على:

| الحقل | مطلوب | الوصف |
|---|---|---|
| `criterion` | ✅ | وصف المعيار |
| `met` | ✅ | هل تحقق المعيار؟ |
| `evidence_level` | لا (موصى به) | مستوى الدليل |

### مثال حي — ACC-1001 (Digital Rise Agency)

```
معايير القبول:
┌──────────────────────────────────────────────┬──────┬───────────────┐
│ المعيار                                       │ تحقق │ evidence_level│
├──────────────────────────────────────────────┼──────┼───────────────┤
│ تسليم خريطة تسرب الإيراد                     │  ✅  │ measured      │
│ تفعيل أول workflow متابعة                    │  ✅  │ measured      │
│ تسليم تقرير القيمة الأول                     │  ✅  │ measured      │
└──────────────────────────────────────────────┴──────┴───────────────┘

accepted: true
accepted_by: "client_authorized_contact"
accepted_at: "2026-06-03T17:30:00+03:00"
scope_changes_requested: []
```

---

## 4. حقول القبول الرسمي

| الحقل | النوع | الوصف |
|---|---|---|
| `accepted` | boolean | `true` = قبول؛ `false` = رفض/تحفظات |
| `accepted_by` | string | جهة التفويض من العميل |
| `accepted_at` | datetime | وقت القبول الرسمي |
| `scope_changes_requested` | array | طلبات تغيير نطاق (تُحال لـ Scope Guard) |

---

## 5. كيف تُحدَّد معايير القبول

معايير القبول تُؤخذ مباشرةً من `scope` في `DHO-XXXX`. كل عنصر في النطاق يصبح معيارًا قابلًا للقياس:

| عنصر النطاق في DHO | معيار القبول في ACC |
|---|---|
| "خريطة تسرب الإيراد" | "تسليم خريطة تسرب الإيراد" + `measured` |
| "تدقيق المتابعة" | "تسليم تقرير تدقيق المتابعة" + `measured` |
| "Proof Pack" | "تسليم Proof Pack مكتمل" + `client_data` |
| "خطة 30 يوم" | "تسليم خطة 30 يوم" + `measured` |

**قاعدة:** لا يوجد معيار قبول بـ `evidence_level: none` أو `assumption`.

---

## 6. إجراء الـAcceptance Checkpoint (Day 11-14)

```
Day 11:
  [L3] Delivery Owner يُعدّ مسودة ACC-XXXX
  [L3] يتحقق من كل معيار + evidence_level

Day 12:
  [L4] تسليم WVR-XXXX للعميل عبر البوابة الآمنة
  [L4] إرسال ACC-XXXX للعميل عبر البوابة للمراجعة

Day 13-14:
  [L4] اجتماع مراجعة مع العميل
  [L5] استلام accepted_by + accepted_at
  تسجيل في ai_action_ledger
  تحديث ONB-XXXX: status → "complete"
```

---

## 7. ماذا يحدث عند الرفض أو التحفظات

**إذا `accepted: false` أو توجد ملاحظات:**

| الحالة | الإجراء |
|---|---|
| ملاحظة ضمن النطاق الأصلي | إصلاح + إعادة عرض ACC-XXXX |
| طلب شيء جديد خارج النطاق | تسجيل في `scope_changes_requested` → Scope Guard |
| خلاف على معيار قبول | مراجعة DHO-XXXX الأصلي كمرجع |
| عجز تقني خارج عن الإرادة | تسجيل كمخاطرة + اقتراح تعديل timeline |

---

## 8. تعامل `scope_changes_requested`

إذا ذكر العميل أثناء جلسة القبول طلبات إضافية:

1. **سجّلها** في `scope_changes_requested` في `ACC-XXXX`
2. **لا تنفّذها** ضمن نطاق التسليم الحالي
3. **أحلها** لـ Scope Guard للتقييم
4. **لا تقبل** النطاق الأصلي مشروطًا بتنفيذها

> انظر [`SCOPE_CONTROL_POLICY_AR.md`](./SCOPE_CONTROL_POLICY_AR.md) للتفاصيل الكاملة.

---

## 9. معايير القبول المثالية لكل منتج

### `revenue_leakage_diagnostic`
| المعيار | الدليل المطلوب |
|---|---|
| خريطة تسرب الإيراد مُسلَّمة | `measured` |
| أول workflow متابعة مُفعَّل | `measured` |
| baseline مقاييس محدد | `client_data` |
| تقرير القيمة الأول مُسلَّم | `measured` |

### `followup_recovery_workflow`
| المعيار | الدليل المطلوب |
|---|---|
| workflow مُبني ومُختبَر | `measured` |
| نسبة متابعة مقاسة | `measured` |
| فريق العميل مدرَّب | `client_reported` |

### `monthly_optimization` (retainer)
| المعيار | الدليل المطلوب |
|---|---|
| 4 WVRs أسبوعية مُسلَّمة | `measured` |
| تقرير شهري مُسلَّم | `measured` |
| Proof Pack محدَّث | `measured` |

---

## 10. فحص ACC-XXXX قبل التسليم للعميل

- [ ] `handoff_id` يشير لـ `DHO-XXXX` الصحيح
- [ ] `criteria` ≥ 1 عنصر
- [ ] كل معيار له `met: true` أو وُثِّق سبب `false`
- [ ] `evidence_level` موجود في كل معيار (موصى به)
- [ ] `accepted_by` يشير لشخص مفوَّض من العميل
- [ ] `scope_changes_requested` وُثِّقت (ولو فارغة `[]`)
- [ ] التقرير يُسلَّم عبر البوابة الآمنة فقط

---

*مرجع الحوكمة: [AGENTS.md](../../AGENTS.md)*
*السكيمة: [`schemas/delivery_acceptance.schema.json`](../../schemas/delivery_acceptance.schema.json)*
*بيانات حقيقية: [`data/delivery/acceptance.jsonl`](../../data/delivery/acceptance.jsonl)*
