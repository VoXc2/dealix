# نظام تسليم العميل (Client Delivery OS)
## من صفقة مربوحة إلى تسليم قيمة حقيقية

> **مصدر الحقيقة:** هذا المستند يصف النظام الكامل للتسليم. لا يُعاد كتابة أي شيء من `company_os/`؛ يُوسَّع ويُربَط فقط.
> **ثابت لا يتغير:** لا يوجد ضمان عائد (ROI). كل رقم يحمل `evidence_level`. كل صفقة مربوحة تنتج handoff.

---

## 1. ما هو نظام التسليم

نظام التسليم هو المسار الذي تسلكه كل صفقة مربوحة (Won Deal) من لحظة التوقيع حتى تسليم القيمة الفعلية للعميل وقبوله الرسمي لها. يمتد النظام من GTM إلى Delivery ويشمل:

| المرحلة | الكيان | المعرّف |
|---|---|---|
| تسليم المبيعات للتسليم | Delivery Handoff | `DHO-XXXX` |
| إعداد العميل (أول 14 يوم) | Client Onboarding | `ONB-XXXX` |
| تقرير القيمة الأسبوعي | Weekly Value Report | `WVR-XXXX` |
| قبول التسليم الرسمي | Delivery Acceptance | `ACC-XXXX` |

---

## 2. قاعدة لا تُكسر: كل صفقة مربوحة = handoff

```
Won Deal (PROP-XXXX) → DHO-XXXX (Delivery Handoff) → ONB-XXXX (Onboarding)
    → WVR-XXXX (Weekly Value Report) → ACC-XXXX (Acceptance)
```

مثال حقيقي: Digital Rise Agency
- عرض مقبول: `PROP-1002`
- handoff مُنشأ: `DHO-1001`
- إعداد عميل: `ONB-1001` (Day0 و Day1 مكتملان)
- تقرير قيمة: `WVR-1001` (نسبة المتابعة 43% → 61%، `evidence_level: measured`)
- قبول رسمي: `ACC-1001` مقبول

---

## 3. الأدوار في نظام التسليم

| الدور | المسؤولية | مستوى الصلاحية |
|---|---|---|
| **Delivery Owner** | المسؤول عن تنفيذ النطاق الكامل | L4 (Act with Approval) |
| **Scope Guard** | يمنع تضخم النطاق؛ يُحيل طلبات التغيير | L3 (Draft) |
| **Client Success** | إيقاع أسبوعي/شهري؛ تقرير القيمة | L3 (Draft) |
| **المؤسس** | موافقة على أي تغيير نطاق أو escalation | L4/L5 |

---

## 4. كتالوج المنتجات المدعومة في التسليم

| `product_id` | الاسم | نوع التسليم |
|---|---|---|
| `readiness_scan` | فحص الجاهزية | تقرير + توصيات |
| `revenue_leakage_diagnostic` | تشخيص تسرب الإيراد | تقرير + خريطة + 30-يوم |
| `followup_recovery_workflow` | سير عمل استرداد المتابعة | workflow نشط |
| `ai_revenue_ops_starter` | مبتدئ عمليات الإيراد بالذكاء | نظام تشغيل أساسي |
| `full_revenue_os` | نظام الإيراد الكامل | تسليم متكامل |
| `monthly_optimization` | تحسين شهري | retainer مستمر |
| `custom_company_os` | نظام شركة مخصص | تصميم + بناء |
| `multi_department_rollout` | توسعة متعددة الأقسام | مشروع كبير |

---

## 5. إيقاع نظام التسليم

### يومي
- مراجعة طابور الموافقات (`approval_queue`)
- تتبع checklist الإعداد (`ONB-XXXX`)
- تحديث `ai_action_ledger` بكل إجراء خارجي

### أسبوعي
- إعداد وتسليم `WVR-XXXX` عبر البوابة الآمنة فقط
- مراجعة المخاطر مع Delivery Owner
- فحص أي طلبات تغيير نطاق (تُحال لـ Scope Guard)

### في Day 11-14
- تحضير معايير القبول (`ACC-XXXX`)
- عرض `ACC-XXXX` على العميل للموافقة الرسمية
- تسجيل القبول أو الملاحظات في النظام

---

## 6. الحدود والخطوط الحمراء في التسليم

| ممنوع | السبب |
|---|---|
| ضمان ROI بنسبة محددة | لا `evidence_level` يدعم ضمانًا |
| تسليم الملفات/الأسرار عبر واتساب | البوابة الآمنة فقط |
| امتصاص طلبات تغيير النطاق بصمت | يجب مرور Scope Guard |
| بدء التسليم بلا `DHO-XXXX` مكتمل | قاعدة لا تُكسر |
| صلاحية وصول أوسع من المطلوب | مبدأ أقل امتياز |
| أرقام في التقارير بلا `evidence_level` | غير صالح في Dealix |

---

## 7. تدفق الموافقات في التسليم

```
صفقة مربوحة
    → [L4] إنشاء DHO-XXXX + موافقة المؤسس
    → [L4] منح صلاحيات الوصول عبر البوابة (أقل امتياز)
    → [L3] تنفيذ Day0-Day14
    → [L3] إعداد WVR-XXXX (مسودة)
    → [L4] تسليم WVR-XXXX للعميل عبر البوابة
    → [L4] عرض ACC-XXXX + موافقة العميل
    → تسجيل في ai_action_ledger
```

---

## 8. مقياس الأدلة في التسليم

كل مقياس في تقرير القيمة يجب أن يحمل `evidence_level` من السلّم الآتي:

| `evidence_level` | المعنى | صالح في WVR؟ |
|---|---|---|
| `none` | لا دليل | لا |
| `assumption` | فرضية داخلية | لا |
| `benchmark` | معيار صناعي | بحذر |
| `client_reported` | العميل ذكره | نعم (مع تحفظ) |
| `client_data` | بيانات العميل الفعلية | نعم |
| `measured` | قِسناه أثناء التسليم | نعم (مثالي) |
| `verified` | مُتحقَّق مستقلًا | نعم (أعلى) |

> مثال: نسبة المتابعة لـ Digital Rise Agency: baseline `43%` → current `61%` بـ `evidence_level: measured`.

---

## 9. الصلاحيات المطلوبة (أقل امتياز)

الصلاحيات المسموح بها فقط عبر البوابة الآمنة:

| الصلاحية | الاستخدام |
|---|---|
| `read_only_crm` | قراءة بيانات CRM فقط |
| `read_only_sheet` | قراءة جداول البيانات |
| `read_only_inbox` | مراجعة الرسائل فقط |
| `file_upload` | رفع ملفات عبر البوابة |
| `report_view` | عرض التقارير |

> لا صلاحيات كتابة إلا بموافقة صريحة من العميل والمؤسس.

---

## 10. الروابط المرجعية

| الوثيقة | الموقع |
|---|---|
| SOP تسليم P1 | [`company_os/delivery/p1_delivery_sop.md`](../../company_os/delivery/p1_delivery_sop.md) |
| قالب Intake | [`company_os/delivery/p1_intake_template.md`](../../company_os/delivery/p1_intake_template.md) |
| خطة نجاح العميل | [`company_os/delivery/client_success_plan.md`](../../company_os/delivery/client_success_plan.md) |
| قالب Proof Pack | [`company_os/delivery/proof_pack_template.md`](../../company_os/delivery/proof_pack_template.md) |
| سكيمة handoff | [`schemas/delivery_handoff.schema.json`](../../schemas/delivery_handoff.schema.json) |
| سكيمة onboarding | [`schemas/client_onboarding.schema.json`](../../schemas/client_onboarding.schema.json) |
| سكيمة WVR | [`schemas/weekly_value_report.schema.json`](../../schemas/weekly_value_report.schema.json) |
| سكيمة acceptance | [`schemas/delivery_acceptance.schema.json`](../../schemas/delivery_acceptance.schema.json) |
| بيانات التسليم | [`data/delivery/`](../../data/delivery/) |

---

*مرجع الحوكمة: [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لـ Dealix.*
*الإصدار 1.0 — Client Delivery OS — Agent #2.*
