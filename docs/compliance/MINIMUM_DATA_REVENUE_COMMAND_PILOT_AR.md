# Dealix — Minimum-Data Revenue Command Pilot

**الحالة:** Technical product boundary only  
**ليس:** DPA، رأيًا قانونيًا، قرار PDPL نهائيًا، أو إذنًا عامًا بمعالجة بيانات شخصية.  
**الهدف:** إتاحة أول Pilot حقيقي لشركة حقيقية بأقل Data risk ممكن، بينما تظل بوابة الخصوصية الأوسع #918 مفتوحة.

## القرار

أول Revenue Command Pilot يمكن تضييقه إلى **Non-personal / minimum-data profile** بدل استيراد CRM أو Inbox أو Contacts كاملًا.

المسار:

```text
Named customer
→ approved opaque company / ICP / workflow references
→ pseudonymous opportunity IDs
→ aggregate numeric baseline metrics
→ internal priorities/actions
→ human approval queue
→ aggregate Proof Pack
→ final outcome review
```

لا يُستخدم هذا Profile إذا كانت قيمة الـPilot تعتمد على أسماء أشخاص، رسائلهم، إيميلاتهم، أرقامهم، transcripts، ملفات شخصية، بيانات دفع، أو أي فئة شخصية/حساسة.

## الحد التنفيذي للـdataset

الـJSON الذي يمر عبر `MinimumDataPilotDataset` **لا يحمل arbitrary free text**. يحمل فقط:

- `tenant_id` و`company_id` كمعرفات opaque/pseudonymous.
- `company_context_source_ref` كمرجع opaque لمصدر context تمت مراجعته خارج الـdataset.
- `icp_id` و`workflow_id` كمعرفات opaque.
- `acceptance_criteria_ref` و`approval_policy_ref` و`proof_target_id` كمراجع opaque.
- `accountable_owner_role` كدور، لا اسم شخص.
- Aggregate metrics رقمية مع `metric_definition_ref` و`measurement_window_ref` و`source_ref`.
- Pseudonymous opportunities بحالة/مرحلة/عمر/value band ودور مالك، دون أسماء أو ملاحظات.

### Company facts / operating context

الاسم العام للشركة، القطاع، الموقع العام، الخدمات، ICP description، workflow description، acceptance criteria أو أي context غني **لا يُنسخ كنص داخل minimum-data dataset**. هذا المحتوى يبقى خلف `company_context_source_ref`/المراجع الأخرى، ولا يصبح مصدرًا مؤهلًا لهذا المسار إلا بعد التحقق أنه لا يحتوي Personal/Sensitive Data وأن provenance الخاص به معروف.

هذا الفصل مقصود: الـtyped gate ليس PII detector ولا يجوز أن يدّعي اكتشاف كل اسم شخص داخل free text.

## Pseudonymous opportunities

مثال مسموح:

```text
OPP-017
stage = proposal
age_days = 19
value_band = medium
next_action_status = missing
owner_role = sales_manager
source_ref = source_customer_aggregate_001
```

غير مسموح داخل الـdataset:

```text
Ahmed Al-...
ahmed@...
+966...
LinkedIn URL
meeting notes
email body
```

## Aggregate metrics

المسموح هو رقم Aggregate + مراجع opaque، مثل:

- Count of opportunities without Next Action.
- Median stage age.
- First-response duration على مستوى Aggregate.
- Follow-up coverage rate.
- Count/rate of overdue approvals.

مثال:

```text
metric_id = metric_next_action_coverage
metric_definition_ref = metric_definition_next_action_coverage
value = 62.0
unit = percent
source_ref = source_customer_aggregate_001
measurement_window_ref = window_previous_30_days
```

لا يوجد `metric_name` أو `measurement_window` حر داخل الـtyped dataset.

## ما هو ممنوع

- Contact names/emails/phones/WhatsApp/LinkedIn profiles.
- Arbitrary company/customer free-text notes داخل الـminimum-data JSON.
- Message bodies أو Inbox exports.
- Meeting transcripts/recordings.
- Raw CRM export.
- IDs وطنية/إقامة/جواز.
- HR أو health data.
- Payment/bank/card data.
- Customer files تحتوي بيانات شخصية.
- Secrets/credentials/tokens.
- Prompts تحتوي Personal Data.

إذا ظهر محتوى شخصي أو حساس بشكل غير متوقع في dataset أو في source يراد اعتماده: **Reject/Quarantine** ولا يُستخدم في التحليل.

## المخرجات المسموحة

- Candidate Company Brain facts غير شخصية ومصدرها مقيد.
- Pseudonymous opportunity prioritization.
- Internal next-best-actions.
- Approval queue items.
- Daily/weekly executive command.
- Aggregate weekly Proof Pack.
- Final outcome review.
- Learning proposal.

## ما يبقى ممنوعًا

- Customer-facing auto-send.
- Named-person outreach generated from imported contacts.
- Invoice/Payment request.
- Live charge.
- Production mutation.
- Legal/compliance conclusion.
- Public customer/result claim.

## Definition of Start

حتى هذا الـprofile لا يفتح Pilot تلقائيًا. يجب أن يوجد:

1. Named-customer scope approved.
2. قبول صريح لهذا Profile للـdataset المحدد.
3. تأكيد أن Workflow لا يحتاج Personal/Sensitive Data.
4. Exact dataset ينجح في `validate_minimum_data_pilot_dataset.py`.
5. Baseline + Proof path محددان.
6. Delivery owner + Approval owner محددان.
7. Production/Tenant controls المطلوبة لهذا Workflow خضراء.

## متى نوسّع Data scope؟

فقط إذا أصبح Personal Data ضروريًا للقيمة، وبعد إغلاق المتطلبات الأوسع للحالة المحددة، ومنها حسب النطاق:

- Data-flow register.
- accountable privacy/legal decisions where required.
- systems/subprocessors/regions.
- tenant isolation.
- durable suppression/consent.
- retention/deletion/export.
- incident ownership/drills.
- customer-specific terms matching actual processing.

## Proof posture

- Synthetic evidence = never customer proof.
- Dealix-on-Dealix evidence = internal only unless separately valid for publication.
- Minimum-data customer evidence = usable only when same-company and source-bound.
- Public case study/logo/result = separate written permission.

## Canonical machine-readable profile

`dealix/config/minimum_data_pilot_profile.yaml`

Verifier:

```bash
python scripts/verify_minimum_data_pilot_profile.py
```

Exact dataset validation without import/persistence:

```bash
python scripts/validate_minimum_data_pilot_dataset.py <dataset.json>
```

Regression:

```bash
pytest -q tests/test_minimum_data_pilot_profile.py tests/test_minimum_data_pilot_dataset.py tests/test_minimum_data_pilot_id_safety.py tests/test_minimum_data_pilot_example.py
```

هذا الـProfile يضيّق مخاطر أول Pilot؛ لا يقرر أن PDPL أو أي نظام آخر غير منطبق، ولا يغلق #918 بمفرده.
