# Dealix — تنفيذ فوري (Execute Now)

هذا الملف ترتيب تنفيذي واحد: من الأمان إلى أول دورة تشغيل كاملة. للتفاصيل التقنية للـ Sheet والفورم راجع [TURN_ON_FULL_OPS_AR.md](TURN_ON_FULL_OPS_AR.md) و [full_ops_pack/DEALIX_FULL_OPS_SETUP.md](full_ops_pack/DEALIX_FULL_OPS_SETUP.md).

---

## القرار التنفيذي

- الهدف: **Level 1 Full Ops** = عميل يدخل من الفورم أو الواتساب → صف في لوحة التشغيل → كرت تشخيص → قياس في الـ Dashboard → دليل (screenshot أو سجل).
- لا تقول «تم» بدون **Evidence** حسب [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md).

---

## المرحلة 0 — أمان

- لا إرسال واتساب بارد؛ لا أتمتة live للواتساب؛ الموافقة أولاً. راجع [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md).
- `WHATSAPP_ALLOW_LIVE_SEND=false` في Staging؛ `MOYASAR_MODE=sandbox` حتى يُعتمد الدفع الحي صراحة. راجع [RAILWAY_DEPLOY_GUIDE_AR.md](../RAILWAY_DEPLOY_GUIDE_AR.md) و [BILLING_MOYASAR_RUNBOOK.md](../BILLING_MOYASAR_RUNBOOK.md).
- لا تضع مفاتيح API أو Moyasar في الـ Sheet أو في Apps Script كنص ثابت؛ استخدم Script Properties أو إدخال يدوي آمن.

---

## المرحلة 1 — Staging

- تأكد أن الـ API يعيد `200` على `/health` وأن سكربت التحقق يمر. راجع [scripts/launch_readiness_check.py](../../scripts/launch_readiness_check.py) و [scripts/smoke_staging.py](../../scripts/smoke_staging.py).

---

## المرحلة 2 — WhatsApp inbound

- جهّز رابط `wa.me` برسالة جاهزة (مثلاً تبدأ بـ `Diagnostic`). سجّل في الـ Sheet مصدر الموافقة عند الرد اليدوي (`consent_source`).

---

## المرحلة 3 — Operating Board

- أنشئ الـ Google Sheet حسب [GOOGLE_SHEET_MODEL_AR.md](full_ops_pack/GOOGLE_SHEET_MODEL_AR.md).
- اربط Google Form بالـ Sheet؛ ثبّت Apps Script من [dealix_google_apps_script.gs](full_ops_pack/dealix_google_apps_script.gs) وشغّل `setupDealixTrigger` ثم `testInsertRow`.

---

## المرحلة 4 — First Outreach

- اتبع [FIRST_10_AGENCIES_OUTREACH_AR.md](full_ops_pack/FIRST_10_AGENCIES_OUTREACH_AR.md) و [LAUNCH_DAY_ONE_KIT.md](LAUNCH_DAY_ONE_KIT.md).

---

## المرحلة 5 — Mini Diagnostic

- بعد كل lead مؤهل: راجع `diagnostic_card`، عدّل الفرص والرسمة العربية، أرسل، حدّث `diagnostic_status`.

---

## المرحلة 6 — Pilot 499

- عرض واضح 499 ريال / 7 أيام؛ حدّث `pilot_status`؛ فاتورة يدوية عبر Moyasar عند الحاجة. راجع [MANUAL_PAYMENT_SOP.md](MANUAL_PAYMENT_SOP.md).

---

## المرحلة 7 — Proof Pack

- املأ تبويب Proof Pack أو الصف المرتبط؛ `proof_pack_status = delivered` عند التسليم.

---

## Definition of Done

- كل بند في [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md) عليه دليل (screenshot، رقم صف، مخرجات terminal، إيميل).
- Scorecard يومي: [DAILY_SCORECARD_TEMPLATE_AR.md](full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md).

---

## روابط سريعة

| الموضوع | الملف |
|--------|--------|
| أول عميل (إنجليزي تفصيلي) | [FIRST_CUSTOMER_ONBOARDING_CHECKLIST.md](FIRST_CUSTOMER_ONBOARDING_CHECKLIST.md) |
| مسار أول عميل (عربي) | [FIRST_CUSTOMER_WORKFLOW_AR.md](FIRST_CUSTOMER_WORKFLOW_AR.md) |
| تشغيل الـ Full Ops | [TURN_ON_FULL_OPS_AR.md](TURN_ON_FULL_OPS_AR.md) |
| ما بعد الإطلاق | [POST_LAUNCH_BACKLOG.md](POST_LAUNCH_BACKLOG.md) |
