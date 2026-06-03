# نموذج أول 14 يوم في التسليم
## من Day 0 إلى Day 14: التفصيل الكامل لكل يوم

> **ثابت:** كل خطوة تعتمد على اكتمال ما قبلها. لا تسريع بدون اكتمال checklist.
> **مرجع السكيمة:** [`schemas/client_onboarding.schema.json`](../../schemas/client_onboarding.schema.json)
> **SOP المرجعي:** [`company_os/delivery/p1_delivery_sop.md`](../../company_os/delivery/p1_delivery_sop.md)

---

## نظرة عامة على النموذج

| المرحلة | الأيام | الهدف الرئيسي | نقطة التحقق |
|---|---|---|---|
| **التأسيس** | Day 0-1 | Handoff + صلاحيات + Intake | `day0_handoff` + `day1_access_intake` |
| **الرسم والتحليل** | Day 2-3 | خريطة الـworkflow الحالي | `day2_3_workflow_mapping` |
| **البناء** | Day 4-7 | أول مسودة/نموذج أولي | `day4_7_first_draft` |
| **المراجعة** | Day 8-10 | تصحيح + ضبط | `day8_10_review_correction` |
| **القبول** | Day 11-14 | تقرير قيمة أول + قبول رسمي | `day11_14_first_report_acceptance` |

---

## Day 0 — تسليم الـHandoff وإعداد بيئة التسليم

**الهدف:** أن يكون كل شيء جاهزًا قبل أن يتصل التسليم بالعميل.

### صباحًا (المؤسس + المبيعات)
- [ ] مراجعة `DHO-XXXX` والتأكد من اكتمال الحقول الإلزامية
- [ ] موافقة المؤسس على `DHO-XXXX` (يُسجَّل `approved_by` + `approved_at`)
- [ ] تسجيل الإجراء في `ai_action_ledger`

### مساءً (Delivery Owner)
- [ ] قبول `DHO-XXXX` وتحديث `status → "accepted"`
- [ ] إنشاء `ONB-XXXX` مرتبط بـ `DHO-XXXX`
- [ ] إعداد بيئة العمل الداخلية (مجلد العميل، قالب التتبع)
- [ ] تحضير رابط البوابة الآمنة لمنح الصلاحيات

### المخرجات
- ✅ `DHO-XXXX` بحالة `accepted`
- ✅ `ONB-XXXX` بحالة `not_started` → `in_progress`
- ✅ `day0_handoff: true` في checklist
- ✅ الـhandoff مُسجَّل في `ai_action_ledger`

---

## Day 1 — صلاحيات الوصول + نموذج الـIntake

**الهدف:** الحصول على كل البيانات والصلاحيات اللازمة.

### أولويات اليوم
- [ ] إرسال رابط البوابة الآمنة للعميل لمنح الصلاحيات (`required_access` من DHO)
- [ ] إرسال [`p1_intake_template.md`](../../company_os/delivery/p1_intake_template.md) للعميل
- [ ] استلام البيانات المطلوبة وفحص اكتمالها
- [ ] الإجابة على أسئلة العميل

### فحص الاكتمال
| البيانات | مطلوبة؟ | وضع Day 1 |
|---|---|---|
| تصدير CRM (آخر 90 يومًا) | ✅ | — |
| 20-50 محادثة مبيعات | ✅ | — |
| 2-3 نماذج عروض | ✅ | — |
| قنوات التواصل المستخدمة | ✅ | — |
| وصف عملية المتابعة الحالية | ✅ | — |

### إذا كانت البيانات ناقصة
- وثّق الناقص في `risks` بـ `ONB-XXXX`
- حدد موعدًا للاستكمال (لا يتجاوز Day 2)
- لا تبدأ التحليل قبل اكتمال البيانات الإلزامية

### المخرجات
- ✅ `access_granted: true` في `ONB-XXXX`
- ✅ `day1_access_intake: true` في checklist
- ✅ بيانات العميل مستلمة ومنظّمة

---

## Day 2-3 — خريطة الـWorkflow الحالي

**الهدف:** فهم عميق لكيفية عمل العميل الآن — لا اقتراحات، فقط وصف.

### Day 2 — الرسم والتوثيق
- [ ] رسم خريطة رحلة العميل المحتمل (Prospect Journey)
- [ ] توثيق كل نقطة تواصل وقناة مستخدمة
- [ ] قياس أوقات الاستجابة الحالية (baseline)
- [ ] تحديد نقاط التسرب الواضحة

### Day 3 — التحليل وتحديد الفجوات
- [ ] مقارنة الوضع الحالي بـ `success_metric` من DHO
- [ ] تحديد أولى الـworkflows للتحسين
- [ ] توثيق الـbaseline لكل مقياس (بـ `evidence_level: client_data` أو `measured`)
- [ ] إعداد ملخص تحليلي

### المخرجات
- ✅ خريطة workflow موثّقة
- ✅ baseline لكل مقياس مع `evidence_level`
- ✅ `day2_3_workflow_mapping: true` في checklist

---

## Day 4-7 — أول مسودة/نموذج أولي

**الهدف:** تسليم أول workflow قابل للاختبار.

### Day 4-5 — البناء
- [ ] بناء أول workflow بناءً على `first_workflow` من DHO-XXXX
- [ ] اختبار داخلي على بيانات العميل (لا إطلاق فعلي)
- [ ] توثيق الافتراضات ومستويات الأدلة

### Day 6-7 — الاختبار وإعداد العرض
- [ ] اختبار النموذج الأولي في بيئة آمنة
- [ ] قياس النتائج الأولية (بـ `evidence_level: measured` إن أمكن)
- [ ] إعداد عرض تقديمي للعميل

### الـworkflow الأول لـ Digital Rise Agency (مرجع)
تذكير متابعة آلي + SLA رد 15 دقيقة:
- خريطة تسرب الإيراد → تحديد 12 فرصة متروكة
- تفعيل تذكير المتابعة → نسبة متابعة 43% → 61%
- `evidence_level: measured` (قُسناه أثناء التسليم)

### المخرجات
- ✅ أول workflow جاهز للمراجعة
- ✅ `first_workflow_delivered: true` في `ONB-XXXX`
- ✅ `day4_7_first_draft: true` في checklist

---

## Day 8-10 — المراجعة والتصحيح

**الهدف:** ضبط الـworkflow بناءً على ملاحظات العميل.

### Day 8 — عرض المسودة للعميل
- [ ] اجتماع مراجعة مع العميل (30-45 دقيقة)
- [ ] عرض النتائج الأولية مع `evidence_level` لكل رقم
- [ ] تسجيل ملاحظات العميل بدقة

### Day 9-10 — التصحيح والضبط
- [ ] تطبيق التصحيحات المتفق عليها
- [ ] التحقق من أن التصحيحات ضمن النطاق الأصلي (DHO-XXXX)
- [ ] أي طلب خارج النطاق → Scope Guard (لا امتصاص صامت)
- [ ] قياس مؤشرات أولية بعد التصحيح

### تحذير: Scope Guard في Day 8-10
إذا طلب العميل شيئًا خارج `scope` في DHO-XXXX:
1. وثّق الطلب كـ `scope_change_request`
2. أحله لـ Scope Guard
3. لا تنفّذه بصمت
4. انظر [`SCOPE_CONTROL_POLICY_AR.md`](./SCOPE_CONTROL_POLICY_AR.md)

### المخرجات
- ✅ workflow مُصحَّح ومعتمد من العميل
- ✅ `day8_10_review_correction: true` في checklist

---

## Day 11-14 — تقرير القيمة الأول ونقطة القبول

**الهدف:** تسليم أول `WVR-XXXX` + الحصول على قبول رسمي (`ACC-XXXX`).

### Day 11-12 — إعداد تقرير القيمة
- [ ] جمع كل المقاييس المقاسة خلال أول أسبوعين
- [ ] مقارنة كل مقياس بـ baseline (من Day 2-3)
- [ ] إعداد `WVR-XXXX` بـ `evidence_level` لكل رقم
- [ ] لا أرقام بلا `evidence_level`، لا ضمان ROI

**مثال WVR-1001 (Digital Rise Agency):**
| المقياس | Baseline | القيمة الحالية | `evidence_level` |
|---|---|---|---|
| نسبة المتابعة | 43% | 61% | `measured` |
| متوسط زمن الرد | 4.2 ساعة | 1.1 ساعة | `measured` |

### Day 13-14 — نقطة القبول الرسمي
- [ ] تسليم `WVR-XXXX` للعميل عبر البوابة الآمنة
- [ ] عرض معايير القبول (`ACC-XXXX`) على العميل
- [ ] الحصول على `accepted: true` + `accepted_by` + `accepted_at`
- [ ] توثيق أي `scope_changes_requested` لـ Scope Guard

### المخرجات
- ✅ `WVR-XXXX` مُسلَّم عبر البوابة
- ✅ `ACC-XXXX` مع `accepted: true`
- ✅ `day11_14_first_report_acceptance: true` في checklist
- ✅ `status: complete` في `ONB-XXXX`

---

## ملخص Checklist أول 14 يوم

| اليوم | الحدث | الحقل في ONB | المسؤول |
|---|---|---|---|
| Day 0 | Handoff + موافقة مؤسس | `day0_handoff` | المؤسس + Delivery Owner |
| Day 1 | صلاحيات + Intake | `day1_access_intake` | Delivery Owner + العميل |
| Day 2-3 | خريطة workflow + baseline | `day2_3_workflow_mapping` | Delivery Owner |
| Day 4-7 | أول workflow | `day4_7_first_draft` | Delivery Owner |
| Day 8-10 | مراجعة + تصحيح | `day8_10_review_correction` | Delivery Owner + العميل |
| Day 11-14 | WVR + قبول رسمي | `day11_14_first_report_acceptance` | Delivery Owner + العميل |

---

## ماذا يحدث بعد Day 14

بعد اكتمال أول 14 يوم والحصول على `ACC-XXXX`:
- ينتقل العميل إلى إيقاع نجاح العميل (انظر [`CLIENT_SUCCESS_RHYTHM_AR.md`](./CLIENT_SUCCESS_RHYTHM_AR.md))
- `WVR-XXXX` يصبح أسبوعيًا مستمرًا
- يبدأ احتساب نافذة التجديد من تاريخ البدء

---

*مرجع الحوكمة: [AGENTS.md](../../AGENTS.md)*
*السكيمة: [`schemas/client_onboarding.schema.json`](../../schemas/client_onboarding.schema.json)*
*SOP المرجعي: [`company_os/delivery/p1_delivery_sop.md`](../../company_os/delivery/p1_delivery_sop.md)*
