# لوحة التشغيل بدون Apps Script — صيغ Google Sheets فقط

إذا تعذّر تشغيل Apps Script أو Triggers، يمكنك تشغيل **Level 1** بهذه الطريقة:

1. **إشعارات البريد من Google Forms** (بدون كود) — كل رد جديد يصلك إيميلاً.  
   [مساعدة Google: تفعيل إشعارات الردود](https://support.google.com/docs/answer/2917686)
2. **صيغ `ARRAYFORMULA` في `02_Operating_Board`** تسحب البيانات من `Form Responses 1` وتبني `recommended_service` و`next_step` و`diagnostic_card`.

---

## ترتيب الأعمدة الرسمي (يلزم أن يطابق الصف 1)

استخدم **نفس ترتيب الرأس** المعرّف في [GOOGLE_SHEET_MODEL_AR.md](GOOGLE_SHEET_MODEL_AR.md) (و`BOARD_COLUMN_ORDER` في `dealix_google_apps_script.gs`).

| عمود | مفتاح الرأس |
|------|-------------|
| A | `submitted_at` |
| B | `lead_name` |
| C | `company` |
| D | `website` |
| E | `sector` |
| F | `city` |
| G | `goal` |
| H | `ideal_customer` |
| I | `offer` |
| J | `contact_method` |
| K | `whatsapp_or_email` |
| L | `has_list` |
| M | `business_type` |
| N | `source` |
| O | `consent` |
| P | `consent_source` |
| Q | `meeting_status` |
| R | `diagnostic_status` |
| S | `pilot_status` |
| T | `proof_pack_status` |
| U | `recommended_service` |
| V | `next_step` |
| W | `diagnostic_card` |
| X | `owner` |
| Y | `invoice_link` |
| Z | `last_touch_at` |
| AA | `notes` |

ضع الصيغة في **الصف 2** (أول صف بيانات بعد الرأس). `ARRAYFORMULA` تمتد مع كل صف جديد في الفورم.

---

## ربط أعمدة «Form Responses 1»

Google يضع **Timestamp** في العمود **A**، ثم أسئلتك بالترتيب **B، C، D…**

قبل لصق الصيغ: افتح `Form Responses 1` وتحقق من **الصف 1** (عناوين الأعمدة) ودوّن أي حرف يقابل كل سؤال. غيّر المراجع أدناه إذا ترتيب أسئلتك يختلف عن هذا الافتراضي (نفس ترتيب [TURN_ON_FULL_OPS_AR.md](../TURN_ON_FULL_OPS_AR.md)):

| سؤال | عمود افتراضي في الردود |
|------|-------------------------|
| Timestamp | `Form Responses 1'!A2:A` |
| الاسم | `B2:B` |
| اسم الشركة | `C2:C` |
| رابط الموقع/الحساب | `D2:D` |
| القطاع | `E2:E` |
| المدينة | `F2:F` |
| الهدف | `G2:G` |
| العميل المثالي | `H2:H` |
| العرض الرئيسي | `I2:I` |
| لديك قائمة عملاء؟ | `J2:J` |
| أفضل وسيلة تواصل | `K2:K` |
| رقم واتساب | `L2:L` |
| الإيميل | `M2:M` |
| الموافقة على التواصل | `N2:N` |

في الأمثلة أدناه استخدمنا المرجع الكامل **`'Form Responses 1'!`** (مع الاقتباس لأن الاسم فيه مسافة).

---

## صيغ الصف 2 (انسخ بعد تعديل أحرف الأعمدة إن لزم)

**شرط عام:** نعتبر الصف lead إذا **اسم الشركة** غير فارغ في عمود الردود C (عدّل الحرف إذا ترتيب أسئلتك مختلف).

### A — `submitted_at`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!A2:A, ""))
```

### B — `lead_name`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!B2:B, ""))
```

### C — `company`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!C2:C, ""))
```

### D — `website`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!D2:D, ""))
```

### E — `sector`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!E2:E, ""))
```

### F — `city`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!F2:F, ""))
```

### G — `goal`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!G2:G, ""))
```

### H — `ideal_customer`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!H2:H, ""))
```

### I — `offer`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!I2:I, ""))
```

### J — `contact_method`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!K2:K, ""))
```

### K — `whatsapp_or_email`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), IF(LEN('Form Responses 1'!L2:L&""), 'Form Responses 1'!L2:L, 'Form Responses 1'!M2:M), ""))
```

### L — `has_list`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!J2:J, ""))
```

### M — `business_type`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!E2:E, ""))
```

### N — `source`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "form_inbound", ""))
```

### O — `consent`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), 'Form Responses 1'!N2:N, ""))
```

### P — `consent_source`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "form_opt_in", ""))
```

### Q — `meeting_status`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "not_booked", ""))
```

### R — `diagnostic_status`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "new", ""))
```

### S — `pilot_status`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "not_offered", ""))
```

### T — `proof_pack_status`
```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C), "not_started", ""))
```

### U — `recommended_service` (منطق اقتراح بسيط — يعتمد على قائمة العملاء والقطاع والهدف من الفورم)

```
=ARRAYFORMULA(IF(LEN('Form Responses 1'!C2:C)=0, "",
  IF('Form Responses 1'!J2:J="نعم", "Data to Revenue",
    IF(REGEXMATCH(LOWER('Form Responses 1'!E2:E&""), "وكالة|مسوق|agency"), "Agency Partner Pilot",
      IF(REGEXMATCH(LOWER('Form Responses 1'!G2:G&""), "اجتماع|meeting"), "Meeting Sprint",
        IF(REGEXMATCH(LOWER('Form Responses 1'!G2:G&""), "شراكات|partnership"), "Partnership Growth",
          IF(REGEXMATCH(LOWER('Form Responses 1'!G2:G&""), "عملاء|leads|نمو"), "Growth Starter",
            "Mini Diagnostic"))))))
```

### V — `next_step` (يعتمد على **عمود الحالة R** في نفس اللوحة، وليس على نص «new» داخل recommended)

```
=ARRAYFORMULA(IF(LEN(C2:C)=0, "",
  IF(R2:R="new", "ابدأ Mini Diagnostic خلال 24 ساعة",
    IF(R2:R="waiting_data", "اطلب البيانات الناقصة من العميل",
      IF(R2:R="in_progress", "أكمل الـ Diagnostic وأرسله",
        IF(R2:R="sent", "اعرض Pilot أو احجز اجتماع",
          "راجع الحالة"))))))
```

### W — `diagnostic_card` (قالب نصي — لا يستبدل مراجعة بشرية)

```
=ARRAYFORMULA(IF(LEN(C2:C)=0, "",
  "📊 Dealix Mini Diagnostic"&CHAR(10)&CHAR(10)&
  "الاسم: "&B2:B&CHAR(10)&
  "الشركة: "&C2:C&CHAR(10)&
  "القطاع: "&E2:E&CHAR(10)&
  "الهدف: "&G2:G&CHAR(10)&CHAR(10)&
  "1. أفضل شريحة (يُعبأ يدوياً)"&CHAR(10)&
  "2. لماذا هذه الشريحة"&CHAR(10)&
  "3. 3 فرص"&CHAR(10)&
  "4. مسودة رسالة (عربي)"&CHAR(10)&
  "5. القناة المقترحة: "&IF(REGEXMATCH(LOWER(E2:E&""),"وكالة|مسوق"),"LinkedIn يدوي + Email","WhatsApp opt-in فقط")&CHAR(10)&CHAR(10)&
  "6. مخاطرة: لا cold WhatsApp"&CHAR(10)&CHAR(10)&
  "7. الخطوة التالية: "&V2:V))
```

(في الصيغة أعلاه، `B2:B` و`C2:C`… تشير إلى **أعمدة اللوحة نفسها** في `02_Operating_Board` — صحيحة داخل `ARRAYFORMULA`.)

---

## أخطاء شائعة

| الخطأ | السبب المحتمل |
|--------|----------------|
| `#REF!` | اسم التبويب ليس `Form Responses 1` أو تمت إعادة ترتيب الأسئلة |
| `#NAME?` | لغة الصيغ ليست إنجليزية؛ استخدم `;` بدل `,` حسب إعدادات اللوحة |
| صفوف فارغة كثيرة | لا تستخدم `A2:A<>""` فقط؛ ربط الصف بعمود إلزامي مثل **اسم الشركة** |
| منطق `next_step` خاطئ | لا تضع `IF(Q5:Q="new"...)` على عمود **خدمة مقترحة**؛ استخدم عمود **`diagnostic_status` (R)** |

---

## بديل سريع: إيميل فقط (سكربت ~30 سطر)

إن احتجت إيميلاً عند كل إرسال دون صيغ معقّدة، راجع المثال المختصر في [DEALIX_FULL_OPS_SETUP.md](DEALIX_FULL_OPS_SETUP.md) أو استخدم الإشعار المدمج في الفورم أعلاه.

---

## المراجع

- [GOOGLE_SHEET_MODEL_AR.md](GOOGLE_SHEET_MODEL_AR.md) — نموذج الأعمدة الكامل  
- [TURN_ON_FULL_OPS_AR.md](../TURN_ON_FULL_OPS_AR.md) — تفعيل الفورم والربط  
- [dealix_google_apps_script.gs](dealix_google_apps_script.gs) — المسار مع Apps Script عندما يكون جاهزاً  
