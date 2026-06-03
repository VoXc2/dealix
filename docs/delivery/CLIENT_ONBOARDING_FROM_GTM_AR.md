# إعداد العميل القادم من GTM
## من صفقة مربوحة إلى عميل نشط خلال 14 يومًا

> **السكيمة المرجعية:** [`schemas/client_onboarding.schema.json`](../../schemas/client_onboarding.schema.json)
> **قالب الـIntake:** [`company_os/delivery/p1_intake_template.md`](../../company_os/delivery/p1_intake_template.md)
> **شرط البدء:** يجب اكتمال `DHO-XXXX` وموافقة المؤسس قبل فتح `ONB-XXXX`.

---

## 1. ما هو الـOnboarding

الـOnboarding هو المرحلة الانتقالية بين قبول الصفقة وبدء تسليم القيمة الفعلية. يمتد من Day 0 إلى Day 14 ويتتبع checklist محددة تضمن:
- استلام كل الصلاحيات والبيانات اللازمة
- وضوح النطاق والتوقعات للعميل
- تسليم أول workflow خلال أسبوع
- وجود أول تقرير قيمة في Day 11-14

---

## 2. الحقول الإلزامية في `client_onboarding.schema.json`

| الحقل | النوع | الوصف | مثال من ONB-1001 |
|---|---|---|---|
| `id` | string | معرّف `ONB-XXXX` | `ONB-1001` |
| `created_at` | datetime | وقت الإنشاء | `2026-06-03T16:05:00+03:00` |
| `company` | string | اسم الشركة | `Digital Rise Agency` |
| `handoff_id` | string | ربط بـ DHO-XXXX | `DHO-1001` |
| `checklist` | object | checklist أول 14 يوم | (انظر §3) |
| `status` | enum | حالة الإعداد | `in_progress` |

---

## 3. Checklist أول 14 يوم (من السكيمة)

| الحقل في الـchecklist | اليوم | ما يعنيه |
|---|---|---|
| `day0_handoff` | Day 0 | اكتمال DHO-XXXX وموافقة المؤسس |
| `day1_access_intake` | Day 1 | منح الصلاحيات + استيفاء نموذج الـIntake |
| `day2_3_workflow_mapping` | Day 2-3 | رسم خريطة الـworkflow الحالي |
| `day4_7_first_draft` | Day 4-7 | تسليم أول مسودة/نموذج أولي |
| `day8_10_review_correction` | Day 8-10 | مراجعة + تصحيح بناءً على ملاحظات العميل |
| `day11_14_first_report_acceptance` | Day 11-14 | تقرير قيمة أول + نقطة قبول رسمية |

**مثال حي — ONB-1001 (Digital Rise Agency):**
- `day0_handoff`: ✅ مكتمل
- `day1_access_intake`: ✅ مكتمل (صلاحيات ممنوحة: `read_only_crm`, `file_upload`)
- `day2_3_workflow_mapping`: ⏳ قيد التنفيذ
- `day4_7_first_draft` إلى `day11_14`: ⏳ لم تبدأ بعد

---

## 4. الحقول الاختيارية المهمة

| الحقل | الوصف | القيمة الافتراضية |
|---|---|---|
| `access_granted` | هل مُنحت الصلاحيات؟ | `false` |
| `first_workflow_delivered` | هل سُلّم أول workflow؟ | `false` |
| `owner` | مالك عملية الإعداد | — |

### قيم `status` المسموح بها

| القيمة | المعنى |
|---|---|
| `not_started` | لم يبدأ (تحذير: يجب البدء Day 0) |
| `in_progress` | جارٍ |
| `at_risk` | متأخر أو معرّض للتعثر |
| `complete` | اكتمل Day 11-14 + قبول رسمي |

---

## 5. متطلبات الـIntake (ربط بـ p1_intake_template.md)

قبل Day 1، يجب استيفاء [`company_os/delivery/p1_intake_template.md`](../../company_os/delivery/p1_intake_template.md) الذي يتضمن:

### البيانات الإلزامية (Required)
- [ ] تصدير CRM / قائمة العملاء المحتملين (آخر 90 يومًا)
- [ ] 20-50 محادثة مبيعات (مُجهَّلة قدر الإمكان)
- [ ] 2-3 عينات عروض/أسعار
- [ ] قائمة قنوات التواصل المستخدمة
- [ ] وصف عملية المتابعة الحالية
- [ ] أهم 3-5 خدمات/منتجات مباعة
- [ ] نطاق الأسعار
- [ ] أهم 5 اعتراضات يواجهها الفريق

### اتفاقية التعامل مع البيانات (PDPL)
- [ ] العميل يؤكد ملكيته للبيانات أو حقه في مشاركتها
- [ ] لا بيانات PII لعملاء العميل النهائيين
- [ ] البيانات تُحذف بعد 90 يومًا من انتهاء الخدمة
- [ ] الرؤى المُجهَّلة تستخدم في دراسات الحالة بموافقة صريحة

---

## 6. منح الصلاحيات عبر البوابة الآمنة

**الصلاحيات لا تُمنح أبدًا عبر:**
- واتساب
- البريد الإلكتروني المباشر
- أي قناة غير البوابة الآمنة

**خطوات منح الصلاحيات:**
1. تحديد الصلاحيات المطلوبة من `required_access` في DHO-XXXX
2. إنشاء رابط بوابة آمن محدود المدة
3. إرسال الرابط للعميل عبر البوابة
4. تسجيل `access_granted: true` في ONB-XXXX بعد التأكيد
5. تدقيق الصلاحيات بانتظام (أقل امتياز)

---

## 7. ما يحدث إذا تأخّر الـOnboarding

| التأخر | التصنيف | الإجراء |
|---|---|---|
| Day 1-2 متأخر | `at_risk` | إشعار فوري للمؤسس |
| بيانات ناقصة في Day 3 | `at_risk` | اجتماع طارئ مع العميل |
| Day 7 بلا access | `blocked` → `at_risk` | تصعيد للمؤسس + وقف العداد |
| Day 14 بلا قبول | مراجعة النطاق | Scope Guard يحلل السبب |

> ملاحظة: وقف العداد (pause) لا يُلغي الالتزامات؛ يُسجَّل بموافقة الطرفين.

---

## 8. العلاقة مع GTM (القادم من المبيعات)

يصل العميل إلى الـOnboarding بعد أن يكون المؤسس قد:
1. وافق على عرض السعر (PROP-XXXX) عبر `approval_queue`
2. أنشأ وأعتمد DHO-XXXX
3. تأكد من ربط `product_id` بكتالوج المنتجات

الـGTM يُسلِّم إلى التسليم عبر DHO-XXXX — **لا يوجد تسليم شفهي أو غير رسمي**.

---

## 9. ما لا يجوز في الـOnboarding

| ممنوع | السبب |
|---|---|
| طلب مفاتيح API أو كلمات مرور في واتساب | أسرار في البوابة فقط |
| تجاهل حقول `out_of_scope` من DHO | يؤدي لتضخم النطاق |
| البدء قبل `day0_handoff: true` | قاعدة لا تُكسر |
| وعد بنتائج محددة لليوم 14 | لا ضمان ROI |
| PII لعملاء العميل في أي مستند | مخالفة PDPL/SDAIA |

---

## 10. نموذج إنشاء ONB-XXXX

```json
{
  "id": "ONB-XXXX",
  "created_at": "<ISO-datetime+03:00>",
  "company": "<اسم الشركة>",
  "handoff_id": "DHO-XXXX",
  "checklist": {
    "day0_handoff": false,
    "day1_access_intake": false,
    "day2_3_workflow_mapping": false,
    "day4_7_first_draft": false,
    "day8_10_review_correction": false,
    "day11_14_first_report_acceptance": false
  },
  "access_granted": false,
  "first_workflow_delivered": false,
  "owner": "<delivery_owner من DHO>",
  "status": "not_started"
}
```

---

*مرجع الحوكمة: [AGENTS.md](../../AGENTS.md)*
*السكيمة: [`schemas/client_onboarding.schema.json`](../../schemas/client_onboarding.schema.json)*
*قالب الـIntake: [`company_os/delivery/p1_intake_template.md`](../../company_os/delivery/p1_intake_template.md)*
*بيانات حقيقية: [`data/delivery/onboarding.jsonl`](../../data/delivery/onboarding.jsonl)*
