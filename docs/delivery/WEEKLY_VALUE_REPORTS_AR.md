# تقارير القيمة الأسبوعية (Weekly Value Reports)

> تقرير القيمة الأسبوعي يصف **قيمة فعلية مُسلَّمة وملاحَظة (observed)** خلال الأسبوع. تُسجَّل التقارير وفق
> `schemas/weekly_value_report.schema.json` وتُدار في قائمة الإصدار `reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md`.
> المرجع الموحّد للمصطلحات: `/home/user/dealix/AGENTS.md`.

الجمهور: **Delivery Operator** (يُصدر التقرير) و**العميل/الإدارة** (يقرأه).

---

## القاعدة الذهبية (اقرأها قبل أي تقرير)

```txt
╔══════════════════════════════════════════════════════════════════════╗
║  صف القيمة المُلاحَظة فقط (OBSERVED value only).                        ║
║  لا وعود. لا ضمانات. لا "سنضاعف". لا "مضمون". لا أرقام مستقبلية مؤكّدة.  ║
║  كل metric تُكتب كـ "ملاحَظ خلال الفترة" لا كنتيجة موعودة.              ║
╚══════════════════════════════════════════════════════════════════════╝
```

- ✅ صحيح: «خلال الأسبوع تمت متابعة 18 lead كانت متوقفة».
- ❌ خطأ: «سنسترجع لك 18 صفقة شهريًا» أو «نضمن زيادة التحويل».

---

## 1. القالب (Template)

الحقول مطابقة للـ schema (الإلزامي: `id`, `company`, `recommended_system`, `week_of`, `value_delivered[]`, `next_week_focus`, `acceptance_status`, `owner`):

| الحقل | النوع | الوصف |
|---|---|---|
| `id` | string | نمط `WVR-[0-9]{3,}` |
| `company` | string | اسم الشركة (synthetic في العيّنات) |
| `recommended_system` | enum | أحد الأنظمة الخمسة |
| `week_of` | string | بداية الأسبوع |
| `period` | string | الفترة المغطاة (اختياري) |
| `value_delivered[]` | array | قيمة مُلاحَظة مُسلَّمة (عنصر واحد على الأقل) |
| `metrics[]` | array | كل عنصر: `name` + `observed` + `note` (اختياري) |
| `next_week_focus` | string | تركيز الأسبوع القادم |
| `acceptance_status` | enum | `pending` / `accepted` / `changes_requested` |
| `owner` | string | المسؤول |

```txt
id:                 WVR-___
company:            ____________ (synthetic)
recommended_system: ____________
week_of:            YYYY-MM-DD
period:             YYYY-MM-DD .. YYYY-MM-DD
value_delivered:
  - ____________ (قيمة مُلاحَظة)
  - ____________
metrics:
  - name: ____ | observed: ____ | note: ____
next_week_focus:    ____________
acceptance_status:  pending | accepted | changes_requested
owner:              Delivery Operator
```

---

## 2. أمثلة "metrics observed" لكل نظام (مصاغة كملاحظات)

> كل القيم أدناه تُكتب كـ **ملاحَظ خلال الفترة**، وليست وعدًا.

### `revenue_os`
| name | observed (مثال صياغة) |
|---|---|
| فرص بلا next action | «انخفض عدد الفرص بلا next action من X إلى Y خلال الأسبوع» |
| تقرير الإيرادات | «صدر التقرير اليومي للإدارة 5 مرات» |

### `executive_command_os`
| name | observed (مثال صياغة) |
|---|---|
| قرارات يومية موثّقة | «سُجّل N قرار في Decision Log خلال الأسبوع» |
| مخاطر مرتّبة | «أُعيد ترتيب أعلى 3 مخاطر في المصفوفة» |

### `followup_recovery_os`
| name | observed (مثال صياغة) |
|---|---|
| leads تمت متابعتها | «تمت متابعة N من leads متوقفة» |
| رسائل أُرسلت في وقتها | «التزم إيقاع التذكير في M حالة» |

### `whatsapp_client_os`
| name | observed (مثال صياغة) |
|---|---|
| محادثات حُوّلت لـ flow | «صُنّفت N محادثة ضمن flows محدّدة» |
| حالات حساسة بـ handoff | «حُوّلت K حالة حساسة إلى human handoff» |

### `proposal_proof_os`
| name | observed (مثال صياغة) |
|---|---|
| عروض بصيغة موحّدة | «أُصدرت N عرض بالقالب الموحّد» |
| proof مُرفق | «أُرفقت حزمة proof في M عرض» |

---

## 3. مثال مُنفّذ بالكامل (Worked example) — `followup_recovery_os`

```txt
id:                 WVR-007
company:            شركة أفق التدريب (synthetic)
recommended_system: followup_recovery_os
week_of:            2026-06-01
period:             2026-06-01 .. 2026-06-05
value_delivered:
  - تم بناء Follow-up Queue وتشغيله على leads الأسبوع
  - أُرسلت رسائل المتابعة وفق Message Set لكل حالة
  - صدر أول Recovery Report للإدارة
metrics:
  - name: leads تمت متابعتها | observed: تمت متابعة 18 lead متوقفة | note: ملاحَظ خلال الفترة فقط
  - name: التزام إيقاع التذكير | observed: التُزم بالتذكير في 22 حالة | note: حسب Reminder Rhythm
  - name: تصعيد للحالات الحساسة | observed: حُوّلت 3 حالات إلى human handoff | note: وفق Escalation Rules
next_week_focus:    ضبط أوقات التذكير وتقليل الحالات المتأخرة
acceptance_status:  pending
owner:              Delivery Operator
```

ملاحظات على المثال:
- لا يوجد أي وعد بنتيجة مستقبلية؛ كل سطر يصف ما حدث فعلًا.
- الأرقام مذكورة كملاحظة (`observed` + `note`)، لا كضمان.
- الأسماء تركيبية (synthetic)، بلا PII ولا أرقام جوال.

---

## 4. دورة الإصدار والقبول

```txt
accepted (المخرج) → أصدر WVR (قيمة ملاحَظة) → الحالة weekly_value_report
   ├─ acceptance_status = accepted          → استمرار + مراقبة دليل القيمة
   ├─ acceptance_status = changes_requested  → عالج الملاحظات ثم أعد الإصدار
   └─ دليل قيمة/توسّع                         → renewal_candidate
```

- تُدار التقارير المستحقّة والمُصدرة في `reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md`.
- التقرير لا يُستخدم أداة بيع بوعود؛ هو إثبات قيمة ملاحَظة فقط.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
