# Dealix Operating Company Contract (Governed Acceleration)

هذا المستند يربط الرؤية التشغيلية الكبرى بـ **عقد تنفيذي داخل الكود** بدلاً من بقائها كنص نظري فقط.

المرجع البرمجي:

- `auto_client_acquisition/orchestrator/operating_company_contract.py`
- `auto_client_acquisition/orchestrator/policies.py`
- `scripts/verify_operating_company_commercial_state.py`

## المعادلة التشغيلية

Dealix = Saudi-first AI Business Operating System، ومدخلها التجاري الحالي هو **Revenue + Proof + Command**.

القاعدة الثابتة:

**No autonomous chaos. Governed acceleration.**

سلسلة القرار التشغيلية العامة:

Signal → Source → Risk → Approval → Action → Evidence → Decision → Value → Asset

وسلسلة الحقيقة التجارية الحالية هي:

**Real Interaction → Verified Relationship → Qualified Problem → Free Mini Diagnostic → Qualified Discovery → Customer-Specific Quote → Pilot Decision → Verified Payment → Pilot Delivery → Proof Review → Expand / Stop**

> أحداث وحالات الـlegacy تبقى فقط للتوافق مع القرّاء/runners التاريخيين، ولا تنشئ authority تجارية جديدة ولا تتغلب على السلسلة الحالية.

## ما الذي تم ترميزه (Codified) داخل العقد؟

1. **المصانع السبعة** كنماذج تشغيلية واضحة:
   - Demand Factory
   - Trust Factory
   - Sales Factory
   - Delivery Factory
   - Proof Factory
   - Product Learning Factory
   - Governance Factory

2. **اللوبات التسعة** مع إعادة توجيه الحركة التجارية إلى العلاقة الحقيقية والدفع والإثبات، لا إلى عدد leads أو markers.

3. **Taxonomy موحّد للأحداث** يحتوي أحداث الحقيقة التجارية الحالية (`interaction_captured`, `relationship_verified`, `problem_qualified`, `diagnostic_started`, `discovery_completed`, `pilot_payment_verified`, `pilot_delivery_started`, `final_proof_pack_ready`) مع إبقاء أحداث legacy للتوافق فقط.

4. **State Machine** يحمي المسار الحالي من `research_signal` حتى `proof_review/closed_won`، مع منع القفز من research إلى relationship أو payment.

5. **قواعد لا تُكسر (Event Guards):**
   - لا `relationship_verified` بدون `interaction_captured` و`interaction_evidence_ref`.
   - لا `problem_qualified` بدون علاقة مثبتة ودليل مشكلة.
   - **Free Mini Diagnostic لا يتطلب دفعًا**؛ يبدأ بعد `problem_qualified`.
   - يمكن قبول `invoice_paid` كـlegacy prior event لقراءة السجلات التاريخية فقط، وليس كمسار authority جديد.
   - لا `discovery_completed` بدون Diagnostic مكتمل وملاحظات Discovery موثقة.
   - لا Customer-Specific Quote بدون Discovery ودليل scope.
   - لا `pilot_payment_verified` بدون `payment_proof_ref`.
   - لا `pilot_delivery_started` بدون حدث دفع مثبت + مرجع إثبات الدفع.
   - لا `closed_won` بدون دليل دفع مثبت.
   - لا `proof_pack_sent` قبل `founder_reviewed=true` في مسار legacy.
   - لا `case_study_approved` بدون `client_permission=true`.

6. **Approval Matrix قابلة للاستدعاء برمجياً:**
   - إرسال Customer-Specific Quote أو scope خارجي يبقى التزامًا تجاريًا محكومًا.
   - `start_delivery` / `start_pilot_delivery` يبقى fail-closed بدون payment proof.
   - `send_invoice` التزام مالي محكوم.
   - `security_claim` و`publish_case_study` و`final_diagnostic` تبقى خاضعة للحوكمة الحالية.
   - `agent_tool_action` يتطلب موافقة عند مخاطر متوسطة فأعلى.

## Truth Firewall

العقد لا يسمح بالترقيات التالية بلا دليل:

- Research ≠ Relationship.
- Exhibitor / badge / CRM row ≠ Relationship.
- Public email/phone ≠ Consent.
- Proposal / Quote ≠ Revenue.
- Invoice ≠ Payment.
- Demo / synthetic evidence ≠ Customer Proof.
- Closed Won يحتاج payment evidence؛ لا يُشتق من partner marker أو proposal state.

## لماذا هذا مهم؟

- يطابق العقد التنفيذي مع المسار التجاري الحالي: Free Mini Diagnostic قبل Discovery والدفع.
- يفصل Free Diagnostic عن paid Pilot Delivery.
- يمنع تضخم حالات الإيراد أو العلاقة أو التسليم بلا دليل.
- يبقي توافق السجلات القديمة بدون أن يعيد إحياء 7-day / 499 SAR / fixed-price authority.
- يجعل كل قرار قابلًا للتدقيق (audit-ready).
- يحول التشغيل اليومي إلى evidence وplaybooks قابلة للمنتجة لاحقًا.

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

ثم شغّل exact-head sovereign verification عبر العقد الموجود `bin/dealix verify ...` على الـVPS. لا تعتبر GitHub-hosted checks التي لم تبدأ steps دليل قبول للكود.

## Execution Hooks التالية

1. ربط `validate_event(...)` على كل بوابة كتابة canonical commercial events بدل الاعتماد على UI filtering.
2. ربط Big 5 / LEAP Interaction Receipts مباشرة بـ `interaction_captured` ثم `relationship_verified` فقط عند وجود evidence.
3. جعل Revenue Leak Map + Decision Pack + Executive Command outputs deterministic/versioned/evidence-bound.
4. إبقاء paid delivery وClosed Won محميين بإثبات الدفع.
5. تسجيل violations وstate promotions في Proof/Trust receipts حتى تصل للـPresident تحت RISKS/DECISIONS بدل dashboard موازٍ.
