# قواعد استهداف جهة الاتصال (Contact Targeting Rules)

> الغرض: تحديد الدور الأنسب للتواصل لكل نظام من أنظمة Dealix الخمسة، مع قواعد المصدر العام والكبت (suppression) ومنع القوائم المشتراة.

المخطط المرجعي: `schemas/contact_target.schema.json`.

## مبدأ عام

- نختار دورًا واحدًا أنسب لكل شركة، من ضمن الأدوار المسموح بها للنظام الموصى به فقط (مصدرها `ops.contact_roles` في `data/systems.json`).
- نتواصل عبر القنوات العامة المنشورة فقط (نموذج الموقع، البريد العام المعلن، رقم معلن للأعمال).
- إذا لم نجد قناة تواصل عامة، لا نخترع واحدة ولا نبحث عن بيانات خاصة — نسجّل الشركة كـ «بلا قناة عامة» ونوقف التواصل.

## خريطة الدور المسموح به لكل نظام

| النظام | المعرّف | الأدوار المسموح بها للتواصل |
|--------|---------|------------------------------|
| نظام تشغيل الإيرادات | `revenue-operating-system` | Founder / CEO، Managing Director، Head of Sales، Commercial Manager |
| نظام القيادة التنفيذية | `executive-command-os` | Founder / CEO، General Manager، Chief Operating Officer، Operations Manager |
| نظام استعادة المتابعة | `follow-up-recovery-os` | Founder / CEO، Sales Manager، Customer Experience Lead، Branch Manager |
| نظام عملاء واتساب | `whatsapp-client-os` | Founder / CEO، Operations Manager، Customer Support Lead، Bookings Manager |
| نظام العروض والإثبات | `proposal-proof-os` | Founder / CEO، Business Development Manager، Sales Director، Account Manager |

> لا يجوز إسناد دور خارج صف النظام الموصى به. مثال: لا نوجّه رسالة «نظام عملاء واتساب» إلى Head of Sales، لأنه ليس ضمن أدوار هذا النظام؛ نختار Operations Manager أو Customer Support Lead أو المؤسس.

## قاعدة المصدر العام فقط

- يُسجَّل مصدر البيانات في الحقل `source` (مثال: «موقع الشركة - صفحة من نحن»).
- مسموح: موقع الشركة، صفحات عامة، إعلان وظيفة منشور، خبر منشور، حساب أعمال عام.
- ممنوع: شراء قوائم، كشط بيانات خاصة، استخراج بيانات تواصل غير معلنة، أي أتمتة على LinkedIn (بحث آلي، رسائل آلية، طلبات اتصال آلية).

## قائمة عدم التواصل والكبت (Do-Not-Contact / Suppression)

تُضبط الحقول: `do_not_contact: true` و `suppression_reason`. أوقف التواصل فورًا في الحالات التالية:

| السبب | المعنى |
|-------|--------|
| `requested_no_contact` | الشركة طلبت عدم التواصل |
| `existing_client` | عميل حالي يُدار عبر مسار آخر |
| `competitor` | منافس مباشر |
| `no_public_channel` | لا توجد قناة تواصل عامة |
| `duplicate` | مكرر مع سجل قائم |
| `out_of_scope` | خارج النطاق (قطاع/دولة غير مستهدفين) |

- يُراجَع علم `do_not_contact` قبل أي إرسال أو مكالمة.
- لا يُعاد تفعيل أي سجل مكبوت إلا بقرار موثّق.

## قائمة تحقق قبل الاستهداف

- [ ] الشركة ضمن القطاع والدولة المستهدفين.
- [ ] النظام الموصى به محدّد ومن المعرّفات الخمسة.
- [ ] الدور المختار ضمن `ops.contact_roles` لذلك النظام.
- [ ] توجد قناة تواصل عامة موثّقة في `source`.
- [ ] `do_not_contact = false` ولا سبب كبت قائم.
- [ ] لا قوائم مشتراة، ولا بيانات خاصة، ولا أتمتة LinkedIn.
