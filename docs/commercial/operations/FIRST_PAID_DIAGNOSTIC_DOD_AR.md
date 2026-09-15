# DoD — أول Revenue Command Pilot مدفوع + Proof Pack

> **اسم الملف Legacy للتوافق فقط.** السلطة التجارية الحالية ليست Paid Diagnostic ولا Sprint قصير. المسار المعتمد هو: Free Execution Diagnostic → qualified discovery → customer-specific quote/intervention → Revenue Command Pilot بنطاق ومدة يحددان حسب الحالة → source-backed Proof → stop / expand / redesign.

**مرجع السلطة:** `dealix/config/first_launch_offer_gate.yaml` + `COMMERCIAL_IDENTITY.md`

---

## Definition of Done — كل البنود إلزامية

### قبل العرض/الدفع

- [ ] Free Mini Diagnostic أو Discovery موثق بما يكفي لفهم المشكلة المحددة.
- [ ] ICP الحالي مناسب، والمشكلة مؤلمة ومحددة، ويوجد accountable decision owner.
- [ ] نطاق واحد فقط: **one ICP + one revenue workflow**؛ لا تحول شامل ولا قائمة باقات.
- [ ] baseline أولي ومصدره أو Missing-evidence report صريح.
- [ ] accountable delivery owner محدد.
- [ ] approved data boundary محددة؛ أقل بيانات ممكنة، ولا بيانات محظورة أو غير مصرّح بها.
- [ ] approval path وacceptance criteria موثقان قبل التنفيذ.
- [ ] target تشغيلي قابل للقياس، وليس ضمان إيراد أو ROI.
- [ ] customer-specific quote معتمد؛ لا يوجد public fixed price أو self-serve checkout.
- [ ] margin floor review + tax/e-invoicing review عند انطباقها.
- [ ] لا Quote أو Invoice/Payment request إذا كان production/privacy/tenant/payment blocker يتعارض مع نطاق العميل.

### عند الإغلاق المالي

- [ ] customer acceptance evidence لنفس الشركة والنطاق المعتمد.
- [ ] `invoice_sent` أو payment-request evidence لا يسجل إلا بعد اعتماد الجهة المُصدرة وطريقة الدفع والشروط للحالة المحددة.
- [ ] `payment_received` لا يسجل إلا من دليل استلام حقيقي، مع same-company reconciliation وعدم التكرار.
- [ ] Quote أو invoice intent أو Payment link أو verbal interest **ليست Revenue**.
- [ ] لا أسرار أو IBAN أو بيانات بنكية أو PII غير ضروري في GitHub أو Proof عام.

### التسليم — نطاق ومدة مخصصان حسب الحالة

- [ ] Kickoff يثبت: scope + baseline + data boundary + owners + approval path + acceptance criteria + stop conditions.
- [ ] Workflow واحد فقط هو محور الـPilot.
- [ ] كل finding/action يحمل source أو `missing/unknown` صريح.
- [ ] أي إجراء حساس أو خارجي يبقى داخل Approval Center/البوابة المناسبة؛ لا customer-facing auto-send.
- [ ] Weekly Proof Pack كل أسبوع.
- [ ] Weekly executive readout كل أسبوع.
- [ ] final Proof Pack في نهاية الـPilot.
- [ ] final outcome review يميز Delivery عن Payment وRevenue وCustomer Value وPublication Permission.
- [ ] `proof_pack_delivered` يسجل فقط بعد التسليم الفعلي لنفس الشركة.

### بعد التسليم

- [ ] القرار النهائي موثق: `STOP` أو `EXPAND` أو `REDESIGN`.
- [ ] أي expansion مبني على Proof مقبول، وليس على توقعات غير مثبتة.
- [ ] تحديث KPI/CRM من المصدر الفعلي؛ لا أرقام مخترعة أو synthetic/customer-like evidence.
- [ ] أي Case Study/Testimonial/Logo يحتاج publication consent منفصلًا.

---

## عرض الدخول الحالي

| المرحلة | السلطة الحالية |
|---|---|
| Entry | Free Mini Diagnostic — minimum-data، بدون دفع أو Lead persistence من الصفحة العامة |
| Qualification | Qualified discovery + first-launch gate |
| Paid motion | Revenue Command Pilot — **النطاق والمدة حسب الحالة بعد Discovery** |
| Price | **Customer-specific quote فقط بعد Discovery والموافقة** |
| Expansion | فقط بعد source-backed Proof وقرار stop / expand / redesign |

لا توجد أسعار عامة ثابتة، ولا package ladder عامة، ولا Sprint قصير كسلطة إطلاق حالية.

---

## ممنوعات قبل الإغلاق

- لا أرقام CRM أو Customer Value مخترعة.
- لا cold WhatsApp / LinkedIn automation / scraping مخالف.
- لا Revenue قبل `payment_received` الموثق والمصالح لنفس الشركة.
- لا Proof مزيّف أو KPI بلا source.
- لا guaranteed revenue/ROI.
- لا public customer proof بدون publication consent.
- لا live checkout/charge قبل إغلاق بوابته المستقلة.

---

## قائمة تحقق سريعة — نسخة لكل Pilot

```text
[ ] qualified_discovery_complete
[ ] one_workflow_scope_approved
[ ] baseline_and_source_or_missing_evidence
[ ] approved_data_boundary
[ ] approval_path_defined
[ ] acceptance_criteria_defined
[ ] customer_specific_quote_approved
[ ] customer_acceptance_evidence
[ ] authorized_invoice_or_payment_request_issued_if_applicable
[ ] payment_received_reconciled_if_required_to_start
[ ] weekly_proof_pack_x4
[ ] weekly_executive_readout_x4
[ ] final_proof_pack_delivered
[ ] outcome_review_stop_expand_or_redesign
[ ] crm_kpi_synced_from_real_source
```
