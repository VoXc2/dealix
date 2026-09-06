# Dealix Operating Company Contract (Governed Acceleration)

هذا المستند يربط الرؤية التشغيلية الكبرى بعقد تنفيذي داخل الكود بدل بقائها كنص نظري فقط.

المراجع البرمجية:

- `auto_client_acquisition/orchestrator/operating_company_contract.py`
- `auto_client_acquisition/orchestrator/policies.py`
- `scripts/verify_operating_company_commercial_state.py`

## المعادلة التشغيلية

Dealix = **AI Business Operating System**، ومدخلها التجاري الحالي هو **Revenue + Proof + Command**.

السعودية سوق انطلاق وسياق تشغيلي مهم، وليست ادعاء `الأول سعوديًا` أو أسبقية/تفوق سوقي دون دليل مستقل.

الـNorth Star:

`CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

التحسين:

`Verified Economic Movement / Founder Minute / Cost / Risk`

القاعدة الثابتة:

**No autonomous chaos. Governed acceleration.**

سلسلة القرار:

`Signal -> Evidence -> Decision -> Approval -> Action -> Outcome -> Proof -> Learning`

وسلسلة الحقيقة التجارية:

`Real Interaction -> Qualified Problem -> Execution Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> Verified Payment -> Governed Delivery -> Customer-Validated Proof -> Expand / Stop / Redesign -> Repeatability`

> أحداث وحالات legacy تبقى فقط للتوافق مع القرّاء/runners التاريخيين، ولا تنشئ authority تجارية جديدة ولا تتغلب على السلسلة الحالية.

## Five canonical agents فقط

- `dealix-pm`
- `dealix-sales`
- `dealix-delivery`
- `dealix-engineer`
- `dealix-content`

أي specialist هو bounded workload تحت أحد هؤلاء، وليس permanent agent جديدًا.

## One Company Machine

لا يتم إنشاء CRM أو Company Brain أو Opportunity Graph أو Approval Center أو Proof Ledger أو Scheduler أو Workflow Engine أو permanent Agent Fleet موازية بلا blocker مقاس يثبت أن المالك الحالي غير كافٍ.

## ما الذي يجب أن يحميه العقد؟

1. **Relationship truth**
   - لا `relationship_verified` بدون real interaction + evidence.
   - public email/phone ≠ consent.
   - research/exhibitor/badge/CRM row ≠ relationship.

2. **Problem / qualification truth**
   - لا problem qualified بلا relationship/interaction evidence والمشكلة المحددة وصاحب القرار/الـworkflow المطلوب حسب السلطة التجارية الحالية.

3. **Diagnostic / discovery truth**
   - Free Mini Diagnostic أو Execution Diagnostic لا يتحول تلقائيًا إلى بيع أو Payment.
   - discovery completion يحتاج evidence وscope واضحين.

4. **Quote / negotiation truth**
   - Customer-Specific Quote يحتاج discovery/scope authority.
   - quote ≠ invoice ≠ payment.
   - named price/discount/payment terms/contract remain governed.

5. **Payment truth**
   - لا `pilot_payment_verified` بلا `payment_proof_ref` أو الدليل المعتمد المكافئ.
   - لا Closed Won/Verified Cash من stage marker أو proposal أو invoice draft.

6. **Delivery truth**
   - paid delivery لا يبدأ بلا start conditions المطلوبة وإثبات الدفع عندما تكون الصفقة مدفوعة.
   - activity ≠ delivery.
   - delivery ≠ customer value.

7. **Proof truth**
   - synthetic/demo/internal ≠ customer proof.
   - customer outcome يحتاج baseline + measured result + evidence + attribution caveats + customer acceptance عندما يوحي الادعاء بقيمة مؤكدة من العميل.
   - case study/public proof يحتاج publication permission.

## Approval Matrix

الأفعال الحساسة تبقى محكومة، ومنها:

- customer-facing send;
- quote/scope commitment عندما يترتب عليه التزام؛
- invoice/payment/refund/spend;
- contract/legal/exclusivity/warranty/tender;
- public publish/customer logo/testimonial/case study;
- Production deploy/config;
- DNS/material DB/secrets mutation;
- unsupported security/compliance/market-first claim.

وجود Draft أو Agent recommendation لا يمنح authority.

## Truth Firewall

- Research ≠ Relationship
- Public contact ≠ Consent
- Draft ≠ Sent
- Quote ≠ Invoice
- Invoice ≠ Payment
- Activity ≠ Delivery
- Delivery ≠ Customer Value
- Synthetic/Demo ≠ Customer Proof
- PR ≠ Production
- Historical PASS ≠ Current Exact-Head PASS
- HTTP 200 ≠ Canonical Release Identity

## WIP / investment law

أي عمل جديد يجب أن يثبت أنه يحرك واحدًا من:

- Production Trust
- Real Interaction
- Verified Cash
- Customer Proof

إذا لا، يدخل backlog بدل أن يفتح architecture جديدة.

## التحقق المطلوب

```bash
python3 scripts/verify_operating_company_commercial_state.py
python3 -m pytest -q \
  tests/unit/test_operating_company_contract.py \
  tests/unit/test_operating_company_commercial_state_contract.py
python3 -m py_compile \
  auto_client_acquisition/orchestrator/operating_company_contract.py \
  scripts/verify_operating_company_commercial_state.py
```

ثم exact-head sovereign verification عبر العقد الموجود `bin/dealix verify ...` على الـVPS. GitHub-hosted checks التي لا تبدأ repository steps ليست code acceptance.

## Execution hooks التالية

1. ربط `validate_event(...)` على كل بوابة كتابة canonical commercial events.
2. ربط Interaction Receipts بـreal interaction/relationship state فقط عند evidence.
3. جعل Targeting / Revenue / Decision / Proof outputs deterministic/versioned/evidence-bound قدر الإمكان.
4. إبقاء paid delivery وVerified Cash محميين بإثبات الدفع.
5. تسجيل violations/state promotions في Proof/Trust receipts لتظهر للرئيس تحت `MONEY / DECISIONS / RISKS / APPROVALS / NEXT_ACTION` بدل dashboard موازٍ.
