# Dealix — تشغيل Full Ops Level 1 (عربي)

خطوات تشغيل النظام اليدوي حول Google Workspace: Sheet + Form + Apps Script + اختبارات + لوحة قياس.

---

## رفع Excel إلى Google Sheets (إن وُجد)

- أنشئ Spreadsheet جديد أو استورد الملف.
- طبّق أسماء التبويبات والأعمدة من [GOOGLE_SHEET_MODEL_AR.md](full_ops_pack/GOOGLE_SHEET_MODEL_AR.md).

---

## إنشاء Google Form

- **12 سؤالاً تقريباً** + حقل **موافقة إلزامي** (نعم/لا).
- اربط الردود بالـ Sheet: Responses → Link to Sheets (راجع مساعدة Google الرسمية للفورم).
- اسم تبويب الردود الافتراضي غالباً: `Form Responses 1` — يجب أن يطابق `FORM_RESPONSES_SHEET` في السكربت.

---

## ربط Form بالـ Sheet

- تأكد أن كل إرسال يظهر صفاً جديداً في `Form Responses 1` قبل تفعيل السكربت.

---

## بدون Apps Script — صيغ فقط + إيميل الفورم

إذا تعذّر **Run** أو **Triggers** في Apps Script:

1. في Google Form: **Responses** → ⋮ → **Get email notifications for new responses** ([مساعدة Google](https://support.google.com/docs/answer/2917686)).
2. في `02_Operating_Board` استخدم صيغ `ARRAYFORMULA` المنسوخة من [OPERATING_BOARD_FORMULAS_ONLY_AR.md](full_ops_pack/OPERATING_BOARD_FORMULAS_ONLY_AR.md) (مع تعديل أحرف أعمدة `Form Responses 1` إذا ترتيب أسئلتك يختلف).

---

## تركيب Apps Script

- Extensions → Apps Script → الصق محتوى [dealix_google_apps_script.gs](full_ops_pack/dealix_google_apps_script.gs).
- عدّل `OWNER_EMAIL` و `WHATSAPP_LINK` و `OPERATING_BOARD_SHEET` إن لزم (أو استخدم Script Properties لاحقاً).
- **لا** تخزن Moyasar أو مفاتيح API في الملف.

---

## تشغيل Trigger

- من المحرر: شغّل `setupDealixTrigger()` مرة واحدة ووافق على الصلاحيات.
- يجب أن يُنشأ trigger من نوع From spreadsheet → On form submit → الدالة `onDealixFormSubmit` (أو الاسم الذي عرّفته في السكربت).

---

## اختبار testInsertRow

- Run → `testInsertRow` → تحقق من صف جديد في `02_Operating_Board` مع `diagnostic_card` و `recommended_service` و `next_step` غير فارغة.

---

## اختبار Form Submit

- أرسل رداً تجريبياً من الفورم؛ راقب Executions في Apps Script وصفاً جديداً في اللوحة وإيميل المالك (إن فُعّل `sendOwnerAlert_`).

---

## فحص Dashboard

- حدّث حالات صف تجريبي (`diagnostic_status`, `pilot_status`, `proof_pack_status`) وتأكد أن صيغ `07_Dashboard` تتغير. راجع نموذج الأعمدة في [GOOGLE_SHEET_MODEL_AR.md](full_ops_pack/GOOGLE_SHEET_MODEL_AR.md).

---

## إطلاق أول 10 رسائل

- [FIRST_10_AGENCIES_OUTREACH_AR.md](full_ops_pack/FIRST_10_AGENCIES_OUTREACH_AR.md)

---

## Troubleshooting

| العرض | التصرف |
|--------|--------|
| الرد في الفورم فقط ولا يظهر في اللوحة | راجع Trigger والدالة المرتبطة؛ نفّذ `testInsertRow` للعزل. |
| صف بدون `consent` | اجعل سؤال الموافقة required في الفورم. |
| أعمدة لا تُملأ | طابق ترتيب/عناوين الأعمدة في `appendToOperatingBoard_` مع الصف الأول في اللوحة. |
| إيميل لا يصل | افحص quota Gmail؛ جرّب `OWNER_EMAIL` صحيح؛ راجع سجل التنفيذ. |

---

## المراجع

- [DEALIX_FULL_OPS_SETUP.md](full_ops_pack/DEALIX_FULL_OPS_SETUP.md) (إنجليزي مختلط تقنياً حيث يلزم)
- [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md)
- [RAILWAY_DEPLOY_GUIDE_AR.md](../RAILWAY_DEPLOY_GUIDE_AR.md) للـ API staging
