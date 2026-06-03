# تسليم المبيعات إلى التسليم (Sales → Delivery Handoff)
## كل صفقة مربوحة تنتج Delivery Handoff — بلا استثناء

> **السكيمة المرجعية:** [`schemas/delivery_handoff.schema.json`](../../schemas/delivery_handoff.schema.json)
> **مبدأ أساسي:** صفقة Won بلا `DHO-XXXX` مكتملة = عملية تسليم غير صالحة ولا تبدأ.

---

## 1. لماذا الـHandoff إلزامي

عندما تُغلق صفقة، يعرف فريق المبيعات أشياء لا يعرفها فريق التسليم:
- ما الذي وعد به العميل بالضبط
- ما الذي يقلق العميل
- ما الذي تفاوض عليه وما الذي رُفض
- السياق البشري والعلاقاتي

بدون نقل منظّم لهذه المعلومات، يبدأ التسليم بفجوة توقعات خطيرة.

---

## 2. متى يُنشأ الـHandoff

| الحدث | الإجراء | التوقيت |
|---|---|---|
| موافقة العميل على العرض | إنشاء `DHO-XXXX` فورًا | Day 0 |
| تعبئة كل الحقول الإلزامية | مراجعة المؤسس والموافقة | Day 0 |
| اكتمال الـHandoff | ينتقل لـ `ONB-XXXX` | Day 0-1 |

---

## 3. الحقول الإلزامية في `delivery_handoff.schema.json`

| الحقل | النوع | الوصف | مثال من DHO-1001 |
|---|---|---|---|
| `id` | string | معرّف فريد `DHO-XXXX` | `DHO-1001` |
| `created_at` | datetime | وقت الإنشاء (ISO 8601 +03:00) | `2026-06-03T16:00:00+03:00` |
| `company` | string | اسم شركة العميل | `Digital Rise Agency` |
| `product_id` | string | معرّف المنتج من الكتالوج | `revenue_leakage_diagnostic` |
| `scope` | array | قائمة ما هو ضمن النطاق | `["خريطة تسرب الإيراد","تدقيق المتابعة","Proof Pack","خطة 30 يوم"]` |
| `out_of_scope` | array | قائمة ما هو خارج النطاق | `["إدارة الإعلانات","كتابة المحتوى"]` |
| `success_metric` | string | مقياس النجاح الرئيسي | `"رفع نسبة المتابعة من 43% إلى 80%+"` |
| `required_access` | array | الصلاحيات المطلوبة | `["read_only_crm","file_upload"]` |
| `first_workflow` | string | أول workflow يُسلَّم | `"تذكير متابعة آلي + SLA رد 15 دقيقة"` |
| `delivery_owner` | string | المسؤول عن التسليم | `"founder"` |
| `timeline` | string | الجدول الزمني | `"5 أيام عمل"` |
| `risks` | array | المخاطر المحددة | `["التزام الفريق بالـSLA"]` |
| `weekly_value_report_template` | string | مرجع قالب WVR | `"reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md"` |

---

## 4. الحقول الاختيارية المهمة

| الحقل | الوصف | متى يُملأ |
|---|---|---|
| `proposal_id` | ربط بعرض المبيعات | دائمًا إن وجد (PROP-XXXX) |
| `client_profile` | وصف موجز للعميل وسياقه | دائمًا |
| `next_meeting` | موعد الاجتماع التالي | عند التحديد |
| `status` | حالة الـhandoff | تُحدَّث مستمرًا |

### قيم `status` المسموح بها

| القيمة | المعنى |
|---|---|
| `created` | أُنشئ، بانتظار موافقة |
| `accepted` | قبله فريق التسليم |
| `in_delivery` | التسليم جارٍ |
| `blocked` | متوقف بسبب عائق |
| `completed` | اكتمل التسليم والقبول |

---

## 5. قيم `required_access` المسموح بها

الصلاحيات تُمنح **حصرًا عبر البوابة الآمنة** وبمبدأ أقل امتياز:

| القيمة | ما تعنيه |
|---|---|
| `read_only_crm` | قراءة CRM فقط، لا كتابة |
| `read_only_sheet` | قراءة جداول البيانات |
| `read_only_inbox` | مراجعة الرسائل فقط |
| `file_upload` | رفع ملفات عبر البوابة |
| `report_view` | عرض التقارير |

> أي صلاحية غير مدرجة تتطلب موافقة مؤسس جديدة وتسجيل في `ai_action_ledger`.

---

## 6. خطوات إنشاء الـHandoff

```
1. [L4] المبيعات تجهّز مسودة DHO-XXXX بكل الحقول الإلزامية
2. [L4] المؤسس يراجع ويوافق (approved_by + approved_at)
3. [L3] Delivery Owner يقبل الـhandoff ويُحدّث status → "accepted"
4. [L4] منح صلاحيات الوصول عبر البوابة (أقل امتياز)
5. [L3] إنشاء ONB-XXXX مرتبط بـ DHO-XXXX
6. تسجيل كل خطوة في ai_action_ledger
```

---

## 7. فحص اكتمال الـHandoff (Checklist)

قبل بدء التسليم، تحقق من:

- [ ] `id` يتطابق مع نمط `DHO-XXXX`
- [ ] `product_id` موجود في كتالوج المنتجات
- [ ] `scope` مكتوب بوضوح (قائمة ≥ 1 عنصر)
- [ ] `out_of_scope` محدد (يمنع تضخم النطاق)
- [ ] `success_metric` محدد وقابل للقياس
- [ ] `required_access` لا يتجاوز الحد الأدنى الضروري
- [ ] `first_workflow` محدد
- [ ] `delivery_owner` مسمّى
- [ ] `risks` موثّقة
- [ ] `weekly_value_report_template` مرتبط
- [ ] موافقة المؤسس مسجّلة

---

## 8. ما لا يجوز في الـHandoff

| ممنوع | البديل الصحيح |
|---|---|
| وعود ROI بأرقام مضمونة | `success_metric` بهدف + `evidence_level` |
| أسرار/مفاتيح API في الحقول | `secret_ref: portal://...` |
| صلاحيات غير محددة في قائمة `required_access` | حصر الصلاحيات المطلوبة فقط |
| نطاق مبهم بلا حدود | `scope` + `out_of_scope` واضحان |
| handoff بلا موافقة المؤسس | approval إلزامي قبل البدء |

---

## 9. ربط الـHandoff بالسجلات المجاورة

```
PROP-1002 (عرض مقبول)
    └── DHO-1001 (handoff)
            └── ONB-1001 (إعداد العميل)
                    └── WVR-1001 (تقرير القيمة الأسبوعي)
                            └── ACC-1001 (قبول رسمي)
```

---

## 10. أمثلة على بيانات حقيقية

**DHO-1001 — Digital Rise Agency**
- `proposal_id`: PROP-1002
- `product_id`: `revenue_leakage_diagnostic`
- `scope`: خريطة تسرب الإيراد، تدقيق المتابعة، Proof Pack، خطة 30 يوم
- `out_of_scope`: إدارة الإعلانات، كتابة المحتوى
- `success_metric`: رفع نسبة المتابعة من 43% إلى 80%+ (هدف)
- `required_access`: `read_only_crm`, `file_upload`
- `status`: `in_delivery`

> ملاحظة: الـ80% هدف بـ`assumption`/`benchmark`، ليس ضمانًا. الرقم الفعلي المُقاس (61%) يحمل `evidence_level: measured` في WVR-1001.

---

*مرجع الحوكمة: [AGENTS.md](../../AGENTS.md)*
*السكيمة: [`schemas/delivery_handoff.schema.json`](../../schemas/delivery_handoff.schema.json)*
*بيانات حقيقية: [`data/delivery/handoffs.jsonl`](../../data/delivery/handoffs.jsonl)*
