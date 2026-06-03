# Post-launch backlog — Dealix Level 1+

بنود تُؤجَّل عن التشغيل اليدوي الأول. كل بند فيه **Blocked until** لتجنب البناء قبل الأدلة.

---

## B1 — WhatsApp Cloud API inbound

- ربط ويب هوك، قوالب Meta، نافذة خدمة 24 ساعة، موافقات الإرسال.
- **Blocked until:** Level 1 يعمل يدوياً + سياسة موافقات موقعة + `WHATSAPP_ALLOW_LIVE_SEND` واضح لكل بيئة.

---

## B2 — Dealix API integration

- إنشاء lead من الفورم عبر API بدلاً من أو بالتوازي مع Sheet.
- **Blocked until:** عقد الحدث والحقول في الـ API مستقر؛ staging يمر smoke كاملاً.

---

## B3 — Proof Pack generator

- توليد PDF/Doc من بيانات اللوحة تلقائياً.
- **Blocked until:** قالب Proof ثابت + مراجعة قانونية للعبارات (لا مبالغة في الوعود).

---

## B4 — CRM

- مزامنة HubSpot/Pipedrive أو جدول موحد.
- **Blocked until:** تعريف مراحل الصفقة ومصدر الحقيقة (Sheet vs CRM).

---

## B5 — Billing automation

- فواتير Moyasar عبر API بدون يدوي.
- **Blocked until:** `MOYASAR_MODE` production + مفاتيح في secrets فقط + webhook موقّع ومختبر.

---

## B6 — Partner dashboard

- لوحة للوكالات الشركاء.
- **Blocked until:** هوية وصلاحيات + بيانات تجريبية معزولة.

---

## External references (repo)

- [INTEGRATIONS_NEEDED.md](INTEGRATIONS_NEEDED.md)
- [PRODUCT_ROADMAP.md](../PRODUCT_ROADMAP.md)
- [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md)
