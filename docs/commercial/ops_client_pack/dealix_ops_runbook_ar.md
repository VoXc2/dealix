# Dealix — Revenue Command Pilot Runbook

> **Internal review only.** هذا الملف يجهز Discovery وScope وProof؛ لا يرسل عرضًا، لا يصدر Quote/Invoice/Payment request، ولا يمنح صلاحية تواصل أو نشر.

## الهدف
تحويل مشكلة إيرادية/تشغيلية واحدة إلى **Revenue Command Pilot** بنطاق ومدة ومعايير قبول خاصة بالعميل، ثم اتخاذ قرار `STOP / EXPAND / REDESIGN` من الأدلة.

## المنتج والمسار المعتمد

**Dealix — Saudi-first AI Business Operating System**

أول wedge: **Revenue + Proof + Command**

```text
Free Mini Diagnostic
→ qualified discovery
→ customer-specific quote بعد الموافقة
→ Revenue Command Pilot بنطاق ومدة ومعايير قبول خاصة بالعميل
→ weekly + final Proof
→ STOP / EXPAND / REDESIGN
```

لا يوجد public fixed price، ولا package ladder، ولا self-serve checkout، ولا Diagnostic مدفوع مستقل كسلطة إطلاق حالية.

## الحزمة التي تُجهز داخليًا
1. Company/problem hypothesis — بيانات شركة وتشغيل فقط قدر الإمكان.
2. Discovery brief — المشكلة، owner، baseline، source، urgency، budget/timing.
3. Pilot scope — **one ICP + one revenue workflow**.
4. Approved data boundary — أقل بيانات وصلاحيات لازمة.
5. Approval path — من يوافق على أي إجراء حساس أو خارجي.
6. Acceptance criteria — كيف نعرف أن النطاق سُلّم كما اتفقنا.
7. Weekly Proof Pack + weekly executive readout.
8. Final Proof Pack + outcome review.
9. Customer-specific quote shell — يظل `TBD` حتى qualified discovery والموافقة.

## Discovery

اسأل فقط ما يلزم لتحديد نطاق قابل للقياس:

- ما المشكلة المحددة؟
- أين يحدث التسرب أو التأخير أو الغموض؟
- من يملك العملية ومن يملك قرار الـPilot؟
- ما baseline وما مصدره؟
- ما البيانات الدنيا المطلوبة؟
- ما الإجراءات التي يجب أن تبقى خلف موافقة؟
- ما acceptance criteria؟
- ما سبب التوقيت الآن؟
- هل توجد ميزانية وتوقيت واقعيان إذا أثبت التشخيص أن Pilot مناسب؟

**لا تُعد المحادثة Qualified** إذا لم يوجد pain محدد + owner + data/proof path + approval willingness + budget/timing discussion.

## Scope المقترح

**Revenue Command Pilot — نطاق ومدة ومعايير قبول خاصة بالعميل**

- Workflow واحد فقط.
- Baseline + first-party source، أو Missing-evidence state صريح.
- Accountable delivery owner.
- Approved data boundary.
- Approval path.
- Acceptance criteria.
- Measured operating target؛ ليس guaranteed revenue/ROI.
- Weekly Proof Pack.
- Weekly executive readout.
- Final Proof Pack.
- Final `STOP / EXPAND / REDESIGN` decision.

## السعر والدفع

- السعر **customer-specific quote after qualified discovery** فقط.
- لا يخرج رقم عام أو Price band من هذا Runbook.
- قبل اعتماد Quote: راجع scope + margin + capacity + approvals + data/production blockers.
- هذا Runbook لا يصدر Invoice أو Payment request ولا ينشئ Revenue state.
- طريقة الدفع والجهة المصدرة والشروط والضرائب/الفوترة تحدد للحالة المعتمدة فقط.
- Quote أو invoice intent أو payment link أو verbal interest ليست Revenue.
- Revenue يحتاج `payment_received` حقيقيًا ومصالحة same-company حيث ينطبق.

## Proof

افصل الحالات دائمًا:

```text
Activity
≠ Delivery
≠ Payment
≠ Revenue
≠ Customer Value
≠ Publication Permission
```

- Synthetic/demo/internal/stale/unsynced evidence لا يتحول إلى Customer Proof.
- Missing evidence يبقى `UNKNOWN / BLOCKED`.
- أي Case Study/Logo/Testimonial يحتاج publication consent منفصلًا.

## حدود التنفيذ

- لا customer-facing auto-send.
- لا cold WhatsApp.
- لا mass LinkedIn automation.
- لا scraping مخالف.
- لا live checkout/charge من هذا المسار.
- لا ضمان Revenue/ROI/Conversion.
- لا Compliance/Residency/Certification claim بلا دليل واعتماد مناسب.
- لا بيانات حساسة أو Secrets في GitHub/Proof/Client Pack.
- أي Production/DNS/Secret/DB mutation يحتاج موافقة مستقلة.

## Minimum-data first Pilot

الأفضل في أول Pilot استخدام:

- public/non-personal company facts؛
- opaque company/workflow IDs؛
- pseudonymous opportunity IDs؛
- stage/age/value bands؛
- aggregate baseline metrics؛
- role-level approval metadata؛
- non-personal proof/run metadata.

إذا احتاج النطاق personal/sensitive data، توقف ومرّر الحالة عبر privacy/tenant/retention/deletion/suppression/transfer/security/customer-terms gates المناسبة قبل توسيع البيانات.

## Definition of Done

```text
[ ] qualified_discovery_complete
[ ] one_workflow_scope_approved
[ ] baseline_and_source_or_missing_evidence
[ ] approved_data_boundary
[ ] approval_path_defined
[ ] acceptance_criteria_defined
[ ] customer_specific_quote_approved
[ ] start/payment condition approved for this customer
[ ] proof_cadence_defined_in_approved_scope
[ ] executive_readout_cadence_defined_in_approved_scope
[ ] final_proof_pack_delivered
[ ] outcome_review_stop_expand_or_redesign
[ ] real-source CRM/KPI sync where applicable
```

## قرار الإغلاق

لا توسّع تلقائي. بعد Final Proof Pack:

- **STOP** إذا لا توجد قيمة قابلة للإثبات أو المخاطر أعلى من القيمة.
- **EXPAND** إذا الدليل يبرر نطاقًا جديدًا معتمدًا.
- **REDESIGN** إذا المشكلة صحيحة لكن النطاق/البيانات/التنفيذ يحتاج إعادة تصميم.

هذا الـRunbook هو دليل تشغيل داخلي. أي نسخة Customer-facing تحتاج مراجعة واعتمادًا خاصًا بالعميل قبل المشاركة.
