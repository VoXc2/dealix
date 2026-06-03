# Sub-Processor Change Notification — Customer Email Template

> Required by PDPL DPA §5. Send 30 days before activating any new sub-processor that touches personal data.

---

## Arabic — Primary

```
الموضوع: إشعار مسبق بإضافة معالج فرعي جديد إلى منظومة Dealix

عملاءنا الكرام،

وفقًا لاتفاقية معالجة البيانات (DPA) المُبرَمة بيننا، نوجه عنايتكم بإضافة معالج
فرعي جديد إلى قائمة المعالجين الفرعيين الذين يقدمون خدماتهم لـ Dealix:

— المعالج الفرعي: {provider_name}
— الموقع: {provider_url}
— الغرض من المعالجة: {purpose}
— فئات البيانات: {data_categories}
— منطقة المعالجة: {region}
— نوع اتفاقية DPA: {dpa_type}
— تاريخ التفعيل المقرر: {go_live_date} (بعد ٣٠ يومًا من تاريخ هذا الإشعار)

تتاح لكم الفرصة، وفقًا للمادة (٥) من DPA، تقديم اعتراض معلّل خلال نافذة الـ ٣٠ يومًا
عبر البريد privacy@dealix.sa.

في حال عدم استلام اعتراض، نعتبر القائمة الجديدة سارية بعد {go_live_date}.

القائمة المحدّثة متاحة دائمًا على:
https://dealix.sa/sub-processors.html

شكرًا لثقتكم،
DPO Dealix
privacy@dealix.sa
```

## English — Secondary

```
Subject: 30-day notice — new sub-processor added to Dealix

Dear customer,

Per our Data Processing Agreement (DPA §5), we are giving you 30 days' notice
of a new sub-processor:

— Sub-processor: {provider_name}
— Website: {provider_url}
— Processing purpose: {purpose}
— Data categories: {data_categories}
— Processing region: {region}
— DPA type: {dpa_type}
— Planned activation: {go_live_date} (30 days from this notice)

Under DPA §5, you may submit a reasoned objection within this 30-day window
to privacy@dealix.sa. If no objection is received, the updated list takes
effect on {go_live_date}.

The live list is at:
https://dealix.sa/sub-processors.html

Thank you,
DPO, Dealix
privacy@dealix.sa
```

---

## Operational checklist before sending

- [ ] Update `landing/sub-processors.html` in a PR but do NOT merge to main until notice goes out (or use a `not-yet-active` flag in the table)
- [ ] Confirm DPA + GDPR/PDPL terms with new sub-processor are signed
- [ ] Schedule send: T-30 days before `go_live_date`
- [ ] Track recipients in `docs/legal/sub_processor_notifications.md`
- [ ] If any customer objects: open conversation, document outcome, may require alternative provider

## Notification log

`docs/legal/sub_processor_notifications.md` keeps the log:

```
| date | provider | purpose | go_live | customers_notified | objections | resolution |
```
